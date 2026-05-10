from __future__ import annotations

from typing import Any

from .profile_utils import finalize_profile_result, normalize_payload, user_candidate_text


PROFILE_ID = "plugin_repair_strategy_planner_profile"


def _as_list(value: Any) -> list[Any]:
    if isinstance(value, list):
        return value
    if value in (None, "", {}, ()):
        return []
    return [value]


def run(context: Any, payload: Any, config: dict[str, Any] | None, manifest: dict[str, Any]) -> dict[str, Any]:
    payload_data, warnings = normalize_payload(payload)
    target = user_candidate_text(payload_data)
    quality_failures = _as_list(payload_data.get("quality_failures"))
    validation_findings = _as_list(payload_data.get("validation_findings"))
    candidate_outputs = _as_list(payload_data.get("candidate_outputs"))
    source_excerpt = str(payload_data.get("plugin_source") or payload_data.get("source_excerpt") or "").strip()
    evidence_items = quality_failures + validation_findings + candidate_outputs + ([source_excerpt] if source_excerpt else [])
    missing = []
    if not target:
        missing.append("plugin_name, slug, task, objective, or capability_spec")
    if not evidence_items:
        missing.append("quality_failures, validation_findings, candidate_outputs, or source_excerpt")

    weak_signals = []
    signal_terms = {
        "profile_routing": ["wrong profile", "profile", "routing", "alias", "logic_profile_id"],
        "semantic_shallow": ["shallow", "constant", "metadata", "generic", "same output", "relabel"],
        "schema_gap": ["missing", "required", "detail", "score", "schema"],
        "runtime_failure": ["exception", "traceback", "import", "syntax", "failed"],
        "forbidden_behavior": ["backlog", "release_package", "next_plugin_specs", "forbidden"],
    }
    for item in evidence_items:
        text = str(item)
        lower = text.lower()
        hits = [label for label, terms in signal_terms.items() if any(term in lower for term in terms)]
        if hits:
            weak_signals.append({"signals": hits, "evidence": text[:240]})

    capability_specific_targets = [
        {"target": "profile_dispatch", "action": "Route aliases to one canonical profile runner"},
        {"target": "machine_details", "action": "Populate required detail keys from payload-derived analysis"},
        {"target": "semantic_probes", "action": "Run duplicate, unique, empty, and non-dict probes before promotion"},
        {"target": "scores", "action": "Make confidence/usefulness/risk derive from observed signals"},
    ]
    repair_plan = [
        {"step": 1, "action": "Classify weak signals", "signals": weak_signals[:8]},
        {"step": 2, "action": "Patch routing or profile logic", "targets": capability_specific_targets[:2]},
        {"step": 3, "action": "Re-run structural and semantic validation", "targets": capability_specific_targets[2:]},
        {"step": 4, "action": "Promote only if the repaired behavior beats the canonical plugin"},
    ]
    acceptance_checks = [
        "required detail keys present",
        "required scores include confidence and usefulness",
        "forbidden generic fields absent",
        "semantic contrast payloads change decisions",
        "promotion gate returns promote",
    ]
    confidence = 0.36 + min(0.24, len(weak_signals) * 0.06) + (0.16 if target else 0.0) + (0.12 if source_excerpt else 0.0)
    result = {
        "summary": f"Repair strategy prepared for {target or 'unidentified capability'}.",
        "primary_insights": [
            {"title": "Weak signals", "detail": weak_signals or "No concrete failure evidence was supplied."},
            {"title": "Repair targets", "detail": capability_specific_targets},
            {"title": "Acceptance checks", "detail": acceptance_checks},
        ],
        "recommended_actions": [
            {"action": "Repair profile routing first", "target": "profile_dispatch"},
            {"action": "Repair required machine details", "target": "machine_details"},
            {"action": "Reject if semantic probes still fail", "acceptance_checks": acceptance_checks},
        ],
        "scores": {"confidence": round(min(0.93, confidence), 2), "usefulness": 0.88 if evidence_items else 0.44},
        "details": {
            "repair_plan": repair_plan,
            "weak_signals": weak_signals,
            "capability_specific_targets": capability_specific_targets,
            "acceptance_checks": acceptance_checks,
            "missing_inputs": missing,
        },
    }
    return finalize_profile_result(result, profile_id=PROFILE_ID, payload_warnings=warnings, manifest=manifest, payload_data=payload_data)
