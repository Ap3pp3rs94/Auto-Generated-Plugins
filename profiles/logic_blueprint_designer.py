from __future__ import annotations

from typing import Any

from .profile_utils import capability_spec_payload, finalize_profile_result, normalize_payload, user_candidate_text


PROFILE_ID = "plugin_logic_blueprint_designer_profile"


def run(context: Any, payload: Any, config: dict[str, Any] | None, manifest: dict[str, Any]) -> dict[str, Any]:
    payload_data, warnings = normalize_payload(payload)
    spec = capability_spec_payload(payload_data)
    missing = [] if spec else ["capability_spec or candidate capability fields"]
    name = str(spec.get("name") or user_candidate_text(payload_data) or "unnamed capability")
    owns = [str(item) for item in spec.get("owns", [])] if isinstance(spec.get("owns"), list) else []
    required_inputs = [str(item) for item in spec.get("required_inputs", [])] if isinstance(spec.get("required_inputs"), list) else []
    required_detail_keys = [str(item) for item in spec.get("required_detail_keys", [])] if isinstance(spec.get("required_detail_keys"), list) else []
    forbidden = [str(item) for item in spec.get("forbidden_detail_keys", [])] if isinstance(spec.get("forbidden_detail_keys"), list) else []
    stages = [
        {"stage": "normalize_inputs", "uses": required_inputs or ["payload"], "output": "normalized_payload"},
        {"stage": "extract_owned_signals", "uses": owns or [name], "output": "capability_signals"},
        {"stage": "construct_machine_details", "uses": required_detail_keys or ["summary", "recommended_actions"], "output": "details"},
        {"stage": "guard_forbidden_behavior", "uses": forbidden or ["metadata-only relabeling"], "output": "rejection_findings"},
        {"stage": "score_and_explain", "uses": ["confidence", "usefulness"], "output": "scores"},
    ]
    data_flow = {"inputs": required_inputs, "stages": [stage["stage"] for stage in stages], "outputs": required_detail_keys}
    result = {
        "summary": f"Logic blueprint derived for {name}.",
        "primary_insights": [
            {"title": "Blueprint stages", "detail": stages},
            {"title": "Data flow", "detail": data_flow},
        ],
        "recommended_actions": [
            {"action": "Implement stages in order", "stages": [stage["stage"] for stage in stages]},
            {"action": "Use required detail keys as acceptance checks", "required_detail_keys": required_detail_keys},
        ],
        "scores": {"confidence": 0.86 if spec else 0.42, "usefulness": 0.9 if spec else 0.5, "stage_count": len(stages)},
        "details": {
            "logic_blueprint": stages,
            "deterministic_rules": ["No external calls", "No file mutation", "Scores derive from observed signals"],
            "data_flow": data_flow,
            "failure_modes": ["metadata-only relabeling", "missing detail keys", "constant outputs across probes"],
            "missing_inputs": missing,
        },
    }
    return finalize_profile_result(result, profile_id=PROFILE_ID, payload_warnings=warnings, manifest=manifest, payload_data=payload_data)

