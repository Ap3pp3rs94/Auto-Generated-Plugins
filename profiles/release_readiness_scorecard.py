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
    git_status = str(payload_data.get("git_status") or "").strip()
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
    ]
    blocking_findings = []
    for check in readiness_checks:
        if not check["passed"]:
            blocking_findings.append({"check": check["check"], "reason": "required release evidence missing"})
    for failure in quality_failures:
        blocking_findings.append({"check": "quality_failure", "reason": str(failure)[:240]})
    release_decision = "ready_to_publish" if not blocking_findings and not missing else "hold_release"
    evidence_summary = {
        "validation_summary": validation_summary,
        "test_results": [str(item)[:240] for item in test_results],
        "changed_files": [str(item) for item in changed_files],
        "git_status": git_status,
    }
    confidence = 0.34 + 0.12 * bool(target) + 0.16 * bool(validation_summary or test_results) + 0.12 * bool(changed_files) - min(0.2, 0.04 * len(blocking_findings))
    result = {
        "summary": f"Release readiness decision for {target or 'unidentified capability'}: {release_decision}.",
        "primary_insights": [
            {"title": "Readiness checks", "detail": readiness_checks},
            {"title": "Blocking findings", "detail": blocking_findings or "No blockers detected from supplied evidence."},
            {"title": "Evidence summary", "detail": evidence_summary},
        ],
        "recommended_actions": [
            {"action": "Hold release until blockers are cleared" if blocking_findings or missing else "Publish after final git review", "decision": release_decision},
            {"action": "Collect missing release evidence", "missing_inputs": missing},
        ],
        "scores": {
            "confidence": round(max(0.1, min(0.94, confidence)), 2),
            "usefulness": 0.88 if validation_summary or test_results or changed_files else 0.42,
            "release_readiness": round(1.0 if release_decision == "ready_to_publish" else max(0.1, 0.68 - 0.08 * len(blocking_findings) - 0.08 * len(missing)), 2),
        },
        "details": {
            "readiness_checks": readiness_checks,
            "blocking_findings": blocking_findings,
            "release_decision": release_decision,
            "evidence_summary": evidence_summary,
            "missing_inputs": missing,
        },
    }
    return finalize_profile_result(result, profile_id=PROFILE_ID, payload_warnings=warnings, manifest=manifest)
