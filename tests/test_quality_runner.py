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
        build_config_from_args,
        AuditResult,
    )
    from factory.profiles import registered_profile_id
except ModuleNotFoundError:
    from quality_runner import (  # type: ignore
        PROFILE_REQUIRED_DETAIL_KEYS,
        QualityConfig,
        _profile_specific_checks,
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
        ]:
            with self.subTest(slug=slug):
                profile_id = registered_profile_id(slug)
                self.assertIn(profile_id, PROFILE_REQUIRED_DETAIL_KEYS)
                self.assertTrue(PROFILE_REQUIRED_DETAIL_KEYS[str(profile_id)])

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
