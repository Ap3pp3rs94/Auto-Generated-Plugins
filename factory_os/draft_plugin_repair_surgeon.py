from __future__ import annotations

import ast
import re
from dataclasses import dataclass, field, replace
from pathlib import Path
from typing import Any, Literal, Optional


RecommendedRepairAction = Literal["repair", "regenerate", "quarantine"]
PatchMode = Literal["text", "ast", "marker_block", "invoke_wrapper"]
RepairRiskLevel = Literal["low", "medium", "high"]
RepairStepStatus = Literal["planned", "applied", "skipped"]


LOGIC_START = "# === LOGIC START ==="
LOGIC_END = "# === LOGIC END ==="

MULTI_PROFILE_BRANCH_IDS = (
    "plugin_spec_architect_profile",
    "plugin_logic_blueprint_designer_profile",
    "plugin_quality_gate_designer_profile",
    "plugin_test_payload_generator_profile",
    "plugin_duplicate_detector_profile",
    "plugin_repair_strategy_planner_profile",
    "plugin_release_packager_profile",
)


@dataclass(frozen=True)
class DraftPluginAnalysis:
    plugin_name: Optional[str]
    plugin_slug: Optional[str]
    logic_profile_id: Optional[str]
    has_logic_markers: bool
    has_goal_fallback_input_bug: bool
    has_payload_warning_drop_bug: bool
    has_thin_diagnostics: bool
    has_missing_input_profile_bug: bool
    has_multi_profile_branch_table: bool
    has_profile_routing_mismatch: bool
    patchable: bool
    recommended_action: RecommendedRepairAction
    has_windows_path_literal_bug: bool = False
    has_patchable_windows_temp_path_bug: bool = False
    has_windows_shell_command_bug: bool = False
    has_windows_subprocess_shell_bug: bool = False


@dataclass(frozen=True)
class RepairStep:
    patch_id: str
    target: str
    description: str
    severity: str
    patch_mode: PatchMode
    status: RepairStepStatus = "planned"


@dataclass(frozen=True)
class RepairPlan:
    plugin_slug: Optional[str]
    repair_steps: list[RepairStep] = field(default_factory=list)
    risk_level: RepairRiskLevel = "low"
    expected_fixed_findings: list[str] = field(default_factory=list)
    must_retest: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class RepairResult:
    original_source: str
    patched_source: str
    applied_patches: list[str] = field(default_factory=list)
    skipped_patches: list[str] = field(default_factory=list)
    remaining_findings: list[str] = field(default_factory=list)
    repair_recipe: dict[str, Any] = field(default_factory=dict)
    recommended_next_action: Literal["retest", "regenerate", "quarantine"] = "retest"


@dataclass(frozen=True)
class PluginFileRepairReport:
    path: str
    plugin_slug: Optional[str]
    changed: bool
    applied_patches: list[str] = field(default_factory=list)
    skipped_patches: list[str] = field(default_factory=list)
    remaining_findings: list[str] = field(default_factory=list)
    recommended_next_action: Literal["retest", "regenerate", "quarantine"] = "retest"
    validation_error: Optional[str] = None
    repair_recipe: dict[str, Any] = field(default_factory=dict)


def _literal_module_constants(source: str) -> dict[str, Any]:
    try:
        tree = ast.parse(source)
    except SyntaxError:
        return {}
    constants: dict[str, Any] = {}
    for node in tree.body:
        target_name: Optional[str] = None
        value: Optional[ast.AST] = None
        if isinstance(node, ast.Assign) and node.targets and isinstance(node.targets[0], ast.Name):
            target_name = node.targets[0].id
            value = node.value
        elif isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name):
            target_name = node.target.id
            value = node.value
        if target_name in {"_PLUGIN_NAME", "_PLUGIN_SLUG"} and value is not None:
            try:
                constants[target_name] = ast.literal_eval(value)
            except Exception:
                constants[target_name] = None
    return constants


def _first_string_assignment(source: str, name: str) -> Optional[str]:
    pattern = re.compile(rf"^\s*{re.escape(name)}\s*=\s*(['\"])(?P<value>.+?)\1", re.MULTILINE)
    match = pattern.search(source)
    return match.group("value") if match else None


def _logic_region(source: str) -> Optional[tuple[int, int, str]]:
    start = source.find(LOGIC_START)
    end = source.find(LOGIC_END)
    if start < 0 or end < 0 or end <= start:
        return None
    body_start = source.find("\n", start)
    if body_start < 0:
        body_start = start + len(LOGIC_START)
    else:
        body_start += 1
    return body_start, end, source[body_start:end]


