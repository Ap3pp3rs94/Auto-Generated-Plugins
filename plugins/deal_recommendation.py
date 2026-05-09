# Auto-generated Francis plugin skill.
# DO NOT EDIT THIS HEADER BY HAND.
# Title      : Deal Recommendation Explorer
# File       : deal_recommendation.py
# Description: Automatically identify and prioritize top deals based on customer intent and behavior
# Goal       : Automatically identify and prioritize top deals based on customer intent and behavior
# Category   : sales | marketing
# Tags       : deal, prioritization
# Version    : 0.1.0
from __future__ import annotations

import asyncio
import json
import time
from pathlib import Path
from typing import Any, Dict, Mapping, MutableMapping, Optional, Sequence

# =====================================================================
# Metadata (baked from PluginSpec at generation time)
# =====================================================================

_PLUGIN_NAME: str = 'Deal Recommendation Explorer'
_PLUGIN_GOAL: str = 'Automatically identify and prioritize top deals based on customer intent and behavior'
_PLUGIN_CATEGORY: str = 'sales | marketing'
_PLUGIN_TAGS = ['deal', 'prioritization']
_PLUGIN_VERSION: str = '0.1.0'
_PLUGIN_SLUG: str = 'deal_recommendation'
_PLUGIN_RESULT_SCHEMA_VERSION: str = "1.0.0"


# A lightweight manifest for registry / discovery usage
_PLUGIN_MANIFEST: Dict[str, Any] = {
    "name": _PLUGIN_NAME,
    "slug": _PLUGIN_SLUG,
    "goal": _PLUGIN_GOAL,
    "category": _PLUGIN_CATEGORY,
    "tags": list(_PLUGIN_TAGS),
    "version": _PLUGIN_VERSION,
    "schema_version": _PLUGIN_RESULT_SCHEMA_VERSION,
}


# =====================================================================
# Context object
# =====================================================================

class SkillContext:
    """Context object passed to plugins for dependency injection.

    This is the primary surface area for Station B to consume "environment"
    and for the orchestrator to pass shared services.

    Attributes
    ----------
    user_id:
        ID of the caller / owner of this invocation.
    run_id:
        Correlation / trace ID for the orchestrator run (optional).
    brain:
        Optional handle to a "brain" / memory / knowledge object.
    logger:
        Optional logger (must support .debug/.info/.warning/.error/.exception).
    learning_profile:
        Optional dict loaded from the learning subsystem. This can contain
        thresholds, preferred modes, or any other tuning data the factory
        has inferred for this plugin slug.
    extra:
        Arbitrary keyword arguments passed through from the orchestrator.
    """  # noqa: D401

    def __init__(
        self,
        user_id: str,
        run_id: Optional[Any] = None,
        brain: Optional[Any] = None,
        logger: Optional[Any] = None,
        learning_profile: Optional[Dict[str, Any]] = None,
        **extra: Any,
    ) -> None:
        self.user_id = user_id
        self.run_id = run_id
        self.brain = brain
        self.logger = logger
        self.learning_profile = learning_profile or {}
        self.extra = extra

    # -----------------------------------------------------------------
    # Convenience helpers
    # -----------------------------------------------------------------

    def get_logger(self) -> Any:
        """Return a logger if available, otherwise a no-op stub."""  # noqa: D401
        if self.logger is not None:
            return self.logger

        class _NullLogger:
            def debug(self, *args: Any, **kwargs: Any) -> None: ...
            def info(self, *args: Any, **kwargs: Any) -> None: ...
            def warning(self, *args: Any, **kwargs: Any) -> None: ...
            def error(self, *args: Any, **kwargs: Any) -> None: ...
            def exception(self, *args: Any, **kwargs: Any) -> None: ...

        return _NullLogger()

    def log_debug(self, message: str, **fields: Any) -> None:
        logger = self.get_logger()
        try:
            # NOTE: double braces so the f-string emits a literal dict
            logger.debug({"message": message, **fields})
        except Exception:
            # Always non-fatal
            pass

    def log_info(self, message: str, **fields: Any) -> None:
        logger = self.get_logger()
        try:
            logger.info({"message": message, **fields})
        except Exception:
            pass

    def log_warning(self, message: str, **fields: Any) -> None:
        logger = self.get_logger()
        try:
            logger.warning({"message": message, **fields})
        except Exception:
            pass

    def log_error(self, message: str, **fields: Any) -> None:
        logger = self.get_logger()
        try:
            logger.error({"message": message, **fields})
        except Exception:
            pass


