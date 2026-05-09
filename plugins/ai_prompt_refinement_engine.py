from __future__ import annotations

"""
Auto-generated Francis plugin module.

THIS FILE IS GENERATED. Manual edits may be overwritten by the factory.

Plugin: AI Prompt Refinement Engine
Slug: ai_prompt_refinement_engine
"""

from typing import Any, Dict, Optional

__all__ = ["invoke", "_run_core_logic", "SkillContext"]

# ---------------------------------------------------------------------------
# Plugin metadata (used by Station C, registry, and tooling)
# ---------------------------------------------------------------------------

_PLUGIN_NAME: str = 'AI Prompt Refinement Engine'
_PLUGIN_SLUG: str = 'ai_prompt_refinement_engine'
_PLUGIN_CATEGORY: str = 'ai_prompting'
_PLUGIN_VERSION: str = '0.1.0'
_PLUGIN_GOAL: str = 'Analyze task instructions and produce clearer, safer, more testable prompts.'
_PLUGIN_TAGS = ['ai', 'prompting', 'instructions', 'quality', 'autonomous_factory', 'ai_progress', 'phase_1']
_PLUGIN_OWNER_ID = 'francis-factory'
_PLUGIN_CAPABILITY_TYPE = 'enrichment'
_PLUGIN_INTENDED_DOMAIN = 'AI prompt engineering and instruction quality'
_PLUGIN_USE_CASES = ['Rewrite vague prompts into specific, testable instructions.', 'Identify missing constraints, inputs, outputs, and acceptance criteria.', 'Suggest prompt variants for different model sizes or latency budgets.', 'Show a compact progress state for this AI capability during baseline capability.', 'Return user-facing guidance that is useful, concise, and safe to act on.', 'Avoid duplicating existing AI plugin behavior; identify what is unique about this capability.']
_PLUGIN_RESULT_SCHEMA_VERSION: str = '1.0.0'

