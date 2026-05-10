from __future__ import annotations

from typing import Any, Callable

try:
    from factory.factory_os.logic_profiles import normalize_logic_profile_id as _normalize_os_profile_id
except Exception:  # pragma: no cover
    try:
        from factory_os.logic_profiles import normalize_logic_profile_id as _normalize_os_profile_id
    except Exception:  # pragma: no cover
        _normalize_os_profile_id = None  # type: ignore[assignment]

from . import logic_blueprint_designer, overlap_checker, quality_gate_designer, test_payload_generator
from .profile_utils import finalize_profile_result, normalize_payload


ProfileRunner = Callable[[Any, Any, dict[str, Any] | None, dict[str, Any]], dict[str, Any]]


_PROFILE_ALIASES: dict[str, str] = {
    "plugin_quality_gate_designer_profile": quality_gate_designer.PROFILE_ID,
    "quality_gate_designer_profile": quality_gate_designer.PROFILE_ID,
    "ai_plugin_quality_gate_designer": quality_gate_designer.PROFILE_ID,
    "plugin_logic_blueprint_designer_profile": logic_blueprint_designer.PROFILE_ID,
    "logic_blueprint_designer_profile": logic_blueprint_designer.PROFILE_ID,
    "ai_plugin_logic_blueprint_designer": logic_blueprint_designer.PROFILE_ID,
    "plugin_test_payload_generator_profile": test_payload_generator.PROFILE_ID,
    "test_payload_generator_profile": test_payload_generator.PROFILE_ID,
    "ai_plugin_test_payload_generator": test_payload_generator.PROFILE_ID,
    "capability_overlap_checker_profile": overlap_checker.PROFILE_ID,
    "continuous_capability_overlap_checker_profile": overlap_checker.PROFILE_ID,
    "plugin_duplicate_detector_profile": overlap_checker.PROFILE_ID,
    "capability_duplicate_detector": overlap_checker.PROFILE_ID,
    "ai_capability_overlap_checker": overlap_checker.PROFILE_ID,
    "ai_plugin_duplicate_detector": overlap_checker.PROFILE_ID,
}


_PROFILE_RUNNERS: dict[str, ProfileRunner] = {
    quality_gate_designer.PROFILE_ID: quality_gate_designer.run,
    logic_blueprint_designer.PROFILE_ID: logic_blueprint_designer.run,
    test_payload_generator.PROFILE_ID: test_payload_generator.run,
    overlap_checker.PROFILE_ID: overlap_checker.run,
}


def resolve_logic_profile(profile_id_or_alias: str | None) -> str | None:
    """Resolve a profile id or legacy alias to the canonical dispatch id."""
    if not profile_id_or_alias:
        return None
    raw = str(profile_id_or_alias).strip()
    if not raw:
        return None
    if raw in _PROFILE_ALIASES:
        return _PROFILE_ALIASES[raw]
    if callable(_normalize_os_profile_id):
        normalized = _normalize_os_profile_id(raw)
        if normalized:
            return _PROFILE_ALIASES.get(normalized, normalized)
    return raw if raw in _PROFILE_RUNNERS else None


def run_profile_logic(
    profile_id: str | None,
    context: Any,
    payload: Any,
    config: dict[str, Any] | None,
    manifest: dict[str, Any],
) -> dict[str, Any]:
    """Run the canonical profile module for a generated capability."""
    resolved = resolve_logic_profile(profile_id)
    if resolved and resolved in _PROFILE_RUNNERS:
        return _PROFILE_RUNNERS[resolved](context, payload, config, manifest)

    payload_data, warnings = normalize_payload(payload)
    requested = str(profile_id or "")
    result = {
        "summary": "No registered profile runner matched this capability.",
        "primary_insights": [
            {"title": "Requested profile", "detail": requested or "missing"},
        ],
        "recommended_actions": [
            {"action": "Register a profile runner before promoting this capability."},
        ],
        "scores": {"confidence": 0.0, "usefulness": 0.2},
        "details": {
            "missing_inputs": ["registered logic profile"],
            "requested_profile_id": requested,
            "payload_keys": sorted(payload_data.keys()),
        },
    }
    return finalize_profile_result(
        result,
        profile_id=requested or "unregistered_profile",
        payload_warnings=warnings,
        manifest=manifest,
    )
