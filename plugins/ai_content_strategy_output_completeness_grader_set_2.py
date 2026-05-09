from __future__ import annotations

"""
Auto-generated Francis plugin module.

THIS FILE IS GENERATED. Manual edits may be overwritten by the factory.

Plugin: AI Content Strategy Output Completeness Grader Set 2
Slug: ai_content_strategy_output_completeness_grader_set_2
"""

from typing import Any, Dict, Optional

__all__ = ["invoke", "_run_core_logic", "SkillContext"]

# ---------------------------------------------------------------------------
# Plugin metadata (used by Station C, registry, and tooling)
# ---------------------------------------------------------------------------

_PLUGIN_NAME: str = 'AI Content Strategy Output Completeness Grader Set 2'
_PLUGIN_SLUG: str = 'ai_content_strategy_output_completeness_grader_set_2'
_PLUGIN_CATEGORY: str = 'ai_evaluation'
_PLUGIN_VERSION: str = '0.1.0'
_PLUGIN_GOAL: str = 'Grade AI content strategy and editorial workflows AI outputs for completeness against task requirements and acceptance criteria.'
_PLUGIN_TAGS = ['content', 'strategy', 'evaluation', 'completeness', 'quality', 'continuous_backlog', 'autonomous_factory', 'ai_progress']
_PLUGIN_OWNER_ID = 'francis-factory'
_PLUGIN_CAPABILITY_TYPE = 'scoring'
_PLUGIN_INTENDED_DOMAIN = 'AI content strategy and editorial workflows output completeness and acceptance scoring'
_PLUGIN_USE_CASES = ['Identify missing sections or unmet requirements.', 'Score completeness using task-specific signals.', 'Recommend edits that close blocking gaps.', 'Show a compact progress state for this AI capability during baseline capability.', 'Return user-facing guidance that is useful, concise, and safe to act on.', 'Avoid duplicating existing AI capability behavior; identify what is unique about this capability.']
_PLUGIN_RESULT_SCHEMA_VERSION: str = '1.0.0'

