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
    quality_failures = _as_list(payload_data.get("quality_failures"))
    candidate_outputs = _as_list(payload_data.get("candidate_outputs"))
    source_notes = _as_list(payload_data.get("source_notes"))
    constraints = _as_list(payload_data.get("constraints"))

    if not probe_results:
        for failure in quality_failures:
            probe_results.append({"probe": "production_quality_signal", "finding": str(failure)})
        for output in candidate_outputs:
            probe_results.append({"probe": "candidate_output_contrast", "finding": output})
    if not validation_findings:
        for note in source_notes:
            text = str(note)
            if any(term in text.lower() for term in ["threshold", "sub-threshold", "reject", "publish", "quality"]):
                validation_findings.append({"source_note": text})
        for constraint in constraints:
            text = str(constraint)
            if any(term in text.lower() for term in ["specific", "concrete", "shallow", "duplicate", "invent"]):
                validation_findings.append({"constraint": text})

    missing = []
    if not target:
        missing.append("plugin_name, slug, task, objective, or capability_spec")
    if not probe_results and not validation_findings:
        missing.append("probe_results or validation_findings")

    probe_failures = []
    contrast_findings = []
    repair_targets = []
    acceptance_evidence = []
    for item in probe_results + validation_findings:
        text = str(item)
        lower = text.lower()
        failed = any(term in lower for term in ["fail", "error", "blocker", "mismatch", "missing", "forbidden"])
        if failed:
            severity = "blocker" if any(term in lower for term in ["forbidden", "error", "blocker"]) else "warning"
            probe_failures.append({"evidence": text[:260], "severity": severity})
        if any(term in lower for term in ["same", "constant", "similar", "no difference", "shallow", "generic"]):
            contrast_findings.append(
                {
                    "evidence": text[:260],
                    "issue": "semantic contrast too weak",
                    "repair_hint": "Add probe-specific decision fields and score variance.",
                }
            )
        if "missing" in lower and ("detail" in lower or "specific" in lower or "output" in lower):
            repair_targets.append({"target": "required_detail_keys", "evidence": text[:200], "priority": "high"})
        if "profile" in lower or "routing" in lower:
            repair_targets.append({"target": "logic_profile_routing", "evidence": text[:200], "priority": "high"})
        if "forbidden" in lower or "backlog" in lower:
            repair_targets.append({"target": "forbidden_behavior_guard", "evidence": text[:200], "priority": "blocker"})
        if any(term in lower for term in ["passed", "specific", "measurable", "threshold", "quality"]):
            acceptance_evidence.append({"evidence": text[:220]})

    if not repair_targets and probe_failures:
        repair_targets.append(
            {
                "target": "semantic_contract",
                "evidence": "Probe failures need capability-specific repair.",
                "priority": "high",
            }
        )
    if not probe_failures and not contrast_findings and probe_results:
        promotion_recommendation = "promote"
    elif repair_targets:
        promotion_recommendation = "repair"
    else:
        promotion_recommendation = "insufficient_evidence"

    failure_density = round(len(probe_failures) / max(1, len(probe_results) + len(validation_findings)), 2)
    confidence = round(
        min(
            0.94,
            0.42
            + 0.07 * min(5, len(probe_results))
            + 0.06 * min(5, len(validation_findings))
            + 0.04 * min(4, len(repair_targets))
            + (0.06 if target else 0),
        ),
        2,
    )
    suggested_probe_contract = {
        "must_compare": ["summary", "recommended_actions", "scores", "details"],
        "must_reject_when": sorted({target_item["target"] for target_item in repair_targets}) or ["missing semantic evidence"],
        "minimum_contrast_expectation": "decision fields and scores must differ across semantically different payloads",
    }

    result = {
        "summary": f"Semantic probe analysis recommends {promotion_recommendation} for {target or 'unidentified capability'}.",
        "primary_insights": [
            {"title": "Probe failures", "detail": probe_failures or "No probe failures supplied."},
            {"title": "Contrast findings", "detail": contrast_findings or "No weak contrast evidence supplied."},
            {"title": "Repair targets", "detail": repair_targets},
            {"title": "Acceptance evidence", "detail": acceptance_evidence or "No positive semantic evidence supplied."},
        ],
        "recommended_actions": [
            {"action": "Apply promotion recommendation", "decision": promotion_recommendation},
            {"action": "Repair listed targets before retry", "targets": repair_targets},
            {"action": "Run contrast probes against repaired output", "contract": suggested_probe_contract},
            {
                "action": "Reject or hold publication when failure density remains high",
                "failure_density": failure_density,
            },
        ],
        "scores": {
            "confidence": confidence,
            "usefulness": 0.88 if probe_results or validation_findings else 0.42,
            "failure_density": failure_density,
            "repair_specificity": round(min(0.96, 0.42 + 0.12 * len(repair_targets) + 0.06 * len(contrast_findings)), 2),
        },
        "details": {
            "probe_failures": probe_failures,
            "contrast_findings": contrast_findings,
            "repair_targets": repair_targets,
            "promotion_recommendation": promotion_recommendation,
            "acceptance_evidence": acceptance_evidence,
            "suggested_probe_contract": suggested_probe_contract,
            "analyzed_probe_count": len(probe_results),
            "analyzed_validation_finding_count": len(validation_findings),
            "failure_density": failure_density,
            "missing_inputs": missing,
        },
    }
    return finalize_profile_result(result, profile_id=PROFILE_ID, payload_warnings=warnings, manifest=manifest, payload_data=payload_data)
