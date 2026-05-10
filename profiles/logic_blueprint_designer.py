from __future__ import annotations

from typing import Any

from .profile_utils import capability_spec_payload, finalize_profile_result, normalize_payload, user_candidate_text, user_target_text


PROFILE_ID = "plugin_logic_blueprint_designer_profile"


def run(context: Any, payload: Any, config: dict[str, Any] | None, manifest: dict[str, Any]) -> dict[str, Any]:
    payload_data, warnings = normalize_payload(payload)
    spec = capability_spec_payload(payload_data)
    missing = [] if spec else ["capability_spec or candidate capability fields"]
    name = str(spec.get("name") or user_candidate_text(payload_data) or "unnamed capability")
    owns = [str(item) for item in spec.get("owns", [])] if isinstance(spec.get("owns"), list) else []
    required_inputs = [str(item) for item in spec.get("required_inputs", [])] if isinstance(spec.get("required_inputs"), list) else []
    required_detail_keys = [str(item) for item in spec.get("required_detail_keys", [])] if isinstance(spec.get("required_detail_keys"), list) else []
    forbidden = [str(item) for item in spec.get("forbidden_detail_keys", [])] if isinstance(spec.get("forbidden_detail_keys"), list) else []
    target_text = user_target_text(payload_data)
    target_lower = target_text.lower()
    signal_groups = []
    for group_name, terms, algorithm in [
        (
            "release_safe_refactor",
            ["auth", "authentication", "login", "middleware", "migration", "rollback", "session", "database"],
            "release-safe refactor planner with rollback and regression gates",
        ),
        (
            "grounded_claim_verification",
            ["medical", "citation", "source", "claim", "retrieval", "hallucination", "dosage", "unsupported"],
            "grounded claim verifier with citation matching and unsupported-claim handling",
        ),
        (
            "tool_orchestration",
            ["tool", "api", "argument", "permission", "browser", "local", "workflow"],
            "tool orchestration planner with permission and argument checks",
        ),
    ]:
        hits = [term for term in terms if term in target_lower]
        if hits:
            signal_groups.append({"group": group_name, "matched_terms": hits, "algorithm": algorithm})
    selected_algorithm = (
        signal_groups[0]["algorithm"]
        if signal_groups
        else "generic deterministic capability analyzer with explicit missing-input handling"
    )
    focus_terms = sorted(
        {
            word.strip(".,:;!?()[]{}").lower()
            for word in target_text.split()
            if len(word.strip(".,:;!?()[]{}")) > 6
        }
    )[:10]
    if signal_groups and signal_groups[0]["group"] == "release_safe_refactor":
        algorithm_actions = [
            "Extract release, rollback, migration, and login-regression signals.",
            "Construct reversible implementation stages before recommending execution.",
            "Score risk from blocked owners, database scope, and missing rollback evidence.",
        ]
    elif signal_groups and signal_groups[0]["group"] == "grounded_claim_verification":
        algorithm_actions = [
            "Extract answer claims and map each claim to source or citation evidence.",
            "Separate supported, unsupported, and caveated claims before response drafting.",
            "Score risk from unsupported medical or factual claims and missing citations.",
        ]
    else:
        algorithm_actions = [
            "Extract capability-owned signals from the payload.",
            "Construct required detail keys from observed values.",
            "Score risk from missing inputs and forbidden behavior.",
        ]
    stages = [
        {"stage": "normalize_inputs", "uses": required_inputs or ["payload"], "output": "normalized_payload"},
        {"stage": "validate_required_inputs", "uses": required_inputs or ["capability intent"], "output": "missing_inputs"},
        {"stage": "extract_owned_signals", "uses": owns or focus_terms or [name], "output": "capability_signals"},
        {"stage": "derive_decision_fields", "uses": algorithm_actions, "output": "machine_decisions"},
        {"stage": "construct_machine_details", "uses": required_detail_keys or ["summary", "recommended_actions"], "output": "details"},
        {"stage": "guard_forbidden_behavior", "uses": forbidden or ["metadata-only relabeling"], "output": "rejection_findings"},
        {"stage": "run_semantic_contrast", "uses": ["duplicate-heavy probe", "unique probe", "missing-input probe"], "output": "semantic_findings"},
        {"stage": "score_and_explain", "uses": ["confidence", "usefulness"], "output": "scores"},
    ]
    output_constructors = [
        {
            "detail_key": key,
            "construction_rule": f"Derive {key} from payload signals, not plugin metadata.",
            "empty_payload_behavior": "leave empty or mark missing; do not use the plugin goal as evidence",
        }
        for key in (required_detail_keys or ["summary", "recommended_actions", "scores"])
    ]
    scoring_formula = {
        "confidence": "increase with required input coverage and contrast-probe agreement",
        "usefulness": "increase when machine-readable detail keys and next actions are populated",
        "risk": "increase when missing inputs or forbidden behaviors appear",
    }
    semantic_probes = [
        {"probe": "empty_payload", "expected": "missing_inputs and blockers are populated"},
        {"probe": "useful_payload", "expected": "required detail keys are populated from supplied values"},
        {"probe": "contrast_payloads", "expected": "details and scores change across different payload meanings"},
    ]
    data_flow = {
        "inputs": required_inputs,
        "stages": [stage["stage"] for stage in stages],
        "outputs": required_detail_keys,
        "forbidden_outputs": forbidden,
    }
    result = {
        "summary": f"Logic blueprint for {name}: {selected_algorithm}. Focus terms: {', '.join(focus_terms[:6]) or 'none'}.",
        "primary_insights": [
            {"title": "Selected algorithm", "detail": selected_algorithm},
            {"title": "Payload signal groups", "detail": signal_groups or "No specialized signal group matched."},
            {"title": "Blueprint stages", "detail": stages},
            {"title": "Data flow", "detail": data_flow},
            {"title": "Output constructors", "detail": output_constructors},
            {"title": "Semantic probes", "detail": semantic_probes},
        ],
        "recommended_actions": [
            {"action": f"Implement {selected_algorithm}", "stages": [stage["stage"] for stage in stages]},
            {"action": "Apply payload-specific algorithm actions", "algorithm_actions": algorithm_actions},
            {"action": "Use required detail keys as acceptance checks", "required_detail_keys": required_detail_keys},
            {"action": "Wire semantic probes before promotion", "semantic_probes": semantic_probes},
            {"action": "Reject forbidden behavior", "forbidden_detail_keys": forbidden},
        ],
        "scores": {
            "confidence": round((0.89 if spec else 0.42) + min(0.04, len(signal_groups) * 0.02), 2),
            "usefulness": round((0.9 if spec else 0.5) + min(0.04, len(focus_terms) * 0.004), 2),
            "stage_count": len(stages),
            "algorithm_specificity": round(min(0.96, 0.55 + 0.1 * len(signal_groups) + 0.02 * len(focus_terms)), 2),
        },
        "details": {
            "logic_blueprint": stages,
            "deterministic_rules": [
                "No external calls",
                "No file mutation",
                "Scores derive from observed signals",
                "Do not use the plugin goal as user-provided input",
                "No metadata-only relabeling counts as behavior",
            ],
            "data_flow": data_flow,
            "failure_modes": ["metadata-only relabeling", "missing detail keys", "constant outputs across probes"],
            "output_constructors": output_constructors,
            "scoring_formula": scoring_formula,
            "semantic_probes": semantic_probes,
            "selected_algorithm": selected_algorithm,
            "payload_signal_groups": signal_groups,
            "algorithm_actions": algorithm_actions,
            "focus_terms": focus_terms,
            "forbidden_behavior": forbidden,
            "missing_inputs": missing,
        },
        "progress_state": {
            "current_stage": PROFILE_ID,
            "next_step": f"Implement {selected_algorithm}",
            "blockers": missing,
            "done_signals": ["logic_blueprint_ready", selected_algorithm],
        },
    }
    return finalize_profile_result(result, profile_id=PROFILE_ID, payload_warnings=warnings, manifest=manifest, payload_data=payload_data)
