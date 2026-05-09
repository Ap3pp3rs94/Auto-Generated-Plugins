from __future__ import annotations

"""
Auto-generated Francis plugin module.

THIS FILE IS GENERATED. Manual edits may be overwritten by the factory.

Plugin: AI Retrieval Query Expander
Slug: ai_retrieval_query_expander
"""

from typing import Any, Dict, Optional

__all__ = ["invoke", "_run_core_logic", "SkillContext"]

# ---------------------------------------------------------------------------
# Plugin metadata (used by Station C, registry, and tooling)
# ---------------------------------------------------------------------------

_PLUGIN_NAME: str = 'AI Retrieval Query Expander'
_PLUGIN_SLUG: str = 'ai_retrieval_query_expander'
_PLUGIN_CATEGORY: str = 'ai_retrieval'
_PLUGIN_VERSION: str = '0.1.0'
_PLUGIN_GOAL: str = 'Generate targeted retrieval queries and filters for RAG-style knowledge lookup.'
_PLUGIN_TAGS = ['ai', 'retrieval', 'rag', 'search', 'autonomous_factory', 'ai_progress', 'phase_1']
_PLUGIN_OWNER_ID = 'francis-factory'
_PLUGIN_CAPABILITY_TYPE = 'research_synthesizer'
_PLUGIN_INTENDED_DOMAIN = 'AI retrieval, RAG, search planning, and knowledge grounding'
_PLUGIN_USE_CASES = ['Expand a user question into precise search queries.', 'Suggest metadata filters and source priorities.', 'Separate broad discovery queries from exact verification queries.', 'Show a compact progress state for this AI capability during baseline capability.', 'Return user-facing guidance that is useful, concise, and safe to act on.', 'Avoid duplicating existing AI plugin behavior; identify what is unique about this capability.']
_PLUGIN_RESULT_SCHEMA_VERSION: str = '1.0.0'

