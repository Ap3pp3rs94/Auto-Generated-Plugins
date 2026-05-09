from __future__ import annotations

"""
Auto-generated Francis plugin module.

THIS FILE IS GENERATED. Manual edits may be overwritten by the factory.

Plugin: AI Output Quality Scorer
Slug: ai_output_quality_scorer
"""

from typing import Any, Dict, Optional

__all__ = ["invoke", "_run_core_logic", "SkillContext"]

# ---------------------------------------------------------------------------
# Plugin metadata (used by Station C, registry, and tooling)
# ---------------------------------------------------------------------------

_PLUGIN_NAME: str = 'AI Output Quality Scorer'
_PLUGIN_SLUG: str = 'ai_output_quality_scorer'
_PLUGIN_CATEGORY: str = 'ai_evaluation'
_PLUGIN_VERSION: str = '0.1.0'
_PLUGIN_GOAL: str = 'Score an AI response for correctness, completeness, usefulness, and instruction adherence.'
_PLUGIN_TAGS = ['ai', 'evaluation', 'quality', 'scoring', 'autonomous_factory', 'ai_progress', 'phase_1']
_PLUGIN_OWNER_ID = 'francis-factory'
_PLUGIN_CAPABILITY_TYPE = 'scoring'
_PLUGIN_INTENDED_DOMAIN = 'AI evaluation and response quality control'
_PLUGIN_USE_CASES = ['Grade a response against a user request and rubric.', 'Highlight missing requirements or weak assumptions.', 'Produce an actionable improvement checklist.', 'Show a compact progress state for this AI capability during baseline capability.', 'Return user-facing guidance that is useful, concise, and safe to act on.', 'Avoid duplicating existing AI plugin behavior; identify what is unique about this capability.']
_PLUGIN_RESULT_SCHEMA_VERSION: str = '1.0.0'

