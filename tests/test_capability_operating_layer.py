from __future__ import annotations

import unittest

from factory_os.capability_specs import get_capability_spec
from factory_os.logic_profiles import get_logic_profile, normalize_logic_profile_id
from factory_os.profiles.overlap_checker import run_capability_overlap_checker
from factory_os.promotion_gate import evaluate_for_promotion
from factory_os.semantic_validator import validate_plugin_output_against_spec


class CapabilityOperatingLayerTests(unittest.TestCase):
    def _spec_profile(self):
        spec = get_capability_spec("ai_capability_overlap_checker")
        self.assertIsNotNone(spec)
        profile = get_logic_profile("capability_overlap_checker_profile")
        self.assertIsNotNone(profile)
        return spec, profile

    def test_overlap_checker_duplicate_payload_routes_to_overlap_logic(self) -> None:
        output = run_capability_overlap_checker(
            {
                "plugin_name": "AI Capability Overlap Checker",
                "objective": "Check whether a proposed AI capability overlaps existing modules.",
                "existing_plugins": [
                    {
                        "name": "AI Capability Overlap Checker 000100",
                        "slug": "ai_capability_overlap_checker_000100",
                        "family_key": "ai_plugin_factory::capability_overlap_checker",
                        "owns": ["capability boundary comparison", "duplicate risk scoring"],
                    }
                ],
            }
        )

        self.assertTrue(output["details"]["duplicate_risks"])
        self.assertIn(output["details"]["merge_or_reject_decision"], {"merge_or_reject", "redesign_boundary"})
        self.assertNotIn("backlog_items", output["details"])
        self.assertNotIn("next_plugin_specs", output["details"])
        self.assertGreater(output["scores"]["duplicate_risk"], 0.3)

    def test_overlap_checker_unique_payload_generates_new(self) -> None:
        output = run_capability_overlap_checker(
            {
                "plugin_name": "Cordyceps Incubation Humidity Drift Analyzer",
                "objective": "Analyze humidity drift in cordyceps incubation chambers and recommend sensor calibration actions.",
                "existing_plugins": [
                    {"name": "AI Capability Overlap Checker", "slug": "ai_capability_overlap_checker"},
                    {"name": "Plugin Release Packager", "slug": "plugin_release_packager"},
                ],
            }
        )

        self.assertEqual(output["details"]["merge_or_reject_decision"], "generate_new")
        self.assertLessEqual(output["scores"]["duplicate_risk"], 0.35)

    def test_overlap_checker_empty_payload_reports_missing_input(self) -> None:
        output = run_capability_overlap_checker({})

        self.assertEqual(output["details"]["merge_or_reject_decision"], "insufficient_input")
        self.assertTrue(output["details"]["missing_inputs"])
        self.assertTrue(output["progress_state"]["blockers"])

    def test_logic_profile_aliases_resolve_to_canonical_profile(self) -> None:
        for alias in [
            "continuous_capability_overlap_checker_profile",
            "plugin_duplicate_detector_profile",
            "capability_overlap_checker_profile",
        ]:
            with self.subTest(alias=alias):
                self.assertEqual(normalize_logic_profile_id(alias), "capability_overlap_checker_profile")

    def test_semantic_validator_rejects_generic_backlog_output_for_overlap_checker(self) -> None:
        spec, profile = self._spec_profile()
        output = {
            "summary": "Generic backlog planner output that should not pass overlap checking.",
            "primary_insights": [{"title": "Backlog", "detail": "Build next plugins"}],
            "recommended_actions": [{"action": "Build the highest-leverage capability factory backlog item"}],
            "scores": {"confidence": 0.8, "usefulness": 0.8, "duplicate_risk": 0.0},
            "details": {
                "backlog_items": [],
                "next_plugin_specs": [],
                "merge_or_reject_decision": "generate_new",
            },
            "progress_state": {},
            "user_experience": {},
        }

        result = validate_plugin_output_against_spec(output, spec, profile)

        self.assertFalse(result.passed)
        self.assertIn("generic_backlog_behavior", {finding.code for finding in result.findings})

    def test_promotion_gate_repairs_good_shell_wrong_behavior(self) -> None:
        spec, profile = self._spec_profile()
        output = {
            "summary": "Generic backlog planner output that has a shell but wrong behavior.",
            "primary_insights": [{"title": "Backlog", "detail": "Build next plugins"}],
            "recommended_actions": [{"action": "Build next plugin"}],
            "scores": {"confidence": 0.8, "usefulness": 0.8, "duplicate_risk": 0.0},
            "details": {
                "duplicate_risks": [],
                "uniqueness_fingerprint": [],
                "comparison_targets": [],
                "merge_or_reject_decision": "generate_new",
                "max_similarity": 0.0,
                "missing_inputs": [],
                "backlog_items": [],
            },
            "progress_state": {},
            "user_experience": {},
        }
        validation = validate_plugin_output_against_spec(output, spec, profile)
        decision = evaluate_for_promotion(output, spec, profile, validation)

        self.assertEqual(decision.decision, "repair")

    def test_promotion_gate_promotes_valid_overlap_checker_output(self) -> None:
        spec, profile = self._spec_profile()
        output = run_capability_overlap_checker(
            {
                "plugin_name": "Cordyceps Incubation Humidity Drift Analyzer",
                "objective": "Analyze humidity drift.",
                "existing_plugins": [{"name": "AI Capability Overlap Checker"}],
            }
        )
        validation = validate_plugin_output_against_spec(output, spec, profile)
        decision = evaluate_for_promotion(output, spec, profile, validation)

        self.assertTrue(validation.passed, validation.findings)
        self.assertEqual(decision.decision, "promote")


if __name__ == "__main__":
    unittest.main()
