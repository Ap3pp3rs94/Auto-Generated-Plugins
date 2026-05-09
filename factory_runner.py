from __future__ import annotations

"""
Francis Plugin Factory Runner (Station Orchestrator)

This module orchestrates the Francis plugin factory:

- Discovers existing plugins in the ./plugins directory.
- Uses a deterministic spec builder (spec_builder.build_next_spec)
  to propose a new PluginSpec across multiple domains
  (system_automation, monitoring, security, ecommerce, etc.).
- Calls Station B to generate the plugin source code.
- Writes the plugin file to disk.
- Runs Station C's validator against the new plugin.
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

import asyncio
import atexit
import json
import logging
import os
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any, Dict, Optional, Set, Tuple

from plugin_spec import PluginSpec
from station_c_validator import validate_plugin_module
from factory.spec_builder import AI_CAPABILITY_ROADMAP, build_next_spec
from station_b import generate_plugin_source, StationBConfig

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

ROOT_DIR = Path(__file__).resolve().parent.parent
PLUGINS_DIR = ROOT_DIR / "plugins"
RUN_LOCK_PATH = ROOT_DIR / ".factory_runner.lock"
AI_ROADMAP_STATE_PATH = ROOT_DIR / "registry" / "ai_roadmap_state.json"

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
    Configuration for the Francis plugin factory runner.

    The runner can either:
    - build a finite number of plugins (max_plugins), or
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
    llm_max_tokens: int = 1024
    llm_timeout_seconds: int = 240

    # Category rotation (to avoid oversaturating a single category)
    rotate_categories: bool = True
    max_per_category: Optional[int] = None

    # Evaluation / critic integration (Station D evaluator)
    evaluation_enabled: bool = False
    evaluation_threshold: float = 0.60   # Score below this is considered "low quality"
    evaluation_profile: Optional[str] = None  # e.g. "research", "default"
    evaluation_log_only: bool = True     # If False, you could later add auto-reject logic.

    def station_b_config(self) -> StationBConfig:
        """Helper to build a StationBConfig from this RunnerConfig."""
        return StationBConfig(
            model=self.llm_model,
            temperature=self.llm_temperature,
            max_tokens=self.llm_max_tokens,
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
    roadmap_size = len(AI_CAPABILITY_ROADMAP)
    for position, blueprint in enumerate(AI_CAPABILITY_ROADMAP, start=1):
        base = blueprint.slug
        if slug == base:
            return position
        prefix = f"{base}_phase_"
        if slug.startswith(prefix):
            suffix = slug[len(prefix):]
            if suffix.isdigit():
                phase = max(int(suffix), 1)
                return (phase - 1) * roadmap_size + position
    return None


def _next_ai_roadmap_index(existing_slugs: Set[str]) -> int:
    """
    Advance from existing AI-roadmap plugins only.

    Old non-AI plugins do not push the factory deep into later AI phases.
    """
    existing_indexes = [
        idx for slug in existing_slugs
        for idx in [_roadmap_slug_index(slug)]
        if idx is not None
    ]
    if not existing_indexes:
        return 1
    return max(existing_indexes) + 1


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
    return data


def _save_ai_roadmap_state(state: Dict[str, Any]) -> None:
    AI_ROADMAP_STATE_PATH.parent.mkdir(parents=True, exist_ok=True)
    tmp = AI_ROADMAP_STATE_PATH.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(state, indent=2, sort_keys=True), encoding="utf-8")
    tmp.replace(AI_ROADMAP_STATE_PATH)


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
        LOG.info("Seeded AI roadmap handoff state from %d existing AI plugin(s).", len(seeded["completed"]))
        return seeded

    return state


def _write_plugin_file(slug: str, source: str) -> Path:
    _ensure_plugins_dir()
    path = PLUGINS_DIR / f"{slug}.py"
    path.write_text(source, encoding="utf-8")
    return path


def _validate_plugin_file(path: Path) -> Tuple[bool, str]:
    return validate_plugin_module(path)


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


async def _maybe_evaluate_plugin(
    *,
    plugin_path: Path,
    spec: PluginSpec,
    capability_type: Optional[str],
    intended_domain: Optional[str],
    config: RunnerConfig,
) -> Optional[Dict[str, Any]]:
    """
    Optional Station D evaluation / critic phase.

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
    ai_roadmap_state = _seed_ai_roadmap_state_from_existing(ai_roadmap_state, existing_slugs)
    LOG.info("Loaded %d existing plugin(s) from plugins/", len(existing_slugs))
    LOG.info(
        "Loaded AI roadmap handoff state with %d completed item(s).",
        len(ai_roadmap_state.get("completed") or []),
    )

    built_count = 0
    category_counts: Dict[str, int] = {}

    target_count = config.max_plugins
    if target_count is None and not config.loop_forever:
        target_count = 1

    index_counter = _next_ai_roadmap_index(existing_slugs)
    LOG.info("Starting AI roadmap at deterministic index %d", index_counter)

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
        capability_type: Optional[str] = None
        intended_domain: Optional[str] = None

        for _candidate_attempt in range(len(AI_CAPABILITY_ROADMAP) * 3):
            candidate_spec, candidate_capability, candidate_domain = build_next_spec(index_counter)
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
                index_counter += 1
                continue

            spec = candidate_spec
            capability_type = candidate_capability
            intended_domain = candidate_domain
            break

        if spec is None or capability_type is None or intended_domain is None:
            LOG.error("Unable to find a non-duplicate AI roadmap spec; stopping factory run.")
            break

        spec.owner_id = config.user_id
        spec.capability_type = capability_type
        spec.intended_domain = intended_domain
        _attach_ai_handoff_to_spec(spec, ai_roadmap_state)

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
        if plugin_path.exists():
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

        # -----------------------------------------------------
        # WRITE PLUGIN FILE
        # -----------------------------------------------------
        plugin_path = _write_plugin_file(spec.slug, result.source)
        LOG.info("✅ Plugin built: %s", plugin_path)
        existing_slugs.add(spec.slug)
        existing_signatures.add(_spec_signature(spec))

        # -----------------------------------------------------
        # VALIDATE WITH STATION C
        # -----------------------------------------------------
        ok, reason = _validate_plugin_file(plugin_path)
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

            # Attempt Station D repair (if available)
            try:
                repair_info = await repair_plugin(
                    spec.slug,
                    max_attempts=3,
                    intended_domain=intended_domain,
                    capability_type=capability_type,
                )
                LOG.info("Station D repair_plugin result for %r → %r", spec.slug, repair_info)

                _se_record(
                    EVENT_FACTORY_STATION_D_REPAIR_ATTEMPT,
                    slug=spec.slug,
                    category=getattr(spec, "category", None),
                    capability_type=capability_type,
                    domain=intended_domain,
                    repaired=repair_info.get("repaired"),
                    attempts=repair_info.get("attempts"),
                    error=repair_info.get("error"),
                )

                # If repaired, re-validate the final_path if present
                if repair_info.get("repaired"):
                    final_path_str = repair_info.get("final_path") or str(plugin_path)
                    final_path = Path(final_path_str)
                    ok, reason = _validate_plugin_file(final_path)
                    LOG.info(
                        "Re-validation of repaired plugin %r → ok=%r reason=%r",
                        spec.slug,
                        ok,
                        reason,
                    )
            except Exception as exc:  # pragma: no cover - defensive
                LOG.warning(
                    "Station D repair for plugin %r failed (non-fatal): %s",
                    spec.slug,
                    exc,
                )
                _se_record(
                    EVENT_FACTORY_STATION_D_REPAIR_ERROR,
                    slug=spec.slug,
                    error=str(exc),
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
                next_spec_for_handoff, _, _ = build_next_spec(index_counter + 1)
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

        # -----------------------------------------------------
        # BOOKKEEPING
        # -----------------------------------------------------
        built_count += 1
        index_counter += 1
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

def main() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="[%(asctime)s] [%(levelname)s] %(message)s",
    )

    cfg = RunnerConfig(
        loop_forever=True,
        llm_model="llama3.1:8b",
        llm_temperature=0.25,
        llm_max_tokens=1024,
        llm_timeout_seconds=240,
        # You can flip this on once Station D evaluator is implemented.
        evaluation_enabled=False,
        evaluation_threshold=0.65,
        evaluation_log_only=True,
    )

    asyncio.run(run_factory(cfg))


if __name__ == "__main__":
    main()
