from __future__ import annotations

"""
Francis Plugin Factory Runner (Station Orchestrator)

This module orchestrates the Francis AI capability factory:

- Discovers existing capability modules in the ./plugins directory.
- Uses a deterministic spec builder (spec_builder.build_next_spec)
  to propose a new PluginSpec across multiple domains
  (system_automation, monitoring, security, ecommerce, etc.).
- Calls Station B to generate the capability module source code.
- Writes the module file to disk.
- Runs Station C's validator against the new module.
- Repeats according to RunnerConfig (max_plugins / loop_forever / sleep_seconds).

Enhancements in this version:
- Station B is configured via StationBConfig (model, temperature, tokens, timeout)
  and uses its own retry/timeout-safe wrapper.
- Optional Station E telemetry + learning_manager hooks:
    * factory_run_started / factory_plugin_result / ... events
    * duck-typed learning hooks (no hard dependency)
- Optional Station D integration:
    * repair_plugin(slug, ...) for structural failures
    * evaluate_plugin_candidate(...) hook for quality scoring (if implemented)
- RunnerConfig exposes:
    * LLM parameters (model, temp, tokens, timeout)
    * Evaluation controls (enable, threshold)
- Supports category rotation to prevent same-category saturation.
- Aware of custom soft-focus prompt (custom_prompt.txt) and logs when it is active.
- Passes a simple memory_context of existing plugins into Station B to help
  reduce duplicate capabilities.
- Contains a non-fatal hook for a cleanup daemon (cleanup_daemon.run_cleanup_cycle).
"""

import argparse
import asyncio
import atexit
import copy
import hashlib
import importlib.util
import inspect
import json
import logging
import os
import random
import subprocess
import sys
import time
from dataclasses import dataclass, asdict, field
from pathlib import Path
from typing import Any, Dict, Optional, Sequence, Set, Tuple

try:
    from .plugin_spec import PluginSpec
    from .station_c_validator import validate_plugin_module
except ImportError:  # pragma: no cover - direct local execution
    from plugin_spec import PluginSpec
    from station_c_validator import validate_plugin_module
try:
    from factory.spec_builder import (
        AI_CAPABILITY_ROADMAP,
        build_next_spec,
        legacy_continuous_expansion_slug,
        numbered_capability_slug,
    )
except (ImportError, ModuleNotFoundError):  # pragma: no cover - standalone sidecar checkout
    from spec_builder import (
        AI_CAPABILITY_ROADMAP,
        build_next_spec,
        legacy_continuous_expansion_slug,
        numbered_capability_slug,
    )

try:
    from factory.profiles import (
        build_profile_source as _build_profile_source,
        registered_profile_id as _registered_profile_id,
    )
except (ImportError, ModuleNotFoundError):  # pragma: no cover - standalone sidecar checkout
    try:
        from profiles import (  # type: ignore
            build_profile_source as _build_profile_source,
            registered_profile_id as _registered_profile_id,
        )
    except (ImportError, ModuleNotFoundError):  # pragma: no cover
        _build_profile_source = None  # type: ignore[assignment]
        _registered_profile_id = None  # type: ignore[assignment]

try:
    from factory.factory_os.capability_spec import CapabilitySpec, LogicProfile, SemanticContract, SemanticProbe
    from factory.factory_os.capability_specs import get_capability_spec as _get_capability_spec
    from factory.factory_os.logic_profiles import (
        get_logic_profile as _get_logic_profile,
        normalize_logic_profile_id as _normalize_logic_profile_id,
    )
    from factory.factory_os.promotion_gate import evaluate_for_promotion as _evaluate_for_promotion
    from factory.factory_os.semantic_contracts import get_semantic_contract as _get_semantic_contract
    from factory.factory_os.semantic_validator import run_semantic_contract_async as _run_semantic_contract_async
    from factory.factory_os.a_plus_certification import (
        A_PLUS_MIN_SCORE,
        certify_plugin_callable as _certify_a_plus_plugin,
        summarize_a_plus_result as _summarize_a_plus_result,
    )
except (ImportError, ModuleNotFoundError):  # pragma: no cover - standalone sidecar checkout
    try:
        from factory_os.capability_spec import CapabilitySpec, LogicProfile, SemanticContract, SemanticProbe  # type: ignore
        from factory_os.capability_specs import get_capability_spec as _get_capability_spec  # type: ignore
        from factory_os.logic_profiles import (  # type: ignore
            get_logic_profile as _get_logic_profile,
            normalize_logic_profile_id as _normalize_logic_profile_id,
        )
        from factory_os.promotion_gate import evaluate_for_promotion as _evaluate_for_promotion  # type: ignore
        from factory_os.semantic_contracts import get_semantic_contract as _get_semantic_contract  # type: ignore
        from factory_os.semantic_validator import run_semantic_contract_async as _run_semantic_contract_async  # type: ignore
        from factory_os.draft_plugin_repair_surgeon import repair_plugin_file as _repair_draft_plugin_file  # type: ignore
        from factory_os.a_plus_certification import (  # type: ignore
            A_PLUS_MIN_SCORE,
            certify_plugin_callable as _certify_a_plus_plugin,
            summarize_a_plus_result as _summarize_a_plus_result,
        )
    except (ImportError, ModuleNotFoundError):  # pragma: no cover
        _get_capability_spec = None  # type: ignore[assignment]
        _get_logic_profile = None  # type: ignore[assignment]
        _normalize_logic_profile_id = None  # type: ignore[assignment]
        _evaluate_for_promotion = None  # type: ignore[assignment]
        _get_semantic_contract = None  # type: ignore[assignment]
        _run_semantic_contract_async = None  # type: ignore[assignment]
        _repair_draft_plugin_file = None  # type: ignore[assignment]
        _certify_a_plus_plugin = None  # type: ignore[assignment]
        _summarize_a_plus_result = None  # type: ignore[assignment]
        A_PLUS_MIN_SCORE = 0.98  # type: ignore[assignment]
        CapabilitySpec = None  # type: ignore[assignment]
        LogicProfile = None  # type: ignore[assignment]
        SemanticContract = None  # type: ignore[assignment]
        SemanticProbe = None  # type: ignore[assignment]
else:
    try:
        from factory.factory_os.draft_plugin_repair_surgeon import repair_plugin_file as _repair_draft_plugin_file
    except (ImportError, ModuleNotFoundError):  # pragma: no cover
        _repair_draft_plugin_file = None  # type: ignore[assignment]

try:
    from plugin_template import render_plugin_source as _render_plugin_source
except (ImportError, ModuleNotFoundError):  # pragma: no cover
    try:
        from factory.plugin_template import render_plugin_source as _render_plugin_source  # type: ignore
    except (ImportError, ModuleNotFoundError):  # pragma: no cover
        _render_plugin_source = None  # type: ignore[assignment]

try:
    from station_b import generate_plugin_source, StationBConfig
except (ImportError, ModuleNotFoundError):  # pragma: no cover - standalone sidecar checkout
    from station_b_generator import station_b_generate

    @dataclass
    class StationBConfig:  # type: ignore[no-redef]
        model: str = "llama3.1:8b"
        temperature: float = 0.25
        max_tokens: int = 4096
        context_length: int = 8192
        timeout_seconds: int = 900
        max_retries: int = 1
        retry_backoff_seconds: float = 0.0

    @dataclass
    class _FallbackStationBResult:
        source: str
        raw_llm_output: str = ""
        logic_profile_id: str = "standalone_station_b_generator"
        logic_blueprint: Dict[str, Any] = field(default_factory=dict)

    async def generate_plugin_source(  # type: ignore[no-redef]
        spec: PluginSpec,
        *,
        capability_type: Optional[str] = None,
        intended_domain: Optional[str] = None,
        extra_instructions: Optional[str] = None,
        memory_context: Optional[str] = None,
        mode: str = "generate",
        existing_source_excerpt: Optional[str] = None,
        config: Optional[StationBConfig] = None,
    ) -> _FallbackStationBResult:
        """
        Minimal local fallback when the full Francis Station B runtime is absent.

        Production Francis runs should use the richer parent `station_b.py`.
        This fallback keeps the sidecar repo runnable enough for development,
        config checks, and emergency local generation.
        """
        cfg = config or StationBConfig()
        source = await asyncio.wait_for(
            station_b_generate(
                spec,
                temperature=cfg.temperature,
                model=cfg.model,
            ),
            timeout=cfg.timeout_seconds,
        )
        return _FallbackStationBResult(
            source=source,
            raw_llm_output="",
            logic_blueprint={
                "capability_type": capability_type,
                "intended_domain": intended_domain,
                "extra_instructions": extra_instructions,
                "memory_context": memory_context,
                "mode": mode,
                "existing_source_excerpt": bool(existing_source_excerpt),
            },
        )

try:
    from station_b import (  # type: ignore
        _build_deterministic_ai_logic_body as _station_b_deterministic_ai_body,
        _update_logic_region as _station_b_update_logic_region,
        _wrap_logic_body as _station_b_wrap_logic_body,
    )
except Exception:  # pragma: no cover - optional parent Station B internals
    _station_b_deterministic_ai_body = None  # type: ignore[assignment]
    _station_b_update_logic_region = None  # type: ignore[assignment]
    _station_b_wrap_logic_body = None  # type: ignore[assignment]

LOG = logging.getLogger(__name__)

# ---------------------------------------------------------------------
# Optional soft-focus integration (user-provided custom_prompt.txt)
# ---------------------------------------------------------------------
try:
    from custom_focus import get_custom_focus_instructions  # type: ignore
except (ImportError, ModuleNotFoundError):  # pragma: no cover
    def get_custom_focus_instructions() -> str:
        """Fallback if custom_focus is unavailable; preserves pre-focus behavior."""
        return ""


# ---------------------------------------------------------------------
# Optional cleanup daemon (best-effort, non-fatal if missing)
# ---------------------------------------------------------------------
try:
    from cleanup_daemon import run_cleanup_cycle  # type: ignore
except (ImportError, ModuleNotFoundError):  # pragma: no cover
    async def run_cleanup_cycle(*args: Any, **kwargs: Any) -> None:
        """No-op fallback when cleanup_daemon is not present."""
        return None


# ---------------------------------------------------------------------
# Optional learning manager / Station E telemetry
# ---------------------------------------------------------------------
try:
    from learning_manager import get_learning_manager  # type: ignore
except (ImportError, ModuleNotFoundError):  # pragma: no cover
    def get_learning_manager() -> Any:
        return None


try:
    from station_e_memory import record_event as _se_record_base  # type: ignore
except (ImportError, ModuleNotFoundError):  # pragma: no cover
    try:
        # Older versions may only expose record_error
        from station_e_memory import record_error as _se_record_base  # type: ignore
    except (ImportError, ModuleNotFoundError):  # pragma: no cover
        def _se_record_base(event_type: str, **meta: Any) -> None:
            # Last-resort stub: keep visible but non-fatal.
            LOG.info("Station E telemetry stub: %s | %s", event_type, meta)


_LEARNING = get_learning_manager()


def _se_record(event_type: str, **meta: Any) -> None:
    """
    Best-effort Station E telemetry wrapper.

    - Never raises.
    - Logs failures at DEBUG so they are visible during development.
    """
    try:
        _se_record_base(event_type, **meta)
    except Exception:
        LOG.debug("Failed to record telemetry event %s | %r", event_type, meta, exc_info=True)


# ---------------------------------------------------------------------
# Optional Station D integration (repair + evaluation hooks)
# ---------------------------------------------------------------------
try:
    from station_d import repair_plugin  # type: ignore
except (ImportError, ModuleNotFoundError):  # pragma: no cover
    async def repair_plugin(*args: Any, **kwargs: Any) -> Dict[str, Any]:
        """
        Fallback repair_plugin for when Station D is unavailable.

        Returns a consistent shape but indicates no repair was done.
        """
        slug: str = kwargs.get("slug") if "slug" in kwargs else (args[0] if args else "<unknown>")
        return {
            "slug": slug,
            "repaired": False,
            "attempts": 0,
            "backup_path": None,
            "final_path": None,
            "error": "station_d_unavailable",
        }


try:
    from station_d import evaluate_plugin_candidate  # type: ignore
except (ImportError, ModuleNotFoundError):  # pragma: no cover
    async def evaluate_plugin_candidate(
        *args: Any,
        **kwargs: Any,
    ) -> Optional[Dict[str, Any]]:
        """
        Fallback evaluator when Station D's evaluation/critic is not available.

        Returns None to indicate "no evaluation performed".
        """
        return None


try:
    from plugin_registry import list_plugins as _list_registered_plugins  # type: ignore
except Exception:  # pragma: no cover
    def _list_registered_plugins(*args: Any, **kwargs: Any) -> list[Any]:
        return []


# =====================================================================
# Paths / event constants
# =====================================================================

FACTORY_DIR = Path(__file__).resolve().parent
ROOT_DIR = FACTORY_DIR.parent
PLUGINS_DIR = FACTORY_DIR / "plugins"
CANDIDATE_PLUGINS_DIR = FACTORY_DIR / ".candidate_plugins"
RUN_LOCK_PATH = FACTORY_DIR / ".factory_runner.lock"
AI_ROADMAP_STATE_PATH = FACTORY_DIR / "registry" / "ai_roadmap_state.json"

EVENT_FACTORY_RUN_STARTED = "factory_run_started"
EVENT_FACTORY_RUN_COMPLETED = "factory_run_completed"
EVENT_FACTORY_STATION_B_GENERATED = "factory_station_b_generated"
EVENT_FACTORY_STATION_B_ERROR = "factory_station_b_error"
EVENT_FACTORY_PLUGIN_STRUCTURAL_FAILED = "factory_plugin_structural_failed"
EVENT_FACTORY_STATION_D_REPAIR_ATTEMPT = "factory_station_d_repair_attempt"
EVENT_FACTORY_STATION_D_REPAIR_ERROR = "factory_station_d_repair_error"
EVENT_FACTORY_PLUGIN_EVALUATED = "factory_plugin_evaluated"
EVENT_FACTORY_PLUGIN_LOW_SCORE = "factory_plugin_low_score"
EVENT_FACTORY_PLUGIN_PASSING_SCORE = "factory_plugin_passing_score"
EVENT_FACTORY_PLUGIN_EVAL_ERROR = "factory_plugin_evaluation_error"
EVENT_FACTORY_PLUGIN_RESULT = "factory_plugin_result"

# Production quality theology:
# A generated capability must be useful enough to score at least this high
# before it is allowed to leave .candidate_plugins/ and become a live plugin.
PRODUCTION_QUALITY_THRESHOLD = 0.95

PRODUCTION_QUALITY_PROBE_PAYLOAD: Dict[str, Any] = {
    "task": "Validate a generated AI capability before publishing it.",
    "objective": "Reject shallow or duplicate output and keep only capability-specific work.",
    "prompt": "Make this production worthy without relabeling generic advice.",
    "constraints": [
        "must produce capability-specific details",
        "must expose concrete next actions",
        "must be useful to an autonomous AI workflow",
        "do not invent facts",
    ],
    "current_plan": ["generate candidate", "validate plugin", "semantic depth check", "commit and push"],
    "completed_steps": ["candidate module generated"],
    "blocked_steps": ["need proof the capability does what it says"],
    "agents": ["builder", "reviewer", "publisher"],
    "workstreams": ["implementation", "semantic validation", "github publishing"],
    "ownership_scopes": ["code changes", "quality gates", "release evidence"],
    "candidate_outputs": [
        {"summary": "Generic capability output with stock advice."},
        {"summary": "Specific capability output with measurable validation evidence."},
    ],
    "source_notes": [
        "Production standard is 0.95 or better.",
        "Sub-threshold capabilities must be discarded instead of published.",
    ],
    "quality_failures": ["duplicate capability", "shallow recommendation", "missing capability-specific outputs"],
}


class FactoryAlreadyRunningError(RuntimeError):
    """Raised when another factory runner process appears to be active."""


def _pid_is_running(pid: int) -> bool:
    if pid <= 0:
        return False
    try:
        os.kill(pid, 0)
    except ProcessLookupError:
        return False
    except PermissionError:
        return True
    return True


def _read_lock_pid() -> Optional[int]:
    try:
        text = RUN_LOCK_PATH.read_text(encoding="utf-8").strip()
    except FileNotFoundError:
        return None
    except Exception:
        return None
    try:
        return int(text)
    except ValueError:
        return None


def _acquire_runner_lock() -> bool:
    """
    Best-effort process lock to prevent duplicate autonomous factories.

    The lock is PID-based so a stale lock from a dead process can be replaced.
    """
    existing_pid = _read_lock_pid()
    current_pid = os.getpid()
    if existing_pid and existing_pid != current_pid and _pid_is_running(existing_pid):
        raise FactoryAlreadyRunningError(
            f"Factory runner already appears to be running as PID {existing_pid}."
        )

    RUN_LOCK_PATH.write_text(str(current_pid), encoding="utf-8")
    atexit.register(_release_runner_lock)
    return True


def _release_runner_lock() -> None:
    try:
        locked_pid = _read_lock_pid()
        if locked_pid == os.getpid():
            RUN_LOCK_PATH.unlink(missing_ok=True)
    except Exception:
        LOG.debug("Unable to release factory runner lock", exc_info=True)


# =====================================================================
# Runner configuration
# =====================================================================

@dataclass
class RunnerConfig:
    """
    Configuration for the Francis AI capability factory runner.

    The runner can either:
    - build a finite number of capability modules (max_plugins), or
    - run indefinitely (loop_forever=True) with periodic sleeps.

    It also controls:
    - which capability_type / domain to bias towards
    - which LLM/model Station B uses
    - optional evaluation via Station D (score-only by default)
    """
    # Core factory behavior
    max_plugins: Optional[int] = None
    sleep_seconds: float = 15.0
    loop_forever: bool = False
    user_id: str = "francis-factory"

    capability_type: str = "data_insight"
    intended_domain: Optional[str] = None

    # LLM CONFIG (Station B)
    llm_model: str = "llama3.1:8b"      # Recommended local model
    llm_temperature: float = 0.25
    llm_max_tokens: int = 4096
    llm_context_length: int = 8192
    llm_timeout_seconds: int = 900

    # Category rotation (to avoid oversaturating a single category)
    rotate_categories: bool = True
    max_per_category: Optional[int] = None

    # Evaluation / critic integration (Station D evaluator)
    evaluation_enabled: bool = False
    evaluation_threshold: float = 0.60   # Score below this is considered "low quality"
    evaluation_profile: Optional[str] = None  # e.g. "research", "default"
    evaluation_log_only: bool = True     # If False, you could later add auto-reject logic.

    # Publishing
    github_publish_enabled: bool = True
    github_remote: str = "origin"
    github_branch: str = "main"
    allow_upgrade_expansion: bool = False
    randomized_expansion: bool = True

    def validate(self) -> None:
        """Fail fast on unsafe or nonsensical production configuration."""
        if self.max_plugins is not None and self.max_plugins <= 0:
            raise ValueError("max_plugins must be positive when provided.")
        if self.sleep_seconds < 0:
            raise ValueError("sleep_seconds must be >= 0.")
        if not self.user_id.strip():
            raise ValueError("user_id must be non-empty.")
        if not self.llm_model.strip():
            raise ValueError("llm_model must be non-empty.")
        if not 0.0 <= self.llm_temperature <= 2.0:
            raise ValueError("llm_temperature must be between 0.0 and 2.0.")
        if self.llm_max_tokens <= 0:
            raise ValueError("llm_max_tokens must be positive.")
        if self.llm_context_length <= 0:
            raise ValueError("llm_context_length must be positive.")
        if self.llm_context_length <= self.llm_max_tokens:
            raise ValueError("llm_context_length must be greater than llm_max_tokens.")
        if self.llm_timeout_seconds <= 0:
            raise ValueError("llm_timeout_seconds must be positive.")
        if self.max_per_category is not None and self.max_per_category <= 0:
            raise ValueError("max_per_category must be positive when provided.")
        if not 0.0 <= self.evaluation_threshold <= 1.0:
            raise ValueError("evaluation_threshold must be between 0.0 and 1.0.")
        if self.github_publish_enabled:
            if not self.github_remote.strip():
                raise ValueError("github_remote must be non-empty when publishing is enabled.")
            if not self.github_branch.strip():
                raise ValueError("github_branch must be non-empty when publishing is enabled.")

    def station_b_config(self) -> StationBConfig:
        """Helper to build a StationBConfig from this RunnerConfig."""
        self.validate()
        return StationBConfig(
            model=self.llm_model,
            temperature=self.llm_temperature,
            max_tokens=self.llm_max_tokens,
            context_length=self.llm_context_length,
            timeout_seconds=self.llm_timeout_seconds,
            max_retries=1,
            retry_backoff_seconds=0.0,
        )


# =====================================================================
# Helpers
# =====================================================================

def _ensure_plugins_dir() -> None:
    PLUGINS_DIR.mkdir(parents=True, exist_ok=True)


def _load_existing_plugin_slugs() -> Set[str]:
    _ensure_plugins_dir()
    slugs: Set[str] = set()
    for path in PLUGINS_DIR.glob("*.py"):
        if path.name == "__init__.py":
            continue
        slugs.add(path.stem)
    return slugs


