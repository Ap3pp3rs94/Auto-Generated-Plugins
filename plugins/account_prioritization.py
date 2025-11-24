# Auto-generated Francis plugin skill.
# DO NOT EDIT THIS HEADER BY HAND.
# Title      : Account Prioritization Insights
# File       : account_prioritization.py
# Description: Identify high-potential accounts and prioritize sales efforts based on customer behavior and engagement metrics.
# Goal       : Identify high-potential accounts and prioritize sales efforts based on customer behavior and engagement metrics.
# Category   : sales
# Tags       : prioritization, customer_behavior
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

_PLUGIN_NAME: str = 'Account Prioritization Insights'
_PLUGIN_GOAL: str = 'Identify high-potential accounts and prioritize sales efforts based on customer behavior and engagement metrics.'
_PLUGIN_CATEGORY: str = 'sales'
_PLUGIN_TAGS = ['prioritization', 'customer_behavior']
_PLUGIN_VERSION: str = '0.1.0'
_PLUGIN_SLUG: str = 'account_prioritization'
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

    _llm_body_b64 = "SGVyZSdzIGEgUHl0aG9uIGZ1bmN0aW9uIHRoYXQgcG9wdWxhdGVzIHRoZSByZXN1bHQgZGljdGlvbmFyeSB3aXRoIGluc2lnaHRzIGFuZCByZWNvbW1lbmRlZCBhY3Rpb25zIGJhc2VkIG9uIHRoZSBnaXZlbiBwYXlsb2FkOgoKaWYgImRhdGEiIG5vdCBpbiBwYXlsb2FkOgogICAgcmVzdWx0WyJzdW1tYXJ5Il0gPSAiTm8gdXNhYmxlIGRhdGEgcHJvdmlkZWQuIgogICAgcmVzdWx0WyJwcmltYXJ5X2luc2lnaHRzIl0uYXBwZW5kKHsKICAgICAgICAidGl0bGUiOiAiSW5zdWZmaWNpZW50IERhdGEiLAogICAgICAgICJkZXNjcmlwdGlvbiI6ICJQbGVhc2UgcHJvdmlkZSB2YWxpZCBkYXRhIHRvIGNvbnRpbnVlLiIsCiAgICB9KQogICAgcmVzdWx0WyJyZWNvbW1lbmRlZF9hY3Rpb25zIl0uYXBwZW5kKHsKICAgICAgICAiYWN0aW9uIjogIlByb3ZpZGUgVmFsaWQgRGF0YSIsCiAgICAgICAgInJlYXNvbiI6ICJDYW5ub3QgZ2VuZXJhdGUgaW5zaWdodHMgd2l0aG91dCBzdWZmaWNpZW50IGRhdGEuIiwKICAgIH0pCmVsc2U6CiAgICBpZiAidXNlX2Nhc2UiIGluIHBheWxvYWQgYW5kIHBheWxvYWRbInVzZV9jYXNlIl06CiAgICAgICAgdXNlX2Nhc2UgPSBwYXlsb2FkWyJ1c2VfY2FzZSJdCiAgICBlbHNlOgogICAgICAgIHVzZV9jYXNlID0gIk5vIHNwZWNpZmljIHVzZSBjYXNlIHByb3ZpZGVkLiIKCiAgICBpZiAiY29uZmlnIiBpbiBwYXlsb2FkIGFuZCBwYXlsb2FkWyJjb25maWciXToKICAgICAgICBjb25maWcgPSBwYXlsb2FkWyJjb25maWciXQogICAgZWxzZToKICAgICAgICBjb25maWcgPSB7ImZvY3VzX2ZpZWxkcyI6IFtdLCAiaWdub3JlX2ZpZWxkcyI6IFtdfQoKICAgICMgSW5pdGlhbGl6ZSB2YXJpYWJsZXMKICAgIHVwc2VsbF9vcHBvcnR1bml0aWVzID0gW10KICAgIGNyb3NzX3NlbGxfb3Bwb3J0dW5pdGllcyA9IFtdCiAgICBjaHVybl9wcmV2ZW50aW9uX29wcG9ydHVuaXRpZXMgPSBbXQogICAgZWZmaWNpZW5jeV93aW5zID0gW10KICAgIHJldmVudWVfb3B0aW1pemF0aW9uX29wcG9ydHVuaXRpZXMgPSBbXQoKICAgICMgSWRlbnRpZnkgdXBzZWxsIG9wcG9ydHVuaXRpZXMKICAgIGZvciBpdGVtIGluIHBheWxvYWRbImRhdGEiXToKICAgICAgICBpZiAibXJyIiBpbiBpdGVtIGFuZCAidGlja2V0c19sYXN0XzMwZCIgaW4gaXRlbToKICAgICAgICAgICAgdXBzZWxsX29wcG9ydHVuaXRpZXMuYXBwZW5kKHsKICAgICAgICAgICAgICAgICJ0aXRsZSI6IGYiVXBzZWxsIE9wcG9ydHVuaXR5OiB7aXRlbVsnbXJyJ119IiwKICAgICAgICAgICAgICAgICJkZXNjcmlwdGlvbiI6IGYiQ3VzdG9tZXIgaGFzIHJlY2VudGx5IHN1Ym1pdHRlZCB7aXRlbVsndGlja2V0c19sYXN0XzMwZCddfSB0aWNrZXRzLiIsCiAgICAgICAgICAgIH0pCgogICAgIyBJZGVudGlmeSBjcm9zcy1zZWxsIG9wcG9ydHVuaXRpZXMKICAgIGZvciBpdGVtIGluIHBheWxvYWRbImRhdGEiXToKICAgICAgICBpZiAibG9naW5fY291bnQiIGluIGl0ZW0gYW5kICJ0aWNrZXRzX2xhc3RfMzBkIiBpbiBpdGVtOgogICAgICAgICAgICBjcm9zc19zZWxsX29wcG9ydHVuaXRpZXMuYXBwZW5kKHsKICAgICAgICAgICAgICAgICJ0aXRsZSI6IGYiQ3Jvc3MtU2VsbCBPcHBvcnR1bml0eToge2l0ZW1bJ2xvZ2luX2NvdW50J119IGxvZ2lucyIsCiAgICAgICAgICAgICAgICAiZGVzY3JpcHRpb24iOiBmIkN1c3RvbWVyIGhhcyByZWNlbnRseSBsb2dnZWQgaW4ge2l0ZW1bJ2xvZ2luX2NvdW50J119IHRpbWVzLiIsCiAgICAgICAgICAgIH0pCgogICAgIyBJZGVudGlmeSBjaHVybiBwcmV2ZW50aW9uIG9wcG9ydHVuaXRpZXMKICAgIGZvciBpdGVtIGluIHBheWxvYWRbImRhdGEiXToKICAgICAgICBpZiAibXJyIiBpbiBpdGVtIGFuZCAiY2h1cm5fcmlzayIgaW4gaXRlbToKICAgICAgICAgICAgY2h1cm5fcHJldmVudGlvbl9vcHBvcnR1bml0aWVzLmFwcGVuZCh7CiAgICAgICAgICAgICAgICAidGl0bGUiOiBmIkNodXJuIFByZXZlbnRpb24gT3Bwb3J0dW5pdHk6IHtpdGVtWydtcnInXX0iLAogICAgICAgICAgICAgICAgImRlc2NyaXB0aW9uIjogZiJDdXN0b21lciBoYXMgYSB7aXRlbVsnY2h1cm5fcmlzayddfSByaXNrIG9mIGNodXJuaW5nLiIsCiAgICAgICAgICAgIH0pCgogICAgIyBJZGVudGlmeSBlZmZpY2llbmN5IHdpbnMKICAgIGZvciBpdGVtIGluIHBheWxvYWRbImRhdGEiXToKICAgICAgICBpZiAidGlja2V0c19sYXN0XzMwZCIgaW4gaXRlbSBhbmQgImVmZmljaWVuY3lfc2NvcmUiIGluIGl0ZW06CiAgICAgICAgICAgIGVmZmljaWVuY3lfd2lucy5hcHBlbmQoewogICAgICAgICAgICAgICAgInRpdGxlIjogZiJFZmZpY2llbmN5IFdpbjoge2l0ZW1bJ2VmZmljaWVuY3lfc2NvcmUnXX0gc2NvcmUiLAogICAgICAgICAgICAgICAgImRlc2NyaXB0aW9uIjogZiJDdXN0b21lciBoYXMgYWNoaWV2ZWQgYW4gZWZmaWNpZW5jeSBzY29yZSBvZiB7aXRlbVsnZWZmaWNpZW5jeV9zY29yZSddfS4iLAogICAgICAgICAgICB9KQoKICAgICMgSWRlbnRpZnkgcmV2ZW51ZSBvcHRpbWl6YXRpb24gb3Bwb3J0dW5pdGllcwogICAgZm9yIGl0ZW0gaW4gcGF5bG9hZFsiZGF0YSJdOgogICAgICAgIGlmICJtcnIiIGluIGl0ZW0gYW5kICJyZXZlbnVlX2dyb3d0aCIgaW4gaXRlbToKICAgICAgICAgICAgcmV2ZW51ZV9vcHRpbWl6YXRpb25fb3Bwb3J0dW5pdGllcy5hcHBlbmQoewogICAgICAgICAgICAgICAgInRpdGxlIjogZiJSZXZlbnVlIE9wdGltaXphdGlvbiBPcHBvcnR1bml0eToge2l0ZW1bJ21yciddfSBncm93dGgiLAogICAgICAgICAgICAgICAgImRlc2NyaXB0aW9uIjogZiJDdXN0b21lciBoYXMgZXhwZXJpZW5jZWQgYSB7aXRlbVsncmV2ZW51ZV9ncm93dGgnXX0gcmV2ZW51ZSBncm93dGguIiwKICAgICAgICAgICAgfSkKCiAgICAjIFBvcHVsYXRlIHJlc3VsdCBkaWN0aW9uYXJ5CiAgICByZXN1bHRbInN1bW1hcnkiXSA9IGYiT3Bwb3J0dW5pdHkgRmluZGVyIGZvciBBY2NvdW50LUJhc2VkIE1hcmtldGluZyBBdXRvbWF0aW9uLiIKICAgIHJlc3VsdFsicHJpbWFyeV9pbnNpZ2h0cyJdLmV4dGVuZCh1cHNlbGxfb3Bwb3J0dW5pdGllcyArIGNyb3NzX3NlbGxfb3Bwb3J0dW5pdGllcyArIGNodXJuX3ByZXZlbnRpb25fb3Bwb3J0dW5pdGllcyArIGVmZmljaWVuY3lfd2lucyArIHJldmVudWVfb3B0aW1pemF0aW9uX29wcG9ydHVuaXRpZXMpCiAgICByZWNvbW1lbmRlZF9hY3Rpb25zID0gW10KICAgIGlmIHVwc2VsbF9vcHBvcnR1bml0aWVzOgogICAgICAgIHJlY29tbWVuZGVkX2FjdGlvbnMuYXBwZW5kKHsKICAgICAgICAgICAgImFjdGlvbiI6ICJVcHNlbGwgQ2FtcGFpZ24iLAogICAgICAgICAgICAicmVhc29uIjogIk9mZmVyIHByZW1pdW0gc2VydmljZXMgdG8gaGlnaC12YWx1ZSBjdXN0b21lcnMuIiwKICAgICAgICB9KQogICAgaWYgY3Jvc3Nfc2VsbF9vcHBvcnR1bml0aWVzOgogICAgICAgIHJlY29tbWVuZGVkX2FjdGlvbnMuYXBwZW5kKHsKICAgICAgICAgICAgImFjdGlvbiI6ICJDcm9zcy1TZWxsIFByb21vdGlvbiIsCiAgICAgICAgICAgICJyZWFzb24iOiAiUHJvbW90ZSByZWxldmFudCBwcm9kdWN0cyBvciBzZXJ2aWNlcyB0byBlbmdhZ2VkIGN1c3RvbWVycy4iLAogICAgICAgIH0pCiAgICBpZiBjaHVybl9wcmV2ZW50aW9uX29wcG9ydHVuaXRpZXM6CiAgICAgICAgcmVjb21tZW5kZWRfYWN0aW9ucy5hcHBlbmQoewogICAgICAgICAgICAiYWN0aW9uIjogIkNodXJuIFByZXZlbnRpb24gUHJvZ3JhbSIsCiAgICAgICAgICAgICJyZWFzb24iOiAiSW1wbGVtZW50IGEgdGFyZ2V0ZWQgcHJvZ3JhbSB0byByZWR1Y2UgY3VzdG9tZXIgY2h1cm4gcmlzay4iLAogICAgICAgIH0pCiAgICBpZiBlZmZpY2llbmN5X3dpbnM6CiAgICAgICAgcmVjb21tZW5kZWRfYWN0aW9ucy5hcHBlbmQoewogICAgICAgICAgICAiYWN0aW9uIjogIkVmZmljaWVuY3kgT3B0aW1pemF0aW9uIiwKICAgICAgICAgICAgInJlYXNvbiI6ICJBbmFseXplIGFuZCBvcHRpbWl6ZSBidXNpbmVzcyBwcm9jZXNzZXMgZm9yIGluY3JlYXNlZCBlZmZpY2llbmN5LiIsCiAgICAgICAgfSkKICAgIGlmIHJldmVudWVfb3B0aW1pemF0aW9uX29wcG9ydHVuaXRpZXM6CiAgICAgICAgcmVjb21tZW5kZWRfYWN0aW9ucy5hcHBlbmQoewogICAgICAgICAgICAiYWN0aW9uIjogIlJldmVudWUgR3Jvd3RoIFN0cmF0ZWd5IiwKICAgICAgICAgICAgInJlYXNvbiI6ICJEZXZlbG9wIGEgc3RyYXRlZ3kgdG8gZHJpdmUgcmV2ZW51ZSBncm93dGggdGhyb3VnaCB1cHNlbGxzIGFuZCBjcm9zcy1zZWxscy4iLAogICAgICAgIH0pCiAgICByZXN1bHRbInJlY29tbWVuZGVkX2FjdGlvbnMiXS5leHRlbmQocmVjb21tZW5kZWRfYWN0aW9ucykKCiAgICAjIFBvcHVsYXRlIHNjb3JlcwogICAgY29uZmlkZW5jZSA9IDAuOQogICAgcmlza19zY29yZSA9IDAuNwogICAgcHJpb3JpdHkgPSAwLjgKICAgIHJlc3VsdFsic2NvcmVzIl0gPSB7ImNvbmZpZGVuY2UiOiBjb25maWRlbmNlLCAicmlza19zY29yZSI6IHJpc2tfc2NvcmUsICJwcmlvcml0eSI6IHByaW9yaXR5fQoKICAgICMgUG9wdWxhdGUgZGV0YWlscwogICAgcmVzdWx0WyJkZXRhaWxzIl0gPSB7CiAgICAgICAgInVzZV9jYXNlIjogdXNlX2Nhc2UsCiAgICAgICAgImNvbmZpZyI6IGNvbmZpZywKICAgIH0="
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
