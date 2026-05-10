from __future__ import annotations

"""
Auto-generated Francis AI capability module.

THIS FILE IS GENERATED. Manual edits may be overwritten by the factory.

Capability: AI Tool Call Sequence Builder 000021
Slug: ai_tool_call_sequence_builder
"""

from typing import Any, Dict, Optional

__all__ = ["invoke", "_run_core_logic", "SkillContext"]

_PLUGIN_NAME: str = 'AI Tool Call Sequence Builder 000021'
_PLUGIN_SLUG: str = 'ai_tool_call_sequence_builder'
_PLUGIN_CATEGORY: str = 'ai_agents'
_PLUGIN_VERSION: str = '0.1.0'
_PLUGIN_GOAL: str = 'Plan a safe order of tool calls for multi-step AI workflows.'
_PLUGIN_TAGS = ['ai', 'tools', 'sequence', 'orchestration', 'autonomous_factory', 'ai_progress']
_PLUGIN_OWNER_ID = 'francis-factory'
_PLUGIN_CAPABILITY_TYPE = 'integration'
_PLUGIN_INTENDED_DOMAIN = 'AI tool sequencing and orchestration'
_PLUGIN_USE_CASES = ['Choose which tool should run first, second, and last.', 'Flag tool calls that need approval or verification first.', 'Explain when no external tool call is needed.', 'Show a compact progress state for this AI capability during baseline capability.', 'Return user-facing guidance that is useful, concise, and safe to act on.', 'Avoid duplicating existing AI capability behavior; identify what is unique about this capability.']
_PLUGIN_RESULT_SCHEMA_VERSION: str = "1.0.0"
_PLUGIN_MANIFEST = {'name': 'AI Tool Call Sequence Builder 000021', 'slug': 'ai_tool_call_sequence_builder', 'goal': 'Plan a safe order of tool calls for multi-step AI workflows.', 'category': 'ai_agents', 'tags': ['ai', 'tools', 'sequence', 'orchestration', 'autonomous_factory', 'ai_progress'], 'version': '0.1.0', 'capability_type': 'integration', 'intended_domain': 'AI tool sequencing and orchestration', 'owner_id': 'francis-factory', 'use_cases': ['Choose which tool should run first, second, and last.', 'Flag tool calls that need approval or verification first.', 'Explain when no external tool call is needed.', 'Show a compact progress state for this AI capability during baseline capability.', 'Return user-facing guidance that is useful, concise, and safe to act on.', 'Avoid duplicating existing AI capability behavior; identify what is unique about this capability.'], 'schema_version': '1.0.0'}
_PLUGIN_DEFAULT_CONFIG: Dict[str, Any] = {}

try:
    from learning_manager import load_plugin_profile as _load_plugin_profile  # type: ignore
except (ImportError, ModuleNotFoundError):
    _load_plugin_profile = None  # type: ignore[assignment]


class SkillContext:
    def __init__(
        self,
        *,
        user_id: str,
        run_id: Optional[str],
        plugin_slug: str,
        plugin_name: str,
        learning_profile: Optional[Dict[str, Any]] = None,
        logger: Optional[Any] = None,
        brain: Optional[Any] = None,
    ) -> None:
        self.user_id = user_id
        self.run_id = run_id
        self.plugin_slug = plugin_slug
        self.plugin_name = plugin_name
        self.learning_profile: Dict[str, Any] = learning_profile or {}
        self.logger = logger
        self.brain = brain

    def _log(self, level: str, message: str, **fields: Any) -> None:
        if self.logger is None:
            return
        try:
            log_fn = getattr(self.logger, level, None)
            if callable(log_fn):
                payload = {"message": message, "plugin_slug": self.plugin_slug, "plugin_name": self.plugin_name}
                payload.update(fields)
                log_fn(payload)
        except Exception:
            return

    def log_info(self, message: str, **fields: Any) -> None:
        self._log("info", message, **fields)

    def log_error(self, message: str, **fields: Any) -> None:
        self._log("error", message, **fields)


