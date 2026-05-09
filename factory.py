from __future__ import annotations

import asyncio
import importlib.util
import logging
import uuid
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Optional

try:
    from .production_queue import ProductionQueue, ProductionTask
    from .plugin_spec import PluginSpec
    from .registry import (
        plugin_path_for_spec,
        RegistryEntry,
        upsert_entry,
        has_duplicate_capability,
    )
    from .station_b_generator import (
        station_b_generate,
        StationBError,
        write_plugin_file,
    )
    from .station_c_validator import validate_plugin_module
except ImportError:  # pragma: no cover - direct script/local-folder import
    from production_queue import ProductionQueue, ProductionTask
    from plugin_spec import PluginSpec
    from registry import (
        plugin_path_for_spec,
        RegistryEntry,
        upsert_entry,
        has_duplicate_capability,
    )
    from station_b_generator import (
        station_b_generate,
        StationBError,
        write_plugin_file,
    )
    from station_c_validator import validate_plugin_module

try:
    from settings import SETTINGS
except ImportError:  # pragma: no cover - optional root-level config unavailable
    SETTINGS = None


# ======================================================================
# Configuration
# ======================================================================

@dataclass
class FactoryConfig:
    """
    Global configuration for the Francis Plugin Factory.

    Attributes:
        max_plugins: Stop after successfully producing this many plugins.
        max_retries_per_plugin: How many times to retry a failing task.
        continue_on_failure: If False, a hard failure stops the factory.
        logic_temperature: Temperature for Station B (logic generation).
        model: Model name to use with Ollama for code generation.
    """

    max_plugins: int = 10
    max_retries_per_plugin: int = 4
    continue_on_failure: bool = True

    logic_temperature: float = 0.25
    model: str = "llama3"

    @classmethod
    def from_settings(cls) -> "FactoryConfig":
        if SETTINGS is None:
            return cls()
        f = SETTINGS.factory
        return cls(
            max_plugins=f.max_plugins,
            max_retries_per_plugin=f.max_retries_per_plugin,
            continue_on_failure=f.continue_on_failure,
            logic_temperature=f.logic_temperature,
            model=f.model,
        )


# ======================================================================
# Internal helpers
# ======================================================================

