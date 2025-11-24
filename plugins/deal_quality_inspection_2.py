# Auto-generated Francis plugin skill.
# DO NOT EDIT THIS HEADER BY HAND.
# Title      : Deal Quality Inspector
# File       : deal_quality_inspection_2.py
# Description: Identifies potential issues with deals and opportunities to improve their quality and close rates.
# Goal       : Identifies potential issues with deals and opportunities to improve their quality and close rates.
# Category   : sales | marketing | support
# Tags       : quality, inspections
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

_PLUGIN_NAME: str = 'Deal Quality Inspector'
_PLUGIN_GOAL: str = 'Identifies potential issues with deals and opportunities to improve their quality and close rates.'
_PLUGIN_CATEGORY: str = 'sales | marketing | support'
_PLUGIN_TAGS = ['quality', 'inspections']
_PLUGIN_VERSION: str = '0.1.0'
_PLUGIN_SLUG: str = 'deal_quality_inspection_2'
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

    _llm_body_b64 = "SGVyZSBpcyB0aGUgQk9EWSBvZiBgX3J1bl9jb3JlX2xvZ2ljKGNvbnRleHQsIHBheWxvYWQpYDoKCmlmICJkYXRhIiBub3QgaW4gcGF5bG9hZDoKICAgIHJlc3VsdFsic3VtbWFyeSJdID0gIk5vIHVzYWJsZSBkYXRhIHByb3ZpZGVkLiIKICAgIHJlc3VsdFsicHJpbWFyeV9pbnNpZ2h0cyJdLmFwcGVuZCh7InRpdGxlIjogIkRhdGEgcmVxdWlyZWQiLCAiZGVzY3JpcHRpb24iOiAiUGxlYXNlIHByb3ZpZGUgZGVhbCByZWNvcmRzLiJ9KQogICAgcmVzdWx0WyJyZWNvbW1lbmRlZF9hY3Rpb25zIl0uYXBwZW5kKHsiYWN0aW9uIjogIlVwbG9hZCBkZWFsIGRhdGEiLCAicmVhc29uIjogIlRvIGVuYWJsZSBpbnNpZ2h0cy4ifSkKZWxzZToKICAgIGRlYWxzX2RhdGEgPSBwYXlsb2FkWyJkYXRhIl0KCiAgICBpZiBub3QgZGVhbHNfZGF0YTogICMgbm8gZGVhbHMgb3IgZW1wdHkgbGlzdAogICAgICAgIHJlc3VsdFsic3VtbWFyeSJdID0gIk5vIHVzYWJsZSBkZWFscyBwcm92aWRlZC4iCiAgICAgICAgcmVzdWx0WyJwcmltYXJ5X2luc2lnaHRzIl0uYXBwZW5kKHsidGl0bGUiOiAiRW1wdHkgZGVhbCBkYXRhc2V0IiwgImRlc2NyaXB0aW9uIjogIlBsZWFzZSBwcm92aWRlIGF0IGxlYXN0IG9uZSBkZWFsIHJlY29yZC4ifSkKICAgICAgICByZXN1bHRbInJlY29tbWVuZGVkX2FjdGlvbnMiXS5hcHBlbmQoeyJhY3Rpb24iOiAiVXBsb2FkIGRlYWwgZGF0YSIsICJyZWFzb24iOiAiVG8gZW5hYmxlIGluc2lnaHRzLiJ9KQogICAgZWxzZToKICAgICAgICAjIERvIHNvbWUgcXVhbGl0eSBjaGVja3Mgb24gdGhlIGRlYWxzIChlLmcuLCBjaGVjayBmb3IgbWlzc2luZyBmaWVsZHMpCiAgICAgICAgIyBDYWxjdWxhdGUgc2NvcmVzIGFuZCBpbnNpZ2h0cwogICAgICAgICMgLi4uCgogICAgICAgIGlmICJ1c2VfY2FzZSIgaW4gcGF5bG9hZDogICMgdXNlLWNhc2UgYXdhcmUgaW5zaWdodHMKICAgICAgICAgICAgaWYgcGF5bG9hZFsidXNlX2Nhc2UiXSA9PSAiRmluZCBjaHVybiByaXNrIHNpZ25hbHMiOgogICAgICAgICAgICAgICAgIyBVc2UtY2FzZSBzcGVjaWZpYyBsb2dpYyBoZXJlLi4uCiAgICAgICAgICAgICAgICByZXN1bHRbInByaW1hcnlfaW5zaWdodHMiXS5hcHBlbmQoeyJ0aXRsZSI6ICJDaHVybiBSaXNrIERldGVjdGVkIiwgImRlc2NyaXB0aW9uIjogIkRlYWwgaXMgYXQgcmlzayBvZiBiZWluZyBsb3N0LiJ9KQogICAgICAgICAgICAgICAgcmVzdWx0WyJyZWNvbW1lbmRlZF9hY3Rpb25zIl0uYXBwZW5kKHsiYWN0aW9uIjogIkZvbGxvdyB1cCB3aXRoIHRoZSBjdXN0b21lciIsICJyZWFzb24iOiAiVG8gcHJldmVudCBjaHVybi4ifSkKICAgICAgICAgICAgZWxpZiBwYXlsb2FkWyJ1c2VfY2FzZSJdID09ICJIaWdobGlnaHQgZXhwYW5zaW9uIG9wcG9ydHVuaXRpZXMiOgogICAgICAgICAgICAgICAgIyBVc2UtY2FzZSBzcGVjaWZpYyBsb2dpYyBoZXJlLi4uCiAgICAgICAgICAgICAgICByZXN1bHRbInByaW1hcnlfaW5zaWdodHMiXS5hcHBlbmQoeyJ0aXRsZSI6ICJFeHBhbnNpb24gT3Bwb3J0dW5pdHkgRm91bmQiLCAiZGVzY3JpcHRpb24iOiAiRGVhbCBoYXMgcG90ZW50aWFsIGZvciBncm93dGguIn0pCiAgICAgICAgICAgICAgICByZXN1bHRbInJlY29tbWVuZGVkX2FjdGlvbnMiXS5hcHBlbmQoeyJhY3Rpb24iOiAiRGV2ZWxvcCBhIGdyb3d0aCBzdHJhdGVneSIsICJyZWFzb24iOiAiVG8gY2FwaXRhbGl6ZSBvbiB0aGUgb3Bwb3J0dW5pdHkuIn0pCiAgICAgICAgZWxzZToKICAgICAgICAgICAgIyBHZW5lcmFsIGluc2lnaHRzCiAgICAgICAgICAgICMgLi4uCgogICAgICAgIGlmICJjb25maWciIGluIHBheWxvYWQ6ICAjIGNvbmZpZy1iYXNlZCBpbnNpZ2h0cwogICAgICAgICAgICByaXNrX3RvbGVyYW5jZSA9IHBheWxvYWRbImNvbmZpZyJdWyJyaXNrX3RvbGVyYW5jZSJdCiAgICAgICAgICAgIGlmIHJpc2tfdG9sZXJhbmNlID09ICJsb3ciOgogICAgICAgICAgICAgICAgIyBMb3ctcmlzayB0b2xlcmFuY2UgbG9naWMgaGVyZS4uLgogICAgICAgICAgICAgICAgcmVzdWx0WyJwcmltYXJ5X2luc2lnaHRzIl0uYXBwZW5kKHsidGl0bGUiOiAiTG93LVJpc2sgT3Bwb3J0dW5pdHkiLCAiZGVzY3JpcHRpb24iOiAiRGVhbCBpcyBsaWtlbHkgdG8gY2xvc2UuIn0pCiAgICAgICAgICAgICAgICByZXN1bHRbInJlY29tbWVuZGVkX2FjdGlvbnMiXS5hcHBlbmQoeyJhY3Rpb24iOiAiTW92ZSBmb3J3YXJkIHdpdGggdGhlIGRlYWwiLCAicmVhc29uIjogIkJhc2VkIG9uIGxvdyByaXNrLiJ9KQogICAgICAgICAgICBlbGlmIHJpc2tfdG9sZXJhbmNlID09ICJoaWdoIjoKICAgICAgICAgICAgICAgICMgSGlnaC1yaXNrIHRvbGVyYW5jZSBsb2dpYyBoZXJlLi4uCiAgICAgICAgICAgICAgICByZXN1bHRbInByaW1hcnlfaW5zaWdodHMiXS5hcHBlbmQoeyJ0aXRsZSI6ICJIaWdoLVJpc2sgT3Bwb3J0dW5pdHkiLCAiZGVzY3JpcHRpb24iOiAiRGVhbCBpcyBsaWtlbHkgdG8gYmUgY2hhbGxlbmdpbmcuIn0pCiAgICAgICAgICAgICAgICByZXN1bHRbInJlY29tbWVuZGVkX2FjdGlvbnMiXS5hcHBlbmQoeyJhY3Rpb24iOiAiQWRqdXN0IHRoZSBzYWxlcyBzdHJhdGVneSIsICJyZWFzb24iOiAiVG8gbWl0aWdhdGUgcmlzay4ifSkKCiAgICAgICAgaWYgImNvbnRleHQiIGluIHBheWxvYWQ6ICAjIGNvbnRleHQtYmFzZWQgaW5zaWdodHMKICAgICAgICAgICAgIyBDb250ZXh0LXNwZWNpZmljIGxvZ2ljIGhlcmUuLi4KICAgICAgICAgICAgcmVzdWx0WyJwcmltYXJ5X2luc2lnaHRzIl0uYXBwZW5kKHsidGl0bGUiOiAiQ29udGV4dHVhbCBJbnNpZ2h0IiwgImRlc2NyaXB0aW9uIjogIkRlYWwgaXMgYWxpZ25lZCB3aXRoIGNvbXBhbnkgZ29hbHMuIn0pCiAgICAgICAgICAgIHJlc3VsdFsicmVjb21tZW5kZWRfYWN0aW9ucyJdLmFwcGVuZCh7ImFjdGlvbiI6ICJNb3ZlIGZvcndhcmQgd2l0aCB0aGUgZGVhbCIsICJyZWFzb24iOiAiQmFzZWQgb24gY29udGV4dHVhbCBhbGlnbm1lbnQuIn0pCgpyZXN1bHRbInNjb3JlcyJdWyJjb25maWRlbmNlIl0gPSAwLjg1ICAjIGV4YW1wbGUgY29uZmlkZW5jZSBzY29yZQ=="
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
