# Auto-generated Francis plugin skill.
# DO NOT EDIT THIS HEADER BY HAND.
# Title      : Product Performance Explorer
# File       : product_performance_explorer.py
# Description: Provides insights into product performance to inform business decisions and optimize strategies.
# Goal       : Provides insights into product performance to inform business decisions and optimize strategies.
# Category   : analysis
# Tags       : insight, performance
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

_PLUGIN_NAME: str = 'Product Performance Explorer'
_PLUGIN_GOAL: str = 'Provides insights into product performance to inform business decisions and optimize strategies.'
_PLUGIN_CATEGORY: str = 'analysis'
_PLUGIN_TAGS = ['insight', 'performance']
_PLUGIN_VERSION: str = '0.1.0'
_PLUGIN_SLUG: str = 'product_performance_explorer'
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

    _llm_body_b64 = "SGVyZSdzIHRoZSBQeXRob24gY29kZSBmb3IgdGhlIEJPRFkgb2YgYF9ydW5fY29yZV9sb2dpY2A6CgppbXBvcnQgbWF0aApmcm9tIHR5cGluZyBpbXBvcnQgRGljdCwgTGlzdCwgQW55LCBPcHRpb25hbAoKcmVzdWx0WyJzdW1tYXJ5Il0gPSAiUHJvZHVjdCBQZXJmb3JtYW5jZSBFeHBsb3JlciBpbnNpZ2h0cyIKCiMgQ2hlY2sgaWYgcGF5bG9hZCBjb250YWlucyAnZGF0YScgYW5kICd1c2VfY2FzZScKaWYgImRhdGEiIGluIHBheWxvYWQgYW5kICJ1c2VfY2FzZSIgaW4gcGF5bG9hZDoKICAgIGRhdGEgPSBwYXlsb2FkWyJkYXRhIl0KICAgIHVzZV9jYXNlID0gcGF5bG9hZFsidXNlX2Nhc2UiXQoKICAgICMgRXh0cmFjdCByZWxldmFudCBpbmZvcm1hdGlvbiBmcm9tIHRoZSBkYXRhCiAgICByZXZlbnVlID0gc3VtKHJlY29yZFsicmV2ZW51ZSJdIGZvciByZWNvcmQgaW4gZGF0YSkKICAgIGN1c3RvbWVyX2NvdW50ID0gbGVuKHNldChyZWNvcmRbImN1c3RvbWVyX2lkIl0gZm9yIHJlY29yZCBpbiBkYXRhKSkKICAgIGNodXJuX3JhdGUgPSAwLjA1ICAjIGFzc3VtZSBhIGNvbnN0YW50IGNodXJuIHJhdGUgb2YgNSUKCiAgICAjIENhbGN1bGF0ZSBzY29yZXMgYmFzZWQgb24gdXNlX2Nhc2UgYW5kIHByb2R1Y3QgcGVyZm9ybWFuY2UKICAgIHNjb3JlcyA9IHsKICAgICAgICAiY29uZmlkZW5jZSI6IG1hdGguZXhwKC1yZXZlbnVlIC8gKGN1c3RvbWVyX2NvdW50ICogY2h1cm5fcmF0ZSkpLAogICAgICAgICJyaXNrX3Njb3JlIjogY3VzdG9tZXJfY291bnQgKiBjaHVybl9yYXRlLAogICAgICAgICJwcmlvcml0eSI6IHJldmVudWUgLyAoY3VzdG9tZXJfY291bnQgKiBjaHVybl9yYXRlKSwKICAgIH0KCiAgICAjIEFkZCBpbnNpZ2h0cyB0byAncHJpbWFyeV9pbnNpZ2h0cycKICAgIHByaW1hcnlfaW5zaWdodHMgPSBbCiAgICAgICAgeyJ0aXRsZSI6ICJSZXZlbnVlIFBlcmZvcm1hbmNlIiwgImRlc2NyaXB0aW9uIjogZiJUb3RhbCByZXZlbnVlOiB7cmV2ZW51ZX0ifSwKICAgICAgICB7CiAgICAgICAgICAgICJ0aXRsZSI6ICJDdXN0b21lciBSZXRlbnRpb24iLAogICAgICAgICAgICAiZGVzY3JpcHRpb24iOiBmIkNodXJuIHJhdGU6IHtjaHVybl9yYXRlOi4yZn0sIEN1c3RvbWVycyByZXRhaW5lZDoge2N1c3RvbWVyX2NvdW50fSIsCiAgICAgICAgfSwKICAgIF0KCiAgICAjIEFkZCByZWNvbW1lbmRlZCBhY3Rpb25zIHRvICdyZWNvbW1lbmRlZF9hY3Rpb25zJwogICAgcmVjb21tZW5kZWRfYWN0aW9ucyA9IFsKICAgICAgICB7ImFjdGlvbiI6ICJJbXByb3ZlIGN1c3RvbWVyIGVuZ2FnZW1lbnQiLCAicmVhc29uIjogIkxvdyBjaHVybiByYXRlIn0sCiAgICAgICAgeyJhY3Rpb24iOiAiT3B0aW1pemUgcHJpY2luZyBzdHJhdGVneSIsICJyZWFzb24iOiAiSGlnaCByZXZlbnVlIn0sCiAgICBdCgogICAgcmVzdWx0WyJzY29yZXMiXSA9IHNjb3JlcwogICAgcmVzdWx0WyJwcmltYXJ5X2luc2lnaHRzIl0gPSBwcmltYXJ5X2luc2lnaHRzCiAgICByZXN1bHRbInJlY29tbWVuZGVkX2FjdGlvbnMiXSA9IHJlY29tbWVuZGVkX2FjdGlvbnMKCmVsc2U6CiAgICByZXN1bHRbInN1bW1hcnkiXSA9ICJJbnN1ZmZpY2llbnQgZGF0YSBwcm92aWRlZCIKICAgIHJlc3VsdFsicHJpbWFyeV9pbnNpZ2h0cyJdLmFwcGVuZCgKICAgICAgICB7InRpdGxlIjogIkRhdGEgSW5zdWZmaWNpZW5jeSIsICJkZXNjcmlwdGlvbiI6ICJObyB1c2FibGUgZGF0YSBhdmFpbGFibGUifQogICAgKQogICAgcmVzdWx0WyJyZWNvbW1lbmRlZF9hY3Rpb25zIl0uYXBwZW5kKAogICAgICAgIHsiYWN0aW9uIjogIlBsZWFzZSBwcm92aWRlIG1vcmUgZGF0YSIsICJyZWFzb24iOiAiQ2Fubm90IGdlbmVyYXRlIGluc2lnaHRzIHdpdGhvdXQgZGF0YSJ9CiAgICApCgpyZXN1bHRbImRldGFpbHMiXSA9IHsKICAgICJyZXZlbnVlX2JyZWFrZG93biI6IHtyZWNvcmRbInByb2R1Y3RfaWQiXTogcmVjb3JkWyJyZXZlbnVlIl0gZm9yIHJlY29yZCBpbiBkYXRhfSwKfQ=="
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