def _has_goal_fallback_input_bug(source: str) -> bool:
    patterns = (
        r"def_text\s*=\s*str\([^)\n]*(?:payload_data\.get\(['\"]prompt['\"]\)|explicit_objective_text|task_text)[^)\n]*\bor\s+goal\)\.strip\(\)",
        r"objective_text\s*=\s*str\([^)\n]*explicit_objective_text\s+or\s+goal\)\.strip\(\)",
    )
    return any(re.search(pattern, source) for pattern in patterns)


def _has_payload_warning_drop_bug(source: str) -> bool:
    return bool(re.search(r"payload_warnings\s*=\s*\[\]\s+if\s+isinstance\(payload,\s*dict\)\s+else", source))


def _has_thin_diagnostics(source: str) -> bool:
    if "diagnostics" not in source:
        return True
    thin_patterns = (
        r"result\[['\"]diagnostics['\"]\]\s*=\s*\{\s*['\"]logic_profile_id['\"]\s*:\s*logic_profile_id\s*\}",
        r"diagnostics\s*=\s*\{\s*['\"]logic_profile_id['\"]\s*:\s*logic_profile_id\s*\}",
    )
    return any(re.search(pattern, source, flags=re.DOTALL) for pattern in thin_patterns)


def _has_missing_input_profile_bug(source: str) -> bool:
    if "profile_missing_inputs" in source:
        return False
    required_profile_markers = {
        "task_planner_profile",
        "prompt_refinement_profile",
        "prompt_test_case_generator_profile",
        "retrieval_query_expander_profile",
        "output_quality_scorer_profile",
        "context_window_optimizer_profile",
        "memory_compression_profile",
        "tool_selection_profile",
        "multi_agent_handoff_profile",
    }
    if not any(marker in source for marker in required_profile_markers):
        return False
    return "missing_inputs" not in source or "if not def_text" in source or "not has_user_input" not in source


def _has_multi_profile_branch_table(source: str) -> bool:
    found = [profile_id for profile_id in MULTI_PROFILE_BRANCH_IDS if profile_id in source]
    return len(found) >= 3


def _has_profile_routing_mismatch(source: str) -> bool:
    if "continuous_capability_overlap_checker_profile" not in source:
        return False
    duplicate_branch = re.search(
        r"(?:if|elif)\s+logic_profile_id\s*==\s*['\"]plugin_duplicate_detector_profile['\"]",
        source,
    )
    canonical_branch = re.search(
        r"(?:if|elif)\s+logic_profile_id\s*(?:==|in)\s*.+capability_overlap_checker_profile",
        source,
    )
    return bool(duplicate_branch and not canonical_branch)


def _has_windows_path_literal_bug(source: str) -> bool:
    absolute_posix_path = re.search(
        r"(?P<quote>['\"])/(?:tmp|home|mnt|var|etc)(?:/[^'\"]*)?(?P=quote)",
        source,
    )
    path_constructor = re.search(
        r"\bPath\(\s*(?P<quote>['\"])/(?:tmp|home|mnt|var|etc)(?:/[^'\"]*)?(?P=quote)\s*\)",
        source,
    )
    return bool(absolute_posix_path or path_constructor or "\\\\wsl$" in source.lower())


def _has_patchable_windows_temp_path_bug(source: str) -> bool:
    return bool(
        re.search(r"\bPath\(\s*(['\"])/tmp(?:/[^'\"]*)?\1\s*\)", source)
        or re.search(r"\bopen\(\s*(['\"])/tmp/[^'\"]*\1", source)
    )


def _has_windows_shell_command_bug(source: str) -> bool:
    if "os.system(" in source:
        return True
    subprocess_call = re.search(
        r"subprocess\.(?:run|check_call|check_output|Popen)\(\s*(?P<quote>['\"])(?P<cmd>.*?)(?P=quote)",
        source,
        flags=re.DOTALL,
    )
    if not subprocess_call:
        return False
    command = subprocess_call.group("cmd").lower()
    shell_only_markers = ("&&", "||", "sh -c", "bash", "rm -rf", " cp ", " mv ")
    return any(marker in command for marker in shell_only_markers)


def _has_windows_subprocess_shell_bug(source: str) -> bool:
    return bool(re.search(r"subprocess\.(?:run|check_call|check_output|Popen)\([^)]*shell\s*=\s*True", source, flags=re.DOTALL))


