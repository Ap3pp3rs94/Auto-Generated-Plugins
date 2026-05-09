from __future__ import annotations

import asyncio
import ast
import importlib.util
import inspect
import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

from plugin_spec import PluginSpec
from registry import (
    has_duplicate_capability,
    entry_exists_for_slug,
    plugin_path_for_spec,
    upsert_entry,
    RegistryEntry,
)

# Optional learning logger – safe no-op if not present yet
try:
    from learning.collector import log_plugin_event  # type: ignore
except ImportError:  # learning subsystem not wired yet
    def log_plugin_event(*args: Any, **kwargs: Any) -> None:
        return


# ======================================================================
# Core data structures
# ======================================================================


@dataclass
class ValidationResult:
    """
    Aggregated validation outcome for a single plugin.

    - ok        : True if there are no errors (warnings are allowed).
    - errors    : Hard failures. Plugin must NOT enter the library.
    - warnings  : Soft issues. Surface to operator / logs, but plugin may pass.
    - infos     : Non-critical diagnostic messages.
    """

    ok: bool
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    infos: List[str] = field(default_factory=list)

    def add_error(self, msg: str) -> None:
        self.errors.append(str(msg))

    def add_warning(self, msg: str) -> None:
        self.warnings.append(str(msg))

    def add_info(self, msg: str) -> None:
        self.infos.append(str(msg))

    @property
    def has_errors(self) -> bool:
        return bool(self.errors)

    @property
    def has_warnings(self) -> bool:
        return bool(self.warnings)

    @property
    def error_report(self) -> str:
        """
        Human-friendly, multi-line report of errors + warnings + infos.
        """
        if not self.errors and not self.warnings and not self.infos:
            return "No errors, warnings, or infos."

        lines: List[str] = []
        if self.errors:
            lines.append("Errors:")
            lines.extend(f"- {e}" for e in self.errors)
        if self.warnings:
            lines.append("Warnings:")
            lines.extend(f"- {w}" for w in self.warnings)
        if self.infos:
            lines.append("Info:")
            lines.extend(f"- {i}" for i in self.infos)
        return "\n".join(lines)


class StationCValidatorError(Exception):
    """Raised when Station C encounters a fatal issue during validation."""


# ======================================================================
# Low-level helpers
# ======================================================================