# Lightweight manifest for discovery/registry.
_PLUGIN_MANIFEST = {'name': 'AI Content Strategy Output Completeness Grader Set 2', 'slug': 'ai_content_strategy_output_completeness_grader_set_2', 'goal': 'Grade AI content strategy and editorial workflows AI outputs for completeness against task requirements and acceptance criteria.', 'category': 'ai_evaluation', 'tags': ['content', 'strategy', 'evaluation', 'completeness', 'quality', 'continuous_backlog', 'autonomous_factory', 'ai_progress'], 'version': '0.1.0', 'capability_type': 'scoring', 'intended_domain': 'AI content strategy and editorial workflows output completeness and acceptance scoring', 'owner_id': 'francis-factory', 'use_cases': ['Identify missing sections or unmet requirements.', 'Score completeness using task-specific signals.', 'Recommend edits that close blocking gaps.', 'Show a compact progress state for this AI capability during baseline capability.', 'Return user-facing guidance that is useful, concise, and safe to act on.', 'Avoid duplicating existing AI capability behavior; identify what is unique about this capability.'], 'primary_use_case': 'Identify missing sections or unmet requirements.', 'problem_statement': 'Francis needs a focused AI capability for AI content strategy and editorial workflows output completeness and acceptance scoring. The generated module must turn messy user notes, model outputs, traces, or workflow state into structured, actionable AI assistance. It should improve autonomous progress by making the next step obvious, reducing duplicated work, and exposing risks before they become failures. The capability must stay deterministic, avoid hidden external side effects, and make its reasoning inspectable through concise details and scores.', 'primary_inputs': 'A payload dict that may contain task, objective, prompt, conversation, artifacts, candidate_outputs, traces, rubric, constraints, user_level, current_plan, completed_steps, blocked_steps, source_notes, and optional customer_config.', 'primary_outputs': 'A normalized result dict with summary, primary_insights, recommended_actions, scores, details, progress_state, user_experience, fun_mode, and machine-readable diagnostics.', 'constraints': 'Do not execute tools, browse, mutate files, call external APIs, or claim facts not present in the payload. Prefer deterministic analysis. If data is missing, say what is missing and return a useful fallback. Keep recommendations concrete. Avoid creating a capability that duplicates another AI roadmap capability.', 'example_use_cases': ['A user asks Francis to improve an AI workflow related to AI content strategy and editorial workflows output completeness and acceptance scoring.', 'A long-running autonomous run needs a checkpoint summary and the next best action.', 'An operator wants a scorecard that separates hard failures from polish improvements.', 'A beginner wants the result explained in plain language without losing technical accuracy.', 'A power user wants structured JSON they can pipe into another agent or dashboard.'], 'io_contract': "Input: payload is a dict. Important optional keys include 'task', 'objective', 'prompt', 'conversation', 'messages', 'candidate_outputs', 'trace', 'rubric', 'constraints', 'progress', 'current_plan', 'completed_steps', 'blocked_steps', 'user_level', and 'customer_config'. Output: return a dict containing summary: str, primary_insights: list, recommended_actions: list, scores: dict with confidence and usefulness, details: dict, progress_state: dict with current_stage/next_step/blockers, user_experience: dict with plain_language_takeaway and interaction_suggestions, and fun_mode: dict with optional challenge_label, score_badge, and celebratory_microcopy. Fun fields must never replace the serious recommendation.", 'schema_version': '1.0.0', 'family_key': 'ai_evaluation::ai content strategy output completeness grader set', 'is_generic_name': False}

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
        plugin_name = 'AI Content Strategy Output Completeness Grader Set 2'
        goal = 'Grade AI content strategy and editorial workflows AI outputs for completeness against task requirements and acceptance criteria.'
        domain = 'AI content strategy and editorial workflows output completeness and acceptance scoring'
        capability_type = 'scoring'
        logic_profile_id = 'continuous_output_completeness_grader_profile'
        generation_note = 'capability profile registry override'
        use_cases = ['Identify missing sections or unmet requirements.', 'Score completeness using task-specific signals.', 'Recommend edits that close blocking gaps.', 'Show a compact progress state for this AI capability during baseline capability.', 'Return user-facing guidance that is useful, concise, and safe to act on.', 'Avoid duplicating existing AI capability behavior; identify what is unique about this capability.']
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
        raw_response = payload_data.get('response') or payload_data.get('answer')
        if raw_response is None and candidate_outputs:
            raw_response = ' '.join(str(item.get('summary') or item.get('text') or item) if isinstance(item, dict) else str(item) for item in candidate_outputs[:4])
        response_text = str(raw_response or '').strip()
        rubric = payload_data.get('rubric') if isinstance(payload_data.get('rubric'), list) else []
        requirements = rubric or constraints or [objective_text, def_text]
        missing_requirements = []
        covered_requirements = []
        lower_response = response_text.lower()
        for requirement in requirements:
            req = str(requirement).strip()
            keywords = [word.strip('.,:;!?').lower() for word in req.split() if len(word.strip('.,:;!?')) > 4][:5]
            hits = [word for word in keywords if word in lower_response]
            if hits:
                covered_requirements.append({'requirement': req, 'matched_terms': hits})
            else:
                missing_requirements.append(req)
        domain_risk_flags = []
        for label, terms in [
            ('release_or_auth', ['auth', 'login', 'database', 'migration', 'rollback', 'production']),
            ('factual_or_medical', ['medical', 'clinical', 'citation', 'claim', 'source', 'unsupported', 'dosage']),
            ('tooling_or_trace', ['tool', 'retrieval', 'trace', 'consistency', 'browse']),
        ]:
            hits = sorted(set(term for term in terms if term in (lower_response + ' ' + def_text.lower() + ' ' + objective_text.lower())))
            if hits:
                domain_risk_flags.append({'category': label, 'signals': hits})
        clarity_flags = []
        if len(response_text.split()) < 20:
            clarity_flags.append('response is very short')
        if any(marker in lower_response for marker in ['maybe', 'probably', 'i think', 'not sure']):
            clarity_flags.append('uncertainty is not resolved')
        if 'test' not in lower_response and 'verify' not in lower_response and 'check' not in lower_response:
            clarity_flags.append('verification step is missing')
        if any(flag['category'] == 'factual_or_medical' for flag in domain_risk_flags) and not any(word in lower_response for word in ['citation', 'source', 'grounded', 'unsupported']):
            clarity_flags.append('factual grounding evidence is missing')
        if any(flag['category'] == 'release_or_auth' for flag in domain_risk_flags) and not any(word in lower_response for word in ['rollback', 'test', 'migration', 'session']):
            clarity_flags.append('release safety evidence is missing')
        coverage = len(covered_requirements) / max(1, len(requirements))
        risk_signal_count = sum(len(flag['signals']) for flag in domain_risk_flags)
        quality_score = round(min(0.95, 0.28 + 0.42 * coverage + (0.12 if not clarity_flags else 0) + min(0.1, len(response_text.split()) / 250)), 2)
        improvement_checklist = []
        for req in missing_requirements[:5]:
            improvement_checklist.append('Address requirement: ' + req[:140])
        for flag in clarity_flags:
            improvement_checklist.append('Fix quality issue: ' + flag)
        for flag in domain_risk_flags[:3]:
            improvement_checklist.append('Add evidence for ' + flag['category'] + ': ' + ', '.join(flag['signals'][:5]))
        if not improvement_checklist:
            improvement_checklist.append('Preserve covered requirements and add evidence for the strongest claim.')
        result['summary'] = plugin_name + ': scored output quality at ' + str(quality_score) + ' for ' + def_text[:130] + '.'
        result['primary_insights'] = [
            {'title': 'Covered requirements', 'detail': covered_requirements[:6]},
            {'title': 'Missing requirements', 'detail': missing_requirements[:6]},
            {'title': 'Clarity flags', 'detail': clarity_flags or 'No major clarity flags.'},
            {'title': 'Domain risk flags', 'detail': domain_risk_flags or 'No high-risk domain flags.'},
        ]
        result['recommended_actions'] = [{'action': item} for item in improvement_checklist[:6]]
        result['scores'] = {'confidence': round(min(0.92, 0.38 + min(0.28, 0.055 * len(requirements)) + min(0.18, len(response_text.split()) / 180) + 0.035 * len(covered_requirements)), 2), 'quality': quality_score, 'coverage': round(coverage, 2), 'risk': round(min(0.92, 0.16 + 0.08 * len(missing_requirements[:4]) + 0.05 * len(clarity_flags) + 0.025 * risk_signal_count), 2), 'domain_risk_signal_count': risk_signal_count}
        result['details'] = {'evaluated_response': response_text[:1200], 'covered_requirements': covered_requirements, 'missing_requirements': missing_requirements, 'clarity_flags': clarity_flags, 'domain_risk_flags': domain_risk_flags, 'improvement_checklist': improvement_checklist, 'missing_inputs': ['response or candidate_outputs'] if not response_text else []}
        result['details']['use_cases'] = use_cases
        result['details']['generation_note'] = generation_note
        result['details']['capability_type'] = capability_type
        result['details']['logic_profile_id'] = logic_profile_id
        result['details']['payload_warnings'] = payload_warnings
        result['progress_state'] = {
            'current_stage': logic_profile_id,
            'next_step': improvement_checklist[0] if improvement_checklist else 'Keep the output as-is.',
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
            'optional_next_challenge': improvement_checklist[0] if improvement_checklist else 'Keep the output as-is.',
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