def analyze_draft_plugin(source: str, *, plugin_path: str | None = None) -> DraftPluginAnalysis:
    constants = _literal_module_constants(source)
    plugin_name = constants.get("_PLUGIN_NAME")
    plugin_slug = constants.get("_PLUGIN_SLUG")
    logic_profile_id = _first_string_assignment(source, "logic_profile_id")
    has_logic_markers = LOGIC_START in source and LOGIC_END in source
    has_goal_bug = _has_goal_fallback_input_bug(source)
    has_warning_bug = _has_payload_warning_drop_bug(source) or (
        "if not isinstance(payload, dict):" in source and "_payload_warnings" not in source
    )
    has_thin_diagnostics = _has_thin_diagnostics(source)
    has_missing_input_bug = _has_missing_input_profile_bug(source)
    has_multi_profile_table = _has_multi_profile_branch_table(source)
    has_routing_mismatch = _has_profile_routing_mismatch(source)
    has_windows_path_bug = _has_windows_path_literal_bug(source)
    has_patchable_windows_temp_bug = _has_patchable_windows_temp_path_bug(source)
    has_windows_shell_bug = _has_windows_shell_command_bug(source)
    has_windows_subprocess_shell_bug = _has_windows_subprocess_shell_bug(source)

    patchable_findings = any(
        [
            has_goal_bug,
            has_warning_bug,
            has_thin_diagnostics,
            has_missing_input_bug,
            has_routing_mismatch,
            has_patchable_windows_temp_bug,
        ]
    )
    has_nonpatchable_windows_risk = (
        has_windows_shell_bug
        or has_windows_subprocess_shell_bug
        or (has_windows_path_bug and not has_patchable_windows_temp_bug)
    )
    patchable = has_logic_markers and patchable_findings and not has_multi_profile_table and not has_nonpatchable_windows_risk
    if not has_logic_markers:
        recommended_action: RecommendedRepairAction = "quarantine"
    elif has_multi_profile_table:
        recommended_action = "regenerate"
    elif has_nonpatchable_windows_risk:
        recommended_action = "regenerate"
    elif patchable_findings:
        recommended_action = "repair"
    else:
        recommended_action = "repair"

    return DraftPluginAnalysis(
        plugin_name=plugin_name if isinstance(plugin_name, str) else None,
        plugin_slug=plugin_slug if isinstance(plugin_slug, str) else plugin_path,
        logic_profile_id=logic_profile_id,
        has_logic_markers=has_logic_markers,
        has_goal_fallback_input_bug=has_goal_bug,
        has_payload_warning_drop_bug=has_warning_bug,
        has_thin_diagnostics=has_thin_diagnostics,
        has_missing_input_profile_bug=has_missing_input_bug,
        has_multi_profile_branch_table=has_multi_profile_table,
        has_profile_routing_mismatch=has_routing_mismatch,
        patchable=patchable,
        recommended_action=recommended_action,
        has_windows_path_literal_bug=has_windows_path_bug,
        has_patchable_windows_temp_path_bug=has_patchable_windows_temp_bug,
        has_windows_shell_command_bug=has_windows_shell_bug,
        has_windows_subprocess_shell_bug=has_windows_subprocess_shell_bug,
    )


def _semantic_findings_request_routing_patch(semantic_findings: list[dict] | None) -> bool:
    if not semantic_findings:
        return False
    text = " ".join(str(item.get("code", "")) + " " + str(item.get("message", "")) for item in semantic_findings).lower()
    return "routing" in text or "alias" in text or "overlap" in text or "profile" in text


