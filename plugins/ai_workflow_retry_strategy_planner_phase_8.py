from __future__ import annotations

"""
Auto-generated Francis plugin module.

THIS FILE IS GENERATED. Manual edits may be overwritten by the factory.

Plugin: AI Workflow Retry Strategy Planner Phase 8
Slug: ai_workflow_retry_strategy_planner_phase_8
"""

from typing import Any, Dict, Optional

__all__ = ["invoke", "_run_core_logic", "SkillContext"]

# ---------------------------------------------------------------------------
# Plugin metadata (used by Station C, registry, and tooling)
# ---------------------------------------------------------------------------

_PLUGIN_NAME: str = 'AI Workflow Retry Strategy Planner Phase 8'
_PLUGIN_SLUG: str = 'ai_workflow_retry_strategy_planner_phase_8'
_PLUGIN_CATEGORY: str = 'ai_agents'
_PLUGIN_VERSION: str = '0.1.0'
_PLUGIN_GOAL: str = 'Extend AI Workflow Retry Strategy Planner with phase 8 behavior: preserve the original AI capability, add stronger edge-case handling, expose clearer user-facing progress signals, and produce more actionable next steps.'
_PLUGIN_TAGS = ['ai', 'retry', 'workflow', 'debugging', 'autonomous_factory', 'ai_progress', 'phase_8']
_PLUGIN_OWNER_ID = 'francis-factory'
_PLUGIN_CAPABILITY_TYPE = 'system_automation'
_PLUGIN_INTENDED_DOMAIN = 'AI workflow retry planning and failure recovery'
_PLUGIN_USE_CASES = ['Convert failure traces into retry strategies.', 'Change one variable at a time for safer debugging.', 'Recommend when to stop retrying and ask for input.', 'Show a compact progress state for this AI capability during advanced refinement pass 8.', 'Return user-facing guidance that is useful, concise, and safe to act on.', 'Avoid duplicating existing AI capability behavior; identify what is unique about this capability.']
_PLUGIN_RESULT_SCHEMA_VERSION: str = '1.0.0'

