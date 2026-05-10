from __future__ import annotations

from typing import Any

from .profile_utils import finalize_profile_result, normalize_payload, user_candidate_text


PROFILE_ID = "plugin_factory_backlog_planner_profile"


def _as_list(value: Any) -> list[Any]:
    if isinstance(value, list):
        return value
    if value in (None, "", {}, ()):
        return []
    return [value]


def run(context: Any, payload: Any, config: dict[str, Any] | None, manifest: dict[str, Any]) -> dict[str, Any]:
    payload_data, warnings = normalize_payload(payload)
    focus = user_candidate_text(payload_data)
    existing_plugins = _as_list(payload_data.get("existing_plugins"))
    quality_failures = _as_list(payload_data.get("quality_failures"))
    constraints = _as_list(payload_data.get("constraints"))
    missing = []
    if not focus:
        missing.append("task, objective, candidate_capability, or capability_spec")

    needs_quality = any("semantic" in str(item).lower() or "shallow" in str(item).lower() for item in quality_failures)
    needs_duplicate_control = any("duplicate" in str(item).lower() or "overlap" in str(item).lower() for item in constraints + quality_failures)
    backlog_items = [
        {
            "slug_hint": "ai_plugin_quality_gate_designer",
            "priority": 1 if needs_quality else 3,
            "why": "tighten promotion gates for generated capabilities",
            "required_outcome": "machine-readable gates and semantic probes",
        },
        {
            "slug_hint": "ai_plugin_duplicate_detector",
            "priority": 1 if needs_duplicate_control else 4,
            "why": "prevent duplicate canonical capabilities",
            "required_outcome": "merge/reject/redesign/generate-new decision",
        },
        {
            "slug_hint": "ai_plugin_repair_strategy_planner",
            "priority": 2,
            "why": "repair good shells with bad semantic behavior",
            "required_outcome": "profile-specific repair plan with acceptance checks",
        },
        {
            "slug_hint": "ai_plugin_logic_blueprint_designer",
            "priority": 2,
            "why": "derive deterministic stages from CapabilitySpec",
            "required_outcome": "implementation stages tied to required details",
        },
    ]
    backlog_items = sorted(backlog_items, key=lambda item: (item["priority"], item["slug_hint"]))
    dependency_order = [
        "spec_architect",
        "logic_blueprint_designer",
        "quality_gate_designer",
        "test_payload_generator",
        "duplicate_detector",
        "repair_strategy_planner",
        "release_packager",
    ]
    priority_rationale = [
        "Quality gates and duplicate control rank first when failures mention shallow or duplicate behavior.",
        "Repair is useful only after the expected profile behavior is explicit.",
        "Release packaging stays last because publishing follows promotion.",
    ]
    result = {
        "summary": "Factory backlog ranked from supplied failures and constraints.",
        "primary_insights": [
            {"title": "Backlog items", "detail": backlog_items},
            {"title": "Dependency order", "detail": dependency_order},
            {"title": "Existing plugin count", "detail": len(existing_plugins)},
        ],
        "recommended_actions": [
            {"action": "Build or repair the top backlog item", "item": backlog_items[0]},
            {"action": "Use dependency order before publishing", "dependency_order": dependency_order},
        ],
        "scores": {
            "confidence": round(min(0.92, 0.44 + 0.08 * bool(focus) + 0.06 * bool(existing_plugins) + 0.04 * len(quality_failures[:4])), 2),
            "usefulness": 0.86 if focus else 0.48,
            "backlog_specificity": round(min(0.94, 0.48 + 0.06 * len(constraints[:5]) + 0.05 * len(quality_failures[:5])), 2),
        },
        "details": {
            "backlog_items": backlog_items,
            "priority_rationale": priority_rationale,
            "dependency_order": dependency_order,
            "next_plugin_specs": [item["slug_hint"] for item in backlog_items],
            "missing_inputs": missing,
        },
    }
    return finalize_profile_result(result, profile_id=PROFILE_ID, payload_warnings=warnings, manifest=manifest, payload_data=payload_data)
