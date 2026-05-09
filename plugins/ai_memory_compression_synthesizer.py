from __future__ import annotations

"""
Auto-generated Francis plugin module.

THIS FILE IS GENERATED. Manual edits may be overwritten by the factory.

Plugin: AI Memory Compression Synthesizer
Slug: ai_memory_compression_synthesizer
"""

from typing import Any, Dict, Optional

__all__ = ["invoke", "_run_core_logic", "SkillContext"]

# ---------------------------------------------------------------------------
# Plugin metadata (used by Station C, registry, and tooling)
# ---------------------------------------------------------------------------

_PLUGIN_NAME: str = 'AI Memory Compression Synthesizer'
_PLUGIN_SLUG: str = 'ai_memory_compression_synthesizer'
_PLUGIN_CATEGORY: str = 'ai_memory'
_PLUGIN_VERSION: str = '0.1.0'
_PLUGIN_GOAL: str = 'Compress conversation or project history into durable memory notes without losing decisions.'
_PLUGIN_TAGS = ['ai', 'memory', 'context', 'summarization', 'autonomous_factory', 'ai_progress', 'phase_1']
_PLUGIN_OWNER_ID = 'francis-factory'
_PLUGIN_CAPABILITY_TYPE = 'research_synthesizer'
_PLUGIN_INTENDED_DOMAIN = 'AI memory, context management, and long-running work'
_PLUGIN_USE_CASES = ['Summarize long work sessions into concise durable memory.', 'Extract stable preferences, constraints, and project facts.', 'Separate decisions from transient discussion.', 'Show a compact progress state for this AI capability during baseline capability.', 'Return user-facing guidance that is useful, concise, and safe to act on.', 'Avoid duplicating existing AI plugin behavior; identify what is unique about this capability.']
_PLUGIN_RESULT_SCHEMA_VERSION: str = '1.0.0'

