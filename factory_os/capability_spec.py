from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Literal, Optional


FindingSeverity = Literal["info", "warning", "error", "blocker"]
RecommendedAction = Literal["promote", "repair", "reject_or_merge"]
PromotionAction = Literal["promote", "repair", "reject_or_merge"]


@dataclass(frozen=True)
class CapabilitySpec:
    name: str
    slug: str
    family_key: str
    purpose: str
    owns: list[str] = field(default_factory=list)
    does_not_own: list[str] = field(default_factory=list)
    required_inputs: list[str] = field(default_factory=list)
    optional_inputs: list[str] = field(default_factory=list)
    required_detail_keys: list[str] = field(default_factory=list)
    required_scores: list[str] = field(default_factory=list)
    forbidden_detail_keys: list[str] = field(default_factory=list)
    logic_profile_ids: list[str] = field(default_factory=list)
    semantic_probe_ids: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class LogicProfile:
    profile_id: str
    aliases: list[str] = field(default_factory=list)
    purpose: str = ""
    required_behavior: str = ""
    forbidden_behavior: list[str] = field(default_factory=list)
    required_detail_keys: list[str] = field(default_factory=list)
    required_scores: list[str] = field(default_factory=list)
    allowed_result_modes: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class SemanticProbe:
    probe_id: str
    name: str
    payload: Any
    expected_min_scores: dict[str, float] = field(default_factory=dict)
    expected_max_scores: dict[str, float] = field(default_factory=dict)
    required_detail_keys: list[str] = field(default_factory=list)
    forbidden_detail_keys: list[str] = field(default_factory=list)
    expected_decision_values: Optional[list[str]] = None


@dataclass(frozen=True)
class SemanticContract:
    spec_slug: str
    probes: list[SemanticProbe] = field(default_factory=list)
    structural_requirements: dict[str, Any] = field(default_factory=dict)
    semantic_requirements: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class ValidationFinding:
    code: str
    severity: FindingSeverity
    message: str
    path: Optional[str] = None
    evidence: Any = None


@dataclass(frozen=True)
class ValidationResult:
    passed: bool
    findings: list[ValidationFinding] = field(default_factory=list)
    scores: dict[str, float] = field(default_factory=dict)
    recommended_action: RecommendedAction = "promote"


@dataclass(frozen=True)
class CanonicalCapabilityRecord:
    slug: str
    name: str
    family_key: str
    owns: list[str] = field(default_factory=list)
    does_not_own: list[str] = field(default_factory=list)
    input_signature: list[str] = field(default_factory=list)
    output_signature: list[str] = field(default_factory=list)
    logic_profile_ids: list[str] = field(default_factory=list)
    version: str = "0.1.0"


@dataclass(frozen=True)
class PromotionDecision:
    decision: PromotionAction
    reason: str
    validation_result: ValidationResult
    canonical_record: Optional[CanonicalCapabilityRecord] = None

