from __future__ import annotations

"""
Auto-generated Francis plugin module.

THIS FILE IS GENERATED. Manual edits may be overwritten by the factory.

Plugin: AI Agent Task Planner
Slug: ai_agent_task_planner
"""

from typing import Any, Dict, Optional

__all__ = ["invoke", "_run_core_logic", "SkillContext"]

# ---------------------------------------------------------------------------
# Plugin metadata (used by Station C, registry, and tooling)
# ---------------------------------------------------------------------------

_PLUGIN_NAME: str = 'AI Agent Task Planner'
_PLUGIN_SLUG: str = 'ai_agent_task_planner'
_PLUGIN_CATEGORY: str = 'ai_agents'
_PLUGIN_VERSION: str = '0.1.0'
_PLUGIN_GOAL: str = 'Turn a user objective into a sequenced AI-agent work plan with checkpoints and handoffs.'
_PLUGIN_TAGS = ['ai', 'agents', 'planning', 'workflow', 'autonomous_factory', 'ai_progress', 'phase_1']
_PLUGIN_OWNER_ID = 'francis-factory'
_PLUGIN_CAPABILITY_TYPE = 'system_automation'
_PLUGIN_INTENDED_DOMAIN = 'AI agent planning and task decomposition'
_PLUGIN_USE_CASES = ['Break a complex AI task into ordered implementation, review, and verification steps.', 'Separate blocking work from parallelizable side tasks.', 'Recommend checkpoints that prevent agent drift or repeated work.', 'Show a compact progress state for this AI capability during baseline capability.', 'Return user-facing guidance that is useful, concise, and safe to act on.', 'Avoid duplicating existing AI plugin behavior; identify what is unique about this capability.']
_PLUGIN_RESULT_SCHEMA_VERSION: str = '1.0.0'