def plan_repairs(
    analysis: DraftPluginAnalysis,
    semantic_findings: list[dict] | None = None,
    capability_spec: dict | None = None,
) -> RepairPlan:
    steps: list[RepairStep] = []
    expected: list[str] = []
    risk: RepairRiskLevel = "low"

    if not analysis.has_logic_markers:
        return RepairPlan(
            plugin_slug=analysis.plugin_slug,
            repair_steps=[],
            risk_level="high",
            expected_fixed_findings=[],
            must_retest=["manual_inspection"],
        )

    allow_routing_patch = _semantic_findings_request_routing_patch(semantic_findings)
    if analysis.has_multi_profile_branch_table and not allow_routing_patch:
        return RepairPlan(
            plugin_slug=analysis.plugin_slug,
            repair_steps=[],
            risk_level="high",
            expected_fixed_findings=["multi_profile_branch_table"],
            must_retest=["regenerate_with_profile_dispatcher"],
        )
    if (
        analysis.has_windows_shell_command_bug
        or analysis.has_windows_subprocess_shell_bug
        or (analysis.has_windows_path_literal_bug and not analysis.has_patchable_windows_temp_path_bug)
    ):
        expected.extend(
            finding
            for finding, present in [
                ("windows_path_literal_bug", analysis.has_windows_path_literal_bug),
                ("windows_shell_command_bug", analysis.has_windows_shell_command_bug),
                ("windows_subprocess_shell_bug", analysis.has_windows_subprocess_shell_bug),
            ]
            if present
        )
        return RepairPlan(
            plugin_slug=analysis.plugin_slug,
            repair_steps=[],
            risk_level="high",
            expected_fixed_findings=list(dict.fromkeys(expected)),
            must_retest=["regenerate_for_windows_portability"],
        )

    if analysis.has_goal_fallback_input_bug:
        steps.append(
            RepairStep(
                patch_id="repair_goal_fallback_input_detection",
                target="logic_region",
                description="Separate real user input detection from display fallback to plugin goal.",
                severity="blocker",
                patch_mode="text",
            )
        )
        expected.append("goal_fallback_input_bug")
    if analysis.has_payload_warning_drop_bug:
        steps.append(
            RepairStep(
                patch_id="preserve_payload_warnings",
                target="logic_region_and_invoke",
                description="Keep invoke-wrapped non-dict payload warnings in details.payload_warnings.",
                severity="error",
                patch_mode="invoke_wrapper",
            )
        )
        expected.append("payload_warning_drop_bug")
    if analysis.has_thin_diagnostics or analysis.has_missing_input_profile_bug or analysis.has_goal_fallback_input_bug:
        steps.append(
            RepairStep(
                patch_id="add_profile_missing_input_and_diagnostics_finalizer",
                target="logic_region",
                description="Add profile-specific missing input checks, diagnostics, usefulness, and fun-mode compatibility.",
                severity="error",
                patch_mode="marker_block",
            )
        )
        expected.extend(["thin_diagnostics", "missing_input_profile_bug"])
    if analysis.has_profile_routing_mismatch and allow_routing_patch:
        steps.append(
            RepairStep(
                patch_id="patch_overlap_profile_alias_routing",
                target="logic_region",
                description="Route overlap-checker aliases to the same duplicate/overlap logic branch.",
                severity="blocker",
                patch_mode="text",
            )
        )
        risk = "medium"
        expected.append("profile_routing_mismatch")
    elif analysis.has_multi_profile_branch_table:
        risk = "high"
    if analysis.has_patchable_windows_temp_path_bug:
        steps.append(
            RepairStep(
                patch_id="normalize_patchable_posix_temp_paths",
                target="source",
                description="Replace simple /tmp Path/open literals with pathlib/tempfile expressions that work on Windows.",
                severity="warning",
                patch_mode="text",
            )
        )
        expected.append("windows_path_literal_bug")
    if analysis.has_windows_shell_command_bug or analysis.has_windows_subprocess_shell_bug:
        risk = "high"
        expected.extend(["windows_shell_command_bug", "windows_subprocess_shell_bug"])
    elif analysis.has_windows_path_literal_bug and not analysis.has_patchable_windows_temp_path_bug:
        risk = "high"
        expected.append("windows_path_literal_bug")

    return RepairPlan(
        plugin_slug=analysis.plugin_slug,
        repair_steps=steps,
        risk_level=risk,
        expected_fixed_findings=list(dict.fromkeys(expected)),
        must_retest=["import", "invoke_empty_payload", "invoke_non_dict_payload", "station_c_validation"],
    )


def _patch_goal_fallback(source: str) -> tuple[str, bool]:
    patched = source
    user_input_lines = (
        "_repair_input_keys = ['task', 'objective', 'prompt', 'instruction', 'query', 'question', 'response', 'answer', 'description']\n"
        "_repair_sequence_keys = ['messages', 'source_notes', 'candidate_outputs', 'trace', 'completed_steps', 'previous_results']\n"
        "_repair_input_values = []\n"
        "for _repair_key in _repair_input_keys:\n"
        "    _repair_value = payload_data.get(_repair_key) if isinstance(payload_data, dict) else None\n"
        "    if _repair_value not in (None, '', [], {}):\n"
        "        _repair_input_values.append(_repair_value)\n"
        "for _repair_key in _repair_sequence_keys:\n"
        "    _repair_value = payload_data.get(_repair_key) if isinstance(payload_data, dict) else None\n"
        "    if _repair_value not in (None, '', [], {}):\n"
        "        _repair_input_values.append(_repair_value)\n"
        "has_user_input = bool(_repair_input_values)\n"
        "input_signal_count = len(_repair_input_values)\n"
        "user_target_text = str(next((value for value in _repair_input_values if isinstance(value, str) and value.strip()), '')).strip()\n"
        "display_target = user_target_text or str(goal).strip()\n"
        "used_goal_fallback = not bool(user_target_text)\n"
        "def_text = display_target"
    )
    def_pattern = re.compile(
        r"(?m)^(?P<indent>\s*)def_text\s*=\s*str\([^)\n]*(?:payload_data\.get\(['\"]prompt['\"]\)|explicit_objective_text|task_text)[^)\n]*\bor\s+goal\)\.strip\(\)"
    )
    def replace_def(match: re.Match[str]) -> str:
        indent = match.group("indent")
        return "\n".join(indent + line for line in user_input_lines.splitlines())

    patched, def_count = def_pattern.subn(replace_def, patched, count=1)
    obj_pattern = re.compile(
        r"(?m)^(?P<indent>\s*)objective_text\s*=\s*str\([^)\n]*explicit_objective_text\s+or\s+goal\)\.strip\(\)"
    )
    patched, obj_count = obj_pattern.subn(
        lambda match: match.group("indent") + "objective_text = str(explicit_objective_text or user_target_text or '').strip()",
        patched,
        count=1,
    )
    return patched, bool(def_count or obj_count)


