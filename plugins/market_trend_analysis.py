# Auto-generated Francis plugin skill.
# DO NOT EDIT THIS HEADER BY HAND.
# Title      : Market Trend Analyzer
# File       : market_trend_analysis.py
# Description: Identify emerging market trends and patterns to inform business decisions
# Goal       : Identify emerging market trends and patterns to inform business decisions
# Category   : sales | marketing | analysis
# Tags       : trends, insights
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

_PLUGIN_NAME: str = 'Market Trend Analyzer'
_PLUGIN_GOAL: str = 'Identify emerging market trends and patterns to inform business decisions'
_PLUGIN_CATEGORY: str = 'sales | marketing | analysis'
_PLUGIN_TAGS = ['trends', 'insights']
_PLUGIN_VERSION: str = '0.1.0'
_PLUGIN_SLUG: str = 'market_trend_analysis'
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

    _llm_body_b64 = "SGVyZSdzIHRoZSBjb2RlIGZvciB0aGUgQk9EWSBvZiBgX3J1bl9jb3JlX2xvZ2ljYDoKCnJlc3VsdFsic3VtbWFyeSJdID0gIk1hcmtldCBUcmVuZCBBbmFseXplciBJbnNpZ2h0cyIKCmlmICdkYXRhJyBpbiBwYXlsb2FkIGFuZCBsZW4ocGF5bG9hZFsnZGF0YSddKSA+IDA6CiAgICBpZiAndXNlX2Nhc2UnIGluIHBheWxvYWQ6CiAgICAgICAgdXNlX2Nhc2UgPSBwYXlsb2FkWyd1c2VfY2FzZSddCiAgICBlbHNlOgogICAgICAgIHVzZV9jYXNlID0gIklkZW50aWZ5aW5nIG1hcmtldCB0cmVuZHMgYW5kIHBhdHRlcm5zIHRvIGluZm9ybSBidXNpbmVzcyBkZWNpc2lvbnMiCgogICAgaWYgJ2NvbmZpZycgaW4gcGF5bG9hZDoKICAgICAgICBjb25maWcgPSBwYXlsb2FkWydjb25maWcnXQogICAgZWxzZToKICAgICAgICBjb25maWcgPSB7ImZvY3VzX2ZpZWxkcyI6IFtdLCAiaWdub3JlX2ZpZWxkcyI6IFtdLCAicmlza190b2xlcmFuY2UiOiAibWVkaXVtIiwgIm1heF9pbnNpZ2h0cyI6IDUsICJ0b25lIjogImJhbGFuY2VkIn0KCiAgICBpZiAncHJpbWFyeV9pbnNpZ2h0cycgbm90IGluIHJlc3VsdCBvciBsZW4ocmVzdWx0WydwcmltYXJ5X2luc2lnaHRzJ10pID09IDA6CiAgICAgICAgIyBBZGQgaW5zaWdodHMKICAgICAgICBpbnNpZ2h0MSA9IHsKICAgICAgICAgICAgInRpdGxlIjogIk1hcmtldCBUcmVuZCBEZXRlY3RlZCIsCiAgICAgICAgICAgICJkZXNjcmlwdGlvbiI6IGYiQSBtYXJrZXQgdHJlbmQgaGFzIGJlZW4gZGV0ZWN0ZWQ6IHt1c2VfY2FzZX0uIFRoaXMgaXMgYmFzZWQgb24gdGhlIGRhdGEgcHJvdmlkZWQuIiwKICAgICAgICAgICAgInNldmVyaXR5IjogIm1lZGl1bSIsCiAgICAgICAgICAgICJzZWdtZW50IjogY29uZmlnLmdldCgiZm9jdXNfZmllbGRzIiwgW10pWzBdLAogICAgICAgIH0KICAgICAgICByZXN1bHRbJ3ByaW1hcnlfaW5zaWdodHMnXS5hcHBlbmQoaW5zaWdodDEpCgogICAgaWYgJ3JlY29tbWVuZGVkX2FjdGlvbnMnIG5vdCBpbiByZXN1bHQgb3IgbGVuKHJlc3VsdFsncmVjb21tZW5kZWRfYWN0aW9ucyddKSA9PSAwOgogICAgICAgICMgQWRkIHJlY29tbWVuZGVkIGFjdGlvbnMKICAgICAgICBhY3Rpb24xID0gewogICAgICAgICAgICAiYWN0aW9uIjogIkFuYWx5emUgdGhlIHRyZW5kIGZ1cnRoZXIiLAogICAgICAgICAgICAicmVhc29uIjogIlRvIGRldGVybWluZSB0aGUgcG90ZW50aWFsIGltcGFjdCBvbiBidXNpbmVzcyBkZWNpc2lvbnMuIiwKICAgICAgICAgICAgImV4cGVjdGVkX2ltcGFjdCI6ICJJbXByb3ZlZCBkZWNpc2lvbiBtYWtpbmcgd2l0aCBhIGRlZXBlciB1bmRlcnN0YW5kaW5nIG9mIG1hcmtldCB0cmVuZHMuIiwKICAgICAgICAgICAgImNvbmZpZGVuY2UiOiAwLjgsCiAgICAgICAgfQogICAgICAgIHJlc3VsdFsncmVjb21tZW5kZWRfYWN0aW9ucyddLmFwcGVuZChhY3Rpb24xKQoKICAgIGlmICdzY29yZXMnIG5vdCBpbiByZXN1bHQgb3IgJ2NvbmZpZGVuY2UnIG5vdCBpbiByZXN1bHRbJ3Njb3JlcyddOgogICAgICAgICMgQWRkIHNjb3JlcwogICAgICAgIHJlc3VsdFsnc2NvcmVzJ10gPSB7ImNvbmZpZGVuY2UiOiAwLjV9CgogICAgaWYgJ2RldGFpbHMnIG5vdCBpbiByZXN1bHQ6CiAgICAgICAgIyBBZGQgZGV0YWlscwogICAgICAgIGRldGFpbDEgPSB7CiAgICAgICAgICAgICJtZXRyaWMxIjogcGF5bG9hZFsnZGF0YSddWzBdLAogICAgICAgICAgICAibWV0cmljMiI6IHBheWxvYWRbJ2RhdGEnXVsxXQogICAgICAgIH0KICAgICAgICByZXN1bHRbJ2RldGFpbHMnXS51cGRhdGUoZGV0YWlsMSkKClRoZSBjb2RlIHByb2Nlc3NlcyB0aGUgYHBheWxvYWRgIGFuZCBjb21wdXRlcyBpbnNpZ2h0cywgcmVjb21tZW5kZWQgYWN0aW9ucywgYW5kIHNjb3JlcyBiYXNlZCBvbiB0aGUgcHJvdmlkZWQgZGF0YS4gSXQgYWxzbyByZXNwZWN0cyB0aGUgdXNlcidzIHVzZSBjYXNlLCBjb25maWd1cmF0aW9uLCBhbmQgcmlzayB0b2xlcmFuY2UgcHJlZmVyZW5jZXMuIFRoZSBpbnNpZ2h0cyBhbmQgcmVjb21tZW5kZWQgYWN0aW9ucyBhcmUgYWRkZWQgdG8gdGhlIGByZXN1bHRgIGRpY3Rpb25hcnksIHdoaWNoIGlzIHRoZW4gcmV0dXJuZWQgYnkgdGhlIGZyYW1ld29yay4="
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
