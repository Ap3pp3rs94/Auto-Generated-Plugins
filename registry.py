from __future__ import annotations

import json
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any, Dict, List

try:
    from .plugin_spec import PluginSpec
except ImportError:  # pragma: no cover - direct script/local-folder import
    from plugin_spec import PluginSpec


REGISTRY_PATH = Path(__file__).resolve().parent.parent / "plugin_registry.json"


@dataclass
class RegistryEntry:
    """
    A single registered plugin.
    """
    name: str
    slug: str
    goal: str
    category: str
    tags: List[str]
    path: str
    runtime_hints: Dict[str, Any]

    @staticmethod
    def from_spec(spec: PluginSpec, *, path: Path, runtime_hints: Dict[str, Any]) -> "RegistryEntry":
        return RegistryEntry(
            name=spec.name,
            slug=spec.slug,
            goal=spec.goal,
            category=spec.category,
            tags=list(spec.tags),
            path=str(path),
            runtime_hints=runtime_hints or {},
        )


def _load_registry() -> Dict[str, Any]:
    if not REGISTRY_PATH.exists():
        return {"plugins": []}
    return json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))


def _save_registry(data: Dict[str, Any]) -> None:
    REGISTRY_PATH.write_text(json.dumps(data, indent=2), encoding="utf-8")


def upsert_entry(entry: RegistryEntry) -> None:
    data = _load_registry()
    plugins = data.get("plugins", [])

    # Overwrite if duplicate slug exists
    plugins = [p for p in plugins if p.get("slug") != entry.slug]
    plugins.append(asdict(entry))

    data["plugins"] = plugins
    _save_registry(data)


def entry_exists_for_slug(slug: str) -> bool:
    data = _load_registry()
    return any(p.get("slug") == slug for p in data.get("plugins", []))


def has_duplicate_capability(spec: PluginSpec) -> bool:
    """
    Soft duplicate detection:
    - name
    - slug
    - goal
    - tag overlap
    """
    data = _load_registry()
    for p in data.get("plugins", []):
        if (
            p.get("name") == spec.name
            or p.get("slug") == spec.slug
            or p.get("goal") == spec.goal
            or set(p.get("tags", [])) & set(spec.tags)
        ):
            return True
    return False


def plugin_path_for_spec(spec: PluginSpec) -> Path:
    """
    Determines where the plugin file should be stored.
    """
    root = Path(__file__).resolve().parent.parent / "library"
    root.mkdir(parents=True, exist_ok=True)
    return root / f"{spec.slug}.py"