def _patch_payload_warnings(source: str) -> tuple[str, bool]:
    patched = source
    changed = False
    warning_pattern = re.compile(r"payload_warnings\s*=\s*\[\]\s+if\s+isinstance\(payload,\s*dict\)\s+else\s+[^\n]+")
    patched, count = warning_pattern.subn(
        "payload_warnings = list(payload_data.get('_payload_warnings', [])) if isinstance(payload_data, dict) else []",
        patched,
    )
    changed = changed or bool(count)

    invoke_pattern = re.compile(
        r"(?P<indent>\s*)if not isinstance\(payload,\s*dict\):\n(?P=indent)\s+payload\s*=\s*\{\s*['\"]_value['\"]\s*:\s*payload\s*\}",
    )

    def replace_invoke(match: re.Match[str]) -> str:
        indent = match.group("indent")
        return (
            f"{indent}if not isinstance(payload, dict):\n"
            f"{indent}    payload = {{\n"
            f"{indent}        '_value': payload,\n"
            f"{indent}        '_payload_warnings': ['payload was not a dict; invoke wrapped it in _value'],\n"
            f"{indent}    }}"
        )

    patched, count = invoke_pattern.subn(replace_invoke, patched, count=1)
    changed = changed or bool(count)
    return patched, changed


def _repair_finalizer_block(indent: str) -> str:
    body = r"""
# AI Draft Plugin Repair Surgeon finalizer.
try:
    details = result.get('details') if isinstance(result.get('details'), dict) else {}
    scores = result.get('scores') if isinstance(result.get('scores'), dict) else {}
    progress_state = result.get('progress_state') if isinstance(result.get('progress_state'), dict) else {}
    user_experience = result.get('user_experience') if isinstance(result.get('user_experience'), dict) else {}
    fun_mode = result.get('fun_mode') if isinstance(result.get('fun_mode'), dict) else {}
    payload_data = payload if isinstance(payload, dict) else {}
    payload_warnings = list(payload_data.get('_payload_warnings', [])) if isinstance(payload_data, dict) else []
    try:
        _repair_has_user_input = bool(has_user_input)
    except NameError:
        _repair_input_values = []
        for _repair_key in ['task', 'objective', 'prompt', 'instruction', 'query', 'question', 'response', 'answer', 'description']:
            _repair_value = payload_data.get(_repair_key)
            if _repair_value not in (None, '', [], {}):
                _repair_input_values.append(_repair_value)
        for _repair_key in ['messages', 'source_notes', 'candidate_outputs', 'trace', 'completed_steps', 'previous_results']:
            _repair_value = payload_data.get(_repair_key)
            if _repair_value not in (None, '', [], {}):
                _repair_input_values.append(_repair_value)
        _repair_has_user_input = bool(_repair_input_values)
        input_signal_count = len(_repair_input_values)
        used_goal_fallback = not _repair_has_user_input
    try:
        _repair_input_signal_count = int(input_signal_count)
    except Exception:
        _repair_input_signal_count = 1 if _repair_has_user_input else 0
    try:
        _repair_used_goal_fallback = bool(used_goal_fallback)
    except NameError:
        _repair_used_goal_fallback = not _repair_has_user_input
    _repair_profile_id = str(details.get('logic_profile_id') or locals().get('logic_profile_id') or '')
    def _repair_present(key):
        value = payload_data.get(key) if isinstance(payload_data, dict) else None
        return value not in (None, '', [], {})
    profile_missing_inputs = []
    if not _repair_has_user_input:
        profile_missing_inputs.append('user-provided payload values')
    if _repair_profile_id == 'prompt_refinement_profile':
        if not (_repair_present('prompt') or _repair_present('instruction')):
            profile_missing_inputs.append('prompt or instruction')
    elif _repair_profile_id == 'prompt_test_case_generator_profile':
        if not _repair_present('prompt'):
            profile_missing_inputs.append('prompt')
        if not (_repair_present('expected_behavior') or _repair_present('objective')):
            profile_missing_inputs.append('expected_behavior or objective')
    elif _repair_profile_id == 'retrieval_query_expander_profile':
        if not any(_repair_present(key) for key in ['task', 'query', 'question', 'objective']):
            profile_missing_inputs.append('task, query, question, or objective')
    elif _repair_profile_id == 'output_quality_scorer_profile':
        if not any(_repair_present(key) for key in ['response', 'answer', 'candidate_outputs']):
            profile_missing_inputs.append('response, answer, or candidate_outputs')
    elif _repair_profile_id == 'context_window_optimizer_profile':
        if not any(_repair_present(key) for key in ['messages', 'source_notes', 'candidate_outputs', 'current_plan', 'completed_steps', 'blocked_steps', 'previous_results', 'trace', 'rubric', 'constraints']):
            profile_missing_inputs.append('context items')
    elif _repair_profile_id == 'memory_compression_profile':
        if not any(_repair_present(key) for key in ['messages', 'source_notes', 'previous_results', 'trace', 'completed_steps']):
            profile_missing_inputs.append('messages, source_notes, previous_results, trace, or completed_steps')
    elif _repair_profile_id == 'tool_selection_profile':
        if not (_repair_present('task') or _repair_present('objective')):
            profile_missing_inputs.append('task or objective')
    elif _repair_profile_id == 'task_planner_profile':
        if not (_repair_present('task') or _repair_present('objective')):
            profile_missing_inputs.append('task or objective')
    elif _repair_profile_id == 'multi_agent_handoff_profile':
        if not _repair_present('objective'):
            profile_missing_inputs.append('objective')
        if not any(_repair_present(key) for key in ['agents', 'workstreams', 'ownership_scopes']):
            profile_missing_inputs.append('agents, workstreams, or ownership_scopes')
    missing_inputs = details.get('missing_inputs')
    if not isinstance(missing_inputs, list):
        missing_inputs = []
    for item in profile_missing_inputs:
        if item not in missing_inputs:
            missing_inputs.append(item)
    details['missing_inputs'] = missing_inputs
    details['payload_warnings'] = payload_warnings
    if _repair_profile_id:
        details.setdefault('logic_profile_id', _repair_profile_id)
    if missing_inputs:
        progress_state['blockers'] = list(dict.fromkeys(list(progress_state.get('blockers') or []) + missing_inputs))
        progress_state.setdefault('current_stage', _repair_profile_id or 'repair_missing_inputs')
        progress_state.setdefault('next_step', 'Provide required input before using this capability.')
    scores.setdefault('usefulness', 0.45 if missing_inputs else max(0.65, float(scores.get('confidence', 0.65) or 0.65)))
    diagnostics = result.get('diagnostics') if isinstance(result.get('diagnostics'), dict) else {}
    diagnostics.update({
        'logic_profile_id': _repair_profile_id,
        'has_user_input': _repair_has_user_input,
        'used_goal_fallback': _repair_used_goal_fallback,
        'input_signal_count': _repair_input_signal_count,
        'missing_inputs_count': len(missing_inputs),
        'payload_warning_count': len(payload_warnings),
        'profile_output_keys': sorted(details.keys()),
        'semantic_probe_ready': bool(_repair_has_user_input and not missing_inputs),
    })
    fun_mode.setdefault('celebratory_microcopy', fun_mode.get('microcopy', 'Capability repair completed.'))
    fun_mode.setdefault('microcopy', fun_mode.get('celebratory_microcopy', 'Capability repair completed.'))
    user_experience.setdefault('plain_language_takeaway', result.get('summary', 'Capability repaired.'))
    result['details'] = details
    result['scores'] = scores
    result['progress_state'] = progress_state
    result['user_experience'] = user_experience
    result['fun_mode'] = fun_mode
    result['diagnostics'] = diagnostics
except Exception as _repair_exc:
    if isinstance(result, dict):
        result.setdefault('details', {})['repair_surgeon_error'] = str(_repair_exc)
"""
    return "\n".join(indent + line if line else line for line in body.strip("\n").splitlines())


