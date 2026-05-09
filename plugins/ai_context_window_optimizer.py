from __future__ import annotations

"""
Auto-generated Francis plugin module.

THIS FILE IS GENERATED. Manual edits may be overwritten by the factory.

Plugin: AI Context Window Optimizer
Slug: ai_context_window_optimizer
"""

from typing import Any, Dict, Optional

__all__ = ["invoke", "_run_core_logic", "SkillContext"]

# ---------------------------------------------------------------------------
# Plugin metadata (used by Station C, registry, and tooling)
# ---------------------------------------------------------------------------

_PLUGIN_NAME: str = 'AI Context Window Optimizer'
_PLUGIN_SLUG: str = 'ai_context_window_optimizer'
_PLUGIN_CATEGORY: str = 'ai_memory'
_PLUGIN_VERSION: str = '0.1.0'
_PLUGIN_GOAL: str = 'Prioritize which context should be kept, compressed, or dropped before an AI model call.'
_PLUGIN_TAGS = ['ai', 'context', 'tokens', 'optimization', 'autonomous_factory', 'ai_progress', 'phase_1']
_PLUGIN_OWNER_ID = 'francis-factory'
_PLUGIN_CAPABILITY_TYPE = 'data_insight'
_PLUGIN_INTENDED_DOMAIN = 'AI context packing and token budget management'
_PLUGIN_USE_CASES = ['Rank context snippets by relevance to the current task.', 'Detect redundant or stale context.', 'Suggest compact replacements for large repeated sections.', 'Show a compact progress state for this AI capability during baseline capability.', 'Return user-facing guidance that is useful, concise, and safe to act on.', 'Avoid duplicating existing AI plugin behavior; identify what is unique about this capability.']
_PLUGIN_RESULT_SCHEMA_VERSION: str = '1.0.0'

