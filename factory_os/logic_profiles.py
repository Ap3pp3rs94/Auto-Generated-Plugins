from __future__ import annotations

from typing import Optional

from .capability_spec import LogicProfile


_PROFILES: dict[str, LogicProfile] = {}
_ALIASES: dict[str, str] = {}


def register_logic_profile(profile: LogicProfile) -> None:
    _PROFILES[profile.profile_id] = profile
    _ALIASES[profile.profile_id] = profile.profile_id
    for alias in profile.aliases:
        _ALIASES[str(alias)] = profile.profile_id


def get_logic_profile(profile_id_or_alias: str) -> Optional[LogicProfile]:
    normalized = normalize_logic_profile_id(profile_id_or_alias)
    if normalized is None:
        return None
    return _PROFILES.get(normalized)


def normalize_logic_profile_id(profile_id_or_alias: str) -> Optional[str]:
    return _ALIASES.get(str(profile_id_or_alias or ""))


def list_logic_profiles() -> list[LogicProfile]:
    return list(_PROFILES.values())


CAPABILITY_OVERLAP_CHECKER_PROFILE = LogicProfile(
    profile_id="capability_overlap_checker_profile",
    aliases=[
        "continuous_capability_overlap_checker_profile",
        "plugin_duplicate_detector_profile",
        "capability_duplicate_detector",
        "ai_capability_overlap_checker",
    ],
    purpose=(
        "Compare a proposed capability against existing plugins/modules and "
        "decide whether to generate a new canonical slot, redesign boundaries, "
        "merge, or reject."
    ),
    required_behavior=(
        "Compute deterministic duplicate risks, uniqueness fingerprint, "
        "comparison targets, max similarity, and a merge/reject decision from "
        "payload values and existing plugin records."
    ),
    forbidden_behavior=[
        "generic backlog planning",
        "next plugin roadmap generation",
        "release packaging",
        "repair planning",
        "metadata-only relabeling",
    ],
    required_detail_keys=[
        "duplicate_risks",
        "uniqueness_fingerprint",
        "comparison_targets",
        "merge_or_reject_decision",
        "max_similarity",
        "missing_inputs",
    ],
    required_scores=["confidence", "usefulness", "duplicate_risk"],
    allowed_result_modes=[
        "generate_new",
        "redesign_boundary",
        "merge_or_reject",
        "insufficient_input",
    ],
)


register_logic_profile(CAPABILITY_OVERLAP_CHECKER_PROFILE)

