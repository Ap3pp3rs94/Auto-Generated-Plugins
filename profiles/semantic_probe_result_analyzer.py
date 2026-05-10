from __future__ import annotations

from typing import Any

from .profile_utils import finalize_profile_result, normalize_payload, user_candidate_text


PROFILE_ID = "semantic_probe_result_analyzer_profile"


def _as_list(value: Any) -> list[Any]:
    if isinstance(value, list):
        return value
    if value in (None, "", {}, ()):
        return []
    return [value]


def run(context: Any, payload: Any, config: dict[str, Any] | None, manifest: dict[str, Any]) -> dict[str, Any]:
    payload_data, warnings = normalize_payload(payload)
    target = user_candidate_text(payload_data)
    probe_results = _as_list(payload_data.get("probe_results") or payload_data.get("semantic_results"))
    validation_findings = _as_list(payload_data.get("validation_findings"))
    missing = []
    if not target:
        missing.append("plugin_name, slug, task, objective, or capability_spec")
    if not probe_results and not validation_findings:
        missing.append("probe_results or validation_findings")

    probe_failures = []
    contrast_findings = []
    repair_targets = []
    for item in probe_results + validation_findings:
        text = str(item)
        lower = text.lower()
        failed = any(term in lower for term in ["fail", "error", "blocker", "mismatch", "missing", "forbidden"])
        if failed:
            probe_failures.append({"evidence": text[:260]})
        if any(term in lower for term in ["same", "constant", "similar", "no difference", "shallow"]):
            contrast_findings.append({"evidence": text[:260], "issue": "semantic contrast too weak"})
        if "missing" in lower and "detail" in lower:
            repair_targets.append({"target": "required_detail_keys", "evidence": text[:200]})
        if "profile" in lower or "routing" in lower:
            repair_targets.append({"target": "logic_profile_routing", "evidence": text[:200]})
        if "forbidden" in lower or "backlog" in lower:
            repair_targets.append({"target": "forbidden_behavior_guard", "evidence": text[:200]})

    if not repair_targets and probe_failures:
        repair_targets.append({"target": "semantic_contract", "evidence": "Probe failures need capability-specific repair."})
    if not probe_failures and not contrast_findings and probe_results:
        promotion_recommendation = "promote"
    elif repair_targets:
        promotion_recommendation = "repair"
    else:
        promotion_recommendation = "insufficient_evidence"

    result = {
        "summary": f"Semantic probe analysis recommends {promotion_recommendation} for {target or 'unidentified capability'}.",
        "primary_insights": [
            {"title": "Probe failures", "detail": probe_failures or "No probe failures supplied."},
            {"title": "Contrast findings", "detail": contrast_findings or "No weak contrast evidence supplied."},
            {"title": "Repair targets", "detail": repair_targets},
        ],
        "recommended_actions": [
            {"action": "Apply promotion recommendation", "decision": promotion_recommendation},
            {"action": "Repair listed targets before retry", "targets": repair_targets},
        ],
        "scores": {
            "confidence": round(min(0.92, 0.34 + 0.08 * len(probe_results[:5]) + 0.08 * len(validation_findings[:5])), 2),
            "usefulness": 0.88 if probe_results or validation_findings else 0.42,
            "failure_density": round(len(probe_failures) / max(1, len(probe_results) + len(validation_findings)), 2),
        },
        "details": {
            "probe_failures": probe_failures,
            "contrast_findings": contrast_findings,
            "repair_targets": repair_targets,
            "promotion_recommendation": promotion_recommendation,
            "missing_inputs": missing,
        },
    }
    return finalize_profile_result(result, profile_id=PROFILE_ID, payload_warnings=warnings, manifest=manifest)
