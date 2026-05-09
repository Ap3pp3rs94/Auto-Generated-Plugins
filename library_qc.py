from __future__ import annotations

import asyncio
import importlib.util
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List

from plugin_spec import PluginSpec
from station_c_validator import validate_plugin_module, ValidationResult
from learning.collector import log_plugin_event


PROJECT_ROOT = Path(__file__).resolve().parent
INDEX_PATH = PROJECT_ROOT.parent / "plugin_index.json"


@dataclass
class PluginIndexEntry:
    name: str
    slug: str
    goal: str
    category: str
    tags: List[str]
    path: str


def load_plugin_index(path: Path = INDEX_PATH) -> List[PluginIndexEntry]:
    if not path.exists():
        print(f"[QC] No plugin_index.json found at {path}")
        return []

    raw = json.loads(path.read_text(encoding="utf-8"))
    entries: List[PluginIndexEntry] = []

    for e in raw.get("plugins", []):
        entries.append(
            PluginIndexEntry(
                name=e["name"],
                slug=e["slug"],
                goal=e.get("goal", ""),
                category=e.get("category", ""),
                tags=list(e.get("tags", [])),
                path=e["path"],
            )
        )

    return entries


def _import_module_from_path(path: Path, slug: str) -> Any:
    module_name = f"francis_plugin_qc_{slug}"
    spec = importlib.util.spec_from_file_location(module_name, str(path))
    if spec is None or not spec.loader:
        raise RuntimeError(f"Could not create import spec for {path}")

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


async def qc_plugin(entry: PluginIndexEntry) -> tuple[PluginIndexEntry, ValidationResult]:
    path = Path(entry.path)

    if not path.exists():
        vr = ValidationResult(
            ok=False,
            errors=[f"Plugin file not found at recorded path: {path}"],
            warnings=[],
        )

        # Log missing file
        log_plugin_event(
            spec=PluginSpec.new(
                name=entry.name,
                goal=entry.goal,
                category=entry.category or "utility",
                tags=entry.tags,
            ),
            status="failure",
            code_path=path,
            validation_result=vr,
            user_id="austin",
            run_id=None,
            extra={"source": "library_qc.missing_file"},
        )

        return entry, vr

    try:
        module = _import_module_from_path(path, entry.slug)
    except Exception as e:
        vr = ValidationResult(
            ok=False,
            errors=[f"Failed to import plugin module from {path}: {e}"],
            warnings=[],
        )

        # Log failed import
        log_plugin_event(
            spec=PluginSpec.new(
                name=entry.name,
                goal=entry.goal,
                category=entry.category or "utility",
                tags=entry.tags,
            ),
            status="failure",
            code_path=path,
            validation_result=vr,
            user_id="austin",
            run_id=None,
            extra={"source": "library_qc.import_failure"},
        )

        return entry, vr

    # Rebuild a PluginSpec for validation
    spec = PluginSpec.new(
        name=entry.name,
        goal=entry.goal,
        category=entry.category or "utility",
        tags=entry.tags or [],
    )

    result = await validate_plugin_module(module, spec)

    # Log QC result
    log_plugin_event(
        spec=spec,
        status="success" if result.ok else "failure",
        code_path=path,
        validation_result=result,
        user_id="austin",
        run_id=None,
        extra={"source": "library_qc.validation"},
    )

    return entry, result


async def main() -> None:
    entries = load_plugin_index()
    if not entries:
        print("[QC] No plugins to validate.")
        return

    print(f"[QC] Loaded {len(entries)} plugin(s) from plugin_index.json\n")

    ok_count = 0
    fail_count = 0

    for entry in entries:
        print(f"[QC] Validating plugin: {entry.slug}")
        plugin_entry, vr = await qc_plugin(entry)

        if vr.ok:
            ok_count += 1
            status_str = "OK"
        else:
            fail_count += 1
            status_str = "FAILED"

        print(f"  -> Status: {status_str}")
        if vr.errors:
            print("  Errors:")
            for e in vr.errors:
                print(f"    - {e}")

        if vr.warnings:
            print("  Warnings:")
            for w in vr.warnings:
                print(f"    - {w}")

        print()

    print("=== QC SUMMARY ===")
    print(f"  Total plugins : {len(entries)}")
    print(f"  OK            : {ok_count}")
    print(f"  FAILED        : {fail_count}")


if __name__ == "__main__":
    asyncio.run(main())
