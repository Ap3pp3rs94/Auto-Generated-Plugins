from __future__ import annotations

import asyncio
import inspect
from typing import Any, Callable

from .capability_spec import (
    CapabilitySpec,
    LogicProfile,
    SemanticContract,
    SemanticProbe,
    ValidationFinding,
    ValidationResult,
)


REQUIRED_TOP_LEVEL = {
    "summary",
    "primary_insights",
    "recommended_actions",
    "scores",
    "details",
    "progress_state",
    "user_experience",
}


def _finding(code: str, severity: str, message: str, path: str | None = None, evidence: Any = None) -> ValidationFinding:
    return ValidationFinding(code=code, severity=severity, message=message, path=path, evidence=evidence)  # type: ignore[arg-type]


def _extract_output(envelope: Any) -> dict[str, Any]:
    if isinstance(envelope, dict) and isinstance(envelope.get("output"), dict):
        return envelope["output"]
    return envelope if isinstance(envelope, dict) else {"raw": envelope}


def _details(output: dict[str, Any]) -> dict[str, Any]:
    details = output.get("details")
    return details if isinstance(details, dict) else {}


def _scores(output: dict[str, Any]) -> dict[str, Any]:
    scores = output.get("scores")
    return scores if isinstance(scores, dict) else {}


def _contains_generic_backlog(output: dict[str, Any]) -> bool:
    details = _details(output)
    if any(key in details for key in ["backlog_items", "next_plugin_specs", "github_publish_plan", "release_package", "repair_plan"]):
        return True
    text = str(output).lower()
    return "highest-leverage capability factory backlog" in text or "next_plugin_specs" in text


def _is_metadata_only(output: dict[str, Any]) -> bool:
    details = _details(output)
    if not details:
        return True
    decision_keys = {
        "duplicate_risks",
        "uniqueness_fingerprint",
        "comparison_targets",
        "merge_or_reject_decision",
        "max_similarity",
        "missing_inputs",
    }
    meaningful = [key for key in decision_keys if key in details and details.get(key) not in (None, "", [], {})]
    if details.get("merge_or_reject_decision") == "insufficient_input" and details.get("missing_inputs"):
        return False
    return len(meaningful) < 3


