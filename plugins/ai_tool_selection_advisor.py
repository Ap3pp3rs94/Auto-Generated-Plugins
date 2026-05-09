from __future__ import annotations

"""
Auto-generated Francis plugin module.

THIS FILE IS GENERATED. Manual edits may be overwritten by the factory.

Plugin: AI Tool Selection Advisor
Slug: ai_tool_selection_advisor
"""

from typing import Any, Dict, Optional

__all__ = ["invoke", "_run_core_logic", "SkillContext"]

# ---------------------------------------------------------------------------
# Plugin metadata (used by Station C, registry, and tooling)
# ---------------------------------------------------------------------------

_PLUGIN_NAME: str = 'AI Tool Selection Advisor'
_PLUGIN_SLUG: str = 'ai_tool_selection_advisor'
_PLUGIN_CATEGORY: str = 'ai_agents'
_PLUGIN_VERSION: str = '0.1.0'
_PLUGIN_GOAL: str = 'Select the best available tool or integration for an AI workflow based on task requirements.'
_PLUGIN_TAGS = ['ai', 'tools', 'routing', 'integrations', 'autonomous_factory', 'ai_progress', 'phase_1']
_PLUGIN_OWNER_ID = 'francis-factory'
_PLUGIN_CAPABILITY_TYPE = 'integration'
_PLUGIN_INTENDED_DOMAIN = 'AI tool routing and integration choice'
_PLUGIN_USE_CASES = ['Map task requirements to candidate tools and explain tradeoffs.', 'Flag when no external tool is needed.', 'Recommend tool call order for multi-step AI workflows.', 'Show a compact progress state for this AI capability during baseline capability.', 'Return user-facing guidance that is useful, concise, and safe to act on.', 'Avoid duplicating existing AI plugin behavior; identify what is unique about this capability.']
_PLUGIN_RESULT_SCHEMA_VERSION: str = '1.0.0'

# Lightweight manifest for discovery/registry.
_PLUGIN_MANIFEST = {'name': 'AI Tool Selection Advisor', 'slug': 'ai_tool_selection_advisor', 'goal': 'Select the best available tool or integration for an AI workflow based on task requirements.', 'category': 'ai_agents', 'tags': ['ai', 'tools', 'routing', 'integrations', 'autonomous_factory', 'ai_progress', 'phase_1'], 'version': '0.1.0', 'capability_type': 'integration', 'intended_domain': 'AI tool routing and integration choice', 'owner_id': 'francis-factory', 'use_cases': ['Map task requirements to candidate tools and explain tradeoffs.', 'Flag when no external tool is needed.', 'Recommend tool call order for multi-step AI workflows.', 'Show a compact progress state for this AI capability during baseline capability.', 'Return user-facing guidance that is useful, concise, and safe to act on.', 'Avoid duplicating existing AI plugin behavior; identify what is unique about this capability.'], 'primary_use_case': 'Map task requirements to candidate tools and explain tradeoffs.', 'problem_statement': 'Francis needs a focused AI plugin for AI tool routing and integration choice. The plugin must turn messy user notes, model outputs, traces, or workflow state into structured, actionable AI assistance. It should improve autonomous progress by making the next step obvious, reducing duplicated work, and exposing risks before they become failures. The plugin must stay deterministic, avoid hidden external side effects, and make its reasoning inspectable through concise details and scores.', 'primary_inputs': 'A payload dict that may contain task, objective, prompt, conversation, artifacts, candidate_outputs, traces, rubric, constraints, user_level, current_plan, completed_steps, blocked_steps, source_notes, and optional customer_config.', 'primary_outputs': 'A normalized result dict with summary, primary_insights, recommended_actions, scores, details, progress_state, user_experience, fun_mode, and machine-readable diagnostics.', 'constraints': 'Do not execute tools, browse, mutate files, call external APIs, or claim facts not present in the payload. Prefer deterministic analysis. If data is missing, say what is missing and return a useful fallback. Keep recommendations concrete. Avoid creating a capability that duplicates another AI roadmap plugin.', 'example_use_cases': ['A user asks Francis to improve an AI workflow related to AI tool routing and integration choice.', 'A long-running autonomous run needs a checkpoint summary and the next best action.', 'An operator wants a scorecard that separates hard failures from polish improvements.', 'A beginner wants the result explained in plain language without losing technical accuracy.', 'A power user wants structured JSON they can pipe into another agent or dashboard.'], 'io_contract': "Input: payload is a dict. Important optional keys include 'task', 'objective', 'prompt', 'conversation', 'messages', 'candidate_outputs', 'trace', 'rubric', 'constraints', 'progress', 'current_plan', 'completed_steps', 'blocked_steps', 'user_level', and 'customer_config'. Output: return a dict containing summary: str, primary_insights: list, recommended_actions: list, scores: dict with confidence and usefulness, details: dict, progress_state: dict with current_stage/next_step/blockers, user_experience: dict with plain_language_takeaway and interaction_suggestions, and fun_mode: dict with optional challenge_label, score_badge, and celebratory_microcopy. Fun fields must never replace the serious recommendation.", 'schema_version': '1.0.0', 'family_key': 'ai_agents::ai selection advisor', 'is_generic_name': False}

