from __future__ import annotations

"""
Auto-generated Francis AI capability module.

THIS FILE IS GENERATED. Manual edits may be overwritten by the factory.

Capability: AI Eval Rubric Generator 000016
Slug: ai_eval_rubric_generator
"""

from typing import Any, Dict, Optional

__all__ = ["invoke", "_run_core_logic", "SkillContext"]

_PLUGIN_NAME: str = 'AI Eval Rubric Generator 000016'
_PLUGIN_SLUG: str = 'ai_eval_rubric_generator'
_PLUGIN_CATEGORY: str = 'ai_evaluation'
_PLUGIN_VERSION: str = '0.1.0'
_PLUGIN_GOAL: str = 'Create practical evaluation rubrics for AI tasks, prompts, and generated artifacts.'
_PLUGIN_TAGS = ['ai', 'evaluation', 'rubric', 'criteria', 'autonomous_factory', 'ai_progress']
_PLUGIN_OWNER_ID = 'francis-factory'
_PLUGIN_CAPABILITY_TYPE = 'research_synthesizer'
_PLUGIN_INTENDED_DOMAIN = 'AI evaluation design and acceptance criteria'
_PLUGIN_USE_CASES = ['Generate scoring criteria for a specific AI task.', 'Separate hard failures from quality preferences.', 'Produce a checklist usable by humans or automated evaluators.', 'Show a compact progress state for this AI capability during baseline capability.', 'Return user-facing guidance that is useful, concise, and safe to act on.', 'Avoid duplicating existing AI capability behavior; identify what is unique about this capability.']
_PLUGIN_RESULT_SCHEMA_VERSION: str = "1.0.0"
_PLUGIN_MANIFEST = {'name': 'AI Eval Rubric Generator 000016', 'slug': 'ai_eval_rubric_generator', 'goal': 'Create practical evaluation rubrics for AI tasks, prompts, and generated artifacts.', 'category': 'ai_evaluation', 'tags': ['ai', 'evaluation', 'rubric', 'criteria', 'autonomous_factory', 'ai_progress'], 'version': '0.1.0', 'capability_type': 'research_synthesizer', 'intended_domain': 'AI evaluation design and acceptance criteria', 'owner_id': 'francis-factory', 'use_cases': ['Generate scoring criteria for a specific AI task.', 'Separate hard failures from quality preferences.', 'Produce a checklist usable by humans or automated evaluators.', 'Show a compact progress state for this AI capability during baseline capability.', 'Return user-facing guidance that is useful, concise, and safe to act on.', 'Avoid duplicating existing AI capability behavior; identify what is unique about this capability.'], 'schema_version': '1.0.0'}
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
        plugin_name = 'AI Eval Rubric Generator 000016'
        goal = 'Create practical evaluation rubrics for AI tasks, prompts, and generated artifacts.'
        domain = 'AI evaluation design and acceptance criteria'
        capability_type = 'research_synthesizer'
        logic_profile_id = 'eval_rubric_generator_profile'
        generation_note = 'capability profile registry override'
        use_cases = ['Generate scoring criteria for a specific AI task.', 'Separate hard failures from quality preferences.', 'Produce a checklist usable by humans or automated evaluators.', 'Show a compact progress state for this AI capability during baseline capability.', 'Return user-facing guidance that is useful, concise, and safe to act on.', 'Avoid duplicating existing AI capability behavior; identify what is unique about this capability.']
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
        rubric_surface = ' '.join([def_text, objective_text, str(payload_data.get('prompt') or ''), ' '.join(str(item) for item in constraints)]).lower()
        risk_tags = []
        for label, terms in [
            ('release_or_auth_eval', ['auth', 'login', 'database', 'migration', 'rollback', 'production']),
            ('factual_grounding_eval', ['medical', 'clinical', 'citation', 'claim', 'source', 'unsupported', 'hallucination']),
            ('tooling_eval', ['tool', 'retrieval', 'browse', 'trace', 'consistency']),
            ('planning_eval', ['agent', 'handoff', 'blocked', 'owner', 'plan']),
        ]:
            hits = [term for term in terms if term in rubric_surface]
            if hits:
                risk_tags.append({'category': label, 'signals': hits})
        criteria = [
            {'name': 'instruction_adherence', 'weight': 0.3, 'pass_check': 'Satisfies the explicit task and constraints.'},
            {'name': 'completeness', 'weight': 0.25, 'pass_check': 'Covers required outputs and edge cases.'},
            {'name': 'evidence', 'weight': 0.2, 'pass_check': 'States assumptions, citations, or verification evidence where needed.'},
            {'name': 'actionability', 'weight': 0.15, 'pass_check': 'Produces concrete next steps.'},
            {'name': 'safety', 'weight': 0.1, 'pass_check': 'Avoids unsafe side effects and unsupported claims.'},
        ]
        if any(tag['category'] == 'factual_grounding_eval' for tag in risk_tags):
            criteria.append({'name': 'source_grounding', 'weight': 0.18, 'pass_check': 'Cites sources or clearly flags unsupported claims for ' + ', '.join(risk_tags[0]['signals'][:4]) + '.'})
        if any(tag['category'] == 'release_or_auth_eval' for tag in risk_tags):
            criteria.append({'name': 'release_safety', 'weight': 0.18, 'pass_check': 'Includes rollback, regression tests, and owner checks for auth/database changes.'})
        if any(tag['category'] == 'tooling_eval' for tag in risk_tags):
            criteria.append({'name': 'tool_trace_validity', 'weight': 0.14, 'pass_check': 'Explains tool choice, trace evidence, and consistency checks.'})
        total_weight = sum(item['weight'] for item in criteria) or 1
        for item in criteria:
            item['weight'] = round(item['weight'] / total_weight, 3)
        hard_failures = ['ignores a hard constraint', 'invents facts not in evidence', 'omits required output format']
        if any(tag['category'] == 'factual_grounding_eval' for tag in risk_tags):
            hard_failures.append('presents high-risk factual claims without citation or uncertainty')
        if any(tag['category'] == 'release_or_auth_eval' for tag in risk_tags):
            hard_failures.append('changes release-sensitive behavior without rollback or regression checks')
        result['summary'] = plugin_name + ': generated a weighted evaluation rubric for ' + def_text[:140] + '.'
        result['primary_insights'] = [
            {'title': 'Rubric criteria', 'detail': criteria},
            {'title': 'Hard failures', 'detail': hard_failures},
            {'title': 'Rubric risk tags', 'detail': risk_tags or 'No specialized rubric risk tags.'},
        ]
        result['recommended_actions'] = [
            {'action': 'Score output with rubric', 'criteria': criteria},
            {'action': 'Reject on hard failure', 'hard_failures': hard_failures},
            {'action': 'Apply specialized risk checks', 'risk_tags': risk_tags},
        ]
        risk_signal_count = sum(len(tag['signals']) for tag in risk_tags)
        result['scores'] = {'confidence': round(min(0.92, 0.48 + min(0.22, len(def_text.split()) / 120) + min(0.14, 0.025 * len(criteria))), 2), 'rubric_coverage': round(min(0.96, 0.58 + 0.04 * len(criteria) + 0.025 * len(risk_tags)), 2), 'risk': round(min(0.85, 0.14 + 0.028 * risk_signal_count + 0.035 * len(hard_failures[3:])), 2), 'risk_signal_count': risk_signal_count}
        result['details'] = {'rubric': criteria, 'hard_failures': hard_failures, 'risk_tags': risk_tags, 'scoring_scale': '0 to 1 weighted average', 'missing_inputs': [] if def_text else ['task']}
        result['details']['use_cases'] = use_cases
        result['details']['generation_note'] = generation_note
        result['details']['capability_type'] = capability_type
        result['details']['logic_profile_id'] = logic_profile_id
        result['details']['payload_warnings'] = payload_warnings
        result['progress_state'] = {
            'current_stage': logic_profile_id,
            'next_step': 'Score output with rubric',
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
            'optional_next_challenge': 'Score output with rubric',
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