# Lightweight manifest for discovery/registry.
_PLUGIN_MANIFEST = {'name': 'AI Workflow Retry Strategy Planner Phase 8', 'slug': 'ai_workflow_retry_strategy_planner_phase_8', 'goal': 'Extend AI Workflow Retry Strategy Planner with phase 8 behavior: preserve the original AI capability, add stronger edge-case handling, expose clearer user-facing progress signals, and produce more actionable next steps.', 'category': 'ai_agents', 'tags': ['ai', 'retry', 'workflow', 'debugging', 'autonomous_factory', 'ai_progress', 'phase_8'], 'version': '0.1.0', 'capability_type': 'system_automation', 'intended_domain': 'AI workflow retry planning and failure recovery', 'owner_id': 'francis-factory', 'use_cases': ['Convert failure traces into retry strategies.', 'Change one variable at a time for safer debugging.', 'Recommend when to stop retrying and ask for input.', 'Show a compact progress state for this AI capability during advanced refinement pass 8.', 'Return user-facing guidance that is useful, concise, and safe to act on.', 'Avoid duplicating existing AI capability behavior; identify what is unique about this capability.'], 'primary_use_case': 'Convert failure traces into retry strategies.', 'problem_statement': 'Francis needs a focused AI capability for AI workflow retry planning and failure recovery. The generated module must turn messy user notes, model outputs, traces, or workflow state into structured, actionable AI assistance. It should improve autonomous progress by making the next step obvious, reducing duplicated work, and exposing risks before they become failures. The capability must stay deterministic, avoid hidden external side effects, and make its reasoning inspectable through concise details and scores.', 'primary_inputs': 'A payload dict that may contain task, objective, prompt, conversation, artifacts, candidate_outputs, traces, rubric, constraints, user_level, current_plan, completed_steps, blocked_steps, source_notes, and optional customer_config.', 'primary_outputs': 'A normalized result dict with summary, primary_insights, recommended_actions, scores, details, progress_state, user_experience, fun_mode, and machine-readable diagnostics.', 'constraints': 'Do not execute tools, browse, mutate files, call external APIs, or claim facts not present in the payload. Prefer deterministic analysis. If data is missing, say what is missing and return a useful fallback. Keep recommendations concrete. Avoid creating a capability that duplicates another AI roadmap capability.', 'example_use_cases': ['A user asks Francis to improve an AI workflow related to AI workflow retry planning and failure recovery.', 'A long-running autonomous run needs a checkpoint summary and the next best action.', 'An operator wants a scorecard that separates hard failures from polish improvements.', 'A beginner wants the result explained in plain language without losing technical accuracy.', 'A power user wants structured JSON they can pipe into another agent or dashboard.'], 'io_contract': "Input: payload is a dict. Important optional keys include 'task', 'objective', 'prompt', 'conversation', 'messages', 'candidate_outputs', 'trace', 'rubric', 'constraints', 'progress', 'current_plan', 'completed_steps', 'blocked_steps', 'user_level', and 'customer_config'. Output: return a dict containing summary: str, primary_insights: list, recommended_actions: list, scores: dict with confidence and usefulness, details: dict, progress_state: dict with current_stage/next_step/blockers, user_experience: dict with plain_language_takeaway and interaction_suggestions, and fun_mode: dict with optional challenge_label, score_badge, and celebratory_microcopy. Fun fields must never replace the serious recommendation.", 'schema_version': '1.0.0', 'family_key': 'ai_agents::ai workflow retry strategy planner phase', 'is_generic_name': False}

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
        plugin_name = 'AI Workflow Retry Strategy Planner Phase 8'
        goal = 'Extend AI Workflow Retry Strategy Planner with phase 8 behavior: preserve the original AI capability, add stronger edge-case handling, expose clearer user-facing progress signals, and produce more actionable next steps.'
        domain = 'AI workflow retry planning and failure recovery'
        capability_type = 'system_automation'
        logic_profile_id = 'workflow_retry_strategy_planner_profile'
        generation_note = 'capability profile registry override'
        use_cases = ['Convert failure traces into retry strategies.', 'Change one variable at a time for safer debugging.', 'Recommend when to stop retrying and ask for input.', 'Show a compact progress state for this AI capability during advanced refinement pass 8.', 'Return user-facing guidance that is useful, concise, and safe to act on.', 'Avoid duplicating existing AI capability behavior; identify what is unique about this capability.']
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
        trace_items = payload_data.get('trace') if isinstance(payload_data.get('trace'), list) else []
        failures = []
        blocked = payload_data.get('blocked_steps') if isinstance(payload_data.get('blocked_steps'), list) else []
        plan = payload_data.get('current_plan') if isinstance(payload_data.get('current_plan'), list) else []
        scan_items = trace_items + candidate_outputs + messages + blocked + plan + constraints
        for idx, item in enumerate(scan_items):
            text = str(item.get('error') or item.get('message') or item.get('summary') or item.get('content') or item if isinstance(item, dict) else item)
            lower = text.lower()
            hits = [term for term in ['timeout', 'failed', 'error', 'invalid', 'empty', 'shallow', 'duplicate', 'mismatch', 'blocked', 'citation', 'migration', 'rollback', 'unsupported', 'clinical'] if term in lower]
            if hits:
                failures.append({'index': idx, 'signals': hits, 'evidence': text[:220]})
        failure_clusters = {}
        for failure in failures:
            for signal in failure['signals']:
                failure_clusters[signal] = failure_clusters.get(signal, 0) + 1
        retry_decision = 'repair_then_retry' if failures else 'continue_with_checkpoint'
        if failure_clusters.get('duplicate', 0) or failure_clusters.get('shallow', 0):
            retry_decision = 'change_spec_or_profile_before_retry'
        if failure_clusters.get('timeout', 0) >= 2:
            retry_decision = 'pause_and_reduce_model_load'
        top_cluster = sorted(failure_clusters, key=failure_clusters.get, reverse=True)[0] if failure_clusters else 'no_failure'
        first_failure_preview = failures[0]['evidence'] if failures else def_text[:180]
        retry_strategy = [
            {'step': 1, 'action': 'Change one variable for ' + top_cluster, 'target': sorted(failure_clusters, key=failure_clusters.get, reverse=True)[:3], 'evidence': first_failure_preview},
            {'step': 2, 'action': 'Re-run checks that address ' + top_cluster, 'target': ['structural_validation', 'semantic_depth', top_cluster]},
            {'step': 3, 'action': 'Stop if ' + top_cluster + ' repeats', 'target': list(failure_clusters.keys())[:5]},
        ]
        stop_conditions = ['same failure repeats twice', 'repair candidate fails validation', 'risk controls are missing for production-affecting work']
        result['summary'] = plugin_name + ': selected retry decision ' + retry_decision + ' for top signal ' + top_cluster + ' from ' + str(len(failures)) + ' failure signal(s).'
        result['primary_insights'] = [
            {'title': 'Failure clusters', 'detail': failure_clusters},
            {'title': 'Retry decision', 'detail': retry_decision},
            {'title': 'Retry strategy', 'detail': retry_strategy},
        ]
        result['recommended_actions'] = [{'action': item['action'], 'target': item['target']} for item in retry_strategy]
        result['scores'] = {'confidence': round(min(0.92, 0.46 + 0.06 * len(failures) + 0.05 * len(failure_clusters)), 2), 'retry_readiness': round(max(0.1, 0.86 - 0.08 * len(failure_clusters)), 2), 'risk': round(min(0.9, 0.18 + 0.1 * len(failure_clusters)), 2), 'failure_signal_count': len(failures)}
        result['details'] = {'retry_strategy': retry_strategy, 'failure_clusters': failure_clusters, 'retry_decision': retry_decision, 'stop_conditions': stop_conditions, 'failure_signals': failures, 'top_cluster': top_cluster, 'missing_inputs': ['trace'] if not trace_items else []}
        result['details']['use_cases'] = use_cases
        result['details']['generation_note'] = generation_note
        result['details']['capability_type'] = capability_type
        result['details']['logic_profile_id'] = logic_profile_id
        result['details']['payload_warnings'] = payload_warnings
        result['progress_state'] = {
            'current_stage': logic_profile_id,
            'next_step': retry_strategy[0]['action'],
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
            'optional_next_challenge': retry_strategy[0]['action'],
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
