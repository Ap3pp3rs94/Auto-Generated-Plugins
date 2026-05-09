from __future__ import annotations

"""
Auto-generated Francis plugin module.

THIS FILE IS GENERATED. Manual edits may be overwritten by the factory.

Plugin: AI Hallucination Risk Auditor
Slug: ai_hallucination_risk_auditor
"""

from typing import Any, Dict, Optional

__all__ = ["invoke", "_run_core_logic", "SkillContext"]

# ---------------------------------------------------------------------------
# Plugin metadata (used by Station C, registry, and tooling)
# ---------------------------------------------------------------------------

_PLUGIN_NAME: str = 'AI Hallucination Risk Auditor'
_PLUGIN_SLUG: str = 'ai_hallucination_risk_auditor'
_PLUGIN_CATEGORY: str = 'ai_evaluation'
_PLUGIN_VERSION: str = '0.1.0'
_PLUGIN_GOAL: str = 'Inspect AI-generated claims and flag unsupported, risky, or source-sensitive statements.'
_PLUGIN_TAGS = ['ai', 'hallucination', 'risk', 'verification', 'autonomous_factory', 'ai_progress', 'phase_1']
_PLUGIN_OWNER_ID = 'francis-factory'
_PLUGIN_CAPABILITY_TYPE = 'scoring'
_PLUGIN_INTENDED_DOMAIN = 'AI reliability, hallucination detection, and factual risk'
_PLUGIN_USE_CASES = ['Identify claims that need citations or external verification.', 'Classify risk by domain such as legal, medical, financial, or technical.', 'Suggest safer rewrites for uncertain claims.', 'Show a compact progress state for this AI capability during baseline capability.', 'Return user-facing guidance that is useful, concise, and safe to act on.', 'Avoid duplicating existing AI plugin behavior; identify what is unique about this capability.']
_PLUGIN_RESULT_SCHEMA_VERSION: str = '1.0.0'