# Lightweight manifest for discovery/registry.
_PLUGIN_MANIFEST = {'name': 'AI Memory Compression Synthesizer', 'slug': 'ai_memory_compression_synthesizer', 'goal': 'Compress conversation or project history into durable memory notes without losing decisions.', 'category': 'ai_memory', 'tags': ['ai', 'memory', 'context', 'summarization', 'autonomous_factory', 'ai_progress', 'phase_1'], 'version': '0.1.0', 'capability_type': 'research_synthesizer', 'intended_domain': 'AI memory, context management, and long-running work', 'owner_id': 'francis-factory', 'use_cases': ['Summarize long work sessions into concise durable memory.', 'Extract stable preferences, constraints, and project facts.', 'Separate decisions from transient discussion.', 'Show a compact progress state for this AI capability during baseline capability.', 'Return user-facing guidance that is useful, concise, and safe to act on.', 'Avoid duplicating existing AI plugin behavior; identify what is unique about this capability.'], 'primary_use_case': 'Summarize long work sessions into concise durable memory.', 'problem_statement': 'Francis needs a focused AI plugin for AI memory, context management, and long-running work. The plugin must turn messy user notes, model outputs, traces, or workflow state into structured, actionable AI assistance. It should improve autonomous progress by making the next step obvious, reducing duplicated work, and exposing risks before they become failures. The plugin must stay deterministic, avoid hidden external side effects, and make its reasoning inspectable through concise details and scores.', 'primary_inputs': 'A payload dict that may contain task, objective, prompt, conversation, artifacts, candidate_outputs, traces, rubric, constraints, user_level, current_plan, completed_steps, blocked_steps, source_notes, and optional customer_config.', 'primary_outputs': 'A normalized result dict with summary, primary_insights, recommended_actions, scores, details, progress_state, user_experience, fun_mode, and machine-readable diagnostics.', 'constraints': 'Do not execute tools, browse, mutate files, call external APIs, or claim facts not present in the payload. Prefer deterministic analysis. If data is missing, say what is missing and return a useful fallback. Keep recommendations concrete. Avoid creating a capability that duplicates another AI roadmap plugin.', 'example_use_cases': ['A user asks Francis to improve an AI workflow related to AI memory, context management, and long-running work.', 'A long-running autonomous run needs a checkpoint summary and the next best action.', 'An operator wants a scorecard that separates hard failures from polish improvements.', 'A beginner wants the result explained in plain language without losing technical accuracy.', 'A power user wants structured JSON they can pipe into another agent or dashboard.'], 'io_contract': "Input: payload is a dict. Important optional keys include 'task', 'objective', 'prompt', 'conversation', 'messages', 'candidate_outputs', 'trace', 'rubric', 'constraints', 'progress', 'current_plan', 'completed_steps', 'blocked_steps', 'user_level', and 'customer_config'. Output: return a dict containing summary: str, primary_insights: list, recommended_actions: list, scores: dict with confidence and usefulness, details: dict, progress_state: dict with current_stage/next_step/blockers, user_experience: dict with plain_language_takeaway and interaction_suggestions, and fun_mode: dict with optional challenge_label, score_badge, and celebratory_microcopy. Fun fields must never replace the serious recommendation.", 'schema_version': '1.0.0', 'family_key': 'ai_memory::ai memory compression synthesizer', 'is_generic_name': False}

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
    # Auto-generated capability-profile core logic envelope. Edits may be overwritten by the factory.
    import base64
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
    _profile_body_b64 = 'cGx1Z2luX25hbWUgPSAnQUkgTWVtb3J5IENvbXByZXNzaW9uIFN5bnRoZXNpemVyJwpnb2FsID0gJ0NvbXByZXNzIGNvbnZlcnNhdGlvbiBvciBwcm9qZWN0IGhpc3RvcnkgaW50byBkdXJhYmxlIG1lbW9yeSBub3RlcyB3aXRob3V0IGxvc2luZyBkZWNpc2lvbnMuJwpkb21haW4gPSAnQUkgbWVtb3J5LCBjb250ZXh0IG1hbmFnZW1lbnQsIGFuZCBsb25nLXJ1bm5pbmcgd29yaycKY2FwYWJpbGl0eV90eXBlID0gJ3Jlc2VhcmNoX3N5bnRoZXNpemVyJwpsb2dpY19wcm9maWxlX2lkID0gJ21lbW9yeV9jb21wcmVzc2lvbl9wcm9maWxlJwpnZW5lcmF0aW9uX25vdGUgPSAnY2FwYWJpbGl0eS1zcGVjaWZpYyBwcm9maWxlIHJlcGxhY2VtZW50IGZvciBnZW5lcmljIHNlbWFudGljIHJlcGFpcicKdXNlX2Nhc2VzID0gWydTdW1tYXJpemUgbG9uZyB3b3JrIHNlc3Npb25zIGludG8gY29uY2lzZSBkdXJhYmxlIG1lbW9yeS4nLCAnRXh0cmFjdCBzdGFibGUgcHJlZmVyZW5jZXMsIGNvbnN0cmFpbnRzLCBhbmQgcHJvamVjdCBmYWN0cy4nLCAnU2VwYXJhdGUgZGVjaXNpb25zIGZyb20gdHJhbnNpZW50IGRpc2N1c3Npb24uJywgJ1Nob3cgYSBjb21wYWN0IHByb2dyZXNzIHN0YXRlIGZvciB0aGlzIEFJIGNhcGFiaWxpdHkgZHVyaW5nIGJhc2VsaW5lIGNhcGFiaWxpdHkuJywgJ1JldHVybiB1c2VyLWZhY2luZyBndWlkYW5jZSB0aGF0IGlzIHVzZWZ1bCwgY29uY2lzZSwgYW5kIHNhZmUgdG8gYWN0IG9uLicsICdBdm9pZCBkdXBsaWNhdGluZyBleGlzdGluZyBBSSBwbHVnaW4gYmVoYXZpb3I7IGlkZW50aWZ5IHdoYXQgaXMgdW5pcXVlIGFib3V0IHRoaXMgY2FwYWJpbGl0eS4nXQpwYXlsb2FkX2RhdGEgPSBwYXlsb2FkIGlmIGlzaW5zdGFuY2UocGF5bG9hZCwgZGljdCkgZWxzZSB7fQpwYXlsb2FkX3dhcm5pbmdzID0gW10gaWYgaXNpbnN0YW5jZShwYXlsb2FkLCBkaWN0KSBlbHNlIFsncGF5bG9hZCB3YXMgbm90IGEgZGljdDsgdXNpbmcgZW1wdHkgcGF5bG9hZCddCmRlZl90ZXh0ID0gc3RyKHBheWxvYWRfZGF0YS5nZXQoJ3Rhc2snKSBvciBwYXlsb2FkX2RhdGEuZ2V0KCdvYmplY3RpdmUnKSBvciBwYXlsb2FkX2RhdGEuZ2V0KCdwcm9tcHQnKSBvciBnb2FsKS5zdHJpcCgpCm9iamVjdGl2ZV90ZXh0ID0gc3RyKHBheWxvYWRfZGF0YS5nZXQoJ29iamVjdGl2ZScpIG9yIGdvYWwpLnN0cmlwKCkKY29uc3RyYWludHMgPSBwYXlsb2FkX2RhdGEuZ2V0KCdjb25zdHJhaW50cycpIGlmIGlzaW5zdGFuY2UocGF5bG9hZF9kYXRhLmdldCgnY29uc3RyYWludHMnKSwgbGlzdCkgZWxzZSBbXQptZXNzYWdlcyA9IHBheWxvYWRfZGF0YS5nZXQoJ21lc3NhZ2VzJykgaWYgaXNpbnN0YW5jZShwYXlsb2FkX2RhdGEuZ2V0KCdtZXNzYWdlcycpLCBsaXN0KSBlbHNlIFtdCmNhbmRpZGF0ZV9vdXRwdXRzID0gcGF5bG9hZF9kYXRhLmdldCgnY2FuZGlkYXRlX291dHB1dHMnKSBpZiBpc2luc3RhbmNlKHBheWxvYWRfZGF0YS5nZXQoJ2NhbmRpZGF0ZV9vdXRwdXRzJyksIGxpc3QpIGVsc2UgW10Kc291cmNlX25vdGVzID0gcGF5bG9hZF9kYXRhLmdldCgnc291cmNlX25vdGVzJykgaWYgaXNpbnN0YW5jZShwYXlsb2FkX2RhdGEuZ2V0KCdzb3VyY2Vfbm90ZXMnKSwgbGlzdCkgZWxzZSBbXQpyYXdfaXRlbXMgPSBbXQpmb3IgaXRlbSBpbiBtZXNzYWdlcyArIHNvdXJjZV9ub3RlcyArIGNhbmRpZGF0ZV9vdXRwdXRzOgogICAgaWYgaXNpbnN0YW5jZShpdGVtLCBkaWN0KToKICAgICAgICByYXdfaXRlbXMuYXBwZW5kKHN0cihpdGVtLmdldCgnY29udGVudCcpIG9yIGl0ZW0uZ2V0KCd0ZXh0Jykgb3IgaXRlbS5nZXQoJ3N1bW1hcnknKSBvciBpdGVtKVs6NTAwXSkKICAgIGVsc2U6CiAgICAgICAgcmF3X2l0ZW1zLmFwcGVuZChzdHIoaXRlbSlbOjUwMF0pCmlmIHBheWxvYWRfZGF0YS5nZXQoJ3ByZXZpb3VzX3Jlc3VsdHMnKToKICAgIHJhd19pdGVtcy5hcHBlbmQoc3RyKHBheWxvYWRfZGF0YS5nZXQoJ3ByZXZpb3VzX3Jlc3VsdHMnKSlbOjcwMF0pCmpvaW5lZCA9ICcgJy5qb2luKHJhd19pdGVtcykuc3RyaXAoKQpzZW50ZW5jZXMgPSBbcGFydC5zdHJpcCgpIGZvciBwYXJ0IGluIGpvaW5lZC5yZXBsYWNlKCdcbicsICcuICcpLnNwbGl0KCcuJykgaWYgcGFydC5zdHJpcCgpXQpkdXJhYmxlX2ZhY3RzID0gW3NlbnRlbmNlIGZvciBzZW50ZW5jZSBpbiBzZW50ZW5jZXMgaWYgYW55KHRva2VuIGluIHNlbnRlbmNlLmxvd2VyKCkgZm9yIHRva2VuIGluIFsnZGVjaWRlZCcsICdjb21wbGV0ZWQnLCAndXNlcycsICdtdXN0JywgJ2NvbnN0cmFpbnQnLCAnYmxvY2tlZCcsICdvd25lcicsICdwYXRoJ10pXQpvcGVuX3RocmVhZHMgPSBbc2VudGVuY2UgZm9yIHNlbnRlbmNlIGluIHNlbnRlbmNlcyBpZiBhbnkodG9rZW4gaW4gc2VudGVuY2UubG93ZXIoKSBmb3IgdG9rZW4gaW4gWyd0b2RvJywgJ25leHQnLCAnYmxvY2tlZCcsICd1bmtub3duJywgJ3F1ZXN0aW9uJywgJ25lZWRzJ10pXQpkaXNjYXJkX2NhbmRpZGF0ZXMgPSBbc2VudGVuY2UgZm9yIHNlbnRlbmNlIGluIHNlbnRlbmNlcyBpZiBsZW4oc2VudGVuY2Uuc3BsaXQoKSkgPCA0IG9yIHNlbnRlbmNlLmxvd2VyKCkgaW4gWydvaycsICd0aGFua3MnLCAnZG9uZSddXQptZW1vcnlfc3VtbWFyeSA9ICc7ICcuam9pbigoZHVyYWJsZV9mYWN0cyBvciBzZW50ZW5jZXMgb3IgW2RlZl90ZXh0XSlbOjRdKVs6NzAwXQpvcmlnaW5hbF90b2tlbnMgPSBtYXgoMSwgbGVuKGpvaW5lZCkgLy8gNCkKY29tcHJlc3NlZF90b2tlbnMgPSBtYXgoMSwgbGVuKG1lbW9yeV9zdW1tYXJ5KSAvLyA0KQpjb21wcmVzc2lvbl9yYXRpbyA9IHJvdW5kKGNvbXByZXNzZWRfdG9rZW5zIC8gb3JpZ2luYWxfdG9rZW5zLCAyKQpjb25maWRlbmNlID0gbWluKDAuOTIsIDAuNDIgKyAwLjA4ICogbGVuKGR1cmFibGVfZmFjdHNbOjVdKSArIDAuMDUgKiBsZW4ob3Blbl90aHJlYWRzWzozXSkpCnJlc3VsdFsnc3VtbWFyeSddID0gcGx1Z2luX25hbWUgKyAnOiBjb21wcmVzc2VkIGNvbnRleHQgaW50byBkdXJhYmxlIG1lbW9yeSB3aXRoIHJhdGlvICcgKyBzdHIoY29tcHJlc3Npb25fcmF0aW8pICsgJy4nCnJlc3VsdFsncHJpbWFyeV9pbnNpZ2h0cyddID0gWwogICAgeyd0aXRsZSc6ICdNZW1vcnkgc3VtbWFyeScsICdkZXRhaWwnOiBtZW1vcnlfc3VtbWFyeX0sCiAgICB7J3RpdGxlJzogJ0R1cmFibGUgZmFjdHMnLCAnZGV0YWlsJzogZHVyYWJsZV9mYWN0c1s6Nl19LAogICAgeyd0aXRsZSc6ICdPcGVuIHRocmVhZHMnLCAnZGV0YWlsJzogb3Blbl90aHJlYWRzWzo1XX0sCl0KcmVzdWx0WydyZWNvbW1lbmRlZF9hY3Rpb25zJ10gPSBbCiAgICB7J2FjdGlvbic6ICdQZXJzaXN0IG1lbW9yeSBzdW1tYXJ5JywgJ21lbW9yeV9zdW1tYXJ5JzogbWVtb3J5X3N1bW1hcnl9LAogICAgeydhY3Rpb24nOiAnQ2Fycnkgb3BlbiB0aHJlYWRzIGZvcndhcmQnLCAnb3Blbl90aHJlYWRzJzogb3Blbl90aHJlYWRzWzo1XX0sCiAgICB7J2FjdGlvbic6ICdEcm9wIGxvdy12YWx1ZSBjaGF0dGVyJywgJ2Rpc2NhcmRfY2FuZGlkYXRlcyc6IGRpc2NhcmRfY2FuZGlkYXRlc1s6NV19LApdCnJlc3VsdFsnc2NvcmVzJ10gPSB7J2NvbmZpZGVuY2UnOiByb3VuZChjb25maWRlbmNlLCAyKSwgJ2NvbXByZXNzaW9uX3JhdGlvJzogY29tcHJlc3Npb25fcmF0aW8sICdyZXRlbnRpb25fdmFsdWUnOiByb3VuZChtaW4oMC45NSwgMC40NSArIDAuMDggKiBsZW4oZHVyYWJsZV9mYWN0c1s6NV0pKSwgMiksICdyaXNrJzogcm91bmQobWF4KDAuMTIsIDAuNTUgLSBjb25maWRlbmNlKSwgMil9CnJlc3VsdFsnZGV0YWlscyddID0geydtZW1vcnlfc3VtbWFyeSc6IG1lbW9yeV9zdW1tYXJ5LCAnZHVyYWJsZV9mYWN0cyc6IGR1cmFibGVfZmFjdHNbOjEwXSwgJ29wZW5fdGhyZWFkcyc6IG9wZW5fdGhyZWFkc1s6MTBdLCAnZGlzY2FyZF9jYW5kaWRhdGVzJzogZGlzY2FyZF9jYW5kaWRhdGVzWzoxMF0sICdvcmlnaW5hbF90b2tlbl9lc3RpbWF0ZSc6IG9yaWdpbmFsX3Rva2VucywgJ2NvbXByZXNzZWRfdG9rZW5fZXN0aW1hdGUnOiBjb21wcmVzc2VkX3Rva2VucywgJ21pc3NpbmdfaW5wdXRzJzogWydtZXNzYWdlcyBvciBzb3VyY2Vfbm90ZXMnXSBpZiBub3QgcmF3X2l0ZW1zIGVsc2UgW119CnJlc3VsdFsnZGV0YWlscyddWyd1c2VfY2FzZXMnXSA9IHVzZV9jYXNlcwpyZXN1bHRbJ2RldGFpbHMnXVsnZ2VuZXJhdGlvbl9ub3RlJ10gPSBnZW5lcmF0aW9uX25vdGUKcmVzdWx0WydkZXRhaWxzJ11bJ2NhcGFiaWxpdHlfdHlwZSddID0gY2FwYWJpbGl0eV90eXBlCnJlc3VsdFsnZGV0YWlscyddWydsb2dpY19wcm9maWxlX2lkJ10gPSBsb2dpY19wcm9maWxlX2lkCnJlc3VsdFsnZGV0YWlscyddWydwYXlsb2FkX3dhcm5pbmdzJ10gPSBwYXlsb2FkX3dhcm5pbmdzCnJlc3VsdFsncHJvZ3Jlc3Nfc3RhdGUnXSA9IHsKICAgICdjdXJyZW50X3N0YWdlJzogbG9naWNfcHJvZmlsZV9pZCwKICAgICduZXh0X3N0ZXAnOiAnUGVyc2lzdCBtZW1vcnkgc3VtbWFyeScsCiAgICAnYmxvY2tlcnMnOiByZXN1bHRbJ2RldGFpbHMnXS5nZXQoJ21pc3NpbmdfaW5wdXRzJywgW10pWzo0XSwKICAgICdkb25lX3NpZ25hbHMnOiBbJ2NhcGFiaWxpdHlfc3BlY2lmaWNfYW5hbHlzaXNfY29tcGxldGUnLCBsb2dpY19wcm9maWxlX2lkXSwKfQpyZXN1bHRbJ3VzZXJfZXhwZXJpZW5jZSddID0gewogICAgJ3BsYWluX2xhbmd1YWdlX3Rha2Vhd2F5JzogcmVzdWx0WydzdW1tYXJ5J10sCiAgICAnYmVnaW5uZXJfdGlwJzogJ1VzZSB0aGUgZmlyc3QgcmVjb21tZW5kYXRpb24gYXMgdGhlIG5leHQgY29uY3JldGUgc3RlcC4nLAogICAgJ3Bvd2VyX3VzZXJfdGlwJzogJ1Bhc3MgZGV0YWlscyBhbmQgc2NvcmVzIGludG8gdGhlIG5leHQgQUkgY2FwYWJpbGl0eSBwbHVnaW4uJywKICAgICdpbnRlcmFjdGlvbl9zdWdnZXN0aW9ucyc6IFtpdGVtLmdldCgnYWN0aW9uJywgc3RyKGl0ZW0pKSBmb3IgaXRlbSBpbiByZXN1bHQuZ2V0KCdyZWNvbW1lbmRlZF9hY3Rpb25zJywgW10pWzozXV0sCn0KcmVzdWx0WydmdW5fbW9kZSddID0gewogICAgJ2NoYWxsZW5nZV9sYWJlbCc6ICdDYXBhYmlsaXR5IFJ1bicsCiAgICAnc2NvcmVfYmFkZ2UnOiAnU3Ryb25nIFNpZ25hbCcgaWYgcmVzdWx0LmdldCgnc2NvcmVzJywge30pLmdldCgnY29uZmlkZW5jZScsIDApID49IDAuNjUgZWxzZSAnTmVlZHMgQ29udGV4dCcsCiAgICAnbWljcm9jb3B5JzogJ1RoZSByZXN1bHQgaXMgc3RydWN0dXJlZCBzbyBhbm90aGVyIGFnZW50IGNhbiBwaWNrIGl0IHVwIGNsZWFubHkuJywKICAgICdvcHRpb25hbF9uZXh0X2NoYWxsZW5nZSc6ICdQZXJzaXN0IG1lbW9yeSBzdW1tYXJ5JywKfQ=='
    try:
        _profile_body_source = base64.b64decode(_profile_body_b64.encode('ascii')).decode('utf-8')
    except Exception:
        _profile_body_source = ''
    result = {
        'summary': '',
        'primary_insights': [],
        'recommended_actions': [],
        'scores': {'confidence': 0.0},
        'details': {},
    }
    schema = infer_tabular_schema(payload.get('data') if isinstance(payload, dict) else None)
    local_vars = {
        'context': context,
        'payload': payload,
        'config': config,
        'schema': schema,
        'pick_numeric_field': pick_numeric_field,
        'result': result,
    }
    if _profile_body_source.strip():
        try:
            exec(_profile_body_source, local_vars, local_vars)
            if isinstance(local_vars.get('result'), dict):
                result = local_vars['result']
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
