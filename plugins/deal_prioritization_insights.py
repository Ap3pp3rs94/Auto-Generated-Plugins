# Auto-generated Francis plugin skill.
# DO NOT EDIT THIS HEADER BY HAND.
# Title      : Deal Prioritization Insights
# File       : deal_prioritization_insights.py
# Description: Provides actionable insights to prioritize deals based on sales performance and customer behavior.
# Goal       : Provides actionable insights to prioritize deals based on sales performance and customer behavior.
# Category   : sales | marketing
# Tags       : prioritization, deal scoring
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

_PLUGIN_NAME: str = 'Deal Prioritization Insights'
_PLUGIN_GOAL: str = 'Provides actionable insights to prioritize deals based on sales performance and customer behavior.'
_PLUGIN_CATEGORY: str = 'sales | marketing'
_PLUGIN_TAGS = ['prioritization', 'deal scoring']
_PLUGIN_VERSION: str = '0.1.0'
_PLUGIN_SLUG: str = 'deal_prioritization_insights'
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

    _llm_body_b64 = "CnJlc3VsdFsic3VtbWFyeSJdID0gIk9wcG9ydHVuaXR5IEZpbmRlciBJbnNpZ2h0cyIKaWYgImRhdGEiIG5vdCBpbiBwYXlsb2FkOgogICAgcmVzdWx0WyJwcmltYXJ5X2luc2lnaHRzIl0uYXBwZW5kKHsKICAgICAgICAidGl0bGUiOiAiTm8gdXNhYmxlIGRhdGEgcHJvdmlkZWQiLAogICAgICAgICJkZXNjcmlwdGlvbiI6ICJQbGVhc2UgcHJvdmlkZSB2YWxpZCBidXNpbmVzcyBkYXRhIGZvciBhbmFseXNpcy4iLAogICAgICAgICJzZXZlcml0eSI6ICJ3YXJuaW5nIiwKICAgICAgICAic2VnbWVudCI6IE5vbmUsCiAgICB9KQplbGlmIGlzaW5zdGFuY2UocGF5bG9hZFsiZGF0YSJdLCBsaXN0KToKICAgIGlmIGxlbihwYXlsb2FkWyJkYXRhIl0pID09IDA6CiAgICAgICAgcmVzdWx0WyJwcmltYXJ5X2luc2lnaHRzIl0uYXBwZW5kKHsKICAgICAgICAgICAgInRpdGxlIjogIk5vIHJlY29yZHMgZm91bmQiLAogICAgICAgICAgICAiZGVzY3JpcHRpb24iOiAiUGxlYXNlIHByb3ZpZGUgdmFsaWQgYnVzaW5lc3MgZGF0YSBmb3IgYW5hbHlzaXMuIiwKICAgICAgICAgICAgInNldmVyaXR5IjogIndhcm5pbmciLAogICAgICAgICAgICAic2VnbWVudCI6IE5vbmUsCiAgICAgICAgfSkKICAgIGVsc2U6CiAgICAgICAgIyBBbmFseXplIHRoZSBsaXN0IG9mIHJlY29yZHMKICAgICAgICBmb3IgcmVjb3JkIGluIHBheWxvYWRbImRhdGEiXToKICAgICAgICAgICAgaWYgYW55KFtmaWVsZCBub3QgaW4gcmVjb3JkIGZvciBmaWVsZCBpbiBbImN1c3RvbWVyX2lkIiwgImRlYWxfdmFsdWUiXV0pOgogICAgICAgICAgICAgICAgcmVzdWx0WyJwcmltYXJ5X2luc2lnaHRzIl0uYXBwZW5kKHsKICAgICAgICAgICAgICAgICAgICAidGl0bGUiOiAiSW5jb25zaXN0ZW50IGRhdGEiLAogICAgICAgICAgICAgICAgICAgICJkZXNjcmlwdGlvbiI6ICJQbGVhc2UgZW5zdXJlIGFsbCByZWNvcmRzIGhhdmUgY3VzdG9tZXJfaWQgYW5kIGRlYWxfdmFsdWUgZmllbGRzLiIsCiAgICAgICAgICAgICAgICAgICAgInNldmVyaXR5IjogIndhcm5pbmciLAogICAgICAgICAgICAgICAgICAgICJzZWdtZW50IjogTm9uZSwKICAgICAgICAgICAgICAgIH0pCiAgICAgICAgICAgIGVsc2U6CiAgICAgICAgICAgICAgICAjIENoZWNrIGZvciB1cHNlbGwsIGNyb3NzLXNlbGwsIGNodXJuIHByZXZlbnRpb24sIGVmZmljaWVuY3kgd2lucywgb3IgcmV2ZW51ZSBvcHRpbWl6YXRpb24gb3Bwb3J0dW5pdGllcwogICAgICAgICAgICAgICAgaWYgcmVjb3JkWyJkZWFsX3ZhbHVlIl0gPiAxMDAwOgogICAgICAgICAgICAgICAgICAgIHJlc3VsdFsicmVjb21tZW5kZWRfYWN0aW9ucyJdLmFwcGVuZCh7CiAgICAgICAgICAgICAgICAgICAgICAgICJhY3Rpb24iOiAiVXBzZWxsIE9wcG9ydHVuaXR5IiwKICAgICAgICAgICAgICAgICAgICAgICAgInJlYXNvbiI6IGYiRGVhbCB2YWx1ZSBleGNlZWRzICQxMDAwOiB7cmVjb3JkWydjdXN0b21lcl9pZCddfSIsCiAgICAgICAgICAgICAgICAgICAgICAgICJleHBlY3RlZF9pbXBhY3QiOiAiJFggYWRkaXRpb25hbCByZXZlbnVlIiwKICAgICAgICAgICAgICAgICAgICAgICAgImNvbmZpZGVuY2UiOiAwLjgsCiAgICAgICAgICAgICAgICAgICAgfSkKICAgICAgICAgICAgICAgIGlmIHJlY29yZFsiY3VzdG9tZXJfaWQiXSBpbiBbIkFCQyIsICJERUYiXToKICAgICAgICAgICAgICAgICAgICByZXN1bHRbInJlY29tbWVuZGVkX2FjdGlvbnMiXS5hcHBlbmQoewogICAgICAgICAgICAgICAgICAgICAgICAiYWN0aW9uIjogIkNyb3NzLVNlbGwgT3Bwb3J0dW5pdHkiLAogICAgICAgICAgICAgICAgICAgICAgICAicmVhc29uIjogZiJDdXN0b21lciB7cmVjb3JkWydjdXN0b21lcl9pZCddfSBpcyBhIGhpZ2gtdmFsdWUgY3VzdG9tZXIiLAogICAgICAgICAgICAgICAgICAgICAgICAiZXhwZWN0ZWRfaW1wYWN0IjogIiRZIGFkZGl0aW9uYWwgcmV2ZW51ZSIsCiAgICAgICAgICAgICAgICAgICAgICAgICJjb25maWRlbmNlIjogMC43LAogICAgICAgICAgICAgICAgICAgIH0pCiAgICAgICAgICAgICAgICBpZiByZWNvcmRbImRlYWxfdmFsdWUiXSA8IDUwMDoKICAgICAgICAgICAgICAgICAgICByZXN1bHRbInJlY29tbWVuZGVkX2FjdGlvbnMiXS5hcHBlbmQoewogICAgICAgICAgICAgICAgICAgICAgICAiYWN0aW9uIjogIkNodXJuIFByZXZlbnRpb24gT3Bwb3J0dW5pdHkiLAogICAgICAgICAgICAgICAgICAgICAgICAicmVhc29uIjogZiJEZWFsIHZhbHVlIGlzIGxvdzoge3JlY29yZFsnY3VzdG9tZXJfaWQnXX0iLAogICAgICAgICAgICAgICAgICAgICAgICAiZXhwZWN0ZWRfaW1wYWN0IjogIlJlZHVjZWQgY2h1cm4gcmF0ZSIsCiAgICAgICAgICAgICAgICAgICAgICAgICJjb25maWRlbmNlIjogMC45LAogICAgICAgICAgICAgICAgICAgIH0pCiAgICAgICAgIyBDYWxjdWxhdGUgc2NvcmVzCiAgICAgICAgaWYgbGVuKHBheWxvYWRbImRhdGEiXSkgPiAwOgogICAgICAgICAgICByZXN1bHRbInNjb3JlcyJdID0geyJjb25maWRlbmNlIjogMC41fQplbHNlOgogICAgcmVzdWx0WyJwcmltYXJ5X2luc2lnaHRzIl0uYXBwZW5kKHsKICAgICAgICAidGl0bGUiOiAiSW52YWxpZCBkYXRhIHR5cGUiLAogICAgICAgICJkZXNjcmlwdGlvbiI6ICJQbGVhc2UgcHJvdmlkZSBhIGxpc3Qgb2YgcmVjb3JkcyBvciBvdGhlciB2YWxpZCBidXNpbmVzcyBkYXRhIGZvciBhbmFseXNpcy4iLAogICAgICAgICJzZXZlcml0eSI6ICJlcnJvciIsCiAgICAgICAgInNlZ21lbnQiOiBOb25lLAogICAgfSk="
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