def _patch_finalizer(source: str) -> tuple[str, bool]:
    region = _logic_region(source)
    if region is None:
        return source, False
    body_start, body_end, body = region
    if "AI Draft Plugin Repair Surgeon finalizer" in body:
        return source, False
    matches = list(re.finditer(r"(?m)^(?P<indent>\s*)return\s+result\s*$", body))
    if not matches:
        return source, False
    match = matches[-1]
    indent = match.group("indent")
    finalizer = _repair_finalizer_block(indent)
    patched_body = body[: match.start()] + finalizer + "\n" + body[match.start() :]
    return source[:body_start] + patched_body + source[body_end:], True


def _patch_overlap_alias(source: str) -> tuple[str, bool]:
    pattern = re.compile(
        r"(?P<prefix>(?:if|elif)\s+)logic_profile_id\s*==\s*(['\"])plugin_duplicate_detector_profile\2\s*:",
    )

    def replace(match: re.Match[str]) -> str:
        return (
            f"{match.group('prefix')}logic_profile_id in "
            "{'plugin_duplicate_detector_profile', 'continuous_capability_overlap_checker_profile', "
            "'capability_overlap_checker_profile', 'ai_capability_overlap_checker'}:"
        )

    patched, count = pattern.subn(replace, source, count=1)
    return patched, bool(count)


