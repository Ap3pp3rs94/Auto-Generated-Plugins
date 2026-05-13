from __future__ import annotations

import asyncio
import inspect
import json
import re
from dataclasses import dataclass, field
from typing import Any, Callable, Literal, Optional


A_PLUS_MIN_SCORE = 0.98

FindingSeverity = Literal["info", "warning", "error", "blocker"]
RecommendedAction = Literal["certify", "repair", "regenerate", "retire"]


@dataclass(frozen=True)
class APlusProbe:
    probe_id: str
    name: str
    payload: Any
    expectation: Literal["missing_input", "payload_warning", "useful_output", "contrast_output"]


@dataclass(frozen=True)
class APlusFinding:
    code: str
    severity: FindingSeverity
    message: str
    probe_id: Optional[str] = None
    evidence: Any = None


@dataclass(frozen=True)
class APlusCertificationResult:
    passed: bool
    score: float
    findings: list[APlusFinding] = field(default_factory=list)
    probe_outputs: dict[str, dict[str, Any]] = field(default_factory=dict)
    recommended_action: RecommendedAction = "certify"


REQUIRED_TOP_LEVEL_KEYS = {
    "summary",
    "primary_insights",
    "recommended_actions",
    "scores",
    "details",
    "progress_state",
    "user_experience",
    "fun_mode",
    "diagnostics",
}

REQUIRED_DIAGNOSTIC_KEYS = {
    "logic_profile_id",
    "has_user_input",
    "used_goal_fallback",
    "input_signal_count",
    "missing_inputs_count",
    "payload_warning_count",
    "profile_output_keys",
    "semantic_probe_ready",
}

GENERIC_DETAIL_KEYS = {
    "logic_profile_id",
    "generation_note",
    "capability_type",
    "use_cases",
    "payload_warnings",
    "has_user_input",
    "used_goal_fallback",
    "input_signals",
    "input_signal_fingerprint",
    "missing_inputs",
}

PROFILE_DETAIL_HINTS: tuple[tuple[str, set[str]], ...] = (
    ("prompt_refinement", {"identified_vagueness", "missing_constraints", "rewrites", "refined_prompt"}),
    ("prompt_test_case_generator", {"test_cases", "ambiguities", "risk_tags"}),
    ("retrieval_query", {"expanded_queries", "facet_terms", "grounding_plan"}),
    ("source_quality_ranker", {"supported_claims", "unsupported_claims", "evidence_map", "answer_plan"}),
    ("context_noise_filter", {"kept_context", "compressed_context", "dropped_context"}),
    ("memory_update_recommender", {"memory_summary", "durable_facts", "open_threads"}),
    ("memory_compression", {"memory_summary", "durable_facts", "open_threads"}),
    ("task_planner", {"sequenced_plan", "handoff_packet", "risk_signals"}),
    ("parallelization_planner", {"sequenced_plan", "handoff_packet"}),
    ("agent_handoff_checker", {"handoff_inputs", "ownership_boundaries", "handoff_overlap_decision"}),
    ("tool_selection", {"tool_recommendations", "rejected_tools", "selection_rationale"}),
    ("tool_safety_reviewer", {"risk_findings", "controls", "approval_required"}),
    ("tool_argument_checker", {"argument_risks", "unsafe_arguments", "sanitized_arguments", "argument_safety_decision"}),
    ("output_quality_scorer", {"covered_requirements", "missing_requirements", "improvement_checklist"}),
    ("output_completeness_grader", {"completeness_findings", "missing_sections", "completeness_score"}),
    ("response_action_planner", {"action_plan", "actionability_gaps", "next_step_checks"}),
    ("hallucination", {"claims", "high_risk_claims", "safer_rewrites"}),
    ("citation", {"claims", "high_risk_claims", "safer_rewrites"}),
    ("workflow_debugger", {"failure_points", "signals_by_stage", "retry_plan"}),
    ("trace_failure_router", {"failure_points", "signals_by_stage", "retry_plan"}),
    ("rollback_guard_builder", {"rollback_plan", "rollback_readiness", "blast_radius"}),
    ("verification_checklist_builder", {"verification_checklist", "automated_checks", "human_review_checks"}),
    ("instruction_hierarchy_checker", {"instruction_sources", "conflicts", "clarified_instruction"}),
    ("capability_router", {"routes", "selected_route", "routing_decision"}),
    ("quality_gate_designer", {"quality_gates", "semantic_probes", "required_detail_keys"}),
    ("logic_blueprint_designer", {"implementation_stages", "deterministic_helpers", "required_detail_keys"}),
    ("data_contract_validator", {"input_contract", "output_contract", "validation_rules"}),
    ("release_evidence_summarizer", {"release_notes", "validation_evidence", "publish_checklist"}),
    ("release_readiness_scorecard", {"release_notes", "validation_evidence", "publish_checklist"}),
    ("capability_overlap_checker", {"duplicate_risks", "uniqueness_fingerprint", "comparison_targets", "merge_or_reject_decision"}),
)