# Lightweight manifest for discovery/registry.
_PLUGIN_MANIFEST = {'name': 'AI Context Window Optimizer', 'slug': 'ai_context_window_optimizer', 'goal': 'Prioritize which context should be kept, compressed, or dropped before an AI model call.', 'category': 'ai_memory', 'tags': ['ai', 'context', 'tokens', 'optimization', 'autonomous_factory', 'ai_progress', 'phase_1'], 'version': '0.1.0', 'capability_type': 'data_insight', 'intended_domain': 'AI context packing and token budget management', 'owner_id': 'francis-factory', 'use_cases': ['Rank context snippets by relevance to the current task.', 'Detect redundant or stale context.', 'Suggest compact replacements for large repeated sections.', 'Show a compact progress state for this AI capability during baseline capability.', 'Return user-facing guidance that is useful, concise, and safe to act on.', 'Avoid duplicating existing AI plugin behavior; identify what is unique about this capability.'], 'primary_use_case': 'Rank context snippets by relevance to the current task.', 'problem_statement': 'Francis needs a focused AI plugin for AI context packing and token budget management. The plugin must turn messy user notes, model outputs, traces, or workflow state into structured, actionable AI assistance. It should improve autonomous progress by making the next step obvious, reducing duplicated work, and exposing risks before they become failures. The plugin must stay deterministic, avoid hidden external side effects, and make its reasoning inspectable through concise details and scores.', 'primary_inputs': 'A payload dict that may contain task, objective, prompt, conversation, artifacts, candidate_outputs, traces, rubric, constraints, user_level, current_plan, completed_steps, blocked_steps, source_notes, and optional customer_config.', 'primary_outputs': 'A normalized result dict with summary, primary_insights, recommended_actions, scores, details, progress_state, user_experience, fun_mode, and machine-readable diagnostics.', 'constraints': 'Do not execute tools, browse, mutate files, call external APIs, or claim facts not present in the payload. Prefer deterministic analysis. If data is missing, say what is missing and return a useful fallback. Keep recommendations concrete. Avoid creating a capability that duplicates another AI roadmap plugin.', 'example_use_cases': ['A user asks Francis to improve an AI workflow related to AI context packing and token budget management.', 'A long-running autonomous run needs a checkpoint summary and the next best action.', 'An operator wants a scorecard that separates hard failures from polish improvements.', 'A beginner wants the result explained in plain language without losing technical accuracy.', 'A power user wants structured JSON they can pipe into another agent or dashboard.'], 'io_contract': "Input: payload is a dict. Important optional keys include 'task', 'objective', 'prompt', 'conversation', 'messages', 'candidate_outputs', 'trace', 'rubric', 'constraints', 'progress', 'current_plan', 'completed_steps', 'blocked_steps', 'user_level', and 'customer_config'. Output: return a dict containing summary: str, primary_insights: list, recommended_actions: list, scores: dict with confidence and usefulness, details: dict, progress_state: dict with current_stage/next_step/blockers, user_experience: dict with plain_language_takeaway and interaction_suggestions, and fun_mode: dict with optional challenge_label, score_badge, and celebratory_microcopy. Fun fields must never replace the serious recommendation.", 'schema_version': '1.0.0', 'family_key': 'ai_memory::ai context window optimizer', 'is_generic_name': False}

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
    _profile_body_b64 = 'cGx1Z2luX25hbWUgPSAnQUkgQ29udGV4dCBXaW5kb3cgT3B0aW1pemVyJwpnb2FsID0gJ1ByaW9yaXRpemUgd2hpY2ggY29udGV4dCBzaG91bGQgYmUga2VwdCwgY29tcHJlc3NlZCwgb3IgZHJvcHBlZCBiZWZvcmUgYW4gQUkgbW9kZWwgY2FsbC4nCmRvbWFpbiA9ICdBSSBjb250ZXh0IHBhY2tpbmcgYW5kIHRva2VuIGJ1ZGdldCBtYW5hZ2VtZW50JwpjYXBhYmlsaXR5X3R5cGUgPSAnZGF0YV9pbnNpZ2h0Jwpsb2dpY19wcm9maWxlX2lkID0gJ2NvbnRleHRfd2luZG93X29wdGltaXplcl9wcm9maWxlJwpnZW5lcmF0aW9uX25vdGUgPSAnY2FwYWJpbGl0eS1zcGVjaWZpYyBwcm9maWxlIHJlcGxhY2VtZW50IGZvciBnZW5lcmljIHNlbWFudGljIHJlcGFpcicKdXNlX2Nhc2VzID0gWydSYW5rIGNvbnRleHQgc25pcHBldHMgYnkgcmVsZXZhbmNlIHRvIHRoZSBjdXJyZW50IHRhc2suJywgJ0RldGVjdCByZWR1bmRhbnQgb3Igc3RhbGUgY29udGV4dC4nLCAnU3VnZ2VzdCBjb21wYWN0IHJlcGxhY2VtZW50cyBmb3IgbGFyZ2UgcmVwZWF0ZWQgc2VjdGlvbnMuJywgJ1Nob3cgYSBjb21wYWN0IHByb2dyZXNzIHN0YXRlIGZvciB0aGlzIEFJIGNhcGFiaWxpdHkgZHVyaW5nIGJhc2VsaW5lIGNhcGFiaWxpdHkuJywgJ1JldHVybiB1c2VyLWZhY2luZyBndWlkYW5jZSB0aGF0IGlzIHVzZWZ1bCwgY29uY2lzZSwgYW5kIHNhZmUgdG8gYWN0IG9uLicsICdBdm9pZCBkdXBsaWNhdGluZyBleGlzdGluZyBBSSBwbHVnaW4gYmVoYXZpb3I7IGlkZW50aWZ5IHdoYXQgaXMgdW5pcXVlIGFib3V0IHRoaXMgY2FwYWJpbGl0eS4nXQpwYXlsb2FkX2RhdGEgPSBwYXlsb2FkIGlmIGlzaW5zdGFuY2UocGF5bG9hZCwgZGljdCkgZWxzZSB7fQpwYXlsb2FkX3dhcm5pbmdzID0gW10gaWYgaXNpbnN0YW5jZShwYXlsb2FkLCBkaWN0KSBlbHNlIFsncGF5bG9hZCB3YXMgbm90IGEgZGljdDsgdXNpbmcgZW1wdHkgcGF5bG9hZCddCmRlZl90ZXh0ID0gc3RyKHBheWxvYWRfZGF0YS5nZXQoJ3Rhc2snKSBvciBwYXlsb2FkX2RhdGEuZ2V0KCdvYmplY3RpdmUnKSBvciBwYXlsb2FkX2RhdGEuZ2V0KCdwcm9tcHQnKSBvciBnb2FsKS5zdHJpcCgpCm9iamVjdGl2ZV90ZXh0ID0gc3RyKHBheWxvYWRfZGF0YS5nZXQoJ29iamVjdGl2ZScpIG9yIGdvYWwpLnN0cmlwKCkKY29uc3RyYWludHMgPSBwYXlsb2FkX2RhdGEuZ2V0KCdjb25zdHJhaW50cycpIGlmIGlzaW5zdGFuY2UocGF5bG9hZF9kYXRhLmdldCgnY29uc3RyYWludHMnKSwgbGlzdCkgZWxzZSBbXQptZXNzYWdlcyA9IHBheWxvYWRfZGF0YS5nZXQoJ21lc3NhZ2VzJykgaWYgaXNpbnN0YW5jZShwYXlsb2FkX2RhdGEuZ2V0KCdtZXNzYWdlcycpLCBsaXN0KSBlbHNlIFtdCmNhbmRpZGF0ZV9vdXRwdXRzID0gcGF5bG9hZF9kYXRhLmdldCgnY2FuZGlkYXRlX291dHB1dHMnKSBpZiBpc2luc3RhbmNlKHBheWxvYWRfZGF0YS5nZXQoJ2NhbmRpZGF0ZV9vdXRwdXRzJyksIGxpc3QpIGVsc2UgW10Kc291cmNlX25vdGVzID0gcGF5bG9hZF9kYXRhLmdldCgnc291cmNlX25vdGVzJykgaWYgaXNpbnN0YW5jZShwYXlsb2FkX2RhdGEuZ2V0KCdzb3VyY2Vfbm90ZXMnKSwgbGlzdCkgZWxzZSBbXQp0b2tlbl9idWRnZXQgPSBpbnQocGF5bG9hZF9kYXRhLmdldCgndG9rZW5fYnVkZ2V0Jykgb3IgcGF5bG9hZF9kYXRhLmdldCgnbWF4X2NvbnRleHRfdG9rZW5zJykgb3IgMjA0OCkKaXRlbXMgPSBbXQpmb3Iga2V5IGluIFsncHJvbXB0JywgJ3Rhc2snLCAnb2JqZWN0aXZlJywgJ2N1cnJlbnRfcGxhbicsICdwcmV2aW91c19yZXN1bHRzJywgJ3RyYWNlJywgJ3J1YnJpYyddOgogICAgdmFsdWUgPSBwYXlsb2FkX2RhdGEuZ2V0KGtleSkKICAgIGlmIHZhbHVlIG5vdCBpbiAoTm9uZSwgJycsIFtdLCB7fSk6CiAgICAgICAgaXRlbXMuYXBwZW5kKHsnc291cmNlJzoga2V5LCAndGV4dCc6IHN0cih2YWx1ZSksICd0b2tlbnMnOiBtYXgoMSwgbGVuKHN0cih2YWx1ZSkpIC8vIDQpfSkKZm9yIGlkeCwgaXRlbSBpbiBlbnVtZXJhdGUobWVzc2FnZXMgKyBzb3VyY2Vfbm90ZXMgKyBjYW5kaWRhdGVfb3V0cHV0cyk6CiAgICB0ZXh0ID0gc3RyKGl0ZW0uZ2V0KCdjb250ZW50Jykgb3IgaXRlbS5nZXQoJ3RleHQnKSBvciBpdGVtIGlmIGlzaW5zdGFuY2UoaXRlbSwgZGljdCkgZWxzZSBpdGVtKQogICAgaXRlbXMuYXBwZW5kKHsnc291cmNlJzogJ2l0ZW1fJWQnICUgaWR4LCAndGV4dCc6IHRleHQsICd0b2tlbnMnOiBtYXgoMSwgbGVuKHRleHQpIC8vIDQpfSkKZm9yIGl0ZW0gaW4gaXRlbXM6CiAgICBsb3dlciA9IGl0ZW1bJ3RleHQnXS5sb3dlcigpCiAgICBpdGVtWydwcmlvcml0eSddID0gMQogICAgaWYgYW55KHdvcmQgaW4gbG93ZXIgZm9yIHdvcmQgaW4gWydtdXN0JywgJ2NvbnN0cmFpbnQnLCAnb2JqZWN0aXZlJywgJ2Vycm9yJywgJ2Jsb2NrZWQnLCAnYWNjZXB0YW5jZSddKToKICAgICAgICBpdGVtWydwcmlvcml0eSddICs9IDMKICAgIGlmIGFueSh3b3JkIGluIGxvd2VyIGZvciB3b3JkIGluIFsnZG9uZScsICd0aGFua3MnLCAnbWF5YmUnLCAnY2hhdHRlciddKToKICAgICAgICBpdGVtWydwcmlvcml0eSddIC09IDEKaXRlbXMgPSBzb3J0ZWQoaXRlbXMsIGtleT1sYW1iZGEgaXRlbTogKGl0ZW1bJ3ByaW9yaXR5J10sIC1pdGVtWyd0b2tlbnMnXSksIHJldmVyc2U9VHJ1ZSkKa2VwdCA9IFtdCmNvbXByZXNzZWQgPSBbXQpkcm9wcGVkID0gW10KdXNlZCA9IDAKZm9yIGl0ZW0gaW4gaXRlbXM6CiAgICBpZiB1c2VkICsgaXRlbVsndG9rZW5zJ10gPD0gdG9rZW5fYnVkZ2V0OgogICAgICAgIGtlcHQuYXBwZW5kKGl0ZW0pCiAgICAgICAgdXNlZCArPSBpdGVtWyd0b2tlbnMnXQogICAgZWxpZiBpdGVtWydwcmlvcml0eSddID49IDM6CiAgICAgICAgY29tcGFjdCA9IGRpY3QoaXRlbSkKICAgICAgICBjb21wYWN0Wydjb21wcmVzc2VkX3RleHQnXSA9IGl0ZW1bJ3RleHQnXVs6MjQwXQogICAgICAgIGNvbXByZXNzZWQuYXBwZW5kKGNvbXBhY3QpCiAgICAgICAgdXNlZCArPSBtaW4oaXRlbVsndG9rZW5zJ10sIDgwKQogICAgZWxzZToKICAgICAgICBkcm9wcGVkLmFwcGVuZChpdGVtKQpmaXQgPSB1c2VkIDw9IHRva2VuX2J1ZGdldApyZXN1bHRbJ3N1bW1hcnknXSA9IHBsdWdpbl9uYW1lICsgJzogb3B0aW1pemVkIGNvbnRleHQgdG8gYWJvdXQgJyArIHN0cih1c2VkKSArICcgdG9rZW5zIGFnYWluc3QgYnVkZ2V0ICcgKyBzdHIodG9rZW5fYnVkZ2V0KSArICcuJwpyZXN1bHRbJ3ByaW1hcnlfaW5zaWdodHMnXSA9IFsKICAgIHsndGl0bGUnOiAnS2VwdCBjb250ZXh0JywgJ2RldGFpbCc6IFtpdGVtWydzb3VyY2UnXSBmb3IgaXRlbSBpbiBrZXB0XX0sCiAgICB7J3RpdGxlJzogJ0NvbXByZXNzZWQgY29udGV4dCcsICdkZXRhaWwnOiBbaXRlbVsnc291cmNlJ10gZm9yIGl0ZW0gaW4gY29tcHJlc3NlZF19LAogICAgeyd0aXRsZSc6ICdEcm9wcGVkIGNvbnRleHQnLCAnZGV0YWlsJzogW2l0ZW1bJ3NvdXJjZSddIGZvciBpdGVtIGluIGRyb3BwZWRdfSwKXQpyZXN1bHRbJ3JlY29tbWVuZGVkX2FjdGlvbnMnXSA9IFsKICAgIHsnYWN0aW9uJzogJ0tlZXAgaGlnaC1wcmlvcml0eSBjb250ZXh0JywgJ2l0ZW1zJzogW2l0ZW1bJ3NvdXJjZSddIGZvciBpdGVtIGluIGtlcHRbOjhdXX0sCiAgICB7J2FjdGlvbic6ICdDb21wcmVzcyBvdmVyc2l6ZWQgYnV0IGltcG9ydGFudCBjb250ZXh0JywgJ2l0ZW1zJzogW2l0ZW1bJ3NvdXJjZSddIGZvciBpdGVtIGluIGNvbXByZXNzZWRbOjhdXX0sCiAgICB7J2FjdGlvbic6ICdEcm9wIGxvdy1zaWduYWwgY29udGV4dCcsICdpdGVtcyc6IFtpdGVtWydzb3VyY2UnXSBmb3IgaXRlbSBpbiBkcm9wcGVkWzo4XV19LApdCnJlc3VsdFsnc2NvcmVzJ10gPSB7J2NvbmZpZGVuY2UnOiByb3VuZChtaW4oMC45MiwgMC40NSArIDAuMDggKiBsZW4oaXRlbXNbOjVdKSksIDIpLCAndG9rZW5fYnVkZ2V0X2ZpdCc6IDEuMCBpZiBmaXQgZWxzZSByb3VuZCh0b2tlbl9idWRnZXQgLyBtYXgoMSwgdXNlZCksIDIpLCAnY29udGV4dF9yZXRlbnRpb24nOiByb3VuZChsZW4oa2VwdCkgLyBtYXgoMSwgbGVuKGl0ZW1zKSksIDIpLCAncmlzayc6IHJvdW5kKDAuMTggKyAoMC4xOCBpZiBub3QgZml0IGVsc2UgMCkgKyAwLjAzICogbGVuKGRyb3BwZWQpLCAyKX0KcmVzdWx0WydkZXRhaWxzJ10gPSB7J2tlcHRfY29udGV4dCc6IGtlcHRbOjEwXSwgJ2NvbXByZXNzZWRfY29udGV4dCc6IGNvbXByZXNzZWRbOjEwXSwgJ2Ryb3BwZWRfY29udGV4dCc6IGRyb3BwZWRbOjEwXSwgJ3Rva2VuX2J1ZGdldCc6IHRva2VuX2J1ZGdldCwgJ2VzdGltYXRlZF90b2tlbnMnOiB1c2VkLCAnbWlzc2luZ19pbnB1dHMnOiBbJ2NvbnRleHQgaXRlbXMnXSBpZiBub3QgaXRlbXMgZWxzZSBbXX0KcmVzdWx0WydkZXRhaWxzJ11bJ3VzZV9jYXNlcyddID0gdXNlX2Nhc2VzCnJlc3VsdFsnZGV0YWlscyddWydnZW5lcmF0aW9uX25vdGUnXSA9IGdlbmVyYXRpb25fbm90ZQpyZXN1bHRbJ2RldGFpbHMnXVsnY2FwYWJpbGl0eV90eXBlJ10gPSBjYXBhYmlsaXR5X3R5cGUKcmVzdWx0WydkZXRhaWxzJ11bJ2xvZ2ljX3Byb2ZpbGVfaWQnXSA9IGxvZ2ljX3Byb2ZpbGVfaWQKcmVzdWx0WydkZXRhaWxzJ11bJ3BheWxvYWRfd2FybmluZ3MnXSA9IHBheWxvYWRfd2FybmluZ3MKcmVzdWx0Wydwcm9ncmVzc19zdGF0ZSddID0gewogICAgJ2N1cnJlbnRfc3RhZ2UnOiBsb2dpY19wcm9maWxlX2lkLAogICAgJ25leHRfc3RlcCc6ICdVc2Uga2VwdF9jb250ZXh0LCB0aGVuIGNvbXByZXNzZWRfY29udGV4dCwgYW5kIG9taXQgZHJvcHBlZF9jb250ZXh0LicsCiAgICAnYmxvY2tlcnMnOiByZXN1bHRbJ2RldGFpbHMnXS5nZXQoJ21pc3NpbmdfaW5wdXRzJywgW10pWzo0XSwKICAgICdkb25lX3NpZ25hbHMnOiBbJ2NhcGFiaWxpdHlfc3BlY2lmaWNfYW5hbHlzaXNfY29tcGxldGUnLCBsb2dpY19wcm9maWxlX2lkXSwKfQpyZXN1bHRbJ3VzZXJfZXhwZXJpZW5jZSddID0gewogICAgJ3BsYWluX2xhbmd1YWdlX3Rha2Vhd2F5JzogcmVzdWx0WydzdW1tYXJ5J10sCiAgICAnYmVnaW5uZXJfdGlwJzogJ1VzZSB0aGUgZmlyc3QgcmVjb21tZW5kYXRpb24gYXMgdGhlIG5leHQgY29uY3JldGUgc3RlcC4nLAogICAgJ3Bvd2VyX3VzZXJfdGlwJzogJ1Bhc3MgZGV0YWlscyBhbmQgc2NvcmVzIGludG8gdGhlIG5leHQgQUkgY2FwYWJpbGl0eSBwbHVnaW4uJywKICAgICdpbnRlcmFjdGlvbl9zdWdnZXN0aW9ucyc6IFtpdGVtLmdldCgnYWN0aW9uJywgc3RyKGl0ZW0pKSBmb3IgaXRlbSBpbiByZXN1bHQuZ2V0KCdyZWNvbW1lbmRlZF9hY3Rpb25zJywgW10pWzozXV0sCn0KcmVzdWx0WydmdW5fbW9kZSddID0gewogICAgJ2NoYWxsZW5nZV9sYWJlbCc6ICdDYXBhYmlsaXR5IFJ1bicsCiAgICAnc2NvcmVfYmFkZ2UnOiAnU3Ryb25nIFNpZ25hbCcgaWYgcmVzdWx0LmdldCgnc2NvcmVzJywge30pLmdldCgnY29uZmlkZW5jZScsIDApID49IDAuNjUgZWxzZSAnTmVlZHMgQ29udGV4dCcsCiAgICAnbWljcm9jb3B5JzogJ1RoZSByZXN1bHQgaXMgc3RydWN0dXJlZCBzbyBhbm90aGVyIGFnZW50IGNhbiBwaWNrIGl0IHVwIGNsZWFubHkuJywKICAgICdvcHRpb25hbF9uZXh0X2NoYWxsZW5nZSc6ICdVc2Uga2VwdF9jb250ZXh0LCB0aGVuIGNvbXByZXNzZWRfY29udGV4dCwgYW5kIG9taXQgZHJvcHBlZF9jb250ZXh0LicsCn0='
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
