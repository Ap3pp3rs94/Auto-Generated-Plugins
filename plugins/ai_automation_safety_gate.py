from __future__ import annotations

"""
Auto-generated Francis plugin module.

THIS FILE IS GENERATED. Manual edits may be overwritten by the factory.

Plugin: AI Automation Safety Gate
Slug: ai_automation_safety_gate
"""

from typing import Any, Dict, Optional

__all__ = ["invoke", "_run_core_logic", "SkillContext"]

_PLUGIN_NAME: str = 'AI Automation Safety Gate'
_PLUGIN_SLUG: str = 'ai_automation_safety_gate'
_PLUGIN_CATEGORY: str = 'ai_safety'
_PLUGIN_VERSION: str = '0.1.0'
_PLUGIN_GOAL: str = 'Review proposed AI automation steps for side effects, missing approvals, and rollback needs.'
_PLUGIN_TAGS = ['ai', 'automation', 'safety', 'risk', 'autonomous_factory', 'ai_progress']
_PLUGIN_OWNER_ID = None
_PLUGIN_CAPABILITY_TYPE = 'scoring'
_PLUGIN_INTENDED_DOMAIN = 'AI automation safety and operational risk'
_PLUGIN_USE_CASES = ['Score automation plans before execution.', 'Flag destructive or irreversible steps.', 'Recommend approval, logging, and rollback controls.', 'Show a compact progress state for this AI capability during baseline capability.', 'Return user-facing guidance that is useful, concise, and safe to act on.', 'Avoid duplicating existing AI plugin behavior; identify what is unique about this capability.']
_PLUGIN_RESULT_SCHEMA_VERSION: str = "1.0.0"
_PLUGIN_MANIFEST = {'name': 'AI Automation Safety Gate', 'slug': 'ai_automation_safety_gate', 'goal': 'Review proposed AI automation steps for side effects, missing approvals, and rollback needs.', 'category': 'ai_safety', 'tags': ['ai', 'automation', 'safety', 'risk', 'autonomous_factory', 'ai_progress'], 'version': '0.1.0', 'capability_type': 'scoring', 'intended_domain': 'AI automation safety and operational risk', 'owner_id': None, 'use_cases': ['Score automation plans before execution.', 'Flag destructive or irreversible steps.', 'Recommend approval, logging, and rollback controls.', 'Show a compact progress state for this AI capability during baseline capability.', 'Return user-facing guidance that is useful, concise, and safe to act on.', 'Avoid duplicating existing AI plugin behavior; identify what is unique about this capability.'], 'schema_version': '1.0.0'}
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
        plugin_name = 'AI Automation Safety Gate'
        goal = 'Review proposed AI automation steps for side effects, missing approvals, and rollback needs.'
        domain = 'AI automation safety and operational risk'
        capability_type = 'scoring'
        logic_profile_id = 'automation_safety_gate_profile'
        generation_note = 'automation safety semantic risk fix'
        use_cases = ['Score automation plans before execution.', 'Flag destructive or irreversible steps.', 'Recommend approval, logging, and rollback controls.', 'Show a compact progress state for this AI capability during baseline capability.', 'Return user-facing guidance that is useful, concise, and safe to act on.', 'Avoid duplicating existing AI plugin behavior; identify what is unique about this capability.']
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
        steps = payload_data.get('steps') if isinstance(payload_data.get('steps'), list) else payload_data.get('current_plan') if isinstance(payload_data.get('current_plan'), list) else []
        context_steps = []
        for key in ['task', 'objective', 'prompt', 'constraints', 'blocked_steps']:
            value = payload_data.get(key)
            if value not in (None, '', [], {}):
                if isinstance(value, list):
                    context_steps.extend(str(item) for item in value)
                else:
                    context_steps.append(str(value))
        steps = list(steps) + context_steps if steps or context_steps else [def_text]
        risky_terms = ['delete', 'overwrite', 'deploy', 'push', 'payment', 'email', 'external', 'permission', 'secret', 'auth', 'login', 'database', 'migration', 'rollback', 'production', 'medical', 'clinical', 'citation', 'claim', 'source', 'unsupported', 'tool', 'retrieval']
        risk_findings = []
        for idx, step in enumerate(steps):
            lower = str(step).lower()
            hits = [term for term in risky_terms if term in lower]
            if hits:
                category = 'release_safety' if any(term in hits for term in ['auth', 'login', 'database', 'migration', 'rollback', 'production', 'deploy']) else 'factual_safety' if any(term in hits for term in ['medical', 'clinical', 'citation', 'claim', 'source', 'unsupported']) else 'tool_safety' if any(term in hits for term in ['tool', 'retrieval', 'external']) else 'destructive_action'
                risk_findings.append({'step_index': idx, 'step': str(step)[:220], 'risk_terms': hits, 'category': category})
        controls = ['dry run first', 'capture logs', 'define rollback', 'require explicit approval for destructive steps']
        if any(item['category'] == 'factual_safety' for item in risk_findings):
            controls.append('require source verification before user-facing claims')
        if any(item['category'] == 'release_safety' for item in risk_findings):
            controls.append('require rollback owner and regression checks')
        approval_required = bool(risk_findings)
        result['summary'] = plugin_name + ': safety-reviewed ' + str(len(steps)) + ' automation step(s).'
        result['primary_insights'] = [
            {'title': 'Risk findings', 'detail': risk_findings},
            {'title': 'Approval required', 'detail': approval_required},
            {'title': 'Controls', 'detail': controls},
        ]
        result['recommended_actions'] = [
            {'action': 'Apply safety controls', 'controls': controls},
            {'action': 'Request approval before execution' if approval_required else 'Proceed with logged dry run'},
        ]
        risk_term_count = sum(len(item['risk_terms']) for item in risk_findings)
        category_count = len(set(item['category'] for item in risk_findings))
        result['scores'] = {'confidence': round(min(0.92, 0.44 + min(0.24, 0.045 * len(steps)) + min(0.16, 0.025 * risk_term_count)), 2), 'safety_risk': round(min(0.95, 0.12 + 0.09 * len(risk_findings) + 0.025 * risk_term_count + 0.04 * category_count), 2), 'approval_readiness': round(0.58 + min(0.32, 0.045 * len(controls)), 2) if approval_required else 0.64, 'risk': round(min(0.95, 0.12 + 0.09 * len(risk_findings) + 0.025 * risk_term_count + 0.04 * category_count), 2), 'risk_term_count': risk_term_count}
        result['details'] = {'risk_findings': risk_findings, 'controls': controls, 'approval_required': approval_required, 'missing_inputs': ['steps'] if not steps else []}
        result['details']['use_cases'] = use_cases
        result['details']['generation_note'] = generation_note
        result['details']['capability_type'] = capability_type
        result['details']['logic_profile_id'] = logic_profile_id
        result['details']['payload_warnings'] = payload_warnings
        result['progress_state'] = {
            'current_stage': logic_profile_id,
            'next_step': 'Apply safety controls',
            'blockers': result['details'].get('missing_inputs', [])[:4],
            'done_signals': ['capability_specific_analysis_complete', logic_profile_id],
        }
        result['user_experience'] = {
            'plain_language_takeaway': result['summary'],
            'beginner_tip': 'Use the first recommendation as the next concrete step.',
            'power_user_tip': 'Pass details and scores into the next AI capability plugin.',
            'interaction_suggestions': [item.get('action', str(item)) for item in result.get('recommended_actions', [])[:3]],
        }
        result['fun_mode'] = {
            'challenge_label': plugin_name,
            'score_badge': 'Strong Signal' if result.get('scores', {}).get('confidence', 0) >= 0.65 else 'Needs Context',
            'microcopy': result['summary'],
            'optional_next_challenge': 'Apply safety controls',
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
        payload = {"_value": payload}
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
