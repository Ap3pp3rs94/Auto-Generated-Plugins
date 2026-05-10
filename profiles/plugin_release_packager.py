from __future__ import annotations

from typing import Any

from .profile_utils import finalize_profile_result, manifest_value, normalize_payload, user_candidate_text, user_target_text


PROFILE_ID = "plugin_release_packager_profile"


def _as_list(value: Any) -> list[Any]:
    if isinstance(value, list):
        return value
    if value in (None, "", {}, ()):
        return []
    return [value]


def run(context: Any, payload: Any, config: dict[str, Any] | None, manifest: dict[str, Any]) -> dict[str, Any]:
    payload_data, warnings = normalize_payload(payload)
    target = user_candidate_text(payload_data) or str(manifest_value(manifest, "name", "generated capability"))
    files = _as_list(payload_data.get("files") or payload_data.get("changed_files"))
    validation_summary = payload_data.get("validation_summary") if isinstance(payload_data.get("validation_summary"), dict) else {}
    quality_failures = _as_list(payload_data.get("quality_failures"))
    source_notes = _as_list(payload_data.get("source_notes") or payload_data.get("notes"))
    test_results = _as_list(payload_data.get("test_results"))
    release_text = user_target_text(payload_data).lower()
    if any(term in release_text for term in ["auth", "login", "middleware", "migration", "rollback", "database"]):
        release_mode = {
            "mode": "release_safety",
            "evidence_required": ["rollback check", "login regression result", "database or migration owner"],
            "publish_action": "Hold publish until rollback and login-regression evidence are attached.",
        }
    elif any(term in release_text for term in ["medical", "citation", "source", "claim", "retrieval", "hallucination", "unsupported"]):
        release_mode = {
            "mode": "grounded_answer_safety",
            "evidence_required": ["claim-source map", "citation verification", "unsupported-claim caveats"],
            "publish_action": "Hold publish until source grounding evidence is attached.",
        }
    else:
        release_mode = {
            "mode": "generic_capability_release",
            "evidence_required": ["validation summary", "semantic depth result", "production quality score"],
            "publish_action": "Publish only after all promotion evidence is present.",
        }
    missing = []
    if not files:
        missing.append("files or changed_files")
    if not validation_summary and not test_results:
        missing.append("validation_summary or test_results")

    release_package = {
        "title": str(target),
        "files": [str(item) for item in files],
        "validation_summary": validation_summary,
        "test_results": [str(item)[:240] for item in test_results],
        "notes": [str(item)[:240] for item in source_notes[:8]],
        "release_mode": release_mode,
    }
    github_publish_plan = [
        {"step": "stage", "command_intent": "stage only changed capability/profile/test files"},
        {"step": "commit", "command_intent": "commit with validation summary in message"},
        {"step": "push", "command_intent": "push origin main only after promotion gate passes"},
    ]
    rollback_notes = [
        release_mode["publish_action"],
        "Do not publish failed candidates.",
        "Keep rejected candidates in junk or quality rejection folders.",
        "Re-run targeted tests before restarting continuous generation.",
    ]
    evidence_checklist = [
        {"evidence": item, "present": any(item.split()[0].lower() in str(note).lower() for note in source_notes + test_results)}
        for item in release_mode["evidence_required"]
    ]
    blockers = list(missing)
    if quality_failures:
        blockers.append("unresolved quality_failures")
    confidence = 0.38 + (0.18 if files else 0.0) + (0.18 if validation_summary or test_results else 0.0) + (0.08 if not quality_failures else -0.06)
    result = {
        "summary": f"Release package for {target}: {release_mode['mode']} with {len(evidence_checklist)} evidence check(s).",
        "primary_insights": [
            {"title": "Release mode", "detail": release_mode},
            {"title": "Evidence checklist", "detail": evidence_checklist},
            {"title": "Release package", "detail": release_package},
            {"title": "Publish plan", "detail": github_publish_plan},
            {"title": "Rollback notes", "detail": rollback_notes},
        ],
        "recommended_actions": [
            {"action": release_mode["publish_action"], "release_mode": release_mode["mode"], "evidence_required": release_mode["evidence_required"]},
            {"action": "Resolve release blockers", "blockers": blockers},
            {"action": "Publish only after gates pass", "publish_plan": github_publish_plan},
            {"action": "Attach release evidence checklist", "evidence_checklist": evidence_checklist},
        ],
        "scores": {
            "confidence": round(max(0.1, min(0.94, confidence)), 2),
            "usefulness": 0.88 if files else 0.48,
            "release_readiness": round(0.86 if not blockers else max(0.2, 0.62 - 0.08 * len(blockers)), 2),
            "evidence_specificity": round(0.58 + min(0.32, 0.08 * len(release_mode["evidence_required"])), 2),
        },
        "details": {
            "release_package": release_package,
            "validation_summary": validation_summary,
            "github_publish_plan": github_publish_plan,
            "rollback_notes": rollback_notes,
            "release_mode": release_mode,
            "evidence_checklist": evidence_checklist,
            "missing_inputs": missing,
        },
        "progress_state": {
            "current_stage": PROFILE_ID,
            "next_step": release_mode["publish_action"],
            "blockers": blockers,
            "done_signals": ["release_package_ready", release_mode["mode"]],
        },
    }
    return finalize_profile_result(result, profile_id=PROFILE_ID, payload_warnings=warnings, manifest=manifest, payload_data=payload_data)