def _ensure_import(source: str, import_line: str) -> str:
    if re.search(rf"^\s*{re.escape(import_line)}\s*$", source, flags=re.MULTILINE):
        return source
    lines = source.splitlines(keepends=True)
    insert_at = 0
    if lines and lines[0].startswith("#!"):
        insert_at = 1
    for index, line in enumerate(lines):
        if line.startswith("from __future__ import"):
            insert_at = index + 1
            break
    lines.insert(insert_at, import_line + "\n")
    return "".join(lines)


def _temp_path_expr(relative_path: str) -> str:
    normalized = relative_path.strip("/")
    if not normalized:
        return "Path(tempfile.gettempdir())"
    return f"Path(tempfile.gettempdir()) / {normalized!r}"


def _patch_patchable_posix_temp_paths(source: str) -> tuple[str, bool]:
    patched = source

    def replace_path(match: re.Match[str]) -> str:
        return "(" + _temp_path_expr(match.group("relative_path")) + ")"

    patched, path_count = re.subn(
        r"\bPath\(\s*(['\"])/tmp(?:/(?P<relative_path>[^'\"]*))?\1\s*\)",
        replace_path,
        patched,
    )

    def replace_open(match: re.Match[str]) -> str:
        return "open(" + _temp_path_expr(match.group("relative_path"))

    patched, open_count = re.subn(
        r"\bopen\(\s*(['\"])/tmp/(?P<relative_path>[^'\"]*)\1",
        replace_open,
        patched,
    )
    changed = bool(path_count or open_count)
    if changed:
        patched = _ensure_import(patched, "from pathlib import Path")
        patched = _ensure_import(patched, "import tempfile")
    return patched, changed


def apply_repair_plan(source: str, repair_plan: RepairPlan) -> RepairResult:
    patched = source
    applied: list[str] = []
    skipped: list[str] = []
    for step in repair_plan.repair_steps:
        before = patched
        changed = False
        if step.patch_id == "repair_goal_fallback_input_detection":
            patched, changed = _patch_goal_fallback(patched)
        elif step.patch_id == "preserve_payload_warnings":
            patched, changed = _patch_payload_warnings(patched)
        elif step.patch_id == "add_profile_missing_input_and_diagnostics_finalizer":
            patched, changed = _patch_finalizer(patched)
        elif step.patch_id == "patch_overlap_profile_alias_routing":
            patched, changed = _patch_overlap_alias(patched)
        elif step.patch_id == "normalize_patchable_posix_temp_paths":
            patched, changed = _patch_patchable_posix_temp_paths(patched)
        if changed and patched != before:
            applied.append(step.patch_id)
        else:
            skipped.append(step.patch_id)

    remaining_analysis = analyze_draft_plugin(patched, plugin_path=repair_plan.plugin_slug)
    remaining_findings: list[str] = []
    if remaining_analysis.has_goal_fallback_input_bug:
        remaining_findings.append("goal_fallback_input_bug")
    if remaining_analysis.has_payload_warning_drop_bug:
        remaining_findings.append("payload_warning_drop_bug")
    if remaining_analysis.has_thin_diagnostics:
        remaining_findings.append("thin_diagnostics")
    if remaining_analysis.has_multi_profile_branch_table:
        remaining_findings.append("multi_profile_branch_table")
    if remaining_analysis.has_profile_routing_mismatch:
        remaining_findings.append("profile_routing_mismatch")
    if remaining_analysis.has_windows_path_literal_bug:
        remaining_findings.append("windows_path_literal_bug")
    if remaining_analysis.has_windows_shell_command_bug:
        remaining_findings.append("windows_shell_command_bug")
    if remaining_analysis.has_windows_subprocess_shell_bug:
        remaining_findings.append("windows_subprocess_shell_bug")

    if repair_plan.risk_level == "high" and not applied:
        next_action: Literal["retest", "regenerate", "quarantine"] = "regenerate"
    elif remaining_analysis.recommended_action == "quarantine":
        next_action = "quarantine"
    elif remaining_findings and "multi_profile_branch_table" in remaining_findings:
        next_action = "regenerate"
    else:
        next_action = "retest"

    recipe = {
        "plugin_slug": repair_plan.plugin_slug,
        "risk_level": repair_plan.risk_level,
        "applied_patches": applied,
        "skipped_patches": skipped,
        "expected_fixed_findings": repair_plan.expected_fixed_findings,
        "must_retest": repair_plan.must_retest,
        "generator_feedback": [
            "separate user input detection from display fallback",
            "read payload_data['_payload_warnings'] after invoke wraps non-dict payloads",
            "emit rich diagnostics with semantic input fields",
            "apply profile-specific missing-input rules before promotion",
            "use pathlib.Path/tempfile for filesystem paths that must work on Windows",
            "avoid shell=True and shell-specific command separators in generated plugin logic",
        ],
    }

    return RepairResult(
        original_source=source,
        patched_source=patched,
        applied_patches=applied,
        skipped_patches=skipped,
        remaining_findings=remaining_findings,
        repair_recipe=recipe,
        recommended_next_action=next_action,
    )


