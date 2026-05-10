from __future__ import annotations

"""
Auto-generated Francis AI capability module.

THIS FILE IS GENERATED. Manual edits may be overwritten by the factory.

Capability: AI Context Window Optimizer 000005
Slug: ai_context_window_optimizer
"""

from typing import Any, Dict, Optional

__all__ = ["invoke", "_run_core_logic", "SkillContext"]

_PLUGIN_NAME: str = 'AI Context Window Optimizer 000005'
_PLUGIN_SLUG: str = 'ai_context_window_optimizer'
_PLUGIN_CATEGORY: str = 'ai_memory'
_PLUGIN_VERSION: str = '0.1.0'
_PLUGIN_GOAL: str = 'Prioritize which context should be kept, compressed, or dropped before an AI model call.'
_PLUGIN_TAGS = ['ai', 'context', 'tokens', 'optimization', 'autonomous_factory', 'ai_progress']
_PLUGIN_OWNER_ID = 'francis-factory'
_PLUGIN_CAPABILITY_TYPE = 'data_insight'
_PLUGIN_INTENDED_DOMAIN = 'AI context packing and token budget management'
_PLUGIN_USE_CASES = ['Rank context snippets by relevance to the current task.', 'Detect redundant or stale context.', 'Suggest compact replacements for large repeated sections.', 'Show a compact progress state for this AI capability during baseline capability.', 'Return user-facing guidance that is useful, concise, and safe to act on.', 'Avoid duplicating existing AI capability behavior; identify what is unique about this capability.']
_PLUGIN_RESULT_SCHEMA_VERSION: str = "1.0.0"
_PLUGIN_MANIFEST = {'name': 'AI Context Window Optimizer 000005', 'slug': 'ai_context_window_optimizer', 'goal': 'Prioritize which context should be kept, compressed, or dropped before an AI model call.', 'category': 'ai_memory', 'tags': ['ai', 'context', 'tokens', 'optimization', 'autonomous_factory', 'ai_progress'], 'version': '0.1.0', 'capability_type': 'data_insight', 'intended_domain': 'AI context packing and token budget management', 'owner_id': 'francis-factory', 'use_cases': ['Rank context snippets by relevance to the current task.', 'Detect redundant or stale context.', 'Suggest compact replacements for large repeated sections.', 'Show a compact progress state for this AI capability during baseline capability.', 'Return user-facing guidance that is useful, concise, and safe to act on.', 'Avoid duplicating existing AI capability behavior; identify what is unique about this capability.'], 'schema_version': '1.0.0'}
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
        plugin_name = 'AI Context Window Optimizer 000005'
        goal = 'Prioritize which context should be kept, compressed, or dropped before an AI model call.'
        domain = 'AI context packing and token budget management'
        capability_type = 'data_insight'
        logic_profile_id = 'context_window_optimizer_profile'
        generation_note = 'capability profile registry override'
        use_cases = ['Rank context snippets by relevance to the current task.', 'Detect redundant or stale context.', 'Suggest compact replacements for large repeated sections.', 'Show a compact progress state for this AI capability during baseline capability.', 'Return user-facing guidance that is useful, concise, and safe to act on.', 'Avoid duplicating existing AI capability behavior; identify what is unique about this capability.']
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
        result['details']['use_cases'] = use_cases
        result['details']['generation_note'] = generation_note
        result['details']['capability_type'] = capability_type
        result['details']['logic_profile_id'] = logic_profile_id
        result['details']['payload_warnings'] = payload_warnings
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