def _load_module_from_path(name: str, path: Path) -> Any:
    """
    Dynamically import a Python module from a given file path.
    """
    spec = importlib.util.spec_from_file_location(name, str(path))
    if spec is None or spec.loader is None:
        raise ImportError(f"Could not create import spec for {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)  # type: ignore[attr-defined]
    return module


def _build_spec_from_task(task: ProductionTask) -> PluginSpec:
    """
    Construct a PluginSpec from a ProductionTask.

    For now this is deterministic (no LLM) to keep the core path robust.
    Later, Station A can be plugged in to generate richer specs.
    """
    # Turn "initial_insight_generator" into "Initial Insight Generator"
    title_parts = task.name.replace("_", " ").replace("-", " ").split()
    title = " ".join(word.capitalize() for word in title_parts) or task.name

    # Use PluginSpec.new to let it handle slug/version normalization
    spec = PluginSpec.new(
        name=title,
        goal=task.goal,
        category=task.category,
        tags=list(task.tags),
    )
    return spec


async def _process_single_task(
    task: ProductionTask,
    config: FactoryConfig,
    *,
    run_id: Optional[str] = None,
) -> bool:
    """
    Execute the full pipeline for a single ProductionTask:

        ProductionTask -> PluginSpec -> Station B (code) ->
        write file -> import module -> Station C (validate) -> registry

    Returns True if the plugin was successfully validated and registered.
    """
    logger = logging.getLogger("francis.factory")
    run_id = run_id or f"factory-{uuid.uuid4().hex[:8]}"

    logger.info("Processing task: name=%s goal=%s", task.name, task.goal)

    # 1) Build spec
    spec = _build_spec_from_task(task)

    # 2) Duplicate detection (hard block)
    if has_duplicate_capability(spec):
        logger.warning(
            "Skipping task '%s': plugin spec appears to duplicate an existing capability (slug=%s).",
            task.name,
            spec.slug,
        )
        return False

    # 3) File path for plugin
    path = plugin_path_for_spec(spec)
    logger.info("Target plugin path: %s", path)

    # 4) Generate full source via Station B
    try:
        source = await station_b_generate(
            spec,
            temperature=config.logic_temperature,
            model=config.model,
        )
    except StationBError as e:
        logger.error("Station B failed for task '%s': %s", task.name, e)
        return False
    except Exception as e:
        logger.exception("Unexpected error in Station B for task '%s': %s", task.name, e)
        return False

    # 5) Write plugin file
    try:
        write_plugin_file(path, source)
    except Exception as e:
        logger.exception("Failed to write plugin file for task '%s': %s", task.name, e)
        return False

    # 6) Import module from fresh file
    try:
        module_name = f"francis_plugin_{spec.slug}"
        module = _load_module_from_path(module_name, path)
    except Exception as e:
        logger.exception("Failed to import generated plugin for task '%s': %s", task.name, e)
        return False

    # 7) Validate via Station C
    try:
        validation_result = await validate_plugin_module(
            module=module,
            spec=spec,
            run_id=run_id,
        )
    except Exception as e:
        logger.exception("Station C validation crashed for task '%s': %s", task.name, e)
        return False

    if not validation_result.ok:
        logger.warning(
            "Validation failed for plugin slug=%s from task='%s'.\nReport:\n%s",
            spec.slug,
            task.name,
            validation_result.error_report,
        )
        return False

    # 8) Registry update
    try:
        entry = RegistryEntry.from_spec(spec, path=path, runtime_hints={"source": "factory"})
        upsert_entry(entry)
        logger.info(
            "Plugin registered successfully: slug=%s name=%s path=%s",
            spec.slug,
            spec.name,
            path,
        )
    except Exception as e:
        logger.exception("Failed to upsert registry entry for slug=%s: %s", spec.slug, e)
        return False

    logger.info("Task '%s' completed successfully.", task.name)
    return True


# ======================================================================
# Factory runner
# ======================================================================

async def run_factory(
    queue: ProductionQueue,
    config: Optional[FactoryConfig] = None,
) -> None:
    """
    Main loop for the Francis Plugin Factory.

    - Consumes tasks from the ProductionQueue.
    - For each task, retries up to max_retries_per_plugin.
    - Stops when:
        * queue is empty, or
        * max_plugins successfully produced, or
        * a critical failure occurs and continue_on_failure is False.
    """
    logger = logging.getLogger("francis.factory")
    if config is None:
        config = FactoryConfig.from_settings()

    produced_count = 0

    logger.info(
        "Factory started: max_plugins=%d, max_retries_per_plugin=%d, continue_on_failure=%s",
        config.max_plugins,
        config.max_retries_per_plugin,
        config.continue_on_failure,
    )

    while not queue.is_empty():
        if produced_count >= config.max_plugins:
            logger.info("Reached max_plugins limit (%d). Stopping factory.", config.max_plugins)
            break

        task = queue.next()
        if task is None:
            break

        logger.info("Starting task '%s' (priority=%d)", task.name, task.priority)

        success = False
        for attempt in range(1, config.max_retries_per_plugin + 1):
            logger.info("Attempt %d/%d for task '%s'", attempt, config.max_retries_per_plugin, task.name)
            try:
                success = await _process_single_task(task, config)
            except Exception as e:
                logger.exception("Unhandled exception while processing task '%s': %s", task.name, e)
                success = False

            if success:
                produced_count += 1
                logger.info(
                    "Task '%s' succeeded on attempt %d. Total produced: %d",
                    task.name,
                    attempt,
                    produced_count,
                )
                break
            else:
                logger.warning(
                    "Task '%s' failed on attempt %d/%d.",
                    task.name,
                    attempt,
                    config.max_retries_per_plugin,
                )

        if not success:
            logger.error(
                "Task '%s' failed after %d attempts.",
                task.name,
                config.max_retries_per_plugin,
            )
            if not config.continue_on_failure:
                logger.error("continue_on_failure is False. Stopping factory.")
                break

    logger.info("Factory loop finished. Total successfully produced plugins: %d", produced_count)
