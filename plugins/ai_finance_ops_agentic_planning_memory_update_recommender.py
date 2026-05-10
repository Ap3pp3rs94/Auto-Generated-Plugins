from __future__ import annotations

"""
Auto-generated Francis plugin module.

THIS FILE IS GENERATED. Manual edits may be overwritten by the factory.

Plugin: AI Finance Ops Agentic Planning Memory Update Recommender 000606
Slug: ai_finance_ops_agentic_planning_memory_update_recommender
"""

from typing import Any, Dict, Optional

__all__ = ["invoke", "_run_core_logic", "SkillContext"]

# ---------------------------------------------------------------------------
# Plugin metadata (used by Station C, registry, and tooling)
# ---------------------------------------------------------------------------

_PLUGIN_NAME: str = 'AI Finance Ops Agentic Planning Memory Update Recommender 000606'
_PLUGIN_SLUG: str = 'ai_finance_ops_agentic_planning_memory_update_recommender'
_PLUGIN_CATEGORY: str = 'ai_memory'
_PLUGIN_VERSION: str = '0.1.0'
_PLUGIN_GOAL: str = 'Recommend durable memory updates from AI finance operations and risk review for agentic planning sessions without saving transient chatter.'
_PLUGIN_TAGS = ['finance', 'risk', 'agentic', 'planning', 'memory', 'facts', 'preferences', 'continuous_backlog', 'autonomous_factory', 'ai_progress']
_PLUGIN_OWNER_ID = 'francis-factory'
_PLUGIN_CAPABILITY_TYPE = 'research_synthesizer'
_PLUGIN_INTENDED_DOMAIN = 'AI finance operations and risk review for agentic planning durable memory and preference extraction'
_PLUGIN_USE_CASES = ['Extract durable decisions and preferences.', 'Separate temporary conversation from reusable memory.', 'Recommend add, update, merge, or ignore actions.', 'Show a compact progress state for this AI capability during baseline capability.', 'Return user-facing guidance that is useful, concise, and safe to act on.', 'Avoid duplicating existing AI capability behavior; identify what is unique about this capability.']
_PLUGIN_RESULT_SCHEMA_VERSION: str = '1.0.0'

