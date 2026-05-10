from __future__ import annotations

from typing import Any

from .profile_utils import capability_spec_payload, finalize_profile_result, normalize_payload, user_candidate_text


PROFILE_ID = "plugin_quality_gate_designer_profile"


def run(context: Any, payload: Any, config: dict[str, Any] | None, manifest: dict[str, Any]) -> dict[str, Any]:
    payload_data, warnings = normalize_payload(payload)
    spec = capability_spec_payload(payload_data)
    missing = []
    if not spec:
        missing.append("capability_spec or candidate capability fields")
    name = str(spec.get("name") or user_candidate_text(payload_data) or "unnamed capability")
    required_detail_keys = [str(item) for item in spec.get("required_detail_keys", [])] if isinstance(spec.get("required_detail_keys"), list) else []
    required_scores = [str(item) for item in spec.get("required_scores", [])] if isinstance(spec.get("required_scores"), list) else ["confidence", "usefulness"]
    forbidden_detail_keys = [str(item) for item in spec.get("forbidden_detail_keys", [])] if isinstance(spec.get("forbidden_detail_keys"), list) else []
    owns = [str(item) for item in spec.get("owns", [])] if isinstance(spec.get("owns"), list) else []

    quality_gates = [
        {"gate_id": "station_c_envelope", "type": "structural", "required": ["async invoke", "status/output/error/meta"], "hard_fail": True},
        {"gate_id": "required_detail_keys", "type": "schema", "required": required_detail_keys, "hard_fail": True},
        {"gate_id": "required_scores", "type": "schema", "required": sorted(set(required_scores + ["confidence", "usefulness"])), "hard_fail": True},
        {"gate_id": "forbidden_detail_keys", "type": "semantic", "forbidden": forbidden_detail_keys, "hard_fail": bool(forbidden_detail_keys)},
        {"gate_id": "semantic_contrast", "type": "behavior", "required": ["different decisions for duplicate vs unique probes"], "hard_fail": True},
    ]
    semantic_probes = [
        {"probe_id": "empty_payload", "payload": {}, "expect": {"missing_inputs": True, "blockers": True}},
        {"probe_id": "capability_owned_behavior", "payload": {"capability_spec": spec, "task": name}, "expect": {"detail_keys": required_detail_keys[:8]}},
        {"probe_id": "forbidden_behavior_guard", "payload": {"capability_spec": spec, "candidate_outputs": forbidden_detail_keys}, "expect": {"forbidden_absent": forbidden_detail_keys}},
    ]
    rejection_rules = [
        {"rule_id": "metadata_only_relabel", "reject_when": "summary and actions only rename the capability without using payload values"},
        {"rule_id": "missing_machine_keys", "reject_when": "required detail keys or required scores are absent"},
        {"rule_id": "forbidden_generic_fields", "reject_when": "forbidden detail keys appear in output"},
    ]
    pass_criteria = [
        {"criterion": "all_hard_gates_pass", "threshold": 1.0},
        {"criterion": "semantic_probe_divergence", "threshold": 0.35},
        {"criterion": "required_schema_coverage", "threshold": 1.0},
    ]
    confidence = 0.45 + min(0.25, len(required_detail_keys) * 0.03) + min(0.12, len(owns) * 0.02)
    result = {
        "summary": f"Quality gates designed for {name}.",
        "primary_insights": [
            {"title": "Hard gates", "detail": quality_gates},
            {"title": "Semantic probes", "detail": semantic_probes},
            {"title": "Rejection rules", "detail": rejection_rules},
        ],
        "recommended_actions": [
            {"action": "Apply hard gates before promotion", "gates": [gate["gate_id"] for gate in quality_gates if gate["hard_fail"]]},
            {"action": "Run semantic probes", "probes": [probe["probe_id"] for probe in semantic_probes]},
        ],
        "scores": {"confidence": round(min(0.94, confidence), 2), "usefulness": 0.9, "schema_coverage": 1.0 if required_detail_keys else 0.55},
        "details": {
            "quality_gates": quality_gates,
            "rejection_rules": rejection_rules,
            "semantic_probes": semantic_probes,
            "pass_criteria": pass_criteria,
            "missing_inputs": missing,
        },
    }
    return finalize_profile_result(result, profile_id=PROFILE_ID, payload_warnings=warnings, manifest=manifest, payload_data=payload_data)

