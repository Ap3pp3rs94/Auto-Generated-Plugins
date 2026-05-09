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

    _llm_body_source_preview = "# Validate payload is a dict and collect relevant fields\nif not isinstance(payload, dict):\n    result['summary'] = 'Invalid input: Payload must be a dictionary.'\nelse:\n    task = payload.get('task')\n    objective = payload.get('objective')\n    prompt = payload.get('prompt')\n    messages = payload.get('messages', [])\n    candidate_outputs = payload.get('candidate_outputs', [])\n    trace = payload.get('trace')\n    current_plan = payload.get('current_plan')\n    completed_steps = payload.get('completed_steps', [])\n    blocked_steps = payload.get('blocked_steps', [])\n\n# Build evidence notes from present fields\nevidence_notes = []\nif task:\n    evidence_notes.append({'field': 'Task', 'value': task})\nif objective:\n    evidence_notes.append({'field': 'Objective', 'value': objective})\nif prompt:\n    evidence_notes.append({'field': 'Prompt', 'value': prompt})\n\n# Create primary insights specific to this plugin goal\nprimary_insights = []\nif not messages:\n    primary_insights.append('No conversation history found.')\nif candidate_outputs and len(candidate_outputs) > 1:\n    primary_insights.append('Multiple model outputs detected.')\n\n# Create recommended actions with clear next steps\nrecommended_actions = []\nif task and objective:\n    recommended_actions.append({'action': 'Rewrite prompt', 'description': f'Use the task and objective to create a specific, testable instruction.'})\nif not messages:\n    recommended_actions.append({'action': 'Start conversation', 'description': 'Begin interacting with the model to gather more information.'})\n\n# Compute scores: confidence, usefulness, novelty, risk\nscores = {}\nif evidence_notes:\n    scores['confidence'] = 0.8\nelse:\n    scores['confidence'] = 0.2\n\nif recommended_actions:\n    scores['usefulness'] = 0.9\nelse:\n    scores['usefulness'] = 0.1\n\n# Populate progress state, user experience, fun mode, and details\nprogress_state = {'current_stage': 'Analysis', 'next_step': 'Rewrite prompt', 'blockers': [], 'done_signals': []}\nuser_experience = {\n    'plain_language_takeaway': 'Your task and objective are clear. Now, let\\'s rewrite the prompt.',\n    'beginner_tip': 'Remember to keep your prompt specific and testable.',\n    'power_user_tip': 'Consider using more advanced techniques for generating prompts.'\n}\nfun_mode = {'challenge_label': 'Clear Path', 'score_badge': 'Ready to Run', 'microcopy': 'You\\'re making great progress!', 'optional_next_challenge': 'Try rewriting the prompt with a different model output.'}\n\n# Assign final data to result\nresult['summary'] = 'AI Prompt Refinement Engine: Analyzing task instructions and producing clearer, safer, more testable prompts.'\nresult['primary_insights'] = primary_insights\nresult['recommended_actions'] = recommended_actions\nresult['scores'] = scores\nresult['details'] = evidence_notes\nresult['progress_state'] = progress_state\nresult['user_experience'] = user_experience\nresult['fun_mode'] = fun_mode"
    _llm_body_b64 = "IyBWYWxpZGF0ZSBwYXlsb2FkIGlzIGEgZGljdCBhbmQgY29sbGVjdCByZWxldmFudCBmaWVsZHMKaWYgbm90IGlzaW5zdGFuY2UocGF5bG9hZCwgZGljdCk6CiAgICByZXN1bHRbJ3N1bW1hcnknXSA9ICdJbnZhbGlkIGlucHV0OiBQYXlsb2FkIG11c3QgYmUgYSBkaWN0aW9uYXJ5LicKZWxzZToKICAgIHRhc2sgPSBwYXlsb2FkLmdldCgndGFzaycpCiAgICBvYmplY3RpdmUgPSBwYXlsb2FkLmdldCgnb2JqZWN0aXZlJykKICAgIHByb21wdCA9IHBheWxvYWQuZ2V0KCdwcm9tcHQnKQogICAgbWVzc2FnZXMgPSBwYXlsb2FkLmdldCgnbWVzc2FnZXMnLCBbXSkKICAgIGNhbmRpZGF0ZV9vdXRwdXRzID0gcGF5bG9hZC5nZXQoJ2NhbmRpZGF0ZV9vdXRwdXRzJywgW10pCiAgICB0cmFjZSA9IHBheWxvYWQuZ2V0KCd0cmFjZScpCiAgICBjdXJyZW50X3BsYW4gPSBwYXlsb2FkLmdldCgnY3VycmVudF9wbGFuJykKICAgIGNvbXBsZXRlZF9zdGVwcyA9IHBheWxvYWQuZ2V0KCdjb21wbGV0ZWRfc3RlcHMnLCBbXSkKICAgIGJsb2NrZWRfc3RlcHMgPSBwYXlsb2FkLmdldCgnYmxvY2tlZF9zdGVwcycsIFtdKQoKIyBCdWlsZCBldmlkZW5jZSBub3RlcyBmcm9tIHByZXNlbnQgZmllbGRzCmV2aWRlbmNlX25vdGVzID0gW10KaWYgdGFzazoKICAgIGV2aWRlbmNlX25vdGVzLmFwcGVuZCh7J2ZpZWxkJzogJ1Rhc2snLCAndmFsdWUnOiB0YXNrfSkKaWYgb2JqZWN0aXZlOgogICAgZXZpZGVuY2Vfbm90ZXMuYXBwZW5kKHsnZmllbGQnOiAnT2JqZWN0aXZlJywgJ3ZhbHVlJzogb2JqZWN0aXZlfSkKaWYgcHJvbXB0OgogICAgZXZpZGVuY2Vfbm90ZXMuYXBwZW5kKHsnZmllbGQnOiAnUHJvbXB0JywgJ3ZhbHVlJzogcHJvbXB0fSkKCiMgQ3JlYXRlIHByaW1hcnkgaW5zaWdodHMgc3BlY2lmaWMgdG8gdGhpcyBwbHVnaW4gZ29hbApwcmltYXJ5X2luc2lnaHRzID0gW10KaWYgbm90IG1lc3NhZ2VzOgogICAgcHJpbWFyeV9pbnNpZ2h0cy5hcHBlbmQoJ05vIGNvbnZlcnNhdGlvbiBoaXN0b3J5IGZvdW5kLicpCmlmIGNhbmRpZGF0ZV9vdXRwdXRzIGFuZCBsZW4oY2FuZGlkYXRlX291dHB1dHMpID4gMToKICAgIHByaW1hcnlfaW5zaWdodHMuYXBwZW5kKCdNdWx0aXBsZSBtb2RlbCBvdXRwdXRzIGRldGVjdGVkLicpCgojIENyZWF0ZSByZWNvbW1lbmRlZCBhY3Rpb25zIHdpdGggY2xlYXIgbmV4dCBzdGVwcwpyZWNvbW1lbmRlZF9hY3Rpb25zID0gW10KaWYgdGFzayBhbmQgb2JqZWN0aXZlOgogICAgcmVjb21tZW5kZWRfYWN0aW9ucy5hcHBlbmQoeydhY3Rpb24nOiAnUmV3cml0ZSBwcm9tcHQnLCAnZGVzY3JpcHRpb24nOiBmJ1VzZSB0aGUgdGFzayBhbmQgb2JqZWN0aXZlIHRvIGNyZWF0ZSBhIHNwZWNpZmljLCB0ZXN0YWJsZSBpbnN0cnVjdGlvbi4nfSkKaWYgbm90IG1lc3NhZ2VzOgogICAgcmVjb21tZW5kZWRfYWN0aW9ucy5hcHBlbmQoeydhY3Rpb24nOiAnU3RhcnQgY29udmVyc2F0aW9uJywgJ2Rlc2NyaXB0aW9uJzogJ0JlZ2luIGludGVyYWN0aW5nIHdpdGggdGhlIG1vZGVsIHRvIGdhdGhlciBtb3JlIGluZm9ybWF0aW9uLid9KQoKIyBDb21wdXRlIHNjb3JlczogY29uZmlkZW5jZSwgdXNlZnVsbmVzcywgbm92ZWx0eSwgcmlzawpzY29yZXMgPSB7fQppZiBldmlkZW5jZV9ub3RlczoKICAgIHNjb3Jlc1snY29uZmlkZW5jZSddID0gMC44CmVsc2U6CiAgICBzY29yZXNbJ2NvbmZpZGVuY2UnXSA9IDAuMgoKaWYgcmVjb21tZW5kZWRfYWN0aW9uczoKICAgIHNjb3Jlc1sndXNlZnVsbmVzcyddID0gMC45CmVsc2U6CiAgICBzY29yZXNbJ3VzZWZ1bG5lc3MnXSA9IDAuMQoKIyBQb3B1bGF0ZSBwcm9ncmVzcyBzdGF0ZSwgdXNlciBleHBlcmllbmNlLCBmdW4gbW9kZSwgYW5kIGRldGFpbHMKcHJvZ3Jlc3Nfc3RhdGUgPSB7J2N1cnJlbnRfc3RhZ2UnOiAnQW5hbHlzaXMnLCAnbmV4dF9zdGVwJzogJ1Jld3JpdGUgcHJvbXB0JywgJ2Jsb2NrZXJzJzogW10sICdkb25lX3NpZ25hbHMnOiBbXX0KdXNlcl9leHBlcmllbmNlID0gewogICAgJ3BsYWluX2xhbmd1YWdlX3Rha2Vhd2F5JzogJ1lvdXIgdGFzayBhbmQgb2JqZWN0aXZlIGFyZSBjbGVhci4gTm93LCBsZXRcJ3MgcmV3cml0ZSB0aGUgcHJvbXB0LicsCiAgICAnYmVnaW5uZXJfdGlwJzogJ1JlbWVtYmVyIHRvIGtlZXAgeW91ciBwcm9tcHQgc3BlY2lmaWMgYW5kIHRlc3RhYmxlLicsCiAgICAncG93ZXJfdXNlcl90aXAnOiAnQ29uc2lkZXIgdXNpbmcgbW9yZSBhZHZhbmNlZCB0ZWNobmlxdWVzIGZvciBnZW5lcmF0aW5nIHByb21wdHMuJwp9CmZ1bl9tb2RlID0geydjaGFsbGVuZ2VfbGFiZWwnOiAnQ2xlYXIgUGF0aCcsICdzY29yZV9iYWRnZSc6ICdSZWFkeSB0byBSdW4nLCAnbWljcm9jb3B5JzogJ1lvdVwncmUgbWFraW5nIGdyZWF0IHByb2dyZXNzIScsICdvcHRpb25hbF9uZXh0X2NoYWxsZW5nZSc6ICdUcnkgcmV3cml0aW5nIHRoZSBwcm9tcHQgd2l0aCBhIGRpZmZlcmVudCBtb2RlbCBvdXRwdXQuJ30KCiMgQXNzaWduIGZpbmFsIGRhdGEgdG8gcmVzdWx0CnJlc3VsdFsnc3VtbWFyeSddID0gJ0FJIFByb21wdCBSZWZpbmVtZW50IEVuZ2luZTogQW5hbHl6aW5nIHRhc2sgaW5zdHJ1Y3Rpb25zIGFuZCBwcm9kdWNpbmcgY2xlYXJlciwgc2FmZXIsIG1vcmUgdGVzdGFibGUgcHJvbXB0cy4nCnJlc3VsdFsncHJpbWFyeV9pbnNpZ2h0cyddID0gcHJpbWFyeV9pbnNpZ2h0cwpyZXN1bHRbJ3JlY29tbWVuZGVkX2FjdGlvbnMnXSA9IHJlY29tbWVuZGVkX2FjdGlvbnMKcmVzdWx0WydzY29yZXMnXSA9IHNjb3JlcwpyZXN1bHRbJ2RldGFpbHMnXSA9IGV2aWRlbmNlX25vdGVzCnJlc3VsdFsncHJvZ3Jlc3Nfc3RhdGUnXSA9IHByb2dyZXNzX3N0YXRlCnJlc3VsdFsndXNlcl9leHBlcmllbmNlJ10gPSB1c2VyX2V4cGVyaWVuY2UKcmVzdWx0WydmdW5fbW9kZSddID0gZnVuX21vZGU="
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
