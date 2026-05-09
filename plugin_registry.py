from __future__ import annotations

"""
PluginRegistry

Small registry that:
- Scans ./plugins for *.py files.
- Tries to import each plugin once.
- Runs Station C's structural validator on the file path
  (ensuring it exposes an invoke(user_id, payload, **kwargs) entrypoint).
- Records whether it is usable or broken.
- Captures basic metadata/manifest for listing / discovery.
- Infers a PluginSpec-style view (family_key, generic-name flag) from
  the manifest to help naming, dedupe, and "creative break" tooling.
- Provides helpers to get/list plugins and load the module.

Used by: run_plugin_once.py, and future factory/maintenance tools.
"""

import logging
from dataclasses import dataclass, field
from pathlib import Path
from types import ModuleType
from typing import Any, Dict, List, Optional

import importlib.util as _importlib_util

from plugin_spec import PluginSpec
from station_c_validator import validate_plugin_module

__all__ = ["PluginRecord", "PluginRegistry"]

ROOT_DIR = Path(__file__).resolve().parent.parent
PLUGINS_DIR = ROOT_DIR / "plugins"

LOG = logging.getLogger(__name__)


@dataclass
class PluginRecord:
    """
    Lightweight record describing a discovered plugin file.

    Fields:
        slug:
            Plugin slug (file stem).
        path:
            Path to the plugin module on disk.
        is_usable:
            True if import + structural validation succeeded.
        import_error:
            If import or validation failed, this describes why.
        validation_message:
            Soft warning / note from validation (e.g., missing optional metadata).
        meta:
            Lightweight manifest / meta info inferred from the plugin module,
            including derived fields like family_key, is_generic_name when possible.
        _module:
            Cached imported module (only set when is_usable is True).
    """

    slug: str
    path: Path
    is_usable: bool = False

    # If import OR structural validation fails, this describes why.
    import_error: Optional[str] = None

    # Optional note/warning from validation (e.g. missing optional metadata).
    validation_message: Optional[str] = None

    # Lightweight manifest / meta info inferred from the plugin module.
    meta: Dict[str, Any] = field(default_factory=dict)

    # Cached imported module (only set when is_usable is True).
    _module: Optional[ModuleType] = field(default=None, repr=False)