def build_a_plus_probes() -> list[APlusProbe]:
    return [
        APlusProbe("empty_payload", "Empty payload", {}, "missing_input"),
        APlusProbe("non_dict_payload", "Non-dict payload", "make this better", "payload_warning"),
        APlusProbe(
            "useful_payload",
            "Rich useful payload",
            {
                "task": "Plan a safe AI capability release for authentication middleware.",
                "objective": "Produce concrete next actions, risk checks, and validation evidence.",
                "prompt": "Make this production-ready without breaking login.",
                "instruction": "Return machine-readable details that another AI agent can use.",
                "query": "auth middleware rollback verification",
                "question": "Which evidence proves the release is safe?",
                "response": "Draft answer with missing rollback and weak citation evidence.",
                "answer": "Candidate answer that needs quality scoring.",
                "expected_behavior": "Detect risks and produce specific checks.",
                "messages": [{"content": "Need auth middleware release plan with tests."}],
                "source_notes": [
                    {"title": "local validation", "type": "command_log", "content": "login regression tests passed"},
                    {"title": "rollback note", "type": "runbook", "content": "rollback command documented"},
                ],
                "candidate_outputs": [
                    {"summary": "Ship after auth regression tests pass."},
                    {"summary": "Hold until rollback is verified."},
                ],
                "trace": [{"stage": "validation", "error": "missing rollback evidence"}],
                "current_plan": ["inspect middleware", "run login tests", "publish release note"],
                "completed_steps": ["mapped auth flow", "added regression test"],
                "blocked_steps": ["need rollback owner"],
                "agents": ["builder", "reviewer", "release owner"],
                "workstreams": ["auth code", "tests", "rollback"],
                "ownership_scopes": ["implementation", "verification", "release"],
                "tool_results": [{"tool": "pytest", "status": "passed"}],
                "rubric": ["mentions validation", "lists risks", "chooses next action"],
                "constraints": ["no production outage", "no hidden side effects"],
                "requirements": ["structured details", "confidence score", "next action"],
                "example_payload": {"task": "release auth middleware"},
                "token_budget": 900,
            },
            "useful_output",
        ),
        APlusProbe(
            "contrast_payload",
            "Contrasting safety payload",
            {
                "task": "Evaluate hallucination risk in a medical citation answer.",
                "objective": "Separate supported claims from claims needing more retrieval.",
                "prompt": "Is this dosage claim safe to show to the user?",
                "instruction": "Use citations and uncertainty language before answering.",
                "query": "clinical citation mismatch dosage claim",
                "question": "Which claims need external verification?",
                "response": "The answer states a dosage claim without source support.",
                "answer": "Candidate medical answer with unsupported claim.",
                "expected_behavior": "Rank citation risk and recommend safer wording.",
                "messages": [{"content": "Need medical citation risk review."}],
                "source_notes": [
                    {"title": "retrieval snippet", "type": "source_note", "content": "source does not mention dosage"},
                    {"title": "citation mismatch", "type": "trace", "content": "claim unsupported by retrieved text"},
                ],
                "candidate_outputs": [
                    {"summary": "States unsupported dosage claim."},
                    {"summary": "Adds caveat and asks for citation."},
                ],
                "trace": [{"stage": "retrieval", "issue": "citation mismatch"}],
                "current_plan": ["compare claim to source", "rewrite with caveat"],
                "completed_steps": ["collected retrieved snippets"],
                "blocked_steps": ["need source verification"],
                "agents": ["researcher", "citation reviewer", "answer editor"],
                "workstreams": ["claim extraction", "source matching", "safe rewrite"],
                "ownership_scopes": ["retrieval", "citation verification", "final answer"],
                "tool_results": [{"tool": "retrieval", "status": "partial", "issue": "mismatch"}],
                "rubric": ["flags unsupported claims", "avoids invented medical facts"],
                "constraints": ["do not invent clinical facts", "escalate uncertainty"],
                "requirements": ["claim list", "citation plan", "safe rewrite"],
                "example_payload": {"task": "audit citation risk"},
                "token_budget": 900,
            },
            "contrast_output",
        ),
    ]


