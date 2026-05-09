from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Dict, Optional


# ======================================================================
# Data structures: ProductionTask
# ======================================================================

@dataclass
class ProductionTask:
    """
    A single unit of work for the Francis Plugin Factory.

    Attributes:
        name: Short machine-friendly identifier for the task.
        goal: Description of the capability the plugin must achieve.
        category: One of: data / utility / integration / system_automation.
        tags: Flexible keyword list to help Station A & B guide generation.
        priority: Lower = executed sooner (0 = highest priority).
    """

    name: str
    goal: str
    category: str
    tags: List[str] = field(default_factory=list)
    priority: int = 100


# ======================================================================
# ProductionQueue — priority-driven task dispatcher
# ======================================================================

@dataclass
class ProductionQueue:
    """
    Priority-sorted queue used by the factory orchestrator.

    Behavior:
        - Add tasks via add()
        - Retrieve next task via next()
        - Check if queue is empty via is_empty()

    Lower priority values execute first (0 = highest priority).
    """

    tasks: List[ProductionTask] = field(default_factory=list)

    # ------------------------------------------------------------------
    # Add a new task
    # ------------------------------------------------------------------
    def add(self, task: ProductionTask) -> None:
        """
        Add a ProductionTask to the queue and re-sort by priority.
        Ensures stable ordering in case of equal priorities.
        """
        self.tasks.append(task)
        self.tasks.sort(key=lambda t: t.priority)

    # ------------------------------------------------------------------
    # Pop next task
    # ------------------------------------------------------------------
    def next(self) -> Optional[ProductionTask]:
        """
        Retrieve and remove the next highest-priority task.
        Returns None if queue is empty.
        """
        if not self.tasks:
            return None
        return self.tasks.pop(0)

    # ------------------------------------------------------------------
    # Check if queue is empty
    # ------------------------------------------------------------------
    def is_empty(self) -> bool:
        """Return True when there are no remaining tasks."""
        return len(self.tasks) == 0

    # ------------------------------------------------------------------
    # Helpful for monitoring & UI later
    # ------------------------------------------------------------------
    def __len__(self) -> int:
        """Return the number of tasks remaining in the queue."""
        return len(self.tasks)