def _normalize_signature(*, name: str, goal: str, category: str, tags: Any) -> str:
    clean_tags = []
    if isinstance(tags, (list, tuple, set)):
        clean_tags = [str(t).strip().lower() for t in tags if str(t).strip()]
    return "|".join(
        [
            "name=" + " ".join(str(name or "").lower().split()),
            "goal=" + " ".join(str(goal or "").lower().split()),
            "category=" + " ".join(str(category or "").lower().split()),
            "tags=" + ",".join(sorted(clean_tags)),
        ]
    )


def _spec_signature(spec: PluginSpec) -> str:
    return _normalize_signature(
        name=getattr(spec, "name", ""),
        goal=getattr(spec, "goal", ""),
        category=getattr(spec, "category", ""),
        tags=getattr(spec, "tags", []),
    )


def _load_existing_capability_signatures() -> Set[str]:
    """
    Load known capability signatures from the root registry.

    This is a pre-generation guard so the runner does not waste model calls on
    exact duplicate specs. Slug checks still protect plugins that are present on
    disk but missing from the registry.
    """
    signatures: Set[str] = set()
    try:
        for rec in _list_registered_plugins():
            signatures.add(
                _normalize_signature(
                    name=getattr(rec, "name", ""),
                    goal=((getattr(rec, "meta", {}) or {}).get("goal") if isinstance(getattr(rec, "meta", {}), dict) else "")
                    or getattr(rec, "name", ""),
                    category=getattr(rec, "category", ""),
                    tags=getattr(rec, "tags", []),
                )
            )
    except Exception:
        LOG.debug("Unable to load root registry signatures for duplicate screening", exc_info=True)
    return signatures


def _roadmap_slug_index(slug: str) -> Optional[int]:
    """
    Convert an existing AI roadmap slug into its deterministic global index.
    """
    # Legacy numbered batches are intentionally not part of the forward cursor.
    # New expansion uses descriptive dimensions instead of `_set_N` clones.
    if "_set_" in str(slug or ""):
        return None

    roadmap_size = len(AI_CAPABILITY_ROADMAP)
    for position, blueprint in enumerate(AI_CAPABILITY_ROADMAP, start=1):
        numbered_slug = numbered_capability_slug(blueprint.slug, position)
        if slug == blueprint.slug or slug == numbered_slug:
            return position

    # Short slugs end with their deterministic global index, e.g.
    # ai_verification_checklist_builder_000734. Resolve those directly so
    # library-wide audits and sibling checks do not walk thousands of legacy
    # candidates for every plugin.
    try:
        suffix = str(slug or "").rsplit("_", 1)[-1]
        if len(suffix) == 6 and suffix.isdigit():
            idx = int(suffix)
            if idx >= 1:
                spec, _capability_type, _intended_domain = build_next_spec(idx)
                if getattr(spec, "slug", None) == slug:
                    return idx
    except Exception:
        pass

    # Continuous expansion specs are generated deterministically after the
    # curated roadmap. During the transition to shorter numbered slugs, keep
    # recognizing already-published legacy descriptive slugs so the forward
    # cursor does not loop back and regenerate old use cases.
    for idx in range(roadmap_size + 1, roadmap_size + 10000):
        try:
            spec, _, _ = build_next_spec(idx)
        except Exception:
            return None
        if getattr(spec, "slug", None) == slug:
            return idx
        try:
            if legacy_continuous_expansion_slug(idx) == slug:
                return idx
        except Exception:
            continue
    return None


def _spec_generation_round(spec: PluginSpec) -> int:
    extra = getattr(spec, "extra", {}) or {}
    try:
        return max(1, int(extra.get("generation_round", 1)))
    except Exception:
        return 1


def _is_upgrade_attempt_spec(spec: PluginSpec) -> bool:
    return _spec_generation_round(spec) > 1


def _canonical_retention_spec(spec: PluginSpec) -> PluginSpec:
    """
    Convert an internal upgrade spec into a canonical base capability spec.

    Upgrade expansion is an internal improvement attempt. It must never create a
    second installable module whose only distinction is metadata.
    """
    generation_round = _spec_generation_round(spec)
    if generation_round <= 1:
        return spec

    extra = getattr(spec, "extra", {}) or {}
    roadmap_number = extra.get("roadmap_number")
    if not isinstance(roadmap_number, int) or roadmap_number < 1:
        return spec

    base_spec, _, _ = build_next_spec(roadmap_number)
    base_spec.goal = (
        f"Improve {base_spec.name}: preserve the original capability, add stronger "
        "edge-case handling, expose clearer user-facing progress signals, and "
        "produce more actionable next steps."
    )
    base_spec.use_cases = list(getattr(spec, "use_cases", []) or base_spec.use_cases)
    base_spec.example_payload = getattr(spec, "example_payload", None)
    base_spec.problem_statement = getattr(spec, "problem_statement", None)
    base_spec.primary_inputs = getattr(spec, "primary_inputs", None)
    base_spec.primary_outputs = getattr(spec, "primary_outputs", None)
    base_spec.constraints = getattr(spec, "constraints", None)
    base_spec.example_use_cases = list(getattr(spec, "example_use_cases", []) or [])
    base_spec.io_contract = getattr(spec, "io_contract", None)
    base_spec.capability_type = getattr(spec, "capability_type", None)
    base_spec.intended_domain = getattr(spec, "intended_domain", None)
    base_spec.owner_id = getattr(spec, "owner_id", None)
    base_spec.tags = [
        tag for tag in list(getattr(spec, "tags", []) or [])
        if str(tag).strip()
    ]
    if "capability_upgrade" not in base_spec.tags:
        base_spec.tags.append("capability_upgrade")
    base_spec.extra = dict(extra)
    base_spec.extra["upgrade_attempt_round"] = generation_round
    base_spec.extra["generation_round"] = 1
    base_spec.extra["retention_policy"] = "upgrade candidates overwrite the base capability only when they improve it"
    base_spec.extra["discard_if_not_better"] = True
    return base_spec


def _next_ai_roadmap_index(
    existing_slugs: Set[str],
    unavailable_slugs: Optional[Set[str]] = None,
) -> int:
    """
    Return the first missing curated capability before expanding forward.

    A later generated capability must not hide an earlier curated gap. Deleted
    plugins are backfilled unless the slug is explicitly unavailable because it
    was rejected under the current factory knowledge.
    """
    known_slugs = set(existing_slugs) | set(unavailable_slugs or set())
    for position, blueprint in enumerate(AI_CAPABILITY_ROADMAP, start=1):
        spec, _, _ = build_next_spec(position)
        slug = str(getattr(spec, "slug", "") or "")
        legacy_slug = str(getattr(blueprint, "slug", "") or "")
        has_current = bool(slug) and (
            slug in known_slugs or (PLUGINS_DIR / f"{slug}.py").exists()
        )
        has_legacy = bool(legacy_slug) and (
            legacy_slug in known_slugs or (PLUGINS_DIR / f"{legacy_slug}.py").exists()
        )
        if slug and not has_current and not has_legacy:
            return position

    existing_indexes = [
        idx for slug in known_slugs
        for idx in [_roadmap_slug_index(slug)]
        if idx is not None
    ]
    if not existing_indexes:
        return 1
    return max(existing_indexes) + 1