def _finding(code: str, severity: FindingSeverity, message: str, probe_id: str | None = None, evidence: Any = None) -> APlusFinding:
    return APlusFinding(code=code, severity=severity, message=message, probe_id=probe_id, evidence=evidence)


def _extract_output(envelope: Any) -> dict[str, Any]:
    if isinstance(envelope, dict) and isinstance(envelope.get("output"), dict):
        return envelope["output"]
    return envelope if isinstance(envelope, dict) else {"raw": envelope}


def _jsonish_text(value: Any, *, max_chars: int = 30000) -> str:
    try:
        return json.dumps(value, sort_keys=True, default=str)[:max_chars].lower()
    except Exception:
        return str(value)[:max_chars].lower()


def _word_set(value: Any) -> set[str]:
    text = _jsonish_text(value)
    return {item for item in re.findall(r"[a-z0-9_]{3,}", text) if item not in {"the", "and", "for", "with", "this", "that", "from"}}


def _details(output: dict[str, Any]) -> dict[str, Any]:
    value = output.get("details")
    return value if isinstance(value, dict) else {}


def _scores(output: dict[str, Any]) -> dict[str, Any]:
    value = output.get("scores")
    return value if isinstance(value, dict) else {}


def _diagnostics(output: dict[str, Any]) -> dict[str, Any]:
    value = output.get("diagnostics")
    return value if isinstance(value, dict) else {}


def _non_empty_detail_keys(output: dict[str, Any]) -> set[str]:
    return {key for key, value in _details(output).items() if value not in (None, "", [], {})}


def _required_detail_hints(metadata: dict[str, Any] | None, output: dict[str, Any] | None = None) -> set[str]:
    text_parts = []
    if metadata:
        text_parts.extend(str(metadata.get(key, "")) for key in ["slug", "name", "logic_profile_id", "category", "capability_type"])
    if output:
        details = _details(output)
        diagnostics = _diagnostics(output)
        text_parts.extend(str(details.get("logic_profile_id", "")) for _ in [0])
        text_parts.extend(str(diagnostics.get("logic_profile_id", "")) for _ in [0])
    haystack = " ".join(text_parts).lower()
    for marker, keys in PROFILE_DETAIL_HINTS:
        if marker in haystack:
            return set(keys)
    return set()


def _looks_generic_or_fallback(output: dict[str, Any]) -> bool:
    text = _jsonish_text(output)
    bad_markers = [
        "fallback applied",
        "capability_profile_error",
        "no-op analysis",
        "placeholder logic",
        "core logic produced an empty result",
        "generic backlog",
        "next_plugin_specs",
    ]
    return any(marker in text for marker in bad_markers)


def _action_text(actions: Any) -> str:
    if not isinstance(actions, list):
        return ""
    parts: list[str] = []
    for item in actions:
        if isinstance(item, dict):
            parts.append(str(item.get("action") or item.get("title") or item))
        else:
            parts.append(str(item))
    return " ".join(parts)


