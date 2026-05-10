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
        {"stage": "validate_required_inputs", "uses": required_inputs or ["capability intent"], "output": "missing_inputs"},
        {"stage": "extract_owned_signals", "uses": owns or [name], "output": "capability_signals"},
        {"stage": "derive_decision_fields", "uses": owns or required_detail_keys or [name], "output": "machine_decisions"},
        {"stage": "construct_machine_details", "uses": required_detail_keys or ["summary", "recommended_actions"], "output": "details"},
        {"stage": "guard_forbidden_behavior", "uses": forbidden or ["metadata-only relabeling"], "output": "rejection_findings"},
        {"stage": "run_semantic_contrast", "uses": ["duplicate-heavy probe", "unique probe", "missing-input probe"], "output": "semantic_findings"},
        {"stage": "score_and_explain", "uses": ["confidence", "usefulness"], "output": "scores"},
    ]
    output_constructors = [
        {
            "detail_key": key,
            "construction_rule": f"Derive {key} from payload signals, not plugin metadata.",
            "empty_payload_behavior": "leave empty or mark missing; do not use the plugin goal as evidence",
        }
        for key in (required_detail_keys or ["summary", "recommended_actions", "scores"])
    ]
    scoring_formula = {
        "confidence": "increase with required input coverage and contrast-probe agreement",
        "usefulness": "increase when machine-readable detail keys and next actions are populated",
        "risk": "increase when missing inputs or forbidden behaviors appear",
    }
    semantic_probes = [
        {"probe": "empty_payload", "expected": "missing_inputs and blockers are populated"},
        {"probe": "useful_payload", "expected": "required detail keys are populated from supplied values"},
        {"probe": "contrast_payloads", "expected": "details and scores change across different payload meanings"},
    ]
    data_flow = {
        "inputs": required_inputs,
        "stages": [stage["stage"] for stage in stages],
        "outputs": required_detail_keys,
        "forbidden_outputs": forbidden,
    }
    result = {
        "summary": f"Logic blueprint derived for {name}.",
        "primary_insights": [
            {"title": "Blueprint stages", "detail": stages},
            {"title": "Data flow", "detail": data_flow},
            {"title": "Output constructors", "detail": output_constructors},
            {"title": "Semantic probes", "detail": semantic_probes},
        ],
        "recommended_actions": [
            {"action": "Implement stages in order", "stages": [stage["stage"] for stage in stages]},
            {"action": "Use required detail keys as acceptance checks", "required_detail_keys": required_detail_keys},
            {"action": "Wire semantic probes before promotion", "semantic_probes": semantic_probes},
            {"action": "Reject forbidden behavior", "forbidden_detail_keys": forbidden},
        ],
        "scores": {"confidence": 0.93 if spec else 0.42, "usefulness": 0.94 if spec else 0.5, "stage_count": len(stages)},
        "details": {
            "logic_blueprint": stages,
            "deterministic_rules": [
                "No external calls",
                "No file mutation",
                "Scores derive from observed signals",
                "Do not use the plugin goal as user-provided input",
                "No metadata-only relabeling counts as behavior",
            ],
            "data_flow": data_flow,
            "failure_modes": ["metadata-only relabeling", "missing detail keys", "constant outputs across probes"],
            "output_constructors": output_constructors,
            "scoring_formula": scoring_formula,
            "semantic_probes": semantic_probes,
            "forbidden_behavior": forbidden,
            "missing_inputs": missing,
        },
    }
    return finalize_profile_result(result, profile_id=PROFILE_ID, payload_warnings=warnings, manifest=manifest, payload_data=payload_data)
