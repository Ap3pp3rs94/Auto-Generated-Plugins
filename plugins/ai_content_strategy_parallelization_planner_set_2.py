from __future__ import annotations

"""
Auto-generated Francis plugin module.

THIS FILE IS GENERATED. Manual edits may be overwritten by the factory.

Plugin: AI Content Strategy Parallelization Planner Set 2
Slug: ai_content_strategy_parallelization_planner_set_2
"""

from typing import Any, Dict, Optional

__all__ = ["invoke", "_run_core_logic", "SkillContext"]

# ---------------------------------------------------------------------------
# Plugin metadata (used by Station C, registry, and tooling)
# ---------------------------------------------------------------------------

_PLUGIN_NAME: str = 'AI Content Strategy Parallelization Planner Set 2'
_PLUGIN_SLUG: str = 'ai_content_strategy_parallelization_planner_set_2'
_PLUGIN_CATEGORY: str = 'ai_agents'
_PLUGIN_VERSION: str = '0.1.0'
_PLUGIN_GOAL: str = 'Identify safe parallel work packets for AI content strategy and editorial workflows without duplicating or blocking work.'
_PLUGIN_TAGS = ['content', 'strategy', 'agents', 'parallel', 'planning', 'continuous_backlog', 'autonomous_factory', 'ai_progress']
_PLUGIN_OWNER_ID = 'francis-factory'
_PLUGIN_CAPABILITY_TYPE = 'system_automation'
_PLUGIN_INTENDED_DOMAIN = 'AI content strategy and editorial workflows parallel AI workflow planning'
_PLUGIN_USE_CASES = ['Split work into blocking and parallelizable paths.', 'Detect dependency conflicts before delegation.', 'Create bounded sidecar tasks with merge checkpoints.', 'Show a compact progress state for this AI capability during baseline capability.', 'Return user-facing guidance that is useful, concise, and safe to act on.', 'Avoid duplicating existing AI capability behavior; identify what is unique about this capability.']
_PLUGIN_RESULT_SCHEMA_VERSION: str = '1.0.0'