def _validate_probe_output(
    output: dict[str, Any],
    probe: APlusProbe,
    *,
    metadata: dict[str, Any] | None = None,
) -> tuple[list[APlusFinding], float]:
    findings: list[APlusFinding] = []
    points = 0.0

    if not isinstance(output, dict):
        return [_finding("output_not_dict", "blocker", "Output is not a dict.", probe.probe_id)], 0.0

    missing_top = sorted(REQUIRED_TOP_LEVEL_KEYS - set(output.keys()))
    if missing_top:
        findings.append(_finding("missing_top_level_keys", "blocker", "Missing A+ top-level keys.", probe.probe_id, missing_top))
    else:
        points += 0.14

    details = _details(output)
    scores = _scores(output)
    diagnostics = _diagnostics(output)
    progress = output.get("progress_state") if isinstance(output.get("progress_state"), dict) else {}
    fun = output.get("fun_mode") if isinstance(output.get("fun_mode"), dict) else {}

    if isinstance(output.get("summary"), str) and len(output["summary"].strip()) >= 35:
        points += 0.06
    else:
        findings.append(_finding("weak_summary", "error", "Summary is missing or too thin.", probe.probe_id))
    if isinstance(output.get("primary_insights"), list) and len(output["primary_insights"]) >= 2:
        points += 0.08
    else:
        findings.append(_finding("weak_insights", "error", "A+ output needs at least two insights.", probe.probe_id))
    if isinstance(output.get("recommended_actions"), list) and len(output["recommended_actions"]) >= 2 and len(_action_text(output["recommended_actions"])) >= 30:
        points += 0.10
    else:
        findings.append(_finding("weak_actions", "error", "A+ output needs concrete recommended actions.", probe.probe_id))

    confidence = scores.get("confidence")
    usefulness = scores.get("usefulness")
    if isinstance(confidence, (int, float)) and isinstance(usefulness, (int, float)):
        points += 0.12
        if probe.expectation in {"useful_output", "contrast_output"} and float(usefulness) < 0.6:
            findings.append(_finding("low_usefulness", "warning", "Useful probes should target usefulness >= 0.6.", probe.probe_id, usefulness))
    else:
        findings.append(_finding("missing_confidence_usefulness", "blocker", "scores must include numeric confidence and usefulness.", probe.probe_id, scores))

    missing_diagnostics = sorted(REQUIRED_DIAGNOSTIC_KEYS - set(diagnostics.keys()))
    if missing_diagnostics:
        findings.append(_finding("thin_diagnostics", "blocker", "Diagnostics do not expose semantic input fields.", probe.probe_id, missing_diagnostics))
    else:
        points += 0.16

    if fun.get("celebratory_microcopy") and fun.get("microcopy"):
        points += 0.04
    else:
        findings.append(_finding("thin_fun_mode", "error", "fun_mode must include celebratory_microcopy and microcopy.", probe.probe_id))

    non_empty_keys = _non_empty_detail_keys(output)
    if probe.expectation in {"useful_output", "contrast_output"}:
        required_hints = _required_detail_hints(metadata, output)
        missing_hints = sorted(required_hints - set(details.keys()))
        if missing_hints:
            findings.append(_finding("missing_profile_detail_keys", "blocker", "Output does not include profile-specific detail keys.", probe.probe_id, missing_hints))
        elif required_hints:
            points += 0.12
        elif len(non_empty_keys - GENERIC_DETAIL_KEYS) >= 2:
            points += 0.08
        else:
            findings.append(_finding("metadata_only_details", "blocker", "Details look metadata-only.", probe.probe_id, sorted(non_empty_keys)))
        if details.get("missing_inputs"):
            findings.append(_finding("unexpected_missing_inputs", "error", "Useful A+ probe should not report missing inputs.", probe.probe_id, details.get("missing_inputs")))
        if diagnostics.get("semantic_probe_ready") is False:
            findings.append(_finding("semantic_probe_not_ready", "error", "Useful A+ probe should be semantic-probe ready.", probe.probe_id))
        else:
            points += 0.05

    if probe.expectation == "missing_input":
        if details.get("missing_inputs") and progress.get("blockers"):
            points += 0.12
        else:
            findings.append(_finding("missing_input_not_reported", "blocker", "Empty payload must produce missing_inputs and blockers.", probe.probe_id))
        if diagnostics.get("has_user_input") is False and diagnostics.get("used_goal_fallback") is True:
            points += 0.08
        else:
            findings.append(_finding("goal_counted_as_input", "blocker", "Empty payload must not count plugin goal as user input.", probe.probe_id, diagnostics))

    if probe.expectation == "payload_warning":
        warnings = details.get("payload_warnings")
        if isinstance(warnings, list) and any("not a dict" in str(item).lower() for item in warnings):
            points += 0.12
        else:
            findings.append(_finding("payload_warning_missing", "blocker", "Non-dict payload warning was not preserved.", probe.probe_id, warnings))
        if diagnostics.get("payload_warning_count", 0):
            points += 0.04
        else:
            findings.append(_finding("payload_warning_count_missing", "error", "Diagnostics must count payload warnings.", probe.probe_id, diagnostics))

    if _looks_generic_or_fallback(output):
        findings.append(_finding("generic_or_fallback_output", "blocker", "Output contains fallback/generic markers.", probe.probe_id))
    else:
        points += 0.08

    return findings, points


