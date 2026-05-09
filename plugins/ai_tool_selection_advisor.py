from __future__ import annotations

"""
Auto-generated Francis plugin module.

THIS FILE IS GENERATED. Manual edits may be overwritten by the factory.

Plugin: AI Tool Selection Advisor
Slug: ai_tool_selection_advisor
"""

from typing import Any, Dict, Optional

__all__ = ["invoke", "_run_core_logic", "SkillContext"]

# ---------------------------------------------------------------------------
# Plugin metadata (used by Station C, registry, and tooling)
# ---------------------------------------------------------------------------

_PLUGIN_NAME: str = 'AI Tool Selection Advisor'
_PLUGIN_SLUG: str = 'ai_tool_selection_advisor'
_PLUGIN_CATEGORY: str = 'ai_agents'
_PLUGIN_VERSION: str = '0.1.0'
_PLUGIN_GOAL: str = 'Select the best available tool or integration for an AI workflow based on task requirements.'
_PLUGIN_TAGS = ['ai', 'tools', 'routing', 'integrations', 'autonomous_factory', 'ai_progress', 'phase_1']
_PLUGIN_OWNER_ID = 'francis-factory'
_PLUGIN_CAPABILITY_TYPE = 'integration'
_PLUGIN_INTENDED_DOMAIN = 'AI tool routing and integration choice'
_PLUGIN_USE_CASES = ['Map task requirements to candidate tools and explain tradeoffs.', 'Flag when no external tool is needed.', 'Recommend tool call order for multi-step AI workflows.', 'Show a compact progress state for this AI capability during baseline capability.', 'Return user-facing guidance that is useful, concise, and safe to act on.', 'Avoid duplicating existing AI plugin behavior; identify what is unique about this capability.']
_PLUGIN_RESULT_SCHEMA_VERSION: str = '1.0.0'

