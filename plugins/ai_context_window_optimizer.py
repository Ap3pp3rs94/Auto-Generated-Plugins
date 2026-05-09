from __future__ import annotations

"""
Auto-generated Francis plugin module.

THIS FILE IS GENERATED. Manual edits may be overwritten by the factory.

Plugin: AI Context Window Optimizer
Slug: ai_context_window_optimizer
"""

from typing import Any, Dict, Optional

__all__ = ["invoke", "_run_core_logic", "SkillContext"]

# ---------------------------------------------------------------------------
# Plugin metadata (used by Station C, registry, and tooling)
# ---------------------------------------------------------------------------

_PLUGIN_NAME: str = 'AI Context Window Optimizer'
_PLUGIN_SLUG: str = 'ai_context_window_optimizer'
_PLUGIN_CATEGORY: str = 'ai_memory'
_PLUGIN_VERSION: str = '0.1.0'
_PLUGIN_GOAL: str = 'Prioritize which context should be kept, compressed, or dropped before an AI model call.'
_PLUGIN_TAGS = ['ai', 'context', 'tokens', 'optimization', 'autonomous_factory', 'ai_progress', 'phase_1']
_PLUGIN_OWNER_ID = 'francis-factory'
_PLUGIN_CAPABILITY_TYPE = 'data_insight'
_PLUGIN_INTENDED_DOMAIN = 'AI context packing and token budget management'
_PLUGIN_USE_CASES = ['Rank context snippets by relevance to the current task.', 'Detect redundant or stale context.', 'Suggest compact replacements for large repeated sections.', 'Show a compact progress state for this AI capability during baseline capability.', 'Return user-facing guidance that is useful, concise, and safe to act on.', 'Avoid duplicating existing AI plugin behavior; identify what is unique about this capability.']
_PLUGIN_RESULT_SCHEMA_VERSION: str = '1.0.0'

