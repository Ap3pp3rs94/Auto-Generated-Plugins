from __future__ import annotations

"""
Auto-generated Francis AI capability module.

THIS FILE IS GENERATED. Manual edits may be overwritten by the factory.

Capability: AI Model Fit Triage 008470
Slug: ai_model_fit_triage_008470
"""

from typing import Any, Dict, Optional

__all__ = ["invoke", "_run_core_logic", "SkillContext"]

_PLUGIN_NAME: str = 'AI Model Fit Triage 008470'
_PLUGIN_SLUG: str = 'ai_model_fit_triage_008470'
_PLUGIN_CATEGORY: str = 'ai_agents'
_PLUGIN_VERSION: str = '0.1.0'
_PLUGIN_GOAL: str = 'Triage which model tier or workflow style fits AI personal productivity and scheduling workflows for agentic planning for detecting signals tasks based on risk and complexity.'
_PLUGIN_TAGS = ['productivity', 'assistant', 'agentic', 'planning', 'detect', 'models', 'routing', 'triage', 'continuous_backlog', 'use_case_seeded', 'autonomous_factory', 'ai_progress']
_PLUGIN_OWNER_ID = 'francis-factory'
_PLUGIN_CAPABILITY_TYPE = 'scoring'
_PLUGIN_INTENDED_DOMAIN = 'AI personal productivity and scheduling workflows for agentic planning for detecting signals model selection and capability fit'
_PLUGIN_USE_CASES = ['Apply this capability to the distinct use case: Personal Assistant Agentic Planning Detection.', 'Score whether a task needs fast, cheap, reasoning-heavy, or tool-using flow.', 'Flag tasks that need stronger verification.', 'Recommend the lowest sufficient capability tier.', 'Show a compact progress state for this AI capability during baseline capability.', 'Return user-facing guidance that is useful, concise, and safe to act on.', 'Avoid duplicating existing AI capability behavior; identify what is unique about this capability.']
_PLUGIN_RESULT_SCHEMA_VERSION: str = "1.0.0"
_PLUGIN_MANIFEST = {'name': 'AI Model Fit Triage 008470', 'slug': 'ai_model_fit_triage_008470', 'goal': 'Triage which model tier or workflow style fits AI personal productivity and scheduling workflows for agentic planning for detecting signals tasks based on risk and complexity.', 'category': 'ai_agents', 'tags': ['productivity', 'assistant', 'agentic', 'planning', 'detect', 'models', 'routing', 'triage', 'continuous_backlog', 'use_case_seeded', 'autonomous_factory', 'ai_progress'], 'version': '0.1.0', 'capability_type': 'scoring', 'intended_domain': 'AI personal productivity and scheduling workflows for agentic planning for detecting signals model selection and capability fit', 'owner_id': 'francis-factory', 'use_cases': ['Apply this capability to the distinct use case: Personal Assistant Agentic Planning Detection.', 'Score whether a task needs fast, cheap, reasoning-heavy, or tool-using flow.', 'Flag tasks that need stronger verification.', 'Recommend the lowest sufficient capability tier.', 'Show a compact progress state for this AI capability during baseline capability.', 'Return user-facing guidance that is useful, concise, and safe to act on.', 'Avoid duplicating existing AI capability behavior; identify what is unique about this capability.'], 'schema_version': '1.0.0'}
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
        plugin_name = 'AI Model Fit Triage 008470'
        goal = 'Triage which model tier or workflow style fits AI personal productivity and scheduling workflows for agentic planning for detecting signals tasks based on risk and complexity.'
        domain = 'AI personal productivity and scheduling workflows for agentic planning for detecting signals model selection and capability fit'
        capability_type = 'scoring'
        logic_profile_id = 'continuous_model_fit_triage_profile'
        generation_note = 'capability profile registry override'
        use_cases = ['Apply this capability to the distinct use case: Personal Assistant Agentic Planning Detection.', 'Score whether a task needs fast, cheap, reasoning-heavy, or tool-using flow.', 'Flag tasks that need stronger verification.', 'Recommend the lowest sufficient capability tier.', 'Show a compact progress state for this AI capability during baseline capability.', 'Return user-facing guidance that is useful, concise, and safe to act on.']
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
        quality_failures = payload_data.get('quality_failures') if isinstance(payload_data.get('quality_failures'), list) else []
        surface_parts = [
            def_text,
            objective_text,
            str(payload_data.get('prompt') or ''),
            ' '.join(str(item) for item in constraints),
            ' '.join(str(item) for item in current_plan),
            ' '.join(str(item) for item in completed_steps),
            ' '.join(str(item) for item in blocked_steps),
            ' '.join(str(item) for item in candidate_outputs),
            ' '.join(str(item) for item in source_notes),
            ' '.join(str(item) for item in agents),
            ' '.join(str(item) for item in workstreams),
            ' '.join(str(item) for item in ownership_scopes),
            ' '.join(str(item) for item in quality_failures),
        ]
        surface = ' '.join(surface_parts).lower()
        tiers = [
            {'model_style': 'fast_small_model', 'cost': 'low', 'strength': 'simple routing, formatting, extraction', 'signals': ['simple', 'format', 'extract', 'classify', 'summarize']},
            {'model_style': 'standard_tool_model', 'cost': 'medium', 'strength': 'tool use, code edits, repo work', 'signals': ['tool', 'code', 'repo', 'github', 'plugin', 'test', 'auth', 'database', 'rollback', 'production', 'commit', 'push', 'validation']},
            {'model_style': 'reasoning_model', 'cost': 'high', 'strength': 'ambiguous planning, debugging, multi-step synthesis', 'signals': ['complex', 'multi-step', 'debug', 'architecture', 'risk', 'refactor', 'migration', 'owner', 'semantic', 'quality', 'duplicate', 'shallow']},
            {'model_style': 'verified_grounded_model', 'cost': 'high', 'strength': 'source-sensitive factual answers', 'signals': ['citation', 'citations', 'medical', 'clinical', 'legal', 'financial', 'latest', 'source', 'claim', 'grounded', 'evidence']},
        ]
        scorecard = []
        for tier in tiers:
            hits = [signal for signal in tier['signals'] if signal in surface]
            score = round(0.25 + 0.16 * len(hits), 2)
            if tier['model_style'] == 'reasoning_model' and len(surface.split()) > 45:
                score += 0.12
            if tier['model_style'] == 'standard_tool_model' and (current_plan or completed_steps or 'github' in surface):
                score += 0.08
            if tier['model_style'] == 'verified_grounded_model' and source_notes:
                score += 0.07
            scorecard.append(dict(tier, matched_signals=hits, score=round(min(0.95, score), 2)))
        scorecard = sorted(scorecard, key=lambda item: item['score'], reverse=True)
        selected = scorecard[0]
        selected_next_steps = {
            'fast_small_model': 'Use fast_small_model only for extraction or formatting with low ambiguity.',
            'standard_tool_model': 'Use standard_tool_model with repo/tool checks before finalizing.',
            'reasoning_model': 'Use reasoning_model for decomposition, risk review, and multi-step debugging.',
            'verified_grounded_model': 'Use verified_grounded_model with citations and claim checks before answering.',
        }
        selected_next_step = selected_next_steps.get(selected['model_style'], 'Use selected model style with validation.')
        escalation_triggers = []
        if any(term in surface for term in ['production', 'auth', 'database', 'rollback']):
            escalation_triggers.append('production_or_release_risk')
        if any(term in surface for term in ['medical', 'legal', 'financial', 'citation', 'latest']):
            escalation_triggers.append('source_sensitive_claims')
        cost_risk_tradeoffs = [tier['model_style'] + ': cost=' + tier['cost'] + ', score=' + str(tier['score']) for tier in scorecard]
        selected_signals = selected.get('matched_signals', [])
        if selected['model_style'] == 'verified_grounded_model':
            decision_mode = 'source_grounded_verification'
            selected_next_step = selected_next_step + ' Prioritize source retrieval, citation inspection, and unsupported-claim caveats.'
        elif selected['model_style'] == 'standard_tool_model':
            decision_mode = 'repo_tool_execution'
            selected_next_step = selected_next_step + ' Prioritize repository inspection, targeted tests, rollback notes, and changed-file evidence.'
        elif selected['model_style'] == 'reasoning_model':
            decision_mode = 'deep_reasoning_planning'
            selected_next_step = selected_next_step + ' Prioritize decomposition, risk registers, and explicit assumption checks.'
        else:
            decision_mode = 'low_ambiguity_fast_path'
            selected_next_step = selected_next_step + ' Keep the task bounded to extraction, formatting, or classification.'
        selection_matrix = [
            {
                'model_style': item['model_style'],
                'score': item['score'],
                'matched_signals': item.get('matched_signals', []),
                'best_for': item['strength'],
                'cost': item['cost'],
                'fit_decision': 'selected' if item['model_style'] == selected['model_style'] else 'available_if_scope_changes',
            }
            for item in scorecard
        ]
        verification_requirements = []
        if selected['model_style'] in ['standard_tool_model', 'reasoning_model']:
            verification_requirements.extend(['inspect affected artifacts', 'run targeted checks', 'record changed-file evidence'])
        if selected['model_style'] == 'verified_grounded_model' or source_notes:
            verification_requirements.extend(['separate supported claims from uncertain claims', 'cite or flag source-sensitive statements'])
        if blocked_steps or quality_failures:
            verification_requirements.extend(['resolve blockers before final answer', 'confirm shallow or duplicate output was rejected'])
        if not verification_requirements:
            verification_requirements.append('confirm output matches the requested format and constraints')
        model_route_plan = {
            'recommended_model_style': selected['model_style'],
            'decision_mode': decision_mode,
            'why': selected_signals or ['no strong signal; selected lowest-risk fit'],
            'execution_policy': selected_next_step,
            'verification_requirements': verification_requirements,
            'fallback_model_style': 'reasoning_model' if selected['model_style'] != 'reasoning_model' else 'verified_grounded_model',
        }
        cost_control_plan = [
            {'step': 'start_with_selected_route', 'policy': selected['model_style'], 'reason': 'highest signal score for the supplied payload'},
            {'step': 'escalate_only_on_trigger', 'policy': escalation_triggers or ['no escalation trigger'], 'reason': 'keep cost tied to explicit risk'},
            {'step': 'downgrade_after_structure_is_clear', 'policy': 'fast_small_model for formatting or extraction follow-ups', 'reason': 'avoid paying for reasoning after the hard decision is made'},
        ]
        escalation_matrix = [
            {'trigger': 'production_or_release_risk', 'route_to': 'standard_tool_model or reasoning_model', 'present': 'production_or_release_risk' in escalation_triggers},
            {'trigger': 'source_sensitive_claims', 'route_to': 'verified_grounded_model', 'present': 'source_sensitive_claims' in escalation_triggers},
            {'trigger': 'semantic_quality_failure', 'route_to': 'reasoning_model', 'present': bool(quality_failures or 'shallow' in surface or 'duplicate' in surface)},
        ]
        result['summary'] = plugin_name + ': selected ' + selected['model_style'] + ' for ' + decision_mode + ' on ' + def_text[:120] + '.'
        result['primary_insights'] = [
            {'title': 'Selected model path', 'detail': {'model_style': selected['model_style'], 'decision_mode': decision_mode, 'matched_signals': selected_signals, 'strength': selected['strength']}},
            {'title': 'Escalation triggers', 'detail': escalation_triggers or 'No escalation trigger detected.'},
            {'title': 'Why this path', 'detail': 'Matched signals: ' + (', '.join(selected_signals) if selected_signals else 'none') + '; task focus: ' + def_text[:120]},
            {'title': 'Verification requirements', 'detail': verification_requirements},
            {'title': 'Cost control plan', 'detail': cost_control_plan},
        ]
        result['recommended_actions'] = [
            {'action': selected_next_step, 'selected_model_style': selected['model_style'], 'decision_mode': decision_mode, 'matched_signals': selected_signals},
            {'action': 'Use escalation triggers before execution', 'triggers': escalation_triggers, 'decision_mode': decision_mode},
            {'action': 'Apply verification requirements before finalizing', 'verification_requirements': verification_requirements},
            {'action': 'Keep the cost route explicit', 'cost_control_plan': cost_control_plan},
            {'action': 'Record model route decision for downstream agents', 'model_route_plan': model_route_plan},
        ]
        result['scores'] = {'confidence': round(min(0.94, selected['score'] + 0.1 + 0.025 * len(selected.get('matched_signals', [])) + 0.03 * bool(verification_requirements)), 2), 'usefulness': round(min(0.95, 0.66 + 0.04 * len(result['recommended_actions']) + 0.03 * bool(selection_matrix)), 2), 'selection_score': selected['score'], 'risk': round(min(0.9, 0.18 + 0.12 * len(escalation_triggers) + (0.08 if selected['model_style'] == 'verified_grounded_model' else 0)), 2), 'cost_pressure': 0.25 if selected['cost'] == 'low' else 0.55 if selected['cost'] == 'medium' else 0.8, 'route_specificity': round(min(0.95, 0.45 + 0.04 * len(selected_signals) + 0.03 * len(verification_requirements)), 2)}
        result['details'] = {'model_scorecard': scorecard, 'selection_matrix': selection_matrix, 'selected_model_style': selected, 'selected_next_step': selected_next_step, 'decision_mode': decision_mode, 'selected_signals': selected_signals, 'cost_risk_tradeoffs': cost_risk_tradeoffs, 'escalation_triggers': escalation_triggers, 'verification_requirements': verification_requirements, 'model_route_plan': model_route_plan, 'cost_control_plan': cost_control_plan, 'escalation_matrix': escalation_matrix, 'input_evidence': {'current_plan': current_plan, 'completed_steps': completed_steps, 'blocked_steps': blocked_steps, 'quality_failures': quality_failures}, 'missing_inputs': ['task or objective'] if not has_user_input else []}
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
            'next_step': selected_next_step,
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
            'optional_next_challenge': selected_next_step,
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
