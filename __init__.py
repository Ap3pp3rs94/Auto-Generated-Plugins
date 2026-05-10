from __future__ import annotations

"""
Francis Plugin Factory – Orchestrator

This module coordinates:
- Station B: code generation for a plugin given a PluginSpec
- Station C: validation + execution of the generated plugin
- Registry: persistent registration of the resulting plugin

Primary surface:
- FactoryResult: dataclass capturing an end-to-end run
- run_factory_for_spec(spec, ...) -> FactoryResult
- run_factory_sync(spec, ...) -> FactoryResult (backwards-compatible wrapper)
"""

import asyncio
import inspect
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Optional

try:
    from .plugin_spec import PluginSpec
except ImportError:  # pragma: no cover - direct local execution
    from plugin_spec import PluginSpec

try:
    from .plugin_registry import FRANCIS_ROOT, register_plugin
except ImportError:  # pragma: no cover - direct local execution
    from plugin_registry import FRANCIS_ROOT, register_plugin

try:
    from .station_c_validator import ValidationError
except ImportError:  # pragma: no cover - direct local execution
    from station_c_validator import ValidationError

try:
    from .station_b import (
        StationBConfig,
        StationBResult,
        generate_plugin_source,
    )
    from .station_c import run_station_c
except ImportError:  # pragma: no cover - sidecar repo without parent stations
    try:
        from station_b import (  # type: ignore
            StationBConfig,
            StationBResult,
            generate_plugin_source,
        )
        from station_c import run_station_c  # type: ignore
    except ImportError:
        StationBConfig = None  # type: ignore[assignment]
        StationBResult = Any  # type: ignore[assignment]

        def generate_plugin_source(*args: Any, **kwargs: Any) -> Any:
            raise RuntimeError("Station B is not available in this checkout.")

        def run_station_c(*args: Any, **kwargs: Any) -> Any:
            raise RuntimeError("Station C is not available in this checkout.")


# =====================================================================
# Paths
# =====================================================================

PLUGINS_DIR = FRANCIS_ROOT / "plugins"
PLUGINS_DIR.mkdir(parents=True, exist_ok=True)


# =====================================================================
# Data structures
# =====================================================================

@dataclass
class FactoryResult:
    """
    End-to-end result of a single factory run for a PluginSpec.
    """

    spec: PluginSpec
    plugin_path: Path

    # Station B
    station_b_result: StationBResult
    capability_type: Optional[str] = None

    # Station C
    station_c_result: Optional[Dict[str, Any]] = None

    # Registry
    registry_record: Optional[Any] = None

    # Overall status / diagnostics
    status: str = "succeeded"  # "succeeded" | "failed"
    failure_stage: Optional[str] = None  # "station_b" | "station_c" | "registry"
    failure_reason: Optional[str] = None


# =====================================================================
# Helpers – Station B / Station C calls
# =====================================================================

def _write_plugin_file(spec: PluginSpec, source: str) -> Path:
    """
    Write a plugin source file under PLUGINS_DIR based on the PluginSpec slug.
    """
    target = PLUGINS_DIR / f"{spec.slug}.py"
    target.write_text(source, encoding="utf-8")
    return target


def _call_station_b(
    spec: PluginSpec,
    config: Optional[StationBConfig] = None,
    *,
    capability_type: Optional[str] = None,
    intended_domain: Optional[str] = None,
    extra_instructions: Optional[str] = None,
) -> StationBResult:
    """
    Invoke Station B to generate plugin source.

    This is signature-flexible and supports both sync and async
    implementations of generate_plugin_source.
    """
    if config is None:
        config = StationBConfig()

    sig = inspect.signature(generate_plugin_source)
    kwargs: Dict[str, Any] = {}

    for name, param in sig.parameters.items():
        if name == "spec":
            kwargs["spec"] = spec
        elif name == "config":
            kwargs["config"] = config
        elif name == "station_b_config":
            kwargs["station_b_config"] = config
        elif name == "capability_type":
            kwargs["capability_type"] = capability_type
        elif name == "intended_domain":
            kwargs["intended_domain"] = intended_domain
        elif name == "extra_instructions":
            kwargs["extra_instructions"] = extra_instructions
        elif param.default is not param.empty:
            # Optional param – let it use its default
            continue
        else:
            raise TypeError(
                f"generate_plugin_source() has required parameter '{name}' "
                "that the factory does not know how to supply."
            )

    result = generate_plugin_source(**kwargs)

    # Support async Station B implementations
    if inspect.iscoroutine(result):
        result = asyncio.run(result)

    if not isinstance(result, StationBResult):
        raise TypeError(
            f"generate_plugin_source() returned {type(result)!r}, "
            "expected StationBResult."
        )
    return result