# Lightweight manifest for discovery/registry.
_PLUGIN_MANIFEST = {'name': 'AI Hallucination Risk Auditor', 'slug': 'ai_hallucination_risk_auditor', 'goal': 'Inspect AI-generated claims and flag unsupported, risky, or source-sensitive statements.', 'category': 'ai_evaluation', 'tags': ['ai', 'hallucination', 'risk', 'verification', 'autonomous_factory', 'ai_progress', 'phase_1'], 'version': '0.1.0', 'capability_type': 'scoring', 'intended_domain': 'AI reliability, hallucination detection, and factual risk', 'owner_id': 'francis-factory', 'use_cases': ['Identify claims that need citations or external verification.', 'Classify risk by domain such as legal, medical, financial, or technical.', 'Suggest safer rewrites for uncertain claims.', 'Show a compact progress state for this AI capability during baseline capability.', 'Return user-facing guidance that is useful, concise, and safe to act on.', 'Avoid duplicating existing AI plugin behavior; identify what is unique about this capability.'], 'primary_use_case': 'Identify claims that need citations or external verification.', 'problem_statement': 'Francis needs a focused AI plugin for AI reliability, hallucination detection, and factual risk. The plugin must turn messy user notes, model outputs, traces, or workflow state into structured, actionable AI assistance. It should improve autonomous progress by making the next step obvious, reducing duplicated work, and exposing risks before they become failures. The plugin must stay deterministic, avoid hidden external side effects, and make its reasoning inspectable through concise details and scores.', 'primary_inputs': 'A payload dict that may contain task, objective, prompt, conversation, artifacts, candidate_outputs, traces, rubric, constraints, user_level, current_plan, completed_steps, blocked_steps, source_notes, and optional customer_config.', 'primary_outputs': 'A normalized result dict with summary, primary_insights, recommended_actions, scores, details, progress_state, user_experience, fun_mode, and machine-readable diagnostics.', 'constraints': 'Do not execute tools, browse, mutate files, call external APIs, or claim facts not present in the payload. Prefer deterministic analysis. If data is missing, say what is missing and return a useful fallback. Keep recommendations concrete. Avoid creating a capability that duplicates another AI roadmap plugin.', 'example_use_cases': ['A user asks Francis to improve an AI workflow related to AI reliability, hallucination detection, and factual risk.', 'A long-running autonomous run needs a checkpoint summary and the next best action.', 'An operator wants a scorecard that separates hard failures from polish improvements.', 'A beginner wants the result explained in plain language without losing technical accuracy.', 'A power user wants structured JSON they can pipe into another agent or dashboard.'], 'io_contract': "Input: payload is a dict. Important optional keys include 'task', 'objective', 'prompt', 'conversation', 'messages', 'candidate_outputs', 'trace', 'rubric', 'constraints', 'progress', 'current_plan', 'completed_steps', 'blocked_steps', 'user_level', and 'customer_config'. Output: return a dict containing summary: str, primary_insights: list, recommended_actions: list, scores: dict with confidence and usefulness, details: dict, progress_state: dict with current_stage/next_step/blockers, user_experience: dict with plain_language_takeaway and interaction_suggestions, and fun_mode: dict with optional challenge_label, score_badge, and celebratory_microcopy. Fun fields must never replace the serious recommendation.", 'schema_version': '1.0.0', 'family_key': 'ai_evaluation::ai hallucination risk auditor', 'is_generic_name': False}

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
    _profile_body_b64 = 'cGx1Z2luX25hbWUgPSAnQUkgSGFsbHVjaW5hdGlvbiBSaXNrIEF1ZGl0b3InCmdvYWwgPSAnSW5zcGVjdCBBSS1nZW5lcmF0ZWQgY2xhaW1zIGFuZCBmbGFnIHVuc3VwcG9ydGVkLCByaXNreSwgb3Igc291cmNlLXNlbnNpdGl2ZSBzdGF0ZW1lbnRzLicKZG9tYWluID0gJ0FJIHJlbGlhYmlsaXR5LCBoYWxsdWNpbmF0aW9uIGRldGVjdGlvbiwgYW5kIGZhY3R1YWwgcmlzaycKY2FwYWJpbGl0eV90eXBlID0gJ3Njb3JpbmcnCmxvZ2ljX3Byb2ZpbGVfaWQgPSAnaGFsbHVjaW5hdGlvbl9yaXNrX2F1ZGl0b3JfcHJvZmlsZScKZ2VuZXJhdGlvbl9ub3RlID0gJ2NhcGFiaWxpdHktc3BlY2lmaWMgcHJvZmlsZSByZXBsYWNlbWVudCBmb3IgZ2VuZXJpYyBzZW1hbnRpYyByZXBhaXInCnVzZV9jYXNlcyA9IFsnSWRlbnRpZnkgY2xhaW1zIHRoYXQgbmVlZCBjaXRhdGlvbnMgb3IgZXh0ZXJuYWwgdmVyaWZpY2F0aW9uLicsICdDbGFzc2lmeSByaXNrIGJ5IGRvbWFpbiBzdWNoIGFzIGxlZ2FsLCBtZWRpY2FsLCBmaW5hbmNpYWwsIG9yIHRlY2huaWNhbC4nLCAnU3VnZ2VzdCBzYWZlciByZXdyaXRlcyBmb3IgdW5jZXJ0YWluIGNsYWltcy4nLCAnU2hvdyBhIGNvbXBhY3QgcHJvZ3Jlc3Mgc3RhdGUgZm9yIHRoaXMgQUkgY2FwYWJpbGl0eSBkdXJpbmcgYmFzZWxpbmUgY2FwYWJpbGl0eS4nLCAnUmV0dXJuIHVzZXItZmFjaW5nIGd1aWRhbmNlIHRoYXQgaXMgdXNlZnVsLCBjb25jaXNlLCBhbmQgc2FmZSB0byBhY3Qgb24uJywgJ0F2b2lkIGR1cGxpY2F0aW5nIGV4aXN0aW5nIEFJIHBsdWdpbiBiZWhhdmlvcjsgaWRlbnRpZnkgd2hhdCBpcyB1bmlxdWUgYWJvdXQgdGhpcyBjYXBhYmlsaXR5LiddCnBheWxvYWRfZGF0YSA9IHBheWxvYWQgaWYgaXNpbnN0YW5jZShwYXlsb2FkLCBkaWN0KSBlbHNlIHt9CnBheWxvYWRfd2FybmluZ3MgPSBbXSBpZiBpc2luc3RhbmNlKHBheWxvYWQsIGRpY3QpIGVsc2UgWydwYXlsb2FkIHdhcyBub3QgYSBkaWN0OyB1c2luZyBlbXB0eSBwYXlsb2FkJ10KZGVmX3RleHQgPSBzdHIocGF5bG9hZF9kYXRhLmdldCgndGFzaycpIG9yIHBheWxvYWRfZGF0YS5nZXQoJ29iamVjdGl2ZScpIG9yIHBheWxvYWRfZGF0YS5nZXQoJ3Byb21wdCcpIG9yIGdvYWwpLnN0cmlwKCkKb2JqZWN0aXZlX3RleHQgPSBzdHIocGF5bG9hZF9kYXRhLmdldCgnb2JqZWN0aXZlJykgb3IgZ29hbCkuc3RyaXAoKQpjb25zdHJhaW50cyA9IHBheWxvYWRfZGF0YS5nZXQoJ2NvbnN0cmFpbnRzJykgaWYgaXNpbnN0YW5jZShwYXlsb2FkX2RhdGEuZ2V0KCdjb25zdHJhaW50cycpLCBsaXN0KSBlbHNlIFtdCm1lc3NhZ2VzID0gcGF5bG9hZF9kYXRhLmdldCgnbWVzc2FnZXMnKSBpZiBpc2luc3RhbmNlKHBheWxvYWRfZGF0YS5nZXQoJ21lc3NhZ2VzJyksIGxpc3QpIGVsc2UgW10KY2FuZGlkYXRlX291dHB1dHMgPSBwYXlsb2FkX2RhdGEuZ2V0KCdjYW5kaWRhdGVfb3V0cHV0cycpIGlmIGlzaW5zdGFuY2UocGF5bG9hZF9kYXRhLmdldCgnY2FuZGlkYXRlX291dHB1dHMnKSwgbGlzdCkgZWxzZSBbXQpzb3VyY2Vfbm90ZXMgPSBwYXlsb2FkX2RhdGEuZ2V0KCdzb3VyY2Vfbm90ZXMnKSBpZiBpc2luc3RhbmNlKHBheWxvYWRfZGF0YS5nZXQoJ3NvdXJjZV9ub3RlcycpLCBsaXN0KSBlbHNlIFtdCnRleHQgPSBzdHIocGF5bG9hZF9kYXRhLmdldCgncmVzcG9uc2UnKSBvciBwYXlsb2FkX2RhdGEuZ2V0KCdhbnN3ZXInKSBvciAoY2FuZGlkYXRlX291dHB1dHNbMF0gaWYgY2FuZGlkYXRlX291dHB1dHMgZWxzZSAnJykpLnN0cmlwKCkKc2VudGVuY2VzID0gW3BhcnQuc3RyaXAoKSBmb3IgcGFydCBpbiB0ZXh0LnJlcGxhY2UoJ1xuJywgJy4gJykuc3BsaXQoJy4nKSBpZiBwYXJ0LnN0cmlwKCldCnJpc2tfdGVybXMgPSBbJ2Fsd2F5cycsICduZXZlcicsICdndWFyYW50ZWVkJywgJ2xhdGVzdCcsICdjdXJyZW50JywgJ2xhdycsICdsZWdhbCcsICdtZWRpY2FsJywgJ2ZpbmFuY2lhbCcsICdwcmljZScsICdzdHVkeScsICdyZXNlYXJjaCcsICdzdGF0aXN0aWMnLCAncGVyY2VudCddCmNsYWltcyA9IFtdCmZvciBzZW50ZW5jZSBpbiBzZW50ZW5jZXM6CiAgICBsb3dlciA9IHNlbnRlbmNlLmxvd2VyKCkKICAgIHNpZ25hbHMgPSBbdGVybSBmb3IgdGVybSBpbiByaXNrX3Rlcm1zIGlmIHRlcm0gaW4gbG93ZXJdCiAgICBoYXNfY2l0YXRpb24gPSAnaHR0cCcgaW4gbG93ZXIgb3IgJ1snIGluIHNlbnRlbmNlIG9yICdzb3VyY2UnIGluIGxvd2VyIG9yICdjaXRhdGlvbicgaW4gbG93ZXIKICAgIGlmIHNpZ25hbHMgb3IgYW55KGNoLmlzZGlnaXQoKSBmb3IgY2ggaW4gc2VudGVuY2UpOgogICAgICAgIGNsYWltcy5hcHBlbmQoeydjbGFpbSc6IHNlbnRlbmNlWzoyMjBdLCAncmlza19zaWduYWxzJzogc2lnbmFscywgJ2hhc19jaXRhdGlvbic6IGhhc19jaXRhdGlvbiwgJ25lZWRzX3ZlcmlmaWNhdGlvbic6IGJvb2woc2lnbmFscykgYW5kIG5vdCBoYXNfY2l0YXRpb259KQpoaWdoX3Jpc2sgPSBbY2xhaW0gZm9yIGNsYWltIGluIGNsYWltcyBpZiBjbGFpbVsnbmVlZHNfdmVyaWZpY2F0aW9uJ11dCnNhZmVyX3Jld3JpdGVzID0gW10KZm9yIGNsYWltIGluIGhpZ2hfcmlza1s6NV06CiAgICBzYWZlcl9yZXdyaXRlcy5hcHBlbmQoeydvcmlnaW5hbCc6IGNsYWltWydjbGFpbSddLCAncmV3cml0ZSc6ICdWZXJpZnkgYmVmb3JlIHJlbHlpbmcgb24gdGhpcyBjbGFpbTogJyArIGNsYWltWydjbGFpbSddfSkKcmlza19zY29yZSA9IHJvdW5kKG1pbigwLjk1LCAwLjE4ICsgMC4xMiAqIGxlbihoaWdoX3Jpc2spICsgMC4wNCAqIGxlbihjbGFpbXMpKSwgMikKcmVzdWx0WydzdW1tYXJ5J10gPSBwbHVnaW5fbmFtZSArICc6IGZvdW5kICcgKyBzdHIobGVuKGhpZ2hfcmlzaykpICsgJyBjbGFpbShzKSBuZWVkaW5nIHZlcmlmaWNhdGlvbi4nCnJlc3VsdFsncHJpbWFyeV9pbnNpZ2h0cyddID0gWwogICAgeyd0aXRsZSc6ICdDbGFpbXMgbmVlZGluZyB2ZXJpZmljYXRpb24nLCAnZGV0YWlsJzogaGlnaF9yaXNrWzo2XX0sCiAgICB7J3RpdGxlJzogJ0NpdGF0aW9uIGNvdmVyYWdlJywgJ2RldGFpbCc6IHN0cihsZW4oW2MgZm9yIGMgaW4gY2xhaW1zIGlmIGNbJ2hhc19jaXRhdGlvbiddXSkpICsgJyBjaXRlZCBvZiAnICsgc3RyKGxlbihjbGFpbXMpKSArICcgZmxhZ2dlZCBjbGFpbXMnfSwKICAgIHsndGl0bGUnOiAnUmlzayBkb21haW5zJywgJ2RldGFpbCc6IHNvcnRlZChzZXQodGVybSBmb3IgY2xhaW0gaW4gY2xhaW1zIGZvciB0ZXJtIGluIGNsYWltWydyaXNrX3NpZ25hbHMnXSkpfSwKXQpyZXN1bHRbJ3JlY29tbWVuZGVkX2FjdGlvbnMnXSA9IFsKICAgIHsnYWN0aW9uJzogJ1ZlcmlmeSBjbGFpbScsICdjbGFpbSc6IGNsYWltWydjbGFpbSddLCAnc2lnbmFscyc6IGNsYWltWydyaXNrX3NpZ25hbHMnXX0gZm9yIGNsYWltIGluIGhpZ2hfcmlza1s6NV0KXQppZiBzYWZlcl9yZXdyaXRlczoKICAgIHJlc3VsdFsncmVjb21tZW5kZWRfYWN0aW9ucyddLmFwcGVuZCh7J2FjdGlvbic6ICdVc2Ugc2FmZXIgcmV3cml0ZXMnLCAncmV3cml0ZXMnOiBzYWZlcl9yZXdyaXRlc30pCnJlc3VsdFsnc2NvcmVzJ10gPSB7J2NvbmZpZGVuY2UnOiByb3VuZCgwLjUgKyBtaW4oMC4zNSwgMC4wNiAqIGxlbihzZW50ZW5jZXMpKSwgMiksICdoYWxsdWNpbmF0aW9uX3Jpc2snOiByaXNrX3Njb3JlLCAnY2l0YXRpb25fY292ZXJhZ2UnOiByb3VuZChsZW4oW2MgZm9yIGMgaW4gY2xhaW1zIGlmIGNbJ2hhc19jaXRhdGlvbiddXSkgLyBtYXgoMSwgbGVuKGNsYWltcykpLCAyKSwgJ3Jpc2snOiByaXNrX3Njb3JlfQpyZXN1bHRbJ2RldGFpbHMnXSA9IHsnY2xhaW1zJzogY2xhaW1zLCAnaGlnaF9yaXNrX2NsYWltcyc6IGhpZ2hfcmlzaywgJ3NhZmVyX3Jld3JpdGVzJzogc2FmZXJfcmV3cml0ZXMsICdtaXNzaW5nX2lucHV0cyc6IFsncmVzcG9uc2Ugb3IgY2FuZGlkYXRlX291dHB1dHMnXSBpZiBub3QgdGV4dCBlbHNlIFtdfQpyZXN1bHRbJ2RldGFpbHMnXVsndXNlX2Nhc2VzJ10gPSB1c2VfY2FzZXMKcmVzdWx0WydkZXRhaWxzJ11bJ2dlbmVyYXRpb25fbm90ZSddID0gZ2VuZXJhdGlvbl9ub3RlCnJlc3VsdFsnZGV0YWlscyddWydjYXBhYmlsaXR5X3R5cGUnXSA9IGNhcGFiaWxpdHlfdHlwZQpyZXN1bHRbJ2RldGFpbHMnXVsnbG9naWNfcHJvZmlsZV9pZCddID0gbG9naWNfcHJvZmlsZV9pZApyZXN1bHRbJ2RldGFpbHMnXVsncGF5bG9hZF93YXJuaW5ncyddID0gcGF5bG9hZF93YXJuaW5ncwpyZXN1bHRbJ3Byb2dyZXNzX3N0YXRlJ10gPSB7CiAgICAnY3VycmVudF9zdGFnZSc6IGxvZ2ljX3Byb2ZpbGVfaWQsCiAgICAnbmV4dF9zdGVwJzogJ1ZlcmlmeSB0aGUgaGlnaGVzdC1yaXNrIHVuY2l0ZWQgY2xhaW0uJywKICAgICdibG9ja2Vycyc6IHJlc3VsdFsnZGV0YWlscyddLmdldCgnbWlzc2luZ19pbnB1dHMnLCBbXSlbOjRdLAogICAgJ2RvbmVfc2lnbmFscyc6IFsnY2FwYWJpbGl0eV9zcGVjaWZpY19hbmFseXNpc19jb21wbGV0ZScsIGxvZ2ljX3Byb2ZpbGVfaWRdLAp9CnJlc3VsdFsndXNlcl9leHBlcmllbmNlJ10gPSB7CiAgICAncGxhaW5fbGFuZ3VhZ2VfdGFrZWF3YXknOiByZXN1bHRbJ3N1bW1hcnknXSwKICAgICdiZWdpbm5lcl90aXAnOiAnVXNlIHRoZSBmaXJzdCByZWNvbW1lbmRhdGlvbiBhcyB0aGUgbmV4dCBjb25jcmV0ZSBzdGVwLicsCiAgICAncG93ZXJfdXNlcl90aXAnOiAnUGFzcyBkZXRhaWxzIGFuZCBzY29yZXMgaW50byB0aGUgbmV4dCBBSSBjYXBhYmlsaXR5IHBsdWdpbi4nLAogICAgJ2ludGVyYWN0aW9uX3N1Z2dlc3Rpb25zJzogW2l0ZW0uZ2V0KCdhY3Rpb24nLCBzdHIoaXRlbSkpIGZvciBpdGVtIGluIHJlc3VsdC5nZXQoJ3JlY29tbWVuZGVkX2FjdGlvbnMnLCBbXSlbOjNdXSwKfQpyZXN1bHRbJ2Z1bl9tb2RlJ10gPSB7CiAgICAnY2hhbGxlbmdlX2xhYmVsJzogJ0NhcGFiaWxpdHkgUnVuJywKICAgICdzY29yZV9iYWRnZSc6ICdTdHJvbmcgU2lnbmFsJyBpZiByZXN1bHQuZ2V0KCdzY29yZXMnLCB7fSkuZ2V0KCdjb25maWRlbmNlJywgMCkgPj0gMC42NSBlbHNlICdOZWVkcyBDb250ZXh0JywKICAgICdtaWNyb2NvcHknOiAnVGhlIHJlc3VsdCBpcyBzdHJ1Y3R1cmVkIHNvIGFub3RoZXIgYWdlbnQgY2FuIHBpY2sgaXQgdXAgY2xlYW5seS4nLAogICAgJ29wdGlvbmFsX25leHRfY2hhbGxlbmdlJzogJ1ZlcmlmeSB0aGUgaGlnaGVzdC1yaXNrIHVuY2l0ZWQgY2xhaW0uJywKfQ=='
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