# Lightweight manifest for discovery/registry.
_PLUGIN_MANIFEST = {'name': 'AI Finance Ops Agentic Planning Memory Update Recommender 000606', 'slug': 'ai_finance_ops_agentic_planning_memory_update_recommender', 'goal': 'Recommend durable memory updates from AI finance operations and risk review for agentic planning sessions without saving transient chatter.', 'category': 'ai_memory', 'tags': ['finance', 'risk', 'agentic', 'planning', 'memory', 'facts', 'preferences', 'continuous_backlog', 'autonomous_factory', 'ai_progress'], 'version': '0.1.0', 'capability_type': 'research_synthesizer', 'intended_domain': 'AI finance operations and risk review for agentic planning durable memory and preference extraction', 'owner_id': 'francis-factory', 'use_cases': ['Extract durable decisions and preferences.', 'Separate temporary conversation from reusable memory.', 'Recommend add, update, merge, or ignore actions.', 'Show a compact progress state for this AI capability during baseline capability.', 'Return user-facing guidance that is useful, concise, and safe to act on.', 'Avoid duplicating existing AI capability behavior; identify what is unique about this capability.'], 'primary_use_case': 'Extract durable decisions and preferences.', 'problem_statement': 'Francis needs a focused AI capability for AI finance operations and risk review for agentic planning durable memory and preference extraction. The generated module must turn messy user notes, model outputs, traces, or workflow state into structured, actionable AI assistance. It should improve autonomous progress by making the next step obvious, reducing duplicated work, and exposing risks before they become failures. The capability must stay deterministic, avoid hidden external side effects, and make its reasoning inspectable through concise details and scores.', 'primary_inputs': 'A payload dict that may contain task, objective, prompt, conversation, artifacts, candidate_outputs, traces, rubric, constraints, user_level, current_plan, completed_steps, blocked_steps, source_notes, and optional customer_config.', 'primary_outputs': 'A normalized result dict with summary, primary_insights, recommended_actions, scores, details, progress_state, user_experience, fun_mode, and machine-readable diagnostics.', 'constraints': 'Do not execute tools, browse, mutate files, call external APIs, or claim facts not present in the payload. Prefer deterministic analysis. If data is missing, say what is missing and return a useful fallback. Keep recommendations concrete. Avoid creating a capability that duplicates another AI roadmap capability.', 'example_use_cases': ['A user asks Francis to improve an AI workflow related to AI finance operations and risk review for agentic planning durable memory and preference extraction.', 'A long-running autonomous run needs a checkpoint summary and the next best action.', 'An operator wants a scorecard that separates hard failures from polish improvements.', 'A beginner wants the result explained in plain language without losing technical accuracy.', 'A power user wants structured JSON they can pipe into another agent or dashboard.'], 'io_contract': "Input: payload is a dict. Important optional keys include 'task', 'objective', 'prompt', 'conversation', 'messages', 'candidate_outputs', 'trace', 'rubric', 'constraints', 'progress', 'current_plan', 'completed_steps', 'blocked_steps', 'user_level', and 'customer_config'. Output: return a dict containing summary: str, primary_insights: list, recommended_actions: list, scores: dict with confidence and usefulness, details: dict, progress_state: dict with current_stage/next_step/blockers, user_experience: dict with plain_language_takeaway and interaction_suggestions, and fun_mode: dict with optional challenge_label, score_badge, and celebratory_microcopy. Fun fields must never replace the serious recommendation.", 'schema_version': '1.0.0', 'family_key': 'ai_memory::ai finance ops agentic planning memory update recommender', 'is_generic_name': False}

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
        plugin_name = 'AI Finance Ops Agentic Planning Memory Update Recommender 000606'
        goal = 'Recommend durable memory updates from AI finance operations and risk review for agentic planning sessions without saving transient chatter.'
        domain = 'AI finance operations and risk review for agentic planning durable memory and preference extraction'
        capability_type = 'research_synthesizer'
        logic_profile_id = 'continuous_memory_update_recommender_profile'
        generation_note = 'capability profile registry override'
        use_cases = ['Extract durable decisions and preferences.', 'Separate temporary conversation from reusable memory.', 'Recommend add, update, merge, or ignore actions.', 'Show a compact progress state for this AI capability during baseline capability.', 'Return user-facing guidance that is useful, concise, and safe to act on.', 'Avoid duplicating existing AI capability behavior; identify what is unique about this capability.']
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
        raw_items = []
        for key in ['task', 'objective', 'prompt']:
            value = payload_data.get(key)
            if value:
                raw_items.append(str(value)[:500])
        for key in ['constraints', 'current_plan', 'completed_steps', 'blocked_steps', 'trace']:
            value = payload_data.get(key)
            if isinstance(value, list):
                for item in value[:8]:
                    raw_items.append(str(item)[:500])
            elif value:
                raw_items.append(str(value)[:500])
        for item in messages + source_notes + candidate_outputs:
            if isinstance(item, dict):
                raw_items.append(str(item.get('content') or item.get('text') or item.get('summary') or item)[:500])
            else:
                raw_items.append(str(item)[:500])
        if payload_data.get('previous_results'):
            raw_items.append(str(payload_data.get('previous_results'))[:700])
        joined = '. '.join(raw_items).strip()
        sentences = [part.strip() for part in joined.replace('\n', '. ').split('.') if part.strip()]
        def _unique(items, limit):
            seen = set()
            kept = []
            for item in items:
                key = item.lower().strip()
                if not key or key in seen:
                    continue
                seen.add(key)
                kept.append(item)
                if len(kept) >= limit:
                    break
            return kept
        durable_facts = [sentence for sentence in sentences if any(token in sentence.lower() for token in ['decided', 'completed', 'uses', 'must', 'constraint', 'blocked', 'owner', 'path', 'objective', 'plan', 'test', 'rollback', 'citation', 'source'])]
        open_threads = [sentence for sentence in sentences if any(token in sentence.lower() for token in ['todo', 'next', 'blocked', 'unknown', 'question', 'needs', 'verify', 'mismatch', 'unsupported', 'uncertain'])]
        blockers = [sentence for sentence in sentences if any(token in sentence.lower() for token in ['blocked', 'need ', 'needs ', 'owner', 'mismatch', 'unsupported'])]
        evidence_gaps = [sentence for sentence in sentences if any(token in sentence.lower() for token in ['citation', 'source', 'claim', 'unsupported', 'clinical', 'medical', 'grounded'])]
        safety_signals = []
        for label, terms in [
            ('release_memory', ['production', 'outage', 'rollback', 'migration', 'database']),
            ('auth_memory', ['auth', 'login', 'session', 'middleware']),
            ('factual_memory', ['medical', 'clinical', 'citation', 'claim', 'source', 'hallucination']),
        ]:
            hits = [term for term in terms if term in joined.lower()]
            if hits:
                safety_signals.append({'category': label, 'signals': hits})
        durable_facts = _unique(durable_facts, 10)
        open_threads = _unique(open_threads, 10)
        blockers = _unique(blockers, 10)
        evidence_gaps = _unique(evidence_gaps, 10)
        discard_candidates = _unique([sentence for sentence in sentences if len(sentence.split()) < 4 or sentence.lower() in ['ok', 'thanks', 'done']], 10)
        memory_summary_parts = _unique(durable_facts[:4] + blockers[:2] + evidence_gaps[:2], 6) or _unique(sentences, 5) or [def_text]
        memory_summary = '; '.join(memory_summary_parts)[:900]
        original_tokens = max(1, len(joined) // 4)
        compressed_tokens = max(1, len(memory_summary) // 4)
        compression_ratio = round(min(1.0, compressed_tokens / original_tokens), 2)
        signal_count = sum(len(item['signals']) for item in safety_signals)
        retained_count = len(durable_facts[:8]) + len(blockers[:4]) + len(evidence_gaps[:4])
        confidence = min(0.92, 0.36 + 0.045 * retained_count + 0.035 * signal_count + (0.08 if memory_summary else 0))
        retention_value = round(min(0.95, 0.36 + 0.055 * len(durable_facts[:8]) + 0.05 * len(blockers[:4]) + 0.06 * len(evidence_gaps[:4])), 2)
        risk = round(min(0.9, max(0.1, 0.22 + 0.045 * len(blockers[:5]) + 0.055 * len(evidence_gaps[:5]) + 0.025 * signal_count - 0.035 * len(durable_facts[:5]))), 2)
        result['summary'] = plugin_name + ': compressed context into durable memory with ratio ' + str(compression_ratio) + '.'
        result['primary_insights'] = [
            {'title': 'Memory summary', 'detail': memory_summary},
            {'title': 'Durable facts', 'detail': durable_facts[:6]},
            {'title': 'Open threads', 'detail': open_threads[:5]},
            {'title': 'Safety signals', 'detail': safety_signals or 'No high-safety memory signal detected.'},
        ]
        result['recommended_actions'] = [
            {'action': 'Persist memory summary', 'memory_summary': memory_summary},
            {'action': 'Carry open threads forward', 'open_threads': open_threads[:5]},
            {'action': 'Preserve blocker/evidence context', 'blockers': blockers[:5], 'evidence_gaps': evidence_gaps[:5]},
            {'action': 'Drop low-value chatter', 'discard_candidates': discard_candidates[:5]},
        ]
        result['scores'] = {'confidence': round(confidence, 2), 'compression_ratio': compression_ratio, 'retention_value': retention_value, 'risk': risk, 'safety_signal_count': signal_count}
        result['details'] = {'memory_summary': memory_summary, 'durable_facts': durable_facts[:10], 'open_threads': open_threads[:10], 'blockers': blockers[:10], 'evidence_gaps': evidence_gaps[:10], 'safety_signals': safety_signals, 'discard_candidates': discard_candidates[:10], 'original_token_estimate': original_tokens, 'compressed_token_estimate': compressed_tokens, 'missing_inputs': ['messages or source_notes'] if not raw_items else []}
        result['details']['use_cases'] = use_cases
        result['details']['generation_note'] = generation_note
        result['details']['capability_type'] = capability_type
        result['details']['logic_profile_id'] = logic_profile_id
        result['details']['payload_warnings'] = payload_warnings
        result['progress_state'] = {
            'current_stage': logic_profile_id,
            'next_step': 'Persist memory summary',
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
            'optional_next_challenge': 'Persist memory summary',
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