# =====================================================================
# Learning profile loader
# =====================================================================

def _load_learning_profile(slug: str) -> Dict[str, Any]:
    """Best-effort load of the learning profile for this plugin.

    Expected path layout (relative to this plugin file):

        <library_root>/
            plugins/
                <slug>.py        (this file)
            learning/
                <slug>.json      (optional; created by learning subsystem)

    If the file is missing or invalid, this gracefully returns an empty dict.
    """  # noqa: D401
    try:
        here = Path(__file__).resolve()
        library_root = here.parent.parent  # go up from 'plugins/'
        learning_dir = library_root / "learning"
        learning_path = learning_dir / f"{slug}.json"

        if not learning_path.exists():
            return {}

        data = json.loads(learning_path.read_text(encoding="utf-8"))
        if isinstance(data, dict):
            return data
        return {}
    except Exception:
        # Learning is optional; never break plugin execution
        return {}


# =====================================================================
# JSON-safety helpers
# =====================================================================

def _to_json_safe(obj: Any, *, max_depth: int = 4) -> Any:
    """Best-effort conversion of arbitrary objects into JSON-safe structures.

    - Primitive types are returned as-is.
    - Mappings and sequences are traversed (up to max_depth).
    - Known non-serializable types are converted to strings.
    - On depth exhaustion or unknown objects, fall back to str(obj).
    """  # noqa: D401
    if max_depth <= 0:
        return str(obj)

    # Primitive JSON-safe types
    if obj is None or isinstance(obj, (bool, int, float, str)):
        return obj

    # Mappings
    if isinstance(obj, Mapping):
        return {
            str(k): _to_json_safe(v, max_depth=max_depth - 1)
            for k, v in obj.items()
        }

    # Sequences
    if isinstance(obj, (list, tuple, set, frozenset)):
        return [
            _to_json_safe(v, max_depth=max_depth - 1)
            for v in obj
        ]

    # Paths
    if isinstance(obj, Path):
        return str(obj)

    # Fallback
    return str(obj)


# =====================================================================
# Config helpers (default + customer overrides)
# =====================================================================

def _merge_shallow(base: Dict[str, Any], override: Dict[str, Any]) -> Dict[str, Any]:
    """Shallow merge of two dicts, with override taking precedence."""  # noqa: D401
    merged = dict(base)
    for key, value in override.items():
        merged[key] = value
    return merged


def _merge_config(default_config: Dict[str, Any], user_config: Dict[str, Any]) -> Dict[str, Any]:
    """Best-effort merge for configuration dictionaries.

    - Top-level keys are merged shallowly.
    - For known nested dict keys ('weights', 'thresholds'), merge key-wise.
    """  # noqa: D401
    if not isinstance(user_config, dict) or not user_config:
        return dict(default_config)

    merged: Dict[str, Any] = dict(default_config)

    for key, value in user_config.items():
        if key in ("weights", "thresholds"):
            base_sub = merged.get(key)
            if isinstance(base_sub, dict) and isinstance(value, dict):
                sub = dict(base_sub)
                sub.update(value)
                merged[key] = sub
            else:
                merged[key] = value
        else:
            merged[key] = value

    return merged


def _build_effective_config(payload: Dict[str, Any]) -> Dict[str, Any]:
    """Build the effective config for this invocation.

    The orchestrator can pass a per-call configuration in:
        payload["customer_config"]

    Shape is intentionally loose, but we standardize a few keys:
        - weights:      dict of factor -> weight
        - thresholds:   dict of name -> numeric threshold
        - fields:       list of field names to pay extra attention to
        - max_insights: int, soft cap on number of insights
        - mode:         string, e.g. "balanced" | "aggressive" | "conservative"
    """  # noqa: D401
    default_config: Dict[str, Any] = {
        "weights": {},
        "thresholds": {},
        "fields": [],
        "max_insights": 8,
        "mode": "balanced",
    }

    user_config: Dict[str, Any] = {}
    if isinstance(payload, dict):
        maybe_cfg = payload.get("customer_config")
        if isinstance(maybe_cfg, dict):
            user_config = maybe_cfg

    return _merge_config(default_config, user_config)