# Lightweight manifest for discovery/registry.
_PLUGIN_MANIFEST = {'name': 'AI Tool Selection Advisor', 'slug': 'ai_tool_selection_advisor', 'goal': 'Select the best available tool or integration for an AI workflow based on task requirements.', 'category': 'ai_agents', 'tags': ['ai', 'tools', 'routing', 'integrations', 'autonomous_factory', 'ai_progress', 'phase_1'], 'version': '0.1.0', 'capability_type': 'integration', 'intended_domain': 'AI tool routing and integration choice', 'owner_id': 'francis-factory', 'use_cases': ['Map task requirements to candidate tools and explain tradeoffs.', 'Flag when no external tool is needed.', 'Recommend tool call order for multi-step AI workflows.', 'Show a compact progress state for this AI capability during baseline capability.', 'Return user-facing guidance that is useful, concise, and safe to act on.', 'Avoid duplicating existing AI plugin behavior; identify what is unique about this capability.'], 'primary_use_case': 'Map task requirements to candidate tools and explain tradeoffs.', 'problem_statement': 'Francis needs a focused AI plugin for AI tool routing and integration choice. The plugin must turn messy user notes, model outputs, traces, or workflow state into structured, actionable AI assistance. It should improve autonomous progress by making the next step obvious, reducing duplicated work, and exposing risks before they become failures. The plugin must stay deterministic, avoid hidden external side effects, and make its reasoning inspectable through concise details and scores.', 'primary_inputs': 'A payload dict that may contain task, objective, prompt, conversation, artifacts, candidate_outputs, traces, rubric, constraints, user_level, current_plan, completed_steps, blocked_steps, source_notes, and optional customer_config.', 'primary_outputs': 'A normalized result dict with summary, primary_insights, recommended_actions, scores, details, progress_state, user_experience, fun_mode, and machine-readable diagnostics.', 'constraints': 'Do not execute tools, browse, mutate files, call external APIs, or claim facts not present in the payload. Prefer deterministic analysis. If data is missing, say what is missing and return a useful fallback. Keep recommendations concrete. Avoid creating a capability that duplicates another AI roadmap plugin.', 'example_use_cases': ['A user asks Francis to improve an AI workflow related to AI tool routing and integration choice.', 'A long-running autonomous run needs a checkpoint summary and the next best action.', 'An operator wants a scorecard that separates hard failures from polish improvements.', 'A beginner wants the result explained in plain language without losing technical accuracy.', 'A power user wants structured JSON they can pipe into another agent or dashboard.'], 'io_contract': "Input: payload is a dict. Important optional keys include 'task', 'objective', 'prompt', 'conversation', 'messages', 'candidate_outputs', 'trace', 'rubric', 'constraints', 'progress', 'current_plan', 'completed_steps', 'blocked_steps', 'user_level', and 'customer_config'. Output: return a dict containing summary: str, primary_insights: list, recommended_actions: list, scores: dict with confidence and usefulness, details: dict, progress_state: dict with current_stage/next_step/blockers, user_experience: dict with plain_language_takeaway and interaction_suggestions, and fun_mode: dict with optional challenge_label, score_badge, and celebratory_microcopy. Fun fields must never replace the serious recommendation.", 'schema_version': '1.0.0', 'family_key': 'ai_agents::ai selection advisor', 'is_generic_name': False}

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
    _profile_body_b64 = 'cGx1Z2luX25hbWUgPSAnQUkgVG9vbCBTZWxlY3Rpb24gQWR2aXNvcicKZ29hbCA9ICdTZWxlY3QgdGhlIGJlc3QgYXZhaWxhYmxlIHRvb2wgb3IgaW50ZWdyYXRpb24gZm9yIGFuIEFJIHdvcmtmbG93IGJhc2VkIG9uIHRhc2sgcmVxdWlyZW1lbnRzLicKZG9tYWluID0gJ0FJIHRvb2wgcm91dGluZyBhbmQgaW50ZWdyYXRpb24gY2hvaWNlJwpjYXBhYmlsaXR5X3R5cGUgPSAnaW50ZWdyYXRpb24nCmxvZ2ljX3Byb2ZpbGVfaWQgPSAndG9vbF9zZWxlY3Rpb25fcHJvZmlsZScKZ2VuZXJhdGlvbl9ub3RlID0gJ2NhcGFiaWxpdHktc3BlY2lmaWMgcHJvZmlsZSByZXBsYWNlbWVudCBmb3IgZ2VuZXJpYyBzZW1hbnRpYyByZXBhaXInCnVzZV9jYXNlcyA9IFsnTWFwIHRhc2sgcmVxdWlyZW1lbnRzIHRvIGNhbmRpZGF0ZSB0b29scyBhbmQgZXhwbGFpbiB0cmFkZW9mZnMuJywgJ0ZsYWcgd2hlbiBubyBleHRlcm5hbCB0b29sIGlzIG5lZWRlZC4nLCAnUmVjb21tZW5kIHRvb2wgY2FsbCBvcmRlciBmb3IgbXVsdGktc3RlcCBBSSB3b3JrZmxvd3MuJywgJ1Nob3cgYSBjb21wYWN0IHByb2dyZXNzIHN0YXRlIGZvciB0aGlzIEFJIGNhcGFiaWxpdHkgZHVyaW5nIGJhc2VsaW5lIGNhcGFiaWxpdHkuJywgJ1JldHVybiB1c2VyLWZhY2luZyBndWlkYW5jZSB0aGF0IGlzIHVzZWZ1bCwgY29uY2lzZSwgYW5kIHNhZmUgdG8gYWN0IG9uLicsICdBdm9pZCBkdXBsaWNhdGluZyBleGlzdGluZyBBSSBwbHVnaW4gYmVoYXZpb3I7IGlkZW50aWZ5IHdoYXQgaXMgdW5pcXVlIGFib3V0IHRoaXMgY2FwYWJpbGl0eS4nXQpwYXlsb2FkX2RhdGEgPSBwYXlsb2FkIGlmIGlzaW5zdGFuY2UocGF5bG9hZCwgZGljdCkgZWxzZSB7fQpwYXlsb2FkX3dhcm5pbmdzID0gW10gaWYgaXNpbnN0YW5jZShwYXlsb2FkLCBkaWN0KSBlbHNlIFsncGF5bG9hZCB3YXMgbm90IGEgZGljdDsgdXNpbmcgZW1wdHkgcGF5bG9hZCddCmRlZl90ZXh0ID0gc3RyKHBheWxvYWRfZGF0YS5nZXQoJ3Rhc2snKSBvciBwYXlsb2FkX2RhdGEuZ2V0KCdvYmplY3RpdmUnKSBvciBwYXlsb2FkX2RhdGEuZ2V0KCdwcm9tcHQnKSBvciBnb2FsKS5zdHJpcCgpCm9iamVjdGl2ZV90ZXh0ID0gc3RyKHBheWxvYWRfZGF0YS5nZXQoJ29iamVjdGl2ZScpIG9yIGdvYWwpLnN0cmlwKCkKY29uc3RyYWludHMgPSBwYXlsb2FkX2RhdGEuZ2V0KCdjb25zdHJhaW50cycpIGlmIGlzaW5zdGFuY2UocGF5bG9hZF9kYXRhLmdldCgnY29uc3RyYWludHMnKSwgbGlzdCkgZWxzZSBbXQptZXNzYWdlcyA9IHBheWxvYWRfZGF0YS5nZXQoJ21lc3NhZ2VzJykgaWYgaXNpbnN0YW5jZShwYXlsb2FkX2RhdGEuZ2V0KCdtZXNzYWdlcycpLCBsaXN0KSBlbHNlIFtdCmNhbmRpZGF0ZV9vdXRwdXRzID0gcGF5bG9hZF9kYXRhLmdldCgnY2FuZGlkYXRlX291dHB1dHMnKSBpZiBpc2luc3RhbmNlKHBheWxvYWRfZGF0YS5nZXQoJ2NhbmRpZGF0ZV9vdXRwdXRzJyksIGxpc3QpIGVsc2UgW10Kc291cmNlX25vdGVzID0gcGF5bG9hZF9kYXRhLmdldCgnc291cmNlX25vdGVzJykgaWYgaXNpbnN0YW5jZShwYXlsb2FkX2RhdGEuZ2V0KCdzb3VyY2Vfbm90ZXMnKSwgbGlzdCkgZWxzZSBbXQp0ZXh0ID0gJyAnLmpvaW4oW2RlZl90ZXh0LCBvYmplY3RpdmVfdGV4dCwgJyAnLmpvaW4oc3RyKGl0ZW0pIGZvciBpdGVtIGluIGNvbnN0cmFpbnRzKV0pLmxvd2VyKCkKdG9vbF9ydWxlcyA9IFsKICAgICgnY29kZV9lZGl0b3InLCBbJ2NvZGUnLCAncmVwbycsICdmaWxlJywgJ2J1ZycsICd0ZXN0JywgJ3B5dGhvbicsICdqYXZhc2NyaXB0J10sICdOZWVkZWQgZm9yIHNvdXJjZSBpbnNwZWN0aW9uIG9yIGNvZGUgY2hhbmdlcy4nKSwKICAgICgndGVybWluYWwnLCBbJ3J1bicsICdjb21tYW5kJywgJ3Rlc3QnLCAnY29tcGlsZScsICdzZXJ2ZXInLCAncHJvY2VzcyddLCAnTmVlZGVkIGZvciBsb2NhbCB2ZXJpZmljYXRpb24gYW5kIHByb2Nlc3MgY29udHJvbC4nKSwKICAgICgnd2ViX3NlYXJjaCcsIFsnbGF0ZXN0JywgJ2N1cnJlbnQnLCAncHJpY2UnLCAnbmV3cycsICdkb2NzJywgJ2NpdGF0aW9uJ10sICdOZWVkZWQgd2hlbiBmYWN0cyBtYXkgaGF2ZSBjaGFuZ2VkIG9yIHNvdXJjZXMgYXJlIHJlcXVpcmVkLicpLAogICAgKCdyZXRyaWV2YWwnLCBbJ3NlYXJjaCcsICdrbm93bGVkZ2UnLCAnZG9jdW1lbnQnLCAnbm90ZXMnLCAnbWVtb3J5J10sICdOZWVkZWQgdG8gZmluZCBncm91bmRpbmcgY29udGV4dCBiZWZvcmUgZ2VuZXJhdGlvbi4nKSwKICAgICgncGxhbm5lcicsIFsnY29tcGxleCcsICdtdWx0aS1zdGVwJywgJ2hhbmRvZmYnLCAnYWdlbnQnLCAnZGVsZWdhdGUnXSwgJ05lZWRlZCB0byBzZXF1ZW5jZSB3b3JrIGFuZCBwcmV2ZW50IGR1cGxpY2F0ZWQgZWZmb3J0LicpLApdCnJlY29tbWVuZGF0aW9ucyA9IFtdCmZvciBuYW1lLCBrZXl3b3JkcywgcmF0aW9uYWxlIGluIHRvb2xfcnVsZXM6CiAgICBoaXRzID0gW3dvcmQgZm9yIHdvcmQgaW4ga2V5d29yZHMgaWYgd29yZCBpbiB0ZXh0XQogICAgaWYgaGl0czoKICAgICAgICByZWNvbW1lbmRhdGlvbnMuYXBwZW5kKHsndG9vbCc6IG5hbWUsICdtYXRjaGVkX3NpZ25hbHMnOiBoaXRzLCAncmF0aW9uYWxlJzogcmF0aW9uYWxlLCAncHJpb3JpdHknOiBsZW4oaGl0cyl9KQpyZWNvbW1lbmRhdGlvbnMgPSBzb3J0ZWQocmVjb21tZW5kYXRpb25zLCBrZXk9bGFtYmRhIGl0ZW06IGl0ZW1bJ3ByaW9yaXR5J10sIHJldmVyc2U9VHJ1ZSkKaWYgbm90IHJlY29tbWVuZGF0aW9uczoKICAgIHJlY29tbWVuZGF0aW9ucy5hcHBlbmQoeyd0b29sJzogJ2NsYXJpZnlpbmdfcHJvbXB0JywgJ21hdGNoZWRfc2lnbmFscyc6IFtdLCAncmF0aW9uYWxlJzogJ1Rhc2sgbGFja3MgZW5vdWdoIG9wZXJhdGlvbmFsIHNpZ25hbHMgdG8gY2hvb3NlIGEgc3Ryb25nZXIgdG9vbC4nLCAncHJpb3JpdHknOiAwfSkKcmVqZWN0ZWRfdG9vbHMgPSBbXQppZiAnZXh0ZXJuYWwnIGluIHRleHQgb3IgJ2ludGVybmV0JyBpbiB0ZXh0OgogICAgcmVqZWN0ZWRfdG9vbHMuYXBwZW5kKHsndG9vbCc6ICdzaWxlbnRfb2ZmbGluZV9hbnN3ZXInLCAncmVhc29uJzogJ0V4dGVybmFsIGdyb3VuZGluZyB3YXMgcmVxdWVzdGVkIG9yIGltcGxpZWQuJ30pCmlmICdkZWxldGUnIGluIHRleHQgb3IgJ2Rlc3RydWN0aXZlJyBpbiB0ZXh0OgogICAgcmVqZWN0ZWRfdG9vbHMuYXBwZW5kKHsndG9vbCc6ICdhdXRvbWF0aWNfbXV0YXRpb24nLCAncmVhc29uJzogJ1BvdGVudGlhbGx5IGRlc3RydWN0aXZlIGFjdGlvbnMgcmVxdWlyZSBleHBsaWNpdCBjb25maXJtYXRpb24uJ30pCnNlbGVjdGlvbl9jb25maWRlbmNlID0gbWluKDAuOTMsIDAuNDggKyAwLjEyICogbGVuKHJlY29tbWVuZGF0aW9ucykgKyAwLjAzICogc3VtKGxlbihpdGVtWydtYXRjaGVkX3NpZ25hbHMnXSkgZm9yIGl0ZW0gaW4gcmVjb21tZW5kYXRpb25zKSkKcmVzdWx0WydzdW1tYXJ5J10gPSBwbHVnaW5fbmFtZSArICc6IHNlbGVjdGVkICcgKyByZWNvbW1lbmRhdGlvbnNbMF1bJ3Rvb2wnXSArICcgYXMgdGhlIGZpcnN0IHRvb2wgZm9yICcgKyBkZWZfdGV4dFs6MTQwXSArICcuJwpyZXN1bHRbJ3ByaW1hcnlfaW5zaWdodHMnXSA9IFsKICAgIHsndGl0bGUnOiAnVG9wIHRvb2wnLCAnZGV0YWlsJzogcmVjb21tZW5kYXRpb25zWzBdfSwKICAgIHsndGl0bGUnOiAnVG9vbCBzaWduYWxzJywgJ2RldGFpbCc6IFtpdGVtWydtYXRjaGVkX3NpZ25hbHMnXSBmb3IgaXRlbSBpbiByZWNvbW1lbmRhdGlvbnNdfSwKICAgIHsndGl0bGUnOiAnUmVqZWN0ZWQgdG9vbHMnLCAnZGV0YWlsJzogcmVqZWN0ZWRfdG9vbHMgb3IgJ05vIGV4cGxpY2l0IHJlamVjdGlvbnMuJ30sCl0KcmVzdWx0WydyZWNvbW1lbmRlZF9hY3Rpb25zJ10gPSBbCiAgICB7J2FjdGlvbic6ICdVc2UgJyArIGl0ZW1bJ3Rvb2wnXSwgJ3doeSc6IGl0ZW1bJ3JhdGlvbmFsZSddLCAnc2lnbmFscyc6IGl0ZW1bJ21hdGNoZWRfc2lnbmFscyddfSBmb3IgaXRlbSBpbiByZWNvbW1lbmRhdGlvbnNbOjRdCl0KcmVzdWx0WydzY29yZXMnXSA9IHsnY29uZmlkZW5jZSc6IHJvdW5kKHNlbGVjdGlvbl9jb25maWRlbmNlLCAyKSwgJ3VzZWZ1bG5lc3MnOiByb3VuZChtaW4oMC45NCwgMC41NSArIDAuMSAqIGxlbihyZWNvbW1lbmRhdGlvbnMpKSwgMiksICdyb3V0aW5nX3NwZWNpZmljaXR5Jzogcm91bmQobWluKDEuMCwgMC4zNSArIDAuMDggKiBzdW0obGVuKGl0ZW1bJ21hdGNoZWRfc2lnbmFscyddKSBmb3IgaXRlbSBpbiByZWNvbW1lbmRhdGlvbnMpKSwgMiksICdyaXNrJzogcm91bmQoMC4yMiArIDAuMDggKiBsZW4ocmVqZWN0ZWRfdG9vbHMpLCAyKX0KcmVzdWx0WydkZXRhaWxzJ10gPSB7J3Rvb2xfcmVjb21tZW5kYXRpb25zJzogcmVjb21tZW5kYXRpb25zLCAncmVqZWN0ZWRfdG9vbHMnOiByZWplY3RlZF90b29scywgJ3NlbGVjdGlvbl9yYXRpb25hbGUnOiByZWNvbW1lbmRhdGlvbnNbMF1bJ3JhdGlvbmFsZSddLCAnbWlzc2luZ19pbnB1dHMnOiBbJ3Rhc2snXSBpZiBub3QgZGVmX3RleHQgZWxzZSBbXX0KcmVzdWx0WydkZXRhaWxzJ11bJ3VzZV9jYXNlcyddID0gdXNlX2Nhc2VzCnJlc3VsdFsnZGV0YWlscyddWydnZW5lcmF0aW9uX25vdGUnXSA9IGdlbmVyYXRpb25fbm90ZQpyZXN1bHRbJ2RldGFpbHMnXVsnY2FwYWJpbGl0eV90eXBlJ10gPSBjYXBhYmlsaXR5X3R5cGUKcmVzdWx0WydkZXRhaWxzJ11bJ2xvZ2ljX3Byb2ZpbGVfaWQnXSA9IGxvZ2ljX3Byb2ZpbGVfaWQKcmVzdWx0WydkZXRhaWxzJ11bJ3BheWxvYWRfd2FybmluZ3MnXSA9IHBheWxvYWRfd2FybmluZ3MKcmVzdWx0Wydwcm9ncmVzc19zdGF0ZSddID0gewogICAgJ2N1cnJlbnRfc3RhZ2UnOiBsb2dpY19wcm9maWxlX2lkLAogICAgJ25leHRfc3RlcCc6ICdVc2UgJyArIHJlY29tbWVuZGF0aW9uc1swXVsndG9vbCddLAogICAgJ2Jsb2NrZXJzJzogcmVzdWx0WydkZXRhaWxzJ10uZ2V0KCdtaXNzaW5nX2lucHV0cycsIFtdKVs6NF0sCiAgICAnZG9uZV9zaWduYWxzJzogWydjYXBhYmlsaXR5X3NwZWNpZmljX2FuYWx5c2lzX2NvbXBsZXRlJywgbG9naWNfcHJvZmlsZV9pZF0sCn0KcmVzdWx0Wyd1c2VyX2V4cGVyaWVuY2UnXSA9IHsKICAgICdwbGFpbl9sYW5ndWFnZV90YWtlYXdheSc6IHJlc3VsdFsnc3VtbWFyeSddLAogICAgJ2JlZ2lubmVyX3RpcCc6ICdVc2UgdGhlIGZpcnN0IHJlY29tbWVuZGF0aW9uIGFzIHRoZSBuZXh0IGNvbmNyZXRlIHN0ZXAuJywKICAgICdwb3dlcl91c2VyX3RpcCc6ICdQYXNzIGRldGFpbHMgYW5kIHNjb3JlcyBpbnRvIHRoZSBuZXh0IEFJIGNhcGFiaWxpdHkgcGx1Z2luLicsCiAgICAnaW50ZXJhY3Rpb25fc3VnZ2VzdGlvbnMnOiBbaXRlbS5nZXQoJ2FjdGlvbicsIHN0cihpdGVtKSkgZm9yIGl0ZW0gaW4gcmVzdWx0LmdldCgncmVjb21tZW5kZWRfYWN0aW9ucycsIFtdKVs6M11dLAp9CnJlc3VsdFsnZnVuX21vZGUnXSA9IHsKICAgICdjaGFsbGVuZ2VfbGFiZWwnOiAnQ2FwYWJpbGl0eSBSdW4nLAogICAgJ3Njb3JlX2JhZGdlJzogJ1N0cm9uZyBTaWduYWwnIGlmIHJlc3VsdC5nZXQoJ3Njb3JlcycsIHt9KS5nZXQoJ2NvbmZpZGVuY2UnLCAwKSA+PSAwLjY1IGVsc2UgJ05lZWRzIENvbnRleHQnLAogICAgJ21pY3JvY29weSc6ICdUaGUgcmVzdWx0IGlzIHN0cnVjdHVyZWQgc28gYW5vdGhlciBhZ2VudCBjYW4gcGljayBpdCB1cCBjbGVhbmx5LicsCiAgICAnb3B0aW9uYWxfbmV4dF9jaGFsbGVuZ2UnOiAnVXNlICcgKyByZWNvbW1lbmRhdGlvbnNbMF1bJ3Rvb2wnXSwKfQ=='
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