# Lightweight manifest for discovery/registry.
_PLUGIN_MANIFEST = {'name': 'AI Output Quality Scorer', 'slug': 'ai_output_quality_scorer', 'goal': 'Score an AI response for correctness, completeness, usefulness, and instruction adherence.', 'category': 'ai_evaluation', 'tags': ['ai', 'evaluation', 'quality', 'scoring', 'autonomous_factory', 'ai_progress', 'phase_1'], 'version': '0.1.0', 'capability_type': 'scoring', 'intended_domain': 'AI evaluation and response quality control', 'owner_id': 'francis-factory', 'use_cases': ['Grade a response against a user request and rubric.', 'Highlight missing requirements or weak assumptions.', 'Produce an actionable improvement checklist.', 'Show a compact progress state for this AI capability during baseline capability.', 'Return user-facing guidance that is useful, concise, and safe to act on.', 'Avoid duplicating existing AI plugin behavior; identify what is unique about this capability.'], 'primary_use_case': 'Grade a response against a user request and rubric.', 'problem_statement': 'Francis needs a focused AI plugin for AI evaluation and response quality control. The plugin must turn messy user notes, model outputs, traces, or workflow state into structured, actionable AI assistance. It should improve autonomous progress by making the next step obvious, reducing duplicated work, and exposing risks before they become failures. The plugin must stay deterministic, avoid hidden external side effects, and make its reasoning inspectable through concise details and scores.', 'primary_inputs': 'A payload dict that may contain task, objective, prompt, conversation, artifacts, candidate_outputs, traces, rubric, constraints, user_level, current_plan, completed_steps, blocked_steps, source_notes, and optional customer_config.', 'primary_outputs': 'A normalized result dict with summary, primary_insights, recommended_actions, scores, details, progress_state, user_experience, fun_mode, and machine-readable diagnostics.', 'constraints': 'Do not execute tools, browse, mutate files, call external APIs, or claim facts not present in the payload. Prefer deterministic analysis. If data is missing, say what is missing and return a useful fallback. Keep recommendations concrete. Avoid creating a capability that duplicates another AI roadmap plugin.', 'example_use_cases': ['A user asks Francis to improve an AI workflow related to AI evaluation and response quality control.', 'A long-running autonomous run needs a checkpoint summary and the next best action.', 'An operator wants a scorecard that separates hard failures from polish improvements.', 'A beginner wants the result explained in plain language without losing technical accuracy.', 'A power user wants structured JSON they can pipe into another agent or dashboard.'], 'io_contract': "Input: payload is a dict. Important optional keys include 'task', 'objective', 'prompt', 'conversation', 'messages', 'candidate_outputs', 'trace', 'rubric', 'constraints', 'progress', 'current_plan', 'completed_steps', 'blocked_steps', 'user_level', and 'customer_config'. Output: return a dict containing summary: str, primary_insights: list, recommended_actions: list, scores: dict with confidence and usefulness, details: dict, progress_state: dict with current_stage/next_step/blockers, user_experience: dict with plain_language_takeaway and interaction_suggestions, and fun_mode: dict with optional challenge_label, score_badge, and celebratory_microcopy. Fun fields must never replace the serious recommendation.", 'schema_version': '1.0.0', 'family_key': 'ai_evaluation::ai output quality scorer', 'is_generic_name': False}

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
    _profile_body_b64 = 'cGx1Z2luX25hbWUgPSAnQUkgT3V0cHV0IFF1YWxpdHkgU2NvcmVyJwpnb2FsID0gJ1Njb3JlIGFuIEFJIHJlc3BvbnNlIGZvciBjb3JyZWN0bmVzcywgY29tcGxldGVuZXNzLCB1c2VmdWxuZXNzLCBhbmQgaW5zdHJ1Y3Rpb24gYWRoZXJlbmNlLicKZG9tYWluID0gJ0FJIGV2YWx1YXRpb24gYW5kIHJlc3BvbnNlIHF1YWxpdHkgY29udHJvbCcKY2FwYWJpbGl0eV90eXBlID0gJ3Njb3JpbmcnCmxvZ2ljX3Byb2ZpbGVfaWQgPSAnb3V0cHV0X3F1YWxpdHlfc2NvcmVyX3Byb2ZpbGUnCmdlbmVyYXRpb25fbm90ZSA9ICdjYXBhYmlsaXR5LXNwZWNpZmljIHByb2ZpbGUgcmVwbGFjZW1lbnQgZm9yIGdlbmVyaWMgc2VtYW50aWMgcmVwYWlyJwp1c2VfY2FzZXMgPSBbJ0dyYWRlIGEgcmVzcG9uc2UgYWdhaW5zdCBhIHVzZXIgcmVxdWVzdCBhbmQgcnVicmljLicsICdIaWdobGlnaHQgbWlzc2luZyByZXF1aXJlbWVudHMgb3Igd2VhayBhc3N1bXB0aW9ucy4nLCAnUHJvZHVjZSBhbiBhY3Rpb25hYmxlIGltcHJvdmVtZW50IGNoZWNrbGlzdC4nLCAnU2hvdyBhIGNvbXBhY3QgcHJvZ3Jlc3Mgc3RhdGUgZm9yIHRoaXMgQUkgY2FwYWJpbGl0eSBkdXJpbmcgYmFzZWxpbmUgY2FwYWJpbGl0eS4nLCAnUmV0dXJuIHVzZXItZmFjaW5nIGd1aWRhbmNlIHRoYXQgaXMgdXNlZnVsLCBjb25jaXNlLCBhbmQgc2FmZSB0byBhY3Qgb24uJywgJ0F2b2lkIGR1cGxpY2F0aW5nIGV4aXN0aW5nIEFJIHBsdWdpbiBiZWhhdmlvcjsgaWRlbnRpZnkgd2hhdCBpcyB1bmlxdWUgYWJvdXQgdGhpcyBjYXBhYmlsaXR5LiddCnBheWxvYWRfZGF0YSA9IHBheWxvYWQgaWYgaXNpbnN0YW5jZShwYXlsb2FkLCBkaWN0KSBlbHNlIHt9CnBheWxvYWRfd2FybmluZ3MgPSBbXSBpZiBpc2luc3RhbmNlKHBheWxvYWQsIGRpY3QpIGVsc2UgWydwYXlsb2FkIHdhcyBub3QgYSBkaWN0OyB1c2luZyBlbXB0eSBwYXlsb2FkJ10KZGVmX3RleHQgPSBzdHIocGF5bG9hZF9kYXRhLmdldCgndGFzaycpIG9yIHBheWxvYWRfZGF0YS5nZXQoJ29iamVjdGl2ZScpIG9yIHBheWxvYWRfZGF0YS5nZXQoJ3Byb21wdCcpIG9yIGdvYWwpLnN0cmlwKCkKb2JqZWN0aXZlX3RleHQgPSBzdHIocGF5bG9hZF9kYXRhLmdldCgnb2JqZWN0aXZlJykgb3IgZ29hbCkuc3RyaXAoKQpjb25zdHJhaW50cyA9IHBheWxvYWRfZGF0YS5nZXQoJ2NvbnN0cmFpbnRzJykgaWYgaXNpbnN0YW5jZShwYXlsb2FkX2RhdGEuZ2V0KCdjb25zdHJhaW50cycpLCBsaXN0KSBlbHNlIFtdCm1lc3NhZ2VzID0gcGF5bG9hZF9kYXRhLmdldCgnbWVzc2FnZXMnKSBpZiBpc2luc3RhbmNlKHBheWxvYWRfZGF0YS5nZXQoJ21lc3NhZ2VzJyksIGxpc3QpIGVsc2UgW10KY2FuZGlkYXRlX291dHB1dHMgPSBwYXlsb2FkX2RhdGEuZ2V0KCdjYW5kaWRhdGVfb3V0cHV0cycpIGlmIGlzaW5zdGFuY2UocGF5bG9hZF9kYXRhLmdldCgnY2FuZGlkYXRlX291dHB1dHMnKSwgbGlzdCkgZWxzZSBbXQpzb3VyY2Vfbm90ZXMgPSBwYXlsb2FkX2RhdGEuZ2V0KCdzb3VyY2Vfbm90ZXMnKSBpZiBpc2luc3RhbmNlKHBheWxvYWRfZGF0YS5nZXQoJ3NvdXJjZV9ub3RlcycpLCBsaXN0KSBlbHNlIFtdCnJlc3BvbnNlX3RleHQgPSBzdHIocGF5bG9hZF9kYXRhLmdldCgncmVzcG9uc2UnKSBvciBwYXlsb2FkX2RhdGEuZ2V0KCdhbnN3ZXInKSBvciAoY2FuZGlkYXRlX291dHB1dHNbMF0gaWYgY2FuZGlkYXRlX291dHB1dHMgZWxzZSAnJykpLnN0cmlwKCkKcnVicmljID0gcGF5bG9hZF9kYXRhLmdldCgncnVicmljJykgaWYgaXNpbnN0YW5jZShwYXlsb2FkX2RhdGEuZ2V0KCdydWJyaWMnKSwgbGlzdCkgZWxzZSBbXQpyZXF1aXJlbWVudHMgPSBydWJyaWMgb3IgY29uc3RyYWludHMgb3IgW29iamVjdGl2ZV90ZXh0LCBkZWZfdGV4dF0KbWlzc2luZ19yZXF1aXJlbWVudHMgPSBbXQpjb3ZlcmVkX3JlcXVpcmVtZW50cyA9IFtdCmxvd2VyX3Jlc3BvbnNlID0gcmVzcG9uc2VfdGV4dC5sb3dlcigpCmZvciByZXF1aXJlbWVudCBpbiByZXF1aXJlbWVudHM6CiAgICByZXEgPSBzdHIocmVxdWlyZW1lbnQpLnN0cmlwKCkKICAgIGtleXdvcmRzID0gW3dvcmQuc3RyaXAoJy4sOjshPycpLmxvd2VyKCkgZm9yIHdvcmQgaW4gcmVxLnNwbGl0KCkgaWYgbGVuKHdvcmQuc3RyaXAoJy4sOjshPycpKSA+IDRdWzo1XQogICAgaGl0cyA9IFt3b3JkIGZvciB3b3JkIGluIGtleXdvcmRzIGlmIHdvcmQgaW4gbG93ZXJfcmVzcG9uc2VdCiAgICBpZiBoaXRzOgogICAgICAgIGNvdmVyZWRfcmVxdWlyZW1lbnRzLmFwcGVuZCh7J3JlcXVpcmVtZW50JzogcmVxLCAnbWF0Y2hlZF90ZXJtcyc6IGhpdHN9KQogICAgZWxzZToKICAgICAgICBtaXNzaW5nX3JlcXVpcmVtZW50cy5hcHBlbmQocmVxKQpjbGFyaXR5X2ZsYWdzID0gW10KaWYgbGVuKHJlc3BvbnNlX3RleHQuc3BsaXQoKSkgPCAyMDoKICAgIGNsYXJpdHlfZmxhZ3MuYXBwZW5kKCdyZXNwb25zZSBpcyB2ZXJ5IHNob3J0JykKaWYgYW55KG1hcmtlciBpbiBsb3dlcl9yZXNwb25zZSBmb3IgbWFya2VyIGluIFsnbWF5YmUnLCAncHJvYmFibHknLCAnaSB0aGluaycsICdub3Qgc3VyZSddKToKICAgIGNsYXJpdHlfZmxhZ3MuYXBwZW5kKCd1bmNlcnRhaW50eSBpcyBub3QgcmVzb2x2ZWQnKQppZiAndGVzdCcgbm90IGluIGxvd2VyX3Jlc3BvbnNlIGFuZCAndmVyaWZ5JyBub3QgaW4gbG93ZXJfcmVzcG9uc2UgYW5kICdjaGVjaycgbm90IGluIGxvd2VyX3Jlc3BvbnNlOgogICAgY2xhcml0eV9mbGFncy5hcHBlbmQoJ3ZlcmlmaWNhdGlvbiBzdGVwIGlzIG1pc3NpbmcnKQpjb3ZlcmFnZSA9IGxlbihjb3ZlcmVkX3JlcXVpcmVtZW50cykgLyBtYXgoMSwgbGVuKHJlcXVpcmVtZW50cykpCnF1YWxpdHlfc2NvcmUgPSByb3VuZChtaW4oMC45NSwgMC4zNSArIDAuNDUgKiBjb3ZlcmFnZSArICgwLjEyIGlmIG5vdCBjbGFyaXR5X2ZsYWdzIGVsc2UgMCkpLCAyKQppbXByb3ZlbWVudF9jaGVja2xpc3QgPSBbXQpmb3IgcmVxIGluIG1pc3NpbmdfcmVxdWlyZW1lbnRzWzo1XToKICAgIGltcHJvdmVtZW50X2NoZWNrbGlzdC5hcHBlbmQoJ0FkZHJlc3MgcmVxdWlyZW1lbnQ6ICcgKyByZXFbOjE0MF0pCmZvciBmbGFnIGluIGNsYXJpdHlfZmxhZ3M6CiAgICBpbXByb3ZlbWVudF9jaGVja2xpc3QuYXBwZW5kKCdGaXggcXVhbGl0eSBpc3N1ZTogJyArIGZsYWcpCmlmIG5vdCBpbXByb3ZlbWVudF9jaGVja2xpc3Q6CiAgICBpbXByb3ZlbWVudF9jaGVja2xpc3QuYXBwZW5kKCdQcmVzZXJ2ZSBjb3ZlcmVkIHJlcXVpcmVtZW50cyBhbmQgYWRkIGV2aWRlbmNlIGZvciB0aGUgc3Ryb25nZXN0IGNsYWltLicpCnJlc3VsdFsnc3VtbWFyeSddID0gcGx1Z2luX25hbWUgKyAnOiBzY29yZWQgb3V0cHV0IHF1YWxpdHkgYXQgJyArIHN0cihxdWFsaXR5X3Njb3JlKSArICcgZm9yICcgKyBkZWZfdGV4dFs6MTMwXSArICcuJwpyZXN1bHRbJ3ByaW1hcnlfaW5zaWdodHMnXSA9IFsKICAgIHsndGl0bGUnOiAnQ292ZXJlZCByZXF1aXJlbWVudHMnLCAnZGV0YWlsJzogY292ZXJlZF9yZXF1aXJlbWVudHNbOjZdfSwKICAgIHsndGl0bGUnOiAnTWlzc2luZyByZXF1aXJlbWVudHMnLCAnZGV0YWlsJzogbWlzc2luZ19yZXF1aXJlbWVudHNbOjZdfSwKICAgIHsndGl0bGUnOiAnQ2xhcml0eSBmbGFncycsICdkZXRhaWwnOiBjbGFyaXR5X2ZsYWdzIG9yICdObyBtYWpvciBjbGFyaXR5IGZsYWdzLid9LApdCnJlc3VsdFsncmVjb21tZW5kZWRfYWN0aW9ucyddID0gW3snYWN0aW9uJzogaXRlbX0gZm9yIGl0ZW0gaW4gaW1wcm92ZW1lbnRfY2hlY2tsaXN0Wzo2XV0KcmVzdWx0WydzY29yZXMnXSA9IHsnY29uZmlkZW5jZSc6IHJvdW5kKDAuNDUgKyBtaW4oMC40LCAwLjA4ICogbGVuKHJlcXVpcmVtZW50cykpLCAyKSwgJ3F1YWxpdHknOiBxdWFsaXR5X3Njb3JlLCAnY292ZXJhZ2UnOiByb3VuZChjb3ZlcmFnZSwgMiksICdyaXNrJzogcm91bmQoMC4xOCArIDAuMSAqIGxlbihtaXNzaW5nX3JlcXVpcmVtZW50c1s6NF0pICsgMC4wNSAqIGxlbihjbGFyaXR5X2ZsYWdzKSwgMil9CnJlc3VsdFsnZGV0YWlscyddID0geydjb3ZlcmVkX3JlcXVpcmVtZW50cyc6IGNvdmVyZWRfcmVxdWlyZW1lbnRzLCAnbWlzc2luZ19yZXF1aXJlbWVudHMnOiBtaXNzaW5nX3JlcXVpcmVtZW50cywgJ2NsYXJpdHlfZmxhZ3MnOiBjbGFyaXR5X2ZsYWdzLCAnaW1wcm92ZW1lbnRfY2hlY2tsaXN0JzogaW1wcm92ZW1lbnRfY2hlY2tsaXN0LCAnbWlzc2luZ19pbnB1dHMnOiBbJ3Jlc3BvbnNlIG9yIGNhbmRpZGF0ZV9vdXRwdXRzJ10gaWYgbm90IHJlc3BvbnNlX3RleHQgZWxzZSBbXX0KcmVzdWx0WydkZXRhaWxzJ11bJ3VzZV9jYXNlcyddID0gdXNlX2Nhc2VzCnJlc3VsdFsnZGV0YWlscyddWydnZW5lcmF0aW9uX25vdGUnXSA9IGdlbmVyYXRpb25fbm90ZQpyZXN1bHRbJ2RldGFpbHMnXVsnY2FwYWJpbGl0eV90eXBlJ10gPSBjYXBhYmlsaXR5X3R5cGUKcmVzdWx0WydkZXRhaWxzJ11bJ2xvZ2ljX3Byb2ZpbGVfaWQnXSA9IGxvZ2ljX3Byb2ZpbGVfaWQKcmVzdWx0WydkZXRhaWxzJ11bJ3BheWxvYWRfd2FybmluZ3MnXSA9IHBheWxvYWRfd2FybmluZ3MKcmVzdWx0Wydwcm9ncmVzc19zdGF0ZSddID0gewogICAgJ2N1cnJlbnRfc3RhZ2UnOiBsb2dpY19wcm9maWxlX2lkLAogICAgJ25leHRfc3RlcCc6IGltcHJvdmVtZW50X2NoZWNrbGlzdFswXSBpZiBpbXByb3ZlbWVudF9jaGVja2xpc3QgZWxzZSAnS2VlcCB0aGUgb3V0cHV0IGFzLWlzLicsCiAgICAnYmxvY2tlcnMnOiByZXN1bHRbJ2RldGFpbHMnXS5nZXQoJ21pc3NpbmdfaW5wdXRzJywgW10pWzo0XSwKICAgICdkb25lX3NpZ25hbHMnOiBbJ2NhcGFiaWxpdHlfc3BlY2lmaWNfYW5hbHlzaXNfY29tcGxldGUnLCBsb2dpY19wcm9maWxlX2lkXSwKfQpyZXN1bHRbJ3VzZXJfZXhwZXJpZW5jZSddID0gewogICAgJ3BsYWluX2xhbmd1YWdlX3Rha2Vhd2F5JzogcmVzdWx0WydzdW1tYXJ5J10sCiAgICAnYmVnaW5uZXJfdGlwJzogJ1VzZSB0aGUgZmlyc3QgcmVjb21tZW5kYXRpb24gYXMgdGhlIG5leHQgY29uY3JldGUgc3RlcC4nLAogICAgJ3Bvd2VyX3VzZXJfdGlwJzogJ1Bhc3MgZGV0YWlscyBhbmQgc2NvcmVzIGludG8gdGhlIG5leHQgQUkgY2FwYWJpbGl0eSBwbHVnaW4uJywKICAgICdpbnRlcmFjdGlvbl9zdWdnZXN0aW9ucyc6IFtpdGVtLmdldCgnYWN0aW9uJywgc3RyKGl0ZW0pKSBmb3IgaXRlbSBpbiByZXN1bHQuZ2V0KCdyZWNvbW1lbmRlZF9hY3Rpb25zJywgW10pWzozXV0sCn0KcmVzdWx0WydmdW5fbW9kZSddID0gewogICAgJ2NoYWxsZW5nZV9sYWJlbCc6ICdDYXBhYmlsaXR5IFJ1bicsCiAgICAnc2NvcmVfYmFkZ2UnOiAnU3Ryb25nIFNpZ25hbCcgaWYgcmVzdWx0LmdldCgnc2NvcmVzJywge30pLmdldCgnY29uZmlkZW5jZScsIDApID49IDAuNjUgZWxzZSAnTmVlZHMgQ29udGV4dCcsCiAgICAnbWljcm9jb3B5JzogJ1RoZSByZXN1bHQgaXMgc3RydWN0dXJlZCBzbyBhbm90aGVyIGFnZW50IGNhbiBwaWNrIGl0IHVwIGNsZWFubHkuJywKICAgICdvcHRpb25hbF9uZXh0X2NoYWxsZW5nZSc6IGltcHJvdmVtZW50X2NoZWNrbGlzdFswXSBpZiBpbXByb3ZlbWVudF9jaGVja2xpc3QgZWxzZSAnS2VlcCB0aGUgb3V0cHV0IGFzLWlzLicsCn0='
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
