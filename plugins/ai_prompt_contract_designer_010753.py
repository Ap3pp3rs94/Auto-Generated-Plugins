from __future__ import annotations

"""
Auto-generated Francis AI capability module.

THIS FILE IS GENERATED. Manual edits may be overwritten by the factory.

Capability: AI Prompt Contract Designer 010753
Slug: ai_prompt_contract_designer_010753
"""

from typing import Any, Dict, Optional

__all__ = ["invoke", "_run_core_logic", "SkillContext"]

_PLUGIN_NAME: str = 'AI Prompt Contract Designer 010753'
_PLUGIN_SLUG: str = 'ai_prompt_contract_designer_010753'
_PLUGIN_CATEGORY: str = 'ai_prompting'
_PLUGIN_VERSION: str = '0.1.0'
_PLUGIN_GOAL: str = 'Design prompt contracts for AI procurement intake, vendor comparison, contract handoff, and spend review workflows for safety controls with explicit inputs, outputs, constraints, and checks.'
_PLUGIN_TAGS = ['procurement', 'vendors', 'contracts', 'safety', 'controls', 'prompting', 'schemas', 'continuous_backlog', 'use_case_seeded', 'autonomous_factory', 'ai_progress']
_PLUGIN_OWNER_ID = 'francis-factory'
_PLUGIN_CAPABILITY_TYPE = 'enrichment'
_PLUGIN_INTENDED_DOMAIN = 'AI procurement intake, vendor comparison, contract handoff, and spend review workflows for safety controls prompt contracts and structured instruction design'
_PLUGIN_USE_CASES = ['Apply this capability to the distinct use case: Procurement Ops Safety Controls.', 'Turn loose Procurement Ops Safety Controls requests into strict prompt contracts.', 'Name required inputs, outputs, constraints, and validation checks.', 'Flag contract gaps before the prompt is sent to a model.', 'Show a compact progress state for this AI capability during baseline capability.', 'Return user-facing guidance that is useful, concise, and safe to act on.', 'Avoid duplicating existing AI capability behavior; identify what is unique about this capability.']
_PLUGIN_RESULT_SCHEMA_VERSION: str = "1.0.0"
_PLUGIN_MANIFEST = {'name': 'AI Prompt Contract Designer 010753', 'slug': 'ai_prompt_contract_designer_010753', 'goal': 'Design prompt contracts for AI procurement intake, vendor comparison, contract handoff, and spend review workflows for safety controls with explicit inputs, outputs, constraints, and checks.', 'category': 'ai_prompting', 'tags': ['procurement', 'vendors', 'contracts', 'safety', 'controls', 'prompting', 'schemas', 'continuous_backlog', 'use_case_seeded', 'autonomous_factory', 'ai_progress'], 'version': '0.1.0', 'capability_type': 'enrichment', 'intended_domain': 'AI procurement intake, vendor comparison, contract handoff, and spend review workflows for safety controls prompt contracts and structured instruction design', 'owner_id': 'francis-factory', 'use_cases': ['Apply this capability to the distinct use case: Procurement Ops Safety Controls.', 'Turn loose Procurement Ops Safety Controls requests into strict prompt contracts.', 'Name required inputs, outputs, constraints, and validation checks.', 'Flag contract gaps before the prompt is sent to a model.', 'Show a compact progress state for this AI capability during baseline capability.', 'Return user-facing guidance that is useful, concise, and safe to act on.', 'Avoid duplicating existing AI capability behavior; identify what is unique about this capability.'], 'schema_version': '1.0.0'}
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
        plugin_name = 'AI Prompt Contract Designer 010753'
        goal = 'Design prompt contracts for AI procurement intake, vendor comparison, contract handoff, and spend review workflows for safety controls with explicit inputs, outputs, constraints, and checks.'
        domain = 'AI procurement intake, vendor comparison, contract handoff, and spend review workflows for safety controls prompt contracts and structured instruction design'
        capability_type = 'enrichment'
        logic_profile_id = 'continuous_prompt_contract_designer_profile'
        generation_note = 'capability profile registry override'
        use_cases = ['Apply this capability to the distinct use case: Procurement Ops Safety Controls.', 'Turn loose Procurement Ops Safety Controls requests into strict prompt contracts.', 'Name required inputs, outputs, constraints, and validation checks.', 'Flag contract gaps before the prompt is sent to a model.', 'Show a compact progress state for this AI capability during baseline capability.', 'Return user-facing guidance that is useful, concise, and safe to act on.']
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
        requirements = payload_data.get('requirements') if isinstance(payload_data.get('requirements'), list) else constraints
        role = str(payload_data.get('role') or 'expert AI assistant')
        inputs = payload_data.get('inputs') if isinstance(payload_data.get('inputs'), list) else ['task', 'context', 'constraints']
        output_schema = payload_data.get('output_schema') if isinstance(payload_data.get('output_schema'), dict) else {'summary': 'string', 'steps': 'list', 'checks': 'list'}
        prompt_surface = ' '.join([def_text, objective_text, ' '.join(str(item) for item in requirements), str(payload_data.get('prompt') or '')]).lower()
        prompt_risk_tags = []
        for label, terms in [
            ('release_or_auth_prompt', ['auth', 'login', 'database', 'migration', 'rollback', 'production']),
            ('factual_grounding_prompt', ['medical', 'clinical', 'citation', 'claim', 'source', 'unsupported']),
            ('tooling_prompt', ['tool', 'retrieval', 'browse', 'trace', 'consistency']),
        ]:
            hits = [term for term in terms if term in prompt_surface]
            if hits:
                prompt_risk_tags.append({'category': label, 'signals': hits})
        checklist = ['list assumptions', 'risks', 'verification steps']
        if any(tag['category'] == 'factual_grounding_prompt' for tag in prompt_risk_tags):
            checklist.append('cite or flag unsupported factual claims')
        if any(tag['category'] == 'release_or_auth_prompt' for tag in prompt_risk_tags):
            checklist.append('include rollback and regression-test checks')
        structured_prompt = 'Role: ' + role + '\nTask: ' + def_text + '\nObjective: ' + objective_text + '\nInputs: ' + ', '.join(str(item) for item in inputs) + '\nRequirements: ' + '; '.join(str(item) for item in requirements) + '\nOutput schema: ' + str(output_schema) + '\nChecks: ' + '; '.join(checklist) + '.'
        result['summary'] = plugin_name + ': built a structured prompt template with role, inputs, outputs, and checks.'
        result['primary_insights'] = [
            {'title': 'Structured prompt', 'detail': structured_prompt},
            {'title': 'Output schema', 'detail': output_schema},
            {'title': 'Prompt risk tags', 'detail': prompt_risk_tags or 'No specialized prompt risk tags.'},
        ]
        result['recommended_actions'] = [
            {'action': 'Use structured prompt', 'prompt': structured_prompt},
            {'action': 'Validate output against schema', 'schema': output_schema},
            {'action': 'Run specialized checks', 'checks': checklist, 'risk_tags': prompt_risk_tags},
        ]
        risk_signal_count = sum(len(tag['signals']) for tag in prompt_risk_tags)
        result['scores'] = {'confidence': round(min(0.92, 0.48 + 0.06 * len([role, inputs, output_schema]) + min(0.16, len(def_text.split()) / 140) + 0.025 * len(checklist)), 2), 'structure_completeness': round(min(0.98, 0.5 + 0.08 * len([role, inputs, output_schema, requirements]) + 0.03 * len(checklist)), 2), 'risk': round(min(0.85, 0.14 + 0.035 * risk_signal_count + (0.08 if not requirements else 0)), 2), 'risk_signal_count': risk_signal_count}
        result['details'] = {'structured_prompt': structured_prompt, 'role': role, 'inputs': inputs, 'output_schema': output_schema, 'requirements': requirements, 'checklist': checklist, 'prompt_risk_tags': prompt_risk_tags, 'missing_inputs': ['requirements'] if not requirements else []}
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
            'next_step': 'Use structured prompt',
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
            'optional_next_challenge': 'Use structured prompt',
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
