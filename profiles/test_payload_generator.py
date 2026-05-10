from __future__ import annotations

from typing import Any

from .profile_utils import capability_spec_payload, finalize_profile_result, normalize_payload, user_candidate_text


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
    test_payloads = [
        {"name": "empty_payload_missing_input", "payload": {}, "expect": {"missing_inputs": True, "blockers": True}},
        {"name": "required_behavior_happy_path", "payload": {"task": name, "required_behavior": required_behavior, "capability_spec": spec}, "expect": {"detail_keys": required_detail_keys}},
        {"name": "forbidden_behavior_guard", "payload": {"task": name, "forbidden_behavior": forbidden_behavior, "capability_spec": spec}, "expect": {"forbidden_detail_keys_absent": forbidden_detail_keys}},
        {"name": "semantic_contrast", "payload": {"task": "different domain contrast", "capability_spec": spec}, "expect": {"decision_surface_differs": True}},
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
            {"title": "Probe execution plan", "detail": probe_execution_plan},
        ],
        "recommended_actions": [
            {"action": "Run generated payloads before promotion", "payload_count": len(test_payloads)},
            {"action": "Fail on forbidden behavior", "forbidden_behavior": forbidden_behavior},
            {"action": "Diff semantic contrast pairs", "contrast_pairs": contrast_pairs},
            {"action": "Track regressions across future repairs", "regression_watchlist": regression_watchlist},
        ],
        "scores": {"confidence": 0.93 if spec else 0.4, "usefulness": 0.94 if spec else 0.5, "probe_count": len(test_payloads), "contrast_pair_count": len(contrast_pairs)},
        "details": {
            "test_payloads": test_payloads,
            "edge_cases": edge_cases,
            "expected_differences": [pair["expected_difference"] for pair in contrast_pairs],
            "contrast_pairs": contrast_pairs,
            "probe_execution_plan": probe_execution_plan,
            "regression_watchlist": regression_watchlist,
            "missing_inputs": missing,
        },
    }
    return finalize_profile_result(result, profile_id=PROFILE_ID, payload_warnings=warnings, manifest=manifest, payload_data=payload_data)