def _randomized_ai_expansion_indexes(
    existing_slugs: Set[str],
    unavailable_slugs: Optional[Set[str]] = None,
) -> list[int]:
    """
    Return a bounded shuffled list of internal upgrade-attempt indexes.

    This keeps autonomous mode varied after the curated roadmap is complete,
    while still anchoring every candidate to an approved capability family and
    registered profile. A retained artifact must overwrite the canonical base
    module or be discarded.
    """
    roadmap_size = len(AI_CAPABILITY_ROADMAP)
    known_slugs = set(existing_slugs) | set(unavailable_slugs or set())
    existing_indexes = [
        idx for slug in known_slugs
        for idx in [_roadmap_slug_index(slug)]
        if idx is not None
    ]
    highest_round = max(((idx - 1) // roadmap_size) + 1 for idx in existing_indexes) if existing_indexes else 1
    max_candidate_round = max(2, highest_round + 2)
    candidates: list[int] = []
    for generation_round in range(2, max_candidate_round + 1):
        for position in range(1, roadmap_size + 1):
            idx = (generation_round - 1) * roadmap_size + position
            spec, _, _ = build_next_spec(idx)
            if spec.slug not in known_slugs and not (PLUGINS_DIR / f"{spec.slug}.py").exists():
                candidates.append(idx)
    random.SystemRandom().shuffle(candidates)
    return candidates


def _is_duplicate_spec(
    spec: PluginSpec,
    *,
    existing_slugs: Set[str],
    existing_signatures: Set[str],
) -> bool:
    plugin_path = PLUGINS_DIR / f"{spec.slug}.py"
    return (
        spec.slug in existing_slugs
        or plugin_path.exists()
        or _spec_signature(spec) in existing_signatures
    )


def _is_ai_roadmap_spec(spec: PluginSpec) -> bool:
    extra = getattr(spec, "extra", None)
    return isinstance(extra, dict) and extra.get("factory_focus") == "ai_functionality_and_progress"


def _station_b_result_is_fallback(result: Any) -> bool:
    raw = str(getattr(result, "raw_llm_output", "") or "")
    return raw.startswith(("TIMEOUT:", "ERROR:", "EMPTY_RESPONSE"))


def _load_ai_roadmap_state() -> Dict[str, Any]:
    try:
        data = json.loads(AI_ROADMAP_STATE_PATH.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return {"completed": [], "next_directive": ""}
    except Exception:
        LOG.warning("AI roadmap state file is unreadable; starting with empty state.")
        return {"completed": [], "next_directive": ""}
    if not isinstance(data, dict):
        return {"completed": [], "next_directive": ""}
    data.setdefault("completed", [])
    data.setdefault("next_directive", "")
    data.setdefault("upgrade_attempts", {})
    data.setdefault("upgrade_attempt_order", [])
    data.setdefault("rejected_capabilities", {})
    data.setdefault("rejected_capability_order", [])
    _normalize_ai_roadmap_state(data)
    return data


def _save_ai_roadmap_state(state: Dict[str, Any]) -> None:
    AI_ROADMAP_STATE_PATH.parent.mkdir(parents=True, exist_ok=True)
    tmp = AI_ROADMAP_STATE_PATH.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(state, indent=2, sort_keys=True), encoding="utf-8")
    tmp.replace(AI_ROADMAP_STATE_PATH)


def _normalize_ai_roadmap_state(state: Dict[str, Any]) -> None:
    completed = state.get("completed")
    if not isinstance(completed, list):
        state["completed"] = []
        completed = state["completed"]

    by_slug: Dict[str, Dict[str, Any]] = {}
    for item in completed:
        if not isinstance(item, dict):
            continue
        slug = str(item.get("slug") or "")
        if not slug:
            continue
        by_slug[slug] = item
    state["completed"] = list(by_slug.values())[-100:]

    attempts = state.get("upgrade_attempts")
    if not isinstance(attempts, dict):
        attempts = {}
    normalized_attempts: Dict[str, Dict[str, Any]] = {}
    for key, item in attempts.items():
        if isinstance(item, dict) and key:
            canonical = str(item.get("canonical_slug") or key)
            if canonical:
                normalized_attempts[canonical] = item
    state["upgrade_attempts"] = normalized_attempts

    order = state.get("upgrade_attempt_order")
    if not isinstance(order, list):
        order = []
    state["upgrade_attempt_order"] = [str(item) for item in order if str(item) in normalized_attempts][-500:]

    rejected = state.get("rejected_capabilities")
    if not isinstance(rejected, dict):
        rejected = {}
    normalized_rejected: Dict[str, Dict[str, Any]] = {}
    for key, item in rejected.items():
        if isinstance(item, dict) and key:
            slug = str(item.get("slug") or key)
            if slug:
                normalized_rejected[slug] = item
    state["rejected_capabilities"] = normalized_rejected

    rejected_order = state.get("rejected_capability_order")
    if not isinstance(rejected_order, list):
        rejected_order = []
    state["rejected_capability_order"] = [
        str(item) for item in rejected_order if str(item) in normalized_rejected
    ][-2000:]


def _prune_ai_roadmap_state_to_existing_plugins(
    state: Dict[str, Any],
    existing_slugs: Set[str],
) -> Dict[str, Any]:
    """
    Keep roadmap memory aligned with the actual plugin directory.

    If generated artifacts are purged, completion/upgrade memory must not make
    the factory believe the capability is still present. Rejection memory is
    different: an A+ purge means the artifact was intentionally retired under
    the current factory knowledge. Keep those records so the runner does not
    immediately regenerate the same known-bad slot; the knowledge fingerprint
    still reopens it after factory/profile logic changes.
    """
    _normalize_ai_roadmap_state(state)

    completed = state.get("completed") if isinstance(state.get("completed"), list) else []
    kept_completed = [
        item for item in completed
        if isinstance(item, dict) and str(item.get("slug") or "") in existing_slugs
    ]
    if len(kept_completed) != len(completed):
        LOG.info(
            "Pruned %d stale AI roadmap completion record(s) for deleted plugin artifact(s).",
            len(completed) - len(kept_completed),
        )
    state["completed"] = kept_completed
    state["last_completed"] = kept_completed[-1] if kept_completed else None

    attempts = state.get("upgrade_attempts") if isinstance(state.get("upgrade_attempts"), dict) else {}
    kept_attempts = {
        key: value for key, value in attempts.items()
        if str(key) in existing_slugs
    }
    if len(kept_attempts) != len(attempts):
        LOG.info(
            "Pruned %d stale upgrade attempt record(s) for deleted canonical plugin artifact(s).",
            len(attempts) - len(kept_attempts),
        )
    state["upgrade_attempts"] = kept_attempts
    state["upgrade_attempt_order"] = [
        str(item) for item in state.get("upgrade_attempt_order", [])
        if str(item) in kept_attempts
    ]

    rejected = state.get("rejected_capabilities") if isinstance(state.get("rejected_capabilities"), dict) else {}
    current_fp = _upgrade_knowledge_fingerprint()
    kept_rejected = {
        key: value for key, value in rejected.items()
        if isinstance(value, dict) and value.get("knowledge_fingerprint") == current_fp
    }
    if len(kept_rejected) != len(rejected):
        LOG.info(
            "Pruned %d stale rejection record(s) from older factory knowledge.",
            len(rejected) - len(kept_rejected),
        )
    state["rejected_capabilities"] = kept_rejected
    state["rejected_capability_order"] = [
        str(item) for item in state.get("rejected_capability_order", [])
        if str(item) in kept_rejected
    ]
    return state


def _remembered_rejected_capability_slugs(state: Dict[str, Any]) -> Set[str]:
    rejected = state.get("rejected_capabilities")
    if not isinstance(rejected, dict):
        return set()
    current_fp = _upgrade_knowledge_fingerprint()
    return {
        str(slug)
        for slug, record in rejected.items()
        if str(slug)
        and isinstance(record, dict)
        and record.get("knowledge_fingerprint") == current_fp
    }


def _upgrade_knowledge_fingerprint() -> str:
    """
    Fingerprint the knowledge that determines generated capability behavior.

    Runner bookkeeping changes should not cause rejected upgrades to replay. A
    retry is only justified when the capability specs, deterministic profiles,
    prompt/template layer, or Station B generation rules change enough to produce
    different candidate behavior.
    """
    digest = hashlib.sha256()
    for rel in [
        "spec_builder.py",
        "profiles/registry.py",
        "profiles/dispatcher.py",
        "plugin_template.py",
        "station_b_generator.py",
    ]:
        path = FACTORY_DIR / rel
        digest.update(rel.encode("utf-8"))
        try:
            digest.update(path.read_bytes())
        except FileNotFoundError:
            digest.update(b"<missing>")
    profiles_dir = FACTORY_DIR / "profiles"
    try:
        profile_paths = sorted(
            path
            for path in profiles_dir.glob("*.py")
            if path.name not in {"__init__.py", "registry.py", "dispatcher.py"}
        )
    except OSError:
        profile_paths = []
    for path in profile_paths:
        rel = path.relative_to(FACTORY_DIR).as_posix()
        digest.update(rel.encode("utf-8"))
        try:
            digest.update(path.read_bytes())
        except OSError:
            digest.update(b"<unreadable>")
    return digest.hexdigest()[:16]


def _upgrade_attempt_key(source_spec: PluginSpec) -> str:
    canonical = _canonical_retention_spec(source_spec)
    return str(getattr(canonical, "slug", "") or getattr(source_spec, "slug", "") or "")


def _upgrade_attempt_record(
    *,
    state: Dict[str, Any],
    source_spec: PluginSpec,
    canonical_spec: PluginSpec,
    status: str,
    reason: str,
    persist: bool = True,
) -> Dict[str, Any]:
    attempts = state.setdefault("upgrade_attempts", {})
    if not isinstance(attempts, dict):
        attempts = {}
        state["upgrade_attempts"] = attempts
    order = state.setdefault("upgrade_attempt_order", [])
    if not isinstance(order, list):
        order = []
        state["upgrade_attempt_order"] = order

    key = _upgrade_attempt_key(source_spec)
    record = {
        "source_slug": key,
        "canonical_slug": canonical_spec.slug,
        "source_name": source_spec.name,
        "canonical_name": canonical_spec.name,
        "generation_round": _spec_generation_round(source_spec),
        "status": status,
        "reason": reason[:1000],
        "knowledge_fingerprint": _upgrade_knowledge_fingerprint(),
        "attempted_at_unix": int(time.time()),
    }
    attempts[key] = record
    if key in order:
        order.remove(key)
    order.append(key)
    for stale_key in order[:-500]:
        attempts.pop(stale_key, None)
    state["upgrade_attempt_order"] = order[-500:]
    if persist:
        _save_ai_roadmap_state(state)
    return record


def _upgrade_attempt_skip_reason(state: Dict[str, Any], source_spec: PluginSpec) -> Optional[str]:
    if not _is_upgrade_attempt_spec(source_spec):
        return None
    attempts = state.get("upgrade_attempts")
    if not isinstance(attempts, dict):
        return None
    record = attempts.get(_upgrade_attempt_key(source_spec))
    if not isinstance(record, dict):
        return None
    current_fp = _upgrade_knowledge_fingerprint()
    if record.get("knowledge_fingerprint") != current_fp:
        return None
    status = str(record.get("status") or "attempted")
    reason = str(record.get("reason") or "")
    return (
        f"already {status} under current factory knowledge "
        f"(fingerprint={current_fp}, reason={reason[:240]})"
    )


def _capability_rejection_record(
    *,
    state: Dict[str, Any],
    spec: PluginSpec,
    reason: str,
    persist: bool = True,
) -> Dict[str, Any]:
    rejected = state.setdefault("rejected_capabilities", {})
    if not isinstance(rejected, dict):
        rejected = {}
        state["rejected_capabilities"] = rejected
    order = state.setdefault("rejected_capability_order", [])
    if not isinstance(order, list):
        order = []
        state["rejected_capability_order"] = order

    key = str(spec.slug)
    record = {
        "slug": key,
        "name": spec.name,
        "category": spec.category,
        "capability_type": getattr(spec, "capability_type", None),
        "intended_domain": getattr(spec, "intended_domain", None),
        "reason": reason[:1000],
        "knowledge_fingerprint": _upgrade_knowledge_fingerprint(),
        "rejected_at_unix": int(time.time()),
    }
    rejected[key] = record
    if key in order:
        order.remove(key)
    order.append(key)
    for stale_key in order[:-2000]:
        rejected.pop(stale_key, None)
    state["rejected_capability_order"] = order[-2000:]
    if persist:
        _save_ai_roadmap_state(state)
    return record


def _capability_rejection_skip_reason(state: Dict[str, Any], spec: PluginSpec) -> Optional[str]:
    rejected = state.get("rejected_capabilities")
    if not isinstance(rejected, dict):
        return None
    record = rejected.get(str(spec.slug))
    if not isinstance(record, dict):
        return None
    current_fp = _upgrade_knowledge_fingerprint()
    if record.get("knowledge_fingerprint") != current_fp:
        return None
    reason = str(record.get("reason") or "")
    return (
        f"already rejected under current factory knowledge "
        f"(fingerprint={current_fp}, reason={reason[:240]})"
    )


def _remembered_upgrade_canonical_slugs(state: Dict[str, Any]) -> Set[str]:
    attempts = state.get("upgrade_attempts")
    if not isinstance(attempts, dict):
        return set()
    current_fp = _upgrade_knowledge_fingerprint()
    remembered: Set[str] = set()
    for item in attempts.values():
        if not isinstance(item, dict):
            continue
        if item.get("knowledge_fingerprint") != current_fp:
            continue
        canonical = str(item.get("canonical_slug") or "")
        if canonical:
            remembered.add(canonical)
    return remembered


def _existing_canonical_has_registered_profile(slug: str) -> bool:
    """
    Return True when the installed canonical module already carries the
    registered deterministic profile for its capability family.

    This is deliberately conservative: it only treats a capability as retained
    when the installed source names the profile that the current registry would
    generate for the same canonical slug. A changed registry/spec/template
    fingerprint still reopens future upgrade attempts.
    """
    if not callable(_registered_profile_id):
        return False
    profile_id = _registered_profile_id(slug)
    if not profile_id:
        return False
    plugin_path = PLUGINS_DIR / f"{slug}.py"
    try:
        source = plugin_path.read_text(encoding="utf-8")
    except OSError:
        return False
    expected_literals = [
        f"logic_profile_id = {profile_id!r}",
        f"\"logic_profile_id\": {profile_id!r}",
        f"'logic_profile_id': {profile_id!r}",
    ]
    return any(literal in source for literal in expected_literals)


def _seed_retained_canonical_upgrade_memory(
    state: Dict[str, Any],
    existing_slugs: Set[str],
    *,
    persist: bool = True,
) -> int:
    """
    Mark existing registered-profile capabilities as retained upgrade baselines.

    Upgrade expansion is an improvement mechanism, not permission to mint
    duplicates. If the canonical module already exists with the registered
    profile, a metadata-only retry is not new knowledge. The
    generation fingerprint keeps this from hiding future improvements after the
    factory's specs, profiles, templates, or Station B rules change.
    """
    attempts = state.setdefault("upgrade_attempts", {})
    if not isinstance(attempts, dict):
        attempts = {}
        state["upgrade_attempts"] = attempts

    seeded = 0
    current_fp = _upgrade_knowledge_fingerprint()
    for position, blueprint in enumerate(AI_CAPABILITY_ROADMAP, start=1):
        canonical_spec, _, _ = build_next_spec(position)
        canonical_slug = canonical_spec.slug
        legacy_slug = blueprint.slug
        active_slug = canonical_slug if canonical_slug in existing_slugs else legacy_slug
        if canonical_slug not in existing_slugs and legacy_slug not in existing_slugs:
            continue
        existing_record = attempts.get(canonical_slug)
        if isinstance(existing_record, dict) and existing_record.get("knowledge_fingerprint") == current_fp:
            continue
        if not _existing_canonical_has_registered_profile(active_slug):
            continue

        upgrade_spec, _, _ = build_next_spec(position)
        upgrade_spec = copy.deepcopy(upgrade_spec)
        upgrade_spec.extra = dict(getattr(upgrade_spec, "extra", {}) or {})
        upgrade_spec.extra["generation_round"] = 2
        canonical_spec = _canonical_retention_spec(upgrade_spec)
        _upgrade_attempt_record(
            state=state,
            source_spec=upgrade_spec,
            canonical_spec=canonical_spec,
            status="retained",
            reason=(
                "canonical capability already has the current registered profile; "
                "metadata-only retry is not an improvement"
            ),
            persist=False,
        )
        seeded += 1

    if seeded and persist:
        _save_ai_roadmap_state(state)
    return seeded


def _upgrade_backlog_exhausted(state: Dict[str, Any], existing_slugs: Set[str]) -> bool:
    canonical_slugs: Set[str] = set()
    for position, blueprint in enumerate(AI_CAPABILITY_ROADMAP, start=1):
        spec, _, _ = build_next_spec(position)
        if spec.slug in existing_slugs or blueprint.slug in existing_slugs:
            canonical_slugs.add(spec.slug)
    if not canonical_slugs:
        return False
    remembered = _remembered_upgrade_canonical_slugs(state)
    return canonical_slugs.issubset(remembered)


def _anticipated_capability_candidates(
    existing_slugs: Set[str],
    *,
    start_index: int,
    limit: int = 6,
    scan_window: int = 300,
) -> list[Dict[str, Any]]:
    """
    Look ahead from the current roadmap cursor and describe fresh capabilities.

    This is deliberately advisory. It does not create duplicate modules or move
    the cursor; it gives Station B/profile handoffs enough forward context to
    build the current capability as part of an intentional sequence.
    """
    anticipated: list[Dict[str, Any]] = []
    seen: Set[str] = set(existing_slugs)
    safe_start = max(int(start_index), 1)
    safe_limit = max(int(limit), 0)
    if safe_limit == 0:
        return anticipated

    for candidate_index in range(safe_start, safe_start + max(int(scan_window), safe_limit)):
        try:
            candidate, capability_type, intended_domain = build_next_spec(candidate_index)
        except Exception:
            LOG.debug("Unable to build anticipated capability at index %s", candidate_index, exc_info=True)
            break
        slug = str(getattr(candidate, "slug", "") or "")
        if not slug or slug in seen or (PLUGINS_DIR / f"{slug}.py").exists():
            seen.add(slug)
            continue
        extra = getattr(candidate, "extra", {}) or {}
        anticipated.append(
            {
                "index": candidate_index,
                "slug": slug,
                "name": getattr(candidate, "name", ""),
                "category": getattr(candidate, "category", ""),
                "capability_type": capability_type,
                "intended_domain": intended_domain,
                "continuous_expansion": bool(extra.get("continuous_expansion")),
                "reason": (
                    "fresh canonical capability after current installed set"
                    if bool(extra.get("continuous_expansion"))
                    else "unbuilt curated roadmap capability"
                ),
            }
        )
        seen.add(slug)
        if len(anticipated) >= safe_limit:
            break
    return anticipated


def _refresh_anticipation_state(
    state: Dict[str, Any],
    existing_slugs: Set[str],
    *,
    start_index: int,
    persist: bool = True,
) -> list[Dict[str, Any]]:
    anticipated = _anticipated_capability_candidates(existing_slugs, start_index=start_index)
    state["anticipated_next_capabilities"] = anticipated
    if persist:
        _save_ai_roadmap_state(state)
    return anticipated


def _build_ai_handoff_context(state: Dict[str, Any], spec: PluginSpec) -> str:
    completed = state.get("completed")
    if not isinstance(completed, list):
        completed = []
    recent = completed[-5:]
    lines = [
        "AI ROADMAP HANDOFF CONTEXT:",
        "Use this to build forward instead of reinventing prior plugins.",
    ]
    next_directive = str(state.get("next_directive") or "").strip()
    if next_directive:
        lines.append("")
        lines.append("Directive from previous plugin:")
        lines.append(next_directive)
    if recent:
        lines.append("")
        lines.append("Recently completed AI roadmap plugins:")
        for item in recent:
            if not isinstance(item, dict):
                continue
            lines.append(
                "- {slug}: {name} | capability={capability} | role={role}".format(
                    slug=item.get("slug", ""),
                    name=item.get("name", ""),
                    capability=item.get("capability_type", ""),
                    role=item.get("handoff_role", ""),
                )
            )
    attempts = state.get("upgrade_attempts")
    order = state.get("upgrade_attempt_order")
    if isinstance(attempts, dict) and isinstance(order, list):
        recent_attempts = [
            attempts.get(str(key))
            for key in order[-8:]
            if isinstance(attempts.get(str(key)), dict)
        ]
        if recent_attempts:
            lines.append("")
            lines.append("Recent canonical upgrade attempts:")
            for item in recent_attempts:
                lines.append(
                    "- {source} -> {canonical}: {status}; {reason}".format(
                        source=item.get("source_slug", ""),
                        canonical=item.get("canonical_slug", ""),
                        status=item.get("status", ""),
                        reason=str(item.get("reason", ""))[:180],
                    )
                )
    anticipated = state.get("anticipated_next_capabilities")
    if isinstance(anticipated, list):
        upcoming = [item for item in anticipated[:6] if isinstance(item, dict)]
        if upcoming:
            lines.append("")
            lines.append("Anticipated next capabilities:")
            for item in upcoming:
                lines.append(
                    "- {slug}: {name} | category={category} | reason={reason}".format(
                        slug=item.get("slug", ""),
                        name=item.get("name", ""),
                        category=item.get("category", ""),
                        reason=item.get("reason", ""),
                    )
                )
    lines.append("")
    lines.append(
        "Current task must be complementary: implement {slug} ({name}) and consume prior outputs "
        "when payload contains previous_results, roadmap_state, progress_state, or completed_plugins.".format(
            slug=spec.slug,
            name=spec.name,
        )
    )
    return "\n".join(lines)


def _attach_ai_handoff_to_spec(spec: PluginSpec, state: Dict[str, Any]) -> None:
    if not _is_ai_roadmap_spec(spec):
        return
    extra = dict(getattr(spec, "extra", {}) or {})
    extra["handoff_context"] = _build_ai_handoff_context(state, spec)
    extra["prior_ai_plugins"] = (state.get("completed") or [])[-8:]
    extra["previous_directive"] = state.get("next_directive", "")
    extra["anticipated_next_capabilities"] = (state.get("anticipated_next_capabilities") or [])[:6]
    spec.extra = extra


def _record_ai_roadmap_success(
    *,
    state: Dict[str, Any],
    spec: PluginSpec,
    plugin_path: Path,
    next_spec: Optional[PluginSpec],
) -> Dict[str, Any]:
    completed = state.get("completed")
    if not isinstance(completed, list):
        completed = []

    handoff_role = (
        f"{spec.name} owns {getattr(spec, 'intended_domain', '')}. Future plugins should reuse its "
        "outputs as previous_results and avoid recreating its prompt, scorecard, progress, or fun-mode behavior."
    )
    completed.append(
        {
            "slug": spec.slug,
            "name": spec.name,
            "category": spec.category,
            "capability_type": getattr(spec, "capability_type", None),
            "intended_domain": getattr(spec, "intended_domain", None),
            "path": str(plugin_path),
            "use_cases": list(getattr(spec, "use_cases", []) or [])[:6],
            "handoff_role": handoff_role,
        }
    )

    if next_spec is not None:
        next_directive = (
            f"Next plugin task: build {next_spec.name} ({next_spec.slug}) as a complementary capability after "
            f"{spec.name}. Do not rebuild {spec.slug}. If payload includes previous_results or roadmap_state, "
            f"read {spec.slug}'s summary, progress_state, user_experience, fun_mode, and recommended_actions, "
            f"then advance the workflow toward {getattr(next_spec, 'intended_domain', '')}."
        )
    else:
        next_directive = (
            f"Continue after {spec.name} by building the next AI roadmap capability as a complement, not a duplicate."
        )

    state["completed"] = completed[-100:]
    state["last_completed"] = completed[-1]
    state["next_directive"] = next_directive
    _save_ai_roadmap_state(state)
    return state


def _seed_ai_roadmap_state_from_existing(
    state: Dict[str, Any],
    existing_slugs: Set[str],
) -> Dict[str, Any]:
    completed = state.get("completed")
    if isinstance(completed, list) and completed:
        return state

    existing_indexes = sorted(
        idx for slug in existing_slugs
        for idx in [_roadmap_slug_index(slug)]
        if idx is not None
    )
    if not existing_indexes:
        return state

    seeded: Dict[str, Any] = {"completed": [], "next_directive": ""}
    last_spec: Optional[PluginSpec] = None
    for idx in existing_indexes:
        try:
            spec, _, _ = build_next_spec(idx)
        except Exception:
            continue
        last_spec = spec
        _record_ai_roadmap_success(
            state=seeded,
            spec=spec,
            plugin_path=PLUGINS_DIR / f"{spec.slug}.py",
            next_spec=None,
        )

    if last_spec is not None:
        try:
            next_spec, _, _ = build_next_spec(max(existing_indexes) + 1)
        except Exception:
            next_spec = None
        _record_ai_roadmap_success(
            state=seeded,
            spec=last_spec,
            plugin_path=PLUGINS_DIR / f"{last_spec.slug}.py",
            next_spec=next_spec,
        )
        # _record_ai_roadmap_success added last_spec twice; collapse by slug.
        by_slug: Dict[str, Dict[str, Any]] = {}
        for item in seeded.get("completed", []):
            if isinstance(item, dict) and item.get("slug"):
                by_slug[str(item["slug"])] = item
        seeded["completed"] = list(by_slug.values())
        _save_ai_roadmap_state(seeded)
        LOG.info("Seeded AI roadmap handoff state from %d existing AI capability module(s).", len(seeded["completed"]))
        return seeded

    return state


def _write_plugin_file(slug: str, source: str) -> Path:
    _ensure_plugins_dir()
    path = PLUGINS_DIR / f"{slug}.py"
    path.write_text(source, encoding="utf-8")
    return path


class DraftRepairGateError(RuntimeError):
    """Raised when the repair surgeon says a candidate must not continue."""

    def __init__(
        self,
        *,
        slug: str,
        action: str,
        findings: Sequence[Any],
        candidate_path: Path,
        quarantine_path: Path | None = None,
    ) -> None:
        self.slug = slug
        self.action = action
        self.findings = list(findings)
        self.candidate_path = candidate_path
        self.quarantine_path = quarantine_path
        location = f"; moved to {quarantine_path}" if quarantine_path is not None else ""
        super().__init__(
            f"draft_repair_gate: {slug} requires {action}; findings={self.findings}{location}"
        )


def _write_candidate_plugin_file(slug: str, source: str) -> Path:
    CANDIDATE_PLUGINS_DIR.mkdir(parents=True, exist_ok=True)
    path = CANDIDATE_PLUGINS_DIR / f"{slug}.py"
    path.write_text(source, encoding="utf-8")
    if _repair_draft_plugin_file is not None:
        try:
            repair_result = _repair_draft_plugin_file(path, dry_run=False, validate=True)
            if repair_result.applied_patches:
                LOG.info(
                    "Draft repair surgeon patched candidate %r: %s",
                    slug,
                    ", ".join(repair_result.applied_patches),
                )
            if repair_result.recommended_next_action != "retest":
                LOG.warning(
                    "Draft repair surgeon flagged candidate %r for %s: %s",
                    slug,
                    repair_result.recommended_next_action,
                    repair_result.remaining_findings,
                )
                reason = (
                    "draft_repair_gate: "
                    f"action={repair_result.recommended_next_action}; "
                    f"findings={repair_result.remaining_findings}; "
                    f"recipe={repair_result.repair_recipe}"
                )
                try:
                    quarantine_path = _discard_candidate_plugin(path, reason=reason)
                except Exception:
                    quarantine_path = None
                    LOG.warning("Unable to quarantine repair-gated candidate %r", slug, exc_info=True)
                raise DraftRepairGateError(
                    slug=slug,
                    action=repair_result.recommended_next_action,
                    findings=repair_result.remaining_findings,
                    candidate_path=path,
                    quarantine_path=quarantine_path,
                )
        except Exception:
            if sys.exc_info()[0] is DraftRepairGateError:
                raise
            LOG.warning("Draft repair surgeon failed for candidate %r.", slug, exc_info=True)
    return path


def _promote_candidate_plugin(candidate_path: Path, slug: str) -> Path:
    _ensure_plugins_dir()
    final_path = PLUGINS_DIR / f"{slug}.py"
    candidate_path.replace(final_path)
    return final_path


def _discard_candidate_plugin(candidate_path: Path, *, reason: str) -> Path:
    quarantine_dir = ROOT_DIR / "junk_plugins" / "semantic_rejections"
    quarantine_dir.mkdir(parents=True, exist_ok=True)
    target = quarantine_dir / candidate_path.name
    if target.exists():
        target = quarantine_dir / f"{candidate_path.stem}_{os.getpid()}{candidate_path.suffix}"
    candidate_path.replace(target)
    reason_path = target.with_suffix(target.suffix + ".reason.txt")
    reason_path.write_text(reason, encoding="utf-8")
    return target


async def _validate_plugin_file(path: Path, spec: PluginSpec) -> Tuple[bool, str]:
    """
    Validate a generated plugin across old and new Station C entrypoint shapes.

    Parent Francis currently exposes a path-based sync helper. The sidecar
    factory validator exposes an async module/spec helper. Supporting both keeps
    this runner usable in production and in isolated repo checks.
    """
    sig = inspect.signature(validate_plugin_module)
    params = list(sig.parameters)

    if len(params) == 1:
        result = validate_plugin_module(path)
    else:
        module_name = spec.slug.replace("-", "_")
        module_spec = importlib.util.spec_from_file_location(module_name, path)
        if module_spec is None or module_spec.loader is None:
            return False, f"Unable to import generated plugin from {path}"
        module = importlib.util.module_from_spec(module_spec)
        module_spec.loader.exec_module(module)  # type: ignore[call-arg]
        result = validate_plugin_module(module, spec)

    if inspect.isawaitable(result):
        result = await result

    if isinstance(result, tuple) and len(result) >= 2:
        return bool(result[0]), str(result[1])

    ok = bool(getattr(result, "ok", False))
    report = str(getattr(result, "error_report", "") or "")
    if not report:
        errors = getattr(result, "errors", None)
        warnings = getattr(result, "warnings", None)
        if errors or warnings:
            report = f"errors={errors or []}; warnings={warnings or []}"
    return ok, report


def _build_memory_context(existing_slugs: Set[str], *, max_items: int = 50) -> Optional[str]:
    """
    Build a simple memory_context string listing existing plugins.

    This gives Station B awareness of current skills so it can avoid
    generating obvious duplicates, even before a richer registry/memory
    layer is wired in.
    """
    if not existing_slugs:
        return None

    sorted_slugs = sorted(existing_slugs)
    if max_items > 0:
        sorted_slugs = sorted_slugs[:max_items]

    lines = [
        f"- {slug}: existing plugin; avoid generating an equivalent capability under a new name."
        for slug in sorted_slugs
    ]
    return "Existing plugins already available in the system:\n" + "\n".join(lines)


def _jsonish_text(value: Any, *, max_chars: int = 12000) -> str:
    try:
        text = json.dumps(value, sort_keys=True, default=str)
    except Exception:
        text = str(value)
    return text[:max_chars].lower()


def _word_set(text: str) -> Set[str]:
    import re

    return {
        token
        for token in re.findall(r"[a-z][a-z0-9_]{3,}", text.lower())
        if token
        not in {
            "action",
            "actions",
            "analysis",
            "available",
            "confidence",
            "context",
            "current",
            "detail",
            "details",
            "field",
            "fields",
            "plugin",
            "prompt",
            "result",
            "score",
            "scores",
            "summary",
            "task",
            "value",
            "workflow",
        }
    }


def _extract_output_payload(envelope: Any) -> Dict[str, Any]:
    if not isinstance(envelope, dict):
        return {"raw": envelope}
    output = envelope.get("output")
    if isinstance(output, dict):
        nested = output.get("result")
        if isinstance(nested, dict):
            return nested
        return output
    return envelope


def _decision_surface(result: Dict[str, Any]) -> Dict[str, Any]:
    """
    Focus semantic checks on decision fields, not passive evidence echoes.

    A shallow plugin can pass by echoing payload values in `details`; the gate
    cares whether those values influence insights, actions, progress, and user
    guidance.
    """
    progress = result.get("progress_state") if isinstance(result.get("progress_state"), dict) else {}
    user_exp = result.get("user_experience") if isinstance(result.get("user_experience"), dict) else {}
    return {
        "summary": result.get("summary"),
        "primary_insights": result.get("primary_insights"),
        "recommended_actions": result.get("recommended_actions"),
        "scores": result.get("scores"),
        "next_step": progress.get("next_step") if isinstance(progress, dict) else None,
        "plain_language_takeaway": user_exp.get("plain_language_takeaway") if isinstance(user_exp, dict) else None,
        "details": {
            "identified_vagueness": (result.get("details") or {}).get("identified_vagueness")
            if isinstance(result.get("details"), dict)
            else None,
            "missing_constraints": (result.get("details") or {}).get("missing_constraints")
            if isinstance(result.get("details"), dict)
            else None,
            "rewrites": (result.get("details") or {}).get("rewrites")
            if isinstance(result.get("details"), dict)
            else None,
        },
    }


def _payload_signal_tokens(payload: Dict[str, Any]) -> Set[str]:
    text = _jsonish_text(payload)
    tokens = _word_set(text)
    # Keep tokens that are likely to distinguish one payload from another.
    generic = {
        "agent",
        "candidate",
        "current_plan",
        "objective",
        "outputs",
        "payload",
        "previous",
        "results",
        "steps",
        "user",
    }
    return {token for token in tokens if token not in generic}


async def _invoke_plugin_for_semantic_check(module: Any, payload: Dict[str, Any], slug: str) -> Dict[str, Any]:
    invoke = getattr(module, "invoke", None)
    if not callable(invoke):
        raise RuntimeError("plugin has no callable invoke")
    result = invoke(
        "factory-semantic-depth",
        payload,
        run_id=f"semantic-depth-{slug}",
    )
    if inspect.isawaitable(result):
        result = await result
    return _extract_output_payload(result)


async def _semantic_depth_check(plugin_path: Path, spec: PluginSpec) -> Tuple[bool, str]:
    """
    Detect capability modules that merely fill the expected shape with stock advice.

    The check compares two structurally similar but semantically different
    payloads. A useful AI capability should let payload values influence insight,
    action, progress, or guidance fields, not only echo values in details.
    """
    module_name = f"semantic_depth_{spec.slug}".replace("-", "_")
    module_spec = importlib.util.spec_from_file_location(module_name, plugin_path)
    if module_spec is None or module_spec.loader is None:
        return False, f"semantic_depth: unable to import {plugin_path}"
    module = importlib.util.module_from_spec(module_spec)
    module_spec.loader.exec_module(module)  # type: ignore[call-arg]

    payload_a = {
        "task": "Plan a multi-agent refactor of authentication middleware without breaking login.",
        "objective": "Separate database migration, API changes, test coverage, and rollback checks.",
        "prompt": "Fix auth and add tests.",
        "current_plan": ["Inspect auth middleware", "Add login regression tests"],
        "completed_steps": ["Mapped current session flow"],
        "blocked_steps": ["Need database migration owner"],
        "agents": ["builder", "database reviewer", "test owner"],
        "workstreams": ["middleware refactor", "migration review", "login regression tests"],
        "ownership_scopes": ["code changes", "schema safety", "test coverage"],
        "candidate_outputs": [
            {"id": "plan_a", "summary": "Change middleware first"},
            {"id": "plan_b", "summary": "Write login tests before code changes"},
        ],
        "constraints": ["No production outage", "Keep rollback explicit"],
    }
    payload_b = {
        "task": "Choose tools for verifying hallucination risk in a retrieved medical-summary answer.",
        "objective": "Decide whether to browse sources, inspect citations, or run local consistency checks.",
        "prompt": "Is this claim grounded enough to show the user?",
        "trace": [{"tool": "retrieval", "status": "partial", "issue": "citation mismatch"}],
        "current_plan": ["Compare answer claims to source snippets"],
        "completed_steps": ["Collected candidate answer"],
        "blocked_steps": ["Need citation verification"],
        "agents": ["researcher", "citation reviewer", "answer editor"],
        "workstreams": ["retrieval review", "citation matching", "safe rewrite"],
        "ownership_scopes": ["source grounding", "unsupported claim audit", "user-facing answer"],
        "candidate_outputs": [
            {"id": "answer_a", "summary": "States an unsupported dosage claim"},
            {"id": "answer_b", "summary": "Flags missing source support"},
        ],
        "constraints": ["Do not invent clinical facts", "Escalate uncertain claims"],
    }

    result_a = await _invoke_plugin_for_semantic_check(module, payload_a, spec.slug)
    result_b = await _invoke_plugin_for_semantic_check(module, payload_b, spec.slug)

    capability_ok, capability_reason = _capability_semantic_contract(spec, result_a, result_b)
    if not capability_ok:
        return False, capability_reason

    decision_a = _decision_surface(result_a)
    decision_b = _decision_surface(result_b)

    text_a = _jsonish_text(decision_a)
    text_b = _jsonish_text(decision_b)
    tokens_a = _payload_signal_tokens(payload_a)
    tokens_b = _payload_signal_tokens(payload_b)
    reflected_a = sorted(tokens_a & _word_set(text_a))
    reflected_b = sorted(tokens_b & _word_set(text_b))

    if len(reflected_a) < 2 or len(reflected_b) < 2:
        return (
            False,
            "semantic_depth: decision fields do not reflect enough payload values "
            f"(a={reflected_a[:5]}, b={reflected_b[:5]}).",
        )

    words_a = _word_set(text_a)
    words_b = _word_set(text_b)
    union = words_a | words_b
    similarity = (len(words_a & words_b) / len(union)) if union else 1.0
    if similarity > 0.78:
        return (
            False,
            f"semantic_depth: outputs are too similar across different payloads (similarity={similarity:.2f}).",
        )

    scores_a = result_a.get("scores") if isinstance(result_a.get("scores"), dict) else {}
    scores_b = result_b.get("scores") if isinstance(result_b.get("scores"), dict) else {}
    if scores_a == scores_b and scores_a:
        return False, "semantic_depth: scores are identical across semantically different payloads."

    return (
        True,
        "semantic_depth: payload values influenced decision fields "
        f"(a={reflected_a[:5]}, b={reflected_b[:5]}, similarity={similarity:.2f}).",
    )


def _module_from_plugin_path(plugin_path: Path, *, slug: str, purpose: str) -> Any:
    module_name = f"{purpose}_{slug}_{os.getpid()}".replace("-", "_")
    module_spec = importlib.util.spec_from_file_location(module_name, plugin_path)
    if module_spec is None or module_spec.loader is None:
        raise RuntimeError(f"unable to import {plugin_path}")
    module = importlib.util.module_from_spec(module_spec)
    module_spec.loader.exec_module(module)  # type: ignore[call-arg]
    return module


def _capability_quality_score(output: Dict[str, Any]) -> float:
    text = _jsonish_text(output, max_chars=20000)
    if any(marker in text for marker in ["fallback applied", "capability_profile_error", "no-op analysis", "semantic_repair"]):
        return -1.0

    summary = output.get("summary")
    insights = output.get("primary_insights")
    actions = output.get("recommended_actions")
    scores = output.get("scores") if isinstance(output.get("scores"), dict) else {}
    details = output.get("details") if isinstance(output.get("details"), dict) else {}
    progress = output.get("progress_state") if isinstance(output.get("progress_state"), dict) else {}
    user_exp = output.get("user_experience") if isinstance(output.get("user_experience"), dict) else {}
    fun = output.get("fun_mode") if isinstance(output.get("fun_mode"), dict) else {}

    score = 0.0
    if isinstance(summary, str) and len(summary.strip()) >= 30:
        score += 0.10
    if isinstance(insights, list) and insights:
        score += min(0.18, 0.045 * len(insights))
    if isinstance(actions, list) and actions:
        score += min(0.24, 0.06 * len(actions))
        action_words = _word_set(_jsonish_text(actions, max_chars=8000))
        score += min(0.12, 0.006 * len(action_words))
    confidence = scores.get("confidence")
    if isinstance(confidence, (int, float)):
        score += max(0.0, min(0.18, float(confidence) * 0.18))
    score += min(0.18, 0.018 * len([key for key, value in details.items() if value not in (None, "", [], {})]))
    if details.get("logic_profile_id"):
        score += 0.08
    if progress.get("next_step"):
        score += 0.05
    if user_exp.get("plain_language_takeaway"):
        score += 0.04
    if fun.get("challenge_label") or fun.get("score_badge"):
        score += 0.02
    return round(score, 4)


async def _production_quality_gate(
    plugin_path: Path,
    spec: PluginSpec,
    *,
    threshold: float = PRODUCTION_QUALITY_THRESHOLD,
) -> Tuple[bool, str]:
    """
    Enforce the production score before a candidate becomes installable.

    This is intentionally stricter than structural validation and semantic
    depth: those gates prove the module runs and reacts to payloads; this gate
    proves it returns enough useful, capability-specific surface area to keep.
    """
    module = _module_from_plugin_path(plugin_path, slug=spec.slug, purpose="production_quality")
    output = await _invoke_plugin_for_semantic_check(
        module,
        PRODUCTION_QUALITY_PROBE_PAYLOAD,
        f"{spec.slug}-production-quality",
    )
    score = _capability_quality_score(output)
    if score < threshold:
        return (
            False,
            f"production_quality: score {score:.4f} < threshold {threshold:.2f}",
        )
    return (
        True,
        f"production_quality: score {score:.4f} >= threshold {threshold:.2f}",
    )


async def _a_plus_certification_gate(
    plugin_path: Path,
    spec: PluginSpec,
    *,
    threshold: float = A_PLUS_MIN_SCORE,
) -> Tuple[bool, str]:
    """
    Certify that a validated capability is A+ material before promotion.

    Production quality proves the module is useful enough to keep. A+ adds
    probe-level checks for missing-input behavior, non-dict payload warnings,
    diagnostics richness, profile-specific details, and semantic contrast.
    """
    if _certify_a_plus_plugin is None or _summarize_a_plus_result is None:
        return False, "a_plus: certification layer is unavailable"
    module = _module_from_plugin_path(plugin_path, slug=spec.slug, purpose="a_plus")
    invoke = getattr(module, "invoke", None)
    if not callable(invoke):
        return False, "a_plus: plugin has no callable invoke"
    result = await _certify_a_plus_plugin(
        invoke,
        metadata={
            "slug": getattr(spec, "slug", ""),
            "name": getattr(spec, "name", ""),
            "category": getattr(spec, "category", ""),
            "capability_type": getattr(spec, "capability_type", ""),
            "intended_domain": getattr(spec, "intended_domain", ""),
            "use_cases": list(getattr(spec, "use_cases", []) or []),
        },
        threshold=threshold,
    )
    return bool(result.passed), _summarize_a_plus_result(result)


_CAPABILITY_NAME_CONTRACTS: tuple[tuple[str, dict[str, Any]], ...] = (
    (
        "tool_argument_checker",
        {
            "required_detail_keys": {"argument_risks", "unsafe_arguments", "sanitized_arguments", "argument_safety_decision"},
            "forbidden_detail_keys": set(),
        },
    ),
    (
        "output_completeness_grader",
        {
            "required_detail_keys": {"completeness_findings", "missing_sections", "completeness_score"},
            "forbidden_detail_keys": {"action_plan", "actionability_gaps"},
        },
    ),
    (
        "response_action_planner",
        {
            "required_detail_keys": {"action_plan", "actionability_gaps", "next_step_checks"},
            "forbidden_detail_keys": {"completeness_findings"},
        },
    ),
    (
        "rollback_guard_builder",
        {
            "required_detail_keys": {"rollback_plan", "rollback_readiness", "blast_radius", "missing_rollback_controls"},
            "forbidden_detail_keys": set(),
        },
    ),
    (
        "verification_checklist_builder",
        {
            "required_detail_keys": {"verification_checklist", "automated_checks", "human_review_checks"},
            "forbidden_detail_keys": set(),
        },
    ),
    (
        "agent_handoff_checker",
        {
            "required_detail_keys": {"handoff_inputs", "ownership_boundaries", "handoff_overlap_decision"},
            "forbidden_detail_keys": set(),
        },
    ),
    (
        "parallelization_planner",
        {
            "required_detail_keys": {"sequenced_plan", "handoff_packet"},
            "forbidden_detail_keys": {"ownership_boundaries"},
        },
    ),
)


def _capability_name_marker(slug: str) -> Optional[str]:
    slug = str(slug or "")
    for marker, _contract in sorted(_CAPABILITY_NAME_CONTRACTS, key=lambda item: len(item[0]), reverse=True):
        if marker in slug:
            return marker
    return None


def _capability_family_prefix(slug: str) -> str:
    marker = _capability_name_marker(slug)
    if not marker:
        return str(slug or "")
    return str(slug or "").split(marker, 1)[0].strip("_-")


_CONTINUOUS_SCENARIO_KEY_CACHE: Dict[str, Optional[str]] = {}


def _continuous_scenario_key(slug: str) -> Optional[str]:
    """
    Return the deterministic use-case scenario for continuous-expansion slugs.

    Short numbered slugs intentionally remove target/context/mode from the
    filename. Sibling comparison still needs that context so it can compare
    handoff vs parallelization inside the same scenario without treating every
    verification checklist across the whole library as the same sibling.
    """
    slug = str(slug or "")
    if slug in _CONTINUOUS_SCENARIO_KEY_CACHE:
        return _CONTINUOUS_SCENARIO_KEY_CACHE[slug]

    try:
        idx = _roadmap_slug_index(slug)
    except Exception:
        idx = None
    if idx is None or idx <= len(AI_CAPABILITY_ROADMAP):
        _CONTINUOUS_SCENARIO_KEY_CACHE[slug] = None
        return None
    try:
        spec, _capability_type, intended_domain = build_next_spec(idx)
    except Exception:
        _CONTINUOUS_SCENARIO_KEY_CACHE[slug] = None
        return None
    use_case = ""
    try:
        if spec.use_cases:
            use_case = str(spec.use_cases[0] or "")
    except Exception:
        use_case = ""
    scenario_key = use_case or str(intended_domain or "")
    _CONTINUOUS_SCENARIO_KEY_CACHE[slug] = scenario_key
    return scenario_key


def _normalized_gate_profile_id(profile_id: Any) -> str:
    raw = str(profile_id or "").strip()
    if not raw:
        return ""
    if callable(_normalize_logic_profile_id):
        try:
            return str(_normalize_logic_profile_id(raw) or raw)
        except Exception:
            return raw
    return raw


_GENERIC_REQUIRED_DETAIL_KEYS = [
    "missing_inputs",
    "payload_warnings",
    "logic_profile_id",
    "has_user_input",
    "used_goal_fallback",
]

_PROFILE_REQUIRED_DETAIL_KEYS: Dict[str, Set[str]] = {
    "prompt_refinement_profile": {"identified_vagueness", "missing_constraints", "rewrites", "refined_prompt"},
    "structured_prompt_builder_profile": {"structured_prompt", "output_schema", "checklist"},
    "grounded_answer_planner_profile": {"supported_claims", "unsupported_claims", "evidence_map", "answer_plan", "caveats"},
    "hallucination_risk_auditor_profile": {"claims", "high_risk_claims", "safer_rewrites"},
    "context_window_optimizer_profile": {"kept_context", "compressed_context", "dropped_context", "token_budget"},
    "memory_compression_profile": {"memory_summary", "durable_facts", "open_threads"},
    "multi_agent_handoff_profile": {"handoff_inputs", "ownership_boundaries", "handoff_overlap_decision"},
    "task_planner_profile": {"sequenced_plan", "handoff_packet", "risk_signals"},
    "automation_safety_gate_profile": {"risk_findings", "controls", "approval_required"},
    "prompt_injection_surface_scanner_profile": {"injection_findings", "trust_boundaries", "handling_rules", "sanitized_context_plan"},
    "output_quality_scorer_profile": {"covered_requirements", "missing_requirements", "improvement_checklist"},
    "requirement_gap_analyzer_profile": {"requirement_gaps", "assumptions", "clarification_questions", "readiness_decision"},
    "artifact_release_note_generator_profile": {"release_notes", "validation_evidence", "changed_artifacts", "known_risks"},
    "data_contract_mapper_profile": {"input_contract", "output_contract", "validation_rules", "schema_gaps"},
    "autonomous_run_governor_profile": {"governance_decision", "run_signals", "stop_conditions", "allowed_next_actions"},
    "model_selection_scorecard_profile": {"model_scorecard", "selected_model_style", "cost_risk_tradeoffs", "escalation_triggers"},
    "instruction_conflict_detector_profile": {"instruction_sources", "conflicts", "clarified_instruction"},
    "retrieval_query_expander_profile": {"expanded_queries", "facet_terms", "grounding_plan"},
    "workflow_debugger_profile": {"failure_points", "signals_by_stage", "retry_plan"},
    "plugin_spec_architect_profile": {"spec_blueprint", "uniqueness_checks", "capability_boundaries", "prompt_requirements"},
    "plugin_logic_blueprint_designer_profile": {"logic_blueprint", "deterministic_rules", "data_flow", "failure_modes"},
    "plugin_quality_gate_designer_profile": {"quality_gates", "rejection_rules", "semantic_probes", "pass_criteria"},
    "plugin_test_payload_generator_profile": {"test_payloads", "edge_cases", "expected_differences", "regression_watchlist"},
    "capability_overlap_checker_profile": {"duplicate_risks", "uniqueness_fingerprint", "comparison_targets", "merge_or_reject_decision", "max_similarity", "missing_inputs"},
    "plugin_repair_strategy_planner_profile": {"repair_plan", "weak_signals", "capability_specific_targets", "acceptance_checks"},
    "plugin_release_packager_profile": {"release_package", "validation_summary", "github_publish_plan", "rollback_notes"},
    "plugin_factory_backlog_planner_profile": {"backlog_items", "priority_rationale", "dependency_order", "next_plugin_specs"},
    "plugin_profile_gap_detector_profile": {"profile_gaps", "missing_profile_slugs", "alias_gaps", "coverage_summary"},
    "semantic_probe_result_analyzer_profile": {"probe_failures", "contrast_findings", "repair_targets", "promotion_recommendation"},
    "release_readiness_scorecard_profile": {"readiness_checks", "blocking_findings", "release_decision", "evidence_summary"},
    "continuous_prompt_contract_designer_profile": {"structured_prompt", "requirements", "output_schema", "checklist"},
    "continuous_evidence_gap_detector_profile": {"answer_plan", "supported_claims", "unsupported_claims", "evidence_map"},
    "continuous_source_quality_ranker_profile": {"ranked_sources", "anchor_sources", "rejected_sources", "ranking_criteria"},
    "continuous_memory_update_recommender_profile": {"memory_summary", "durable_facts", "discard_candidates", "open_threads"},
    "continuous_tool_safety_reviewer_profile": {"risk_findings", "approval_required", "controls"},
    "continuous_trace_failure_router_profile": {"failure_points", "root_cause_stage", "retry_plan"},
    "continuous_retrieval_query_planner_profile": {"core_query", "expanded_queries", "grounding_plan"},
    "continuous_citation_priority_scorer_profile": {"claims", "risk_domains", "verification_priorities", "citation_plan"},
    "continuous_instruction_hierarchy_checker_profile": {"conflicts", "clarified_instruction", "instruction_sources"},
    "continuous_tool_argument_checker_profile": {"argument_risks", "unsafe_arguments", "sanitized_arguments", "argument_safety_decision"},
    "continuous_output_completeness_grader_profile": {"completeness_findings", "missing_sections", "completeness_score"},
    "continuous_response_action_planner_profile": {"action_plan", "actionability_gaps", "next_step_checks"},
    "continuous_verification_checklist_builder_profile": {"verification_checklist", "automated_checks", "human_review_checks"},
    "continuous_rollback_guard_builder_profile": {"rollback_plan", "rollback_readiness", "blast_radius", "missing_rollback_controls"},
}

_PROFILE_REQUIRED_DETAIL_FALLBACKS: tuple[tuple[str, str], ...] = (
    ("continuous_prompt_contract_designer_profile", "structured_prompt_builder_profile"),
    ("continuous_prompt_clarity_auditor_profile", "prompt_refinement_profile"),
    ("continuous_evidence_gap_detector_profile", "grounded_answer_planner_profile"),
    ("continuous_source_quality_ranker_profile", "grounded_answer_planner_profile"),
    ("continuous_context_noise_filter_profile", "context_window_optimizer_profile"),
    ("continuous_memory_update_recommender_profile", "memory_compression_profile"),
    ("continuous_agent_handoff_checker_profile", "multi_agent_handoff_profile"),
    ("continuous_parallelization_planner_profile", "task_planner_profile"),
    ("continuous_tool_safety_reviewer_profile", "automation_safety_gate_profile"),
    ("continuous_tool_argument_checker_profile", "prompt_injection_surface_scanner_profile"),
    ("continuous_output_completeness_grader_profile", "output_quality_scorer_profile"),
    ("continuous_response_action_planner_profile", "output_quality_scorer_profile"),
    ("continuous_assumption_risk_mapper_profile", "requirement_gap_analyzer_profile"),
    ("continuous_verification_checklist_builder_profile", "prompt_test_case_generator_profile"),
    ("continuous_rollback_guard_builder_profile", "automation_safety_gate_profile"),
    ("continuous_anomaly_watch_builder_profile", "autonomous_run_governor_profile"),
    ("continuous_release_evidence_summarizer_profile", "artifact_release_note_generator_profile"),
    ("continuous_trace_failure_router_profile", "workflow_debugger_profile"),
    ("continuous_retrieval_query_planner_profile", "retrieval_query_expander_profile"),
    ("continuous_citation_priority_scorer_profile", "hallucination_risk_auditor_profile"),
    ("continuous_model_fit_triage_profile", "model_selection_scorecard_profile"),
    ("continuous_instruction_hierarchy_checker_profile", "instruction_conflict_detector_profile"),
    ("continuous_data_contract_validator_profile", "data_contract_mapper_profile"),
)


def _required_detail_keys_for_profile(profile_id: str) -> list[str]:
    normalized = _normalized_gate_profile_id(profile_id) or str(profile_id or "")
    required = _PROFILE_REQUIRED_DETAIL_KEYS.get(normalized)
    if required is None:
        for continuous_profile, base_profile in _PROFILE_REQUIRED_DETAIL_FALLBACKS:
            if normalized == continuous_profile:
                required = _PROFILE_REQUIRED_DETAIL_KEYS.get(base_profile, set())
                break
    return sorted(required or set())


def _generic_probe_payload(spec: PluginSpec) -> Dict[str, Any]:
    return {
        "task": getattr(spec, "goal", "") or getattr(spec, "name", ""),
        "objective": getattr(spec, "goal", "") or "Validate this AI capability.",
        "prompt": "Plan, verify, and safely improve this AI capability without inventing facts.",
        "instruction": "Return machine-readable findings and concrete next actions.",
        "query": "capability validation evidence",
        "question": "What should be checked before promoting this capability?",
        "response": "Draft response with missing evidence, unclear assumptions, and unverified claims.",
        "answer": "Candidate answer requiring quality review.",
        "messages": [
            {"role": "user", "content": "Check whether this AI capability is ready."},
            {"role": "assistant", "content": "Drafted a plan with assumptions and gaps."},
        ],
        "source_notes": [
            "Source A supports the implementation boundary.",
            "Source B conflicts with one unstated assumption.",
        ],
        "candidate_outputs": [
            {"summary": "Candidate A omits verification evidence."},
            {"summary": "Candidate B includes citations and caveats."},
        ],
        "current_plan": ["inspect inputs", "build logic", "validate semantics"],
        "completed_steps": ["created draft capability shell"],
        "blocked_steps": ["need promotion evidence"],
        "constraints": ["preserve Station C envelope", "reject shallow behavior"],
        "agents": [{"name": "builder", "role": "implementation"}, {"name": "reviewer", "role": "validation"}],
        "workstreams": ["implementation", "semantic validation"],
        "ownership_scopes": ["plugin source", "validation evidence"],
        "context_items": [
            {"text": "Keep this constraint because it affects safety.", "importance": "high"},
            {"text": "Ignore this unrelated noisy status note.", "importance": "low"},
        ],
        "existing_plugins": [
            {"name": "Existing Capability", "slug": "existing_capability", "owns": ["baseline comparison"]},
        ],
    }


def _build_generic_capability_spec(spec: PluginSpec, profile_id: str) -> Any:
    if CapabilitySpec is None:
        return None
    profile_required = _required_detail_keys_for_profile(profile_id)
    return CapabilitySpec(
        name=str(getattr(spec, "name", "") or getattr(spec, "slug", "")),
        slug=str(getattr(spec, "slug", "")),
        family_key=str((getattr(spec, "extra", {}) or {}).get("family_key") or getattr(spec, "slug", "")),
        purpose=str(getattr(spec, "goal", "") or getattr(spec, "name", "")),
        owns=list(getattr(spec, "use_cases", []) or []),
        does_not_own=["metadata-only relabeling", "generic fallback behavior", "hidden external side effects"],
        required_inputs=["user-provided payload values"],
        optional_inputs=[
            "task",
            "objective",
            "prompt",
            "instruction",
            "query",
            "question",
            "response",
            "messages",
            "source_notes",
            "candidate_outputs",
            "current_plan",
            "completed_steps",
            "blocked_steps",
            "agents",
            "workstreams",
            "ownership_scopes",
        ],
        required_detail_keys=list(_GENERIC_REQUIRED_DETAIL_KEYS),
        required_scores=["confidence", "usefulness"],
        forbidden_detail_keys=[],
        logic_profile_ids=[profile_id],
        semantic_probe_ids=[
            "generic_empty_payload_missing_input_test",
            "generic_non_dict_payload_warning_test",
            "generic_useful_payload_profile_contract_test",
        ],
    )


def _build_generic_logic_profile(profile_id: str) -> Any:
    if LogicProfile is None:
        return None
    return LogicProfile(
        profile_id=profile_id,
        aliases=[],
        purpose="Generic generated AI capability profile contract.",
        required_behavior=(
            "Use actual payload values, report profile-specific details, preserve payload warnings, "
            "and expose diagnostics proving the plugin did not treat its own goal as user input."
        ),
        forbidden_behavior=[
            "metadata-only relabeling",
            "empty payload treated as complete",
            "dropping non-dict payload warnings",
            "generic fallback output",
        ],
        required_detail_keys=list(_GENERIC_REQUIRED_DETAIL_KEYS),
        required_scores=["confidence", "usefulness"],
        allowed_result_modes=[],
    )


def _build_generic_semantic_contract(spec: PluginSpec, cap_spec: Any, profile_id: str) -> Any:
    if SemanticContract is None or SemanticProbe is None:
        return None
    profile_required = _required_detail_keys_for_profile(profile_id)
    return SemanticContract(
        spec_slug=cap_spec.slug,
        probes=[
            SemanticProbe(
                probe_id="generic_empty_payload_missing_input_test",
                name="Generic empty payload missing-input test",
                payload={},
                required_detail_keys=["missing_inputs", "payload_warnings", "has_user_input", "used_goal_fallback"],
            ),
            SemanticProbe(
                probe_id="generic_non_dict_payload_warning_test",
                name="Generic non-dict payload warning test",
                payload="make this capability better",
                required_detail_keys=["missing_inputs", "payload_warnings", "has_user_input", "used_goal_fallback"],
            ),
            SemanticProbe(
                probe_id="generic_useful_payload_profile_contract_test",
                name="Generic useful payload profile contract test",
                payload=_generic_probe_payload(spec),
                expected_min_scores={"confidence": 0.2, "usefulness": 0.2},
                required_detail_keys=profile_required,
            ),
        ],
        structural_requirements={
            "required_top_level_keys": [
                "summary",
                "primary_insights",
                "recommended_actions",
                "scores",
                "details",
                "progress_state",
                "user_experience",
            ]
        },
        semantic_requirements={
            "forbid_metadata_only_relabeling": True,
            "require_payload_warning_preservation": True,
            "require_profile_specific_details": True,
        },
    )


def _result_detail_keys(output: Dict[str, Any]) -> Set[str]:
    details = output.get("details")
    if not isinstance(details, dict):
        return set()
    return {str(key) for key in details.keys()}


async def _capability_identity_gate(plugin_path: Path, spec: PluginSpec) -> Tuple[bool, str]:
    """
    Prove that the generated behavior matches the capability name/profile.

    Production score measures richness. This gate makes sure the name is not a
    metadata-only relabel of another profile: the advertised capability must
    expose its own machine-readable detail keys and route through the expected
    profile id.
    """
    module = _module_from_plugin_path(plugin_path, slug=spec.slug, purpose="capability_identity")
    output = await _invoke_plugin_for_semantic_check(
        module,
        PRODUCTION_QUALITY_PROBE_PAYLOAD,
        f"{spec.slug}-identity",
    )
    details = output.get("details") if isinstance(output.get("details"), dict) else {}
    diagnostics = output.get("diagnostics") if isinstance(output.get("diagnostics"), dict) else {}

    expected_profile = _registered_profile_id(spec.slug) if callable(_registered_profile_id) else None
    actual_profile = details.get("logic_profile_id") or diagnostics.get("logic_profile_id")
    if expected_profile:
        expected_norm = _normalized_gate_profile_id(expected_profile)
        actual_norm = _normalized_gate_profile_id(actual_profile)
        if actual_norm and actual_norm != expected_norm:
            return (
                False,
                "capability_identity: logic profile mismatch "
                f"(expected={expected_norm}, actual={actual_norm})",
            )
        if not actual_norm:
            return False, f"capability_identity: missing logic_profile_id for expected profile {expected_norm}"

    marker = _capability_name_marker(str(getattr(spec, "slug", "") or ""))
    if not marker:
        return True, "capability_identity: no specialized name contract"

    contract = dict(next(item[1] for item in _CAPABILITY_NAME_CONTRACTS if item[0] == marker))
    detail_keys = _result_detail_keys(output)
    required = set(contract.get("required_detail_keys") or set())
    forbidden = set(contract.get("forbidden_detail_keys") or set())
    missing = sorted(required - detail_keys)
    present_forbidden = sorted(forbidden & detail_keys)
    if missing:
        return (
            False,
            f"capability_identity: {marker} missing required detail keys {missing}; "
            f"present={sorted(detail_keys)}",
        )
    if present_forbidden:
        return (
            False,
            f"capability_identity: {marker} contains sibling-only detail keys {present_forbidden}",
        )

    return (
        True,
        f"capability_identity: {marker} matched profile {expected_profile or actual_profile} "
        f"with detail keys {sorted(required)}",
    )


def _sibling_candidate_paths(spec: PluginSpec, *, max_paths: int = 24) -> list[Path]:
    slug = str(getattr(spec, "slug", "") or "")
    scenario_key = _continuous_scenario_key(slug)
    if scenario_key:
        siblings = [
            path
            for path in sorted(PLUGINS_DIR.glob("*.py"))
            if path.stem != slug and _continuous_scenario_key(path.stem) == scenario_key
        ]
        return siblings[-max_paths:]

    prefix = _capability_family_prefix(slug)
    if not prefix or prefix == slug:
        return []
    siblings = [
        path
        for path in sorted(PLUGINS_DIR.glob("*.py"))
        if path.stem != slug and _capability_family_prefix(path.stem) == prefix
    ]
    return siblings[-max_paths:]


def _sibling_comparison_surface(output: Dict[str, Any]) -> str:
    details = output.get("details") if isinstance(output.get("details"), dict) else {}
    surface = {
        "summary": output.get("summary"),
        "primary_insights": output.get("primary_insights"),
        "recommended_actions": output.get("recommended_actions"),
        "scores": output.get("scores"),
        "progress_state": output.get("progress_state"),
        "detail_keys": sorted(str(key) for key in details.keys()),
        "details": details,
    }
    return _jsonish_text(surface, max_chars=16000)


async def _sibling_uniqueness_gate(
    plugin_path: Path,
    spec: PluginSpec,
    *,
    sibling_paths: Optional[Sequence[Path]] = None,
) -> Tuple[bool, str]:
    """
    Prevent a new same-family plugin from being accepted when its behavior is
    effectively the same as an already-retained sibling.
    """
    paths = list(sibling_paths) if sibling_paths is not None else _sibling_candidate_paths(spec)
    if not paths:
        return True, "sibling_uniqueness: no same-family siblings to compare"

    candidate_module = _module_from_plugin_path(plugin_path, slug=spec.slug, purpose="sibling_candidate")
    candidate_output = await _invoke_plugin_for_semantic_check(
        candidate_module,
        PRODUCTION_QUALITY_PROBE_PAYLOAD,
        f"{spec.slug}-sibling-candidate",
    )
    candidate_words = _word_set(_sibling_comparison_surface(candidate_output))
    candidate_keys = _result_detail_keys(candidate_output)
    strongest: tuple[float, float, str] = (0.0, 0.0, "")

    for sibling_path in paths:
        try:
            sibling_module = _module_from_plugin_path(
                sibling_path,
                slug=sibling_path.stem,
                purpose="sibling_existing",
            )
            sibling_output = await _invoke_plugin_for_semantic_check(
                sibling_module,
                PRODUCTION_QUALITY_PROBE_PAYLOAD,
                f"{spec.slug}-sibling-existing-{sibling_path.stem}",
            )
        except Exception:
            LOG.debug("Skipping sibling comparison for %s", sibling_path, exc_info=True)
            continue
        sibling_words = _word_set(_sibling_comparison_surface(sibling_output))
        union = candidate_words | sibling_words
        similarity = (len(candidate_words & sibling_words) / len(union)) if union else 1.0
        sibling_keys = _result_detail_keys(sibling_output)
        key_union = candidate_keys | sibling_keys
        key_similarity = (len(candidate_keys & sibling_keys) / len(key_union)) if key_union else 1.0
        if similarity > strongest[0]:
            strongest = (similarity, key_similarity, sibling_path.stem)
        if similarity >= 0.95 and key_similarity >= 0.72:
            return (
                False,
                "sibling_uniqueness: candidate behavior is too close to retained sibling "
                f"{sibling_path.stem} (similarity={similarity:.2f}, detail_key_similarity={key_similarity:.2f})",
            )

    return (
        True,
        "sibling_uniqueness: closest sibling "
        f"{strongest[2] or 'none'} similarity={strongest[0]:.2f}, detail_key_similarity={strongest[1]:.2f}",
    )


async def _capability_name_and_uniqueness_gate(plugin_path: Path, spec: PluginSpec) -> Tuple[bool, str]:
    identity_ok, identity_reason = await _capability_identity_gate(plugin_path, spec)
    if not identity_ok:
        return False, identity_reason
    sibling_ok, sibling_reason = await _sibling_uniqueness_gate(plugin_path, spec)
    if not sibling_ok:
        return False, sibling_reason
    return True, f"{identity_reason}; {sibling_reason}"


async def _capability_promotion_gate(
    plugin_path: Path,
    spec: PluginSpec,
) -> Tuple[bool, str]:
    if not (
        callable(_get_logic_profile)
        and callable(_run_semantic_contract_async)
        and callable(_evaluate_for_promotion)
    ):
        return True, "capability_promotion: operating layer unavailable"

    profile_id = _registered_profile_id(spec.slug) if callable(_registered_profile_id) else None
    if callable(_normalize_logic_profile_id):
        profile_id = _normalize_logic_profile_id(profile_id or "") or profile_id
    if not profile_id:
        return False, "capability_promotion: missing registered logic profile"

    cap_spec = _get_capability_spec(str(getattr(spec, "slug", "") or "")) if callable(_get_capability_spec) else None
    profile = _get_logic_profile(profile_id or "")
    contract = _get_semantic_contract(cap_spec.slug) if cap_spec is not None and callable(_get_semantic_contract) else None

    using_generic_contract = False
    if cap_spec is None:
        cap_spec = _build_generic_capability_spec(spec, profile_id)
        profile = _build_generic_logic_profile(profile_id)
        contract = _build_generic_semantic_contract(spec, cap_spec, profile_id) if cap_spec is not None else None
        using_generic_contract = True

    if cap_spec is None:
        return False, "capability_promotion: unable to build CapabilitySpec"
    if profile is None or contract is None:
        return False, f"capability_promotion: missing profile or semantic contract for {cap_spec.slug}"

    module = _module_from_plugin_path(plugin_path, slug=spec.slug, purpose="capability_promotion")
    semantic_result = await _run_semantic_contract_async(module.invoke, cap_spec, profile, contract)
    first_payload = contract.probes[0].payload if contract.probes else {}
    first_output = await _invoke_plugin_for_semantic_check(module, first_payload, f"{spec.slug}-promotion")
    decision = _evaluate_for_promotion(first_output, cap_spec, profile, semantic_result)
    if decision.decision == "promote":
        if using_generic_contract:
            return True, "capability_promotion: generated generic CapabilitySpec contract passed and promotion approved"
        return True, "capability_promotion: semantic contract passed and promotion approved"
    finding_text = "; ".join(
        f"{finding.code}: {finding.message}" for finding in semantic_result.findings[:8]
    )
    return False, f"capability_promotion: {decision.decision}: {decision.reason}; {finding_text}"


async def _upgrade_candidate_improves_existing(
    *,
    candidate_path: Path,
    existing_path: Path,
    spec: PluginSpec,
) -> Tuple[bool, str]:
    """
    Decide whether an upgrade candidate earns the right to overwrite the base module.

    Passing normal validation is not enough. The candidate must produce a
    meaningfully stronger output than the currently retained capability.
    """
    if not existing_path.exists():
        return True, "upgrade_gate: no existing base capability; candidate may become canonical"

    candidate_module = _module_from_plugin_path(candidate_path, slug=spec.slug, purpose="upgrade_candidate")
    existing_module = _module_from_plugin_path(existing_path, slug=spec.slug, purpose="upgrade_existing")
    probe_payloads = [
        {
            "task": "Validate a generated AI capability before publishing it.",
            "objective": "Reject shallow or duplicate output and keep only a capability-specific improvement.",
            "prompt": "Make this better without just renaming it.",
            "constraints": ["must improve the canonical capability", "discard if not better", "no duplicate module"],
            "candidate_outputs": [
                {"summary": "Generic capability output with stock advice."},
                {"summary": "Specific capability output with measurable validation evidence."},
            ],
            "quality_failures": ["duplicate capability", "shallow recommendation"],
            "current_plan": ["generate candidate", "compare with canonical module", "overwrite only if better"],
            "blocked_steps": ["need proof this candidate improves the retained capability"],
        },
        {
            "task": "Prepare a production-safe AI workflow upgrade.",
            "objective": "Find concrete risks, verification checks, and the next action.",
            "prompt": "Review auth/database risk, citation gaps, and tool-result mismatch before release.",
            "constraints": ["include rollback evidence", "cite uncertainty", "produce non-empty actions"],
            "trace": [{"tool": "retrieval", "status": "partial", "issue": "citation mismatch"}],
            "completed_steps": ["generated candidate module"],
            "blocked_steps": ["prove it is more useful than the current module"],
        },
    ]

    candidate_scores: list[float] = []
    existing_scores: list[float] = []
    candidate_surfaces: list[str] = []
    existing_surfaces: list[str] = []
    for idx, payload in enumerate(probe_payloads, start=1):
        candidate_output = await _invoke_plugin_for_semantic_check(candidate_module, payload, f"{spec.slug}-candidate-{idx}")
        existing_output = await _invoke_plugin_for_semantic_check(existing_module, payload, f"{spec.slug}-existing-{idx}")
        candidate_scores.append(_capability_quality_score(candidate_output))
        existing_scores.append(_capability_quality_score(existing_output))
        candidate_surfaces.append(_jsonish_text(_decision_surface(candidate_output), max_chars=10000))
        existing_surfaces.append(_jsonish_text(_decision_surface(existing_output), max_chars=10000))

    candidate_avg = sum(candidate_scores) / max(1, len(candidate_scores))
    existing_avg = sum(existing_scores) / max(1, len(existing_scores))
    candidate_words = _word_set(" ".join(candidate_surfaces))
    existing_words = _word_set(" ".join(existing_surfaces))
    union = candidate_words | existing_words
    similarity = (len(candidate_words & existing_words) / len(union)) if union else 1.0

    if candidate_avg < existing_avg + 0.05:
        return (
            False,
            f"upgrade_gate: candidate not better than canonical capability "
            f"(candidate={candidate_avg:.3f}, existing={existing_avg:.3f}, similarity={similarity:.2f})",
        )
    if similarity > 0.93 and candidate_avg < existing_avg + 0.10:
        return (
            False,
            f"upgrade_gate: candidate output is too similar to canonical capability "
            f"(candidate={candidate_avg:.3f}, existing={existing_avg:.3f}, similarity={similarity:.2f})",
        )
    return (
        True,
        f"upgrade_gate: candidate improves canonical capability "
        f"(candidate={candidate_avg:.3f}, existing={existing_avg:.3f}, similarity={similarity:.2f})",
    )


def _capability_semantic_contract(
    spec: PluginSpec,
    result_a: Dict[str, Any],
    result_b: Dict[str, Any],
) -> Tuple[bool, str]:
    slug = str(getattr(spec, "slug", "") or "").lower()
    category = str(getattr(spec, "category", "") or "").lower()
    goal = str(getattr(spec, "goal", "") or "").lower()
    if "prompt_refinement" in slug:
        return _prompt_refinement_contract(result_a, result_b)
    if slug == "ai_multi_agent_handoff_planner":
        return _multi_agent_handoff_contract(result_a, result_b)
    return True, "capability_semantic_contract: no specialized contract"


def _multi_agent_handoff_contract(result_a: Dict[str, Any], result_b: Dict[str, Any]) -> Tuple[bool, str]:
    def _details(result: Dict[str, Any]) -> Dict[str, Any]:
        details = result.get("details")
        return details if isinstance(details, dict) else {}

    failures = []
    for label, result in [("a", result_a), ("b", result_b)]:
        details = _details(result)
        boundaries = details.get("ownership_boundaries")
        handoff_inputs = details.get("handoff_inputs")
        decision = details.get("handoff_overlap_decision")
        if not isinstance(boundaries, list) or not boundaries:
            failures.append(f"{label}: missing payload-derived ownership_boundaries")
        if not isinstance(handoff_inputs, dict):
            failures.append(f"{label}: missing handoff_inputs")
        if decision == "repair_or_merge":
            failures.append(f"{label}: handoff profile marked repair_or_merge")
        boundary_text = _jsonish_text(boundaries, max_chars=8000)
        if not any(token in boundary_text.lower() for token in ["builder", "reviewer", "researcher", "citation", "database"]):
            failures.append(f"{label}: ownership_boundaries do not reflect supplied agents/workstreams")
    if failures:
        return False, "multi_agent_handoff_contract: " + "; ".join(failures[:8])
    return True, "multi_agent_handoff_contract: payload-derived ownership boundaries present"


def _prompt_refinement_contract(result_a: Dict[str, Any], result_b: Dict[str, Any]) -> Tuple[bool, str]:
    def _details(result: Dict[str, Any]) -> Dict[str, Any]:
        details = result.get("details")
        return details if isinstance(details, dict) else {}

    def _actions_text(result: Dict[str, Any]) -> str:
        return _jsonish_text(result.get("recommended_actions", []), max_chars=5000)

    failures = []
    for label, result in [("a", result_a), ("b", result_b)]:
        details = _details(result)
        vagueness = details.get("identified_vagueness")
        missing = details.get("missing_constraints")
        rewrites = details.get("rewrites")
        refined = details.get("refined_prompt")
        actions = _actions_text(result)

        if not isinstance(vagueness, list):
            failures.append(f"{label}: missing details.identified_vagueness list")
        if not isinstance(missing, list):
            failures.append(f"{label}: missing details.missing_constraints list")
        if not isinstance(rewrites, list) or not rewrites:
            failures.append(f"{label}: missing details.rewrites list")
        if not isinstance(refined, str) or len(refined.strip()) < 40:
            failures.append(f"{label}: missing substantial details.refined_prompt")
        if "rewrite" not in actions and "refined" not in actions:
            failures.append(f"{label}: recommended_actions do not include a rewrite/refinement")
        contract_text = _jsonish_text(
            {
                "details": details,
                "actions": result.get("recommended_actions"),
                "summary": result.get("summary"),
            },
            max_chars=10000,
        )
        for required in ["audience", "format", "constraint", "verification"]:
            if required not in contract_text:
                failures.append(f"{label}: prompt contract missing {required}")

    refined_a = str(_details(result_a).get("refined_prompt", ""))
    refined_b = str(_details(result_b).get("refined_prompt", ""))
    if refined_a and refined_b and refined_a == refined_b:
        failures.append("refined prompts are identical across different payloads")

    if failures:
        return False, "prompt_refinement_contract: " + "; ".join(failures[:8])
    return True, "prompt_refinement_contract: rewrites and missing constraints present"


def _quarantine_rejected_plugin(plugin_path: Path, *, reason: str) -> Path:
    quarantine_dir = ROOT_DIR / "junk_plugins" / "semantic_rejections"
    quarantine_dir.mkdir(parents=True, exist_ok=True)
    target = quarantine_dir / plugin_path.name
    if target.exists():
        target = quarantine_dir / f"{plugin_path.stem}_{os.getpid()}{plugin_path.suffix}"
    plugin_path.replace(target)
    reason_path = target.with_suffix(target.suffix + ".reason.txt")
    reason_path.write_text(reason, encoding="utf-8")
    return target


def _git_run(args: Sequence[str], *, timeout_seconds: int = 180) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", "-C", str(FACTORY_DIR), *args],
        text=True,
        capture_output=True,
        timeout=timeout_seconds,
        check=False,
    )


def _publish_plugin_to_github(
    *,
    plugin_path: Path,
    spec: PluginSpec,
    config: RunnerConfig,
) -> bool:
    """
    Commit the generated plugin artifact and push it to GitHub.

    The commit is intentionally limited to the plugin file so runtime state,
    lock files, and unrelated local edits never get swept into autonomous
    publishes.
    """
    if not config.github_publish_enabled:
        LOG.info("GitHub publish disabled; leaving %s local only.", plugin_path)
        return True

    if not (FACTORY_DIR / ".git").exists():
        LOG.error("GitHub publish requested, but %s is not a Git repository.", FACTORY_DIR)
        return False

    try:
        relative_path = plugin_path.resolve().relative_to(FACTORY_DIR.resolve())
    except ValueError:
        LOG.error("Refusing to publish plugin outside factory repo: %s", plugin_path)
        return False

    rel = relative_path.as_posix()

    try:
        status = _git_run(["status", "--porcelain", "--", rel])
    except Exception as exc:
        LOG.error("Git status failed before publishing %r: %s", spec.slug, exc)
        return False

    if status.returncode != 0:
        LOG.error(
            "Git status failed before publishing %r: %s",
            spec.slug,
            (status.stderr or status.stdout).strip(),
        )
        return False

    if status.stdout.strip():
        add_result = _git_run(["add", "--", rel])
        if add_result.returncode != 0:
            LOG.error(
                "Git add failed for plugin %r: %s",
                spec.slug,
                (add_result.stderr or add_result.stdout).strip(),
            )
            return False

        diff_result = _git_run(["diff", "--cached", "--quiet", "--", rel])
        if diff_result.returncode == 1:
            commit_result = _git_run(
                [
                    "commit",
                    "-m",
                    f"Publish generated capability {spec.slug}",
                    "--",
                    rel,
                ]
            )
            if commit_result.returncode != 0:
                LOG.error(
                    "Git commit failed for plugin %r: %s",
                    spec.slug,
                    (commit_result.stderr or commit_result.stdout).strip(),
                )
                return False
            LOG.info(
                "Committed generated plugin %r to %s.",
                spec.slug,
                rel,
            )
        elif diff_result.returncode == 0:
            LOG.info("Generated plugin %r has no staged file changes.", spec.slug)
        else:
            LOG.error(
                "Git diff check failed for plugin %r: %s",
                spec.slug,
                (diff_result.stderr or diff_result.stdout).strip(),
            )
            return False
    else:
        LOG.info(
            "Generated plugin %r already matches Git working tree; pushing any pending commits.",
            spec.slug,
        )

    push_result = _git_run(
        ["push", config.github_remote, config.github_branch],
        timeout_seconds=300,
    )
    if push_result.returncode != 0:
        LOG.error(
            "GitHub push failed for plugin %r to %s/%s: %s",
            spec.slug,
            config.github_remote,
            config.github_branch,
            (push_result.stderr or push_result.stdout).strip(),
        )
        return False

    LOG.info(
        "GitHub updated for generated plugin %r via %s/%s.",
        spec.slug,
        config.github_remote,
        config.github_branch,
    )
    return True


def _build_semantic_repair_source(
    *,
    source: str,
    spec: PluginSpec,
    capability_type: Optional[str],
    logic_profile_id: Optional[str],
    reason: str,
) -> Optional[str]:
    """
    Build a deterministic semantic repair for shallow AI-roadmap outputs.

    This uses Station B's same envelope helpers when the full Francis runtime is
    present. Standalone checkouts without those internals simply skip repair.
    """
    if callable(_build_profile_source):
        profile_source = _build_profile_source(
            source,
            spec,
            capability_type,
            logic_profile_id,
            reason=reason,
        )
        if profile_source:
            return profile_source

    if not (
        callable(_station_b_deterministic_ai_body)
        and callable(_station_b_wrap_logic_body)
        and callable(_station_b_update_logic_region)
    ):
        return None
    body = _station_b_deterministic_ai_body(
        spec,
        capability_type,
        logic_profile_id,
        reason=reason,
    )
    wrapped = _station_b_wrap_logic_body(body)
    return _station_b_update_logic_region(source, wrapped)


def _render_profile_base_source(spec: PluginSpec) -> str:
    """
    Render the standard plugin shell needed by deterministic profiles.

    Prefer the parent Francis template when available. If the local sidecar
    template is older or incompatible, fall back to a compact shell that exposes
    the same Station C surface: SkillContext, _run_core_logic, and invoke.
    """
    if callable(_render_plugin_source):
        try:
            source = _render_plugin_source(spec)
            if "_run_core_logic" in source and "# === LOGIC START ===" in source:
                return source
        except Exception:
            LOG.debug("Plugin template render failed; using profile base shell.", exc_info=True)

    if hasattr(spec, "to_manifest") and callable(getattr(spec, "to_manifest")):
        manifest = spec.to_manifest()
    else:
        manifest = {
            "name": getattr(spec, "name", ""),
            "slug": getattr(spec, "slug", ""),
            "goal": getattr(spec, "goal", ""),
            "category": getattr(spec, "category", ""),
            "tags": list(getattr(spec, "tags", []) or []),
            "version": str(getattr(spec, "version", "") or "0.1.0"),
            "capability_type": getattr(spec, "capability_type", None),
            "intended_domain": getattr(spec, "intended_domain", None),
            "owner_id": getattr(spec, "owner_id", None),
            "use_cases": list(getattr(spec, "use_cases", []) or []),
        }
    manifest["schema_version"] = "1.0.0"
    try:
        manifest.setdefault("family_key", spec.family_key)
        manifest.setdefault("is_generic_name", spec.is_generic_name())
    except Exception:
        pass

    return f'''from __future__ import annotations

"""
Auto-generated Francis AI capability module.

THIS FILE IS GENERATED. Manual edits may be overwritten by the factory.

Capability: {spec.name}
Slug: {spec.slug}
"""

from typing import Any, Dict, Optional

__all__ = ["invoke", "_run_core_logic", "SkillContext"]

_PLUGIN_NAME: str = {spec.name!r}
_PLUGIN_SLUG: str = {spec.slug!r}
_PLUGIN_CATEGORY: str = {spec.category!r}
_PLUGIN_VERSION: str = {str(spec.version or "0.1.0")!r}
_PLUGIN_GOAL: str = {spec.goal!r}
_PLUGIN_TAGS = {list(spec.tags)!r}
_PLUGIN_OWNER_ID = {spec.owner_id!r}
_PLUGIN_CAPABILITY_TYPE = {getattr(spec, "capability_type", None)!r}
_PLUGIN_INTENDED_DOMAIN = {getattr(spec, "intended_domain", None)!r}
_PLUGIN_USE_CASES = {list(getattr(spec, "use_cases", []) or [])!r}
_PLUGIN_RESULT_SCHEMA_VERSION: str = "1.0.0"
_PLUGIN_MANIFEST = {manifest!r}
_PLUGIN_DEFAULT_CONFIG: Dict[str, Any] = {{}}

try:
    from learning_manager import load_plugin_profile as _load_plugin_profile  # type: ignore
except (ImportError, ModuleNotFoundError):
    _load_plugin_profile = None  # type: ignore[assignment]


class SkillContext:
    def __init__(
        self,
        *,
        user_id: str,
        run_id: Optional[str],
        plugin_slug: str,
        plugin_name: str,
        learning_profile: Optional[Dict[str, Any]] = None,
        logger: Optional[Any] = None,
        brain: Optional[Any] = None,
    ) -> None:
        self.user_id = user_id
        self.run_id = run_id
        self.plugin_slug = plugin_slug
        self.plugin_name = plugin_name
        self.learning_profile: Dict[str, Any] = learning_profile or {{}}
        self.logger = logger
        self.brain = brain

    def _log(self, level: str, message: str, **fields: Any) -> None:
        if self.logger is None:
            return
        try:
            log_fn = getattr(self.logger, level, None)
            if callable(log_fn):
                payload = {{"message": message, "plugin_slug": self.plugin_slug, "plugin_name": self.plugin_name}}
                payload.update(fields)
                log_fn(payload)
        except Exception:
            return

    def log_info(self, message: str, **fields: Any) -> None:
        self._log("info", message, **fields)

    def log_error(self, message: str, **fields: Any) -> None:
        self._log("error", message, **fields)


def _build_effective_config(payload: Dict[str, Any], runtime_config: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    cfg: Dict[str, Any] = dict(_PLUGIN_DEFAULT_CONFIG)
    if isinstance(payload.get("customer_config"), dict):
        cfg.update(payload["customer_config"])
    if isinstance(payload.get("config"), dict):
        cfg.update(payload["config"])
    if isinstance(runtime_config, dict):
        cfg.update(runtime_config)
    return cfg


def _load_learning_profile() -> Dict[str, Any]:
    if _load_plugin_profile is None:
        return {{}}
    try:
        prof = _load_plugin_profile(_PLUGIN_SLUG)
        return prof if isinstance(prof, dict) else {{}}
    except Exception:
        return {{}}


def _run_core_logic(context: SkillContext, payload: Dict[str, Any], config: Dict[str, Any]) -> Dict[str, Any]:
    # === LOGIC START ===
    return {{"summary": "Profile logic was not injected.", "primary_insights": [], "recommended_actions": [], "scores": {{"confidence": 0.0}}, "details": {{}}}}
    # === LOGIC END ===


async def invoke(
    user_id: str,
    payload: Dict[str, Any],
    *,
    run_id: Optional[str] = None,
    brain: Optional[Any] = None,
    logger: Optional[Any] = None,
    config: Optional[Dict[str, Any]] = None,
    **kwargs: Any,
) -> Dict[str, Any]:
    if not isinstance(payload, dict):
        payload = {{
            "_value": payload,
            "_payload_warnings": ["payload was not a dict; invoke wrapped it in _value"],
        }}
    context = SkillContext(
        user_id=user_id,
        run_id=run_id,
        plugin_slug=_PLUGIN_SLUG,
        plugin_name=_PLUGIN_NAME,
        learning_profile=_load_learning_profile(),
        logger=logger,
        brain=brain,
    )
    status = "failed"
    error_msg = ""
    core_output: Optional[Dict[str, Any]] = None
    try:
        core_output = _run_core_logic(context, payload, _build_effective_config(payload, config))
        if not isinstance(core_output, dict):
            raise TypeError("_run_core_logic must return a dict")
        status = "succeeded"
    except Exception as exc:
        context.log_error("Core logic raised an exception.", error=str(exc), exception_type=type(exc).__name__)
        error_msg = str(exc)
    meta = {{
        "plugin_name": _PLUGIN_NAME,
        "plugin_slug": _PLUGIN_SLUG,
        "plugin_category": _PLUGIN_CATEGORY,
        "plugin_version": _PLUGIN_VERSION,
        "user_id": user_id,
        "run_id": run_id,
        "owner_id": _PLUGIN_OWNER_ID,
        "capability_type": _PLUGIN_CAPABILITY_TYPE,
        "intended_domain": _PLUGIN_INTENDED_DOMAIN,
        "schema_version": _PLUGIN_RESULT_SCHEMA_VERSION,
        "plugin_manifest": _PLUGIN_MANIFEST,
    }}
    return {{"status": status, "output": core_output if status == "succeeded" else None, "error": error_msg, "meta": meta}}
'''


@dataclass
class _ProfileStationBResult:
    source: str
    raw_llm_output: str = ""
    capability_type: Optional[str] = None
    system_prompt: str = "DETERMINISTIC_PROFILE_BYPASS"
    user_prompt: str = "Registered AI roadmap profile generated without LLM code generation."
    logic_profile_id: Optional[str] = None
    profile_selection_raw: Optional[str] = "REGISTERED_PROFILE"
    logic_blueprint: Optional[Dict[str, Any]] = field(default_factory=dict)


def _build_registered_profile_result(
    *,
    spec: PluginSpec,
    capability_type: Optional[str],
    reason: str,
) -> Optional[_ProfileStationBResult]:
    """
    Build registered AI-roadmap profile plugins without calling Station B/Ollama.

    For these capabilities the profile registry is the source of truth. Calling
    the LLM first only adds latency and can produce code that is immediately
    overwritten by the deterministic profile.
    """
    if not (
        _is_ai_roadmap_spec(spec)
        and callable(_registered_profile_id)
        and callable(_build_profile_source)
        and callable(_render_plugin_source)
    ):
        return None

    profile_id = _registered_profile_id(spec.slug)
    if not profile_id:
        return None

    base_source = _render_profile_base_source(spec)
    source = _build_profile_source(
        base_source,
        spec,
        capability_type,
        profile_id,
        reason=reason,
    )
    if not source:
        return None

    return _ProfileStationBResult(
        source=source,
        raw_llm_output="REGISTERED_PROFILE_BYPASS",
        capability_type=capability_type,
        logic_profile_id=profile_id,
        logic_blueprint={
            "profile_id": profile_id,
            "generation_mode": "registered_profile_bypass",
            "reason": reason,
        },
    )


async def _maybe_evaluate_plugin(
    *,
    plugin_path: Path,
    spec: PluginSpec,
    capability_type: Optional[str],
    intended_domain: Optional[str],
    config: RunnerConfig,
) -> Optional[Dict[str, Any]]:
    """
    Optional Station D evaluation / critic stage.

    Behavior:
    - Imports the plugin module from plugin_path.
    - Calls station_d.evaluate_plugin_candidate(...) if available.
    - Logs + records Station E telemetry.
    - Returns evaluation_result dict or None if not evaluated.

    This is deliberately conservative: it NEVER raises.
    """
    if not config.evaluation_enabled:
        return None

    try:
        import importlib.util

        module_name = spec.slug.replace("-", "_")
        module_spec = importlib.util.spec_from_file_location(module_name, plugin_path)
        if module_spec is None or module_spec.loader is None:
            LOG.warning(
                "Could not build module spec for evaluation of plugin %r; skipping evaluation.",
                spec.slug,
            )
            return None

        module = importlib.util.module_from_spec(module_spec)
        module_spec.loader.exec_module(module)  # type: ignore[call-arg]

        eval_result = await evaluate_plugin_candidate(
            plugin_module=module,
            spec=spec,
            capability_type=capability_type,
            intended_domain=intended_domain,
            user_id=config.user_id,
            profile=config.evaluation_profile,
        )

        if not isinstance(eval_result, dict):
            LOG.info("Station D evaluation returned non-dict for %r → %r", spec.slug, eval_result)
            return None

        score = eval_result.get("score")
        crash_rate = eval_result.get("crash_rate")
        insight_score = eval_result.get("insight_score")
        payload_count = eval_result.get("payload_count")

        LOG.info(
            "Station D evaluation for %r → score=%r crash_rate=%r insight_score=%r payloads=%r",
            spec.slug,
            score,
            crash_rate,
            insight_score,
            payload_count,
        )

        _se_record(
            EVENT_FACTORY_PLUGIN_EVALUATED,
            slug=spec.slug,
            category=getattr(spec, "category", None),
            capability_type=capability_type,
            domain=intended_domain,
            score=score,
            crash_rate=crash_rate,
            insight_score=insight_score,
            payload_count=payload_count,
        )

        # Simple threshold handling (log-only by default)
        if isinstance(score, (int, float)):
            if score < config.evaluation_threshold:
                LOG.warning(
                    "Evaluation score %.3f < threshold %.3f for plugin %s.",
                    score,
                    config.evaluation_threshold,
                    spec.slug,
                )
                _se_record(
                    EVENT_FACTORY_PLUGIN_LOW_SCORE,
                    slug=spec.slug,
                    score=score,
                    threshold=config.evaluation_threshold,
                )
            else:
                LOG.info(
                    "Evaluation score %.3f >= threshold %.3f for plugin %s.",
                    score,
                    config.evaluation_threshold,
                    spec.slug,
                )
                _se_record(
                    EVENT_FACTORY_PLUGIN_PASSING_SCORE,
                    slug=spec.slug,
                    score=score,
                    threshold=config.evaluation_threshold,
                )

        # Learning manager hook (if present)
        manager = _LEARNING
        if manager is not None:
            try:
                if hasattr(manager, "record_factory_evaluation"):
                    manager.record_factory_evaluation(
                        slug=spec.slug,
                        category=getattr(spec, "category", None),
                        capability_type=capability_type,
                        domain=intended_domain,
                        eval_result=eval_result,
                    )
            except Exception:
                LOG.debug("Learning manager record_factory_evaluation failed", exc_info=True)

        return eval_result

    except Exception as exc:  # pragma: no cover - defensive
        LOG.warning(
            "Station D evaluation failed for plugin %r (non-fatal): %s",
            spec.slug,
            exc,
        )
        _se_record(
            EVENT_FACTORY_PLUGIN_EVAL_ERROR,
            slug=spec.slug,
            error=str(exc),
        )
        return None


# =====================================================================
# Core Runner
# =====================================================================

async def run_factory(config: RunnerConfig) -> None:
    LOG.info("Starting Francis factory runner: %s", config)
    _acquire_runner_lock()

    # Telemetry: run started
    try:
        _se_record(
            EVENT_FACTORY_RUN_STARTED,
            config=asdict(config),
        )
        manager = _LEARNING
        if manager is not None and hasattr(manager, "record_factory_start"):
            manager.record_factory_start(config=config)
    except Exception:
        LOG.debug("Factory start telemetry failed", exc_info=True)

    _ensure_plugins_dir()
    existing_slugs = _load_existing_plugin_slugs()
    existing_signatures = _load_existing_capability_signatures()
    ai_roadmap_state = _load_ai_roadmap_state()
    ai_roadmap_state = _prune_ai_roadmap_state_to_existing_plugins(ai_roadmap_state, existing_slugs)
    ai_roadmap_state = _seed_ai_roadmap_state_from_existing(ai_roadmap_state, existing_slugs)
    _save_ai_roadmap_state(ai_roadmap_state)
    remembered_rejected_slugs = _remembered_rejected_capability_slugs(ai_roadmap_state)
    LOG.info("Loaded %d existing plugin(s) from plugins/", len(existing_slugs))
    if remembered_rejected_slugs:
        LOG.info(
            "Loaded %d remembered rejected capability slot(s) under current factory knowledge.",
            len(remembered_rejected_slugs),
        )
    LOG.info(
        "Loaded AI roadmap handoff state with %d completed item(s).",
        len(ai_roadmap_state.get("completed") or []),
    )

    built_count = 0
    category_counts: Dict[str, int] = {}

    target_count = config.max_plugins
    if target_count is None and not config.loop_forever:
        target_count = 1

    index_counter = _next_ai_roadmap_index(existing_slugs, remembered_rejected_slugs)
    LOG.info("Starting AI roadmap at deterministic index %d", index_counter)
    anticipated = _refresh_anticipation_state(
        ai_roadmap_state,
        existing_slugs | remembered_rejected_slugs,
        start_index=index_counter,
    )
    if anticipated:
        LOG.info(
            "Anticipated next capability candidates: %s",
            ", ".join(str(item.get("slug", "")) for item in anticipated[:6]),
        )

    # Track whether a custom focus prompt is currently active.
    last_focus_active: Optional[bool] = None

    while True:
        if target_count is not None and built_count >= target_count:
            LOG.info("Reached max_plugins=%s → stopping", target_count)
            break

        # -----------------------------------------------------
        # CUSTOM FOCUS STATE LOGGING (non-intrusive)
        # -----------------------------------------------------
        focus_hint = get_custom_focus_instructions()
        focus_active = bool(focus_hint)
        if focus_active != last_focus_active:
            if focus_active:
                LOG.info(
                    "Custom focus is now ACTIVE "
                    "(custom_prompt.txt is non-empty; plugins will be biased toward your focus)."
                )
            else:
                LOG.info(
                    "Custom focus is now INACTIVE "
                    "(custom_prompt.txt is empty or missing; plugins generated in fully autonomous mode)."
                )
            last_focus_active = focus_active

        # -----------------------------------------------------
        # BUILD NEXT AI ROADMAP SPEC
        # -----------------------------------------------------
        spec: Optional[PluginSpec] = None
        source_spec: Optional[PluginSpec] = None
        is_upgrade_attempt = False
        capability_type: Optional[str] = None
        intended_domain: Optional[str] = None
        remembered_rejected_slugs = _remembered_rejected_capability_slugs(ai_roadmap_state)
        anticipated = _refresh_anticipation_state(
            ai_roadmap_state,
            existing_slugs | remembered_rejected_slugs,
            start_index=index_counter,
        )

        randomized_indexes: list[int] = []
        if not config.allow_upgrade_expansion and index_counter > len(AI_CAPABILITY_ROADMAP):
            if config.randomized_expansion:
                next_candidate, _, _ = build_next_spec(index_counter)
                if (getattr(next_candidate, "extra", {}) or {}).get("continuous_expansion"):
                    LOG.info(
                        "AI roadmap base complete at %d curated capability module(s); continuous canonical expansion is active at index %d.",
                        len(AI_CAPABILITY_ROADMAP),
                        index_counter,
                    )
                else:
                    seeded_count = _seed_retained_canonical_upgrade_memory(ai_roadmap_state, existing_slugs)
                    if seeded_count:
                        LOG.info(
                            "Recorded %d existing registered-profile capability module(s) as retained under the current factory knowledge.",
                            seeded_count,
                        )
                    if _upgrade_backlog_exhausted(ai_roadmap_state, existing_slugs):
                        LOG.info(
                            "All canonical capabilities already have upgrade attempts under the current factory knowledge; idling until factory/profile logic changes."
                        )
                        if config.loop_forever:
                            await asyncio.sleep(config.sleep_seconds)
                            existing_slugs = _load_existing_plugin_slugs()
                            existing_signatures = _load_existing_capability_signatures()
                            ai_roadmap_state = _load_ai_roadmap_state()
                            remembered_rejected_slugs = _remembered_rejected_capability_slugs(ai_roadmap_state)
                            index_counter = _next_ai_roadmap_index(existing_slugs, remembered_rejected_slugs)
                            continue
                        break
                    randomized_indexes = _randomized_ai_expansion_indexes(existing_slugs, remembered_rejected_slugs)
                    LOG.info(
                        "AI roadmap base complete at %d unique plugin(s); randomized bounded expansion has %d candidate(s).",
                        len(AI_CAPABILITY_ROADMAP),
                        len(randomized_indexes),
                    )
                    if not randomized_indexes:
                        if config.loop_forever:
                            LOG.info(
                                "Factory will stay alive and recheck for new randomized candidates in %.1f seconds.",
                                config.sleep_seconds,
                            )
                            await asyncio.sleep(config.sleep_seconds)
                            existing_slugs = _load_existing_plugin_slugs()
                            existing_signatures = _load_existing_capability_signatures()
                            ai_roadmap_state = _load_ai_roadmap_state()
                            remembered_rejected_slugs = _remembered_rejected_capability_slugs(ai_roadmap_state)
                            index_counter = _next_ai_roadmap_index(existing_slugs, remembered_rejected_slugs)
                            continue
                        break
            else:
                LOG.info(
                    "AI roadmap complete at %d unique capability module(s); upgrade expansion and randomized expansion are disabled.",
                    len(AI_CAPABILITY_ROADMAP),
                )
                if config.loop_forever:
                    LOG.info(
                        "Factory will stay alive and recheck for newly added roadmap specs in %.1f seconds.",
                        config.sleep_seconds,
                    )
                    await asyncio.sleep(config.sleep_seconds)
                    existing_slugs = _load_existing_plugin_slugs()
                    existing_signatures = _load_existing_capability_signatures()
                    ai_roadmap_state = _load_ai_roadmap_state()
                    remembered_rejected_slugs = _remembered_rejected_capability_slugs(ai_roadmap_state)
                    index_counter = _next_ai_roadmap_index(existing_slugs, remembered_rejected_slugs)
                    continue
                break

        candidate_indexes = randomized_indexes or list(
            range(index_counter, index_counter + len(AI_CAPABILITY_ROADMAP) * 3)
        )
        selected_index = index_counter
        for candidate_index in candidate_indexes:
            candidate_spec, candidate_capability, candidate_domain = build_next_spec(candidate_index)
            rejection_reason = _capability_rejection_skip_reason(ai_roadmap_state, candidate_spec)
            if rejection_reason:
                LOG.info(
                    "Skipping remembered rejected capability %r → %s",
                    candidate_spec.slug,
                    rejection_reason,
                )
                if not randomized_indexes:
                    index_counter = candidate_index + 1
                continue
            skip_reason = _upgrade_attempt_skip_reason(ai_roadmap_state, candidate_spec)
            if skip_reason:
                LOG.info(
                    "Skipping remembered upgrade attempt %r → %s",
                    candidate_spec.slug,
                    skip_reason,
                )
                continue
            if (
                not config.allow_upgrade_expansion
                and not randomized_indexes
                and int((getattr(candidate_spec, "extra", {}) or {}).get("generation_round", 1)) > 1
            ):
                LOG.info(
                    "Skipping upgrade expansion spec while disabled: slug=%r round=%r",
                    candidate_spec.slug,
                    (getattr(candidate_spec, "extra", {}) or {}).get("generation_round"),
                )
                break
            if _is_duplicate_spec(
                candidate_spec,
                existing_slugs=existing_slugs,
                existing_signatures=existing_signatures,
            ):
                LOG.info(
                    "Skipping duplicate AI roadmap spec: slug=%r name=%r",
                    candidate_spec.slug,
                    candidate_spec.name,
                )
                existing_slugs.add(candidate_spec.slug)
                if not randomized_indexes:
                    index_counter = candidate_index + 1
                continue

            source_spec = candidate_spec
            spec = _canonical_retention_spec(candidate_spec)
            is_upgrade_attempt = _is_upgrade_attempt_spec(candidate_spec)
            capability_type = candidate_capability
            intended_domain = candidate_domain
            selected_index = candidate_index
            break

        if spec is None or source_spec is None or capability_type is None or intended_domain is None:
            LOG.warning("Unable to find a new or untried AI roadmap candidate.")
            if config.loop_forever:
                LOG.info(
                    "Factory will stay alive and recheck after %.1f seconds.",
                    config.sleep_seconds,
                )
                await asyncio.sleep(config.sleep_seconds)
                existing_slugs = _load_existing_plugin_slugs()
                existing_signatures = _load_existing_capability_signatures()
                ai_roadmap_state = _load_ai_roadmap_state()
                remembered_rejected_slugs = _remembered_rejected_capability_slugs(ai_roadmap_state)
                index_counter = _next_ai_roadmap_index(existing_slugs, remembered_rejected_slugs)
                continue
            break

        spec.owner_id = config.user_id
        spec.capability_type = capability_type
        spec.intended_domain = intended_domain
        source_spec.owner_id = config.user_id
        source_spec.capability_type = capability_type
        source_spec.intended_domain = intended_domain
        _attach_ai_handoff_to_spec(spec, ai_roadmap_state)

        if is_upgrade_attempt:
            LOG.info(
                "Treating upgrade candidate %r as an attempt for canonical capability %r.",
                source_spec.slug,
                spec.slug,
            )

        LOG.info(
            "Proposed PluginSpec: name=%r slug=%r category=%r capability=%r domain=%r",
            spec.name, spec.slug, spec.category, capability_type, intended_domain,
        )

        if getattr(spec, "use_cases", None):
            LOG.info(
                "Plugin use-cases (%d): %s",
                len(spec.use_cases),
                "; ".join(spec.use_cases),
            )

        # -----------------------------------------------------
        # CATEGORY ROTATION (loop_forever only)
        # -----------------------------------------------------
        if config.loop_forever and config.rotate_categories and config.max_per_category is not None:
            cat = str(spec.category)
            if category_counts.get(cat, 0) >= config.max_per_category:
                LOG.info("Skipping category %r → rotation active.", cat)
                index_counter += 1
                continue

        plugin_path = PLUGINS_DIR / f"{spec.slug}.py"
        if plugin_path.exists() and not is_upgrade_attempt:
            LOG.warning("Slug %r already exists → skipping", spec.slug)
            existing_slugs.add(spec.slug)
            existing_signatures.add(_spec_signature(spec))
            index_counter += 1
            continue

        # -----------------------------------------------------
        # EXTRA INSTRUCTIONS (use-case shaping)
        # -----------------------------------------------------
        extra_instructions = None
        if getattr(spec, "use_cases", None):
            extra_instructions = (
                "Optimize this plugin for these concrete use-cases:\n"
                + "\n".join(f"- {uc}" for uc in spec.use_cases)
                + "\n\nAlways produce insights and actions directly useful for these scenarios."
            )
        if _is_ai_roadmap_spec(spec):
            handoff_context = (getattr(spec, "extra", {}) or {}).get("handoff_context", "")
            if handoff_context:
                extra_instructions = (
                    (extra_instructions or "")
                    + "\n\n"
                    + handoff_context
                    + "\n\nUse the handoff as continuity context. Do not reinvent earlier AI roadmap plugins."
                ).strip()

        # -----------------------------------------------------
        # MEMORY CONTEXT (simple existing-slug awareness)
        # -----------------------------------------------------
        memory_context = _build_memory_context(existing_slugs)
        if _is_ai_roadmap_spec(spec):
            handoff_context = (getattr(spec, "extra", {}) or {}).get("handoff_context", "")
            if handoff_context:
                memory_context = "\n\n".join(part for part in [memory_context, handoff_context] if part)

        # -----------------------------------------------------
        # CALL STATION B
        # -----------------------------------------------------
        try:
            result = _build_registered_profile_result(
                spec=spec,
                capability_type=capability_type,
                reason="registered AI roadmap profile bypassed Station B LLM generation",
            )
            if result is not None:
                LOG.info(
                    "Registered profile %r generated %r without Station B LLM call.",
                    getattr(result, "logic_profile_id", None),
                    spec.slug,
                )
            else:
                sb_cfg = config.station_b_config()

                result = await generate_plugin_source(
                    spec,
                    capability_type=capability_type,
                    intended_domain=intended_domain,
                    extra_instructions=extra_instructions,
                    memory_context=memory_context,
                    mode="generate",
                    existing_source_excerpt=None,
                    config=sb_cfg,
                )

            LOG.info(
                "Station B generation completed for %r (logic_profile_id=%r).",
                spec.slug,
                getattr(result, "logic_profile_id", None),
            )

            _se_record(
                EVENT_FACTORY_STATION_B_GENERATED,
                slug=spec.slug,
                category=getattr(spec, "category", None),
                capability_type=capability_type,
                domain=intended_domain,
                logic_profile_id=getattr(result, "logic_profile_id", None),
            )

            manager = _LEARNING
            if manager is not None and hasattr(manager, "record_station_b_result"):
                try:
                    manager.record_station_b_result(
                        slug=spec.slug,
                        category=getattr(spec, "category", None),
                        capability_type=capability_type,
                        domain=intended_domain,
                        logic_profile_id=getattr(result, "logic_profile_id", None),
                        logic_blueprint=getattr(result, "logic_blueprint", None),
                    )
                except Exception:
                    LOG.debug("Learning manager record_station_b_result failed", exc_info=True)

        except Exception as exc:
            LOG.exception("❌ Station B failed for slug=%r → %s", spec.slug, exc)

            _se_record(
                EVENT_FACTORY_STATION_B_ERROR,
                slug=spec.slug,
                category=getattr(spec, "category", None),
                capability_type=capability_type,
                domain=intended_domain,
                error=str(exc),
            )

            if not config.loop_forever:
                LOG.error("Aborting build (non-loop mode).")
                break

            LOG.info("Retry in %s seconds…", config.sleep_seconds)
            await asyncio.sleep(config.sleep_seconds)
            index_counter += 1
            continue

        if _is_ai_roadmap_spec(spec) and _station_b_result_is_fallback(result):
            raw_reason = str(getattr(result, "raw_llm_output", "") or "unknown Station B fallback")
            profile_id = _registered_profile_id(spec.slug) if callable(_registered_profile_id) else None
            if profile_id and callable(_build_profile_source):
                profile_source = _build_profile_source(
                    result.source,
                    spec,
                    capability_type,
                    getattr(result, "logic_profile_id", None),
                    reason=f"Station B fallback replaced by capability profile: {raw_reason}",
                )
                if profile_source:
                    result.source = profile_source
                    try:
                        result.logic_profile_id = profile_id
                    except Exception:
                        pass
                    LOG.warning(
                        "Station B fallback for AI roadmap plugin %r was replaced by capability profile %r.",
                        spec.slug,
                        profile_id,
                    )
                else:
                    profile_id = None
            if profile_id:
                pass
            else:
                LOG.error(
                    "Rejecting AI roadmap plugin %r because Station B returned fallback output: %s",
                    spec.slug,
                    raw_reason,
                )
                _se_record(
                    EVENT_FACTORY_STATION_B_ERROR,
                    slug=spec.slug,
                    category=getattr(spec, "category", None),
                    capability_type=capability_type,
                    domain=intended_domain,
                    error=raw_reason,
                    rejected=True,
                )
                if not config.loop_forever:
                    break

                LOG.info(
                    "AI roadmap generation did not produce real model logic; retrying same spec in %.1f seconds.",
                    config.sleep_seconds,
                )
                await asyncio.sleep(config.sleep_seconds)
                continue

        if _is_ai_roadmap_spec(spec) and callable(_build_profile_source):
            profile_id = _registered_profile_id(spec.slug) if callable(_registered_profile_id) else None
            if profile_id:
                profile_source = _build_profile_source(
                    result.source,
                    spec,
                    capability_type,
                    getattr(result, "logic_profile_id", None),
                    reason="capability profile registry override",
                )
                if profile_source:
                    result.source = profile_source
                    try:
                        result.logic_profile_id = profile_id
                    except Exception:
                        pass
                    LOG.info(
                        "Applied capability profile %r to AI roadmap plugin %r.",
                        profile_id,
                        spec.slug,
                    )
            else:
                LOG.error(
                    "Rejecting AI roadmap plugin %r because no capability profile is registered.",
                    spec.slug,
                )
                _se_record(
                    EVENT_FACTORY_STATION_B_ERROR,
                    slug=spec.slug,
                    category=getattr(spec, "category", None),
                    capability_type=capability_type,
                    domain=intended_domain,
                    error="missing capability profile",
                    rejected=True,
                )
                if not config.loop_forever:
                    break
                await asyncio.sleep(config.sleep_seconds)
                continue

        # -----------------------------------------------------
        # STAGE CANDIDATE FILE
        # -----------------------------------------------------
        # Candidates are intentionally kept out of plugins/ until every gate
        # passes. A rejected plugin should never appear as an installable
        # artifact or be committed to GitHub.
        try:
            candidate_path = _write_candidate_plugin_file(spec.slug, result.source)
        except DraftRepairGateError as exc:
            reason = str(exc)
            LOG.error("Draft repair gate rejected AI roadmap plugin %r → %s", spec.slug, reason)
            if is_upgrade_attempt and source_spec is not None:
                _upgrade_attempt_record(
                    state=ai_roadmap_state,
                    source_spec=source_spec,
                    canonical_spec=spec,
                    status="rejected",
                    reason=reason,
                )
            elif source_spec is not None:
                _capability_rejection_record(
                    state=ai_roadmap_state,
                    spec=source_spec,
                    reason=reason,
                    repair_gate_failed=True,
                )
                existing_slugs.add(spec.slug)
                existing_signatures.add(_spec_signature(spec))
                index_counter = selected_index + 1
            if not config.loop_forever:
                break
            LOG.info(
                "AI roadmap plugin failed draft repair gate; retrying same spec in %.1f seconds.",
                config.sleep_seconds,
            )
            await asyncio.sleep(config.sleep_seconds)
            continue
        plugin_path = candidate_path
        LOG.info("Plugin candidate staged: %s", candidate_path)

        # -----------------------------------------------------
        # VALIDATE WITH STATION C
        # -----------------------------------------------------
        ok, reason = await _validate_plugin_file(candidate_path, spec)
        if ok:
            LOG.info(
                "Plugin validation OK%s%s",
                " (note: " if reason else "",
                f"{reason})" if reason else "",
            )
        else:
            LOG.error("Structural validation FAILED → %s", reason)
            _se_record(
                EVENT_FACTORY_PLUGIN_STRUCTURAL_FAILED,
                slug=spec.slug,
                category=getattr(spec, "category", None),
                capability_type=capability_type,
                domain=intended_domain,
                reason=reason,
            )
            try:
                rejected_path = _discard_candidate_plugin(candidate_path, reason=f"structural_validation: {reason}")
                LOG.info("Rejected structurally invalid candidate moved to %s", rejected_path)
            except Exception:
                LOG.warning("Unable to discard structurally invalid candidate %r", spec.slug, exc_info=True)
            if is_upgrade_attempt and source_spec is not None:
                _upgrade_attempt_record(
                    state=ai_roadmap_state,
                    source_spec=source_spec,
                    canonical_spec=spec,
                    status="rejected",
                    reason=f"structural_validation: {reason}",
                )

            if not config.loop_forever:
                break

            LOG.info(
                "Plugin candidate did not pass structural validation; retrying same spec in %.1f seconds.",
                config.sleep_seconds,
            )
            await asyncio.sleep(config.sleep_seconds)
            continue

        # -----------------------------------------------------
        # SEMANTIC DEPTH CHECK (AI roadmap only)
        # -----------------------------------------------------
        if ok and _is_ai_roadmap_spec(spec):
            try:
                semantic_ok, semantic_reason = await _semantic_depth_check(candidate_path, spec)
            except Exception as exc:
                semantic_ok = False
                semantic_reason = f"semantic_depth: check crashed: {exc}"

            if semantic_ok:
                LOG.info("Plugin semantic depth OK: %s", semantic_reason)
            else:
                LOG.error(
                    "Semantic depth FAILED for AI roadmap plugin %r → %s",
                    spec.slug,
                    semantic_reason,
                )
                repair_source = _build_semantic_repair_source(
                    source=result.source,
                    spec=spec,
                    capability_type=capability_type,
                    logic_profile_id=getattr(result, "logic_profile_id", None),
                    reason=semantic_reason,
                )
                if repair_source:
                    try:
                        candidate_path = _write_candidate_plugin_file(spec.slug, repair_source)
                    except DraftRepairGateError as exc:
                        semantic_ok = False
                        semantic_reason = str(exc)
                        LOG.error(
                            "Draft repair gate rejected semantic repair for AI roadmap plugin %r → %s",
                            spec.slug,
                            semantic_reason,
                        )
                    else:
                        plugin_path = candidate_path
                        ok, reason = await _validate_plugin_file(candidate_path, spec)
                        if ok:
                            try:
                                semantic_ok, semantic_reason = await _semantic_depth_check(candidate_path, spec)
                            except Exception as exc:
                                semantic_ok = False
                                semantic_reason = f"semantic_depth: repaired check crashed: {exc}"
                        if ok and semantic_ok:
                            LOG.info(
                                "Semantic repair accepted for AI roadmap plugin %r: %s",
                                spec.slug,
                                semantic_reason,
                            )
                            result.source = repair_source
                        else:
                            LOG.error(
                                "Semantic repair failed for AI roadmap plugin %r → validation_ok=%r reason=%s semantic=%s",
                                spec.slug,
                                ok,
                                reason,
                                semantic_reason,
                            )

                if semantic_ok:
                    # Repair succeeded; continue to optional evaluation/handoff.
                    pass
                else:
                    try:
                        quarantine_path = _discard_candidate_plugin(
                            candidate_path,
                            reason=semantic_reason,
                        )
                        LOG.info("Rejected shallow candidate moved to %s", quarantine_path)
                    except Exception:
                        LOG.warning("Unable to discard rejected candidate %r", spec.slug, exc_info=True)
                    if is_upgrade_attempt and source_spec is not None:
                        _upgrade_attempt_record(
                            state=ai_roadmap_state,
                            source_spec=source_spec,
                            canonical_spec=spec,
                            status="rejected",
                            reason=semantic_reason,
                        )

                    _se_record(
                        EVENT_FACTORY_PLUGIN_LOW_SCORE,
                        slug=spec.slug,
                        category=getattr(spec, "category", None),
                        capability_type=capability_type,
                        domain=intended_domain,
                        score=0.0,
                        threshold=config.evaluation_threshold,
                        reason=semantic_reason,
                        semantic_depth_failed=True,
                    )

                    if not config.loop_forever:
                        break

                    LOG.info(
                        "AI roadmap plugin was structurally valid but semantically shallow; retrying same spec in %.1f seconds.",
                        config.sleep_seconds,
                    )
                    await asyncio.sleep(config.sleep_seconds)
                    continue

        # -----------------------------------------------------
        # PRODUCTION QUALITY SCORE GATE (AI roadmap only)
        # -----------------------------------------------------
        if ok and _is_ai_roadmap_spec(spec):
            try:
                promotion_ok, promotion_reason = await _capability_promotion_gate(candidate_path, spec)
            except Exception as exc:
                promotion_ok = False
                promotion_reason = f"capability_promotion: check crashed: {exc}"

            if promotion_ok:
                LOG.info("Plugin capability promotion OK: %s", promotion_reason)
            else:
                LOG.error(
                    "Capability promotion FAILED for AI roadmap plugin %r → %s",
                    spec.slug,
                    promotion_reason,
                )
                repair_source = _build_semantic_repair_source(
                    source=result.source,
                    spec=spec,
                    capability_type=capability_type,
                    logic_profile_id=getattr(result, "logic_profile_id", None),
                    reason=promotion_reason,
                )
                if repair_source:
                    try:
                        candidate_path = _write_candidate_plugin_file(spec.slug, repair_source)
                    except DraftRepairGateError as exc:
                        promotion_ok = False
                        promotion_reason = str(exc)
                        LOG.error(
                            "Draft repair gate rejected promotion repair for AI roadmap plugin %r → %s",
                            spec.slug,
                            promotion_reason,
                        )
                    else:
                        plugin_path = candidate_path
                        try:
                            promotion_ok, promotion_reason = await _capability_promotion_gate(candidate_path, spec)
                        except Exception as exc:
                            promotion_ok = False
                            promotion_reason = f"capability_promotion: repaired check crashed: {exc}"
                        if promotion_ok:
                            LOG.info("Capability promotion repair accepted for %r: %s", spec.slug, promotion_reason)
                            result.source = repair_source

                if not promotion_ok:
                    try:
                        rejected_path = _discard_candidate_plugin(candidate_path, reason=promotion_reason)
                        LOG.info("Rejected non-promotable candidate moved to %s", rejected_path)
                    except Exception:
                        LOG.warning("Unable to discard non-promotable candidate %r", spec.slug, exc_info=True)
                    if is_upgrade_attempt and source_spec is not None:
                        _upgrade_attempt_record(
                            state=ai_roadmap_state,
                            source_spec=source_spec,
                            canonical_spec=spec,
                            status="rejected",
                            reason=promotion_reason,
                        )
                    elif source_spec is not None:
                        _capability_rejection_record(
                            state=ai_roadmap_state,
                            spec=source_spec,
                            reason=promotion_reason,
                        )
                        existing_slugs.add(spec.slug)
                        existing_signatures.add(_spec_signature(spec))
                        index_counter = selected_index + 1
                    if not config.loop_forever:
                        break
                    LOG.info(
                        "AI roadmap plugin failed capability promotion; retrying same spec in %.1f seconds.",
                        config.sleep_seconds,
                    )
                    await asyncio.sleep(config.sleep_seconds)
                    continue

            try:
                production_ok, production_reason = await _production_quality_gate(candidate_path, spec)
            except Exception as exc:
                production_ok = False
                production_reason = f"production_quality: check crashed: {exc}"

            if production_ok:
                LOG.info("Plugin production quality OK: %s", production_reason)
            else:
                LOG.error(
                    "Production quality FAILED for AI roadmap plugin %r → %s",
                    spec.slug,
                    production_reason,
                )
                try:
                    rejected_path = _discard_candidate_plugin(candidate_path, reason=production_reason)
                    LOG.info("Rejected sub-threshold candidate moved to %s", rejected_path)
                except Exception:
                    LOG.warning("Unable to discard sub-threshold candidate %r", spec.slug, exc_info=True)
                if is_upgrade_attempt and source_spec is not None:
                    _upgrade_attempt_record(
                        state=ai_roadmap_state,
                        source_spec=source_spec,
                        canonical_spec=spec,
                        status="rejected",
                        reason=production_reason,
                    )
                elif source_spec is not None:
                    _capability_rejection_record(
                        state=ai_roadmap_state,
                        spec=source_spec,
                        reason=production_reason,
                    )
                    existing_slugs.add(spec.slug)
                    existing_signatures.add(_spec_signature(spec))
                    index_counter = selected_index + 1

                _se_record(
                    EVENT_FACTORY_PLUGIN_LOW_SCORE,
                    slug=spec.slug,
                    category=getattr(spec, "category", None),
                    capability_type=capability_type,
                    domain=intended_domain,
                    score=0.0,
                    threshold=PRODUCTION_QUALITY_THRESHOLD,
                    reason=production_reason,
                    production_quality_failed=True,
                )

                if not config.loop_forever:
                    break

                LOG.info(
                    "AI roadmap plugin scored below production threshold; retrying same spec in %.1f seconds.",
                    config.sleep_seconds,
                )
                await asyncio.sleep(config.sleep_seconds)
                continue

            try:
                identity_ok, identity_reason = await _capability_name_and_uniqueness_gate(candidate_path, spec)
            except Exception as exc:
                identity_ok = False
                identity_reason = f"capability_identity: check crashed: {exc}"

            if identity_ok:
                LOG.info("Plugin capability identity OK: %s", identity_reason)
            else:
                LOG.error(
                    "Capability identity FAILED for AI roadmap plugin %r → %s",
                    spec.slug,
                    identity_reason,
                )
                try:
                    rejected_path = _discard_candidate_plugin(candidate_path, reason=identity_reason)
                    LOG.info("Rejected identity/overlap candidate moved to %s", rejected_path)
                except Exception:
                    LOG.warning("Unable to discard identity/overlap candidate %r", spec.slug, exc_info=True)
                if is_upgrade_attempt and source_spec is not None:
                    _upgrade_attempt_record(
                        state=ai_roadmap_state,
                        source_spec=source_spec,
                        canonical_spec=spec,
                        status="rejected",
                        reason=identity_reason,
                    )
                elif source_spec is not None:
                    _capability_rejection_record(
                        state=ai_roadmap_state,
                        spec=source_spec,
                        reason=identity_reason,
                    )
                    existing_slugs.add(spec.slug)
                    existing_signatures.add(_spec_signature(spec))
                    index_counter = selected_index + 1

                _se_record(
                    EVENT_FACTORY_PLUGIN_LOW_SCORE,
                    slug=spec.slug,
                    category=getattr(spec, "category", None),
                    capability_type=capability_type,
                    domain=intended_domain,
                    score=0.0,
                    threshold=PRODUCTION_QUALITY_THRESHOLD,
                    reason=identity_reason,
                    identity_quality_failed=True,
                )

                if not config.loop_forever:
                    break

                LOG.info(
                    "AI roadmap plugin failed name/uniqueness gate; retrying same spec in %.1f seconds.",
                    config.sleep_seconds,
                )
                await asyncio.sleep(config.sleep_seconds)
                continue

            try:
                a_plus_ok, a_plus_reason = await _a_plus_certification_gate(candidate_path, spec)
            except Exception as exc:
                a_plus_ok = False
                a_plus_reason = f"a_plus: check crashed: {exc}"

            if a_plus_ok:
                LOG.info("Plugin A+ certification OK: %s", a_plus_reason)
            else:
                LOG.error(
                    "A+ certification FAILED for AI roadmap plugin %r → %s",
                    spec.slug,
                    a_plus_reason,
                )
                try:
                    rejected_path = _discard_candidate_plugin(candidate_path, reason=a_plus_reason)
                    LOG.info("Rejected non-A+ candidate moved to %s", rejected_path)
                except Exception:
                    LOG.warning("Unable to discard non-A+ candidate %r", spec.slug, exc_info=True)
                if is_upgrade_attempt and source_spec is not None:
                    _upgrade_attempt_record(
                        state=ai_roadmap_state,
                        source_spec=source_spec,
                        canonical_spec=spec,
                        status="rejected",
                        reason=a_plus_reason,
                    )
                elif source_spec is not None:
                    _capability_rejection_record(
                        state=ai_roadmap_state,
                        spec=source_spec,
                        reason=a_plus_reason,
                    )
                    existing_slugs.add(spec.slug)
                    existing_signatures.add(_spec_signature(spec))
                    index_counter = selected_index + 1

                _se_record(
                    EVENT_FACTORY_PLUGIN_LOW_SCORE,
                    slug=spec.slug,
                    category=getattr(spec, "category", None),
                    capability_type=capability_type,
                    domain=intended_domain,
                    score=0.0,
                    threshold=A_PLUS_MIN_SCORE,
                    reason=a_plus_reason,
                    a_plus_certification_failed=True,
                )

                if not config.loop_forever:
                    break

                LOG.info(
                    "AI roadmap plugin failed A+ certification; retrying same spec in %.1f seconds.",
                    config.sleep_seconds,
                )
                await asyncio.sleep(config.sleep_seconds)
                continue

        if is_upgrade_attempt:
            existing_canonical_path = PLUGINS_DIR / f"{spec.slug}.py"
            try:
                upgrade_ok, upgrade_reason = await _upgrade_candidate_improves_existing(
                    candidate_path=candidate_path,
                    existing_path=existing_canonical_path,
                    spec=spec,
                )
            except Exception as exc:
                upgrade_ok = False
                upgrade_reason = f"upgrade_gate: check crashed: {exc}"

            if upgrade_ok:
                LOG.info(
                    "Upgrade candidate accepted as canonical upgrade for %r: %s",
                    spec.slug,
                    upgrade_reason,
                )
            else:
                LOG.error(
                    "Discarding upgrade candidate for %r because it did not improve the canonical capability: %s",
                    spec.slug,
                    upgrade_reason,
                )
                try:
                    rejected_path = _discard_candidate_plugin(candidate_path, reason=upgrade_reason)
                    LOG.info("Rejected non-improving upgrade candidate moved to %s", rejected_path)
                except Exception:
                    LOG.warning("Unable to discard non-improving candidate %r", spec.slug, exc_info=True)
                if source_spec is not None:
                    _upgrade_attempt_record(
                        state=ai_roadmap_state,
                        source_spec=source_spec,
                        canonical_spec=spec,
                        status="rejected",
                        reason=upgrade_reason,
                    )

                if not config.loop_forever:
                    break
                await asyncio.sleep(config.sleep_seconds)
                continue

        plugin_path = _promote_candidate_plugin(candidate_path, spec.slug)
        LOG.info("✅ Plugin built: %s", plugin_path)
        existing_slugs.add(spec.slug)
        existing_signatures.add(_spec_signature(spec))
        if is_upgrade_attempt and source_spec is not None:
            _upgrade_attempt_record(
                state=ai_roadmap_state,
                source_spec=source_spec,
                canonical_spec=spec,
                status="accepted",
                reason="candidate improved canonical capability and overwrote the base module",
            )

        # -----------------------------------------------------
        # OPTIONAL EVALUATION (Station D critic)
        # -----------------------------------------------------
        eval_result: Optional[Dict[str, Any]] = None
        if ok:
            eval_result = await _maybe_evaluate_plugin(
                plugin_path=plugin_path,
                spec=spec,
                capability_type=capability_type,
                intended_domain=intended_domain,
                config=config,
            )

        if ok and _is_ai_roadmap_spec(spec):
            try:
                next_spec_for_handoff, _, _ = build_next_spec(selected_index + 1)
            except Exception:
                next_spec_for_handoff = None
            ai_roadmap_state = _record_ai_roadmap_success(
                state=ai_roadmap_state,
                spec=spec,
                plugin_path=plugin_path,
                next_spec=next_spec_for_handoff,
            )
            LOG.info(
                "AI roadmap handoff updated for %r; next directive prepared.",
                spec.slug,
            )

        if ok:
            publish_ok = _publish_plugin_to_github(
                plugin_path=plugin_path,
                spec=spec,
                config=config,
            )
            if not publish_ok:
                LOG.error(
                    "GitHub was not updated for generated plugin %r. The local artifact remains at %s.",
                    spec.slug,
                    plugin_path,
                )

        # -----------------------------------------------------
        # BOOKKEEPING
        # -----------------------------------------------------
        built_count += 1
        index_counter = max(index_counter, selected_index + 1)
        category_counts[spec.category] = category_counts.get(spec.category, 0) + 1

        # Telemetry: per-plugin result summary
        try:
            _se_record(
                EVENT_FACTORY_PLUGIN_RESULT,
                slug=spec.slug,
                category=getattr(spec, "category", None),
                capability_type=capability_type,
                domain=intended_domain,
                validation_ok=ok,
                validation_note=reason,
                eval_score=(eval_result or {}).get("score") if isinstance(eval_result, dict) else None,
            )
        except Exception:
            LOG.debug("Factory plugin result telemetry failed", exc_info=True)

        # -----------------------------------------------------
        # CLEANUP CYCLE (best-effort, never fatal)
        # -----------------------------------------------------
        try:
            await run_cleanup_cycle(
                root_dir=ROOT_DIR,
                plugins_dir=PLUGINS_DIR,
            )
        except Exception as exc:  # pragma: no cover - defensive
            LOG.warning("Cleanup cycle failed (non-fatal): %s", exc)

        # -----------------------------------------------------
        # LOOP CONTROL
        # -----------------------------------------------------
        if not config.loop_forever:
            if target_count is not None and built_count >= target_count:
                LOG.info("Factory run completed.")
                break
            LOG.info("Factory run completed (non-loop mode).")
            break

        LOG.info("Sleeping for %.1f seconds…", config.sleep_seconds)
        await asyncio.sleep(config.sleep_seconds)

    # Run-level telemetry
    try:
        _se_record(
            EVENT_FACTORY_RUN_COMPLETED,
            built_count=built_count,
        )
    except Exception:
        LOG.debug("Factory run completion telemetry failed", exc_info=True)


# =====================================================================
# CLI
# =====================================================================

def _env(name: str, default: Optional[str] = None) -> Optional[str]:
    value = os.environ.get(name)
    if value is None or value == "":
        return default
    return value


def _env_bool(name: str, default: bool) -> bool:
    raw = _env(name)
    if raw is None:
        return default
    return raw.strip().lower() in {"1", "true", "yes", "on"}


def _env_int(name: str, default: Optional[int]) -> Optional[int]:
    raw = _env(name)
    if raw is None:
        return default
    return int(raw)


def _env_float(name: str, default: float) -> float:
    raw = _env(name)
    if raw is None:
        return default
    return float(raw)


def _build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="python -m factory.factory_runner",
        description="Run the Francis autonomous AI capability factory.",
    )
    parser.add_argument(
        "--once",
        action="store_true",
        help="Build one capability module and stop. Overrides loop mode unless --max-plugins is provided.",
    )
    parser.add_argument(
        "--max-plugins",
        type=int,
        default=_env_int("FRANCIS_FACTORY_MAX_PLUGINS", None),
        help="Build a finite number of capability modules and stop.",
    )
    parser.add_argument(
        "--loop",
        action="store_true",
        default=_env_bool("FRANCIS_FACTORY_LOOP", True),
        help="Run continuously. Enabled by default for side-project operation.",
    )
    parser.add_argument(
        "--sleep-seconds",
        type=float,
        default=_env_float("FRANCIS_FACTORY_SLEEP_SECONDS", 15.0),
        help="Seconds to sleep between production attempts.",
    )
    parser.add_argument(
        "--user-id",
        default=_env("FRANCIS_FACTORY_USER_ID", "francis-factory"),
        help="User/owner id recorded on generated capability specs.",
    )
    parser.add_argument(
        "--model",
        default=_env("FRANCIS_FACTORY_MODEL", "llama3.1:8b"),
        help="Ollama model used by Station B.",
    )
    parser.add_argument(
        "--temperature",
        type=float,
        default=_env_float("FRANCIS_FACTORY_TEMPERATURE", 0.25),
        help="Station B model temperature.",
    )
    parser.add_argument(
        "--max-tokens",
        type=int,
        default=_env_int("FRANCIS_FACTORY_MAX_TOKENS", 4096),
        help="Station B maximum output tokens.",
    )
    parser.add_argument(
        "--context-length",
        type=int,
        default=_env_int("FRANCIS_FACTORY_CONTEXT_LENGTH", 8192),
        help="Station B Ollama context length. Must exceed --max-tokens.",
    )
    parser.add_argument(
        "--timeout-seconds",
        type=int,
        default=_env_int("FRANCIS_FACTORY_TIMEOUT_SECONDS", 900),
        help="Station B LLM timeout in seconds.",
    )
    parser.add_argument(
        "--evaluation-enabled",
        action="store_true",
        default=_env_bool("FRANCIS_FACTORY_EVALUATION_ENABLED", False),
        help="Enable optional Station D evaluation when available.",
    )
    parser.add_argument(
        "--evaluation-threshold",
        type=float,
        default=_env_float("FRANCIS_FACTORY_EVALUATION_THRESHOLD", 0.65),
        help="Minimum acceptable Station D evaluation score.",
    )
    parser.add_argument(
        "--evaluation-profile",
        default=_env("FRANCIS_FACTORY_EVALUATION_PROFILE", None),
        help="Optional Station D evaluation profile.",
    )
    parser.add_argument(
        "--evaluation-enforce",
        action="store_true",
        default=_env_bool("FRANCIS_FACTORY_EVALUATION_ENFORCE", False),
        help="Reserve flag for future reject-on-low-score behavior.",
    )
    parser.add_argument(
        "--no-category-rotation",
        action="store_true",
        default=_env_bool("FRANCIS_FACTORY_NO_CATEGORY_ROTATION", False),
        help="Disable category rotation guardrails.",
    )
    parser.add_argument(
        "--max-per-category",
        type=int,
        default=_env_int("FRANCIS_FACTORY_MAX_PER_CATEGORY", None),
        help="Maximum capability modules per category during a loop run.",
    )
    parser.add_argument(
        "--no-github-publish",
        action="store_true",
        default=_env_bool("FRANCIS_FACTORY_NO_GITHUB_PUBLISH", False),
        help="Disable automatic git commit/push for each validated capability module.",
    )
    parser.add_argument(
        "--github-remote",
        default=_env("FRANCIS_FACTORY_GITHUB_REMOTE", "origin"),
        help="Git remote used when publishing generated capability modules.",
    )
    parser.add_argument(
        "--github-branch",
        default=_env("FRANCIS_FACTORY_GITHUB_BRANCH", "main"),
        help="Git branch pushed after each generated plugin commit.",
    )
    parser.add_argument(
        "--allow-upgrade-expansion",
        action="store_true",
        default=_env_bool("FRANCIS_FACTORY_ALLOW_UPGRADE_EXPANSION", False),
        help="Allow internal second-pass upgrade attempts after the unique AI roadmap is complete.",
    )
    parser.add_argument(
        "--no-randomized-expansion",
        action="store_true",
        default=_env_bool("FRANCIS_FACTORY_NO_RANDOMIZED_EXPANSION", False),
        help="Disable bounded randomized upgrade attempts after the curated roadmap is complete.",
    )
    parser.add_argument(
        "--print-config",
        action="store_true",
        help="Print the resolved RunnerConfig as JSON and exit.",
    )
    parser.add_argument(
        "--log-level",
        default=_env("FRANCIS_FACTORY_LOG_LEVEL", "INFO"),
        help="Python logging level: DEBUG, INFO, WARNING, ERROR.",
    )
    return parser


