from __future__ import annotations

from typing import Any

from .profile_utils import capability_spec_payload, finalize_profile_result, normalize_payload, user_candidate_text, user_target_text


PROFILE_ID = "plugin_test_payload_generator_profile"
__test__ = False


def run(context: Any, payload: Any, config: dict[str, Any] | None, manifest: dict[str, Any]) -> dict[str, Any]:
    payload_data, warnings = normalize_payload(payload)
    spec = capability_spec_payload(payload_data)
    missing = [] if spec else ["capability_spec or candidate capability fields"]
    name = str(spec.get("name") or user_candidate_text(payload_data) or "unnamed capability")
    required_behavior = str(spec.get("required_behavior") or payload_data.get("required_behavior") or "perform the named capability")
    forbidden_behavior = spec.get("forbidden_behavior")
    if not isinstance(forbidden_behavior, list):
        forbidden_behavior = spec.get("does_not_own") if isinstance(spec.get("does_not_own"), list) else []
    required_detail_keys = spec.get("required_detail_keys") if isinstance(spec.get("required_detail_keys"), list) else []
    forbidden_detail_keys = spec.get("forbidden_detail_keys") if isinstance(spec.get("forbidden_detail_keys"), list) else []
    target_text = user_target_text(payload_data)
    target_lower = target_text.lower()
    if any(term in target_lower for term in ["auth", "login", "middleware", "migration", "rollback", "database"]):
        domain_probe = {
            "name": "release_safety_domain_probe",
            "payload": {"task": "Verify auth middleware rollback and login regression safety", "capability_spec": spec},
            "expect": {"must_reflect_terms": ["auth", "rollback", "login"], "risk_topic": "release_safety"},
        }
        domain_expectation = "release probes should produce rollback, migration, and login-regression decisions"
    elif any(term in target_lower for term in ["medical", "citation", "source", "claim", "retrieval", "hallucination"]):
        domain_probe = {
            "name": "grounded_answer_domain_probe",
            "payload": {"task": "Verify medical claim support against citations and source notes", "capability_spec": spec},
            "expect": {"must_reflect_terms": ["claim", "citation", "source"], "risk_topic": "grounding"},
        }
        domain_expectation = "grounding probes should produce claim, citation, source-support, and caveat decisions"
    else:
        domain_probe = {
            "name": "generic_domain_probe",
            "payload": {"task": name, "capability_spec": spec},
            "expect": {"must_reflect_terms": [str(name).split()[0] if str(name).split() else "capability"], "risk_topic": "generic"},
        }
        domain_expectation = "generic probes should still change decision fields from empty and forbidden probes"
    test_payloads = [
        {"name": "empty_payload_missing_input", "payload": {}, "expect": {"missing_inputs": True, "blockers": True}},
        {"name": "required_behavior_happy_path", "payload": {"task": name, "required_behavior": required_behavior, "capability_spec": spec}, "expect": {"detail_keys": required_detail_keys}},
        {"name": "forbidden_behavior_guard", "payload": {"task": name, "forbidden_behavior": forbidden_behavior, "capability_spec": spec}, "expect": {"forbidden_detail_keys_absent": forbidden_detail_keys}},
        {"name": "semantic_contrast", "payload": {"task": "different domain contrast", "capability_spec": spec}, "expect": {"decision_surface_differs": True}},
        domain_probe,
    ]
    contrast_pairs = [
        {"left": "required_behavior_happy_path", "right": "semantic_contrast", "expected_difference": "summary, recommended_actions, scores, and machine details should change"},
        {"left": "empty_payload_missing_input", "right": "required_behavior_happy_path", "expected_difference": "missing_inputs and blockers clear only when useful input exists"},
        {"left": "forbidden_behavior_guard", "right": "required_behavior_happy_path", "expected_difference": "forbidden behavior creates repair or reject evidence"},
    ]
    edge_cases = ["non-dict payload", "missing candidate capability", "forbidden behavior appears", "required details absent", "constant scores across probes"]
    regression_watchlist = [
        "metadata-only relabeling",
        "generic backlog output",
        "constant scores",
        "goal text treated as user input",
        "forbidden detail keys present",
    ]
    probe_execution_plan = [
        {"step": "invoke_empty_payload", "assert": "missing_inputs and blockers are non-empty"},
        {"step": "invoke_happy_path", "assert": "required detail keys are populated"},
        {"step": "invoke_forbidden_behavior", "assert": "forbidden outputs are absent or rejected"},
        {"step": "diff_contrast_pair", "assert": "decision surface and scores differ"},
    ]
    result = {
        "summary": f"Semantic test payloads generated for {name}: {len(test_payloads)} probes and {len(contrast_pairs)} contrast pair(s).",
        "primary_insights": [
            {"title": "Generated probes", "detail": test_payloads},
            {"title": "Edge cases", "detail": edge_cases},
            {"title": "Contrast pairs", "detail": contrast_pairs},
            {"title": "Domain-specific expectation", "detail": domain_expectation},
            {"title": "Probe execution plan", "detail": probe_execution_plan},
        ],
        "recommended_actions": [
            {"action": "Run domain-specific probe", "probe": domain_probe["name"], "expectation": domain_expectation},
            {"action": "Run generated payloads before promotion", "payload_count": len(test_payloads)},
            {"action": "Fail on forbidden behavior", "forbidden_behavior": forbidden_behavior},
            {"action": "Diff semantic contrast pairs", "contrast_pairs": contrast_pairs},
            {"action": "Track regressions across future repairs", "regression_watchlist": regression_watchlist},
        ],
        "scores": {"confidence": 0.93 if spec else 0.4, "usefulness": 0.94 if spec else 0.5, "probe_count": len(test_payloads), "contrast_pair_count": len(contrast_pairs), "domain_probe_specificity": 0.9 if domain_probe["name"] != "generic_domain_probe" else 0.62},
        "details": {
            "test_payloads": test_payloads,
            "edge_cases": edge_cases,
            "expected_differences": [pair["expected_difference"] for pair in contrast_pairs],
            "contrast_pairs": contrast_pairs,
            "domain_probe": domain_probe,
            "domain_expectation": domain_expectation,
            "probe_execution_plan": probe_execution_plan,
            "regression_watchlist": regression_watchlist,
            "missing_inputs": missing,
        },
        "progress_state": {
            "current_stage": PROFILE_ID,
            "next_step": f"Run {domain_probe['name']}",
            "blockers": missing,
            "done_signals": ["test_payloads_ready", domain_probe["name"]],
        },
    }
    return finalize_profile_result(result, profile_id=PROFILE_ID, payload_warnings=warnings, manifest=manifest, payload_data=payload_data)
