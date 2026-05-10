from __future__ import annotations

from typing import Any

from .profile_utils import finalize_profile_result, normalize_payload, user_candidate_text


PROFILE_ID = "release_readiness_scorecard_profile"


def _as_list(value: Any) -> list[Any]:
    if isinstance(value, list):
        return value
    if value in (None, "", {}, ()):
        return []
    return [value]


def run(context: Any, payload: Any, config: dict[str, Any] | None, manifest: dict[str, Any]) -> dict[str, Any]:
    payload_data, warnings = normalize_payload(payload)
    target = user_candidate_text(payload_data)
    validation_summary = payload_data.get("validation_summary") if isinstance(payload_data.get("validation_summary"), dict) else {}
    test_results = _as_list(payload_data.get("test_results"))
    changed_files = _as_list(payload_data.get("files") or payload_data.get("changed_files"))
    quality_failures = _as_list(payload_data.get("quality_failures"))
    constraints = _as_list(payload_data.get("constraints"))
    source_notes = _as_list(payload_data.get("source_notes"))
    current_plan = _as_list(payload_data.get("current_plan"))
    completed_steps = _as_list(payload_data.get("completed_steps"))
    candidate_outputs = _as_list(payload_data.get("candidate_outputs"))
    git_status = str(payload_data.get("git_status") or "").strip()

    if not validation_summary:
        validation_summary = {
            "structural_ok": any("validate" in str(item).lower() for item in current_plan + completed_steps),
            "semantic_ok": not quality_failures
            and any("semantic" in str(item).lower() or "specific" in str(item).lower() for item in constraints + source_notes),
            "production_threshold": next(
                (str(item) for item in source_notes if "threshold" in str(item).lower()),
                "",
            ),
        }
        validation_summary = {key: value for key, value in validation_summary.items() if value not in (None, "", [], {})}
    if not test_results:
        for item in current_plan + completed_steps:
            text = str(item)
            if any(term in text.lower() for term in ["test", "validate", "semantic", "quality"]):
                test_results.append(text)
    if not changed_files:
        for scope in _as_list(payload_data.get("ownership_scopes")):
            if any(term in str(scope).lower() for term in ["code", "quality", "release"]):
                changed_files.append(str(scope))

    missing = []
    if not target:
        missing.append("plugin_name, slug, task, objective, or capability_spec")
    if not validation_summary and not test_results:
        missing.append("validation_summary or test_results")

    readiness_checks = [
        {"check": "structural_validation", "passed": bool(validation_summary.get("structural_ok", validation_summary.get("ok", False)) or test_results)},
        {"check": "semantic_validation", "passed": bool(validation_summary.get("semantic_ok", False) or not quality_failures)},
        {"check": "changed_files_declared", "passed": bool(changed_files)},
        {"check": "git_status_reviewed", "passed": bool(git_status or changed_files)},
        {"check": "quality_failures_reviewed", "passed": bool(not quality_failures or candidate_outputs or source_notes)},
        {"check": "release_constraints_declared", "passed": bool(constraints or source_notes)},
    ]
    blocking_findings = []
    for check in readiness_checks:
        if not check["passed"]:
            blocking_findings.append({"check": check["check"], "reason": "required release evidence missing"})
    for failure in quality_failures:
        blocking_findings.append(
            {
                "check": "quality_failure",
                "reason": str(failure)[:240],
                "required_resolution": "repair or reject before publication",
            }
        )
    release_decision = "ready_to_publish" if not blocking_findings and not missing else "hold_release"
    release_risks = [
        {
            "risk": finding["check"],
            "impact": "blocks canonical promotion",
            "mitigation": finding.get("required_resolution", finding.get("reason", "collect evidence")),
        }
        for finding in blocking_findings
    ]
    release_evidence_checklist = [
        {"evidence": "structural validation", "present": readiness_checks[0]["passed"]},
        {"evidence": "semantic depth or contract validation", "present": readiness_checks[1]["passed"]},
        {"evidence": "changed files or ownership scopes", "present": readiness_checks[2]["passed"]},
        {"evidence": "quality failure disposition", "present": readiness_checks[4]["passed"]},
        {"evidence": "publish constraints", "present": readiness_checks[5]["passed"]},
    ]
    evidence_summary = {
        "validation_summary": validation_summary,
        "test_results": [str(item)[:240] for item in test_results],
        "changed_files": [str(item) for item in changed_files],
        "quality_failures": [str(item)[:240] for item in quality_failures],
        "release_constraints": [str(item)[:240] for item in constraints],
        "source_notes": [str(item)[:240] for item in source_notes],
        "git_status": git_status,
    }
    confidence = (
        0.42
        + 0.12 * bool(target)
        + 0.14 * bool(validation_summary or test_results)
        + 0.08 * bool(changed_files)
        + 0.05 * bool(constraints or source_notes)
        - min(0.18, 0.035 * len(blocking_findings))
    )
    result = {
        "summary": f"Release readiness decision for {target or 'unidentified capability'}: {release_decision}.",
        "primary_insights": [
            {"title": "Readiness checks", "detail": readiness_checks},
            {"title": "Blocking findings", "detail": blocking_findings or "No blockers detected from supplied evidence."},
            {"title": "Evidence summary", "detail": evidence_summary},
            {"title": "Release risks", "detail": release_risks or "No release-blocking risk detected."},
        ],
        "recommended_actions": [
            {"action": "Hold release until blockers are cleared" if blocking_findings or missing else "Publish after final git review", "decision": release_decision},
            {"action": "Collect missing release evidence", "missing_inputs": missing},
            {"action": "Resolve release risks", "risks": release_risks},
            {"action": "Attach release evidence checklist", "checklist": release_evidence_checklist},
        ],
        "scores": {
            "confidence": round(max(0.1, min(0.94, confidence)), 2),
            "usefulness": 0.88 if validation_summary or test_results or changed_files else 0.42,
            "release_readiness": round(1.0 if release_decision == "ready_to_publish" else max(0.1, 0.68 - 0.08 * len(blocking_findings) - 0.08 * len(missing)), 2),
            "blocker_count": len(blocking_findings),
            "evidence_coverage": round(
                len([item for item in release_evidence_checklist if item["present"]]) / max(1, len(release_evidence_checklist)),
                2,
            ),
        },
        "details": {
            "readiness_checks": readiness_checks,
            "blocking_findings": blocking_findings,
            "release_decision": release_decision,
            "evidence_summary": evidence_summary,
            "release_risks": release_risks,
            "release_evidence_checklist": release_evidence_checklist,
            "publish_guardrails": [
                "do not publish while release_decision is hold_release",
                "do not publish with unresolved quality_failures",
                "record validation evidence before GitHub push",
            ],
            "missing_inputs": missing,
        },
    }
    return finalize_profile_result(result, profile_id=PROFILE_ID, payload_warnings=warnings, manifest=manifest, payload_data=payload_data)
