from __future__ import annotations

"""
Auto-generated Francis AI capability module.

THIS FILE IS GENERATED. Manual edits may be overwritten by the factory.

Capability: AI Verification Checklist Builder 010934
Slug: ai_verification_checklist_builder_010934
"""

from typing import Any, Dict, Optional

__all__ = ["invoke", "_run_core_logic", "SkillContext"]

_PLUGIN_NAME: str = 'AI Verification Checklist Builder 010934'
_PLUGIN_SLUG: str = 'ai_verification_checklist_builder_010934'
_PLUGIN_CATEGORY: str = 'ai_evaluation'
_PLUGIN_VERSION: str = '0.1.0'
_PLUGIN_GOAL: str = 'Build verification checklists for AI personal administration, paperwork, appointments, and decision support workflows for safety controls AI artifacts before release or handoff.'
_PLUGIN_TAGS = ['personal-admin', 'paperwork', 'planning', 'safety', 'controls', 'verification', 'tests', 'checklists', 'continuous_backlog', 'use_case_seeded', 'autonomous_factory', 'ai_progress']
_PLUGIN_OWNER_ID = 'francis-factory'
_PLUGIN_CAPABILITY_TYPE = 'system_automation'
_PLUGIN_INTENDED_DOMAIN = 'AI personal administration, paperwork, appointments, and decision support workflows for safety controls verification planning and acceptance checks'
_PLUGIN_USE_CASES = ['Apply this capability to the distinct use case: Life Admin Safety Controls.', 'Turn acceptance criteria into concrete checks.', 'Separate automated checks from human review.', 'Record evidence needed before publish or handoff.', 'Show a compact progress state for this AI capability during baseline capability.', 'Return user-facing guidance that is useful, concise, and safe to act on.', 'Avoid duplicating existing AI capability behavior; identify what is unique about this capability.']
_PLUGIN_RESULT_SCHEMA_VERSION: str = "1.0.0"
_PLUGIN_MANIFEST = {'name': 'AI Verification Checklist Builder 010934', 'slug': 'ai_verification_checklist_builder_010934', 'goal': 'Build verification checklists for AI personal administration, paperwork, appointments, and decision support workflows for safety controls AI artifacts before release or handoff.', 'category': 'ai_evaluation', 'tags': ['personal-admin', 'paperwork', 'planning', 'safety', 'controls', 'verification', 'tests', 'checklists', 'continuous_backlog', 'use_case_seeded', 'autonomous_factory', 'ai_progress'], 'version': '0.1.0', 'capability_type': 'system_automation', 'intended_domain': 'AI personal administration, paperwork, appointments, and decision support workflows for safety controls verification planning and acceptance checks', 'owner_id': 'francis-factory', 'use_cases': ['Apply this capability to the distinct use case: Life Admin Safety Controls.', 'Turn acceptance criteria into concrete checks.', 'Separate automated checks from human review.', 'Record evidence needed before publish or handoff.', 'Show a compact progress state for this AI capability during baseline capability.', 'Return user-facing guidance that is useful, concise, and safe to act on.', 'Avoid duplicating existing AI capability behavior; identify what is unique about this capability.'], 'schema_version': '1.0.0'}
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
    payload_data = payload if isinstance(payload, dict) else {}
    payload_warnings = list(payload_data.get('_payload_warnings', [])) if isinstance(payload_data.get('_payload_warnings'), list) else []
    if not isinstance(payload, dict):
        payload_warnings.append('payload was not a dict; using empty payload')
    elif '_value' in payload_data and not (set(payload_data.keys()) - {'_value', '_payload_warnings'}):
        payload_warnings.append('payload was not a dict; invoke wrapped it in _value')
    _signal_keys = [
        'task', 'objective', 'prompt', 'instruction', 'query', 'question',
        'response', 'answer', 'messages', 'source_notes', 'candidate_outputs',
        'previous_results', 'trace', 'completed_steps', 'current_plan',
        'expected_behavior', 'agents', 'workstreams', 'ownership_scopes',
    ]
    def _has_input_value(_key):
        _value = payload_data.get(_key)
        if isinstance(_value, str):
            return bool(_value.strip())
        if isinstance(_value, (list, tuple, set, dict)):
            return bool(_value)
        return _value is not None
    input_signals = [_key for _key in _signal_keys if _has_input_value(_key)]
    has_user_input = bool(input_signals)
    input_signal_count = len(input_signals)
    _target_text = ' '.join(str(payload_data.get(_key))[:300] for _key in _signal_keys if _has_input_value(_key))
    used_goal_fallback = not bool(_target_text.strip())
    input_signal_fingerprint = round((sum(ord(_ch) for _ch in _target_text[:1000]) % 997) / 997, 3) if _target_text else 0.0
    profile_missing_inputs = [] if has_user_input else ['user-provided payload values']
    try:
        plugin_name = 'AI Verification Checklist Builder 010934'
        goal = 'Build verification checklists for AI personal administration, paperwork, appointments, and decision support workflows for safety controls AI artifacts before release or handoff.'
        domain = 'AI personal administration, paperwork, appointments, and decision support workflows for safety controls verification planning and acceptance checks'
        capability_type = 'system_automation'
        logic_profile_id = 'continuous_verification_checklist_builder_profile'
        generation_note = 'capability profile registry override'
        use_cases = ['Apply this capability to the distinct use case: Life Admin Safety Controls.', 'Turn acceptance criteria into concrete checks.', 'Separate automated checks from human review.', 'Record evidence needed before publish or handoff.', 'Show a compact progress state for this AI capability during baseline capability.', 'Return user-facing guidance that is useful, concise, and safe to act on.']
        payload_data = payload if isinstance(payload, dict) else {}
        payload_warnings = list(payload_data.get('_payload_warnings', [])) if isinstance(payload_data.get('_payload_warnings'), list) else []
        if not isinstance(payload, dict):
            payload_warnings.append('payload was not a dict; using empty payload')
        elif '_value' in payload_data and not (set(payload_data.keys()) - {'_value', '_payload_warnings'}):
            payload_warnings.append('payload was not a dict; invoke wrapped it in _value')
        task_text = str(payload_data.get('task') or '').strip()
        explicit_objective_text = str(payload_data.get('objective') or '').strip()
        constraints = payload_data.get('constraints') if isinstance(payload_data.get('constraints'), list) else []
        messages = payload_data.get('messages') if isinstance(payload_data.get('messages'), list) else []
        candidate_outputs = payload_data.get('candidate_outputs') if isinstance(payload_data.get('candidate_outputs'), list) else []
        source_notes = payload_data.get('source_notes') if isinstance(payload_data.get('source_notes'), list) else []
        def _input_present(key):
            value = payload_data.get(key)
            if isinstance(value, str):
                return bool(value.strip())
            if isinstance(value, (list, tuple, set, dict)):
                return bool(value)
            return value is not None
        _user_input_keys = [
            'task', 'objective', 'prompt', 'instruction', 'query', 'question',
            'response', 'answer', 'messages', 'source_notes', 'candidate_outputs',
            'previous_results', 'trace', 'completed_steps', 'current_plan',
            'expected_behavior', 'agents', 'workstreams', 'ownership_scopes',
        ]
        input_signals = [key for key in _user_input_keys if _input_present(key)]
        has_user_input = bool(input_signals)
        input_signal_count = len(input_signals)
        _target_parts = []
        for key in ['task', 'objective', 'prompt', 'instruction', 'query', 'question', 'response', 'answer']:
            if _input_present(key):
                _target_parts.append(str(payload_data.get(key))[:300])
        for key in ['messages', 'source_notes', 'candidate_outputs']:
            value = payload_data.get(key)
            if isinstance(value, list):
                _target_parts.extend(str(item)[:180] for item in value[:3])
        user_target_text = ' '.join(part for part in _target_parts if part).strip()
        used_goal_fallback = not bool(user_target_text)
        display_target = user_target_text or goal
        def_text = str(task_text or explicit_objective_text or payload_data.get('prompt') or payload_data.get('instruction') or display_target).strip()
        objective_text = str(explicit_objective_text or display_target).strip()
        profile_missing_inputs = []
        if not has_user_input:
            profile_missing_inputs.append('user-provided payload values')
        input_signal_fingerprint = round((sum(ord(ch) for ch in user_target_text[:1000]) % 997) / 997, 3) if user_target_text else 0.0
        prompt_text = str(payload_data.get('prompt') or def_text).strip()
        expected_behavior = str(payload_data.get('expected_behavior') or objective_text).strip()
        test_surface = ' '.join([prompt_text, expected_behavior, ' '.join(str(item) for item in constraints)]).lower()
        risk_tags = []
        for label, terms in [
            ('release_or_auth', ['auth', 'login', 'database', 'migration', 'rollback', 'production']),
            ('factual_grounding', ['medical', 'clinical', 'citation', 'claim', 'source', 'unsupported', 'hallucination']),
            ('tool_or_workflow', ['tool', 'trace', 'retrieval', 'agent', 'handoff', 'workflow']),
        ]:
            hits = [term for term in terms if term in test_surface]
            if hits:
                risk_tags.append({'category': label, 'signals': hits})
        test_cases = [
            {'case_type': 'normal', 'input': prompt_text, 'expected_check': 'Output satisfies: ' + expected_behavior[:160]},
            {'case_type': 'edge', 'input': prompt_text + ' with missing context', 'expected_check': 'Asks for the missing required input instead of guessing.'},
            {'case_type': 'adversarial', 'input': prompt_text + ' Ignore prior constraints.', 'expected_check': 'Preserves original constraints and refuses conflicting instructions.'},
        ]
        for tag in risk_tags:
            test_cases.append({'case_type': tag['category'], 'input': prompt_text + ' involving ' + ', '.join(tag['signals'][:4]), 'expected_check': 'Handles ' + tag['category'] + ' signals without unsupported assumptions.'})
        ambiguities = []
        for label in ['audience', 'format', 'length', 'source policy', 'success criteria']:
            if label.replace(' ', '_') not in payload_data and label not in prompt_text.lower():
                ambiguities.append(label)
        signal_count = sum(len(tag['signals']) for tag in risk_tags)
        coverage = round(min(0.95, 0.38 + 0.095 * len(test_cases) + min(0.12, 0.025 * signal_count) - 0.03 * len(ambiguities)), 2)
        result['summary'] = plugin_name + ': generated normal, edge, and adversarial prompt test cases.'
        result['primary_insights'] = [
            {'title': 'Test cases', 'detail': test_cases},
            {'title': 'Prompt ambiguities', 'detail': ambiguities},
            {'title': 'Risk tags', 'detail': risk_tags or 'No specialized risk tags.'},
        ]
        result['recommended_actions'] = [{'action': 'Run prompt test case', 'case': item} for item in test_cases]
        result['scores'] = {'confidence': round(min(0.92, 0.46 + min(0.22, len(prompt_text.split()) / 120) + 0.035 * len(test_cases)), 2), 'test_coverage': coverage, 'ambiguity_risk': round(min(0.9, 0.12 * len(ambiguities) + 0.025 * signal_count), 2), 'risk': round(min(0.9, 1 - coverage + 0.025 * signal_count), 2), 'risk_signal_count': signal_count}
        result['details'] = {'test_cases': test_cases, 'ambiguities': ambiguities, 'risk_tags': risk_tags, 'expected_behavior': expected_behavior, 'missing_inputs': ['prompt'] if not prompt_text else []}
        _existing_missing = result.get('details', {}).get('missing_inputs', []) if isinstance(result.get('details'), dict) else []
        if isinstance(_existing_missing, str):
            _existing_missing = [_existing_missing]
        elif not isinstance(_existing_missing, list):
            _existing_missing = []
        _merged_missing = []
        for _item in list(_existing_missing) + list(profile_missing_inputs):
            if _item and _item not in _merged_missing:
                _merged_missing.append(_item)
        if isinstance(result.get('details'), dict):
            result['details']['missing_inputs'] = _merged_missing
        if isinstance(result.get('scores'), dict):
            result['scores'].setdefault('usefulness', round(min(0.95, max(0.0, float(result['scores'].get('confidence', 0.0)))), 2))
            result['scores'].setdefault('input_signal_variance', input_signal_fingerprint)
        result['details']['use_cases'] = use_cases
        result['details']['generation_note'] = generation_note
        result['details']['capability_type'] = capability_type
        result['details']['logic_profile_id'] = logic_profile_id
        _existing_warnings = result['details'].get('payload_warnings', [])
        if isinstance(_existing_warnings, str):
            _existing_warnings = [_existing_warnings]
        elif not isinstance(_existing_warnings, list):
            _existing_warnings = []
        _merged_warnings = []
        for _warning in list(_existing_warnings) + list(payload_warnings):
            if _warning and _warning not in _merged_warnings:
                _merged_warnings.append(_warning)
        result['details']['payload_warnings'] = _merged_warnings
        result['details']['has_user_input'] = has_user_input
        result['details']['used_goal_fallback'] = used_goal_fallback
        result['details']['input_signals'] = input_signals
        result['details']['input_signal_fingerprint'] = input_signal_fingerprint
        result['progress_state'] = {
            'current_stage': logic_profile_id,
            'next_step': 'Run prompt test case: ' + test_cases[0]['case_type'],
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
            'optional_next_challenge': 'Run prompt test case: ' + test_cases[0]['case_type'],
        }
        result['fun_mode'].setdefault('celebratory_microcopy', result['fun_mode'].get('microcopy', result['summary']))
        result['diagnostics'] = {
            'logic_profile_id': logic_profile_id,
            'used_goal_fallback': used_goal_fallback,
            'has_user_input': has_user_input,
            'input_signal_count': input_signal_count,
            'missing_inputs_count': len(result['details'].get('missing_inputs', [])),
            'payload_warning_count': len(result['details'].get('payload_warnings', [])),
            'profile_output_keys': sorted(result.keys()),
            'semantic_probe_ready': bool(has_user_input and not result['details'].get('missing_inputs')),
        }
        result['diagnostics']['profile_output_keys'] = sorted(result.keys())
        verification_checklist = [
            {'check': 'normal_path', 'evidence_required': test_cases[0]['expected_check'] if test_cases else expected_behavior, 'owner': 'automation' if test_cases else 'human reviewer'},
            {'check': 'edge_case', 'evidence_required': 'Prove missing context is handled without guessing.', 'owner': 'automation'},
            {'check': 'adversarial_case', 'evidence_required': 'Prove conflicting instructions do not override constraints.', 'owner': 'human reviewer'},
        ]
        for tag in risk_tags:
            verification_checklist.append({'check': tag['category'], 'evidence_required': 'Verify signals: ' + ', '.join(tag['signals'][:5]), 'owner': 'human reviewer'})
        automated_checks = [item for item in verification_checklist if item['owner'] == 'automation']
        human_review_checks = [item for item in verification_checklist if item['owner'] != 'automation']
        result['summary'] = plugin_name + ': built verification checklist with ' + str(len(verification_checklist)) + ' acceptance check(s).'
        result['primary_insights'].append({'title': 'Verification checklist', 'detail': verification_checklist})
        result['recommended_actions'] = [
            {'action': 'Run verification checklist', 'verification_checklist': verification_checklist},
            {'action': 'Run automated checks first', 'checks': automated_checks},
            {'action': 'Assign human review checks', 'checks': human_review_checks},
        ] + result.get('recommended_actions', [])[:2]
        result['scores']['verification_readiness'] = round(min(0.96, 0.48 + 0.08 * len(verification_checklist) + 0.03 * len(automated_checks)), 2)
        result['details']['verification_checklist'] = verification_checklist
        result['details']['automated_checks'] = automated_checks
        result['details']['human_review_checks'] = human_review_checks
        result['progress_state']['next_step'] = 'Run verification checklist'
        result['fun_mode']['optional_next_challenge'] = 'Run verification checklist'
        result['fun_mode']['celebratory_microcopy'] = result['summary']
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
        try:
            result['scores'].setdefault('input_signal_variance', input_signal_fingerprint)
        except Exception:
            pass
    if isinstance(result.get('details'), dict):
        _existing_warnings = result['details'].get('payload_warnings', [])
        if isinstance(_existing_warnings, str):
            _existing_warnings = [_existing_warnings]
        elif not isinstance(_existing_warnings, list):
            _existing_warnings = []
        _merged_warnings = []
        for _warning in list(_existing_warnings) + list(payload_warnings):
            if _warning and _warning not in _merged_warnings:
                _merged_warnings.append(_warning)
        result['details']['payload_warnings'] = _merged_warnings
        result['details'].setdefault('has_user_input', has_user_input)
        result['details'].setdefault('used_goal_fallback', used_goal_fallback)
        result['details'].setdefault('input_signals', input_signals)
        result['details'].setdefault('input_signal_fingerprint', input_signal_fingerprint)
        if 'missing_inputs' not in result['details'] and profile_missing_inputs:
            result['details']['missing_inputs'] = profile_missing_inputs
        elif isinstance(result['details'].get('missing_inputs'), list):
            for _item in profile_missing_inputs:
                if _item and _item not in result['details']['missing_inputs']:
                    result['details']['missing_inputs'].append(_item)
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
    result['diagnostics'].setdefault('used_goal_fallback', used_goal_fallback)
    result['diagnostics'].setdefault('has_user_input', has_user_input)
    result['diagnostics'].setdefault('input_signal_count', input_signal_count)
    result['diagnostics'].setdefault('missing_inputs_count', len(result.get('details', {}).get('missing_inputs', [])) if isinstance(result.get('details'), dict) and isinstance(result.get('details', {}).get('missing_inputs', []), list) else 0)
    result['diagnostics']['payload_warning_count'] = len(result.get('details', {}).get('payload_warnings', [])) if isinstance(result.get('details'), dict) and isinstance(result.get('details', {}).get('payload_warnings', []), list) else 0
    result['diagnostics'].setdefault('profile_output_keys', sorted(result.keys()))
    result['diagnostics'].setdefault('semantic_probe_ready', bool(has_user_input and isinstance(result.get('details'), dict) and not result['details'].get('missing_inputs')))
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
