from __future__ import annotations

from typing import Optional

from .capability_spec import SemanticContract, SemanticProbe


OVERLAP_CHECKER_CONTRACT = SemanticContract(
    spec_slug="ai_capability_overlap_checker",
    probes=[
        SemanticProbe(
            probe_id="duplicate_existing_plugin_test",
            name="Duplicate existing plugin test",
            payload={
                "plugin_name": "AI Capability Overlap Checker",
                "objective": "Check whether a proposed AI capability overlaps existing modules or deserves a new canonical slot.",
                "existing_plugins": [
                    {
                        "name": "AI Capability Overlap Checker 000100",
                        "slug": "ai_capability_overlap_checker_000100",
                        "family_key": "ai_plugin_factory::capability_overlap_checker",
                        "owns": [
                            "capability boundary comparison",
                            "duplicate risk scoring",
                            "merge or reject recommendation",
                        ],
                        "required_detail_keys": [
                            "duplicate_risks",
                            "uniqueness_fingerprint",
                            "merge_or_reject_decision",
                        ],
                    },
                    {
                        "name": "Plugin Duplicate Detector",
                        "slug": "plugin_duplicate_detector",
                        "owns": [
                            "detect duplicate plugin proposals",
                            "compare proposed plugin against existing plugin names",
                        ],
                    },
                ],
            },
            expected_min_scores={"duplicate_risk": 0.35},
            required_detail_keys=["duplicate_risks", "merge_or_reject_decision"],
            expected_decision_values=["merge_or_reject", "redesign_boundary"],
        ),
        SemanticProbe(
            probe_id="unique_capability_test",
            name="Unique capability test",
            payload={
                "plugin_name": "Cordyceps Incubation Humidity Drift Analyzer",
                "objective": "Analyze humidity drift in cordyceps incubation chambers and recommend sensor calibration actions.",
                "existing_plugins": [
                    {
                        "name": "AI Capability Overlap Checker",
                        "slug": "ai_capability_overlap_checker",
                        "owns": ["capability boundary comparison"],
                    },
                    {
                        "name": "Plugin Release Packager",
                        "slug": "plugin_release_packager",
                        "owns": ["release packaging", "github publish planning"],
                    },
                ],
            },
            expected_max_scores={"duplicate_risk": 0.35},
            forbidden_detail_keys=["backlog_items", "next_plugin_specs", "github_publish_plan", "release_package"],
            expected_decision_values=["generate_new"],
        ),
        SemanticProbe(
            probe_id="empty_payload_missing_input_test",
            name="Empty payload missing input test",
            payload={},
            required_detail_keys=["missing_inputs"],
            expected_decision_values=["insufficient_input"],
        ),
        SemanticProbe(
            probe_id="non_dict_payload_test",
            name="Non-dict payload test",
            payload="make me a plugin",
            required_detail_keys=["missing_inputs", "payload_warnings"],
            expected_decision_values=["insufficient_input"],
        ),
    ],
    structural_requirements={
        "required_top_level_keys": [
            "summary",
            "primary_insights",
            "recommended_actions",
            "scores",
            "details",
            "progress_state",
            "user_experience",
        ]
    },
    semantic_requirements={
        "decision_detail_key": "merge_or_reject_decision",
        "forbid_metadata_only_relabeling": True,
        "forbid_generic_backlog_guidance": True,
    },
)


_CONTRACTS = {OVERLAP_CHECKER_CONTRACT.spec_slug: OVERLAP_CHECKER_CONTRACT}


def get_semantic_contract(spec_slug_or_family_key: str) -> Optional[SemanticContract]:
    value = str(spec_slug_or_family_key or "")
    if value in _CONTRACTS:
        return _CONTRACTS[value]
    if "capability_overlap_checker" in value:
        return OVERLAP_CHECKER_CONTRACT
    return None

