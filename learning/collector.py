from __future__ import annotations

import json
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Mapping, Optional

from ..plugin_spec import PluginSpec



# Where we store the learning log (JSONL)
_LOG_DIR = Path(__file__).resolve().parent
_LOG_PATH = _LOG_DIR / "plugins_log.jsonl"


@dataclass
class PluginEvent:
    """
    A single plugin generation + validation event.

    This is intentionally generic so we can evolve the schema over time
    without breaking consumers. Extra fields can go into `extra`.
    """

    timestamp: str

    user_id: Optional[str]
    run_id: Optional[str]

    plugin_name: str
    plugin_slug: str
    category: str
    tags: List[str]
    goal: str
    version: str

    status: str  # "success" | "failure" | "skipped"
    validator_ok: Optional[bool]
    validator_errors: List[str]
    validator_warnings: List[str]

    code_path: Optional[str]
    code_size_bytes: Optional[int]

    extra: Dict[str, Any]


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _safe_read_code_size(path: Optional[Path]) -> Optional[int]:
    if not path:
        return None
    try:
        return path.stat().st_size
    except OSError:
        return None


def _normalise_validation_result(
    validation_result: Optional[Mapping[str, Any]]
) -> Dict[str, Any]:
    """
    Normalise whatever Station C returns into a simple dict with:
    - ok: Optional[bool]
    - errors: List[str]
    - warnings: List[str]
    """
    if validation_result is None:
        return {"ok": None, "errors": [], "warnings": []}

    # Accept both object-style and dict-style validation results.
    ok = getattr(validation_result, "ok", None)
    errors = getattr(validation_result, "errors", None)
    warnings = getattr(validation_result, "warnings", None)

    if ok is None and isinstance(validation_result, Mapping):
        ok = validation_result.get("ok")
        errors = validation_result.get("errors", errors)
        warnings = validation_result.get("warnings", warnings)

    def _to_list(value: Any) -> List[str]:
        if value is None:
            return []
        if isinstance(value, str):
            return [value]
        if isinstance(value, (list, tuple)):
            return [str(v) for v in value]
        return [str(value)]

    return {
        "ok": bool(ok) if ok is not None else None,
        "errors": _to_list(errors),
        "warnings": _to_list(warnings),
    }


def _ensure_log_dir() -> None:
    _LOG_DIR.mkdir(parents=True, exist_ok=True)


def log_plugin_event(
    *,
    spec: PluginSpec,
    status: str,
    code_path: Optional[Path],
    validation_result: Optional[Mapping[str, Any]] = None,
    user_id: Optional[str] = None,
    run_id: Optional[str] = None,
    extra: Optional[Dict[str, Any]] = None,
) -> None:
    """
    Append a single PluginEvent to plugins_log.jsonl.

    This should be called by the factory once per plugin generation attempt,
    regardless of whether validation succeeded or failed.

    Args:
        spec: The PluginSpec used to generate the plugin.
        status: "success", "failure", or "skipped".
        code_path: Path to the generated plugin source file, if any.
        validation_result: Whatever Station C returned (ok/errors/warnings).
        user_id: Optional. Who triggered this run.
        run_id: Optional. Unique run identifier.
        extra: Optional. Any additional metadata you want to log.
    """
    if status not in {"success", "failure", "skipped"}:
        # Be conservative and avoid raising; just coerce.
        status = str(status)

    vr = _normalise_validation_result(validation_result)
    code_size = _safe_read_code_size(code_path)

    event = PluginEvent(
        timestamp=_now_iso(),
        user_id=user_id,
        run_id=run_id,
        plugin_name=spec.name,
        plugin_slug=spec.slug,
        category=spec.category,
        tags=list(spec.tags),
        goal=spec.goal,
        version=str(getattr(spec, "version", "0.1.0")),
        status=status,
        validator_ok=vr["ok"],
        validator_errors=vr["errors"],
        validator_warnings=vr["warnings"],
        code_path=str(code_path) if code_path is not None else None,
        code_size_bytes=code_size,
        extra=extra or {},
    )

    _ensure_log_dir()

    line = json.dumps(asdict(event), ensure_ascii=False)
    try:
        with _LOG_PATH.open("a", encoding="utf-8") as f:
            f.write(line + "\n")
    except OSError:
        # Last-resort: never let logging kill the factory.
        # Intentionally swallow exceptions here.
        pass


def iter_events() -> "list[PluginEvent]":
    """
    Convenience helper to read all logged events back into memory.

    This is primarily for:
    - analytics
    - building training datasets
    - debugging the factory

    Safe to call even if the log file doesn't exist yet.
    """
    events: List[PluginEvent] = []
    if not _LOG_PATH.exists():
        return events

    with _LOG_PATH.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                raw = json.loads(line)
                events.append(PluginEvent(**raw))
            except Exception:
                # Skip malformed lines; log file is append-only anyway.
                continue

    return events
