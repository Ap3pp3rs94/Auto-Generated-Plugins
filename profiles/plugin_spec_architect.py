from __future__ import annotations

from typing import Any

from .profile_utils import capability_spec_payload, finalize_profile_result, normalize_payload, user_candidate_text


PROFILE_ID = "plugin_spec_architect_profile"


def run(context: Any, payload: Any, config: dict[str, Any] | None, manifest: dict[str, Any]) -> dict[str, Any]:
    payload_data, warnings = normalize_payload(payload)
    spec = capability_spec_payload(payload_data)
    candidate = user_candidate_text(payload_data)
    name = str(spec.get("name") or candidate or "unnamed capability")
    purpose = str(spec.get("purpose") or payload_data.get("objective") or payload_data.get("description") or "").strip()
    owns = [str(item) for item in spec.get("owns", [])] if isinstance(spec.get("owns"), list) else []
    does_not_own = [str(item) for item in spec.get("does_not_own", [])] if isinstance(spec.get("does_not_own"), list) else []
    required_inputs = [str(item) for item in spec.get("required_inputs", [])] if isinstance(spec.get("required_inputs"), list) else []
    required_detail_keys = [str(item) for item in spec.get("required_detail_keys", [])] if isinstance(spec.get("required_detail_keys"), list) else []
    required_scores = [str(item) for item in spec.get("required_scores", [])] if isinstance(spec.get("required_scores"), list) else []
    forbidden_detail_keys = [str(item) for item in spec.get("forbidden_detail_keys", [])] if isinstance(spec.get("forbidden_detail_keys"), list) else []
    missing = []
    if not candidate and not spec:
        missing.append("candidate capability fields or capability_spec")
    if not purpose:
        missing.append("purpose or objective")

    spec_blueprint = {
        "name": name,
        "family_key": str(spec.get("family_key") or payload_data.get("family_key") or ""),
        "purpose": purpose or "Define the concrete capability purpose before generation.",
        "owns": owns,
        "does_not_own": does_not_own,
        "required_inputs": required_inputs or ["task", "objective"],
        "required_detail_keys": required_detail_keys,
        "required_scores": sorted(set(required_scores + ["confidence", "usefulness"])),
        "forbidden_detail_keys": forbidden_detail_keys,
    }
    uniqueness_checks = [
        {"check": "family_key_boundary", "expected": "family_key is unique or explicitly upgrades an existing canonical capability"},
        {"check": "owned_outputs", "expected": "required_detail_keys prove behavior beyond metadata relabeling"},
        {"check": "does_not_own", "expected": "adjacent capabilities are named and excluded"},
    ]
    capability_boundaries = [
        {"boundary": "owns", "items": owns or ["Add concrete owned behaviors before promotion"]},
        {"boundary": "does_not_own", "items": does_not_own or ["List adjacent capabilities this one must not duplicate"]},
    ]
    prompt_requirements = [
        {"requirement": "capability_spec", "why": "Station B must generate against a declared machine-readable contract"},
        {"requirement": "semantic_probes", "why": "Acceptance must include contrast payloads, not only import success"},
        {"requirement": "promotion_gate", "why": "A good shell with wrong behavior should be repaired or rejected"},
    ]
    confidence = 0.44 + (0.16 if spec else 0.0) + min(0.18, len(required_detail_keys) * 0.03) + min(0.12, len(owns) * 0.02)
    result = {
        "summary": f"CapabilitySpec blueprint prepared for {name}.",
        "primary_insights": [
            {"title": "Spec blueprint", "detail": spec_blueprint},
            {"title": "Boundary checks", "detail": capability_boundaries},
            {"title": "Uniqueness checks", "detail": uniqueness_checks},
        ],
        "recommended_actions": [
            {"action": "Fill missing spec fields", "missing_inputs": missing},
            {"action": "Use blueprint as generation contract", "required_detail_keys": spec_blueprint["required_detail_keys"]},
            {"action": "Attach semantic probes before promotion", "checks": [item["check"] for item in uniqueness_checks]},
        ],
        "scores": {"confidence": round(min(0.94, confidence), 2), "usefulness": 0.9 if spec or candidate else 0.45},
        "details": {
            "spec_blueprint": spec_blueprint,
            "uniqueness_checks": uniqueness_checks,
            "capability_boundaries": capability_boundaries,
            "prompt_requirements": prompt_requirements,
            "missing_inputs": missing,
        },
    }
    return finalize_profile_result(result, profile_id=PROFILE_ID, payload_warnings=warnings, manifest=manifest, payload_data=payload_data)