def validate_plugin_output_against_spec(
    output: dict[str, Any],
    spec: CapabilitySpec,
    profile: LogicProfile,
    probe: SemanticProbe | None = None,
) -> ValidationResult:
    findings: list[ValidationFinding] = []
    if not isinstance(output, dict):
        findings.append(_finding("output_not_dict", "blocker", "Output is not a dict."))
        return ValidationResult(False, findings, {}, "reject_or_merge")

    missing_top = sorted(REQUIRED_TOP_LEVEL - set(output.keys()))
    for key in missing_top:
        findings.append(_finding("missing_top_level_key", "blocker", f"Missing top-level key {key!r}.", key))

    details = _details(output)
    scores = _scores(output)
    if not isinstance(output.get("details"), dict):
        findings.append(_finding("details_not_dict", "blocker", "details must be a dict.", "details"))
    if not isinstance(output.get("scores"), dict):
        findings.append(_finding("scores_not_dict", "blocker", "scores must be a dict.", "scores"))

    required_scores = sorted(set(spec.required_scores) | set(profile.required_scores))
    for score_key in required_scores:
        value = scores.get(score_key)
        if not isinstance(value, (int, float)):
            findings.append(_finding("missing_required_score", "blocker", f"Missing numeric score {score_key!r}.", f"scores.{score_key}", value))

    required_detail_keys = sorted(set(spec.required_detail_keys) | set(profile.required_detail_keys))
    if probe is not None:
        required_detail_keys = sorted(set(required_detail_keys) | set(probe.required_detail_keys))
    for key in required_detail_keys:
        if key not in details:
            findings.append(_finding("missing_required_detail_key", "blocker", f"Missing detail key {key!r}.", f"details.{key}"))

    forbidden_keys = sorted(set(spec.forbidden_detail_keys) | set(probe.forbidden_detail_keys if probe else []))
    for key in forbidden_keys:
        if key in details:
            findings.append(_finding("forbidden_detail_key", "blocker", f"Forbidden detail key {key!r} is present.", f"details.{key}", details.get(key)))

    decision = details.get("merge_or_reject_decision")
    if profile.allowed_result_modes and decision not in profile.allowed_result_modes:
        findings.append(
            _finding(
                "invalid_decision_value",
                "blocker",
                f"merge_or_reject_decision must be one of {profile.allowed_result_modes}, got {decision!r}.",
                "details.merge_or_reject_decision",
                decision,
            )
        )
    if probe and probe.expected_decision_values and decision not in probe.expected_decision_values:
        findings.append(
            _finding(
                "probe_decision_mismatch",
                "blocker",
                f"Probe {probe.probe_id} expected decision in {probe.expected_decision_values}, got {decision!r}.",
                "details.merge_or_reject_decision",
                decision,
            )
        )

    duplicate_risk = scores.get("duplicate_risk")
    max_similarity = details.get("max_similarity")
    if isinstance(duplicate_risk, (int, float)) and isinstance(max_similarity, (int, float)):
        if decision == "merge_or_reject" and duplicate_risk < min(0.3, float(max_similarity)):
            findings.append(_finding("duplicate_risk_inconsistent", "error", "duplicate_risk is too low for merge_or_reject.", "scores.duplicate_risk"))
        if float(duplicate_risk) + 0.25 < float(max_similarity):
            findings.append(_finding("duplicate_risk_inconsistent", "error", "duplicate_risk is not consistent with max_similarity.", "scores.duplicate_risk"))

    for score_key, minimum in (probe.expected_min_scores if probe else {}).items():
        value = scores.get(score_key)
        if not isinstance(value, (int, float)) or float(value) < minimum:
            findings.append(_finding("probe_score_too_low", "blocker", f"Probe expected {score_key} >= {minimum}, got {value!r}.", f"scores.{score_key}", value))
    for score_key, maximum in (probe.expected_max_scores if probe else {}).items():
        value = scores.get(score_key)
        if not isinstance(value, (int, float)) or float(value) > maximum:
            findings.append(_finding("probe_score_too_high", "blocker", f"Probe expected {score_key} <= {maximum}, got {value!r}.", f"scores.{score_key}", value))

    probe_id = probe.probe_id if probe else ""
    if probe_id in {"empty_payload_missing_input_test", "non_dict_payload_test"}:
        if decision != "insufficient_input":
            findings.append(_finding("missing_input_probe_failed", "blocker", "Missing-input probe must produce insufficient_input.", "details.merge_or_reject_decision"))
        if not details.get("missing_inputs"):
            findings.append(_finding("missing_inputs_not_reported", "blocker", "Missing-input probe must report missing_inputs.", "details.missing_inputs"))
    if probe_id == "duplicate_existing_plugin_test":
        if decision not in {"merge_or_reject", "redesign_boundary"}:
            findings.append(_finding("duplicate_probe_failed", "blocker", "Duplicate probe must merge/reject or redesign.", "details.merge_or_reject_decision"))
    if probe_id == "unique_capability_test":
        if decision != "generate_new":
            findings.append(_finding("unique_probe_failed", "blocker", "Unique probe must generate_new unless evidence says otherwise.", "details.merge_or_reject_decision"))

    if _is_metadata_only(output):
        findings.append(_finding("metadata_only_behavior", "blocker", "Output looks like metadata-only relabeling, not capability behavior."))
    if _contains_generic_backlog(output):
        findings.append(_finding("generic_backlog_behavior", "blocker", "Overlap checker output contains generic backlog/release/repair fields."))

    blockers = [item for item in findings if item.severity in {"error", "blocker"}]
    recommended = "promote" if not blockers else "repair"
    return ValidationResult(not blockers, findings, {key: float(value) for key, value in scores.items() if isinstance(value, (int, float))}, recommended)  # type: ignore[arg-type]


async def _call_plugin(plugin_callable: Callable[..., Any], payload: Any) -> dict[str, Any]:
    try:
        result = plugin_callable("semantic-contract", payload, run_id="semantic-contract")
    except TypeError:
        result = plugin_callable(payload)
    if inspect.isawaitable(result):
        result = await result
    return _extract_output(result)


async def run_semantic_contract_async(
    plugin_callable: Callable[..., Any],
    spec: CapabilitySpec,
    profile: LogicProfile,
    contract: SemanticContract,
) -> ValidationResult:
    findings: list[ValidationFinding] = []
    scores: dict[str, float] = {}
    for probe in contract.probes:
        try:
            output = await _call_plugin(plugin_callable, probe.payload)
        except Exception as exc:
            findings.append(_finding("probe_crash", "blocker", f"Probe {probe.probe_id} crashed: {exc}", evidence=probe.probe_id))
            continue
        probe_result = validate_plugin_output_against_spec(output, spec, profile, probe)
        scores.update({f"{probe.probe_id}.{key}": value for key, value in probe_result.scores.items()})
        findings.extend(probe_result.findings)
    blockers = [item for item in findings if item.severity in {"error", "blocker"}]
    return ValidationResult(not blockers, findings, scores, "promote" if not blockers else "repair")


def run_semantic_contract(
    plugin_callable: Callable[..., Any],
    spec: CapabilitySpec,
    contract: SemanticContract,
) -> ValidationResult:
    from .logic_profiles import get_logic_profile

    profile = get_logic_profile(spec.logic_profile_ids[0])
    if profile is None:
        return ValidationResult(
            False,
            [_finding("missing_logic_profile", "blocker", f"No logic profile registered for {spec.logic_profile_ids[0]!r}.")],
            {},
            "reject_or_merge",
        )
    return asyncio.run(run_semantic_contract_async(plugin_callable, spec, profile, contract))