def _load_module_from_path(module_name: str, path: Path):
    """
    Dynamically load a module from a file path without requiring it to be
    part of a package. This is used for contract + runtime inspection.
    """
    spec = importlib.util.spec_from_file_location(module_name, str(path))
    if spec is None or spec.loader is None:
        raise StationCValidatorError(f"Could not create import spec for {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)  # type: ignore[attr-defined]
    return module


def _safe_read_source(path: Path, result: ValidationResult) -> Optional[str]:
    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError:
        result.add_error(f"Plugin file not found: {path}")
    except UnicodeDecodeError:
        result.add_error(f"Plugin file is not valid UTF-8: {path}")
    return None


# ======================================================================
# Static checks (syntax + AST safety)
# ======================================================================


def validate_syntax(path: Path, result: ValidationResult) -> Optional[str]:
    """
    Step 1: basic syntax validation via compile().

    Returns the source string on success, or None on failure.
    """
    source = _safe_read_source(path, result)
    if source is None:
        return None

    try:
        compile(source, str(path), "exec")
    except SyntaxError as e:
        result.add_error(
            f"Syntax error in plugin file {path}:\n"
            f"  {e.msg} (line {e.lineno}, column {e.offset})"
        )
        return None

    return source


def _collect_ast_features(tree: ast.AST) -> Tuple[Set[str], Set[str], Set[str]]:
    """
    Scan AST and collect:
    - imported_modules: top-level modules imported
    - dangerous_calls: names of "obviously dangerous" builtins/functions
    - attribute_calls: attribute call targets like 'os.system', 'subprocess.run'
    """
    imported_modules: Set[str] = set()
    dangerous_calls: Set[str] = set()
    attribute_calls: Set[str] = set()

    dangerous_builtin_names = {"eval", "exec", "__import__"}
    # Attribute patterns considered "dangerous-ish". We'll match by prefix.
    dangerous_attrs_prefixes = {
        "os.system",
        "os.popen",
        "subprocess.run",
        "subprocess.Popen",
        "subprocess.call",
        "subprocess.check_output",
    }

    class Visitor(ast.NodeVisitor):
        def visit_Import(self, node: ast.Import) -> None:
            for alias in node.names:
                if alias.name:
                    imported_modules.add(alias.name.split(".")[0])
            self.generic_visit(node)

        def visit_ImportFrom(self, node: ast.ImportFrom) -> None:
            if node.module:
                imported_modules.add(node.module.split(".")[0])
            self.generic_visit(node)

        def visit_Call(self, node: ast.Call) -> None:
            # direct builtin call like eval(...), exec(...)
            if isinstance(node.func, ast.Name):
                if node.func.id in dangerous_builtin_names:
                    dangerous_calls.add(node.func.id)

            # attribute call like os.system(...), subprocess.run(...)
            elif isinstance(node.func, ast.Attribute):
                parts: List[str] = []
                attr = node.func
                while isinstance(attr, ast.Attribute):
                    parts.append(attr.attr)
                    attr = attr.value
                if isinstance(attr, ast.Name):
                    parts.append(attr.id)
                full = ".".join(reversed(parts))  # e.g. "os.system"
                attribute_calls.add(full)

            self.generic_visit(node)

    Visitor().visit(tree)

    # Filter attribute_calls to those that start with known dangerous prefixes
    filtered_attr_calls: Set[str] = set()
    for a in attribute_calls:
        if any(a.startswith(prefix) for prefix in dangerous_attrs_prefixes):
            filtered_attr_calls.add(a)

    return imported_modules, dangerous_calls, filtered_attr_calls


def validate_static_safety(
    source: str,
    spec: PluginSpec,
    result: ValidationResult,
) -> None:
    """
    Perform static inspection (AST) for obviously dangerous patterns.
    """
    try:
        tree = ast.parse(source)
    except SyntaxError:
        # Syntax validation will have already logged this as an error.
        return

    imported_modules, dangerous_calls, dangerous_attr_calls = _collect_ast_features(
        tree
    )

    cat = (spec.category or "").lower()

    # 1) Hard fail: eval/exec/__import__
    if dangerous_calls:
        for name in sorted(dangerous_calls):
            result.add_error(
                f"Forbidden builtin call detected: {name}(...). "
                "Plugins must not use eval/exec/__import__."
            )

    # 2) Import-level checks
    risky_imports = {
        "os",
        "sys",
        "subprocess",
        "socket",
        "requests",
        "urllib",
        "http",
        "ftplib",
        "paramiko",
        "shutil",
    }

    risky_found = imported_modules & risky_imports
    if risky_found:
        if cat in ("system_automation", "integration"):
            result.add_warning(
                "High-risk imports detected (system/network/filesystem): "
                f"{sorted(risky_found)}. "
                "Allowed for system_automation/integration, but use with care."
            )
        else:
            result.add_warning(
                "High-risk imports detected in non-automation plugin: "
                f"{sorted(risky_found)}. "
                "Consider restricting side effects or moving this logic "
                "to a dedicated system_automation plugin."
            )

    # 3) Dangerous attribute calls (os.system, subprocess.*)
    if dangerous_attr_calls:
        if cat in ("system_automation", "integration"):
            for call in sorted(dangerous_attr_calls):
                result.add_warning(
                    f"Potentially dangerous call detected: {call}(...). "
                    "This is allowed but should be wrapped with robust error "
                    "handling and security considerations."
                )
        else:
            for call in sorted(dangerous_attr_calls):
                result.add_error(
                    f"Disallowed call {call}(...) in non-automation plugin. "
                    "Shell/process spawning is restricted to system_automation/integration."
                )


# ======================================================================
# Contract checks: SkillContext + invoke
# ======================================================================


def validate_contract(
    path: Path,
    spec: PluginSpec,
    result: ValidationResult,
) -> Optional[Any]:
    """
    Validate basic contract directly from the plugin file path.
    """
    if result.has_errors:
        return None

    try:
        module = _load_module_from_path(f"francis_plugin_{spec.slug}", path)
    except Exception as e:
        result.add_error(f"Failed to import plugin module: {e}")
        return None

    # SkillContext existence
    if not hasattr(module, "SkillContext"):
        result.add_error("Plugin is missing 'SkillContext' class.")
    else:
        cls = getattr(module, "SkillContext")
        if not inspect.isclass(cls):
            result.add_error("'SkillContext' is not a class.")

    # invoke existence
    if not hasattr(module, "invoke"):
        result.add_error("Plugin is missing 'invoke' function.")
        return module

    invoke = getattr(module, "invoke")

    if not inspect.iscoroutinefunction(invoke):
        result.add_error("'invoke' must be defined as an async function.")

    # Check signature: (user_id: str, payload: Dict[str, Any], **kwargs)
    sig = inspect.signature(invoke)
    params = list(sig.parameters.values())
    if len(params) < 2:
        result.add_error("invoke() must accept at least (user_id, payload, **kwargs).")
    else:
        if params[0].name != "user_id":
            result.add_error("First parameter of invoke() must be 'user_id'.")
        if params[1].name != "payload":
            result.add_error("Second parameter of invoke() must be 'payload'.")

        user_param = params[0]
        payload_param = params[1]

        if (
            user_param.annotation not in (inspect._empty, str)
            or payload_param.annotation not in (inspect._empty, Dict, dict)
        ):
            result.add_warning(
                "invoke() parameters should be typed as "
                "(user_id: str, payload: Dict[str, Any], **kwargs)."
            )

    return module


def validate_contract_on_module(
    module: Any,
    spec: PluginSpec,
    result: ValidationResult,
) -> None:
    """
    Same contract checks as validate_contract(), but starting from
    an already-imported module (factory uses this).
    """
    if result.has_errors:
        return

    if not hasattr(module, "SkillContext"):
        result.add_error("Plugin is missing 'SkillContext' class.")
    else:
        cls = getattr(module, "SkillContext")
        if not inspect.isclass(cls):
            result.add_error("'SkillContext' is not a class.")

    if not hasattr(module, "invoke"):
        result.add_error("Plugin is missing 'invoke' function.")
        return

    invoke = getattr(module, "invoke")
    if not inspect.iscoroutinefunction(invoke):
        result.add_error("'invoke' must be defined as an async function.")
        return

    sig = inspect.signature(invoke)
    params = list(sig.parameters.values())
    if len(params) < 2:
        result.add_error("invoke() must accept at least (user_id, payload, **kwargs).")
        return

    if params[0].name != "user_id":
        result.add_error("First parameter of invoke() must be 'user_id'.")
    if params[1].name != "payload":
        result.add_error("Second parameter of invoke() must be 'payload'.")

    user_param = params[0]
    payload_param = params[1]
    if (
        user_param.annotation not in (inspect._empty, str)
        or payload_param.annotation not in (inspect._empty, Dict, dict)
    ):
        result.add_warning(
            "invoke() parameters should be typed as "
            "(user_id: str, payload: Dict[str, Any], **kwargs)."
        )


# ======================================================================
# Runtime validation
# ======================================================================


def _build_test_payloads(spec: PluginSpec) -> List[Tuple[str, Dict[str, Any]]]:
    """
    Generate category-aware test payloads to probe core behavior.
    """
    test_payloads: List[Tuple[str, Dict[str, Any]]] = []

    # Always: health ping
    test_payloads.append(("health_check", {"ping": True}))

    cat = (spec.category or "").lower()
    goal_blob = f"{spec.name} {spec.goal} {' '.join(spec.tags)}".lower()

    if cat in ("data", "utility") or any(
        kw in goal_blob for kw in ("profile", "summary", "analy", "insight")
    ):
        test_payloads.append(
            (
                "data_sample",
                {
                    "data": [
                        {"value": 1, "group": "A"},
                        {"value": 2, "group": "A"},
                        {"value": 10, "group": "B"},
                        {"value": 20, "group": "B"},
                    ],
                    "notes": "basic distribution check",
                },
            )
        )

    if cat in ("integration", "system_automation") or "entity" in goal_blob:
        test_payloads.append(
            (
                "entities_sample",
                {
                    "entities": [
                        {
                            "id": "e1",
                            "name": "Acme Corp",
                            "aliases": ["ACME CORPORATION"],
                            "source": "crm",
                        },
                        {
                            "id": "e2",
                            "name": "ACME CORPORATION",
                            "aliases": ["Acme Corp"],
                            "source": "billing",
                        },
                    ],
                    "strategy": "merge_by_name_and_alias",
                },
            )
        )

    if len(test_payloads) == 1:
        test_payloads.append(
            (
                "generic_payload",
                {"data": [1, 2, 3], "note": "generic runtime sanity payload"},
            )
        )

    return test_payloads


async def validate_runtime(
    module: Any,
    spec: PluginSpec,
    result: ValidationResult,
    *,
    timeout_seconds: float = 5.0,
) -> None:
    """
    Strengthened runtime test for production validation.
    """
    if result.has_errors:
        return

    invoke = getattr(module, "invoke", None)
    if invoke is None or not inspect.iscoroutinefunction(invoke):
        return

    test_payloads = _build_test_payloads(spec)

    for label, payload in test_payloads:
        try:
            output = await asyncio.wait_for(
                invoke("station-c-test", payload),
                timeout=timeout_seconds,
            )
        except asyncio.TimeoutError:
            result.add_error(
                f"Runtime timeout when calling invoke() with payload '{label}': "
                f"exceeded {timeout_seconds} seconds."
            )
            return
        except Exception as e:
            result.add_error(
                f"Runtime error when calling invoke() with payload '{label}': {e}"
            )
            return

        if not isinstance(output, dict):
            result.add_error(
                f"invoke() must return a dict (payload '{label}'); got {type(output)}"
            )
            return

        required_keys = {"status", "output", "error", "meta"}
        missing = required_keys - set(output.keys())
        if missing:
            result.add_error(
                f"invoke() return dict is missing required keys {sorted(missing)} "
                f"for payload '{label}'."
            )
            return

        status = output.get("status")
        if status != "succeeded":
            result.add_error(
                f"invoke()['status'] must be 'succeeded' for payload '{label}'; "
                f"got {status!r}."
            )
            return

        meta = output.get("meta", {})
        if not isinstance(meta, dict):
            result.add_error(
                f"invoke()['meta'] must be a dict (payload '{label}'); "
                f"got {type(meta)}."
            )
            return

        err_field = output.get("error")
        if err_field not in (None, "", {}):
            result.add_error(
                f"invoke()['error'] must be empty/None when status='succeeded' "
                f"(payload '{label}'); got {err_field!r}."
            )
            return

        out_payload = output.get("output")
        if isinstance(out_payload, dict):
            internal_err = out_payload.get("error") or out_payload.get(
                "exception_type"
            )
            if internal_err:
                result.add_error(
                    f"Plugin core logic reported error for payload '{label}': "
                    f"{out_payload.get('error')!r} / "
                    f"{out_payload.get('exception_type')!r}"
                )
                return

        try:
            json.dumps(output.get("output"))
        except TypeError as e:
            result.add_error(
                f"invoke()['output'] must be JSON-serializable for payload "
                f"'{label}'; got non-serializable value: {e}"
            )
            return

        result.add_info(f"Runtime check passed for payload '{label}'.")


# ======================================================================
# Duplicate checks
# ======================================================================


def validate_duplicates_hard(spec: PluginSpec, result: ValidationResult) -> None:
    if has_duplicate_capability(spec) or entry_exists_for_slug(spec.slug):
        result.add_error(
            "Plugin appears to be a duplicate or near-duplicate of an existing "
            "capability (slug/name/goal/tags collision)."
        )


def validate_duplicates_soft(spec: PluginSpec, result: ValidationResult) -> None:
    if has_duplicate_capability(spec) or entry_exists_for_slug(spec.slug):
        result.add_warning(
            "Plugin appears to be a duplicate or near-duplicate of an existing "
            "capability (slug/name/goal/tags collision). "
            "Treating as warning for factory pipeline."
        )


# ======================================================================
# Factory entrypoint: module already imported
# ======================================================================


async def validate_plugin_module(
    module: Any,
    spec: PluginSpec,
    run_id: Optional[str] = None,
) -> ValidationResult:
    """
    Station C entrypoint for the factory runner.
    """
    result = ValidationResult(ok=False)

    validate_contract_on_module(module, spec, result)
    await validate_runtime(module, spec, result)
    validate_duplicates_soft(spec, result)

    result.ok = not result.errors

    # Log validation for learning
    try:
        code_path = plugin_path_for_spec(spec)
        status = "success" if result.ok else "failure"
        log_plugin_event(
            spec=spec,
            status=status,
            code_path=code_path,
            validation_result=result,
            user_id="austin",
            run_id=run_id or "station-c-module",
            extra={
                "source": "station_c_validator.validate_plugin_module",
            },
        )
    except Exception:
        # Never let logging break validation
        pass

    return result


# ======================================================================
# Full path-based validation (manual / CLI / demo)
# ======================================================================


async def validate_plugin(
    spec: PluginSpec,
    *,
    update_registry_on_success: bool = True,
    skip_duplicate_check: bool = False,
    skip_runtime_check: bool = False,
    run_id: Optional[str] = None,
) -> ValidationResult:
    """
    Full Station C validation when starting from a spec/file path.
    """
    result = ValidationResult(ok=False)
    path = plugin_path_for_spec(spec)

    source = validate_syntax(path, result)

    if source is not None:
        validate_static_safety(source, spec, result)

    module = None
    if not result.has_errors:
        module = validate_contract(path, spec, result)

    if module is not None and not skip_runtime_check:
        await validate_runtime(module, spec, result)

    if not skip_duplicate_check:
        validate_duplicates_hard(spec, result)

    result.ok = not result.errors

    # Update registry on success
    if result.ok and update_registry_on_success:
        entry = RegistryEntry.from_spec(spec, path=path, runtime_hints={})
        upsert_entry(entry)
        result.add_info("Registry updated with validated plugin entry.")

    # Log validation for learning
    try:
        status = "success" if result.ok else "failure"
        log_plugin_event(
            spec=spec,
            status=status,
            code_path=path,
            validation_result=result,
            user_id="austin",
            run_id=run_id or "station-c-path",
            extra={
                "source": "station_c_validator.validate_plugin",
                "update_registry_on_success": update_registry_on_success,
            },
        )
    except Exception:
        pass

    return result


# ======================================================================
# Demo / CLI helper
# ======================================================================


async def station_c_demo() -> None:
    spec = PluginSpec.new(
        name="Demo Plugin",
        goal="Demonstrate Station C",
        category="utility",
        tags=["demo"],
    )

    print("Station C: Validating plugin for:", spec.slug)
    result = await validate_plugin(
        spec,
        update_registry_on_success=False,
        skip_duplicate_check=True,
        skip_runtime_check=True,
        run_id="station-c-demo",
    )

    print("\nValidation OK:", result.ok)
    print("\nDetailed report:")
    print(result.error_report)


if __name__ == "__main__":
    asyncio.run(station_c_demo())