# =====================================================================
# Result envelope helpers
# =====================================================================

def _base_meta(
    *,
    learning_profile: Dict[str, Any],
    context: Optional[SkillContext],
    duration_ms: Optional[float],
) -> Dict[str, Any]:
    meta: Dict[str, Any] = {
        "plugin_name": _PLUGIN_NAME,
        "plugin_slug": _PLUGIN_SLUG,
        "plugin_category": _PLUGIN_CATEGORY,
        "plugin_version": _PLUGIN_VERSION,
        "schema_version": _PLUGIN_RESULT_SCHEMA_VERSION,
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }

    if duration_ms is not None:
        meta["duration_ms"] = float(duration_ms)

    if context is not None:
        meta["user_id"] = context.user_id
        if context.run_id is not None:
            meta["run_id"] = context.run_id

    if learning_profile:
        meta["learning_profile"] = learning_profile

    return meta


def _normalize_success_output(
    core_output: Any,
    *,
    learning_profile: Dict[str, Any],
    context: Optional[SkillContext],
    duration_ms: Optional[float],
) -> Dict[str, Any]:
    """Wrap raw core logic output into the standard response envelope.

    Station C expects:
        {
          "status": "succeeded",
          "output": <JSON-serializable>,
          "error": None or "",
          "meta": { ... }
        }
    """  # noqa: D401
    meta = _base_meta(
        learning_profile=learning_profile,
        context=context,
        duration_ms=duration_ms,
    )

    safe_output = _to_json_safe(core_output)

    return {
        "status": "succeeded",
        "output": safe_output,
        "error": None,
        "meta": meta,
    }


def _normalize_error_output(
    exc: BaseException,
    *,
    learning_profile: Dict[str, Any],
    context: Optional[SkillContext],
    duration_ms: Optional[float],
) -> Dict[str, Any]:
    """Standardized error envelope for plugin failures."""  # noqa: D401
    meta = _base_meta(
        learning_profile=learning_profile,
        context=context,
        duration_ms=duration_ms,
    )
    meta.update(
        {
            "exception_type": type(exc).__name__,
        }
    )

    message = str(exc)
    if len(message) > 2000:
        message = message[:2000] + "...[truncated]"

    return {
        "status": "failed",
        "output": None,
        "error": message,
        "meta": meta,
    }


# =====================================================================
# Core logic hook (Station B overwrites this)
# =====================================================================

