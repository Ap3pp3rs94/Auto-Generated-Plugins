from __future__ import annotations

"""
Auto-generated Francis AI capability module.

THIS FILE IS GENERATED. Manual edits may be overwritten by the factory.

Capability: AI Agent Handoff Checker 008887
Slug: ai_agent_handoff_checker_008887
"""

from typing import Any, Dict, Optional

__all__ = ["invoke", "_run_core_logic", "SkillContext"]

_PLUGIN_NAME: str = 'AI Agent Handoff Checker 008887'
_PLUGIN_SLUG: str = 'ai_agent_handoff_checker_008887'
_PLUGIN_CATEGORY: str = 'ai_agents'
_PLUGIN_VERSION: str = '0.1.0'
_PLUGIN_GOAL: str = 'Check AI capability factory and generated module operations for AI tool use for detecting signals agent handoffs for missing context, ownership overlap, and unsafe next steps.'
_PLUGIN_TAGS = ['capabilities', 'factory', 'tools', 'tool-use', 'detect', 'agents', 'handoff', 'coordination', 'continuous_backlog', 'use_case_seeded', 'autonomous_factory', 'ai_progress']
_PLUGIN_OWNER_ID = 'francis-factory'
_PLUGIN_CAPABILITY_TYPE = 'system_automation'
_PLUGIN_INTENDED_DOMAIN = 'AI capability factory and generated module operations for AI tool use for detecting signals agent handoff quality and coordination'
_PLUGIN_USE_CASES = ['Apply this capability to the distinct use case: Capability Factory Tool Use Detection.', 'Validate handoff packets before another agent starts.', 'Detect duplicated ownership and missing changed-file context.', 'Recommend handoff fixes and integration checkpoints.', 'Show a compact progress state for this AI capability during baseline capability.', 'Return user-facing guidance that is useful, concise, and safe to act on.', 'Avoid duplicating existing AI capability behavior; identify what is unique about this capability.']
_PLUGIN_RESULT_SCHEMA_VERSION: str = "1.0.0"
_PLUGIN_MANIFEST = {'name': 'AI Agent Handoff Checker 008887', 'slug': 'ai_agent_handoff_checker_008887', 'goal': 'Check AI capability factory and generated module operations for AI tool use for detecting signals agent handoffs for missing context, ownership overlap, and unsafe next steps.', 'category': 'ai_agents', 'tags': ['capabilities', 'factory', 'tools', 'tool-use', 'detect', 'agents', 'handoff', 'coordination', 'continuous_backlog', 'use_case_seeded', 'autonomous_factory', 'ai_progress'], 'version': '0.1.0', 'capability_type': 'system_automation', 'intended_domain': 'AI capability factory and generated module operations for AI tool use for detecting signals agent handoff quality and coordination', 'owner_id': 'francis-factory', 'use_cases': ['Apply this capability to the distinct use case: Capability Factory Tool Use Detection.', 'Validate handoff packets before another agent starts.', 'Detect duplicated ownership and missing changed-file context.', 'Recommend handoff fixes and integration checkpoints.', 'Show a compact progress state for this AI capability during baseline capability.', 'Return user-facing guidance that is useful, concise, and safe to act on.', 'Avoid duplicating existing AI capability behavior; identify what is unique about this capability.'], 'schema_version': '1.0.0'}
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
        plugin_name = 'AI Agent Handoff Checker 008887'
        goal = 'Check AI capability factory and generated module operations for AI tool use for detecting signals agent handoffs for missing context, ownership overlap, and unsafe next steps.'
        domain = 'AI capability factory and generated module operations for AI tool use for detecting signals agent handoff quality and coordination'
        capability_type = 'system_automation'
        logic_profile_id = 'continuous_agent_handoff_checker_profile'
        generation_note = 'capability profile registry override'
        use_cases = ['Apply this capability to the distinct use case: Capability Factory Tool Use Detection.', 'Validate handoff packets before another agent starts.', 'Detect duplicated ownership and missing changed-file context.', 'Recommend handoff fixes and integration checkpoints.', 'Show a compact progress state for this AI capability during baseline capability.', 'Return user-facing guidance that is useful, concise, and safe to act on.']
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
        current_plan = payload_data.get('current_plan') if isinstance(payload_data.get('current_plan'), list) else []
        completed_steps = payload_data.get('completed_steps') if isinstance(payload_data.get('completed_steps'), list) else []
        blocked_steps = payload_data.get('blocked_steps') if isinstance(payload_data.get('blocked_steps'), list) else []
        agents = payload_data.get('agents') if isinstance(payload_data.get('agents'), list) else []
        workstreams = payload_data.get('workstreams') if isinstance(payload_data.get('workstreams'), list) else []
        ownership_scopes = payload_data.get('ownership_scopes') if isinstance(payload_data.get('ownership_scopes'), list) else []
        ownership_boundaries = []
        if agents or workstreams or ownership_scopes:
            max_items = max(len(agents), len(workstreams), len(ownership_scopes), 1)
            for idx in range(max_items):
                ownership_boundaries.append({
                    'agent': str(agents[idx]) if idx < len(agents) else 'agent_' + str(idx + 1),
                    'workstream': str(workstreams[idx]) if idx < len(workstreams) else 'unassigned workstream',
                    'owns': str(ownership_scopes[idx]) if idx < len(ownership_scopes) else 'scope requires owner',
                    'handoff_required': True,
                })
        handoff_overlap_decision = 'handoff_ready' if ownership_boundaries else 'repair_or_merge'
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
        result['summary'] = plugin_name + ': built a multi-agent handoff plan with ownership boundaries for ' + def_text[:140] + '.'
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
        result['details'] = {'sequenced_plan': sequenced_plan, 'handoff_packet': handoff_packet, 'ownership_boundaries': ownership_boundaries, 'handoff_overlap_decision': handoff_overlap_decision, 'handoff_inputs': {'agents': agents, 'workstreams': workstreams, 'ownership_scopes': ownership_scopes}, 'risk_signals': risk_signals, 'complexity_terms': complexity_terms, 'specialized_action_count': len(capability_actions), 'missing_inputs': [key for key in ['objective', 'current_plan', 'blocked_steps'] if not payload_data.get(key)]}
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
