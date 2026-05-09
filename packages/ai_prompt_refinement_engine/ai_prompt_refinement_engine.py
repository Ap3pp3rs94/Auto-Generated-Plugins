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
_PLUGIN_VERSION: str = '0.1.2'
_PLUGIN_GOAL: str = 'Analyze task instructions and produce clearer, safer, more testable prompts.'
_PLUGIN_TAGS = ['ai', 'prompting', 'instructions', 'quality', 'autonomous_factory', 'ai_progress', 'phase_1']
_PLUGIN_OWNER_ID = 'francis-factory'
_PLUGIN_CAPABILITY_TYPE = 'enrichment'
_PLUGIN_INTENDED_DOMAIN = 'AI prompt engineering and instruction quality'
_PLUGIN_USE_CASES = ['Rewrite vague prompts into specific, testable instructions.', 'Identify missing constraints, inputs, outputs, and acceptance criteria.', 'Suggest prompt variants for different model sizes or latency budgets.', 'Show a compact progress state for this AI capability during baseline capability.', 'Return user-facing guidance that is useful, concise, and safe to act on.', 'Avoid duplicating existing AI plugin behavior; identify what is unique about this capability.']
_PLUGIN_RESULT_SCHEMA_VERSION: str = '1.0.0'

# Lightweight manifest for discovery/registry.
_PLUGIN_MANIFEST = {'name': 'AI Prompt Refinement Engine', 'slug': 'ai_prompt_refinement_engine', 'goal': 'Analyze task instructions and produce clearer, safer, more testable prompts.', 'category': 'ai_prompting', 'tags': ['ai', 'prompting', 'instructions', 'quality', 'autonomous_factory', 'ai_progress', 'phase_1'], 'version': '0.1.2', 'capability_type': 'enrichment', 'intended_domain': 'AI prompt engineering and instruction quality', 'owner_id': 'francis-factory', 'use_cases': ['Rewrite vague prompts into specific, testable instructions.', 'Identify missing constraints, inputs, outputs, and acceptance criteria.', 'Suggest prompt variants for different model sizes or latency budgets.', 'Show a compact progress state for this AI capability during baseline capability.', 'Return user-facing guidance that is useful, concise, and safe to act on.', 'Avoid duplicating existing AI plugin behavior; identify what is unique about this capability.'], 'primary_use_case': 'Rewrite vague prompts into specific, testable instructions.', 'problem_statement': 'Francis needs a focused AI plugin for AI prompt engineering and instruction quality. The plugin must turn messy user notes, model outputs, traces, or workflow state into structured, actionable AI assistance. It should improve autonomous progress by making the next step obvious, reducing duplicated work, and exposing risks before they become failures. The plugin must stay deterministic, avoid hidden external side effects, and make its reasoning inspectable through concise details and scores.', 'primary_inputs': 'A payload dict that may contain task, objective, prompt, conversation, artifacts, candidate_outputs, traces, rubric, constraints, user_level, current_plan, completed_steps, blocked_steps, source_notes, and optional customer_config.', 'primary_outputs': 'A normalized result dict with summary, primary_insights, recommended_actions, scores, details, progress_state, user_experience, fun_mode, and machine-readable diagnostics.', 'constraints': 'Do not execute tools, browse, mutate files, call external APIs, or claim facts not present in the payload. Prefer deterministic analysis. If data is missing, say what is missing and return a useful fallback. Keep recommendations concrete. Avoid creating a capability that duplicates another AI roadmap plugin.', 'example_use_cases': ['A user asks Francis to improve an AI workflow related to AI prompt engineering and instruction quality.', 'A long-running autonomous run needs a checkpoint summary and the next best action.', 'An operator wants a scorecard that separates hard failures from polish improvements.', 'A beginner wants the result explained in plain language without losing technical accuracy.', 'A power user wants structured JSON they can pipe into another agent or dashboard.'], 'io_contract': "Input: payload is a dict. Important optional keys include 'task', 'objective', 'prompt', 'conversation', 'messages', 'candidate_outputs', 'trace', 'rubric', 'constraints', 'progress', 'current_plan', 'completed_steps', 'blocked_steps', 'user_level', and 'customer_config'. Output: return a dict containing summary: str, primary_insights: list, recommended_actions: list, scores: dict with confidence and usefulness, details: dict, progress_state: dict with current_stage/next_step/blockers, user_experience: dict with plain_language_takeaway and interaction_suggestions, and fun_mode: dict with optional challenge_label, score_badge, and celebratory_microcopy. Fun fields must never replace the serious recommendation.", 'schema_version': '1.0.0', 'family_key': 'ai_prompting::ai prompt refinement engine', 'is_generic_name': False}

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

    _llm_body_source_preview = "plugin_name = 'AI Prompt Refinement Engine'\ngoal = 'Analyze task instructions and produce clearer, safer, more testable prompts.'\ndomain = 'AI prompt engineering and instruction quality'\ncapability_type = 'enrichment'\nlogic_profile_id = 'prompt_refinement_semantic_repair'\nfallback_reason = 'capability-specific prompt refinement repair'\npayload_data = payload if isinstance(payload, dict) else {}\nraw_prompt = str(payload_data.get('prompt') or payload_data.get('instruction') or payload_data.get('task') or '').strip()\ntask_text = str(payload_data.get('task') or '').strip()\nobjective_text = str(payload_data.get('objective') or '').strip()\nconstraints = payload_data.get('constraints') if isinstance(payload_data.get('constraints'), list) else []\naudience = str(payload_data.get('audience') or payload_data.get('user_level') or '').strip()\noutput_format = str(payload_data.get('output_format') or payload_data.get('format') or '').strip()\ntone = str((payload_data.get('customer_config') or {}).get('tone') if isinstance(payload_data.get('customer_config'), dict) else payload_data.get('tone') or '').strip()\nprompt_lower = raw_prompt.lower()\nvague_markers = ['make it better', 'good', 'nice', 'stuff', 'something', 'things', 'improve this', 'fix it', 'do it', 'help me']\nidentified_vagueness = [marker for marker in vague_markers if marker in prompt_lower]\nif raw_prompt and len(raw_prompt.split()) < 8:\n    identified_vagueness.append('too short to communicate constraints')\nmissing_constraints = []\nif not objective_text:\n    missing_constraints.append({'category': 'objective', 'suggestion': 'State the concrete outcome the model should optimize for.'})\nif not audience:\n    missing_constraints.append({'category': 'audience', 'suggestion': 'Name the target reader or operator skill level.'})\nif not output_format:\n    missing_constraints.append({'category': 'format', 'suggestion': 'Specify the required output format, sections, or schema.'})\nif not constraints:\n    missing_constraints.append({'category': 'acceptance_criteria', 'suggestion': 'Add success criteria and hard constraints.'})\nif 'test' not in prompt_lower and 'verify' not in prompt_lower:\n    missing_constraints.append({'category': 'verification', 'suggestion': 'Say how the answer should be checked or tested.'})\nbase_task = task_text or raw_prompt or 'Complete the requested AI task'\nobjective_clause = objective_text or 'produce a useful, verifiable result'\naudience_clause = audience or 'the intended user'\nformat_clause = output_format or 'a concise structured response with assumptions, steps, and checks'\nconstraint_clause = '; '.join(str(item) for item in constraints[:4]) if constraints else 'Do not invent facts; list assumptions; include acceptance criteria.'\nrefined_prompt = (\n    'You are helping with: ' + base_task + '\\n'\n    'Objective: ' + objective_clause + '\\n'\n    'Audience: ' + audience_clause + '\\n'\n    'Output format: ' + format_clause + '\\n'\n    'Constraints: ' + constraint_clause + '\\n'\n    'Before finalizing, identify missing information, state assumptions, and provide verification checks.'\n)\nstrict_rewrite = refined_prompt + '\\nReturn only the requested artifact plus a short validation checklist.'\nexploratory_rewrite = refined_prompt + '\\nIf requirements are ambiguous, ask up to three targeted clarification questions before drafting.'\nrewrites = [\n    {'label': 'structured_refinement', 'rewrite': refined_prompt},\n    {'label': 'strict_execution', 'rewrite': strict_rewrite},\n    {'label': 'clarifying_mode', 'rewrite': exploratory_rewrite},\n]\nprimary_insights = [\n    {'title': 'Original prompt analyzed', 'detail': raw_prompt or 'No explicit prompt was provided.'},\n    {'title': 'Vagueness found', 'items': identified_vagueness or ['No common vague phrase found; still check constraints.']},\n    {'title': 'Missing constraints', 'items': missing_constraints},\n]\nrecommended_actions = [\n    {'action': 'Use structured_refinement rewrite', 'rewrite': refined_prompt},\n    {'action': 'Add missing constraints', 'items': missing_constraints[:5]},\n    {'action': 'Choose strict_execution when the model should not ask follow-up questions', 'rewrite': strict_rewrite},\n]\nspecificity = max(0.1, 1.0 - (0.12 * len(missing_constraints)) - (0.08 * len(identified_vagueness)))\nconfidence = min(0.92, max(0.25, specificity + (0.08 if raw_prompt else -0.1)))\nresult['summary'] = 'Refined prompt for: ' + base_task[:160]\nresult['primary_insights'] = primary_insights\nresult['recommended_actions'] = recommended_actions\nresult['scores'] = {'confidence': round(confidence, 2), 'usefulness': 0.9, 'novelty': 0.72, 'risk': round(1.0 - confidence, 2), 'specificity': round(specificity, 2)}\nresult['details'] = {'original_prompt': raw_prompt, 'identified_vagueness': identified_vagueness, 'missing_constraints': missing_constraints, 'rewrites': rewrites, 'refined_prompt': refined_prompt, 'generation_note': fallback_reason, 'capability_type': capability_type, 'logic_profile_id': logic_profile_id}\nresult['progress_state'] = {'current_stage': 'prompt_refined', 'next_step': 'Review the structured_refinement rewrite against the missing constraints.', 'blockers': [item['category'] for item in missing_constraints[:4]], 'done_signals': ['rewrites_available', 'missing_constraints_identified']}\nresult['user_experience'] = {'plain_language_takeaway': 'The prompt now names the task, objective, audience, output format, constraints, and verification checks.', 'beginner_tip': 'Use the structured rewrite first; add any missing audience or format details before running it.', 'power_user_tip': 'Use strict_execution for automation and clarifying_mode when discovery is safer.', 'interaction_suggestions': ['Compare the three rewrites', 'Fill missing constraints', 'Run the strict rewrite through prompt tests']}\nresult['fun_mode'] = {'challenge_label': 'Prompt Sharpened', 'score_badge': 'Specificity ' + str(round(specificity, 2)), 'microcopy': 'A vague prompt became a testable instruction.', 'optional_next_challenge': 'Add one measurable acceptance criterion before sending it to a model.'}"
    _llm_body_b64 = "cGx1Z2luX25hbWUgPSAnQUkgUHJvbXB0IFJlZmluZW1lbnQgRW5naW5lJwpnb2FsID0gJ0FuYWx5emUgdGFzayBpbnN0cnVjdGlvbnMgYW5kIHByb2R1Y2UgY2xlYXJlciwgc2FmZXIsIG1vcmUgdGVzdGFibGUgcHJvbXB0cy4nCmRvbWFpbiA9ICdBSSBwcm9tcHQgZW5naW5lZXJpbmcgYW5kIGluc3RydWN0aW9uIHF1YWxpdHknCmNhcGFiaWxpdHlfdHlwZSA9ICdlbnJpY2htZW50Jwpsb2dpY19wcm9maWxlX2lkID0gJ3Byb21wdF9yZWZpbmVtZW50X3NlbWFudGljX3JlcGFpcicKZmFsbGJhY2tfcmVhc29uID0gJ2NhcGFiaWxpdHktc3BlY2lmaWMgcHJvbXB0IHJlZmluZW1lbnQgcmVwYWlyJwpwYXlsb2FkX2RhdGEgPSBwYXlsb2FkIGlmIGlzaW5zdGFuY2UocGF5bG9hZCwgZGljdCkgZWxzZSB7fQpyYXdfcHJvbXB0ID0gc3RyKHBheWxvYWRfZGF0YS5nZXQoJ3Byb21wdCcpIG9yIHBheWxvYWRfZGF0YS5nZXQoJ2luc3RydWN0aW9uJykgb3IgcGF5bG9hZF9kYXRhLmdldCgndGFzaycpIG9yICcnKS5zdHJpcCgpCnRhc2tfdGV4dCA9IHN0cihwYXlsb2FkX2RhdGEuZ2V0KCd0YXNrJykgb3IgJycpLnN0cmlwKCkKb2JqZWN0aXZlX3RleHQgPSBzdHIocGF5bG9hZF9kYXRhLmdldCgnb2JqZWN0aXZlJykgb3IgJycpLnN0cmlwKCkKY29uc3RyYWludHMgPSBwYXlsb2FkX2RhdGEuZ2V0KCdjb25zdHJhaW50cycpIGlmIGlzaW5zdGFuY2UocGF5bG9hZF9kYXRhLmdldCgnY29uc3RyYWludHMnKSwgbGlzdCkgZWxzZSBbXQphdWRpZW5jZSA9IHN0cihwYXlsb2FkX2RhdGEuZ2V0KCdhdWRpZW5jZScpIG9yIHBheWxvYWRfZGF0YS5nZXQoJ3VzZXJfbGV2ZWwnKSBvciAnJykuc3RyaXAoKQpvdXRwdXRfZm9ybWF0ID0gc3RyKHBheWxvYWRfZGF0YS5nZXQoJ291dHB1dF9mb3JtYXQnKSBvciBwYXlsb2FkX2RhdGEuZ2V0KCdmb3JtYXQnKSBvciAnJykuc3RyaXAoKQp0b25lID0gc3RyKChwYXlsb2FkX2RhdGEuZ2V0KCdjdXN0b21lcl9jb25maWcnKSBvciB7fSkuZ2V0KCd0b25lJykgaWYgaXNpbnN0YW5jZShwYXlsb2FkX2RhdGEuZ2V0KCdjdXN0b21lcl9jb25maWcnKSwgZGljdCkgZWxzZSBwYXlsb2FkX2RhdGEuZ2V0KCd0b25lJykgb3IgJycpLnN0cmlwKCkKcHJvbXB0X2xvd2VyID0gcmF3X3Byb21wdC5sb3dlcigpCnZhZ3VlX21hcmtlcnMgPSBbJ21ha2UgaXQgYmV0dGVyJywgJ2dvb2QnLCAnbmljZScsICdzdHVmZicsICdzb21ldGhpbmcnLCAndGhpbmdzJywgJ2ltcHJvdmUgdGhpcycsICdmaXggaXQnLCAnZG8gaXQnLCAnaGVscCBtZSddCmlkZW50aWZpZWRfdmFndWVuZXNzID0gW21hcmtlciBmb3IgbWFya2VyIGluIHZhZ3VlX21hcmtlcnMgaWYgbWFya2VyIGluIHByb21wdF9sb3dlcl0KaWYgcmF3X3Byb21wdCBhbmQgbGVuKHJhd19wcm9tcHQuc3BsaXQoKSkgPCA4OgogICAgaWRlbnRpZmllZF92YWd1ZW5lc3MuYXBwZW5kKCd0b28gc2hvcnQgdG8gY29tbXVuaWNhdGUgY29uc3RyYWludHMnKQptaXNzaW5nX2NvbnN0cmFpbnRzID0gW10KaWYgbm90IG9iamVjdGl2ZV90ZXh0OgogICAgbWlzc2luZ19jb25zdHJhaW50cy5hcHBlbmQoeydjYXRlZ29yeSc6ICdvYmplY3RpdmUnLCAnc3VnZ2VzdGlvbic6ICdTdGF0ZSB0aGUgY29uY3JldGUgb3V0Y29tZSB0aGUgbW9kZWwgc2hvdWxkIG9wdGltaXplIGZvci4nfSkKaWYgbm90IGF1ZGllbmNlOgogICAgbWlzc2luZ19jb25zdHJhaW50cy5hcHBlbmQoeydjYXRlZ29yeSc6ICdhdWRpZW5jZScsICdzdWdnZXN0aW9uJzogJ05hbWUgdGhlIHRhcmdldCByZWFkZXIgb3Igb3BlcmF0b3Igc2tpbGwgbGV2ZWwuJ30pCmlmIG5vdCBvdXRwdXRfZm9ybWF0OgogICAgbWlzc2luZ19jb25zdHJhaW50cy5hcHBlbmQoeydjYXRlZ29yeSc6ICdmb3JtYXQnLCAnc3VnZ2VzdGlvbic6ICdTcGVjaWZ5IHRoZSByZXF1aXJlZCBvdXRwdXQgZm9ybWF0LCBzZWN0aW9ucywgb3Igc2NoZW1hLid9KQppZiBub3QgY29uc3RyYWludHM6CiAgICBtaXNzaW5nX2NvbnN0cmFpbnRzLmFwcGVuZCh7J2NhdGVnb3J5JzogJ2FjY2VwdGFuY2VfY3JpdGVyaWEnLCAnc3VnZ2VzdGlvbic6ICdBZGQgc3VjY2VzcyBjcml0ZXJpYSBhbmQgaGFyZCBjb25zdHJhaW50cy4nfSkKaWYgJ3Rlc3QnIG5vdCBpbiBwcm9tcHRfbG93ZXIgYW5kICd2ZXJpZnknIG5vdCBpbiBwcm9tcHRfbG93ZXI6CiAgICBtaXNzaW5nX2NvbnN0cmFpbnRzLmFwcGVuZCh7J2NhdGVnb3J5JzogJ3ZlcmlmaWNhdGlvbicsICdzdWdnZXN0aW9uJzogJ1NheSBob3cgdGhlIGFuc3dlciBzaG91bGQgYmUgY2hlY2tlZCBvciB0ZXN0ZWQuJ30pCmJhc2VfdGFzayA9IHRhc2tfdGV4dCBvciByYXdfcHJvbXB0IG9yICdDb21wbGV0ZSB0aGUgcmVxdWVzdGVkIEFJIHRhc2snCm9iamVjdGl2ZV9jbGF1c2UgPSBvYmplY3RpdmVfdGV4dCBvciAncHJvZHVjZSBhIHVzZWZ1bCwgdmVyaWZpYWJsZSByZXN1bHQnCmF1ZGllbmNlX2NsYXVzZSA9IGF1ZGllbmNlIG9yICd0aGUgaW50ZW5kZWQgdXNlcicKZm9ybWF0X2NsYXVzZSA9IG91dHB1dF9mb3JtYXQgb3IgJ2EgY29uY2lzZSBzdHJ1Y3R1cmVkIHJlc3BvbnNlIHdpdGggYXNzdW1wdGlvbnMsIHN0ZXBzLCBhbmQgY2hlY2tzJwpjb25zdHJhaW50X2NsYXVzZSA9ICc7ICcuam9pbihzdHIoaXRlbSkgZm9yIGl0ZW0gaW4gY29uc3RyYWludHNbOjRdKSBpZiBjb25zdHJhaW50cyBlbHNlICdEbyBub3QgaW52ZW50IGZhY3RzOyBsaXN0IGFzc3VtcHRpb25zOyBpbmNsdWRlIGFjY2VwdGFuY2UgY3JpdGVyaWEuJwpyZWZpbmVkX3Byb21wdCA9ICgKICAgICdZb3UgYXJlIGhlbHBpbmcgd2l0aDogJyArIGJhc2VfdGFzayArICdcbicKICAgICdPYmplY3RpdmU6ICcgKyBvYmplY3RpdmVfY2xhdXNlICsgJ1xuJwogICAgJ0F1ZGllbmNlOiAnICsgYXVkaWVuY2VfY2xhdXNlICsgJ1xuJwogICAgJ091dHB1dCBmb3JtYXQ6ICcgKyBmb3JtYXRfY2xhdXNlICsgJ1xuJwogICAgJ0NvbnN0cmFpbnRzOiAnICsgY29uc3RyYWludF9jbGF1c2UgKyAnXG4nCiAgICAnQmVmb3JlIGZpbmFsaXppbmcsIGlkZW50aWZ5IG1pc3NpbmcgaW5mb3JtYXRpb24sIHN0YXRlIGFzc3VtcHRpb25zLCBhbmQgcHJvdmlkZSB2ZXJpZmljYXRpb24gY2hlY2tzLicKKQpzdHJpY3RfcmV3cml0ZSA9IHJlZmluZWRfcHJvbXB0ICsgJ1xuUmV0dXJuIG9ubHkgdGhlIHJlcXVlc3RlZCBhcnRpZmFjdCBwbHVzIGEgc2hvcnQgdmFsaWRhdGlvbiBjaGVja2xpc3QuJwpleHBsb3JhdG9yeV9yZXdyaXRlID0gcmVmaW5lZF9wcm9tcHQgKyAnXG5JZiByZXF1aXJlbWVudHMgYXJlIGFtYmlndW91cywgYXNrIHVwIHRvIHRocmVlIHRhcmdldGVkIGNsYXJpZmljYXRpb24gcXVlc3Rpb25zIGJlZm9yZSBkcmFmdGluZy4nCnJld3JpdGVzID0gWwogICAgeydsYWJlbCc6ICdzdHJ1Y3R1cmVkX3JlZmluZW1lbnQnLCAncmV3cml0ZSc6IHJlZmluZWRfcHJvbXB0fSwKICAgIHsnbGFiZWwnOiAnc3RyaWN0X2V4ZWN1dGlvbicsICdyZXdyaXRlJzogc3RyaWN0X3Jld3JpdGV9LAogICAgeydsYWJlbCc6ICdjbGFyaWZ5aW5nX21vZGUnLCAncmV3cml0ZSc6IGV4cGxvcmF0b3J5X3Jld3JpdGV9LApdCnByaW1hcnlfaW5zaWdodHMgPSBbCiAgICB7J3RpdGxlJzogJ09yaWdpbmFsIHByb21wdCBhbmFseXplZCcsICdkZXRhaWwnOiByYXdfcHJvbXB0IG9yICdObyBleHBsaWNpdCBwcm9tcHQgd2FzIHByb3ZpZGVkLid9LAogICAgeyd0aXRsZSc6ICdWYWd1ZW5lc3MgZm91bmQnLCAnaXRlbXMnOiBpZGVudGlmaWVkX3ZhZ3VlbmVzcyBvciBbJ05vIGNvbW1vbiB2YWd1ZSBwaHJhc2UgZm91bmQ7IHN0aWxsIGNoZWNrIGNvbnN0cmFpbnRzLiddfSwKICAgIHsndGl0bGUnOiAnTWlzc2luZyBjb25zdHJhaW50cycsICdpdGVtcyc6IG1pc3NpbmdfY29uc3RyYWludHN9LApdCnJlY29tbWVuZGVkX2FjdGlvbnMgPSBbCiAgICB7J2FjdGlvbic6ICdVc2Ugc3RydWN0dXJlZF9yZWZpbmVtZW50IHJld3JpdGUnLCAncmV3cml0ZSc6IHJlZmluZWRfcHJvbXB0fSwKICAgIHsnYWN0aW9uJzogJ0FkZCBtaXNzaW5nIGNvbnN0cmFpbnRzJywgJ2l0ZW1zJzogbWlzc2luZ19jb25zdHJhaW50c1s6NV19LAogICAgeydhY3Rpb24nOiAnQ2hvb3NlIHN0cmljdF9leGVjdXRpb24gd2hlbiB0aGUgbW9kZWwgc2hvdWxkIG5vdCBhc2sgZm9sbG93LXVwIHF1ZXN0aW9ucycsICdyZXdyaXRlJzogc3RyaWN0X3Jld3JpdGV9LApdCnNwZWNpZmljaXR5ID0gbWF4KDAuMSwgMS4wIC0gKDAuMTIgKiBsZW4obWlzc2luZ19jb25zdHJhaW50cykpIC0gKDAuMDggKiBsZW4oaWRlbnRpZmllZF92YWd1ZW5lc3MpKSkKY29uZmlkZW5jZSA9IG1pbigwLjkyLCBtYXgoMC4yNSwgc3BlY2lmaWNpdHkgKyAoMC4wOCBpZiByYXdfcHJvbXB0IGVsc2UgLTAuMSkpKQpyZXN1bHRbJ3N1bW1hcnknXSA9ICdSZWZpbmVkIHByb21wdCBmb3I6ICcgKyBiYXNlX3Rhc2tbOjE2MF0KcmVzdWx0WydwcmltYXJ5X2luc2lnaHRzJ10gPSBwcmltYXJ5X2luc2lnaHRzCnJlc3VsdFsncmVjb21tZW5kZWRfYWN0aW9ucyddID0gcmVjb21tZW5kZWRfYWN0aW9ucwpyZXN1bHRbJ3Njb3JlcyddID0geydjb25maWRlbmNlJzogcm91bmQoY29uZmlkZW5jZSwgMiksICd1c2VmdWxuZXNzJzogMC45LCAnbm92ZWx0eSc6IDAuNzIsICdyaXNrJzogcm91bmQoMS4wIC0gY29uZmlkZW5jZSwgMiksICdzcGVjaWZpY2l0eSc6IHJvdW5kKHNwZWNpZmljaXR5LCAyKX0KcmVzdWx0WydkZXRhaWxzJ10gPSB7J29yaWdpbmFsX3Byb21wdCc6IHJhd19wcm9tcHQsICdpZGVudGlmaWVkX3ZhZ3VlbmVzcyc6IGlkZW50aWZpZWRfdmFndWVuZXNzLCAnbWlzc2luZ19jb25zdHJhaW50cyc6IG1pc3NpbmdfY29uc3RyYWludHMsICdyZXdyaXRlcyc6IHJld3JpdGVzLCAncmVmaW5lZF9wcm9tcHQnOiByZWZpbmVkX3Byb21wdCwgJ2dlbmVyYXRpb25fbm90ZSc6IGZhbGxiYWNrX3JlYXNvbiwgJ2NhcGFiaWxpdHlfdHlwZSc6IGNhcGFiaWxpdHlfdHlwZSwgJ2xvZ2ljX3Byb2ZpbGVfaWQnOiBsb2dpY19wcm9maWxlX2lkfQpyZXN1bHRbJ3Byb2dyZXNzX3N0YXRlJ10gPSB7J2N1cnJlbnRfc3RhZ2UnOiAncHJvbXB0X3JlZmluZWQnLCAnbmV4dF9zdGVwJzogJ1JldmlldyB0aGUgc3RydWN0dXJlZF9yZWZpbmVtZW50IHJld3JpdGUgYWdhaW5zdCB0aGUgbWlzc2luZyBjb25zdHJhaW50cy4nLCAnYmxvY2tlcnMnOiBbaXRlbVsnY2F0ZWdvcnknXSBmb3IgaXRlbSBpbiBtaXNzaW5nX2NvbnN0cmFpbnRzWzo0XV0sICdkb25lX3NpZ25hbHMnOiBbJ3Jld3JpdGVzX2F2YWlsYWJsZScsICdtaXNzaW5nX2NvbnN0cmFpbnRzX2lkZW50aWZpZWQnXX0KcmVzdWx0Wyd1c2VyX2V4cGVyaWVuY2UnXSA9IHsncGxhaW5fbGFuZ3VhZ2VfdGFrZWF3YXknOiAnVGhlIHByb21wdCBub3cgbmFtZXMgdGhlIHRhc2ssIG9iamVjdGl2ZSwgYXVkaWVuY2UsIG91dHB1dCBmb3JtYXQsIGNvbnN0cmFpbnRzLCBhbmQgdmVyaWZpY2F0aW9uIGNoZWNrcy4nLCAnYmVnaW5uZXJfdGlwJzogJ1VzZSB0aGUgc3RydWN0dXJlZCByZXdyaXRlIGZpcnN0OyBhZGQgYW55IG1pc3NpbmcgYXVkaWVuY2Ugb3IgZm9ybWF0IGRldGFpbHMgYmVmb3JlIHJ1bm5pbmcgaXQuJywgJ3Bvd2VyX3VzZXJfdGlwJzogJ1VzZSBzdHJpY3RfZXhlY3V0aW9uIGZvciBhdXRvbWF0aW9uIGFuZCBjbGFyaWZ5aW5nX21vZGUgd2hlbiBkaXNjb3ZlcnkgaXMgc2FmZXIuJywgJ2ludGVyYWN0aW9uX3N1Z2dlc3Rpb25zJzogWydDb21wYXJlIHRoZSB0aHJlZSByZXdyaXRlcycsICdGaWxsIG1pc3NpbmcgY29uc3RyYWludHMnLCAnUnVuIHRoZSBzdHJpY3QgcmV3cml0ZSB0aHJvdWdoIHByb21wdCB0ZXN0cyddfQpyZXN1bHRbJ2Z1bl9tb2RlJ10gPSB7J2NoYWxsZW5nZV9sYWJlbCc6ICdQcm9tcHQgU2hhcnBlbmVkJywgJ3Njb3JlX2JhZGdlJzogJ1NwZWNpZmljaXR5ICcgKyBzdHIocm91bmQoc3BlY2lmaWNpdHksIDIpKSwgJ21pY3JvY29weSc6ICdBIHZhZ3VlIHByb21wdCBiZWNhbWUgYSB0ZXN0YWJsZSBpbnN0cnVjdGlvbi4nLCAnb3B0aW9uYWxfbmV4dF9jaGFsbGVuZ2UnOiAnQWRkIG9uZSBtZWFzdXJhYmxlIGFjY2VwdGFuY2UgY3JpdGVyaW9uIGJlZm9yZSBzZW5kaW5nIGl0IHRvIGEgbW9kZWwuJ30="
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
