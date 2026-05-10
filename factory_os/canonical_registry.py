from __future__ import annotations

from typing import Any, Optional

from .capability_spec import CanonicalCapabilityRecord, CapabilitySpec


_RECORDS_BY_SLUG: dict[str, CanonicalCapabilityRecord] = {}
_RECORDS_BY_FAMILY: dict[str, CanonicalCapabilityRecord] = {}


def register_canonical_capability(record: CanonicalCapabilityRecord) -> None:
    _RECORDS_BY_SLUG[record.slug] = record
    _RECORDS_BY_FAMILY[record.family_key] = record


def get_canonical_capability(slug_or_family_key: str) -> Optional[CanonicalCapabilityRecord]:
    value = str(slug_or_family_key or "")
    if value in _RECORDS_BY_SLUG:
        return _RECORDS_BY_SLUG[value]
    if value in _RECORDS_BY_FAMILY:
        return _RECORDS_BY_FAMILY[value]
    if "capability_overlap_checker" in value:
        return _RECORDS_BY_SLUG.get("ai_capability_overlap_checker")
    return None


def find_potential_overlaps(candidate: CapabilitySpec | dict[str, Any]) -> list[CanonicalCapabilityRecord]:
    if isinstance(candidate, CapabilitySpec):
        text = " ".join([candidate.slug, candidate.family_key, candidate.name, *candidate.owns]).lower()
    else:
        text = " ".join(str(candidate.get(key, "")) for key in ["slug", "family_key", "name", "purpose", "goal"]).lower()
    matches = []
    for record in _RECORDS_BY_SLUG.values():
        record_text = " ".join([record.slug, record.family_key, record.name, *record.owns]).lower()
        if record.slug in text or record.family_key in text or any(term in record_text for term in text.split()):
            matches.append(record)
    return matches


def list_canonical_capabilities() -> list[CanonicalCapabilityRecord]:
    return list(_RECORDS_BY_SLUG.values())


register_canonical_capability(
    CanonicalCapabilityRecord(
        slug="ai_capability_overlap_checker",
        name="AI Capability Overlap Checker",
        family_key="ai_plugin_factory::capability_overlap_checker",
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
        input_signature=["candidate_capability", "plugin_name", "slug", "task", "objective", "existing_plugins"],
        output_signature=[
            "duplicate_risks",
            "uniqueness_fingerprint",
            "comparison_targets",
            "merge_or_reject_decision",
            "max_similarity",
        ],
        logic_profile_ids=[
            "capability_overlap_checker_profile",
            "continuous_capability_overlap_checker_profile",
            "plugin_duplicate_detector_profile",
        ],
    )
)