def _call_station_c(
    plugin_path: Path,
    spec: PluginSpec,
    *,
    user_id: str,
    payload: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Invoke Station C in a signature-adaptive way so we don't tightly couple
    to its exact function signature.

    Supports Station C implementations requiring:
      - plugin_path
      - plugin_module
      - spec
      - user_id
      - payload
      - extra_kwargs (optional dict)
    """
    import importlib.util

    # 1) Dynamically import the plugin module
    module_name = spec.slug.replace("-", "_")
    module_spec = importlib.util.spec_from_file_location(module_name, plugin_path)
    if module_spec is None or module_spec.loader is None:
        raise RuntimeError(f"Unable to load plugin module from {plugin_path}")

    plugin_module = importlib.util.module_from_spec(module_spec)
    module_spec.loader.exec_module(plugin_module)

    # 2) Prepare kwargs for run_station_c based on its signature
    sig = inspect.signature(run_station_c)
    kwargs: Dict[str, Any] = {}

    for name, param in sig.parameters.items():
        if name == "plugin_path":
            kwargs["plugin_path"] = plugin_path
        elif name == "plugin_module":
            kwargs["plugin_module"] = plugin_module
        elif name == "spec":
            kwargs["spec"] = spec
        elif name == "user_id":
            kwargs["user_id"] = user_id
        elif name == "payload":
            kwargs["payload"] = payload
        elif name == "extra_kwargs":
            # Station C wants a dict of extra kwargs; factory doesn't need to pass any yet.
            kwargs["extra_kwargs"] = {}
        elif param.default is not param.empty:
            # Optional – skip and let it use its default
            continue
        else:
            raise TypeError(
                f"run_station_c() has required parameter '{name}' "
                "that the factory does not know how to supply."
            )

    # 3) Execute Station C (supports sync or async)
    result = run_station_c(**kwargs)
    if inspect.iscoroutine(result):
        result = asyncio.run(result)

    if not isinstance(result, Dict):
        raise TypeError(
            f"run_station_c() returned {type(result)!r}, expected dict result envelope."
        )
    return result


# =====================================================================
# Public API – Single-run orchestrator
# =====================================================================

def run_factory_for_spec(
    spec: PluginSpec,
    *,
    user_id: str = "factory-smoke-test",
    payload: Optional[Dict[str, Any]] = None,
    station_b_config: Optional[StationBConfig] = None,
    capability_type: Optional[str] = None,
    intended_domain: Optional[str] = None,
    extra_instructions: Optional[str] = None,
    auto_register: bool = True,
) -> FactoryResult:
    """
    Run the full A → B → C → registry pipeline for a single PluginSpec.

    - Generate plugin source with Station B
    - Write the plugin file to plugins/
    - Run Station C validation + execution
    - Register the plugin in the registry (if auto_register=True)
    """

    # ---------------------------------------
    # Station B – generate plugin source
    # ---------------------------------------
    try:
        station_b_result = _call_station_b(
            spec,
            station_b_config,
            capability_type=capability_type,
            intended_domain=intended_domain,
            extra_instructions=extra_instructions,
        )
        source = station_b_result.source
    except Exception as exc:  # noqa: BLE001
        # Hard failure at Station B – nothing else to do
        dummy_path = PLUGINS_DIR / f"{spec.slug}.py"
        return FactoryResult(
            spec=spec,
            plugin_path=dummy_path,
            station_b_result=StationBResult(
                source="",
                raw_llm_output="",
                capability_type=None,
                system_prompt="",
                user_prompt="",
            ),
            capability_type=None,
            station_c_result=None,
            registry_record=None,
            status="failed",
            failure_stage="station_b",
            failure_reason=f"Station B failed: {exc}",
        )

    # Write plugin file
    plugin_path = _write_plugin_file(spec, source)

    # Capability type (if Station B populated it)
    capability_type = getattr(station_b_result, "capability_type", None) or capability_type

    # ---------------------------------------
    # Station C – validate + execute plugin
    # ---------------------------------------
    if payload is None:
        payload = {"test": "value", "input": "smoke"}

    station_c_result: Optional[Dict[str, Any]] = None
    validation_error: Optional[str] = None
    status: str = "succeeded"
    failure_stage: Optional[str] = None
    failure_reason: Optional[str] = None

    try:
        station_c_result = _call_station_c(
            plugin_path=plugin_path,
            spec=spec,
            user_id=user_id,
            payload=payload,
        )
    except ValidationError as exc:
        status = "failed"
        failure_stage = "station_c"
        validation_error = str(exc)
        failure_reason = f"Station C validation error: {exc}"
    except Exception as exc:  # noqa: BLE001
        status = "failed"
        failure_stage = "station_c"
        validation_error = str(exc)
        failure_reason = f"Station C execution error: {exc}"
    else:
        # Check Station C envelope status
        if isinstance(station_c_result, dict):
            env_status = station_c_result.get("status")
            if env_status != "succeeded":
                status = "failed"
                failure_stage = "station_c"
                validation_error = station_c_result.get("error") or "non-succeeded status"
                failure_reason = (
                    f"Station C returned status={env_status!r}, "
                    f"error={station_c_result.get('error')!r}"
                )

    # ---------------------------------------
    # Registry – record plugin + diagnostics
    # ---------------------------------------
    registry_record: Optional[Any] = None
    if auto_register:
        reg_status = "active" if status == "succeeded" else "failed"

        meta: Dict[str, Any] = {
            "station_b": {
                "capability_type": capability_type,
                "system_prompt": station_b_result.system_prompt,
                "user_prompt": station_b_result.user_prompt,
            },
        }
        if station_b_result.raw_llm_output:
            meta["station_b"]["raw_llm_output"] = station_b_result.raw_llm_output

        if station_c_result is not None:
            meta["station_c"] = station_c_result

        try:
            registry_record = register_plugin(
                slug=spec.slug,
                name=spec.name,
                category=spec.category,
                version=spec.version,
                path=plugin_path,
                capability_type=capability_type,
                tags=spec.tags,
                status=reg_status,
                meta=meta,
                validation_error=validation_error,
            )
        except Exception as exc:  # noqa: BLE001
            status = "failed"
            failure_stage = failure_stage or "registry"
            failure_reason = f"Failed to register plugin: {exc}"

    # Final FactoryResult
    return FactoryResult(
        spec=spec,
        plugin_path=plugin_path,
        station_b_result=station_b_result,
        capability_type=capability_type,
        station_c_result=station_c_result,
        registry_record=registry_record,
        status=status,
        failure_stage=failure_stage,
        failure_reason=failure_reason,
    )


# =====================================================================
# Backwards-compatible sync wrapper
# =====================================================================

def run_factory_sync(
    spec: PluginSpec,
    *,
    user_id: str = "factory-smoke-test",
    payload: Optional[Dict[str, Any]] = None,
    station_b_config: Optional[StationBConfig] = None,
    capability_type: Optional[str] = None,
    intended_domain: Optional[str] = None,
    extra_instructions: Optional[str] = None,
    auto_register: bool = True,
) -> FactoryResult:
    """
    Backwards-compatible synchronous wrapper used by factory_smoke.py.

    Delegates to run_factory_for_spec with the same arguments.
    """
    return run_factory_for_spec(
        spec,
        user_id=user_id,
        payload=payload,
        station_b_config=station_b_config,
        capability_type=capability_type,
        intended_domain=intended_domain,
        extra_instructions=extra_instructions,
        auto_register=auto_register,
    )