def repair_draft_plugin(
    source: str,
    *,
    plugin_path: str | None = None,
    semantic_findings: list[dict] | None = None,
    capability_spec: dict | None = None,
) -> RepairResult:
    analysis = analyze_draft_plugin(source, plugin_path=plugin_path)
    plan = plan_repairs(analysis, semantic_findings=semantic_findings, capability_spec=capability_spec)
    return apply_repair_plan(source, plan)


def _compile_error(source: str, *, filename: str) -> Optional[str]:
    try:
        compile(source, filename, "exec")
    except SyntaxError as exc:
        return f"{type(exc).__name__}: {exc}"
    return None


def analyze_plugin_file(path: str | Path) -> DraftPluginAnalysis:
    path_obj = Path(path)
    source = path_obj.read_text(encoding="utf-8")
    return analyze_draft_plugin(source, plugin_path=str(path_obj))


def repair_plugin_file(
    path: str | Path,
    *,
    dry_run: bool = True,
    semantic_findings: list[dict] | None = None,
    capability_spec: dict | None = None,
    validate: bool = True,
) -> RepairResult:
    path_obj = Path(path)
    source = path_obj.read_text(encoding="utf-8")
    result = repair_draft_plugin(
        source,
        plugin_path=str(path_obj),
        semantic_findings=semantic_findings,
        capability_spec=capability_spec,
    )
    validation_error = _compile_error(result.patched_source, filename=str(path_obj)) if validate else None
    if validation_error:
        result = replace(
            result,
            remaining_findings=list(dict.fromkeys(result.remaining_findings + [f"compile_error: {validation_error}"])),
            recommended_next_action="quarantine",
        )
    changed = result.patched_source != source
    if changed and not dry_run and result.recommended_next_action == "retest":
        path_obj.write_text(result.patched_source, encoding="utf-8", newline="\n")
    return result


def repair_plugin_tree(
    plugin_dir: str | Path,
    *,
    dry_run: bool = True,
    validate: bool = True,
    max_files: int | None = None,
) -> list[PluginFileRepairReport]:
    root = Path(plugin_dir)
    paths = sorted(path for path in root.rglob("*.py") if "__pycache__" not in path.parts)
    if max_files is not None:
        paths = paths[:max_files]
    reports: list[PluginFileRepairReport] = []
    for path in paths:
        result = repair_plugin_file(path, dry_run=dry_run, validate=validate)
        validation_error = None
        for finding in result.remaining_findings:
            if finding.startswith("compile_error: "):
                validation_error = finding.removeprefix("compile_error: ")
                break
        reports.append(
            PluginFileRepairReport(
                path=str(path),
                plugin_slug=analyze_draft_plugin(result.patched_source, plugin_path=str(path)).plugin_slug,
                changed=result.patched_source != result.original_source and result.recommended_next_action == "retest",
                applied_patches=result.applied_patches,
                skipped_patches=result.skipped_patches,
                remaining_findings=result.remaining_findings,
                recommended_next_action=result.recommended_next_action,
                validation_error=validation_error,
                repair_recipe=result.repair_recipe,
            )
        )
    return reports