# Lightweight manifest for discovery/registry.
_PLUGIN_MANIFEST = {'name': 'AI Agent Task Planner', 'slug': 'ai_agent_task_planner', 'goal': 'Turn a user objective into a sequenced AI-agent work plan with checkpoints and handoffs.', 'category': 'ai_agents', 'tags': ['ai', 'agents', 'planning', 'workflow', 'autonomous_factory', 'ai_progress', 'phase_1'], 'version': '0.1.0', 'capability_type': 'system_automation', 'intended_domain': 'AI agent planning and task decomposition', 'owner_id': 'francis-factory', 'use_cases': ['Break a complex AI task into ordered implementation, review, and verification steps.', 'Separate blocking work from parallelizable side tasks.', 'Recommend checkpoints that prevent agent drift or repeated work.', 'Show a compact progress state for this AI capability during baseline capability.', 'Return user-facing guidance that is useful, concise, and safe to act on.', 'Avoid duplicating existing AI plugin behavior; identify what is unique about this capability.'], 'primary_use_case': 'Break a complex AI task into ordered implementation, review, and verification steps.', 'problem_statement': 'Francis needs a focused AI plugin for AI agent planning and task decomposition. The plugin must turn messy user notes, model outputs, traces, or workflow state into structured, actionable AI assistance. It should improve autonomous progress by making the next step obvious, reducing duplicated work, and exposing risks before they become failures. The plugin must stay deterministic, avoid hidden external side effects, and make its reasoning inspectable through concise details and scores.', 'primary_inputs': 'A payload dict that may contain task, objective, prompt, conversation, artifacts, candidate_outputs, traces, rubric, constraints, user_level, current_plan, completed_steps, blocked_steps, source_notes, and optional customer_config.', 'primary_outputs': 'A normalized result dict with summary, primary_insights, recommended_actions, scores, details, progress_state, user_experience, fun_mode, and machine-readable diagnostics.', 'constraints': 'Do not execute tools, browse, mutate files, call external APIs, or claim facts not present in the payload. Prefer deterministic analysis. If data is missing, say what is missing and return a useful fallback. Keep recommendations concrete. Avoid creating a capability that duplicates another AI roadmap plugin.', 'example_use_cases': ['A user asks Francis to improve an AI workflow related to AI agent planning and task decomposition.', 'A long-running autonomous run needs a checkpoint summary and the next best action.', 'An operator wants a scorecard that separates hard failures from polish improvements.', 'A beginner wants the result explained in plain language without losing technical accuracy.', 'A power user wants structured JSON they can pipe into another agent or dashboard.'], 'io_contract': "Input: payload is a dict. Important optional keys include 'task', 'objective', 'prompt', 'conversation', 'messages', 'candidate_outputs', 'trace', 'rubric', 'constraints', 'progress', 'current_plan', 'completed_steps', 'blocked_steps', 'user_level', and 'customer_config'. Output: return a dict containing summary: str, primary_insights: list, recommended_actions: list, scores: dict with confidence and usefulness, details: dict, progress_state: dict with current_stage/next_step/blockers, user_experience: dict with plain_language_takeaway and interaction_suggestions, and fun_mode: dict with optional challenge_label, score_badge, and celebratory_microcopy. Fun fields must never replace the serious recommendation.", 'schema_version': '1.0.0', 'family_key': 'ai_agents::ai agent task planner', 'is_generic_name': False}

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
    _profile_body_b64 = 'cGx1Z2luX25hbWUgPSAnQUkgQWdlbnQgVGFzayBQbGFubmVyJwpnb2FsID0gJ1R1cm4gYSB1c2VyIG9iamVjdGl2ZSBpbnRvIGEgc2VxdWVuY2VkIEFJLWFnZW50IHdvcmsgcGxhbiB3aXRoIGNoZWNrcG9pbnRzIGFuZCBoYW5kb2Zmcy4nCmRvbWFpbiA9ICdBSSBhZ2VudCBwbGFubmluZyBhbmQgdGFzayBkZWNvbXBvc2l0aW9uJwpjYXBhYmlsaXR5X3R5cGUgPSAnc3lzdGVtX2F1dG9tYXRpb24nCmxvZ2ljX3Byb2ZpbGVfaWQgPSAndGFza19wbGFubmVyX3Byb2ZpbGUnCmdlbmVyYXRpb25fbm90ZSA9ICdjYXBhYmlsaXR5LXNwZWNpZmljIHByb2ZpbGUgcmVwbGFjZW1lbnQgZm9yIGdlbmVyaWMgc2VtYW50aWMgcmVwYWlyJwp1c2VfY2FzZXMgPSBbJ0JyZWFrIGEgY29tcGxleCBBSSB0YXNrIGludG8gb3JkZXJlZCBpbXBsZW1lbnRhdGlvbiwgcmV2aWV3LCBhbmQgdmVyaWZpY2F0aW9uIHN0ZXBzLicsICdTZXBhcmF0ZSBibG9ja2luZyB3b3JrIGZyb20gcGFyYWxsZWxpemFibGUgc2lkZSB0YXNrcy4nLCAnUmVjb21tZW5kIGNoZWNrcG9pbnRzIHRoYXQgcHJldmVudCBhZ2VudCBkcmlmdCBvciByZXBlYXRlZCB3b3JrLicsICdTaG93IGEgY29tcGFjdCBwcm9ncmVzcyBzdGF0ZSBmb3IgdGhpcyBBSSBjYXBhYmlsaXR5IGR1cmluZyBiYXNlbGluZSBjYXBhYmlsaXR5LicsICdSZXR1cm4gdXNlci1mYWNpbmcgZ3VpZGFuY2UgdGhhdCBpcyB1c2VmdWwsIGNvbmNpc2UsIGFuZCBzYWZlIHRvIGFjdCBvbi4nLCAnQXZvaWQgZHVwbGljYXRpbmcgZXhpc3RpbmcgQUkgcGx1Z2luIGJlaGF2aW9yOyBpZGVudGlmeSB3aGF0IGlzIHVuaXF1ZSBhYm91dCB0aGlzIGNhcGFiaWxpdHkuJ10KcGF5bG9hZF9kYXRhID0gcGF5bG9hZCBpZiBpc2luc3RhbmNlKHBheWxvYWQsIGRpY3QpIGVsc2Uge30KcGF5bG9hZF93YXJuaW5ncyA9IFtdIGlmIGlzaW5zdGFuY2UocGF5bG9hZCwgZGljdCkgZWxzZSBbJ3BheWxvYWQgd2FzIG5vdCBhIGRpY3Q7IHVzaW5nIGVtcHR5IHBheWxvYWQnXQpkZWZfdGV4dCA9IHN0cihwYXlsb2FkX2RhdGEuZ2V0KCd0YXNrJykgb3IgcGF5bG9hZF9kYXRhLmdldCgnb2JqZWN0aXZlJykgb3IgcGF5bG9hZF9kYXRhLmdldCgncHJvbXB0Jykgb3IgZ29hbCkuc3RyaXAoKQpvYmplY3RpdmVfdGV4dCA9IHN0cihwYXlsb2FkX2RhdGEuZ2V0KCdvYmplY3RpdmUnKSBvciBnb2FsKS5zdHJpcCgpCmNvbnN0cmFpbnRzID0gcGF5bG9hZF9kYXRhLmdldCgnY29uc3RyYWludHMnKSBpZiBpc2luc3RhbmNlKHBheWxvYWRfZGF0YS5nZXQoJ2NvbnN0cmFpbnRzJyksIGxpc3QpIGVsc2UgW10KbWVzc2FnZXMgPSBwYXlsb2FkX2RhdGEuZ2V0KCdtZXNzYWdlcycpIGlmIGlzaW5zdGFuY2UocGF5bG9hZF9kYXRhLmdldCgnbWVzc2FnZXMnKSwgbGlzdCkgZWxzZSBbXQpjYW5kaWRhdGVfb3V0cHV0cyA9IHBheWxvYWRfZGF0YS5nZXQoJ2NhbmRpZGF0ZV9vdXRwdXRzJykgaWYgaXNpbnN0YW5jZShwYXlsb2FkX2RhdGEuZ2V0KCdjYW5kaWRhdGVfb3V0cHV0cycpLCBsaXN0KSBlbHNlIFtdCnNvdXJjZV9ub3RlcyA9IHBheWxvYWRfZGF0YS5nZXQoJ3NvdXJjZV9ub3RlcycpIGlmIGlzaW5zdGFuY2UocGF5bG9hZF9kYXRhLmdldCgnc291cmNlX25vdGVzJyksIGxpc3QpIGVsc2UgW10KY3VycmVudF9wbGFuID0gcGF5bG9hZF9kYXRhLmdldCgnY3VycmVudF9wbGFuJykgaWYgaXNpbnN0YW5jZShwYXlsb2FkX2RhdGEuZ2V0KCdjdXJyZW50X3BsYW4nKSwgbGlzdCkgZWxzZSBbXQpjb21wbGV0ZWRfc3RlcHMgPSBwYXlsb2FkX2RhdGEuZ2V0KCdjb21wbGV0ZWRfc3RlcHMnKSBpZiBpc2luc3RhbmNlKHBheWxvYWRfZGF0YS5nZXQoJ2NvbXBsZXRlZF9zdGVwcycpLCBsaXN0KSBlbHNlIFtdCmJsb2NrZWRfc3RlcHMgPSBwYXlsb2FkX2RhdGEuZ2V0KCdibG9ja2VkX3N0ZXBzJykgaWYgaXNpbnN0YW5jZShwYXlsb2FkX2RhdGEuZ2V0KCdibG9ja2VkX3N0ZXBzJyksIGxpc3QpIGVsc2UgW10KcGFyYWxsZWxfaGludHMgPSBbXQppZiAndGVzdCcgaW4gZGVmX3RleHQubG93ZXIoKSBvciAndmVyaWZ5JyBpbiBvYmplY3RpdmVfdGV4dC5sb3dlcigpOgogICAgcGFyYWxsZWxfaGludHMuYXBwZW5kKCdwcmVwYXJlIHZlcmlmaWNhdGlvbiB3aGlsZSBpbXBsZW1lbnRhdGlvbiBpcyBwbGFubmVkJykKaWYgJ2ZpbGUnIGluIGRlZl90ZXh0Lmxvd2VyKCkgb3IgJ2NvZGUnIGluIGRlZl90ZXh0Lmxvd2VyKCk6CiAgICBwYXJhbGxlbF9oaW50cy5hcHBlbmQoJ2luc3BlY3QgYWZmZWN0ZWQgZmlsZXMgYmVmb3JlIGVkaXRpbmcnKQpzZXF1ZW5jZWRfcGxhbiA9IFtdCmlmIG5vdCBvYmplY3RpdmVfdGV4dDoKICAgIHNlcXVlbmNlZF9wbGFuLmFwcGVuZCh7J3N0ZXAnOiAxLCAncGhhc2UnOiAnY2xhcmlmeScsICd0YXNrJzogJ0RlZmluZSB0aGUgb2JqZWN0aXZlIGFuZCBhY2NlcHRhbmNlIGNyaXRlcmlhLicsICdibG9ja2luZyc6IFRydWV9KQpzZXF1ZW5jZWRfcGxhbi5hcHBlbmQoeydzdGVwJzogbGVuKHNlcXVlbmNlZF9wbGFuKSArIDEsICdwaGFzZSc6ICdwbGFuJywgJ3Rhc2snOiAnQnJlYWsgd29yayBpbnRvIGltcGxlbWVudGF0aW9uLCByZXZpZXcsIGFuZCB2ZXJpZmljYXRpb24gY2hlY2twb2ludHMgZm9yICcgKyBkZWZfdGV4dFs6MTYwXSwgJ2Jsb2NraW5nJzogVHJ1ZX0pCnNlcXVlbmNlZF9wbGFuLmFwcGVuZCh7J3N0ZXAnOiBsZW4oc2VxdWVuY2VkX3BsYW4pICsgMSwgJ3BoYXNlJzogJ2V4ZWN1dGUnLCAndGFzayc6ICdDb21wbGV0ZSB0aGUgc21hbGxlc3QgcmV2ZXJzaWJsZSBpbXBsZW1lbnRhdGlvbiB1bml0LicsICdibG9ja2luZyc6IEZhbHNlfSkKc2VxdWVuY2VkX3BsYW4uYXBwZW5kKHsnc3RlcCc6IGxlbihzZXF1ZW5jZWRfcGxhbikgKyAxLCAncGhhc2UnOiAndmVyaWZ5JywgJ3Rhc2snOiAnUnVuIHRlc3RzIG9yIGV4cGxpY2l0IGNoZWNrcyB0aWVkIHRvICcgKyBvYmplY3RpdmVfdGV4dFs6MTQwXSwgJ2Jsb2NraW5nJzogVHJ1ZX0pCmhhbmRvZmZfcGFja2V0ID0gewogICAgJ29iamVjdGl2ZSc6IG9iamVjdGl2ZV90ZXh0LAogICAgJ2NvbXBsZXRlZF9zdGVwcyc6IGNvbXBsZXRlZF9zdGVwcywKICAgICdibG9ja2VkX3N0ZXBzJzogYmxvY2tlZF9zdGVwcywKICAgICdwYXJhbGxlbGl6YWJsZV93b3JrJzogcGFyYWxsZWxfaGludHMgb3IgWydkb2N1bWVudCBhc3N1bXB0aW9ucycsICdwcmVwYXJlIHZlcmlmaWNhdGlvbiBjaGVja2xpc3QnXSwKICAgICdpbnRlZ3JhdGlvbl9jaGVja3BvaW50JzogJ0NvbmZpcm0gY29tcGxldGVkIHdvcmssIGJsb2NrZXJzLCBjaGFuZ2VkIGZpbGVzLCBhbmQgdGVzdCBldmlkZW5jZSBiZWZvcmUgdGhlIG5leHQgYWdlbnQgc3RhcnRzLicsCn0KY292ZXJhZ2UgPSAwLjQ1ICsgKDAuMTIgaWYgb2JqZWN0aXZlX3RleHQgZWxzZSAwKSArICgwLjEgaWYgY3VycmVudF9wbGFuIGVsc2UgMCkgKyAoMC4xIGlmIGNvbXBsZXRlZF9zdGVwcyBlbHNlIDApICsgKDAuMDggaWYgYmxvY2tlZF9zdGVwcyBlbHNlIDApICsgbWluKDAuMSwgbGVuKGNvbnN0cmFpbnRzKSAqIDAuMDMpCnJlc3VsdFsnc3VtbWFyeSddID0gcGx1Z2luX25hbWUgKyAnOiBidWlsdCBhIHNlcXVlbmNlZCBBSS1hZ2VudCBwbGFuIHdpdGggY2hlY2twb2ludHMgZm9yICcgKyBkZWZfdGV4dFs6MTQwXSArICcuJwpyZXN1bHRbJ3ByaW1hcnlfaW5zaWdodHMnXSA9IFsKICAgIHsndGl0bGUnOiAnUGxhbiBjb3ZlcmFnZScsICdkZXRhaWwnOiAnRm91bmQgJWQgZXhpc3RpbmcgcGxhbiBzdGVwKHMpLCAlZCBjb21wbGV0ZWQgc3RlcChzKSwgYW5kICVkIGJsb2NrZXIocykuJyAlIChsZW4oY3VycmVudF9wbGFuKSwgbGVuKGNvbXBsZXRlZF9zdGVwcyksIGxlbihibG9ja2VkX3N0ZXBzKSl9LAogICAgeyd0aXRsZSc6ICdCbG9ja2luZyBwYXRoJywgJ2RldGFpbCc6IGJsb2NrZWRfc3RlcHNbMF0gaWYgYmxvY2tlZF9zdGVwcyBlbHNlICdObyBleHBsaWNpdCBibG9ja2VyIHdhcyBwcm92aWRlZC4nfSwKICAgIHsndGl0bGUnOiAnUGFyYWxsZWwgd29yaycsICdkZXRhaWwnOiBoYW5kb2ZmX3BhY2tldFsncGFyYWxsZWxpemFibGVfd29yayddfSwKXQpyZXN1bHRbJ3JlY29tbWVuZGVkX2FjdGlvbnMnXSA9IFsKICAgIHsnYWN0aW9uJzogaXRlbVsndGFzayddLCAncGhhc2UnOiBpdGVtWydwaGFzZSddLCAnYmxvY2tpbmcnOiBpdGVtWydibG9ja2luZyddfSBmb3IgaXRlbSBpbiBzZXF1ZW5jZWRfcGxhbgpdCnJlc3VsdFsnc2NvcmVzJ10gPSB7J2NvbmZpZGVuY2UnOiByb3VuZChtaW4oMC45MiwgY292ZXJhZ2UpLCAyKSwgJ3BsYW5fY292ZXJhZ2UnOiByb3VuZChtaW4oMS4wLCBjb3ZlcmFnZSArIDAuMDgpLCAyKSwgJ2hhbmRvZmZfcmVhZGluZXNzJzogcm91bmQoMC41NSArIG1pbigwLjM1LCBsZW4oaGFuZG9mZl9wYWNrZXRbJ3BhcmFsbGVsaXphYmxlX3dvcmsnXSkgKiAwLjA4KSwgMiksICdyaXNrJzogcm91bmQobWF4KDAuMTIsIDAuNjIgLSBjb3ZlcmFnZSksIDIpfQpyZXN1bHRbJ2RldGFpbHMnXSA9IHsnc2VxdWVuY2VkX3BsYW4nOiBzZXF1ZW5jZWRfcGxhbiwgJ2hhbmRvZmZfcGFja2V0JzogaGFuZG9mZl9wYWNrZXQsICdtaXNzaW5nX2lucHV0cyc6IFtrZXkgZm9yIGtleSBpbiBbJ29iamVjdGl2ZScsICdjdXJyZW50X3BsYW4nLCAnYmxvY2tlZF9zdGVwcyddIGlmIG5vdCBwYXlsb2FkX2RhdGEuZ2V0KGtleSldfQpyZXN1bHRbJ2RldGFpbHMnXVsndXNlX2Nhc2VzJ10gPSB1c2VfY2FzZXMKcmVzdWx0WydkZXRhaWxzJ11bJ2dlbmVyYXRpb25fbm90ZSddID0gZ2VuZXJhdGlvbl9ub3RlCnJlc3VsdFsnZGV0YWlscyddWydjYXBhYmlsaXR5X3R5cGUnXSA9IGNhcGFiaWxpdHlfdHlwZQpyZXN1bHRbJ2RldGFpbHMnXVsnbG9naWNfcHJvZmlsZV9pZCddID0gbG9naWNfcHJvZmlsZV9pZApyZXN1bHRbJ2RldGFpbHMnXVsncGF5bG9hZF93YXJuaW5ncyddID0gcGF5bG9hZF93YXJuaW5ncwpyZXN1bHRbJ3Byb2dyZXNzX3N0YXRlJ10gPSB7CiAgICAnY3VycmVudF9zdGFnZSc6IGxvZ2ljX3Byb2ZpbGVfaWQsCiAgICAnbmV4dF9zdGVwJzogc2VxdWVuY2VkX3BsYW5bMF1bJ3Rhc2snXSBpZiBzZXF1ZW5jZWRfcGxhbiBlbHNlICdEZWZpbmUgdGhlIG5leHQgcGxhbm5pbmcgc3RlcC4nLAogICAgJ2Jsb2NrZXJzJzogcmVzdWx0WydkZXRhaWxzJ10uZ2V0KCdtaXNzaW5nX2lucHV0cycsIFtdKVs6NF0sCiAgICAnZG9uZV9zaWduYWxzJzogWydjYXBhYmlsaXR5X3NwZWNpZmljX2FuYWx5c2lzX2NvbXBsZXRlJywgbG9naWNfcHJvZmlsZV9pZF0sCn0KcmVzdWx0Wyd1c2VyX2V4cGVyaWVuY2UnXSA9IHsKICAgICdwbGFpbl9sYW5ndWFnZV90YWtlYXdheSc6IHJlc3VsdFsnc3VtbWFyeSddLAogICAgJ2JlZ2lubmVyX3RpcCc6ICdVc2UgdGhlIGZpcnN0IHJlY29tbWVuZGF0aW9uIGFzIHRoZSBuZXh0IGNvbmNyZXRlIHN0ZXAuJywKICAgICdwb3dlcl91c2VyX3RpcCc6ICdQYXNzIGRldGFpbHMgYW5kIHNjb3JlcyBpbnRvIHRoZSBuZXh0IEFJIGNhcGFiaWxpdHkgcGx1Z2luLicsCiAgICAnaW50ZXJhY3Rpb25fc3VnZ2VzdGlvbnMnOiBbaXRlbS5nZXQoJ2FjdGlvbicsIHN0cihpdGVtKSkgZm9yIGl0ZW0gaW4gcmVzdWx0LmdldCgncmVjb21tZW5kZWRfYWN0aW9ucycsIFtdKVs6M11dLAp9CnJlc3VsdFsnZnVuX21vZGUnXSA9IHsKICAgICdjaGFsbGVuZ2VfbGFiZWwnOiAnQ2FwYWJpbGl0eSBSdW4nLAogICAgJ3Njb3JlX2JhZGdlJzogJ1N0cm9uZyBTaWduYWwnIGlmIHJlc3VsdC5nZXQoJ3Njb3JlcycsIHt9KS5nZXQoJ2NvbmZpZGVuY2UnLCAwKSA+PSAwLjY1IGVsc2UgJ05lZWRzIENvbnRleHQnLAogICAgJ21pY3JvY29weSc6ICdUaGUgcmVzdWx0IGlzIHN0cnVjdHVyZWQgc28gYW5vdGhlciBhZ2VudCBjYW4gcGljayBpdCB1cCBjbGVhbmx5LicsCiAgICAnb3B0aW9uYWxfbmV4dF9jaGFsbGVuZ2UnOiBzZXF1ZW5jZWRfcGxhblswXVsndGFzayddIGlmIHNlcXVlbmNlZF9wbGFuIGVsc2UgJ0RlZmluZSB0aGUgbmV4dCBwbGFubmluZyBzdGVwLicsCn0='
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