def _run_core_logic(context: SkillContext, payload: Dict[str, Any], config: Dict[str, Any]) -> Any:
    """Core plugin logic.

    Station B overwrites the BODY between the logic markers below.

    IMPORTANT:
    - 'payload' contains the raw input.
    - 'config' is the merged configuration:
        default_config + payload.get("customer_config", {}).
    - Station B is responsible for updating and returning a structured result.

    Expected logical structure for the LLM:
    - Read fields from payload.
    - Read tunable parameters from config.
    - Populate 'result' with summary, insights, actions, scores, and details.
    """  # noqa: D401
    # === LOGIC START ===
    import base64
    try:
        if hasattr(context, "log_info"):
            context.log_info(
                "Executing LLM-generated core logic.",
                plugin_slug=_PLUGIN_SLUG,
            )
    except Exception:
        pass

    _llm_body_b64 = "SGVyZSdzIHRoZSBnZW5lcmF0ZWQgcGx1Z2luIGJvZHk6CgojIFlvdXIgY29kZSBnb2VzIGhlcmUKIyBUaGlzIHBsdWdpbiBmaW5kcyBvcHBvcnR1bml0aWVzIGJhc2VkIG9uIFNob3BpZnkgYXV0b21hdGlvbiBkYXRhLgoKaWYgJ2RhdGEnIG5vdCBpbiBwYXlsb2FkOgogICAgcmVzdWx0WydzdW1tYXJ5J10gPSAiTm8gdXNhYmxlIGRhdGEgcHJvdmlkZWQuIgogICAgcmVzdWx0WydwcmltYXJ5X2luc2lnaHRzJ10uYXBwZW5kKHsKICAgICAgICAndGl0bGUnOiAnRGF0YSBNaXNzaW5nJywKICAgICAgICAnZGVzY3JpcHRpb24nOiAnUGxlYXNlIHByb3ZpZGUgdGhlIG5lY2Vzc2FyeSBkYXRhIHRvIGZpbmQgb3Bwb3J0dW5pdGllcy4nLAogICAgICAgICdzZXZlcml0eSc6ICdsb3cnCiAgICB9KQogICAgaWYgJ3VzZV9jYXNlJyBpbiBwYXlsb2FkIGFuZCBwYXlsb2FkWyd1c2VfY2FzZSddOgogICAgICAgIHJlc3VsdFsncmVjb21tZW5kZWRfYWN0aW9ucyddLmFwcGVuZCh7CiAgICAgICAgICAgICdhY3Rpb24nOiAnUHJvdmlkZSBEYXRhJywKICAgICAgICAgICAgJ3JlYXNvbic6IGYiU2luY2Uge3BheWxvYWRbJ3VzZV9jYXNlJ119LCB3ZSBuZWVkIHRoaXMgZGF0YSB0byBwcm9jZWVkLiIKICAgICAgICB9KQogICAgcmV0dXJuCgojIENoZWNrIGZvciB1c2UgY2FzZQppZiAndXNlX2Nhc2UnIG5vdCBpbiBwYXlsb2FkOgogICAgcmVzdWx0WydzdW1tYXJ5J10gPSAiTm8gc3BlY2lmaWMgdXNlIGNhc2UgcHJvdmlkZWQuIgogICAgcmVzdWx0WydwcmltYXJ5X2luc2lnaHRzJ10uYXBwZW5kKHsKICAgICAgICAndGl0bGUnOiAnVW5jbGVhciBVc2UgQ2FzZScsCiAgICAgICAgJ2Rlc2NyaXB0aW9uJzogJ1BsZWFzZSBzcGVjaWZ5IHRoZSB1c2UgY2FzZSB0byBmaW5kIHJlbGV2YW50IG9wcG9ydHVuaXRpZXMuJywKICAgICAgICAnc2V2ZXJpdHknOiAnbG93JwogICAgfSkKICAgIGlmICdjb25maWcnIGluIHBheWxvYWQgYW5kIHBheWxvYWRbJ2NvbmZpZyddOgogICAgICAgIHJlc3VsdFsncmVjb21tZW5kZWRfYWN0aW9ucyddLmFwcGVuZCh7CiAgICAgICAgICAgICdhY3Rpb24nOiAnU3BlY2lmeSBVc2UgQ2FzZScsCiAgICAgICAgICAgICdyZWFzb24nOiBmIlNpbmNlIHlvdSBwcm92aWRlZCBjb25maWd1cmF0aW9uLCBwbGVhc2UgY2xhcmlmeSB5b3VyIHVzZSBjYXNlLiIKICAgICAgICB9KQogICAgcmV0dXJuCgojIENoZWNrIGZvciBjb25maWcKaWYgJ2ZvY3VzX2ZpZWxkcycgbm90IGluIHBheWxvYWRbJ2NvbmZpZyddIG9yIG5vdCBwYXlsb2FkWydjb25maWcnXVsnZm9jdXNfZmllbGRzJ106CiAgICByZXN1bHRbJ3N1bW1hcnknXSA9ICJObyBmb2N1cyBmaWVsZHMgcHJvdmlkZWQuIgogICAgcmVzdWx0WydwcmltYXJ5X2luc2lnaHRzJ10uYXBwZW5kKHsKICAgICAgICAndGl0bGUnOiAnVW5jbGVhciBGb2N1cycsCiAgICAgICAgJ2Rlc2NyaXB0aW9uJzogJ1BsZWFzZSBzcGVjaWZ5IHRoZSBmb2N1cyBmaWVsZHMgdG8gZmluZCByZWxldmFudCBvcHBvcnR1bml0aWVzLicsCiAgICAgICAgJ3NldmVyaXR5JzogJ2xvdycKICAgIH0pCiAgICBpZiAnZGF0YScgaW4gcGF5bG9hZCBhbmQgcGF5bG9hZFsnZGF0YSddOgogICAgICAgIHJlc3VsdFsncmVjb21tZW5kZWRfYWN0aW9ucyddLmFwcGVuZCh7CiAgICAgICAgICAgICdhY3Rpb24nOiAnU3BlY2lmeSBGb2N1cyBGaWVsZHMnLAogICAgICAgICAgICAncmVhc29uJzogZiJTaW5jZSB5b3UgcHJvdmlkZWQgZGF0YSwgcGxlYXNlIGNsYXJpZnkgeW91ciBmb2N1cyBmaWVsZHMuIgogICAgICAgIH0pCiAgICByZXR1cm4KCiMgQ2hlY2sgZm9yIHVzZSBjYXNlIGFuZCBjb25maWcKaWYgJ3VzZV9jYXNlJyBub3QgaW4gcGF5bG9hZCBvciAnY29uZmlnJyBub3QgaW4gcGF5bG9hZDoKICAgIHJlc3VsdFsnc3VtbWFyeSddID0gIkluc3VmZmljaWVudCBpbmZvcm1hdGlvbi4iCiAgICByZXN1bHRbJ3ByaW1hcnlfaW5zaWdodHMnXS5hcHBlbmQoewogICAgICAgICd0aXRsZSc6ICdNaXNzaW5nIEluZm9ybWF0aW9uJywKICAgICAgICAnZGVzY3JpcHRpb24nOiAnUGxlYXNlIHByb3ZpZGUgdGhlIG5lY2Vzc2FyeSBpbmZvcm1hdGlvbiB0byBmaW5kIG9wcG9ydHVuaXRpZXMuJywKICAgICAgICAnc2V2ZXJpdHknOiAnbG93JwogICAgfSkKICAgIGlmICdkYXRhJyBpbiBwYXlsb2FkIGFuZCBwYXlsb2FkWydkYXRhJ106CiAgICAgICAgcmVzdWx0WydyZWNvbW1lbmRlZF9hY3Rpb25zJ10uYXBwZW5kKHsKICAgICAgICAgICAgJ2FjdGlvbic6ICdQcm92aWRlIE1vcmUgSW5mb3JtYXRpb24nLAogICAgICAgICAgICAncmVhc29uJzogZiJTaW5jZSB5b3UgcHJvdmlkZWQgZGF0YSwgcGxlYXNlIHNwZWNpZnkgeW91ciB1c2UgY2FzZSBhbmQgZm9jdXMgZmllbGRzLiIKICAgICAgICB9KQogICAgcmV0dXJuCgojIENoZWNrIGZvciBjaHVybiByaXNrIHNpZ25hbHMKY2h1cm5fcmlza19zaWduYWxzID0gW10KZm9yIGl0ZW0gaW4gcGF5bG9hZFsnZGF0YSddOgogICAgaWYgaXRlbVsnY3VzdG9tZXInXVsnY2h1cm5lZCddIG9yIGl0ZW1bJ3JldmVudWUnXVsnbGFzdF9tb250aCddIDwgMC41ICogaXRlbVsncmV2ZW51ZSddWydhdmVyYWdlX2xhc3RfNl9tb250aHMnXToKICAgICAgICBjaHVybl9yaXNrX3NpZ25hbHMuYXBwZW5kKGl0ZW0pCgppZiBjaHVybl9yaXNrX3NpZ25hbHM6CiAgICByZXN1bHRbJ3N1bW1hcnknXSA9ICJDaHVybiByaXNrIHNpZ25hbHMgZGV0ZWN0ZWQuIgogICAgZm9yIHNpZ25hbCBpbiBjaHVybl9yaXNrX3NpZ25hbHM6CiAgICAgICAgcmVzdWx0WydwcmltYXJ5X2luc2lnaHRzJ10uYXBwZW5kKHsKICAgICAgICAgICAgJ3RpdGxlJzogZiJDaHVybiBSaXNrIFNpZ25hbCAtIHtzaWduYWxbJ2N1c3RvbWVyJ11bJ25hbWUnXX0iLAogICAgICAgICAgICAnZGVzY3JpcHRpb24nOiBmIlRoZSBjdXN0b21lciB7c2lnbmFsWydjdXN0b21lciddWyduYW1lJ119IGhhcyBhIGNodXJuIHJpc2sgc2lnbmFsIGR1ZSB0byB0aGVpciByZWNlbnQgcmV2ZW51ZSBwZXJmb3JtYW5jZS4iLAogICAgICAgICAgICAnc2V2ZXJpdHknOiAnaGlnaCcKICAgICAgICB9KQogICAgaWYgJ3JlY29tbWVuZGVkX2FjdGlvbnMnIG5vdCBpbiByZXN1bHQgb3Igbm90IHJlc3VsdFsncmVjb21tZW5kZWRfYWN0aW9ucyddOgogICAgICAgIHJlc3VsdFsncmVjb21tZW5kZWRfYWN0aW9ucyddLmFwcGVuZCh7CiAgICAgICAgICAgICdhY3Rpb24nOiAnUmVhY2ggT3V0JywKICAgICAgICAgICAgJ3JlYXNvbic6IGYiQmFzZWQgb24gdGhlIGNodXJuIHJpc2sgc2lnbmFscywgaXQgaXMgcmVjb21tZW5kZWQgdG8gcmVhY2ggb3V0IHRvIHRoZSBjdXN0b21lcnMgYW5kIGFkZHJlc3MgdGhlaXIgY29uY2VybnMuIgogICAgICAgIH0pCgojIENoZWNrIGZvciB1cHNlbGwgb3Bwb3J0dW5pdGllcwp1cHNlbGxfb3Bwb3J0dW5pdGllcyA9IFtdCmZvciBpdGVtIGluIHBheWxvYWRbJ2RhdGEnXToKICAgIGlmIGl0ZW1bJ2N1c3RvbWVyJ11bJ3BsYW4nXSAhPSAncHJlbWl1bScgYW5kIGl0ZW1bJ3JldmVudWUnXVsnbGFzdF9tb250aCddID4gMS41ICogaXRlbVsncmV2ZW51ZSddWydhdmVyYWdlX2xhc3RfNl9tb250aHMnXToKICAgICAgICB1cHNlbGxfb3Bwb3J0dW5pdGllcy5hcHBlbmQoaXRlbSkKCmlmIHVwc2VsbF9vcHBvcnR1bml0aWVzOgogICAgcmVzdWx0WydzdW1tYXJ5J10gPSAiVXBzZWxsIG9wcG9ydHVuaXRpZXMgZGV0ZWN0ZWQuIgogICAgZm9yIG9wcG9ydHVuaXR5IGluIHVwc2VsbF9vcHBvcnR1bml0aWVzOgogICAgICAgIHJlc3VsdFsncHJpbWFyeV9pbnNpZ2h0cyddLmFwcGVuZCh7CiAgICAgICAgICAgICd0aXRsZSc6IGYiVXBzZWxsIE9wcG9ydHVuaXR5IC0ge29wcG9ydHVuaXR5WydjdXN0b21lciddWyduYW1lJ119IiwKICAgICAgICAgICAgJ2Rlc2NyaXB0aW9uJzogZiJUaGUgY3VzdG9tZXIge29wcG9ydHVuaXR5WydjdXN0b21lciddWyduYW1lJ119IGhhcyBhbiB1cHNlbGwgb3Bwb3J0dW5pdHkgZHVlIHRvIHRoZWlyIHJlY2VudCByZXZlbnVlIHBlcmZvcm1hbmNlLiIsCiAgICAgICAgICAgICdzZXZlcml0eSc6ICdoaWdoJwogICAgICAgIH0pCiAgICBpZiAncmVjb21tZW5kZWRfYWN0aW9ucycgbm90IGluIHJlc3VsdCBvciBub3QgcmVzdWx0WydyZWNvbW1lbmRlZF9hY3Rpb25zJ106CiAgICAgICAgcmVzdWx0WydyZWNvbW1lbmRlZF9hY3Rpb25zJ10uYXBwZW5kKHsKICAgICAgICAgICAgJ2FjdGlvbic6ICdVcHNlbGwnLAogICAgICAgICAgICAncmVhc29uJzogZiJCYXNlZCBvbiB0aGUgdXBzZWxsIG9wcG9ydHVuaXRpZXMsIGl0IGlzIHJlY29tbWVuZGVkIHRvIG9mZmVyIHByZW1pdW0gcGxhbnMgdG8gdGhlIGN1c3RvbWVycy4iCiAgICAgICAgfSkKCiMgQ2hlY2sgZm9yIGNyb3NzLXNlbGwgb3Bwb3J0dW5pdGllcwpjcm9zc19zZWxsX29wcG9ydHVuaXRpZXMgPSBbXQpmb3IgaXRlbSBpbiBwYXlsb2FkWydkYXRhJ106CiAgICBpZiBpdGVtWydjdXN0b21lciddWydwbGFuJ10gIT0gJ3ByZW1pdW0nIGFuZCAoaXRlbVsncmV2ZW51ZSddWydsYXN0X21vbnRoJ10gPiAxLjUgKiBpdGVtWydyZXZlbnVlJ11bJ2F2ZXJhZ2VfbGFzdF82X21vbnRocyddIG9yIGxlbihpdGVtWydwcm9kdWN0cyddKSA+IDMpOgogICAgICAgIGNyb3NzX3NlbGxfb3Bwb3J0dW5pdGllcy5hcHBlbmQoaXRlbSkKCmlmIGNyb3NzX3NlbGxfb3Bwb3J0dW5pdGllczoKICAgIHJlc3VsdFsnc3VtbWFyeSddID0gIkNyb3NzLXNlbGwgb3Bwb3J0dW5pdGllcyBkZXRlY3RlZC4iCiAgICBmb3Igb3Bwb3J0dW5pdHkgaW4gY3Jvc3Nfc2VsbF9vcHBvcnR1bml0aWVzOgogICAgICAgIHJlc3VsdFsncHJpbWFyeV9pbnNpZ2h0cyddLmFwcGVuZCh7CiAgICAgICAgICAgICd0aXRsZSc6IGYiQ3Jvc3MtU2VsbCBPcHBvcnR1bml0eSAtIHtvcHBvcnR1bml0eVsnY3VzdG9tZXInXVsnbmFtZSddfSIsCiAgICAgICAgICAgICdkZXNjcmlwdGlvbic6IGYiVGhlIGN1c3RvbWVyIHtvcHBvcnR1bml0eVsnY3VzdG9tZXInXVsnbmFtZSddfSBoYXMgYSBjcm9zcy1zZWxsIG9wcG9ydHVuaXR5IGR1ZSB0byB0aGVpciByZWNlbnQgcmV2ZW51ZSBwZXJmb3JtYW5jZSBhbmQgcHJvZHVjdCB1c2FnZS4iLAogICAgICAgICAgICAnc2V2ZXJpdHknOiAnaGlnaCcKICAgICAgICB9KQogICAgaWYgJ3JlY29tbWVuZGVkX2FjdGlvbnMnIG5vdCBpbiByZXN1bHQgb3Igbm90IHJlc3VsdFsncmVjb21tZW5kZWRfYWN0aW9ucyddOgogICAgICAgIHJlc3VsdFsncmVjb21tZW5kZWRfYWN0aW9ucyddLmFwcGVuZCh7CiAgICAgICAgICAgICdhY3Rpb24nOiAnQ3Jvc3MtU2VsbCcsCiAgICAgICAgICAgICdyZWFzb24nOiBmIkJhc2VkIG9uIHRoZSBjcm9zcy1zZWxsIG9wcG9ydHVuaXRpZXMsIGl0IGlzIHJlY29tbWVuZGVkIHRvIG9mZmVyIHJlbGV2YW50IHByb2R1Y3RzIHRvIHRoZSBjdXN0b21lcnMuIgogICAgICAgIH0pCgojIEZpbGwgc2NvcmVzIGFuZCBkZXRhaWxzIGFzIG5lZWRlZAppZiAnc2NvcmVzJyBub3QgaW4gcmVzdWx0OgogICAgcmVzdWx0WydzY29yZXMnXSA9IHsnY29uZmlkZW5jZSc6IDAuOX0KcmVzdWx0WydkZXRhaWxzJ10gPSB7CiAgICAnY2h1cm5fcmlza19zaWduYWxzJzogY2h1cm5fcmlza19zaWduYWxzLAogICAgJ3Vwc2VsbF9vcHBvcnR1bml0aWVzJzogdXBzZWxsX29wcG9ydHVuaXRpZXMsCiAgICAnY3Jvc3Nfc2VsbF9vcHBvcnR1bml0aWVzJzogY3Jvc3Nfc2VsbF9vcHBvcnR1bml0aWVzCn0="
    try:
        _llm_source_bytes = base64.b64decode(_llm_body_b64.encode("ascii"))
        _llm_body_source = _llm_source_bytes.decode("utf-8")
    except Exception:
        _llm_body_source = ""

    result = {
        "summary": "",
        "primary_insights": [],
        "recommended_actions": [],
        "scores": {"confidence": 0.0},
        "details": {},
    }

    local_vars = {
        "context": context,
        "payload": payload,
        "result": result,
    }

    if _llm_body_source.strip():
        try:
            exec(_llm_body_source, {}, local_vars)
            if "result" in local_vars:
                result = local_vars["result"]
        except Exception as _exc:
            try:
                if hasattr(context, "log_error"):
                    context.log_error(
                        "LLM logic execution failed.",
                        error=str(_exc),
                        plugin_slug=_PLUGIN_SLUG,
                    )
            except Exception:
                pass
            if isinstance(result, dict):
                details = result.get("details")
                if not isinstance(details, dict):
                    details = {}
                details["llm_error"] = str(_exc)
                result["details"] = details
            else:
                result = {
                    "summary": "Core logic failed; fallback applied.",
                    "primary_insights": [],
                    "recommended_actions": [],
                    "scores": {"confidence": 0.0},
                    "details": {"error": str(_exc)},
                }
    else:
        result = {
            "summary": "Core logic executed but returned no details.",
            "primary_insights": [],
            "recommended_actions": [],
            "scores": {"confidence": 0.0},
            "details": {"note": "Fallback result injected by factory."},
        }

    # Ensure non-empty result for Station C
    if (
        result is None
        or result == ""
        or result == []
        or result == {}
        or (
            isinstance(result, dict)
            and not result.get("summary")
            and not result.get("primary_insights")
            and not result.get("recommended_actions")
        )
    ):
        result = {
            "summary": "Core logic produced an empty result; fallback applied.",
            "primary_insights": [
                {"title": "No-op analysis", "description": "Plugin executed but did not generate insights; fallback applied by the factory."}
            ],
            "recommended_actions": [
                "Review payload format and plugin logic for this skill.",
                "Consider regenerating the plugin with stricter prompts."
            ],
            "scores": {"confidence": 0.0},
            "details": {"note": "Fallback result injected by factory due to empty output."},
        }

    return result