# Lightweight manifest for discovery/registry.
_PLUGIN_MANIFEST = {'name': 'AI Prompt Refinement Engine', 'slug': 'ai_prompt_refinement_engine', 'goal': 'Analyze task instructions and produce clearer, safer, more testable prompts.', 'category': 'ai_prompting', 'tags': ['ai', 'prompting', 'instructions', 'quality', 'autonomous_factory', 'ai_progress', 'phase_1'], 'version': '0.1.0', 'capability_type': 'enrichment', 'intended_domain': 'AI prompt engineering and instruction quality', 'owner_id': 'francis-factory', 'use_cases': ['Rewrite vague prompts into specific, testable instructions.', 'Identify missing constraints, inputs, outputs, and acceptance criteria.', 'Suggest prompt variants for different model sizes or latency budgets.', 'Show a compact progress state for this AI capability during baseline capability.', 'Return user-facing guidance that is useful, concise, and safe to act on.', 'Avoid duplicating existing AI plugin behavior; identify what is unique about this capability.'], 'primary_use_case': 'Rewrite vague prompts into specific, testable instructions.', 'problem_statement': 'Francis needs a focused AI plugin for AI prompt engineering and instruction quality. The plugin must turn messy user notes, model outputs, traces, or workflow state into structured, actionable AI assistance. It should improve autonomous progress by making the next step obvious, reducing duplicated work, and exposing risks before they become failures. The plugin must stay deterministic, avoid hidden external side effects, and make its reasoning inspectable through concise details and scores.', 'primary_inputs': 'A payload dict that may contain task, objective, prompt, conversation, artifacts, candidate_outputs, traces, rubric, constraints, user_level, current_plan, completed_steps, blocked_steps, source_notes, and optional customer_config.', 'primary_outputs': 'A normalized result dict with summary, primary_insights, recommended_actions, scores, details, progress_state, user_experience, fun_mode, and machine-readable diagnostics.', 'constraints': 'Do not execute tools, browse, mutate files, call external APIs, or claim facts not present in the payload. Prefer deterministic analysis. If data is missing, say what is missing and return a useful fallback. Keep recommendations concrete. Avoid creating a capability that duplicates another AI roadmap plugin.', 'example_use_cases': ['A user asks Francis to improve an AI workflow related to AI prompt engineering and instruction quality.', 'A long-running autonomous run needs a checkpoint summary and the next best action.', 'An operator wants a scorecard that separates hard failures from polish improvements.', 'A beginner wants the result explained in plain language without losing technical accuracy.', 'A power user wants structured JSON they can pipe into another agent or dashboard.'], 'io_contract': "Input: payload is a dict. Important optional keys include 'task', 'objective', 'prompt', 'conversation', 'messages', 'candidate_outputs', 'trace', 'rubric', 'constraints', 'progress', 'current_plan', 'completed_steps', 'blocked_steps', 'user_level', and 'customer_config'. Output: return a dict containing summary: str, primary_insights: list, recommended_actions: list, scores: dict with confidence and usefulness, details: dict, progress_state: dict with current_stage/next_step/blockers, user_experience: dict with plain_language_takeaway and interaction_suggestions, and fun_mode: dict with optional challenge_label, score_badge, and celebratory_microcopy. Fun fields must never replace the serious recommendation.", 'schema_version': '1.0.0', 'family_key': 'ai_prompting::ai prompt refinement engine', 'is_generic_name': False}

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

    _llm_body_source_preview = "plugin_name = 'AI Prompt Refinement Engine'\ngoal = 'Analyze task instructions and produce clearer, safer, more testable prompts.'\ndomain = 'AI prompt engineering and instruction quality'\ncapability_type = 'enrichment'\nlogic_profile_id = 'semantic_repair'\nfallback_reason = 'semantic_depth: decision fields do not reflect enough payload values (a=[], b=[]).'\nuse_cases = ['Rewrite vague prompts into specific, testable instructions.', 'Identify missing constraints, inputs, outputs, and acceptance criteria.', 'Suggest prompt variants for different model sizes or latency budgets.', 'Show a compact progress state for this AI capability during baseline capability.']\npayload_data = payload if isinstance(payload, dict) else {}\npayload_warnings = [] if isinstance(payload, dict) else ['payload was not a dict; using empty payload']\nimportant_keys = ['task', 'objective', 'prompt', 'messages', 'candidate_outputs', 'trace', 'current_plan', 'completed_steps', 'blocked_steps', 'constraints', 'previous_results', 'roadmap_state']\npresent_keys = [key for key in important_keys if payload_data.get(key) not in (None, '', [], {})]\nmissing_keys = [key for key in important_keys[:8] if key not in present_keys]\nevidence = [{'field': key, 'value_preview': str(payload_data.get(key))[:220]} for key in present_keys[:8]]\ntask_preview = str(payload_data.get('task') or payload_data.get('objective') or payload_data.get('prompt') or 'the requested AI workflow')[:180]\nobjective_preview = str(payload_data.get('objective') or goal)[:180]\nblocker_preview = str((payload_data.get('blocked_steps') or missing_keys[:2] or ['no explicit blockers'])[0])[:160] if isinstance(payload_data.get('blocked_steps') or missing_keys[:2] or ['no explicit blockers'], list) else str(payload_data.get('blocked_steps'))[:160]\ncandidate_preview = str((payload_data.get('candidate_outputs') or payload_data.get('trace') or ['no candidate output provided'])[0])[:180] if isinstance(payload_data.get('candidate_outputs') or payload_data.get('trace') or ['no candidate output provided'], list) else str(payload_data.get('candidate_outputs') or payload_data.get('trace'))[:180]\nprimary_insights = []\nprimary_insights.append({'title': 'Capability focus', 'detail': 'Apply ' + plugin_name + ' to: ' + task_preview, 'domain': domain})\nif present_keys:\n    primary_insights.append({'title': 'Available context', 'detail': 'Use objective: ' + objective_preview, 'fields': present_keys})\nelse:\n    primary_insights.append({'title': 'Missing context', 'detail': 'No strong task context was provided.', 'missing_fields': missing_keys})\nprimary_insights.append({'title': 'Key blocker or uncertainty', 'detail': blocker_preview})\nprimary_insights.append({'title': 'Candidate evidence', 'detail': candidate_preview})\nif payload_data.get('previous_results') or payload_data.get('roadmap_state'):\n    primary_insights.append({'title': 'Roadmap continuity', 'detail': 'Previous AI roadmap context is available and should be reused.'})\nrecommended_actions = []\nrecommended_actions.append({'action': 'Define the next AI workflow step for ' + task_preview, 'why': 'Keeps autonomous progress concrete and testable.'})\nrecommended_actions.append({'action': 'Separate blocking work around ' + blocker_preview + ' from parallel work', 'why': 'Prevents duplicated agent effort and drift.'})\nrecommended_actions.append({'action': 'Record a verification checkpoint for ' + objective_preview, 'why': 'Makes the result easier for later plugins to consume.'})\nif missing_keys:\n    recommended_actions.append({'action': 'Provide missing context', 'fields': missing_keys[:5]})\nconfidence = min(0.9, 0.25 + (0.08 * len(present_keys)))\nrisk = max(0.1, min(0.9, 0.68 - (0.04 * len(present_keys)) + (0.08 if missing_keys else 0.0)))\nresult['summary'] = plugin_name + ': produced deterministic AI workflow guidance for ' + task_preview + ' in ' + domain + '.'\nresult['primary_insights'] = primary_insights\nresult['recommended_actions'] = recommended_actions\nresult['scores'] = {'confidence': round(confidence, 2), 'usefulness': round(0.55 + min(0.35, 0.05 * len(recommended_actions)), 2), 'novelty': round(0.52 + min(0.28, 0.04 * len(present_keys)), 2), 'risk': round(risk, 2)}\nresult['details'] = {'evidence': evidence, 'missing_keys': missing_keys, 'use_cases': use_cases, 'generation_note': fallback_reason, 'capability_type': capability_type, 'logic_profile_id': logic_profile_id, 'payload_warnings': payload_warnings}\nresult['progress_state'] = {'current_stage': 'roadmap_capability_generated', 'next_step': recommended_actions[0]['action'], 'blockers': missing_keys[:3] + ([blocker_preview] if blocker_preview and blocker_preview != 'no explicit blockers' else []), 'done_signals': ['structured_result_returned', 'recommendations_available']}\nresult['user_experience'] = {'plain_language_takeaway': 'The next move for ' + task_preview + ' is: ' + recommended_actions[0]['action'], 'beginner_tip': 'Start by making ' + objective_preview + ' testable.', 'power_user_tip': 'Pass previous_results and roadmap_state into the next plugin to preserve continuity for ' + task_preview + '.', 'interaction_suggestions': ['Review blocker: ' + blocker_preview, 'Choose a checkpoint for ' + objective_preview, 'Pass this result forward']}\nresult['fun_mode'] = {'challenge_label': 'Next Step Locked', 'score_badge': 'Ready to Route' if confidence >= 0.5 else 'Needs Context', 'microcopy': 'Small clear steps beat repeated work on ' + task_preview + '.', 'optional_next_challenge': 'Turn the first action into a testable prompt for ' + objective_preview + '.'}"
    _llm_body_b64 = "cGx1Z2luX25hbWUgPSAnQUkgUHJvbXB0IFJlZmluZW1lbnQgRW5naW5lJwpnb2FsID0gJ0FuYWx5emUgdGFzayBpbnN0cnVjdGlvbnMgYW5kIHByb2R1Y2UgY2xlYXJlciwgc2FmZXIsIG1vcmUgdGVzdGFibGUgcHJvbXB0cy4nCmRvbWFpbiA9ICdBSSBwcm9tcHQgZW5naW5lZXJpbmcgYW5kIGluc3RydWN0aW9uIHF1YWxpdHknCmNhcGFiaWxpdHlfdHlwZSA9ICdlbnJpY2htZW50Jwpsb2dpY19wcm9maWxlX2lkID0gJ3NlbWFudGljX3JlcGFpcicKZmFsbGJhY2tfcmVhc29uID0gJ3NlbWFudGljX2RlcHRoOiBkZWNpc2lvbiBmaWVsZHMgZG8gbm90IHJlZmxlY3QgZW5vdWdoIHBheWxvYWQgdmFsdWVzIChhPVtdLCBiPVtdKS4nCnVzZV9jYXNlcyA9IFsnUmV3cml0ZSB2YWd1ZSBwcm9tcHRzIGludG8gc3BlY2lmaWMsIHRlc3RhYmxlIGluc3RydWN0aW9ucy4nLCAnSWRlbnRpZnkgbWlzc2luZyBjb25zdHJhaW50cywgaW5wdXRzLCBvdXRwdXRzLCBhbmQgYWNjZXB0YW5jZSBjcml0ZXJpYS4nLCAnU3VnZ2VzdCBwcm9tcHQgdmFyaWFudHMgZm9yIGRpZmZlcmVudCBtb2RlbCBzaXplcyBvciBsYXRlbmN5IGJ1ZGdldHMuJywgJ1Nob3cgYSBjb21wYWN0IHByb2dyZXNzIHN0YXRlIGZvciB0aGlzIEFJIGNhcGFiaWxpdHkgZHVyaW5nIGJhc2VsaW5lIGNhcGFiaWxpdHkuJ10KcGF5bG9hZF9kYXRhID0gcGF5bG9hZCBpZiBpc2luc3RhbmNlKHBheWxvYWQsIGRpY3QpIGVsc2Uge30KcGF5bG9hZF93YXJuaW5ncyA9IFtdIGlmIGlzaW5zdGFuY2UocGF5bG9hZCwgZGljdCkgZWxzZSBbJ3BheWxvYWQgd2FzIG5vdCBhIGRpY3Q7IHVzaW5nIGVtcHR5IHBheWxvYWQnXQppbXBvcnRhbnRfa2V5cyA9IFsndGFzaycsICdvYmplY3RpdmUnLCAncHJvbXB0JywgJ21lc3NhZ2VzJywgJ2NhbmRpZGF0ZV9vdXRwdXRzJywgJ3RyYWNlJywgJ2N1cnJlbnRfcGxhbicsICdjb21wbGV0ZWRfc3RlcHMnLCAnYmxvY2tlZF9zdGVwcycsICdjb25zdHJhaW50cycsICdwcmV2aW91c19yZXN1bHRzJywgJ3JvYWRtYXBfc3RhdGUnXQpwcmVzZW50X2tleXMgPSBba2V5IGZvciBrZXkgaW4gaW1wb3J0YW50X2tleXMgaWYgcGF5bG9hZF9kYXRhLmdldChrZXkpIG5vdCBpbiAoTm9uZSwgJycsIFtdLCB7fSldCm1pc3Npbmdfa2V5cyA9IFtrZXkgZm9yIGtleSBpbiBpbXBvcnRhbnRfa2V5c1s6OF0gaWYga2V5IG5vdCBpbiBwcmVzZW50X2tleXNdCmV2aWRlbmNlID0gW3snZmllbGQnOiBrZXksICd2YWx1ZV9wcmV2aWV3Jzogc3RyKHBheWxvYWRfZGF0YS5nZXQoa2V5KSlbOjIyMF19IGZvciBrZXkgaW4gcHJlc2VudF9rZXlzWzo4XV0KdGFza19wcmV2aWV3ID0gc3RyKHBheWxvYWRfZGF0YS5nZXQoJ3Rhc2snKSBvciBwYXlsb2FkX2RhdGEuZ2V0KCdvYmplY3RpdmUnKSBvciBwYXlsb2FkX2RhdGEuZ2V0KCdwcm9tcHQnKSBvciAndGhlIHJlcXVlc3RlZCBBSSB3b3JrZmxvdycpWzoxODBdCm9iamVjdGl2ZV9wcmV2aWV3ID0gc3RyKHBheWxvYWRfZGF0YS5nZXQoJ29iamVjdGl2ZScpIG9yIGdvYWwpWzoxODBdCmJsb2NrZXJfcHJldmlldyA9IHN0cigocGF5bG9hZF9kYXRhLmdldCgnYmxvY2tlZF9zdGVwcycpIG9yIG1pc3Npbmdfa2V5c1s6Ml0gb3IgWydubyBleHBsaWNpdCBibG9ja2VycyddKVswXSlbOjE2MF0gaWYgaXNpbnN0YW5jZShwYXlsb2FkX2RhdGEuZ2V0KCdibG9ja2VkX3N0ZXBzJykgb3IgbWlzc2luZ19rZXlzWzoyXSBvciBbJ25vIGV4cGxpY2l0IGJsb2NrZXJzJ10sIGxpc3QpIGVsc2Ugc3RyKHBheWxvYWRfZGF0YS5nZXQoJ2Jsb2NrZWRfc3RlcHMnKSlbOjE2MF0KY2FuZGlkYXRlX3ByZXZpZXcgPSBzdHIoKHBheWxvYWRfZGF0YS5nZXQoJ2NhbmRpZGF0ZV9vdXRwdXRzJykgb3IgcGF5bG9hZF9kYXRhLmdldCgndHJhY2UnKSBvciBbJ25vIGNhbmRpZGF0ZSBvdXRwdXQgcHJvdmlkZWQnXSlbMF0pWzoxODBdIGlmIGlzaW5zdGFuY2UocGF5bG9hZF9kYXRhLmdldCgnY2FuZGlkYXRlX291dHB1dHMnKSBvciBwYXlsb2FkX2RhdGEuZ2V0KCd0cmFjZScpIG9yIFsnbm8gY2FuZGlkYXRlIG91dHB1dCBwcm92aWRlZCddLCBsaXN0KSBlbHNlIHN0cihwYXlsb2FkX2RhdGEuZ2V0KCdjYW5kaWRhdGVfb3V0cHV0cycpIG9yIHBheWxvYWRfZGF0YS5nZXQoJ3RyYWNlJykpWzoxODBdCnByaW1hcnlfaW5zaWdodHMgPSBbXQpwcmltYXJ5X2luc2lnaHRzLmFwcGVuZCh7J3RpdGxlJzogJ0NhcGFiaWxpdHkgZm9jdXMnLCAnZGV0YWlsJzogJ0FwcGx5ICcgKyBwbHVnaW5fbmFtZSArICcgdG86ICcgKyB0YXNrX3ByZXZpZXcsICdkb21haW4nOiBkb21haW59KQppZiBwcmVzZW50X2tleXM6CiAgICBwcmltYXJ5X2luc2lnaHRzLmFwcGVuZCh7J3RpdGxlJzogJ0F2YWlsYWJsZSBjb250ZXh0JywgJ2RldGFpbCc6ICdVc2Ugb2JqZWN0aXZlOiAnICsgb2JqZWN0aXZlX3ByZXZpZXcsICdmaWVsZHMnOiBwcmVzZW50X2tleXN9KQplbHNlOgogICAgcHJpbWFyeV9pbnNpZ2h0cy5hcHBlbmQoeyd0aXRsZSc6ICdNaXNzaW5nIGNvbnRleHQnLCAnZGV0YWlsJzogJ05vIHN0cm9uZyB0YXNrIGNvbnRleHQgd2FzIHByb3ZpZGVkLicsICdtaXNzaW5nX2ZpZWxkcyc6IG1pc3Npbmdfa2V5c30pCnByaW1hcnlfaW5zaWdodHMuYXBwZW5kKHsndGl0bGUnOiAnS2V5IGJsb2NrZXIgb3IgdW5jZXJ0YWludHknLCAnZGV0YWlsJzogYmxvY2tlcl9wcmV2aWV3fSkKcHJpbWFyeV9pbnNpZ2h0cy5hcHBlbmQoeyd0aXRsZSc6ICdDYW5kaWRhdGUgZXZpZGVuY2UnLCAnZGV0YWlsJzogY2FuZGlkYXRlX3ByZXZpZXd9KQppZiBwYXlsb2FkX2RhdGEuZ2V0KCdwcmV2aW91c19yZXN1bHRzJykgb3IgcGF5bG9hZF9kYXRhLmdldCgncm9hZG1hcF9zdGF0ZScpOgogICAgcHJpbWFyeV9pbnNpZ2h0cy5hcHBlbmQoeyd0aXRsZSc6ICdSb2FkbWFwIGNvbnRpbnVpdHknLCAnZGV0YWlsJzogJ1ByZXZpb3VzIEFJIHJvYWRtYXAgY29udGV4dCBpcyBhdmFpbGFibGUgYW5kIHNob3VsZCBiZSByZXVzZWQuJ30pCnJlY29tbWVuZGVkX2FjdGlvbnMgPSBbXQpyZWNvbW1lbmRlZF9hY3Rpb25zLmFwcGVuZCh7J2FjdGlvbic6ICdEZWZpbmUgdGhlIG5leHQgQUkgd29ya2Zsb3cgc3RlcCBmb3IgJyArIHRhc2tfcHJldmlldywgJ3doeSc6ICdLZWVwcyBhdXRvbm9tb3VzIHByb2dyZXNzIGNvbmNyZXRlIGFuZCB0ZXN0YWJsZS4nfSkKcmVjb21tZW5kZWRfYWN0aW9ucy5hcHBlbmQoeydhY3Rpb24nOiAnU2VwYXJhdGUgYmxvY2tpbmcgd29yayBhcm91bmQgJyArIGJsb2NrZXJfcHJldmlldyArICcgZnJvbSBwYXJhbGxlbCB3b3JrJywgJ3doeSc6ICdQcmV2ZW50cyBkdXBsaWNhdGVkIGFnZW50IGVmZm9ydCBhbmQgZHJpZnQuJ30pCnJlY29tbWVuZGVkX2FjdGlvbnMuYXBwZW5kKHsnYWN0aW9uJzogJ1JlY29yZCBhIHZlcmlmaWNhdGlvbiBjaGVja3BvaW50IGZvciAnICsgb2JqZWN0aXZlX3ByZXZpZXcsICd3aHknOiAnTWFrZXMgdGhlIHJlc3VsdCBlYXNpZXIgZm9yIGxhdGVyIHBsdWdpbnMgdG8gY29uc3VtZS4nfSkKaWYgbWlzc2luZ19rZXlzOgogICAgcmVjb21tZW5kZWRfYWN0aW9ucy5hcHBlbmQoeydhY3Rpb24nOiAnUHJvdmlkZSBtaXNzaW5nIGNvbnRleHQnLCAnZmllbGRzJzogbWlzc2luZ19rZXlzWzo1XX0pCmNvbmZpZGVuY2UgPSBtaW4oMC45LCAwLjI1ICsgKDAuMDggKiBsZW4ocHJlc2VudF9rZXlzKSkpCnJpc2sgPSBtYXgoMC4xLCBtaW4oMC45LCAwLjY4IC0gKDAuMDQgKiBsZW4ocHJlc2VudF9rZXlzKSkgKyAoMC4wOCBpZiBtaXNzaW5nX2tleXMgZWxzZSAwLjApKSkKcmVzdWx0WydzdW1tYXJ5J10gPSBwbHVnaW5fbmFtZSArICc6IHByb2R1Y2VkIGRldGVybWluaXN0aWMgQUkgd29ya2Zsb3cgZ3VpZGFuY2UgZm9yICcgKyB0YXNrX3ByZXZpZXcgKyAnIGluICcgKyBkb21haW4gKyAnLicKcmVzdWx0WydwcmltYXJ5X2luc2lnaHRzJ10gPSBwcmltYXJ5X2luc2lnaHRzCnJlc3VsdFsncmVjb21tZW5kZWRfYWN0aW9ucyddID0gcmVjb21tZW5kZWRfYWN0aW9ucwpyZXN1bHRbJ3Njb3JlcyddID0geydjb25maWRlbmNlJzogcm91bmQoY29uZmlkZW5jZSwgMiksICd1c2VmdWxuZXNzJzogcm91bmQoMC41NSArIG1pbigwLjM1LCAwLjA1ICogbGVuKHJlY29tbWVuZGVkX2FjdGlvbnMpKSwgMiksICdub3ZlbHR5Jzogcm91bmQoMC41MiArIG1pbigwLjI4LCAwLjA0ICogbGVuKHByZXNlbnRfa2V5cykpLCAyKSwgJ3Jpc2snOiByb3VuZChyaXNrLCAyKX0KcmVzdWx0WydkZXRhaWxzJ10gPSB7J2V2aWRlbmNlJzogZXZpZGVuY2UsICdtaXNzaW5nX2tleXMnOiBtaXNzaW5nX2tleXMsICd1c2VfY2FzZXMnOiB1c2VfY2FzZXMsICdnZW5lcmF0aW9uX25vdGUnOiBmYWxsYmFja19yZWFzb24sICdjYXBhYmlsaXR5X3R5cGUnOiBjYXBhYmlsaXR5X3R5cGUsICdsb2dpY19wcm9maWxlX2lkJzogbG9naWNfcHJvZmlsZV9pZCwgJ3BheWxvYWRfd2FybmluZ3MnOiBwYXlsb2FkX3dhcm5pbmdzfQpyZXN1bHRbJ3Byb2dyZXNzX3N0YXRlJ10gPSB7J2N1cnJlbnRfc3RhZ2UnOiAncm9hZG1hcF9jYXBhYmlsaXR5X2dlbmVyYXRlZCcsICduZXh0X3N0ZXAnOiByZWNvbW1lbmRlZF9hY3Rpb25zWzBdWydhY3Rpb24nXSwgJ2Jsb2NrZXJzJzogbWlzc2luZ19rZXlzWzozXSArIChbYmxvY2tlcl9wcmV2aWV3XSBpZiBibG9ja2VyX3ByZXZpZXcgYW5kIGJsb2NrZXJfcHJldmlldyAhPSAnbm8gZXhwbGljaXQgYmxvY2tlcnMnIGVsc2UgW10pLCAnZG9uZV9zaWduYWxzJzogWydzdHJ1Y3R1cmVkX3Jlc3VsdF9yZXR1cm5lZCcsICdyZWNvbW1lbmRhdGlvbnNfYXZhaWxhYmxlJ119CnJlc3VsdFsndXNlcl9leHBlcmllbmNlJ10gPSB7J3BsYWluX2xhbmd1YWdlX3Rha2Vhd2F5JzogJ1RoZSBuZXh0IG1vdmUgZm9yICcgKyB0YXNrX3ByZXZpZXcgKyAnIGlzOiAnICsgcmVjb21tZW5kZWRfYWN0aW9uc1swXVsnYWN0aW9uJ10sICdiZWdpbm5lcl90aXAnOiAnU3RhcnQgYnkgbWFraW5nICcgKyBvYmplY3RpdmVfcHJldmlldyArICcgdGVzdGFibGUuJywgJ3Bvd2VyX3VzZXJfdGlwJzogJ1Bhc3MgcHJldmlvdXNfcmVzdWx0cyBhbmQgcm9hZG1hcF9zdGF0ZSBpbnRvIHRoZSBuZXh0IHBsdWdpbiB0byBwcmVzZXJ2ZSBjb250aW51aXR5IGZvciAnICsgdGFza19wcmV2aWV3ICsgJy4nLCAnaW50ZXJhY3Rpb25fc3VnZ2VzdGlvbnMnOiBbJ1JldmlldyBibG9ja2VyOiAnICsgYmxvY2tlcl9wcmV2aWV3LCAnQ2hvb3NlIGEgY2hlY2twb2ludCBmb3IgJyArIG9iamVjdGl2ZV9wcmV2aWV3LCAnUGFzcyB0aGlzIHJlc3VsdCBmb3J3YXJkJ119CnJlc3VsdFsnZnVuX21vZGUnXSA9IHsnY2hhbGxlbmdlX2xhYmVsJzogJ05leHQgU3RlcCBMb2NrZWQnLCAnc2NvcmVfYmFkZ2UnOiAnUmVhZHkgdG8gUm91dGUnIGlmIGNvbmZpZGVuY2UgPj0gMC41IGVsc2UgJ05lZWRzIENvbnRleHQnLCAnbWljcm9jb3B5JzogJ1NtYWxsIGNsZWFyIHN0ZXBzIGJlYXQgcmVwZWF0ZWQgd29yayBvbiAnICsgdGFza19wcmV2aWV3ICsgJy4nLCAnb3B0aW9uYWxfbmV4dF9jaGFsbGVuZ2UnOiAnVHVybiB0aGUgZmlyc3QgYWN0aW9uIGludG8gYSB0ZXN0YWJsZSBwcm9tcHQgZm9yICcgKyBvYmplY3RpdmVfcHJldmlldyArICcuJ30="
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
