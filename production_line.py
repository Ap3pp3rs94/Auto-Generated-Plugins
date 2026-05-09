from __future__ import annotations

import asyncio
from typing import Iterable, List, Optional, Tuple

from production_queue import ProductionTask, ProductionQueue
from factory_runner import FactoryConfig, build_single_plugin


async def run_queue(
    cfg: FactoryConfig,
    queue: ProductionQueue,
    *,
    start_plugin_id: int = 1,
) -> None:
    """
    Core production loop for the Francis plugin factory.

    This is a generic version of the factory loop that:
    - Consumes tasks from a ProductionQueue
    - Calls build_single_plugin() for each task
    - Prints a structured report for each plugin
    """

    plugin_id = start_plugin_id

    while not queue.is_empty():
        task = queue.next()
        if task is None:
            break

        print(f"\n[ProductionLine] Starting task: {task.name} (priority={task.priority})")

        ok, report = await build_single_plugin(cfg, task, plugin_id)

        print("=" * 120)
        print(f"TASK RESULT for '{task.name}': {'SUCCESS' if ok else 'FAILURE'}")
        print(report)
        print("=" * 120)

        if not ok and not cfg.continue_on_failure:
            print("[ProductionLine] Halting due to failure and continue_on_failure=False.")
            break

        plugin_id += 1


def build_queue(tasks: Iterable[ProductionTask]) -> ProductionQueue:
    """
    Helper to create a ProductionQueue from an iterable of tasks.
    """
    queue = ProductionQueue()
    for task in tasks:
        queue.add(task)
    return queue


async def run_tasks_async(
    cfg: Optional[FactoryConfig] = None,
    tasks: Optional[Iterable[ProductionTask]] = None,
) -> None:
    """
    Asynchronous entrypoint for running a production line.

    Args:
        cfg: FactoryConfig instance. If None, a default config is created.
        tasks: Iterable of ProductionTask instances. If None, nothing runs.
    """
    if cfg is None:
        cfg = FactoryConfig()

    if not tasks:
        print("[ProductionLine] No tasks supplied; nothing to do.")
        return

    queue = build_queue(tasks)
    await run_queue(cfg, queue)


def run_tasks(
    cfg: Optional[FactoryConfig] = None,
    tasks: Optional[Iterable[ProductionTask]] = None,
) -> None:
    """
    Synchronous wrapper for run_tasks_async(), using asyncio.run().

    This is convenient for:
    - CLI scripts
    - One-off production runs
    - External orchestrators that do not manage their own event loop
    """
    asyncio.run(run_tasks_async(cfg=cfg, tasks=tasks))