def _contrast_findings(outputs: dict[str, dict[str, Any]]) -> tuple[list[APlusFinding], float]:
    useful = outputs.get("useful_payload")
    contrast = outputs.get("contrast_payload")
    if not useful or not contrast:
        return [_finding("missing_contrast_outputs", "blocker", "A+ contrast outputs are missing.")], 0.0
    decision_a = {
        "summary": useful.get("summary"),
        "primary_insights": useful.get("primary_insights"),
        "recommended_actions": useful.get("recommended_actions"),
        "scores": useful.get("scores"),
        "details": useful.get("details"),
        "progress_state": useful.get("progress_state"),
    }
    decision_b = {
        "summary": contrast.get("summary"),
        "primary_insights": contrast.get("primary_insights"),
        "recommended_actions": contrast.get("recommended_actions"),
        "scores": contrast.get("scores"),
        "details": contrast.get("details"),
        "progress_state": contrast.get("progress_state"),
    }
    words_a = _word_set(decision_a)
    words_b = _word_set(decision_b)
    union = words_a | words_b
    similarity = len(words_a & words_b) / len(union) if union else 1.0
    findings: list[APlusFinding] = []
    points = 0.0
    if similarity <= 0.78:
        points += 0.16
    elif similarity <= 0.90:
        points += 0.08
        findings.append(_finding("contrast_somewhat_similar", "warning", f"A+ contrast outputs should diverge more: {similarity:.2f}", evidence={"similarity": similarity}))
    else:
        findings.append(_finding("contrast_too_similar", "blocker", f"A+ contrast outputs are too similar: {similarity:.2f}", evidence={"similarity": similarity}))
    if _scores(useful) != _scores(contrast):
        points += 0.06
    else:
        findings.append(_finding("contrast_scores_identical", "error", "A+ contrast scores must change across semantic probes."))
    if _details(useful) != _details(contrast):
        points += 0.08
    else:
        findings.append(_finding("contrast_details_identical", "error", "A+ contrast details must change across semantic probes."))
    return findings, points


async def _call_plugin(plugin_callable: Callable[..., Any], payload: Any, probe_id: str) -> dict[str, Any]:
    try:
        result = plugin_callable("a-plus-certifier", payload, run_id=f"a-plus-{probe_id}")
    except TypeError:
        result = plugin_callable(payload)
    if inspect.isawaitable(result):
        result = await result
    return _extract_output(result)


async def certify_plugin_callable(
    plugin_callable: Callable[..., Any],
    *,
    metadata: dict[str, Any] | None = None,
    threshold: float = A_PLUS_MIN_SCORE,
    probes: list[APlusProbe] | None = None,
) -> APlusCertificationResult:
    findings: list[APlusFinding] = []
    outputs: dict[str, dict[str, Any]] = {}
    points = 0.0
    probe_list = probes or build_a_plus_probes()

    for probe in probe_list:
        try:
            output = await _call_plugin(plugin_callable, probe.payload, probe.probe_id)
        except Exception as exc:
            findings.append(_finding("probe_crash", "blocker", f"A+ probe crashed: {exc}", probe.probe_id))
            continue
        outputs[probe.probe_id] = output
        probe_findings, probe_points = _validate_probe_output(output, probe, metadata=metadata)
        findings.extend(probe_findings)
        points += probe_points

    contrast_findings, contrast_points = _contrast_findings(outputs)
    findings.extend(contrast_findings)
    points += contrast_points

    score = round(min(1.2, points / max(1.0, len(probe_list) * 0.35)), 4)
    blockers = [item for item in findings if item.severity in {"error", "blocker"}]
    passed = not blockers and score >= threshold
    if passed:
        action: RecommendedAction = "certify"
    elif any(item.code in {"probe_crash", "missing_top_level_keys", "generic_or_fallback_output"} for item in findings):
        action = "regenerate"
    elif any(item.severity == "blocker" for item in findings):
        action = "repair"
    else:
        action = "repair"

    return APlusCertificationResult(
        passed=passed,
        score=score,
        findings=findings,
        probe_outputs=outputs,
        recommended_action=action,
    )


def certify_plugin_callable_sync(
    plugin_callable: Callable[..., Any],
    *,
    metadata: dict[str, Any] | None = None,
    threshold: float = A_PLUS_MIN_SCORE,
    probes: list[APlusProbe] | None = None,
) -> APlusCertificationResult:
    return asyncio.run(
        certify_plugin_callable(
            plugin_callable,
            metadata=metadata,
            threshold=threshold,
            probes=probes,
        )
    )


def summarize_a_plus_result(result: APlusCertificationResult, *, max_findings: int = 6) -> str:
    if result.passed:
        return f"a_plus: certified score {result.score:.4f} >= threshold {A_PLUS_MIN_SCORE:.2f}"
    finding_text = "; ".join(
        f"{item.code}:{item.probe_id or 'global'}:{item.message}" for item in result.findings[:max_findings]
    )
    return (
        f"a_plus: score {result.score:.4f} < threshold {A_PLUS_MIN_SCORE:.2f} "
        f"or blockers present; action={result.recommended_action}; {finding_text}"
    )
