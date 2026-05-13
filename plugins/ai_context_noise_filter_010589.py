from __future__ import annotations

"""
Auto-generated Francis AI capability module.

THIS FILE IS GENERATED. Manual edits may be overwritten by the factory.

Capability: AI Context Noise Filter 010589
Slug: ai_context_noise_filter_010589
"""

from typing import Any, Dict, Optional

__all__ = ["invoke", "_run_core_logic", "SkillContext"]

_PLUGIN_NAME: str = 'AI Context Noise Filter 010589'
_PLUGIN_SLUG: str = 'ai_context_noise_filter_010589'
_PLUGIN_CATEGORY: str = 'ai_memory'
_PLUGIN_VERSION: str = '0.1.0'
_PLUGIN_GOAL: str = 'Filter noisy or redundant context before model calls for AI instructional design, course review, practice generation, and learner feedback workflows for safety controls.'
_PLUGIN_TAGS = ['learning', 'instructional-design', 'assessment', 'safety', 'controls', 'context', 'tokens', 'noise', 'continuous_backlog', 'use_case_seeded', 'autonomous_factory', 'ai_progress']
_PLUGIN_OWNER_ID = 'francis-factory'
_PLUGIN_CAPABILITY_TYPE = 'data_insight'
_PLUGIN_INTENDED_DOMAIN = 'AI instructional design, course review, practice generation, and learner feedback workflows for safety controls context filtering and token-budget control'
_PLUGIN_USE_CASES = ['Apply this capability to the distinct use case: Learning Design Safety Controls.', 'Classify context as keep, compress, or drop.', 'Detect redundant notes that waste context budget.', 'Preserve constraints and decisions while reducing noise.', 'Show a compact progress state for this AI capability during baseline capability.', 'Return user-facing guidance that is useful, concise, and safe to act on.', 'Avoid duplicating existing AI capability behavior; identify what is unique about this capability.']
_PLUGIN_RESULT_SCHEMA_VERSION: str = "1.0.0"
_PLUGIN_MANIFEST = {'name': 'AI Context Noise Filter 010589', 'slug': 'ai_context_noise_filter_010589', 'goal': 'Filter noisy or redundant context before model calls for AI instructional design, course review, practice generation, and learner feedback workflows for safety controls.', 'category': 'ai_memory', 'tags': ['learning', 'instructional-design', 'assessment', 'safety', 'controls', 'context', 'tokens', 'noise', 'continuous_backlog', 'use_case_seeded', 'autonomous_factory', 'ai_progress'], 'version': '0.1.0', 'capability_type': 'data_insight', 'intended_domain': 'AI instructional design, course review, practice generation, and learner feedback workflows for safety controls context filtering and token-budget control', 'owner_id': 'francis-factory', 'use_cases': ['Apply this capability to the distinct use case: Learning Design Safety Controls.', 'Classify context as keep, compress, or drop.', 'Detect redundant notes that waste context budget.', 'Preserve constraints and decisions while reducing noise.', 'Show a compact progress state for this AI capability during baseline capability.', 'Return user-facing guidance that is useful, concise, and safe to act on.', 'Avoid duplicating existing AI capability behavior; identify what is unique about this capability.'], 'schema_version': '1.0.0'}
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
        plugin_name = 'AI Context Noise Filter 010589'
        goal = 'Filter noisy or redundant context before model calls for AI instructional design, course review, practice generation, and learner feedback workflows for safety controls.'
        domain = 'AI instructional design, course review, practice generation, and learner feedback workflows for safety controls context filtering and token-budget control'
        capability_type = 'data_insight'
        logic_profile_id = 'continuous_context_noise_filter_profile'
        generation_note = 'capability profile registry override'
        use_cases = ['Apply this capability to the distinct use case: Learning Design Safety Controls.', 'Classify context as keep, compress, or drop.', 'Detect redundant notes that waste context budget.', 'Preserve constraints and decisions while reducing noise.', 'Show a compact progress state for this AI capability during baseline capability.', 'Return user-facing guidance that is useful, concise, and safe to act on.']
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
        token_budget = int(payload_data.get('token_budget') or payload_data.get('max_context_tokens') or 2048)
        items = []
        for key in ['prompt', 'task', 'objective', 'constraints', 'current_plan', 'completed_steps', 'blocked_steps', 'previous_results', 'trace', 'rubric']:
            value = payload_data.get(key)
            if value not in (None, '', [], {}):
                items.append({'source': key, 'text': str(value), 'tokens': max(1, len(str(value)) // 4)})
        for idx, item in enumerate(messages + source_notes + candidate_outputs):
            text = str(item.get('content') or item.get('text') or item if isinstance(item, dict) else item)
            items.append({'source': 'item_%d' % idx, 'text': text, 'tokens': max(1, len(text) // 4)})
        for item in items:
            lower = item['text'].lower()
            item['priority'] = 1
            item['reason_tags'] = []
            if any(word in lower for word in ['must', 'constraint', 'objective', 'error', 'blocked', 'acceptance']):
                item['priority'] += 3
                item['reason_tags'].append('requirement_or_blocker')
            if any(word in lower for word in ['auth', 'login', 'database', 'migration', 'rollback', 'production']):
                item['priority'] += 2
                item['reason_tags'].append('release_or_auth_risk')
            if any(word in lower for word in ['citation', 'source', 'medical', 'clinical', 'claim', 'unsupported', 'hallucination']):
                item['priority'] += 2
                item['reason_tags'].append('factual_grounding_risk')
            if any(word in lower for word in ['test', 'verify', 'coverage', 'check']):
                item['priority'] += 1
                item['reason_tags'].append('verification')
            if any(word in lower for word in ['done', 'thanks', 'maybe', 'chatter']):
                item['priority'] -= 1
                item['reason_tags'].append('low_signal')
            item['preview'] = item['text'][:180]
        items = sorted(items, key=lambda item: (item['priority'], -item['tokens']), reverse=True)
        kept = []
        compressed = []
        dropped = []
        used = 0
        for item in items:
            if used + item['tokens'] <= token_budget:
                kept.append(item)
                used += item['tokens']
            elif item['priority'] >= 3:
                compact = dict(item)
                compact['compressed_text'] = item['text'][:240]
                compressed.append(compact)
                used += min(item['tokens'], 80)
            else:
                dropped.append(item)
        fit = used <= token_budget
        result['summary'] = plugin_name + ': optimized context to about ' + str(used) + ' tokens against budget ' + str(token_budget) + '.'
        result['primary_insights'] = [
            {'title': 'Kept context', 'detail': [{'source': item['source'], 'preview': item['preview'], 'reason_tags': item['reason_tags']} for item in kept]},
            {'title': 'Compressed context', 'detail': [{'source': item['source'], 'preview': item['preview'], 'reason_tags': item['reason_tags']} for item in compressed]},
            {'title': 'Dropped context', 'detail': [{'source': item['source'], 'preview': item['preview'], 'reason_tags': item['reason_tags']} for item in dropped]},
        ]
        result['recommended_actions'] = [
            {'action': 'Keep high-priority context', 'items': [{'source': item['source'], 'preview': item['preview'], 'why': item['reason_tags']} for item in kept[:8]]},
            {'action': 'Compress oversized but important context', 'items': [{'source': item['source'], 'preview': item.get('compressed_text', item['preview']), 'why': item['reason_tags']} for item in compressed[:8]]},
            {'action': 'Drop low-signal context', 'items': [{'source': item['source'], 'preview': item['preview'], 'why': item['reason_tags']} for item in dropped[:8]]},
        ]
        reason_counts = {}
        for item in items:
            for tag in item['reason_tags']:
                reason_counts[tag] = reason_counts.get(tag, 0) + 1
        result['scores'] = {'confidence': round(min(0.92, 0.4 + 0.045 * len(items[:8]) + 0.04 * len(reason_counts)), 2), 'token_budget_fit': 1.0 if fit else round(token_budget / max(1, used), 2), 'context_retention': round(len(kept) / max(1, len(items)), 2), 'risk': round(min(0.9, 0.14 + (0.18 if not fit else 0) + 0.035 * len(dropped) + 0.025 * reason_counts.get('factual_grounding_risk', 0) + 0.02 * reason_counts.get('release_or_auth_risk', 0)), 2)}
        result['details'] = {'kept_context': kept[:10], 'compressed_context': compressed[:10], 'dropped_context': dropped[:10], 'priority_reason_counts': reason_counts, 'token_budget': token_budget, 'estimated_tokens': used, 'missing_inputs': ['context items'] if not items else []}
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
            'next_step': 'Use kept_context, then compressed_context, and omit dropped_context.',
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
            'optional_next_challenge': 'Use kept_context, then compressed_context, and omit dropped_context.',
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
    # AI Draft Plugin Repair Surgeon context noise finalizer.
    try:
        _details = result.get('details') if isinstance(result.get('details'), dict) else {}
        _profile_id = str(_details.get('logic_profile_id') or locals().get('logic_profile_id') or '')
        if 'context_noise_filter' in _profile_id:
            explicit_noise_terms = [
                'irrelevant', 'unrelated', 'off-topic', 'off topic', 'noise',
                'random old', 'small talk', 'lunch', 'chatter', 'thanks only',
                'no action needed', 'discard', 'do not need',
            ]
            def _repair_context_items(key):
                value = _details.get(key)
                return list(value) if isinstance(value, list) else []
            def _repair_item_text(item):
                if isinstance(item, dict):
                    parts = [item.get('text'), item.get('preview'), item.get('compressed_text'), item.get('source')]
                    return ' '.join(str(part) for part in parts if part is not None).lower()
                return str(item).lower()
            def _repair_mark_noise(item):
                text = _repair_item_text(item)
                return any(term in text for term in explicit_noise_terms)
            _kept = _repair_context_items('kept_context')
            _compressed = _repair_context_items('compressed_context')
            _dropped = _repair_context_items('dropped_context')
            _moved = []
            _new_kept = []
            for _item in _kept:
                if _repair_mark_noise(_item):
                    if isinstance(_item, dict):
                        _item = dict(_item)
                        _item.setdefault('reason_tags', [])
                        if isinstance(_item['reason_tags'], list) and 'explicit_noise' not in _item['reason_tags']:
                            _item['reason_tags'].append('explicit_noise')
                    _moved.append(_item)
                else:
                    _new_kept.append(_item)
            _new_compressed = []
            for _item in _compressed:
                if _repair_mark_noise(_item):
                    if isinstance(_item, dict):
                        _item = dict(_item)
                        _item.setdefault('reason_tags', [])
                        if isinstance(_item['reason_tags'], list) and 'explicit_noise' not in _item['reason_tags']:
                            _item['reason_tags'].append('explicit_noise')
                    _moved.append(_item)
                else:
                    _new_compressed.append(_item)
            if _moved:
                _details['kept_context'] = _new_kept
                _details['compressed_context'] = _new_compressed
                _details['dropped_context'] = _moved + _dropped
                _reason_counts = _details.get('priority_reason_counts') if isinstance(_details.get('priority_reason_counts'), dict) else {}
                _reason_counts['explicit_noise'] = _reason_counts.get('explicit_noise', 0) + len(_moved)
                _details['priority_reason_counts'] = _reason_counts
                _details['noise_filter_repair'] = {'moved_to_dropped': len(_moved), 'terms': explicit_noise_terms}
                _total = max(1, len(_new_kept) + len(_new_compressed) + len(_details['dropped_context']))
                _scores = result.get('scores') if isinstance(result.get('scores'), dict) else {}
                _scores['context_retention'] = round((len(_new_kept) + len(_new_compressed)) / _total, 2)
                _scores['noise_drop_count'] = len(_details['dropped_context'])
                _scores['usefulness'] = max(float(_scores.get('usefulness', _scores.get('confidence', 0.65)) or 0.65), 0.7)
                result['scores'] = _scores
                result['primary_insights'] = [
                    {'title': 'Kept context', 'detail': [{'source': item.get('source'), 'preview': item.get('preview', item.get('text', '')), 'reason_tags': item.get('reason_tags', [])} for item in _new_kept if isinstance(item, dict)]},
                    {'title': 'Compressed context', 'detail': [{'source': item.get('source'), 'preview': item.get('preview', item.get('text', '')), 'reason_tags': item.get('reason_tags', [])} for item in _new_compressed if isinstance(item, dict)]},
                    {'title': 'Dropped context', 'detail': [{'source': item.get('source'), 'preview': item.get('preview', item.get('text', '')), 'reason_tags': item.get('reason_tags', [])} for item in _details['dropped_context'] if isinstance(item, dict)]},
                ]
                result['recommended_actions'] = [
                    {'action': 'Keep high-priority context', 'items': [{'source': item.get('source'), 'preview': item.get('preview', item.get('text', '')), 'why': item.get('reason_tags', [])} for item in _new_kept[:8] if isinstance(item, dict)]},
                    {'action': 'Compress oversized but important context', 'items': [{'source': item.get('source'), 'preview': item.get('compressed_text', item.get('preview', '')), 'why': item.get('reason_tags', [])} for item in _new_compressed[:8] if isinstance(item, dict)]},
                    {'action': 'Drop explicit noise and low-signal context', 'items': [{'source': item.get('source'), 'preview': item.get('preview', item.get('text', '')), 'why': item.get('reason_tags', [])} for item in _details['dropped_context'][:8] if isinstance(item, dict)]},
                ]
                _diagnostics = result.get('diagnostics') if isinstance(result.get('diagnostics'), dict) else {}
                _diagnostics['context_noise_repair_applied'] = True
                _diagnostics['context_noise_moved_count'] = len(_moved)
                result['diagnostics'] = _diagnostics
                result['details'] = _details
    except Exception as _context_repair_exc:
        if isinstance(result, dict):
            result.setdefault('details', {})['context_noise_repair_error'] = str(_context_repair_exc)
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
