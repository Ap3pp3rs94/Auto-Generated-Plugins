from __future__ import annotations

from .canonical_registry import get_canonical_capability
from .capability_spec import CapabilitySpec, LogicProfile, PromotionDecision, ValidationResult


def evaluate_for_promotion(
    plugin_output: dict,
    spec: CapabilitySpec,
    profile: LogicProfile,
    validation_result: ValidationResult,
) -> PromotionDecision:
    if validation_result.passed:
        return PromotionDecision(
            decision="promote",
            reason="structural and semantic validation passed",
            validation_result=validation_result,
            canonical_record=get_canonical_capability(spec.slug) or get_canonical_capability(spec.family_key),
        )

    codes = {finding.code for finding in validation_result.findings}
    repairable = {
        "missing_required_detail_key",
        "forbidden_detail_key",
        "generic_backlog_behavior",
        "metadata_only_behavior",
        "invalid_decision_value",
        "probe_decision_mismatch",
        "duplicate_risk_inconsistent",
        "missing_required_score",
    }
    if codes & repairable:
        return PromotionDecision(
            decision="repair",
            reason="shell is valid enough to repair semantic routing or shallow logic",
            validation_result=validation_result,
            canonical_record=get_canonical_capability(spec.slug) or get_canonical_capability(spec.family_key),
        )

    details = plugin_output.get("details") if isinstance(plugin_output.get("details"), dict) else {}
    scores = plugin_output.get("scores") if isinstance(plugin_output.get("scores"), dict) else {}
    duplicate_risk = scores.get("duplicate_risk")
    decision = details.get("merge_or_reject_decision")
    if decision == "merge_or_reject" and isinstance(duplicate_risk, (int, float)) and duplicate_risk >= 0.7:
        return PromotionDecision(
            decision="reject_or_merge",
            reason="candidate duplicates an existing canonical capability",
            validation_result=validation_result,
            canonical_record=get_canonical_capability(spec.slug) or get_canonical_capability(spec.family_key),
        )

    return PromotionDecision(
        decision="reject_or_merge",
        reason="output is unrecoverably malformed or unsafe for promotion",
        validation_result=validation_result,
        canonical_record=get_canonical_capability(spec.slug) or get_canonical_capability(spec.family_key),
    )