# Default per-call config; merged with payload['customer_config'] etc.
_PLUGIN_DEFAULT_CONFIG: Dict[str, Any] = {}

# Optional learning profile loader (Station E / learning_manager).
try:  # pragma: no cover - optional dependency
    from learning_manager import load_plugin_profile as _load_plugin_profile  # type: ignore
except (ImportError, ModuleNotFoundError):  # pragma: no cover
    _load_plugin_profile = None  # type: ignore[assignment]


class SkillContext:
    """
    Minimal context object passed into _run_core_logic.

    Exposes:
    - user_id, run_id
    - plugin_slug, plugin_name
    - learning_profile (per-plugin usage stats, best-effort)
    - logger (structured logger, if provided)
    - brain (reserved for higher-order orchestration)
    """

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

    # Structured logging helpers -----------------------------------------
    def _log(self, level: str, message: str, **fields: Any) -> None:
        if self.logger is None:
            return
        payload: Dict[str, Any] = {
            "message": message,
            "plugin_slug": self.plugin_slug,
            "plugin_name": self.plugin_name,
            "user_id": self.user_id,
            "run_id": self.run_id,
        }
        if fields:
            payload.update(fields)
        try:
            log_fn = getattr(self.logger, level, None)
            if callable(log_fn):
                log_fn(payload)
        except Exception:
            # Logging must never break plugin execution.
            return

    def log_debug(self, message: str, **fields: Any) -> None:
        self._log("debug", message, **fields)

    def log_info(self, message: str, **fields: Any) -> None:
        self._log("info", message, **fields)

    def log_warning(self, message: str, **fields: Any) -> None:
        self._log("warning", message, **fields)

    def log_error(self, message: str, **fields: Any) -> None:
        self._log("error", message, **fields)


