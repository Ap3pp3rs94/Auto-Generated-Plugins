from __future__ import annotations

from typing import Optional

from .capability_spec import CapabilitySpec


_SPECS_BY_SLUG: dict[str, CapabilitySpec] = {}
_SPECS_BY_FAMILY: dict[str, CapabilitySpec] = {}


def register_capability_spec(spec: CapabilitySpec) -> None:
    _SPECS_BY_SLUG[spec.slug] = spec
    _SPECS_BY_FAMILY[spec.family_key] = spec


def get_capability_spec(slug_or_family_key: str) -> Optional[CapabilitySpec]:
    value = str(slug_or_family_key or "")
    if value in _SPECS_BY_SLUG:
        return _SPECS_BY_SLUG[value]
    if value in _SPECS_BY_FAMILY:
        return _SPECS_BY_FAMILY[value]
    if "capability_overlap_checker" in value:
        return _SPECS_BY_SLUG.get("ai_capability_overlap_checker")
    if value.endswith("::ai capability overlap checker"):
        return _SPECS_BY_SLUG.get("ai_capability_overlap_checker")
    return None


def list_capability_specs() -> list[CapabilitySpec]:
    return list(_SPECS_BY_SLUG.values())


OVERLAP_CHECKER_SPEC = CapabilitySpec(
    name="AI Capability Overlap Checker",
    slug="ai_capability_overlap_checker",
    family_key="ai_plugin_factory::capability_overlap_checker",
    purpose=(
        "Determine whether a proposed AI capability duplicates, overlaps, "
        "or deserves a new canonical slot."
    ),
    owns=[
        "capability boundary comparison",
        "duplicate risk scoring",
        "uniqueness fingerprinting",
        "merge/reject/redesign/generate-new recommendation",
        "comparison against existing plugin records",
    ],
    does_not_own=[
        "generating plugin specs",
        "writing full implementation blueprints",
        "packaging releases",
        "repairing failed plugins",
        "creating backlog roadmaps",
    ],
    required_inputs=[
        "candidate_capability or plugin_name or slug or task or objective",
        "existing_plugins",
    ],
    optional_inputs=["prompt", "description", "goal"],
    required_detail_keys=[
        "duplicate_risks",
        "uniqueness_fingerprint",
        "comparison_targets",
        "merge_or_reject_decision",
        "max_similarity",
        "missing_inputs",
    ],
    required_scores=["confidence", "usefulness", "duplicate_risk"],
    forbidden_detail_keys=[
        "backlog_items",
        "next_plugin_specs",
        "github_publish_plan",
        "repair_plan",
        "release_package",
    ],
    logic_profile_ids=[
        "capability_overlap_checker_profile",
        "continuous_capability_overlap_checker_profile",
        "plugin_duplicate_detector_profile",
    ],
    semantic_probe_ids=[
        "duplicate_existing_plugin_test",
        "unique_capability_test",
        "empty_payload_missing_input_test",
        "non_dict_payload_test",
    ],
)


register_capability_spec(OVERLAP_CHECKER_SPEC)