def build_config_from_args(argv: Optional[Sequence[str]] = None) -> tuple[RunnerConfig, str, bool]:
    """
    Resolve production configuration from environment variables and CLI flags.

    Environment variables use the FRANCIS_FACTORY_* prefix; CLI flags take
    precedence naturally because argparse receives env-backed defaults.
    """
    parser = _build_arg_parser()
    args = parser.parse_args(argv)

    max_plugins = args.max_plugins
    loop_forever = bool(args.loop)
    if args.once:
        loop_forever = False
        if max_plugins is None:
            max_plugins = 1
    elif max_plugins is not None:
        loop_forever = False

    cfg = RunnerConfig(
        max_plugins=max_plugins,
        sleep_seconds=args.sleep_seconds,
        loop_forever=loop_forever,
        user_id=args.user_id,
        llm_model=args.model,
        llm_temperature=args.temperature,
        llm_max_tokens=args.max_tokens,
        llm_context_length=args.context_length,
        llm_timeout_seconds=args.timeout_seconds,
        rotate_categories=not args.no_category_rotation,
        max_per_category=args.max_per_category,
        evaluation_enabled=args.evaluation_enabled,
        evaluation_threshold=args.evaluation_threshold,
        evaluation_profile=args.evaluation_profile,
        evaluation_log_only=not args.evaluation_enforce,
        github_publish_enabled=not args.no_github_publish,
        github_remote=args.github_remote,
        github_branch=args.github_branch,
        allow_upgrade_expansion=args.allow_upgrade_expansion,
        randomized_expansion=not args.no_randomized_expansion,
    )
    cfg.validate()
    return cfg, str(args.log_level).upper(), bool(args.print_config)


def main(argv: Optional[Sequence[str]] = None) -> int:
    try:
        cfg, log_level_name, print_config = build_config_from_args(argv)
    except Exception as exc:
        print(f"factory_runner configuration error: {exc}", file=sys.stderr)
        return 2

    logging.basicConfig(
        level=getattr(logging, log_level_name, logging.INFO),
        format="[%(asctime)s] [%(levelname)s] %(message)s",
    )

    if print_config:
        print(json.dumps(asdict(cfg), indent=2, sort_keys=True))
        return 0

    try:
        asyncio.run(run_factory(cfg))
    except FactoryAlreadyRunningError as exc:
        LOG.error("%s", exc)
        return 3
    except KeyboardInterrupt:
        LOG.info("Factory runner stopped by operator.")
        return 130
    except Exception:
        LOG.exception("Factory runner crashed.")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
