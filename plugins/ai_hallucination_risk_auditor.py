from __future__ import annotations

"""
Auto-generated Francis plugin module.

THIS FILE IS GENERATED. Manual edits may be overwritten by the factory.

Plugin: AI Hallucination Risk Auditor
Slug: ai_hallucination_risk_auditor
"""

from typing import Any, Dict, Optional

__all__ = ["invoke", "_run_core_logic", "SkillContext"]

_PLUGIN_NAME: str = 'AI Hallucination Risk Auditor'
_PLUGIN_SLUG: str = 'ai_hallucination_risk_auditor'
_PLUGIN_CATEGORY: str = 'ai_evaluation'
_PLUGIN_VERSION: str = '0.1.0'
_PLUGIN_GOAL: str = 'Inspect AI-generated claims and flag unsupported, risky, or source-sensitive statements.'
_PLUGIN_TAGS = ['ai', 'hallucination', 'risk', 'verification', 'autonomous_factory', 'ai_progress']
_PLUGIN_OWNER_ID = None
_PLUGIN_CAPABILITY_TYPE = 'scoring'
_PLUGIN_INTENDED_DOMAIN = 'AI reliability, hallucination detection, and factual risk'
_PLUGIN_USE_CASES = ['Identify claims that need citations or external verification.', 'Classify risk by domain such as legal, medical, financial, or technical.', 'Suggest safer rewrites for uncertain claims.', 'Show a compact progress state for this AI capability during baseline capability.', 'Return user-facing guidance that is useful, concise, and safe to act on.', 'Avoid duplicating existing AI plugin behavior; identify what is unique about this capability.']
_PLUGIN_RESULT_SCHEMA_VERSION: str = "1.0.0"
_PLUGIN_MANIFEST = {'name': 'AI Hallucination Risk Auditor', 'slug': 'ai_hallucination_risk_auditor', 'goal': 'Inspect AI-generated claims and flag unsupported, risky, or source-sensitive statements.', 'category': 'ai_evaluation', 'tags': ['ai', 'hallucination', 'risk', 'verification', 'autonomous_factory', 'ai_progress'], 'version': '0.1.0', 'capability_type': 'scoring', 'intended_domain': 'AI reliability, hallucination detection, and factual risk', 'owner_id': None, 'use_cases': ['Identify claims that need citations or external verification.', 'Classify risk by domain such as legal, medical, financial, or technical.', 'Suggest safer rewrites for uncertain claims.', 'Show a compact progress state for this AI capability during baseline capability.', 'Return user-facing guidance that is useful, concise, and safe to act on.', 'Avoid duplicating existing AI plugin behavior; identify what is unique about this capability.'], 'schema_version': '1.0.0'}
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
        plugin_name = 'AI Hallucination Risk Auditor'
        goal = 'Inspect AI-generated claims and flag unsupported, risky, or source-sensitive statements.'
        domain = 'AI reliability, hallucination detection, and factual risk'
        capability_type = 'scoring'
        logic_profile_id = 'hallucination_risk_auditor_profile'
        generation_note = 'production_validation_repair: ensure non-empty actions for low-risk hallucination payloads'
        use_cases = ['Identify claims that need citations or external verification.', 'Classify risk by domain such as legal, medical, financial, or technical.', 'Suggest safer rewrites for uncertain claims.', 'Show a compact progress state for this AI capability during baseline capability.', 'Return user-facing guidance that is useful, concise, and safe to act on.', 'Avoid duplicating existing AI plugin behavior; identify what is unique about this capability.']
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
        raw_text = payload_data.get('response') or payload_data.get('answer')
        if raw_text is None and candidate_outputs:
            raw_text = ' '.join(str(item.get('summary') or item.get('text') or item) if isinstance(item, dict) else str(item) for item in candidate_outputs[:4])
        context_text = ' '.join([def_text, objective_text, ' '.join(str(item) for item in constraints), str(payload_data.get('trace') or '')]).strip()
        text = (str(raw_text or '') + '. ' + context_text).strip()
        sentences = [part.strip() for part in text.replace('\n', '. ').split('.') if part.strip()]
        risk_terms = ['always', 'never', 'guaranteed', 'latest', 'current', 'law', 'legal', 'medical', 'clinical', 'financial', 'price', 'study', 'research', 'statistic', 'percent', 'dosage', 'unsupported', 'citation', 'source', 'claim', 'auth', 'login', 'database', 'migration', 'rollback']
        claims = []
        for sentence in sentences:
            lower = sentence.lower()
            signals = [term for term in risk_terms if term in lower]
            has_citation = 'http' in lower or '[' in sentence or 'source' in lower or 'citation' in lower
            if signals or any(ch.isdigit() for ch in sentence):
                needs_verification = bool(signals) and not has_citation
                if any(term in signals for term in ['unsupported', 'claim', 'dosage', 'medical', 'clinical']):
                    needs_verification = True
                claims.append({'claim': sentence[:220], 'risk_signals': signals, 'has_citation': has_citation, 'needs_verification': needs_verification})
        high_risk = [claim for claim in claims if claim['needs_verification']]
        context_signals = sorted(set(term for term in risk_terms if term in context_text.lower()))
        safer_rewrites = []
        for claim in high_risk[:5]:
            safer_rewrites.append({'original': claim['claim'], 'rewrite': 'Verify before relying on this claim: ' + claim['claim']})
        risk_score = round(min(0.95, 0.14 + 0.11 * len(high_risk) + 0.035 * len(claims) + 0.02 * len(context_signals)), 2)
        result['summary'] = plugin_name + ': found ' + str(len(high_risk)) + ' claim(s) needing verification.'
        result['primary_insights'] = [
            {'title': 'Claims needing verification', 'detail': high_risk[:6]},
            {'title': 'Citation coverage', 'detail': str(len([c for c in claims if c['has_citation']])) + ' cited of ' + str(len(claims)) + ' flagged claims'},
            {'title': 'Risk domains', 'detail': sorted(set(term for claim in claims for term in claim['risk_signals']))},
            {'title': 'Context signals', 'detail': context_signals or 'No context risk signals.'},
        ]
        result['recommended_actions'] = [
            {'action': 'Verify claim', 'claim': claim['claim'], 'signals': claim['risk_signals']} for claim in high_risk[:5]
        ]
        if not result['recommended_actions'] and context_signals:
            result['recommended_actions'].append({'action': 'Preserve context caveat', 'signals': context_signals, 'context': context_text[:240]})
        if not result['recommended_actions']:
            result['recommended_actions'].append({'action': 'Keep answer caveated and cite any new factual claims', 'context': context_text[:240] or def_text[:240]})
        if safer_rewrites:
            result['recommended_actions'].append({'action': 'Use safer rewrites', 'rewrites': safer_rewrites})
        result['scores'] = {'confidence': round(min(0.92, 0.44 + min(0.24, 0.045 * len(sentences)) + min(0.16, 0.025 * len(context_signals)) + (0.08 if claims else 0)), 2), 'hallucination_risk': risk_score, 'citation_coverage': round(len([c for c in claims if c['has_citation']]) / max(1, len(claims)), 2), 'risk': risk_score, 'context_signal_count': len(context_signals)}
        result['details'] = {'claims': claims, 'high_risk_claims': high_risk, 'context_signals': context_signals, 'evaluated_text': text[:1200], 'safer_rewrites': safer_rewrites, 'missing_inputs': ['response or candidate_outputs'] if not raw_text and not candidate_outputs else []}
        result['details']['use_cases'] = use_cases
        result['details']['generation_note'] = generation_note
        result['details']['capability_type'] = capability_type
        result['details']['logic_profile_id'] = logic_profile_id
        result['details']['payload_warnings'] = payload_warnings
        result['progress_state'] = {
            'current_stage': logic_profile_id,
            'next_step': 'Verify the highest-risk uncited claim.',
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
            'optional_next_challenge': 'Verify the highest-risk uncited claim.',
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