# === LOGIC END ===


# =====================================================================
# Async entrypoint
# =====================================================================

async def invoke(user_id: str, payload: Dict[str, Any], **kwargs: Any) -> Dict[str, Any]:
    """Async entrypoint used by the factory and runtime."""  # noqa: D401
    if not isinstance(payload, dict):
        payload = {"_value": payload}

    learning_profile = _load_learning_profile(_PLUGIN_SLUG)

    ctx = SkillContext(
        user_id=user_id,
        run_id=kwargs.get("run_id"),
        brain=kwargs.get("brain"),
        logger=kwargs.get("logger"),
        learning_profile=learning_profile,
        **{k: v for k, v in kwargs.items() if k not in ("run_id", "brain", "logger")},
    )

    # Build effective per-call config from payload["customer_config"] if present
    config = _build_effective_config(payload)

    start = time.perf_counter()

    try:
        maybe_output = _run_core_logic(ctx, payload, config)

        if asyncio.iscoroutine(maybe_output):
            core_output = await maybe_output
        else:
            core_output = maybe_output

        duration_ms = (time.perf_counter() - start) * 1000.0

        return _normalize_success_output(
            core_output,
            learning_profile=learning_profile,
            context=ctx,
            duration_ms=duration_ms,
        )
    except Exception as exc:  # noqa: BLE001
        duration_ms = (time.perf_counter() - start) * 1000.0

        return _normalize_error_output(
            exc,
            learning_profile=learning_profile,
            context=ctx,
            duration_ms=duration_ms,
        )