# Lightweight manifest for discovery/registry.
_PLUGIN_MANIFEST = {'name': 'AI Context Window Optimizer', 'slug': 'ai_context_window_optimizer', 'goal': 'Prioritize which context should be kept, compressed, or dropped before an AI model call.', 'category': 'ai_memory', 'tags': ['ai', 'context', 'tokens', 'optimization', 'autonomous_factory', 'ai_progress', 'phase_1'], 'version': '0.1.0', 'capability_type': 'data_insight', 'intended_domain': 'AI context packing and token budget management', 'owner_id': 'francis-factory', 'use_cases': ['Rank context snippets by relevance to the current task.', 'Detect redundant or stale context.', 'Suggest compact replacements for large repeated sections.', 'Show a compact progress state for this AI capability during baseline capability.', 'Return user-facing guidance that is useful, concise, and safe to act on.', 'Avoid duplicating existing AI plugin behavior; identify what is unique about this capability.'], 'primary_use_case': 'Rank context snippets by relevance to the current task.', 'problem_statement': 'Francis needs a focused AI plugin for AI context packing and token budget management. The plugin must turn messy user notes, model outputs, traces, or workflow state into structured, actionable AI assistance. It should improve autonomous progress by making the next step obvious, reducing duplicated work, and exposing risks before they become failures. The plugin must stay deterministic, avoid hidden external side effects, and make its reasoning inspectable through concise details and scores.', 'primary_inputs': 'A payload dict that may contain task, objective, prompt, conversation, artifacts, candidate_outputs, traces, rubric, constraints, user_level, current_plan, completed_steps, blocked_steps, source_notes, and optional customer_config.', 'primary_outputs': 'A normalized result dict with summary, primary_insights, recommended_actions, scores, details, progress_state, user_experience, fun_mode, and machine-readable diagnostics.', 'constraints': 'Do not execute tools, browse, mutate files, call external APIs, or claim facts not present in the payload. Prefer deterministic analysis. If data is missing, say what is missing and return a useful fallback. Keep recommendations concrete. Avoid creating a capability that duplicates another AI roadmap plugin.', 'example_use_cases': ['A user asks Francis to improve an AI workflow related to AI context packing and token budget management.', 'A long-running autonomous run needs a checkpoint summary and the next best action.', 'An operator wants a scorecard that separates hard failures from polish improvements.', 'A beginner wants the result explained in plain language without losing technical accuracy.', 'A power user wants structured JSON they can pipe into another agent or dashboard.'], 'io_contract': "Input: payload is a dict. Important optional keys include 'task', 'objective', 'prompt', 'conversation', 'messages', 'candidate_outputs', 'trace', 'rubric', 'constraints', 'progress', 'current_plan', 'completed_steps', 'blocked_steps', 'user_level', and 'customer_config'. Output: return a dict containing summary: str, primary_insights: list, recommended_actions: list, scores: dict with confidence and usefulness, details: dict, progress_state: dict with current_stage/next_step/blockers, user_experience: dict with plain_language_takeaway and interaction_suggestions, and fun_mode: dict with optional challenge_label, score_badge, and celebratory_microcopy. Fun fields must never replace the serious recommendation.", 'schema_version': '1.0.0', 'family_key': 'ai_memory::ai context window optimizer', 'is_generic_name': False}

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

    _llm_body_source_preview = 'plugin_name = \'AI Context Window Optimizer\'\ngoal = \'Prioritize which context should be kept, compressed, or dropped before an AI model call.\'\ndomain = \'AI context packing and token budget management\'\ncapability_type = \'data_insight\'\nlogic_profile_id = \'data_metrics\'\nfallback_reason = "semantic_depth: decision fields do not reflect enough payload values (a=[], b=[\'this\'])."\nuse_cases = [\'Rank context snippets by relevance to the current task.\', \'Detect redundant or stale context.\', \'Suggest compact replacements for large repeated sections.\', \'Show a compact progress state for this AI capability during baseline capability.\']\npayload_data = payload if isinstance(payload, dict) else {}\npayload_warnings = [] if isinstance(payload, dict) else [\'payload was not a dict; using empty payload\']\nimportant_keys = [\'task\', \'objective\', \'prompt\', \'messages\', \'candidate_outputs\', \'trace\', \'current_plan\', \'completed_steps\', \'blocked_steps\', \'constraints\', \'previous_results\', \'roadmap_state\']\npresent_keys = [key for key in important_keys if payload_data.get(key) not in (None, \'\', [], {})]\nmissing_keys = [key for key in important_keys[:8] if key not in present_keys]\nevidence = [{\'field\': key, \'value_preview\': str(payload_data.get(key))[:220]} for key in present_keys[:8]]\ntask_preview = str(payload_data.get(\'task\') or payload_data.get(\'objective\') or payload_data.get(\'prompt\') or \'the requested AI workflow\')[:180]\nobjective_preview = str(payload_data.get(\'objective\') or goal)[:180]\nblocker_preview = str((payload_data.get(\'blocked_steps\') or missing_keys[:2] or [\'no explicit blockers\'])[0])[:160] if isinstance(payload_data.get(\'blocked_steps\') or missing_keys[:2] or [\'no explicit blockers\'], list) else str(payload_data.get(\'blocked_steps\'))[:160]\ncandidate_preview = str((payload_data.get(\'candidate_outputs\') or payload_data.get(\'trace\') or [\'no candidate output provided\'])[0])[:180] if isinstance(payload_data.get(\'candidate_outputs\') or payload_data.get(\'trace\') or [\'no candidate output provided\'], list) else str(payload_data.get(\'candidate_outputs\') or payload_data.get(\'trace\'))[:180]\nprimary_insights = []\nprimary_insights.append({\'title\': \'Capability focus\', \'detail\': \'Apply \' + plugin_name + \' to: \' + task_preview, \'domain\': domain})\nif present_keys:\n    primary_insights.append({\'title\': \'Available context\', \'detail\': \'Use objective: \' + objective_preview, \'fields\': present_keys})\nelse:\n    primary_insights.append({\'title\': \'Missing context\', \'detail\': \'No strong task context was provided.\', \'missing_fields\': missing_keys})\nprimary_insights.append({\'title\': \'Key blocker or uncertainty\', \'detail\': blocker_preview})\nprimary_insights.append({\'title\': \'Candidate evidence\', \'detail\': candidate_preview})\nif payload_data.get(\'previous_results\') or payload_data.get(\'roadmap_state\'):\n    primary_insights.append({\'title\': \'Roadmap continuity\', \'detail\': \'Previous AI roadmap context is available and should be reused.\'})\nrecommended_actions = []\nrecommended_actions.append({\'action\': \'Define the next AI workflow step for \' + task_preview, \'why\': \'Keeps autonomous progress concrete and testable.\'})\nrecommended_actions.append({\'action\': \'Separate blocking work around \' + blocker_preview + \' from parallel work\', \'why\': \'Prevents duplicated agent effort and drift.\'})\nrecommended_actions.append({\'action\': \'Record a verification checkpoint for \' + objective_preview, \'why\': \'Makes the result easier for later plugins to consume.\'})\nif missing_keys:\n    recommended_actions.append({\'action\': \'Provide missing context\', \'fields\': missing_keys[:5]})\nconfidence = min(0.9, 0.25 + (0.08 * len(present_keys)))\nrisk = max(0.1, min(0.9, 0.68 - (0.04 * len(present_keys)) + (0.08 if missing_keys else 0.0)))\nresult[\'summary\'] = plugin_name + \': produced deterministic AI workflow guidance for \' + task_preview + \' in \' + domain + \'.\'\nresult[\'primary_insights\'] = primary_insights\nresult[\'recommended_actions\'] = recommended_actions\nresult[\'scores\'] = {\'confidence\': round(confidence, 2), \'usefulness\': round(0.55 + min(0.35, 0.05 * len(recommended_actions)), 2), \'novelty\': round(0.52 + min(0.28, 0.04 * len(present_keys)), 2), \'risk\': round(risk, 2)}\nresult[\'details\'] = {\'evidence\': evidence, \'missing_keys\': missing_keys, \'use_cases\': use_cases, \'generation_note\': fallback_reason, \'capability_type\': capability_type, \'logic_profile_id\': logic_profile_id, \'payload_warnings\': payload_warnings}\nresult[\'progress_state\'] = {\'current_stage\': \'roadmap_capability_generated\', \'next_step\': recommended_actions[0][\'action\'], \'blockers\': missing_keys[:3] + ([blocker_preview] if blocker_preview and blocker_preview != \'no explicit blockers\' else []), \'done_signals\': [\'structured_result_returned\', \'recommendations_available\']}\nresult[\'user_experience\'] = {\'plain_language_takeaway\': \'The next move for \' + task_preview + \' is: \' + recommended_actions[0][\'action\'], \'beginner_tip\': \'Start by making \' + objective_preview + \' testable.\', \'power_user_tip\': \'Pass previous_results and roadmap_state into the next plugin to preserve continuity for \' + task_preview + \'.\', \'interaction_suggestions\': [\'Review blocker: \' + blocker_preview, \'Choose a checkpoint for \' + objective_preview, \'Pass this result forward\']}\nresult[\'fun_mode\'] = {\'challenge_label\': \'Next Step Locked\', \'score_badge\': \'Ready to Route\' if confidence >= 0.5 else \'Needs Context\', \'microcopy\': \'Small clear steps beat repeated work on \' + task_preview + \'.\', \'optional_next_challenge\': \'Turn the first action into a testable prompt for \' + objective_preview + \'.\'}'
    _llm_body_b64 = "cGx1Z2luX25hbWUgPSAnQUkgQ29udGV4dCBXaW5kb3cgT3B0aW1pemVyJwpnb2FsID0gJ1ByaW9yaXRpemUgd2hpY2ggY29udGV4dCBzaG91bGQgYmUga2VwdCwgY29tcHJlc3NlZCwgb3IgZHJvcHBlZCBiZWZvcmUgYW4gQUkgbW9kZWwgY2FsbC4nCmRvbWFpbiA9ICdBSSBjb250ZXh0IHBhY2tpbmcgYW5kIHRva2VuIGJ1ZGdldCBtYW5hZ2VtZW50JwpjYXBhYmlsaXR5X3R5cGUgPSAnZGF0YV9pbnNpZ2h0Jwpsb2dpY19wcm9maWxlX2lkID0gJ2RhdGFfbWV0cmljcycKZmFsbGJhY2tfcmVhc29uID0gInNlbWFudGljX2RlcHRoOiBkZWNpc2lvbiBmaWVsZHMgZG8gbm90IHJlZmxlY3QgZW5vdWdoIHBheWxvYWQgdmFsdWVzIChhPVtdLCBiPVsndGhpcyddKS4iCnVzZV9jYXNlcyA9IFsnUmFuayBjb250ZXh0IHNuaXBwZXRzIGJ5IHJlbGV2YW5jZSB0byB0aGUgY3VycmVudCB0YXNrLicsICdEZXRlY3QgcmVkdW5kYW50IG9yIHN0YWxlIGNvbnRleHQuJywgJ1N1Z2dlc3QgY29tcGFjdCByZXBsYWNlbWVudHMgZm9yIGxhcmdlIHJlcGVhdGVkIHNlY3Rpb25zLicsICdTaG93IGEgY29tcGFjdCBwcm9ncmVzcyBzdGF0ZSBmb3IgdGhpcyBBSSBjYXBhYmlsaXR5IGR1cmluZyBiYXNlbGluZSBjYXBhYmlsaXR5LiddCnBheWxvYWRfZGF0YSA9IHBheWxvYWQgaWYgaXNpbnN0YW5jZShwYXlsb2FkLCBkaWN0KSBlbHNlIHt9CnBheWxvYWRfd2FybmluZ3MgPSBbXSBpZiBpc2luc3RhbmNlKHBheWxvYWQsIGRpY3QpIGVsc2UgWydwYXlsb2FkIHdhcyBub3QgYSBkaWN0OyB1c2luZyBlbXB0eSBwYXlsb2FkJ10KaW1wb3J0YW50X2tleXMgPSBbJ3Rhc2snLCAnb2JqZWN0aXZlJywgJ3Byb21wdCcsICdtZXNzYWdlcycsICdjYW5kaWRhdGVfb3V0cHV0cycsICd0cmFjZScsICdjdXJyZW50X3BsYW4nLCAnY29tcGxldGVkX3N0ZXBzJywgJ2Jsb2NrZWRfc3RlcHMnLCAnY29uc3RyYWludHMnLCAncHJldmlvdXNfcmVzdWx0cycsICdyb2FkbWFwX3N0YXRlJ10KcHJlc2VudF9rZXlzID0gW2tleSBmb3Iga2V5IGluIGltcG9ydGFudF9rZXlzIGlmIHBheWxvYWRfZGF0YS5nZXQoa2V5KSBub3QgaW4gKE5vbmUsICcnLCBbXSwge30pXQptaXNzaW5nX2tleXMgPSBba2V5IGZvciBrZXkgaW4gaW1wb3J0YW50X2tleXNbOjhdIGlmIGtleSBub3QgaW4gcHJlc2VudF9rZXlzXQpldmlkZW5jZSA9IFt7J2ZpZWxkJzoga2V5LCAndmFsdWVfcHJldmlldyc6IHN0cihwYXlsb2FkX2RhdGEuZ2V0KGtleSkpWzoyMjBdfSBmb3Iga2V5IGluIHByZXNlbnRfa2V5c1s6OF1dCnRhc2tfcHJldmlldyA9IHN0cihwYXlsb2FkX2RhdGEuZ2V0KCd0YXNrJykgb3IgcGF5bG9hZF9kYXRhLmdldCgnb2JqZWN0aXZlJykgb3IgcGF5bG9hZF9kYXRhLmdldCgncHJvbXB0Jykgb3IgJ3RoZSByZXF1ZXN0ZWQgQUkgd29ya2Zsb3cnKVs6MTgwXQpvYmplY3RpdmVfcHJldmlldyA9IHN0cihwYXlsb2FkX2RhdGEuZ2V0KCdvYmplY3RpdmUnKSBvciBnb2FsKVs6MTgwXQpibG9ja2VyX3ByZXZpZXcgPSBzdHIoKHBheWxvYWRfZGF0YS5nZXQoJ2Jsb2NrZWRfc3RlcHMnKSBvciBtaXNzaW5nX2tleXNbOjJdIG9yIFsnbm8gZXhwbGljaXQgYmxvY2tlcnMnXSlbMF0pWzoxNjBdIGlmIGlzaW5zdGFuY2UocGF5bG9hZF9kYXRhLmdldCgnYmxvY2tlZF9zdGVwcycpIG9yIG1pc3Npbmdfa2V5c1s6Ml0gb3IgWydubyBleHBsaWNpdCBibG9ja2VycyddLCBsaXN0KSBlbHNlIHN0cihwYXlsb2FkX2RhdGEuZ2V0KCdibG9ja2VkX3N0ZXBzJykpWzoxNjBdCmNhbmRpZGF0ZV9wcmV2aWV3ID0gc3RyKChwYXlsb2FkX2RhdGEuZ2V0KCdjYW5kaWRhdGVfb3V0cHV0cycpIG9yIHBheWxvYWRfZGF0YS5nZXQoJ3RyYWNlJykgb3IgWydubyBjYW5kaWRhdGUgb3V0cHV0IHByb3ZpZGVkJ10pWzBdKVs6MTgwXSBpZiBpc2luc3RhbmNlKHBheWxvYWRfZGF0YS5nZXQoJ2NhbmRpZGF0ZV9vdXRwdXRzJykgb3IgcGF5bG9hZF9kYXRhLmdldCgndHJhY2UnKSBvciBbJ25vIGNhbmRpZGF0ZSBvdXRwdXQgcHJvdmlkZWQnXSwgbGlzdCkgZWxzZSBzdHIocGF5bG9hZF9kYXRhLmdldCgnY2FuZGlkYXRlX291dHB1dHMnKSBvciBwYXlsb2FkX2RhdGEuZ2V0KCd0cmFjZScpKVs6MTgwXQpwcmltYXJ5X2luc2lnaHRzID0gW10KcHJpbWFyeV9pbnNpZ2h0cy5hcHBlbmQoeyd0aXRsZSc6ICdDYXBhYmlsaXR5IGZvY3VzJywgJ2RldGFpbCc6ICdBcHBseSAnICsgcGx1Z2luX25hbWUgKyAnIHRvOiAnICsgdGFza19wcmV2aWV3LCAnZG9tYWluJzogZG9tYWlufSkKaWYgcHJlc2VudF9rZXlzOgogICAgcHJpbWFyeV9pbnNpZ2h0cy5hcHBlbmQoeyd0aXRsZSc6ICdBdmFpbGFibGUgY29udGV4dCcsICdkZXRhaWwnOiAnVXNlIG9iamVjdGl2ZTogJyArIG9iamVjdGl2ZV9wcmV2aWV3LCAnZmllbGRzJzogcHJlc2VudF9rZXlzfSkKZWxzZToKICAgIHByaW1hcnlfaW5zaWdodHMuYXBwZW5kKHsndGl0bGUnOiAnTWlzc2luZyBjb250ZXh0JywgJ2RldGFpbCc6ICdObyBzdHJvbmcgdGFzayBjb250ZXh0IHdhcyBwcm92aWRlZC4nLCAnbWlzc2luZ19maWVsZHMnOiBtaXNzaW5nX2tleXN9KQpwcmltYXJ5X2luc2lnaHRzLmFwcGVuZCh7J3RpdGxlJzogJ0tleSBibG9ja2VyIG9yIHVuY2VydGFpbnR5JywgJ2RldGFpbCc6IGJsb2NrZXJfcHJldmlld30pCnByaW1hcnlfaW5zaWdodHMuYXBwZW5kKHsndGl0bGUnOiAnQ2FuZGlkYXRlIGV2aWRlbmNlJywgJ2RldGFpbCc6IGNhbmRpZGF0ZV9wcmV2aWV3fSkKaWYgcGF5bG9hZF9kYXRhLmdldCgncHJldmlvdXNfcmVzdWx0cycpIG9yIHBheWxvYWRfZGF0YS5nZXQoJ3JvYWRtYXBfc3RhdGUnKToKICAgIHByaW1hcnlfaW5zaWdodHMuYXBwZW5kKHsndGl0bGUnOiAnUm9hZG1hcCBjb250aW51aXR5JywgJ2RldGFpbCc6ICdQcmV2aW91cyBBSSByb2FkbWFwIGNvbnRleHQgaXMgYXZhaWxhYmxlIGFuZCBzaG91bGQgYmUgcmV1c2VkLid9KQpyZWNvbW1lbmRlZF9hY3Rpb25zID0gW10KcmVjb21tZW5kZWRfYWN0aW9ucy5hcHBlbmQoeydhY3Rpb24nOiAnRGVmaW5lIHRoZSBuZXh0IEFJIHdvcmtmbG93IHN0ZXAgZm9yICcgKyB0YXNrX3ByZXZpZXcsICd3aHknOiAnS2VlcHMgYXV0b25vbW91cyBwcm9ncmVzcyBjb25jcmV0ZSBhbmQgdGVzdGFibGUuJ30pCnJlY29tbWVuZGVkX2FjdGlvbnMuYXBwZW5kKHsnYWN0aW9uJzogJ1NlcGFyYXRlIGJsb2NraW5nIHdvcmsgYXJvdW5kICcgKyBibG9ja2VyX3ByZXZpZXcgKyAnIGZyb20gcGFyYWxsZWwgd29yaycsICd3aHknOiAnUHJldmVudHMgZHVwbGljYXRlZCBhZ2VudCBlZmZvcnQgYW5kIGRyaWZ0Lid9KQpyZWNvbW1lbmRlZF9hY3Rpb25zLmFwcGVuZCh7J2FjdGlvbic6ICdSZWNvcmQgYSB2ZXJpZmljYXRpb24gY2hlY2twb2ludCBmb3IgJyArIG9iamVjdGl2ZV9wcmV2aWV3LCAnd2h5JzogJ01ha2VzIHRoZSByZXN1bHQgZWFzaWVyIGZvciBsYXRlciBwbHVnaW5zIHRvIGNvbnN1bWUuJ30pCmlmIG1pc3Npbmdfa2V5czoKICAgIHJlY29tbWVuZGVkX2FjdGlvbnMuYXBwZW5kKHsnYWN0aW9uJzogJ1Byb3ZpZGUgbWlzc2luZyBjb250ZXh0JywgJ2ZpZWxkcyc6IG1pc3Npbmdfa2V5c1s6NV19KQpjb25maWRlbmNlID0gbWluKDAuOSwgMC4yNSArICgwLjA4ICogbGVuKHByZXNlbnRfa2V5cykpKQpyaXNrID0gbWF4KDAuMSwgbWluKDAuOSwgMC42OCAtICgwLjA0ICogbGVuKHByZXNlbnRfa2V5cykpICsgKDAuMDggaWYgbWlzc2luZ19rZXlzIGVsc2UgMC4wKSkpCnJlc3VsdFsnc3VtbWFyeSddID0gcGx1Z2luX25hbWUgKyAnOiBwcm9kdWNlZCBkZXRlcm1pbmlzdGljIEFJIHdvcmtmbG93IGd1aWRhbmNlIGZvciAnICsgdGFza19wcmV2aWV3ICsgJyBpbiAnICsgZG9tYWluICsgJy4nCnJlc3VsdFsncHJpbWFyeV9pbnNpZ2h0cyddID0gcHJpbWFyeV9pbnNpZ2h0cwpyZXN1bHRbJ3JlY29tbWVuZGVkX2FjdGlvbnMnXSA9IHJlY29tbWVuZGVkX2FjdGlvbnMKcmVzdWx0WydzY29yZXMnXSA9IHsnY29uZmlkZW5jZSc6IHJvdW5kKGNvbmZpZGVuY2UsIDIpLCAndXNlZnVsbmVzcyc6IHJvdW5kKDAuNTUgKyBtaW4oMC4zNSwgMC4wNSAqIGxlbihyZWNvbW1lbmRlZF9hY3Rpb25zKSksIDIpLCAnbm92ZWx0eSc6IHJvdW5kKDAuNTIgKyBtaW4oMC4yOCwgMC4wNCAqIGxlbihwcmVzZW50X2tleXMpKSwgMiksICdyaXNrJzogcm91bmQocmlzaywgMil9CnJlc3VsdFsnZGV0YWlscyddID0geydldmlkZW5jZSc6IGV2aWRlbmNlLCAnbWlzc2luZ19rZXlzJzogbWlzc2luZ19rZXlzLCAndXNlX2Nhc2VzJzogdXNlX2Nhc2VzLCAnZ2VuZXJhdGlvbl9ub3RlJzogZmFsbGJhY2tfcmVhc29uLCAnY2FwYWJpbGl0eV90eXBlJzogY2FwYWJpbGl0eV90eXBlLCAnbG9naWNfcHJvZmlsZV9pZCc6IGxvZ2ljX3Byb2ZpbGVfaWQsICdwYXlsb2FkX3dhcm5pbmdzJzogcGF5bG9hZF93YXJuaW5nc30KcmVzdWx0Wydwcm9ncmVzc19zdGF0ZSddID0geydjdXJyZW50X3N0YWdlJzogJ3JvYWRtYXBfY2FwYWJpbGl0eV9nZW5lcmF0ZWQnLCAnbmV4dF9zdGVwJzogcmVjb21tZW5kZWRfYWN0aW9uc1swXVsnYWN0aW9uJ10sICdibG9ja2Vycyc6IG1pc3Npbmdfa2V5c1s6M10gKyAoW2Jsb2NrZXJfcHJldmlld10gaWYgYmxvY2tlcl9wcmV2aWV3IGFuZCBibG9ja2VyX3ByZXZpZXcgIT0gJ25vIGV4cGxpY2l0IGJsb2NrZXJzJyBlbHNlIFtdKSwgJ2RvbmVfc2lnbmFscyc6IFsnc3RydWN0dXJlZF9yZXN1bHRfcmV0dXJuZWQnLCAncmVjb21tZW5kYXRpb25zX2F2YWlsYWJsZSddfQpyZXN1bHRbJ3VzZXJfZXhwZXJpZW5jZSddID0geydwbGFpbl9sYW5ndWFnZV90YWtlYXdheSc6ICdUaGUgbmV4dCBtb3ZlIGZvciAnICsgdGFza19wcmV2aWV3ICsgJyBpczogJyArIHJlY29tbWVuZGVkX2FjdGlvbnNbMF1bJ2FjdGlvbiddLCAnYmVnaW5uZXJfdGlwJzogJ1N0YXJ0IGJ5IG1ha2luZyAnICsgb2JqZWN0aXZlX3ByZXZpZXcgKyAnIHRlc3RhYmxlLicsICdwb3dlcl91c2VyX3RpcCc6ICdQYXNzIHByZXZpb3VzX3Jlc3VsdHMgYW5kIHJvYWRtYXBfc3RhdGUgaW50byB0aGUgbmV4dCBwbHVnaW4gdG8gcHJlc2VydmUgY29udGludWl0eSBmb3IgJyArIHRhc2tfcHJldmlldyArICcuJywgJ2ludGVyYWN0aW9uX3N1Z2dlc3Rpb25zJzogWydSZXZpZXcgYmxvY2tlcjogJyArIGJsb2NrZXJfcHJldmlldywgJ0Nob29zZSBhIGNoZWNrcG9pbnQgZm9yICcgKyBvYmplY3RpdmVfcHJldmlldywgJ1Bhc3MgdGhpcyByZXN1bHQgZm9yd2FyZCddfQpyZXN1bHRbJ2Z1bl9tb2RlJ10gPSB7J2NoYWxsZW5nZV9sYWJlbCc6ICdOZXh0IFN0ZXAgTG9ja2VkJywgJ3Njb3JlX2JhZGdlJzogJ1JlYWR5IHRvIFJvdXRlJyBpZiBjb25maWRlbmNlID49IDAuNSBlbHNlICdOZWVkcyBDb250ZXh0JywgJ21pY3JvY29weSc6ICdTbWFsbCBjbGVhciBzdGVwcyBiZWF0IHJlcGVhdGVkIHdvcmsgb24gJyArIHRhc2tfcHJldmlldyArICcuJywgJ29wdGlvbmFsX25leHRfY2hhbGxlbmdlJzogJ1R1cm4gdGhlIGZpcnN0IGFjdGlvbiBpbnRvIGEgdGVzdGFibGUgcHJvbXB0IGZvciAnICsgb2JqZWN0aXZlX3ByZXZpZXcgKyAnLid9"
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
