from __future__ import annotations

import unittest
from pathlib import Path
import sys


REPO_ROOT = Path(__file__).resolve().parents[1]
FRANCIS_ROOT = Path(__file__).resolve().parents[2]
for path in (REPO_ROOT, FRANCIS_ROOT):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

try:
    from factory.quality_runner import (
        PROFILE_REQUIRED_DETAIL_KEYS,
        QualityConfig,
        _profile_specific_checks,
        _required_detail_keys,
        _roadmap_spec_from_slug,
        build_config_from_args,
        AuditResult,
    )
    from factory.profiles import registered_profile_id
except ModuleNotFoundError:
    from quality_runner import (  # type: ignore
        PROFILE_REQUIRED_DETAIL_KEYS,
        QualityConfig,
        _profile_specific_checks,
        _required_detail_keys,
        _roadmap_spec_from_slug,
        build_config_from_args,
        AuditResult,
    )
    from profiles import registered_profile_id  # type: ignore


class QualityRunnerTests(unittest.TestCase):
    def test_config_defaults_repair_and_publish(self) -> None:
        config, _ = build_config_from_args(["--once"])

        self.assertTrue(config.repair)
        self.assertTrue(config.github_publish_enabled)
        self.assertFalse(config.loop_forever)

    def test_config_can_run_audit_only(self) -> None:
        config, _ = build_config_from_args(["--once", "--no-repair", "--no-github-publish", "--slug", "x"])

        self.assertFalse(config.repair)
        self.assertFalse(config.github_publish_enabled)
        self.assertEqual(config.slugs, ["x"])

    def test_every_registered_profile_has_required_quality_keys(self) -> None:
        for slug in [
            "ai_prompt_refinement_engine",
            "ai_tool_selection_advisor",
            "ai_capability_router",
            "ai_regression_watchlist_builder",
            "ai_grounded_answer_planner",
            "ai_tool_result_consistency_checker",
            "ai_operator_status_brief_builder",
            "ai_prompt_injection_surface_scanner",
            "ai_workflow_retry_strategy_planner",
            "ai_model_selection_scorecard",
            "ai_requirement_gap_analyzer",
            "ai_artifact_release_note_generator",
            "ai_data_contract_mapper",
            "ai_autonomous_run_governor",
            "ai_plugin_spec_architect",
            "ai_plugin_logic_blueprint_designer",
            "ai_plugin_quality_gate_designer",
            "ai_plugin_test_payload_generator",
            "ai_plugin_duplicate_detector",
            "ai_plugin_repair_strategy_planner",
            "ai_plugin_release_packager",
            "ai_plugin_factory_backlog_planner",
        ]:
            with self.subTest(slug=slug):
                profile_id = registered_profile_id(slug)
                self.assertIn(profile_id, PROFILE_REQUIRED_DETAIL_KEYS)
                self.assertTrue(PROFILE_REQUIRED_DETAIL_KEYS[str(profile_id)])

    def test_late_roadmap_profiles_require_capability_specific_outputs(self) -> None:
        expected = {
            "ai_grounded_answer_planner": ("grounded_answer_planner_profile", "answer_plan"),
            "ai_tool_result_consistency_checker": ("tool_result_consistency_checker_profile", "consistency_findings"),
            "ai_operator_status_brief_builder": ("operator_status_brief_builder_profile", "status_brief"),
            "ai_prompt_injection_surface_scanner": ("prompt_injection_surface_scanner_profile", "injection_findings"),
            "ai_workflow_retry_strategy_planner": ("workflow_retry_strategy_planner_profile", "retry_strategy"),
            "ai_model_selection_scorecard": ("model_selection_scorecard_profile", "model_scorecard"),
            "ai_requirement_gap_analyzer": ("requirement_gap_analyzer_profile", "requirement_gaps"),
            "ai_artifact_release_note_generator": ("artifact_release_note_generator_profile", "release_notes"),
            "ai_data_contract_mapper": ("data_contract_mapper_profile", "input_contract"),
            "ai_autonomous_run_governor": ("autonomous_run_governor_profile", "governance_decision"),
            "ai_plugin_spec_architect": ("plugin_spec_architect_profile", "spec_blueprint"),
            "ai_plugin_logic_blueprint_designer": ("plugin_logic_blueprint_designer_profile", "logic_blueprint"),
            "ai_plugin_quality_gate_designer": ("plugin_quality_gate_designer_profile", "quality_gates"),
            "ai_plugin_test_payload_generator": ("plugin_test_payload_generator_profile", "test_payloads"),
            "ai_plugin_duplicate_detector": ("capability_overlap_checker_profile", "duplicate_risks"),
            "ai_plugin_repair_strategy_planner": ("plugin_repair_strategy_planner_profile", "repair_plan"),
            "ai_plugin_release_packager": ("plugin_release_packager_profile", "release_package"),
            "ai_plugin_factory_backlog_planner": ("plugin_factory_backlog_planner_profile", "backlog_items"),
        }

        for slug, (profile_id, required_key) in expected.items():
            with self.subTest(slug=slug):
                self.assertEqual(registered_profile_id(slug), profile_id)
                self.assertIn(required_key, PROFILE_REQUIRED_DETAIL_KEYS[profile_id])

    def test_continuous_expansion_slug_resolves_to_spec(self) -> None:
        slug = "ai_coding_agent_prompt_contract_designer"

        spec = _roadmap_spec_from_slug(slug)

        self.assertIsNotNone(spec)
        self.assertEqual(spec.slug, slug)
        self.assertTrue(spec.extra["continuous_expansion"])
        self.assertEqual(registered_profile_id(slug), "continuous_prompt_contract_designer_profile")

    def test_legacy_verbose_continuous_slug_still_resolves_to_spec(self) -> None:
        slug = "ai_plugin_factory_agentic_planning_capability_overlap_checker"

        spec = _roadmap_spec_from_slug(slug)

        self.assertIsNotNone(spec)
        self.assertEqual(spec.slug, slug)
        self.assertTrue(spec.extra["continuous_expansion"])
        self.assertEqual(registered_profile_id(slug), "capability_overlap_checker_profile")

    def test_continuous_profiles_inherit_required_detail_keys(self) -> None:
        self.assertEqual(
            _required_detail_keys("continuous_prompt_contract_designer_profile"),
            PROFILE_REQUIRED_DETAIL_KEYS["structured_prompt_builder_profile"],
        )
        self.assertEqual(
            _required_detail_keys("continuous_tool_argument_checker_profile"),
            PROFILE_REQUIRED_DETAIL_KEYS["continuous_tool_argument_checker_profile"],
        )
        self.assertIn(
            "completeness_findings",
            _required_detail_keys("continuous_output_completeness_grader_profile"),
        )
        self.assertIn(
            "action_plan",
            _required_detail_keys("continuous_response_action_planner_profile"),
        )
        self.assertIn(
            "verification_checklist",
            _required_detail_keys("continuous_verification_checklist_builder_profile"),
        )
        self.assertIn(
            "rollback_plan",
            _required_detail_keys("continuous_rollback_guard_builder_profile"),
        )

    def test_tool_routing_probe_rejects_missing_github_tool(self) -> None:
        result = AuditResult(
            slug="ai_tool_selection_advisor",
            path=Path("plugins/ai_tool_selection_advisor.py"),
            profile_id="tool_selection_profile",
            passed=True,
        )
        output = {
            "summary": "selected clarifier",
            "primary_insights": [{"title": "Top tool"}],
            "recommended_actions": [{"action": "Use clarifying_prompt"}],
            "scores": {"confidence": 0.7},
            "details": {
                "logic_profile_id": "tool_selection_profile",
                "tool_recommendations": [{"tool": "clarifying_prompt"}],
                "selection_rationale": "No signal.",
            },
        }

        _profile_specific_checks(result, output)

        self.assertFalse(result.passed)
        self.assertTrue(any(issue.code == "weak_tool_routing" for issue in result.issues))

    def test_intent_probe_accepts_github_route(self) -> None:
        result = AuditResult(
            slug="ai_user_intent_classifier",
            path=Path("plugins/ai_user_intent_classifier.py"),
            profile_id="user_intent_classifier_profile",
            passed=True,
        )
        output = {
            "summary": "routed",
            "primary_insights": [{"title": "Route"}],
            "recommended_actions": [{"action": "Route"}],
            "scores": {"confidence": 0.7},
            "details": {
                "logic_profile_id": "user_intent_classifier_profile",
                "routes": [{"route": "github_publish_agent"}],
                "selected_route": "github_publish_agent",
                "split_needed": False,
            },
        }

        _profile_specific_checks(result, output)

        self.assertTrue(result.passed, [issue.message for issue in result.issues])


if __name__ == "__main__":
    unittest.main()