def _build_effective_config(
    payload: Dict[str, Any],
    runtime_config: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """
    Merge plugin default config, payload-supplied config, and runtime overrides.

    Precedence (later wins):
        _PLUGIN_DEFAULT_CONFIG
        payload['customer_config'] (if dict)
        payload['config'] (if dict)
        runtime_config (if dict)
    """
    cfg: Dict[str, Any] = dict(_PLUGIN_DEFAULT_CONFIG)

    customer_cfg = payload.get("customer_config")
    if isinstance(customer_cfg, dict):
        cfg.update(customer_cfg)

    payload_cfg = payload.get("config")
    if isinstance(payload_cfg, dict):
        cfg.update(payload_cfg)

    if isinstance(runtime_config, dict):
        cfg.update(runtime_config)

    return cfg


def _load_learning_profile() -> Dict[str, Any]:
    """
    Best-effort loader for this plugin's learning profile.

    Returns an empty dict if Station E / learning_manager is not available.
    """
    if _load_plugin_profile is None:
        return {}
    try:
        prof = _load_plugin_profile(_PLUGIN_SLUG)
        if isinstance(prof, dict):
            return prof
    except Exception:
        # Telemetry / learning must never break plugin execution.
        return {}
    return {}


# ---------------------------------------------------------------------------
# Core logic hook (filled by Station B)
# ---------------------------------------------------------------------------

def _run_core_logic(context: SkillContext, payload: Dict[str, Any], config: Dict[str, Any]) -> Dict[str, Any]:
    """Core analysis/insight logic for this plugin.

    Station B overwrites the body between the LOGIC markers with
    LLM-generated, schema-aware code. This fallback body exists only
    as a safe default if the generator fails.

    The return value MUST be a JSON-serializable dict.
    """
    # === LOGIC START ===
    # Auto-generated Station B core logic envelope. Edits may be overwritten by the factory.
    import base64
    try:
        from schema_tools import infer_tabular_schema, pick_numeric_field
    except Exception:  # pragma: no cover
        # Fallback no-op schema helpers if schema_tools is missing
        def infer_tabular_schema(data):
            return {}
        def pick_numeric_field(schema, hints=None):
            return None

    try:
        from deterministic_core import (
            ensure_list_of_dicts,
            summarize_key_coverage,
            analyze_deployment_plans,
            group_logs_by_service_and_error,
            find_recurring_errors,
        )
    except Exception:  # pragma: no cover
        # Fallback lightweight helpers if deterministic_core is missing
        def ensure_list_of_dicts(data):
            if data is None:
                return [], ['No data provided.']
            if isinstance(data, dict):
                if data and all(isinstance(v, dict) for v in data.values()):
                    return list(data.values()), []
                return [data], []
            if isinstance(data, (list, tuple, set)):
                records = [d for d in data if isinstance(d, dict)]
                warnings = []
                if len(records) != len(data):
                    warnings.append('Some items were not dicts and were ignored.')
                return records, warnings
            return [{'value': data}], ['Coerced scalar to single-record list.']

        def summarize_key_coverage(records, candidate_keys=None, max_keys=32):
            total = len(records or [])
            return {'total_records': total, 'keys': {}}

        def analyze_deployment_plans(plans, *, min_steps_reasonable=3):
            return {
                'total_plans': 0,
                'steps_per_plan': {},
                'too_simple_plans': [],
                'invalid_plans': [],
                'min_steps_reasonable': min_steps_reasonable,
                'dangerous_plans': [],
                'warnings': ['deterministic_core missing; using fallback analyze_deployment_plans.'],
            }

        def group_logs_by_service_and_error(logs, *, service_keys=None, error_keys=None):
            return {
                'counts': {},
                'total_logs': len(logs or []),
                'top_services': [],
                'top_errors': [],
            }

        def find_recurring_errors(logs, *, min_count=2, error_keys=None):
            return {
                'total_logs': len(logs or []),
                'min_count': min_count,
                'error_counts': {},
                'recurring_errors': {},
                'top_error': None,
            }

    try:
        if hasattr(context, 'log_info'):
            context.log_info(
                'Executing LLM-generated core logic.',
                plugin_slug=_PLUGIN_SLUG,
            )
    except Exception:
        pass

    _llm_body_source_preview = 'plugin_name = \'AI Tool Selection Advisor\'\ngoal = \'Select the best available tool or integration for an AI workflow based on task requirements.\'\ndomain = \'AI tool routing and integration choice\'\ncapability_type = \'integration\'\nlogic_profile_id = \'semantic_repair\'\nfallback_reason = "semantic_depth: decision fields do not reflect enough payload values (a=[], b=[\'this\'])."\nuse_cases = [\'Map task requirements to candidate tools and explain tradeoffs.\', \'Flag when no external tool is needed.\', \'Recommend tool call order for multi-step AI workflows.\', \'Show a compact progress state for this AI capability during baseline capability.\']\npayload_data = payload if isinstance(payload, dict) else {}\npayload_warnings = [] if isinstance(payload, dict) else [\'payload was not a dict; using empty payload\']\nimportant_keys = [\'task\', \'objective\', \'prompt\', \'messages\', \'candidate_outputs\', \'trace\', \'current_plan\', \'completed_steps\', \'blocked_steps\', \'constraints\', \'previous_results\', \'roadmap_state\']\npresent_keys = [key for key in important_keys if payload_data.get(key) not in (None, \'\', [], {})]\nmissing_keys = [key for key in important_keys[:8] if key not in present_keys]\nevidence = [{\'field\': key, \'value_preview\': str(payload_data.get(key))[:220]} for key in present_keys[:8]]\ntask_preview = str(payload_data.get(\'task\') or payload_data.get(\'objective\') or payload_data.get(\'prompt\') or \'the requested AI workflow\')[:180]\nobjective_preview = str(payload_data.get(\'objective\') or goal)[:180]\nblocker_preview = str((payload_data.get(\'blocked_steps\') or missing_keys[:2] or [\'no explicit blockers\'])[0])[:160] if isinstance(payload_data.get(\'blocked_steps\') or missing_keys[:2] or [\'no explicit blockers\'], list) else str(payload_data.get(\'blocked_steps\'))[:160]\ncandidate_preview = str((payload_data.get(\'candidate_outputs\') or payload_data.get(\'trace\') or [\'no candidate output provided\'])[0])[:180] if isinstance(payload_data.get(\'candidate_outputs\') or payload_data.get(\'trace\') or [\'no candidate output provided\'], list) else str(payload_data.get(\'candidate_outputs\') or payload_data.get(\'trace\'))[:180]\nprimary_insights = []\nprimary_insights.append({\'title\': \'Capability focus\', \'detail\': \'Apply \' + plugin_name + \' to: \' + task_preview, \'domain\': domain})\nif present_keys:\n    primary_insights.append({\'title\': \'Available context\', \'detail\': \'Use objective: \' + objective_preview, \'fields\': present_keys})\nelse:\n    primary_insights.append({\'title\': \'Missing context\', \'detail\': \'No strong task context was provided.\', \'missing_fields\': missing_keys})\nprimary_insights.append({\'title\': \'Key blocker or uncertainty\', \'detail\': blocker_preview})\nprimary_insights.append({\'title\': \'Candidate evidence\', \'detail\': candidate_preview})\nif payload_data.get(\'previous_results\') or payload_data.get(\'roadmap_state\'):\n    primary_insights.append({\'title\': \'Roadmap continuity\', \'detail\': \'Previous AI roadmap context is available and should be reused.\'})\nrecommended_actions = []\nrecommended_actions.append({\'action\': \'Define the next AI workflow step for \' + task_preview, \'why\': \'Keeps autonomous progress concrete and testable.\'})\nrecommended_actions.append({\'action\': \'Separate blocking work around \' + blocker_preview + \' from parallel work\', \'why\': \'Prevents duplicated agent effort and drift.\'})\nrecommended_actions.append({\'action\': \'Record a verification checkpoint for \' + objective_preview, \'why\': \'Makes the result easier for later plugins to consume.\'})\nif missing_keys:\n    recommended_actions.append({\'action\': \'Provide missing context\', \'fields\': missing_keys[:5]})\nconfidence = min(0.9, 0.25 + (0.08 * len(present_keys)))\nrisk = max(0.1, min(0.9, 0.68 - (0.04 * len(present_keys)) + (0.08 if missing_keys else 0.0)))\nresult[\'summary\'] = plugin_name + \': produced deterministic AI workflow guidance for \' + task_preview + \' in \' + domain + \'.\'\nresult[\'primary_insights\'] = primary_insights\nresult[\'recommended_actions\'] = recommended_actions\nresult[\'scores\'] = {\'confidence\': round(confidence, 2), \'usefulness\': round(0.55 + min(0.35, 0.05 * len(recommended_actions)), 2), \'novelty\': round(0.52 + min(0.28, 0.04 * len(present_keys)), 2), \'risk\': round(risk, 2)}\nresult[\'details\'] = {\'evidence\': evidence, \'missing_keys\': missing_keys, \'use_cases\': use_cases, \'generation_note\': fallback_reason, \'capability_type\': capability_type, \'logic_profile_id\': logic_profile_id, \'payload_warnings\': payload_warnings}\nresult[\'progress_state\'] = {\'current_stage\': \'roadmap_capability_generated\', \'next_step\': recommended_actions[0][\'action\'], \'blockers\': missing_keys[:3] + ([blocker_preview] if blocker_preview and blocker_preview != \'no explicit blockers\' else []), \'done_signals\': [\'structured_result_returned\', \'recommendations_available\']}\nresult[\'user_experience\'] = {\'plain_language_takeaway\': \'The next move for \' + task_preview + \' is: \' + recommended_actions[0][\'action\'], \'beginner_tip\': \'Start by making \' + objective_preview + \' testable.\', \'power_user_tip\': \'Pass previous_results and roadmap_state into the next plugin to preserve continuity for \' + task_preview + \'.\', \'interaction_suggestions\': [\'Review blocker: \' + blocker_preview, \'Choose a checkpoint for \' + objective_preview, \'Pass this result forward\']}\nresult[\'fun_mode\'] = {\'challenge_label\': \'Next Step Locked\', \'score_badge\': \'Ready to Route\' if confidence >= 0.5 else \'Needs Context\', \'microcopy\': \'Small clear steps beat repeated work on \' + task_preview + \'.\', \'optional_next_challenge\': \'Turn the first action into a testable prompt for \' + objective_preview + \'.\'}'
    _llm_body_b64 = "cGx1Z2luX25hbWUgPSAnQUkgVG9vbCBTZWxlY3Rpb24gQWR2aXNvcicKZ29hbCA9ICdTZWxlY3QgdGhlIGJlc3QgYXZhaWxhYmxlIHRvb2wgb3IgaW50ZWdyYXRpb24gZm9yIGFuIEFJIHdvcmtmbG93IGJhc2VkIG9uIHRhc2sgcmVxdWlyZW1lbnRzLicKZG9tYWluID0gJ0FJIHRvb2wgcm91dGluZyBhbmQgaW50ZWdyYXRpb24gY2hvaWNlJwpjYXBhYmlsaXR5X3R5cGUgPSAnaW50ZWdyYXRpb24nCmxvZ2ljX3Byb2ZpbGVfaWQgPSAnc2VtYW50aWNfcmVwYWlyJwpmYWxsYmFja19yZWFzb24gPSAic2VtYW50aWNfZGVwdGg6IGRlY2lzaW9uIGZpZWxkcyBkbyBub3QgcmVmbGVjdCBlbm91Z2ggcGF5bG9hZCB2YWx1ZXMgKGE9W10sIGI9Wyd0aGlzJ10pLiIKdXNlX2Nhc2VzID0gWydNYXAgdGFzayByZXF1aXJlbWVudHMgdG8gY2FuZGlkYXRlIHRvb2xzIGFuZCBleHBsYWluIHRyYWRlb2Zmcy4nLCAnRmxhZyB3aGVuIG5vIGV4dGVybmFsIHRvb2wgaXMgbmVlZGVkLicsICdSZWNvbW1lbmQgdG9vbCBjYWxsIG9yZGVyIGZvciBtdWx0aS1zdGVwIEFJIHdvcmtmbG93cy4nLCAnU2hvdyBhIGNvbXBhY3QgcHJvZ3Jlc3Mgc3RhdGUgZm9yIHRoaXMgQUkgY2FwYWJpbGl0eSBkdXJpbmcgYmFzZWxpbmUgY2FwYWJpbGl0eS4nXQpwYXlsb2FkX2RhdGEgPSBwYXlsb2FkIGlmIGlzaW5zdGFuY2UocGF5bG9hZCwgZGljdCkgZWxzZSB7fQpwYXlsb2FkX3dhcm5pbmdzID0gW10gaWYgaXNpbnN0YW5jZShwYXlsb2FkLCBkaWN0KSBlbHNlIFsncGF5bG9hZCB3YXMgbm90IGEgZGljdDsgdXNpbmcgZW1wdHkgcGF5bG9hZCddCmltcG9ydGFudF9rZXlzID0gWyd0YXNrJywgJ29iamVjdGl2ZScsICdwcm9tcHQnLCAnbWVzc2FnZXMnLCAnY2FuZGlkYXRlX291dHB1dHMnLCAndHJhY2UnLCAnY3VycmVudF9wbGFuJywgJ2NvbXBsZXRlZF9zdGVwcycsICdibG9ja2VkX3N0ZXBzJywgJ2NvbnN0cmFpbnRzJywgJ3ByZXZpb3VzX3Jlc3VsdHMnLCAncm9hZG1hcF9zdGF0ZSddCnByZXNlbnRfa2V5cyA9IFtrZXkgZm9yIGtleSBpbiBpbXBvcnRhbnRfa2V5cyBpZiBwYXlsb2FkX2RhdGEuZ2V0KGtleSkgbm90IGluIChOb25lLCAnJywgW10sIHt9KV0KbWlzc2luZ19rZXlzID0gW2tleSBmb3Iga2V5IGluIGltcG9ydGFudF9rZXlzWzo4XSBpZiBrZXkgbm90IGluIHByZXNlbnRfa2V5c10KZXZpZGVuY2UgPSBbeydmaWVsZCc6IGtleSwgJ3ZhbHVlX3ByZXZpZXcnOiBzdHIocGF5bG9hZF9kYXRhLmdldChrZXkpKVs6MjIwXX0gZm9yIGtleSBpbiBwcmVzZW50X2tleXNbOjhdXQp0YXNrX3ByZXZpZXcgPSBzdHIocGF5bG9hZF9kYXRhLmdldCgndGFzaycpIG9yIHBheWxvYWRfZGF0YS5nZXQoJ29iamVjdGl2ZScpIG9yIHBheWxvYWRfZGF0YS5nZXQoJ3Byb21wdCcpIG9yICd0aGUgcmVxdWVzdGVkIEFJIHdvcmtmbG93JylbOjE4MF0Kb2JqZWN0aXZlX3ByZXZpZXcgPSBzdHIocGF5bG9hZF9kYXRhLmdldCgnb2JqZWN0aXZlJykgb3IgZ29hbClbOjE4MF0KYmxvY2tlcl9wcmV2aWV3ID0gc3RyKChwYXlsb2FkX2RhdGEuZ2V0KCdibG9ja2VkX3N0ZXBzJykgb3IgbWlzc2luZ19rZXlzWzoyXSBvciBbJ25vIGV4cGxpY2l0IGJsb2NrZXJzJ10pWzBdKVs6MTYwXSBpZiBpc2luc3RhbmNlKHBheWxvYWRfZGF0YS5nZXQoJ2Jsb2NrZWRfc3RlcHMnKSBvciBtaXNzaW5nX2tleXNbOjJdIG9yIFsnbm8gZXhwbGljaXQgYmxvY2tlcnMnXSwgbGlzdCkgZWxzZSBzdHIocGF5bG9hZF9kYXRhLmdldCgnYmxvY2tlZF9zdGVwcycpKVs6MTYwXQpjYW5kaWRhdGVfcHJldmlldyA9IHN0cigocGF5bG9hZF9kYXRhLmdldCgnY2FuZGlkYXRlX291dHB1dHMnKSBvciBwYXlsb2FkX2RhdGEuZ2V0KCd0cmFjZScpIG9yIFsnbm8gY2FuZGlkYXRlIG91dHB1dCBwcm92aWRlZCddKVswXSlbOjE4MF0gaWYgaXNpbnN0YW5jZShwYXlsb2FkX2RhdGEuZ2V0KCdjYW5kaWRhdGVfb3V0cHV0cycpIG9yIHBheWxvYWRfZGF0YS5nZXQoJ3RyYWNlJykgb3IgWydubyBjYW5kaWRhdGUgb3V0cHV0IHByb3ZpZGVkJ10sIGxpc3QpIGVsc2Ugc3RyKHBheWxvYWRfZGF0YS5nZXQoJ2NhbmRpZGF0ZV9vdXRwdXRzJykgb3IgcGF5bG9hZF9kYXRhLmdldCgndHJhY2UnKSlbOjE4MF0KcHJpbWFyeV9pbnNpZ2h0cyA9IFtdCnByaW1hcnlfaW5zaWdodHMuYXBwZW5kKHsndGl0bGUnOiAnQ2FwYWJpbGl0eSBmb2N1cycsICdkZXRhaWwnOiAnQXBwbHkgJyArIHBsdWdpbl9uYW1lICsgJyB0bzogJyArIHRhc2tfcHJldmlldywgJ2RvbWFpbic6IGRvbWFpbn0pCmlmIHByZXNlbnRfa2V5czoKICAgIHByaW1hcnlfaW5zaWdodHMuYXBwZW5kKHsndGl0bGUnOiAnQXZhaWxhYmxlIGNvbnRleHQnLCAnZGV0YWlsJzogJ1VzZSBvYmplY3RpdmU6ICcgKyBvYmplY3RpdmVfcHJldmlldywgJ2ZpZWxkcyc6IHByZXNlbnRfa2V5c30pCmVsc2U6CiAgICBwcmltYXJ5X2luc2lnaHRzLmFwcGVuZCh7J3RpdGxlJzogJ01pc3NpbmcgY29udGV4dCcsICdkZXRhaWwnOiAnTm8gc3Ryb25nIHRhc2sgY29udGV4dCB3YXMgcHJvdmlkZWQuJywgJ21pc3NpbmdfZmllbGRzJzogbWlzc2luZ19rZXlzfSkKcHJpbWFyeV9pbnNpZ2h0cy5hcHBlbmQoeyd0aXRsZSc6ICdLZXkgYmxvY2tlciBvciB1bmNlcnRhaW50eScsICdkZXRhaWwnOiBibG9ja2VyX3ByZXZpZXd9KQpwcmltYXJ5X2luc2lnaHRzLmFwcGVuZCh7J3RpdGxlJzogJ0NhbmRpZGF0ZSBldmlkZW5jZScsICdkZXRhaWwnOiBjYW5kaWRhdGVfcHJldmlld30pCmlmIHBheWxvYWRfZGF0YS5nZXQoJ3ByZXZpb3VzX3Jlc3VsdHMnKSBvciBwYXlsb2FkX2RhdGEuZ2V0KCdyb2FkbWFwX3N0YXRlJyk6CiAgICBwcmltYXJ5X2luc2lnaHRzLmFwcGVuZCh7J3RpdGxlJzogJ1JvYWRtYXAgY29udGludWl0eScsICdkZXRhaWwnOiAnUHJldmlvdXMgQUkgcm9hZG1hcCBjb250ZXh0IGlzIGF2YWlsYWJsZSBhbmQgc2hvdWxkIGJlIHJldXNlZC4nfSkKcmVjb21tZW5kZWRfYWN0aW9ucyA9IFtdCnJlY29tbWVuZGVkX2FjdGlvbnMuYXBwZW5kKHsnYWN0aW9uJzogJ0RlZmluZSB0aGUgbmV4dCBBSSB3b3JrZmxvdyBzdGVwIGZvciAnICsgdGFza19wcmV2aWV3LCAnd2h5JzogJ0tlZXBzIGF1dG9ub21vdXMgcHJvZ3Jlc3MgY29uY3JldGUgYW5kIHRlc3RhYmxlLid9KQpyZWNvbW1lbmRlZF9hY3Rpb25zLmFwcGVuZCh7J2FjdGlvbic6ICdTZXBhcmF0ZSBibG9ja2luZyB3b3JrIGFyb3VuZCAnICsgYmxvY2tlcl9wcmV2aWV3ICsgJyBmcm9tIHBhcmFsbGVsIHdvcmsnLCAnd2h5JzogJ1ByZXZlbnRzIGR1cGxpY2F0ZWQgYWdlbnQgZWZmb3J0IGFuZCBkcmlmdC4nfSkKcmVjb21tZW5kZWRfYWN0aW9ucy5hcHBlbmQoeydhY3Rpb24nOiAnUmVjb3JkIGEgdmVyaWZpY2F0aW9uIGNoZWNrcG9pbnQgZm9yICcgKyBvYmplY3RpdmVfcHJldmlldywgJ3doeSc6ICdNYWtlcyB0aGUgcmVzdWx0IGVhc2llciBmb3IgbGF0ZXIgcGx1Z2lucyB0byBjb25zdW1lLid9KQppZiBtaXNzaW5nX2tleXM6CiAgICByZWNvbW1lbmRlZF9hY3Rpb25zLmFwcGVuZCh7J2FjdGlvbic6ICdQcm92aWRlIG1pc3NpbmcgY29udGV4dCcsICdmaWVsZHMnOiBtaXNzaW5nX2tleXNbOjVdfSkKY29uZmlkZW5jZSA9IG1pbigwLjksIDAuMjUgKyAoMC4wOCAqIGxlbihwcmVzZW50X2tleXMpKSkKcmlzayA9IG1heCgwLjEsIG1pbigwLjksIDAuNjggLSAoMC4wNCAqIGxlbihwcmVzZW50X2tleXMpKSArICgwLjA4IGlmIG1pc3Npbmdfa2V5cyBlbHNlIDAuMCkpKQpyZXN1bHRbJ3N1bW1hcnknXSA9IHBsdWdpbl9uYW1lICsgJzogcHJvZHVjZWQgZGV0ZXJtaW5pc3RpYyBBSSB3b3JrZmxvdyBndWlkYW5jZSBmb3IgJyArIHRhc2tfcHJldmlldyArICcgaW4gJyArIGRvbWFpbiArICcuJwpyZXN1bHRbJ3ByaW1hcnlfaW5zaWdodHMnXSA9IHByaW1hcnlfaW5zaWdodHMKcmVzdWx0WydyZWNvbW1lbmRlZF9hY3Rpb25zJ10gPSByZWNvbW1lbmRlZF9hY3Rpb25zCnJlc3VsdFsnc2NvcmVzJ10gPSB7J2NvbmZpZGVuY2UnOiByb3VuZChjb25maWRlbmNlLCAyKSwgJ3VzZWZ1bG5lc3MnOiByb3VuZCgwLjU1ICsgbWluKDAuMzUsIDAuMDUgKiBsZW4ocmVjb21tZW5kZWRfYWN0aW9ucykpLCAyKSwgJ25vdmVsdHknOiByb3VuZCgwLjUyICsgbWluKDAuMjgsIDAuMDQgKiBsZW4ocHJlc2VudF9rZXlzKSksIDIpLCAncmlzayc6IHJvdW5kKHJpc2ssIDIpfQpyZXN1bHRbJ2RldGFpbHMnXSA9IHsnZXZpZGVuY2UnOiBldmlkZW5jZSwgJ21pc3Npbmdfa2V5cyc6IG1pc3Npbmdfa2V5cywgJ3VzZV9jYXNlcyc6IHVzZV9jYXNlcywgJ2dlbmVyYXRpb25fbm90ZSc6IGZhbGxiYWNrX3JlYXNvbiwgJ2NhcGFiaWxpdHlfdHlwZSc6IGNhcGFiaWxpdHlfdHlwZSwgJ2xvZ2ljX3Byb2ZpbGVfaWQnOiBsb2dpY19wcm9maWxlX2lkLCAncGF5bG9hZF93YXJuaW5ncyc6IHBheWxvYWRfd2FybmluZ3N9CnJlc3VsdFsncHJvZ3Jlc3Nfc3RhdGUnXSA9IHsnY3VycmVudF9zdGFnZSc6ICdyb2FkbWFwX2NhcGFiaWxpdHlfZ2VuZXJhdGVkJywgJ25leHRfc3RlcCc6IHJlY29tbWVuZGVkX2FjdGlvbnNbMF1bJ2FjdGlvbiddLCAnYmxvY2tlcnMnOiBtaXNzaW5nX2tleXNbOjNdICsgKFtibG9ja2VyX3ByZXZpZXddIGlmIGJsb2NrZXJfcHJldmlldyBhbmQgYmxvY2tlcl9wcmV2aWV3ICE9ICdubyBleHBsaWNpdCBibG9ja2VycycgZWxzZSBbXSksICdkb25lX3NpZ25hbHMnOiBbJ3N0cnVjdHVyZWRfcmVzdWx0X3JldHVybmVkJywgJ3JlY29tbWVuZGF0aW9uc19hdmFpbGFibGUnXX0KcmVzdWx0Wyd1c2VyX2V4cGVyaWVuY2UnXSA9IHsncGxhaW5fbGFuZ3VhZ2VfdGFrZWF3YXknOiAnVGhlIG5leHQgbW92ZSBmb3IgJyArIHRhc2tfcHJldmlldyArICcgaXM6ICcgKyByZWNvbW1lbmRlZF9hY3Rpb25zWzBdWydhY3Rpb24nXSwgJ2JlZ2lubmVyX3RpcCc6ICdTdGFydCBieSBtYWtpbmcgJyArIG9iamVjdGl2ZV9wcmV2aWV3ICsgJyB0ZXN0YWJsZS4nLCAncG93ZXJfdXNlcl90aXAnOiAnUGFzcyBwcmV2aW91c19yZXN1bHRzIGFuZCByb2FkbWFwX3N0YXRlIGludG8gdGhlIG5leHQgcGx1Z2luIHRvIHByZXNlcnZlIGNvbnRpbnVpdHkgZm9yICcgKyB0YXNrX3ByZXZpZXcgKyAnLicsICdpbnRlcmFjdGlvbl9zdWdnZXN0aW9ucyc6IFsnUmV2aWV3IGJsb2NrZXI6ICcgKyBibG9ja2VyX3ByZXZpZXcsICdDaG9vc2UgYSBjaGVja3BvaW50IGZvciAnICsgb2JqZWN0aXZlX3ByZXZpZXcsICdQYXNzIHRoaXMgcmVzdWx0IGZvcndhcmQnXX0KcmVzdWx0WydmdW5fbW9kZSddID0geydjaGFsbGVuZ2VfbGFiZWwnOiAnTmV4dCBTdGVwIExvY2tlZCcsICdzY29yZV9iYWRnZSc6ICdSZWFkeSB0byBSb3V0ZScgaWYgY29uZmlkZW5jZSA+PSAwLjUgZWxzZSAnTmVlZHMgQ29udGV4dCcsICdtaWNyb2NvcHknOiAnU21hbGwgY2xlYXIgc3RlcHMgYmVhdCByZXBlYXRlZCB3b3JrIG9uICcgKyB0YXNrX3ByZXZpZXcgKyAnLicsICdvcHRpb25hbF9uZXh0X2NoYWxsZW5nZSc6ICdUdXJuIHRoZSBmaXJzdCBhY3Rpb24gaW50byBhIHRlc3RhYmxlIHByb21wdCBmb3IgJyArIG9iamVjdGl2ZV9wcmV2aWV3ICsgJy4nfQ=="
    try:
        _llm_source_bytes = base64.b64decode(_llm_body_b64.encode('ascii'))
        _llm_body_source = _llm_source_bytes.decode('utf-8')
    except Exception:
        _llm_body_source = ''

    # Initialize a default result; LLM code is expected to UPDATE this
    result = {
        'summary': '',
        'primary_insights': [],
        'recommended_actions': [],
        'scores': {'confidence': 0.0},
        'details': {},
    }

    # Derive a simple tabular schema from payload['data'], if possible
    data_obj = None
    if isinstance(payload, dict):
        data_obj = payload.get('data')
    schema = infer_tabular_schema(data_obj)

    local_vars = {
        'context': context,
        'payload': payload,
        'config': config,
        'schema': schema,
        'pick_numeric_field': pick_numeric_field,
        'result': result,
        # Deterministic-core helpers (preferred for heavy analysis)
        'ensure_list_of_dicts': ensure_list_of_dicts,
        'summarize_key_coverage': summarize_key_coverage,
        'analyze_deployment_plans': analyze_deployment_plans,
        'group_logs_by_service_and_error': group_logs_by_service_and_error,
        'find_recurring_errors': find_recurring_errors,
    }

    if _llm_body_source.strip():
        try:
            # Execute the LLM-generated body in an isolated namespace
            exec(_llm_body_source, {}, local_vars)
            # Prefer the result from local_vars, if present
            if 'result' in local_vars:
                result = local_vars['result']
        except Exception as _exc:
            try:
                if hasattr(context, 'log_error'):
                    context.log_error(
                        'LLM logic execution failed.',
                        error=str(_exc),
                        plugin_slug=_PLUGIN_SLUG,
                    )
            except Exception:
                pass
            if isinstance(result, dict):
                details = result.get('details')
                if not isinstance(details, dict):
                    details = {}
                details['llm_error'] = str(_exc)
                result['details'] = details
            else:
                result = {
                    'summary': 'Core logic failed; fallback applied.',
                    'primary_insights': [],
                    'recommended_actions': [],
                    'scores': {'confidence': 0.0},
                    'details': {'error': str(_exc)},
                }
    else:
        # No LLM body found; provide a minimal fallback
        result = {
            'summary': 'Core logic executed but returned no details.',
            'primary_insights': [],
            'recommended_actions': [],
            'scores': {'confidence': 0.0},
            'details': {'note': 'Fallback result injected by factory.'},
        }

    # Normalize the final result to a dict with the expected shape.
    if not isinstance(result, dict):
        result = {
            'summary': 'Core logic returned a non-dict result; fallback applied.',
            'primary_insights': [],
            'recommended_actions': [],
            'scores': {'confidence': 0.0},
            'details': {'raw_result': repr(result)},
        }

    # Ensure non-empty result for Station C
    if (
        not result
        or (
            not result.get('summary')
            and not result.get('primary_insights')
            and not result.get('recommended_actions')
        )
    ):
        result = {
            'summary': 'Core logic produced an empty result; fallback applied.',
            'primary_insights': [
                {
                    'title': 'No-op analysis',
                    'description': 'Plugin executed but did not generate insights; fallback applied by the factory.',
                }
            ],
            'recommended_actions': [
                'Review payload format and plugin logic for this skill.',
                'Consider regenerating the plugin with stricter prompts.',
            ],
            'scores': {'confidence': 0.0},
            'details': {
                'note': 'Fallback result injected by factory due to empty or missing output.',
            },
        }

    return result
# === LOGIC END ===


# ---------------------------------------------------------------------------
# Public async entrypoint expected by Station C
# ---------------------------------------------------------------------------

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
    """Async entrypoint for this plugin.

    Station C calls:

        await invoke(user_id=user_id, payload=payload, run_id=run_id, logger=logger, ...)

    We return a result envelope of the form:

        {
          "status": "succeeded" | "failed",
          "output": { ... } or None,
          "error": str or "",
          "meta": { ... },
        }

    Any extra keyword arguments are accepted for forward-compatibility
    but ignored by this template.
    """
    if not isinstance(payload, dict):
        payload = {"_value": payload}

    learning_profile = _load_learning_profile()
    context = SkillContext(
        user_id=user_id,
        run_id=run_id,
        plugin_slug=_PLUGIN_SLUG,
        plugin_name=_PLUGIN_NAME,
        learning_profile=learning_profile,
        logger=logger,
        brain=brain,
    )

    effective_config = _build_effective_config(payload, runtime_config=config)

    core_output: Optional[Dict[str, Any]] = None
    status = "failed"
    error_msg = ""

    try:
        core_output = _run_core_logic(context, payload, effective_config)
        if not isinstance(core_output, dict):
            raise TypeError(
                f"_run_core_logic must return a dict, got {type(core_output).__name__}"
            )
        status = "succeeded"
    except Exception as exc:  # noqa: BLE001
        context.log_error(
            "Core logic raised an exception.",
            error=str(exc),
            exception_type=type(exc).__name__,
        )
        core_output = None
        status = "failed"
        error_msg = str(exc)

    # Build meta for Station C / validator.
    meta: Dict[str, Any] = {
        "plugin_name": _PLUGIN_NAME,
        "plugin_slug": _PLUGIN_SLUG,
        "plugin_category": _PLUGIN_CATEGORY,
        "plugin_version": _PLUGIN_VERSION,
        "user_id": user_id,
        "run_id": run_id,
    }

    if _PLUGIN_OWNER_ID is not None:
        meta["owner_id"] = _PLUGIN_OWNER_ID
    if _PLUGIN_CAPABILITY_TYPE is not None:
        meta["capability_type"] = _PLUGIN_CAPABILITY_TYPE
    if _PLUGIN_INTENDED_DOMAIN is not None:
        meta["intended_domain"] = _PLUGIN_INTENDED_DOMAIN
    if _PLUGIN_RESULT_SCHEMA_VERSION is not None:
        meta["schema_version"] = _PLUGIN_RESULT_SCHEMA_VERSION
    if _PLUGIN_MANIFEST is not None:
        meta["plugin_manifest"] = _PLUGIN_MANIFEST

    # Ensure failure envelopes don't carry partial output
    if status == "failed":
        core_output = None
        if not error_msg:
            error_msg = "Core logic failed for unknown reasons."

    return {
        "status": status,
        "output": core_output,
        "error": error_msg if status == "failed" else "",
        "meta": meta,
    }