# Lightweight manifest for discovery/registry.
_PLUGIN_MANIFEST = {'name': 'AI Retrieval Query Expander', 'slug': 'ai_retrieval_query_expander', 'goal': 'Generate targeted retrieval queries and filters for RAG-style knowledge lookup.', 'category': 'ai_retrieval', 'tags': ['ai', 'retrieval', 'rag', 'search', 'autonomous_factory', 'ai_progress', 'phase_1'], 'version': '0.1.0', 'capability_type': 'research_synthesizer', 'intended_domain': 'AI retrieval, RAG, search planning, and knowledge grounding', 'owner_id': 'francis-factory', 'use_cases': ['Expand a user question into precise search queries.', 'Suggest metadata filters and source priorities.', 'Separate broad discovery queries from exact verification queries.', 'Show a compact progress state for this AI capability during baseline capability.', 'Return user-facing guidance that is useful, concise, and safe to act on.', 'Avoid duplicating existing AI plugin behavior; identify what is unique about this capability.'], 'primary_use_case': 'Expand a user question into precise search queries.', 'problem_statement': 'Francis needs a focused AI plugin for AI retrieval, RAG, search planning, and knowledge grounding. The plugin must turn messy user notes, model outputs, traces, or workflow state into structured, actionable AI assistance. It should improve autonomous progress by making the next step obvious, reducing duplicated work, and exposing risks before they become failures. The plugin must stay deterministic, avoid hidden external side effects, and make its reasoning inspectable through concise details and scores.', 'primary_inputs': 'A payload dict that may contain task, objective, prompt, conversation, artifacts, candidate_outputs, traces, rubric, constraints, user_level, current_plan, completed_steps, blocked_steps, source_notes, and optional customer_config.', 'primary_outputs': 'A normalized result dict with summary, primary_insights, recommended_actions, scores, details, progress_state, user_experience, fun_mode, and machine-readable diagnostics.', 'constraints': 'Do not execute tools, browse, mutate files, call external APIs, or claim facts not present in the payload. Prefer deterministic analysis. If data is missing, say what is missing and return a useful fallback. Keep recommendations concrete. Avoid creating a capability that duplicates another AI roadmap plugin.', 'example_use_cases': ['A user asks Francis to improve an AI workflow related to AI retrieval, RAG, search planning, and knowledge grounding.', 'A long-running autonomous run needs a checkpoint summary and the next best action.', 'An operator wants a scorecard that separates hard failures from polish improvements.', 'A beginner wants the result explained in plain language without losing technical accuracy.', 'A power user wants structured JSON they can pipe into another agent or dashboard.'], 'io_contract': "Input: payload is a dict. Important optional keys include 'task', 'objective', 'prompt', 'conversation', 'messages', 'candidate_outputs', 'trace', 'rubric', 'constraints', 'progress', 'current_plan', 'completed_steps', 'blocked_steps', 'user_level', and 'customer_config'. Output: return a dict containing summary: str, primary_insights: list, recommended_actions: list, scores: dict with confidence and usefulness, details: dict, progress_state: dict with current_stage/next_step/blockers, user_experience: dict with plain_language_takeaway and interaction_suggestions, and fun_mode: dict with optional challenge_label, score_badge, and celebratory_microcopy. Fun fields must never replace the serious recommendation.", 'schema_version': '1.0.0', 'family_key': 'ai_retrieval::ai retrieval query expander', 'is_generic_name': False}

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
    _profile_body_b64 = 'cGx1Z2luX25hbWUgPSAnQUkgUmV0cmlldmFsIFF1ZXJ5IEV4cGFuZGVyJwpnb2FsID0gJ0dlbmVyYXRlIHRhcmdldGVkIHJldHJpZXZhbCBxdWVyaWVzIGFuZCBmaWx0ZXJzIGZvciBSQUctc3R5bGUga25vd2xlZGdlIGxvb2t1cC4nCmRvbWFpbiA9ICdBSSByZXRyaWV2YWwsIFJBRywgc2VhcmNoIHBsYW5uaW5nLCBhbmQga25vd2xlZGdlIGdyb3VuZGluZycKY2FwYWJpbGl0eV90eXBlID0gJ3Jlc2VhcmNoX3N5bnRoZXNpemVyJwpsb2dpY19wcm9maWxlX2lkID0gJ3JldHJpZXZhbF9xdWVyeV9leHBhbmRlcl9wcm9maWxlJwpnZW5lcmF0aW9uX25vdGUgPSAnY2FwYWJpbGl0eS1zcGVjaWZpYyBwcm9maWxlIHJlcGxhY2VtZW50IGZvciBnZW5lcmljIHNlbWFudGljIHJlcGFpcicKdXNlX2Nhc2VzID0gWydFeHBhbmQgYSB1c2VyIHF1ZXN0aW9uIGludG8gcHJlY2lzZSBzZWFyY2ggcXVlcmllcy4nLCAnU3VnZ2VzdCBtZXRhZGF0YSBmaWx0ZXJzIGFuZCBzb3VyY2UgcHJpb3JpdGllcy4nLCAnU2VwYXJhdGUgYnJvYWQgZGlzY292ZXJ5IHF1ZXJpZXMgZnJvbSBleGFjdCB2ZXJpZmljYXRpb24gcXVlcmllcy4nLCAnU2hvdyBhIGNvbXBhY3QgcHJvZ3Jlc3Mgc3RhdGUgZm9yIHRoaXMgQUkgY2FwYWJpbGl0eSBkdXJpbmcgYmFzZWxpbmUgY2FwYWJpbGl0eS4nLCAnUmV0dXJuIHVzZXItZmFjaW5nIGd1aWRhbmNlIHRoYXQgaXMgdXNlZnVsLCBjb25jaXNlLCBhbmQgc2FmZSB0byBhY3Qgb24uJywgJ0F2b2lkIGR1cGxpY2F0aW5nIGV4aXN0aW5nIEFJIHBsdWdpbiBiZWhhdmlvcjsgaWRlbnRpZnkgd2hhdCBpcyB1bmlxdWUgYWJvdXQgdGhpcyBjYXBhYmlsaXR5LiddCnBheWxvYWRfZGF0YSA9IHBheWxvYWQgaWYgaXNpbnN0YW5jZShwYXlsb2FkLCBkaWN0KSBlbHNlIHt9CnBheWxvYWRfd2FybmluZ3MgPSBbXSBpZiBpc2luc3RhbmNlKHBheWxvYWQsIGRpY3QpIGVsc2UgWydwYXlsb2FkIHdhcyBub3QgYSBkaWN0OyB1c2luZyBlbXB0eSBwYXlsb2FkJ10KZGVmX3RleHQgPSBzdHIocGF5bG9hZF9kYXRhLmdldCgndGFzaycpIG9yIHBheWxvYWRfZGF0YS5nZXQoJ29iamVjdGl2ZScpIG9yIHBheWxvYWRfZGF0YS5nZXQoJ3Byb21wdCcpIG9yIGdvYWwpLnN0cmlwKCkKb2JqZWN0aXZlX3RleHQgPSBzdHIocGF5bG9hZF9kYXRhLmdldCgnb2JqZWN0aXZlJykgb3IgZ29hbCkuc3RyaXAoKQpjb25zdHJhaW50cyA9IHBheWxvYWRfZGF0YS5nZXQoJ2NvbnN0cmFpbnRzJykgaWYgaXNpbnN0YW5jZShwYXlsb2FkX2RhdGEuZ2V0KCdjb25zdHJhaW50cycpLCBsaXN0KSBlbHNlIFtdCm1lc3NhZ2VzID0gcGF5bG9hZF9kYXRhLmdldCgnbWVzc2FnZXMnKSBpZiBpc2luc3RhbmNlKHBheWxvYWRfZGF0YS5nZXQoJ21lc3NhZ2VzJyksIGxpc3QpIGVsc2UgW10KY2FuZGlkYXRlX291dHB1dHMgPSBwYXlsb2FkX2RhdGEuZ2V0KCdjYW5kaWRhdGVfb3V0cHV0cycpIGlmIGlzaW5zdGFuY2UocGF5bG9hZF9kYXRhLmdldCgnY2FuZGlkYXRlX291dHB1dHMnKSwgbGlzdCkgZWxzZSBbXQpzb3VyY2Vfbm90ZXMgPSBwYXlsb2FkX2RhdGEuZ2V0KCdzb3VyY2Vfbm90ZXMnKSBpZiBpc2luc3RhbmNlKHBheWxvYWRfZGF0YS5nZXQoJ3NvdXJjZV9ub3RlcycpLCBsaXN0KSBlbHNlIFtdCmJhc2UgPSAnICcuam9pbihbZGVmX3RleHQsIG9iamVjdGl2ZV90ZXh0XSkuc3RyaXAoKQpub2lzZSA9IFsncGxlYXNlJywgJ2hlbHAnLCAnbWFrZScsICdiZXR0ZXInLCAnc3R1ZmYnLCAndGhpbmdzJywgJ3ZlcnknXQp0b2tlbnMgPSBbd29yZC5zdHJpcCgnLiw6OyE/JykubG93ZXIoKSBmb3Igd29yZCBpbiBiYXNlLnNwbGl0KCldCmtleXdvcmRzID0gW10KZm9yIHRva2VuIGluIHRva2VuczoKICAgIGlmIGxlbih0b2tlbikgPiAzIGFuZCB0b2tlbiBub3QgaW4gbm9pc2UgYW5kIHRva2VuIG5vdCBpbiBrZXl3b3JkczoKICAgICAgICBrZXl3b3Jkcy5hcHBlbmQodG9rZW4pCmZhY2V0X3Rlcm1zID0gewogICAgJ2ltcGxlbWVudGF0aW9uJzogW3dvcmQgZm9yIHdvcmQgaW4ga2V5d29yZHMgaWYgd29yZCBpbiBbJ2NvZGUnLCAncHl0aG9uJywgJ2FwaScsICdwbHVnaW4nLCAndGVzdCcsICdlcnJvciddXSwKICAgICdldmFsdWF0aW9uJzogW3dvcmQgZm9yIHdvcmQgaW4ga2V5d29yZHMgaWYgd29yZCBpbiBbJ3F1YWxpdHknLCAncnVicmljJywgJ3Njb3JlJywgJ3ZlcmlmeScsICdjaXRhdGlvbiddXSwKICAgICdwbGFubmluZyc6IFt3b3JkIGZvciB3b3JkIGluIGtleXdvcmRzIGlmIHdvcmQgaW4gWydhZ2VudCcsICd3b3JrZmxvdycsICdoYW5kb2ZmJywgJ3Rhc2snLCAncGxhbiddXSwKfQpleHBhbmRlZF9xdWVyaWVzID0gW10KY29yZSA9ICcgJy5qb2luKGtleXdvcmRzWzo4XSkgb3IgYmFzZVs6MTIwXSBvciBnb2FsCmV4cGFuZGVkX3F1ZXJpZXMuYXBwZW5kKGNvcmUpCmV4cGFuZGVkX3F1ZXJpZXMuYXBwZW5kKGNvcmUgKyAnIGV4YW1wbGVzIGltcGxlbWVudGF0aW9uJykKZXhwYW5kZWRfcXVlcmllcy5hcHBlbmQoY29yZSArICcgYmVzdCBwcmFjdGljZXMgdmFsaWRhdGlvbicpCmlmIG9iamVjdGl2ZV90ZXh0OgogICAgZXhwYW5kZWRfcXVlcmllcy5hcHBlbmQoY29yZSArICcgJyArIG9iamVjdGl2ZV90ZXh0Wzo4MF0pCm5lZ2F0aXZlX3Rlcm1zID0gW3dvcmQgZm9yIHdvcmQgaW4gbm9pc2UgaWYgd29yZCBpbiB0b2tlbnNdCmdyb3VuZGluZ19wbGFuID0gWwogICAgJ1NlYXJjaCBicm9hZCBxdWVyeSBmaXJzdDogJyArIGV4cGFuZGVkX3F1ZXJpZXNbMF0sCiAgICAnVGhlbiBzZWFyY2ggaW1wbGVtZW50YXRpb24tc3BlY2lmaWMgcXVlcnkgaWYgY29kZSBvciBwbHVnaW4gc2lnbmFscyBhcHBlYXIuJywKICAgICdQcmVmZXIgcHJpbWFyeSBkb2N1bWVudGF0aW9uIG9yIGRpcmVjdCBzb3VyY2UgYXJ0aWZhY3RzIG92ZXIgc3VtbWFyaWVzLicsCl0KcmVzdWx0WydzdW1tYXJ5J10gPSBwbHVnaW5fbmFtZSArICc6IGV4cGFuZGVkIHJldHJpZXZhbCBpbnRvICcgKyBzdHIobGVuKGV4cGFuZGVkX3F1ZXJpZXMpKSArICcgZ3JvdW5kZWQgcXVlcmllcy4nCnJlc3VsdFsncHJpbWFyeV9pbnNpZ2h0cyddID0gWwogICAgeyd0aXRsZSc6ICdDb3JlIHF1ZXJ5JywgJ2RldGFpbCc6IGNvcmV9LAogICAgeyd0aXRsZSc6ICdGYWNldCB0ZXJtcycsICdkZXRhaWwnOiBmYWNldF90ZXJtc30sCiAgICB7J3RpdGxlJzogJ05vaXNlIHJlbW92ZWQnLCAnZGV0YWlsJzogbmVnYXRpdmVfdGVybXN9LApdCnJlc3VsdFsncmVjb21tZW5kZWRfYWN0aW9ucyddID0gWwogICAgeydhY3Rpb24nOiAnUnVuIHJldHJpZXZhbCBxdWVyeScsICdxdWVyeSc6IHF1ZXJ5fSBmb3IgcXVlcnkgaW4gZXhwYW5kZWRfcXVlcmllcwpdCnJlc3VsdFsnc2NvcmVzJ10gPSB7J2NvbmZpZGVuY2UnOiByb3VuZChtaW4oMC45LCAwLjQyICsgMC4wNSAqIGxlbihrZXl3b3JkcykpLCAyKSwgJ3F1ZXJ5X3NwZWNpZmljaXR5Jzogcm91bmQobWluKDAuOTUsIDAuMyArIDAuMDYgKiBsZW4oa2V5d29yZHMpKSwgMiksICdncm91bmRpbmdfdmFsdWUnOiByb3VuZCgwLjU4ICsgbWluKDAuMywgMC4wNiAqIGxlbihleHBhbmRlZF9xdWVyaWVzKSksIDIpLCAncmlzayc6IHJvdW5kKDAuMjIgKyAoMC4xMiBpZiBsZW4oa2V5d29yZHMpIDwgMyBlbHNlIDApLCAyKX0KcmVzdWx0WydkZXRhaWxzJ10gPSB7J2NvcmVfcXVlcnknOiBjb3JlLCAnZXhwYW5kZWRfcXVlcmllcyc6IGV4cGFuZGVkX3F1ZXJpZXMsICdmYWNldF90ZXJtcyc6IGZhY2V0X3Rlcm1zLCAnbmVnYXRpdmVfdGVybXMnOiBuZWdhdGl2ZV90ZXJtcywgJ2dyb3VuZGluZ19wbGFuJzogZ3JvdW5kaW5nX3BsYW4sICdtaXNzaW5nX2lucHV0cyc6IFsndGFzayBvciBvYmplY3RpdmUnXSBpZiBub3QgYmFzZSBlbHNlIFtdfQpyZXN1bHRbJ2RldGFpbHMnXVsndXNlX2Nhc2VzJ10gPSB1c2VfY2FzZXMKcmVzdWx0WydkZXRhaWxzJ11bJ2dlbmVyYXRpb25fbm90ZSddID0gZ2VuZXJhdGlvbl9ub3RlCnJlc3VsdFsnZGV0YWlscyddWydjYXBhYmlsaXR5X3R5cGUnXSA9IGNhcGFiaWxpdHlfdHlwZQpyZXN1bHRbJ2RldGFpbHMnXVsnbG9naWNfcHJvZmlsZV9pZCddID0gbG9naWNfcHJvZmlsZV9pZApyZXN1bHRbJ2RldGFpbHMnXVsncGF5bG9hZF93YXJuaW5ncyddID0gcGF5bG9hZF93YXJuaW5ncwpyZXN1bHRbJ3Byb2dyZXNzX3N0YXRlJ10gPSB7CiAgICAnY3VycmVudF9zdGFnZSc6IGxvZ2ljX3Byb2ZpbGVfaWQsCiAgICAnbmV4dF9zdGVwJzogJ1J1biByZXRyaWV2YWwgcXVlcnk6ICcgKyBleHBhbmRlZF9xdWVyaWVzWzBdLAogICAgJ2Jsb2NrZXJzJzogcmVzdWx0WydkZXRhaWxzJ10uZ2V0KCdtaXNzaW5nX2lucHV0cycsIFtdKVs6NF0sCiAgICAnZG9uZV9zaWduYWxzJzogWydjYXBhYmlsaXR5X3NwZWNpZmljX2FuYWx5c2lzX2NvbXBsZXRlJywgbG9naWNfcHJvZmlsZV9pZF0sCn0KcmVzdWx0Wyd1c2VyX2V4cGVyaWVuY2UnXSA9IHsKICAgICdwbGFpbl9sYW5ndWFnZV90YWtlYXdheSc6IHJlc3VsdFsnc3VtbWFyeSddLAogICAgJ2JlZ2lubmVyX3RpcCc6ICdVc2UgdGhlIGZpcnN0IHJlY29tbWVuZGF0aW9uIGFzIHRoZSBuZXh0IGNvbmNyZXRlIHN0ZXAuJywKICAgICdwb3dlcl91c2VyX3RpcCc6ICdQYXNzIGRldGFpbHMgYW5kIHNjb3JlcyBpbnRvIHRoZSBuZXh0IEFJIGNhcGFiaWxpdHkgcGx1Z2luLicsCiAgICAnaW50ZXJhY3Rpb25fc3VnZ2VzdGlvbnMnOiBbaXRlbS5nZXQoJ2FjdGlvbicsIHN0cihpdGVtKSkgZm9yIGl0ZW0gaW4gcmVzdWx0LmdldCgncmVjb21tZW5kZWRfYWN0aW9ucycsIFtdKVs6M11dLAp9CnJlc3VsdFsnZnVuX21vZGUnXSA9IHsKICAgICdjaGFsbGVuZ2VfbGFiZWwnOiAnQ2FwYWJpbGl0eSBSdW4nLAogICAgJ3Njb3JlX2JhZGdlJzogJ1N0cm9uZyBTaWduYWwnIGlmIHJlc3VsdC5nZXQoJ3Njb3JlcycsIHt9KS5nZXQoJ2NvbmZpZGVuY2UnLCAwKSA+PSAwLjY1IGVsc2UgJ05lZWRzIENvbnRleHQnLAogICAgJ21pY3JvY29weSc6ICdUaGUgcmVzdWx0IGlzIHN0cnVjdHVyZWQgc28gYW5vdGhlciBhZ2VudCBjYW4gcGljayBpdCB1cCBjbGVhbmx5LicsCiAgICAnb3B0aW9uYWxfbmV4dF9jaGFsbGVuZ2UnOiAnUnVuIHJldHJpZXZhbCBxdWVyeTogJyArIGV4cGFuZGVkX3F1ZXJpZXNbMF0sCn0='
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