# Lightweight manifest for discovery/registry.
_PLUGIN_MANIFEST = {'name': 'AI Content Strategy Parallelization Planner Set 2', 'slug': 'ai_content_strategy_parallelization_planner_set_2', 'goal': 'Identify safe parallel work packets for AI content strategy and editorial workflows without duplicating or blocking work.', 'category': 'ai_agents', 'tags': ['content', 'strategy', 'agents', 'parallel', 'planning', 'continuous_backlog', 'autonomous_factory', 'ai_progress'], 'version': '0.1.0', 'capability_type': 'system_automation', 'intended_domain': 'AI content strategy and editorial workflows parallel AI workflow planning', 'owner_id': 'francis-factory', 'use_cases': ['Split work into blocking and parallelizable paths.', 'Detect dependency conflicts before delegation.', 'Create bounded sidecar tasks with merge checkpoints.', 'Show a compact progress state for this AI capability during baseline capability.', 'Return user-facing guidance that is useful, concise, and safe to act on.', 'Avoid duplicating existing AI capability behavior; identify what is unique about this capability.'], 'primary_use_case': 'Split work into blocking and parallelizable paths.', 'problem_statement': 'Francis needs a focused AI capability for AI content strategy and editorial workflows parallel AI workflow planning. The generated module must turn messy user notes, model outputs, traces, or workflow state into structured, actionable AI assistance. It should improve autonomous progress by making the next step obvious, reducing duplicated work, and exposing risks before they become failures. The capability must stay deterministic, avoid hidden external side effects, and make its reasoning inspectable through concise details and scores.', 'primary_inputs': 'A payload dict that may contain task, objective, prompt, conversation, artifacts, candidate_outputs, traces, rubric, constraints, user_level, current_plan, completed_steps, blocked_steps, source_notes, and optional customer_config.', 'primary_outputs': 'A normalized result dict with summary, primary_insights, recommended_actions, scores, details, progress_state, user_experience, fun_mode, and machine-readable diagnostics.', 'constraints': 'Do not execute tools, browse, mutate files, call external APIs, or claim facts not present in the payload. Prefer deterministic analysis. If data is missing, say what is missing and return a useful fallback. Keep recommendations concrete. Avoid creating a capability that duplicates another AI roadmap capability.', 'example_use_cases': ['A user asks Francis to improve an AI workflow related to AI content strategy and editorial workflows parallel AI workflow planning.', 'A long-running autonomous run needs a checkpoint summary and the next best action.', 'An operator wants a scorecard that separates hard failures from polish improvements.', 'A beginner wants the result explained in plain language without losing technical accuracy.', 'A power user wants structured JSON they can pipe into another agent or dashboard.'], 'io_contract': "Input: payload is a dict. Important optional keys include 'task', 'objective', 'prompt', 'conversation', 'messages', 'candidate_outputs', 'trace', 'rubric', 'constraints', 'progress', 'current_plan', 'completed_steps', 'blocked_steps', 'user_level', and 'customer_config'. Output: return a dict containing summary: str, primary_insights: list, recommended_actions: list, scores: dict with confidence and usefulness, details: dict, progress_state: dict with current_stage/next_step/blockers, user_experience: dict with plain_language_takeaway and interaction_suggestions, and fun_mode: dict with optional challenge_label, score_badge, and celebratory_microcopy. Fun fields must never replace the serious recommendation.", 'schema_version': '1.0.0', 'family_key': 'ai_agents::ai content strategy parallelization planner set', 'is_generic_name': False}

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
        plugin_name = 'AI Content Strategy Parallelization Planner Set 2'
        goal = 'Identify safe parallel work packets for AI content strategy and editorial workflows without duplicating or blocking work.'
        domain = 'AI content strategy and editorial workflows parallel AI workflow planning'
        capability_type = 'system_automation'
        logic_profile_id = 'continuous_parallelization_planner_profile'
        generation_note = 'capability profile registry override'
        use_cases = ['Split work into blocking and parallelizable paths.', 'Detect dependency conflicts before delegation.', 'Create bounded sidecar tasks with merge checkpoints.', 'Show a compact progress state for this AI capability during baseline capability.', 'Return user-facing guidance that is useful, concise, and safe to act on.', 'Avoid duplicating existing AI capability behavior; identify what is unique about this capability.']
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
        current_plan = payload_data.get('current_plan') if isinstance(payload_data.get('current_plan'), list) else []
        completed_steps = payload_data.get('completed_steps') if isinstance(payload_data.get('completed_steps'), list) else []
        blocked_steps = payload_data.get('blocked_steps') if isinstance(payload_data.get('blocked_steps'), list) else []
        parallel_hints = []
        planning_text = ' '.join([
            def_text,
            objective_text,
            ' '.join(str(item) for item in constraints),
            ' '.join(str(item) for item in blocked_steps),
        ]).lower()
        if 'test' in planning_text or 'verify' in planning_text:
            parallel_hints.append('prepare verification while implementation is planned')
        if any(word in planning_text for word in ['file', 'code', 'api', 'middleware', 'database', 'migration']):
            parallel_hints.append('inspect affected files before editing')
        if any(word in planning_text for word in ['citation', 'source', 'retrieval', 'medical', 'clinical', 'hallucination']):
            parallel_hints.append('verify source grounding before final response')
        risk_signals = []
        for label, terms in [
            ('release_safety', ['production', 'outage', 'rollback', 'migration', 'database']),
            ('security_auth', ['auth', 'login', 'session', 'permission']),
            ('factual_safety', ['medical', 'clinical', 'citation', 'claim', 'hallucination']),
            ('coordination', ['multi-agent', 'handoff', 'owner', 'blocked']),
        ]:
            hits = [term for term in terms if term in planning_text]
            if hits:
                risk_signals.append({'category': label, 'signals': hits})
        complexity_terms = sorted(set(
            word.strip('.,:;!?').lower()
            for word in planning_text.split()
            if len(word.strip('.,:;!?')) > 7
        ))[:12]
        risk_action_templates = {
            'release_safety': ('safety_review', 'Create rollback, migration, and production-safety checks for', True),
            'security_auth': ('security_review', 'Verify authentication, session, and permission behavior for', True),
            'factual_safety': ('grounding_review', 'Collect citations and mark unsupported claims before drafting', True),
            'coordination': ('handoff_review', 'Assign owner, handoff packet, and blocker resolution path for', False),
        }
        capability_actions = []
        for signal in risk_signals:
            template = risk_action_templates.get(signal['category'])
            if template:
                capability_actions.append({
                    'stage': template[0],
                    'task': template[1] + ' ' + ', '.join(signal['signals']),
                    'blocking': template[2],
                    'source_signal': signal['category'],
                })
        for index, existing_step in enumerate(current_plan[:3], 1):
            capability_actions.append({
                'stage': 'align',
                'task': 'Reconcile existing plan step %d with the new objective: %s' % (index, str(existing_step)[:140]),
                'blocking': False,
                'source_signal': 'current_plan',
            })
        for blocker in blocked_steps[:3]:
            capability_actions.append({
                'stage': 'unblock',
                'task': 'Resolve or route blocker before dependent work continues: ' + str(blocker)[:160],
                'blocking': True,
                'source_signal': 'blocked_steps',
            })
        sequenced_plan = []
        if not explicit_objective_text:
            sequenced_plan.append({'step': 1, 'stage': 'clarify', 'task': 'Define the objective and acceptance criteria.', 'blocking': True})
        sequenced_plan.append({'step': len(sequenced_plan) + 1, 'stage': 'plan', 'task': 'Break work into implementation, review, and verification checkpoints for ' + def_text[:160], 'blocking': True})
        for action in capability_actions:
            action = dict(action)
            action['step'] = len(sequenced_plan) + 1
            sequenced_plan.append(action)
        sequenced_plan.append({'step': len(sequenced_plan) + 1, 'stage': 'execute', 'task': 'Complete the smallest reversible implementation unit.', 'blocking': False})
        sequenced_plan.append({'step': len(sequenced_plan) + 1, 'stage': 'verify', 'task': 'Run tests or explicit checks tied to ' + objective_text[:140], 'blocking': True})
        sequenced_plan.append({'step': len(sequenced_plan) + 1, 'stage': 'handoff', 'task': 'Package changed files, decisions, blockers, and verification evidence for the next agent.', 'blocking': True})
        handoff_packet = {
            'objective': objective_text,
            'completed_steps': completed_steps,
            'blocked_steps': blocked_steps,
            'parallelizable_work': parallel_hints or ['document assumptions', 'prepare verification checklist'],
            'risk_signals': risk_signals,
            'specialized_actions': capability_actions,
            'integration_checkpoint': 'Confirm completed work, blockers, changed files, and test evidence before the next agent starts.',
        }
        complexity_score = min(0.12, len(complexity_terms) * 0.01)
        risk_signal_score = min(0.14, sum(len(item['signals']) for item in risk_signals) * 0.025)
        coverage = 0.34 + (0.12 if explicit_objective_text else 0) + (0.09 if current_plan else 0) + (0.09 if completed_steps else 0) + (0.08 if blocked_steps else 0) + min(0.1, len(constraints) * 0.03) + complexity_score + min(0.08, len(capability_actions) * 0.015) + min(0.06, len(parallel_hints) * 0.02)
        result['summary'] = plugin_name + ': built a sequenced AI-agent plan with checkpoints for ' + def_text[:140] + '.'
        result['primary_insights'] = [
            {'title': 'Plan coverage', 'detail': 'Found %d existing plan step(s), %d completed step(s), and %d blocker(s).' % (len(current_plan), len(completed_steps), len(blocked_steps))},
            {'title': 'Blocking path', 'detail': blocked_steps[0] if blocked_steps else 'No explicit blocker was provided.'},
            {'title': 'Parallel work', 'detail': handoff_packet['parallelizable_work']},
            {'title': 'Risk signals', 'detail': risk_signals or 'No high-risk planning signal detected.'},
            {'title': 'Specialized actions', 'detail': capability_actions or 'No specialized action was required beyond the standard plan.'},
        ]
        result['recommended_actions'] = [
            {'action': item['task'], 'stage': item['stage'], 'blocking': item['blocking'], 'source_signal': item.get('source_signal', 'standard')} for item in sequenced_plan
        ]
        risk_score = round(min(0.92, max(0.12, 0.42 + risk_signal_score + 0.04 * len(blocked_steps) - min(0.18, len(completed_steps) * 0.04))), 2)
        result['scores'] = {'confidence': round(min(0.92, coverage), 2), 'plan_coverage': round(min(1.0, coverage + 0.08 + complexity_score), 2), 'handoff_readiness': round(0.48 + min(0.4, len(handoff_packet['parallelizable_work']) * 0.06 + len(sequenced_plan) * 0.018 + len(capability_actions) * 0.025), 2), 'risk': risk_score, 'complexity': round(complexity_score + risk_signal_score, 2)}
        result['details'] = {'sequenced_plan': sequenced_plan, 'handoff_packet': handoff_packet, 'risk_signals': risk_signals, 'complexity_terms': complexity_terms, 'specialized_action_count': len(capability_actions), 'missing_inputs': [key for key in ['objective', 'current_plan', 'blocked_steps'] if not payload_data.get(key)]}
        result['details']['use_cases'] = use_cases
        result['details']['generation_note'] = generation_note
        result['details']['capability_type'] = capability_type
        result['details']['logic_profile_id'] = logic_profile_id
        result['details']['payload_warnings'] = payload_warnings
        result['progress_state'] = {
            'current_stage': logic_profile_id,
            'next_step': sequenced_plan[0]['task'] if sequenced_plan else 'Define the next planning step.',
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
            'optional_next_challenge': sequenced_plan[0]['task'] if sequenced_plan else 'Define the next planning step.',
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