class PluginRegistry:
    """
    Simple in-memory registry of plugin modules.

    Typical usage:

        reg = PluginRegistry()
        reg.refresh()

        # Get a record
        rec = reg.get("saleschurnpredictor")
        if rec and rec.is_usable:
            module = reg.load_module("saleschurnpredictor")

        # Or inspect by family
        families = reg.list_families()
    """

    def __init__(self) -> None:
        self._records: Dict[str, PluginRecord] = {}

    # ------------------------------------------------------------------
    # Discovery
    # ------------------------------------------------------------------

    def refresh(self) -> None:
        """
        Scan the plugins directory, attempt to import each plugin,
        and run basic structural validation.

        A plugin is considered usable if:
        - It imports successfully, AND
        - validate_plugin_module(path) returns ok=True
          (i.e., it exposes a callable invoke(user_id, payload, **kwargs)).
        """
        LOG.info("Refreshing plugin registry from %s", PLUGINS_DIR)
        self._records.clear()

        PLUGINS_DIR.mkdir(parents=True, exist_ok=True)

        for path in PLUGINS_DIR.glob("*.py"):
            if path.name == "__init__.py":
                continue

            slug = path.stem
            rec = PluginRecord(slug=slug, path=path)

            # First, try to import the module.
            try:
                module = self._import_module(slug, path)
            except Exception as exc:  # noqa: BLE001
                msg = f"ImportError: {exc}"
                LOG.warning("Failed to import plugin %r: %s", slug, msg)
                rec.is_usable = False
                rec.import_error = msg
                rec.validation_message = None
                rec._module = None
                self._records[slug] = rec
                continue

            # Next, run structural validation (invoke entrypoint, metadata).
            try:
                ok, reason = validate_plugin_module(path)
            except Exception as exc:  # extremely defensive; validator itself should not raise
                ok = False
                reason = f"Validator raised: {exc}"
                LOG.warning(
                    "Validator raised unexpectedly for plugin %r: %s", slug, reason
                )

            if not ok:
                # Hard failure: plugin is present but structurally unusable.
                LOG.warning(
                    "Plugin %r failed structural validation: %s", slug, reason
                )
                rec.is_usable = False
                rec.import_error = reason or "Plugin failed structural validation."
                rec.validation_message = reason or None
                rec._module = None
            else:
                rec.is_usable = True
                rec.import_error = None
                rec.validation_message = reason or None
                rec._module = module
                rec.meta = self._extract_meta_from_module(module)

            self._records[slug] = rec

        LOG.info(
            "Plugin registry refresh complete: %d usable / %d total",
            len(self.list_usable_plugins()),
            len(self._records),
        )

    def _import_module(self, module_name: str, path: Path) -> ModuleType:
        """Import a module from a specific file path."""
        spec = _importlib_util.spec_from_file_location(module_name, path)
        if spec is None or spec.loader is None:
            raise RuntimeError(f"Could not create module spec for {path}")

        module = _importlib_util.module_from_spec(spec)
        spec.loader.exec_module(module)  # type: ignore[attr-defined]
        return module

    def _extract_meta_from_module(self, module: ModuleType) -> Dict[str, Any]:
        """
        Infer a small manifest-like meta dict from the plugin module.

        Newer plugins (generated by the current template) expose:
            _PLUGIN_MANIFEST: Dict[str, Any]

        If that is present and a dict, we prefer it and lightly
        normalize a few identity fields. Otherwise we fall back to
        individual constants.

        Additionally, we derive a PluginSpec-shaped view to compute:
            - family_key       (category-normalized family grouping)
            - is_generic_name  (whether naming looks factory/generic)
        which can be used by dedupe and naming-improvement steps.
        """
        slug = getattr(module, "_PLUGIN_SLUG", module.__name__.split(".")[-1])
        name = getattr(module, "_PLUGIN_NAME", module.__name__)
        category = getattr(module, "_PLUGIN_CATEGORY", "unknown")
        version = getattr(module, "_PLUGIN_VERSION", "0.0.0")

        manifest = getattr(module, "_PLUGIN_MANIFEST", None)
        if isinstance(manifest, dict):
            meta: Dict[str, Any] = dict(manifest)
            # Ensure core identity fields exist even if the manifest is sparse
            meta.setdefault("slug", slug)
            meta.setdefault("name", name)
            meta.setdefault("category", category)
            meta.setdefault("version", version)
        else:
            # Fallback: build a minimal meta dict from constants
            meta = {
                "slug": slug,
                "name": name,
                "category": category,
                "version": version,
            }

            goal = getattr(module, "_PLUGIN_GOAL", None)
            if goal is not None:
                meta["goal"] = goal

            tags = getattr(module, "_PLUGIN_TAGS", None)
            if tags is not None:
                try:
                    meta["tags"] = list(tags)
                except TypeError:
                    # If _PLUGIN_TAGS is not iterable, ignore it
                    LOG.debug(
                        "Plugin %r has non-iterable _PLUGIN_TAGS; ignoring.", slug
                    )

            # Extended metadata (if present)
            owner_id = getattr(module, "_PLUGIN_OWNER_ID", None)
            if owner_id is not None:
                meta["owner_id"] = owner_id

            capability_type = getattr(module, "_PLUGIN_CAPABILITY_TYPE", None)
            if capability_type is not None:
                meta["capability_type"] = capability_type

            intended_domain = getattr(module, "_PLUGIN_INTENDED_DOMAIN", None)
            if intended_domain is not None:
                meta["intended_domain"] = intended_domain

            use_cases = getattr(module, "_PLUGIN_USE_CASES", None)
            if isinstance(use_cases, (list, tuple)) and use_cases:
                meta["use_cases"] = list(use_cases)

            schema_version = getattr(module, "_PLUGIN_RESULT_SCHEMA_VERSION", None)
            if schema_version is not None:
                meta["schema_version"] = schema_version

        # Derive PluginSpec-style helpers where possible (family_key, generic-name flag)
        try:
            spec_like = PluginSpec.from_manifest(
                {
                    "name": meta.get("name", ""),
                    "slug": meta.get("slug", ""),
                    "goal": meta.get("goal", ""),
                    "category": meta.get("category", "analysis"),
                    "tags": meta.get("tags", []),
                    "version": meta.get("version", "0.1.0"),
                    "capability_type": meta.get("capability_type"),
                    "intended_domain": meta.get("intended_domain"),
                    "owner_id": meta.get("owner_id"),
                    "use_cases": meta.get("use_cases", []),
                    "primary_use_case": meta.get("primary_use_case"),
                    "problem_statement": meta.get("problem_statement"),
                    "primary_inputs": meta.get("primary_inputs"),
                    "primary_outputs": meta.get("primary_outputs"),
                    "constraints": meta.get("constraints"),
                    "example_use_cases": meta.get("example_use_cases", []),
                    "io_contract": meta.get("io_contract"),
                }
            )
            meta.setdefault("family_key", spec_like.family_key)
            meta.setdefault("is_generic_name", spec_like.is_generic_name())
        except Exception as exc:  # pragma: no cover - defensive
            # Derivation is best-effort; never break registry on bad metadata.
            LOG.debug(
                "Failed to derive PluginSpec-style meta for %r: %s", slug, exc
            )

        return meta

    # ------------------------------------------------------------------
    # Accessors
    # ------------------------------------------------------------------

    def list_plugins(self) -> List[PluginRecord]:
        """Return all plugin records (usable and broken)."""
        return list(self._records.values())

    def list_usable_plugins(self) -> List[PluginRecord]:
        """Return only plugins that imported and validated successfully."""
        return [rec for rec in self._records.values() if rec.is_usable]

    def list_families(self) -> Dict[str, List[PluginRecord]]:
        """
        Group usable plugins by their family_key (if available).

        Returns:
            dict: family_key -> list[PluginRecord]
        """
        families: Dict[str, List[PluginRecord]] = {}
        for rec in self.list_usable_plugins():
            family_key = rec.meta.get("family_key") or rec.slug
            families.setdefault(family_key, []).append(rec)
        return families

    def get(self, slug: str) -> Optional[PluginRecord]:
        """Get a PluginRecord by slug, or None if unknown."""
        return self._records.get(slug)

    def load_module(self, slug: str) -> ModuleType:
        """
        Return the imported module for a slug.

        Raises:
            KeyError if not present.
            RuntimeError if present but not usable.
        """
        rec = self._records.get(slug)
        if rec is None:
            raise KeyError(f"Unknown plugin slug: {slug!r}")

        if not rec.is_usable or rec._module is None:
            raise RuntimeError(
                f"Plugin {slug!r} is not usable: {rec.import_error}"
            )

        return rec._module

    def get_spec(self, slug: str) -> Optional[PluginSpec]:
        """
        Convenience: build a PluginSpec view from the stored meta for a slug.

        Returns:
            PluginSpec or None if the slug is unknown or has no usable meta.
        """
        rec = self.get(slug)
        if rec is None or not rec.meta:
            return None

        try:
            return PluginSpec.from_manifest(rec.meta)
        except Exception:
            # Meta may not be fully manifest-shaped; treat as absent.
            return None