def _build_effective_config(payload: Dict[str, Any], runtime_config: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    cfg: Dict[str, Any] = dict(_PLUGIN_DEFAULT_CONFIG)
    if isinstance(payload.get("customer_config"), dict):
        cfg.update(payload["customer_config"])
    if isinstance(payload.get("config"), dict):
        cfg.update(payload["config"])
    if isinstance(runtime_config, dict):
        cfg.update(runtime_config)
    return cfg


def _load_learning_profile() -> Dict[str, Any]:
    if _load_plugin_profile is None:
        return {}
    try:
        prof = _load_plugin_profile(_PLUGIN_SLUG)
        return prof if isinstance(prof, dict) else {}
    except Exception:
        return {}


def _run_core_logic(context: SkillContext, payload: Dict[str, Any], config: Dict[str, Any]) -> Dict[str, Any]:
    # === LOGIC START ===
    # Auto-generated readable capability-profile core logic. Edits may be overwritten by the factory.
    try:
        from schema_tools import infer_tabular_schema, pick_numeric_field
    except Exception:  # pragma: no cover
        def infer_tabular_schema(data):
            return {}
        def pick_numeric_field(schema, hints=None):
            return None
    try:
        if hasattr(context, 'log_info'):
            context.log_info('Executing capability-profile core logic.', plugin_slug=_PLUGIN_SLUG)
    except Exception:
        pass
    result = {
        'summary': '',
        'primary_insights': [],
        'recommended_actions': [],
        'scores': {'confidence': 0.0},
        'details': {},
    }
    schema = infer_tabular_schema(payload.get('data') if isinstance(payload, dict) else None)
    try:
        plugin_name = 'AI Tool Call Sequence Builder 000021'
        goal = 'Plan a safe order of tool calls for multi-step AI workflows.'
        domain = 'AI tool sequencing and orchestration'
        capability_type = 'integration'
        logic_profile_id = 'tool_call_sequence_builder_profile'
        generation_note = 'capability profile registry override'
        use_cases = ['Choose which tool should run first, second, and last.', 'Flag tool calls that need approval or verification first.', 'Explain when no external tool call is needed.', 'Show a compact progress state for this AI capability during baseline capability.', 'Return user-facing guidance that is useful, concise, and safe to act on.', 'Avoid duplicating existing AI capability behavior; identify what is unique about this capability.']
        payload_data = payload if isinstance(payload, dict) else {}
        payload_warnings = [] if isinstance(payload, dict) else ['payload was not a dict; using empty payload']
        task_text = str(payload_data.get('task') or '').strip()
        explicit_objective_text = str(payload_data.get('objective') or '').strip()
        def_text = str(task_text or explicit_objective_text or payload_data.get('prompt') or goal).strip()
        objective_text = str(explicit_objective_text or goal).strip()
        constraints = payload_data.get('constraints') if isinstance(payload_data.get('constraints'), list) else []
        messages = payload_data.get('messages') if isinstance(payload_data.get('messages'), list) else []
        candidate_outputs = payload_data.get('candidate_outputs') if isinstance(payload_data.get('candidate_outputs'), list) else []
        source_notes = payload_data.get('source_notes') if isinstance(payload_data.get('source_notes'), list) else []
        text = ' '.join([def_text, objective_text, ' '.join(str(item) for item in constraints)]).lower()
        tool_rules = [
            ('code_editor', ['code', 'repo', 'repository', 'file', 'bug', 'test', 'python', 'javascript', 'plugin', 'factory', 'validation'], 'Needed for source inspection, generated plugin work, or code changes.'),
            ('terminal', ['run', 'command', 'test', 'compile', 'server', 'process', 'pid', 'restart', 'ollama', 'factory_runner'], 'Needed for local verification and process control.'),
            ('git_github', ['git', 'github', 'commit', 'push', 'branch', 'remote', 'origin', 'pull request', 'pr'], 'Needed when the workflow must publish, inspect, or verify repository state.'),
            ('web_search', ['latest', 'current', 'price', 'news', 'docs', 'citation'], 'Needed when facts may have changed or sources are required.'),
            ('retrieval', ['search', 'knowledge', 'document', 'notes', 'memory'], 'Needed to find grounding context before generation.'),
            ('planner', ['complex', 'multi-step', 'handoff', 'agent', 'delegate', 'autonomous', 'continuous'], 'Needed to sequence work and prevent duplicated effort.'),
            ('validator', ['validate', 'validation', 'semantic', 'schema', 'quality', 'pass', 'fail', 'reject'], 'Needed to prove the result passes structural and semantic gates.'),
        ]
        recommendations = []
        for name, keywords, rationale in tool_rules:
            hits = [word for word in keywords if word in text]
            if hits:
                recommendations.append({'tool': name, 'matched_signals': hits, 'rationale': rationale, 'priority': len(hits)})
        recommendations = sorted(recommendations, key=lambda item: item['priority'], reverse=True)
        if not recommendations:
            recommendations.append({'tool': 'clarifying_prompt', 'matched_signals': [], 'rationale': 'Task lacks enough operational signals to choose a stronger tool.', 'priority': 0})
        rejected_tools = []
        if 'external' in text or 'internet' in text:
            rejected_tools.append({'tool': 'silent_offline_answer', 'reason': 'External grounding was requested or implied.'})
        if 'delete' in text or 'destructive' in text:
            rejected_tools.append({'tool': 'automatic_mutation', 'reason': 'Potentially destructive actions require explicit confirmation.'})
        selection_confidence = min(0.93, 0.48 + 0.12 * len(recommendations) + 0.03 * sum(len(item['matched_signals']) for item in recommendations))
        result['summary'] = plugin_name + ': selected ' + recommendations[0]['tool'] + ' as the first tool for ' + def_text[:140] + '.'
        result['primary_insights'] = [
            {'title': 'Top tool', 'detail': recommendations[0]},
            {'title': 'Tool signals', 'detail': [item['matched_signals'] for item in recommendations]},
            {'title': 'Rejected tools', 'detail': rejected_tools or 'No explicit rejections.'},
        ]
        result['recommended_actions'] = [
            {'action': 'Use ' + item['tool'], 'why': item['rationale'], 'signals': item['matched_signals']} for item in recommendations[:4]
        ]
        result['scores'] = {'confidence': round(selection_confidence, 2), 'usefulness': round(min(0.94, 0.55 + 0.1 * len(recommendations)), 2), 'routing_specificity': round(min(1.0, 0.35 + 0.08 * sum(len(item['matched_signals']) for item in recommendations)), 2), 'risk': round(0.22 + 0.08 * len(rejected_tools), 2)}
        result['details'] = {'tool_recommendations': recommendations, 'rejected_tools': rejected_tools, 'selection_rationale': recommendations[0]['rationale'], 'missing_inputs': ['task'] if not def_text else []}
        result['details']['use_cases'] = use_cases
        result['details']['generation_note'] = generation_note
        result['details']['capability_type'] = capability_type
        result['details']['logic_profile_id'] = logic_profile_id
        result['details']['payload_warnings'] = payload_warnings
        result['progress_state'] = {
            'current_stage': logic_profile_id,
            'next_step': 'Use ' + recommendations[0]['tool'],
            'blockers': result['details'].get('missing_inputs', [])[:4],
            'done_signals': ['capability_specific_analysis_complete', logic_profile_id],
        }
        result['user_experience'] = {
            'plain_language_takeaway': result['summary'],
            'beginner_tip': 'Use the first recommendation as the next concrete step.',
            'power_user_tip': 'Pass details and scores into the next AI capability module.',
            'interaction_suggestions': [item.get('action', str(item)) for item in result.get('recommended_actions', [])[:3]],
        }
        result['fun_mode'] = {
            'challenge_label': plugin_name,
            'score_badge': 'Strong Signal' if result.get('scores', {}).get('confidence', 0) >= 0.65 else 'Needs Context',
            'microcopy': result['summary'],
            'optional_next_challenge': 'Use ' + recommendations[0]['tool'],
        }
    except Exception as _exc:
        result = {
            'summary': 'Capability profile failed; fallback applied.',
            'primary_insights': [],
            'recommended_actions': ['Review payload and capability profile.'],
            'scores': {'confidence': 0.0},
            'details': {'error': str(_exc), 'logic_profile_id': 'capability_profile_error'},
        }
    if not isinstance(result, dict):
        result = {'summary': 'Capability profile returned non-dict output.', 'primary_insights': [], 'recommended_actions': [], 'scores': {'confidence': 0.0}, 'details': {}}
    result.setdefault('summary', 'Capability profile completed.')
    result.setdefault('primary_insights', [])
    result.setdefault('recommended_actions', [])
    result.setdefault('scores', {'confidence': 0.0})
    result.setdefault('details', {})
    if isinstance(result.get('scores'), dict):
        result['scores'].setdefault('confidence', 0.0)
        if 'usefulness' not in result['scores']:
            try:
                result['scores']['usefulness'] = round(min(0.95, max(0.0, float(result['scores'].get('confidence', 0.0)))), 2)
            except Exception:
                result['scores']['usefulness'] = 0.0
    if isinstance(result.get('fun_mode'), dict):
        result['fun_mode'].setdefault('microcopy', result.get('summary', 'Capability profile completed.'))
        result['fun_mode'].setdefault('celebratory_microcopy', result['fun_mode'].get('microcopy', result.get('summary', 'Capability profile completed.')))
    else:
        result['fun_mode'] = {
            'challenge_label': result.get('details', {}).get('logic_profile_id', 'Capability Run') if isinstance(result.get('details'), dict) else 'Capability Run',
            'score_badge': 'Ready',
            'microcopy': result.get('summary', 'Capability profile completed.'),
            'celebratory_microcopy': result.get('summary', 'Capability profile completed.'),
        }
    if not isinstance(result.get('diagnostics'), dict):
        result['diagnostics'] = {}
    result['diagnostics'].setdefault('logic_profile_id', result.get('details', {}).get('logic_profile_id', 'capability_profile') if isinstance(result.get('details'), dict) else 'capability_profile')
    return result
# === LOGIC END ===


async def invoke(
    user_id: str,
    payload: Dict[str, Any],
    *,
    run_id: Optional[str] = None,
    brain: Optional[Any] = None,
    logger: Optional[Any] = None,
    config: Optional[Dict[str, Any]] = None,
    **kwargs: Any,
) -> Dict[str, Any]:
    if not isinstance(payload, dict):
        payload = {
            "_value": payload,
            "_payload_warnings": ["payload was not a dict; invoke wrapped it in _value"],
        }
    context = SkillContext(
        user_id=user_id,
        run_id=run_id,
        plugin_slug=_PLUGIN_SLUG,
        plugin_name=_PLUGIN_NAME,
        learning_profile=_load_learning_profile(),
        logger=logger,
        brain=brain,
    )
    status = "failed"
    error_msg = ""
    core_output: Optional[Dict[str, Any]] = None
    try:
        core_output = _run_core_logic(context, payload, _build_effective_config(payload, config))
        if not isinstance(core_output, dict):
            raise TypeError("_run_core_logic must return a dict")
        status = "succeeded"
    except Exception as exc:
        context.log_error("Core logic raised an exception.", error=str(exc), exception_type=type(exc).__name__)
        error_msg = str(exc)
    meta = {
        "plugin_name": _PLUGIN_NAME,
        "plugin_slug": _PLUGIN_SLUG,
        "plugin_category": _PLUGIN_CATEGORY,
        "plugin_version": _PLUGIN_VERSION,
        "user_id": user_id,
        "run_id": run_id,
        "owner_id": _PLUGIN_OWNER_ID,
        "capability_type": _PLUGIN_CAPABILITY_TYPE,
        "intended_domain": _PLUGIN_INTENDED_DOMAIN,
        "schema_version": _PLUGIN_RESULT_SCHEMA_VERSION,
        "plugin_manifest": _PLUGIN_MANIFEST,
    }
    return {"status": status, "output": core_output if status == "succeeded" else None, "error": error_msg, "meta": meta}
