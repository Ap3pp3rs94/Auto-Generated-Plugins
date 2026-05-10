from __future__ import annotations

import asyncio
import tempfile
import textwrap
import unittest
from pathlib import Path
import sys


REPO_ROOT = Path(__file__).resolve().parents[1]
FRANCIS_ROOT = Path(__file__).resolve().parents[2]
for path in (REPO_ROOT, FRANCIS_ROOT):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

try:
    from factory.factory_runner import (
        _build_registered_profile_result,
        _capability_identity_gate,
        _sibling_uniqueness_gate,
    )
    from factory.plugin_spec import PluginSpec
    from factory.spec_builder import build_next_spec
except ModuleNotFoundError:
    from factory_runner import (  # type: ignore
        _build_registered_profile_result,
        _capability_identity_gate,
        _sibling_uniqueness_gate,
    )
    from plugin_spec import PluginSpec  # type: ignore
    from spec_builder import build_next_spec  # type: ignore


class CapabilityIdentityGateTests(unittest.TestCase):
    def test_tool_argument_checker_rejects_prompt_injection_only_body(self) -> None:
        source = """
async def invoke(user_id, payload, **kwargs):
    return {
        "status": "succeeded",
        "output": {
            "summary": "Tool argument checker used generic prompt-injection handling.",
            "primary_insights": [{"title": "Injection", "detail": []}],
            "recommended_actions": [{"action": "Apply prompt-injection handling rules"}],
            "scores": {"confidence": 0.9, "usefulness": 0.9},
            "details": {
                "logic_profile_id": "continuous_tool_argument_checker_profile",
                "injection_findings": [],
                "trust_boundaries": [],
                "handling_rules": [],
                "sanitized_context_plan": {},
            },
            "progress_state": {"next_step": "Apply prompt-injection handling rules"},
            "user_experience": {"plain_language_takeaway": "Generic handling only."},
            "fun_mode": {"challenge_label": "Tool Args", "celebratory_microcopy": "Done"},
            "diagnostics": {"logic_profile_id": "continuous_tool_argument_checker_profile"},
        },
        "error": "",
        "meta": {},
    }
"""
        spec = self._spec("ai_security_review_tool_argument_checker")

        ok, reason = self._run_identity(source, spec)

        self.assertFalse(ok)
        self.assertIn("missing required detail keys", reason)
        self.assertIn("argument_risks", reason)

    def test_generated_tool_argument_checker_matches_name_contract(self) -> None:
        spec, capability_type, domain = build_next_spec(322)
        spec.capability_type = capability_type
        spec.intended_domain = domain
        result = _build_registered_profile_result(
            spec=spec,
            capability_type=capability_type,
            reason="identity test",
        )

        ok, reason = self._run_identity(result.source, spec)

        self.assertTrue(ok, reason)

    def test_sibling_uniqueness_rejects_near_clone_behavior(self) -> None:
        source = """
async def invoke(user_id, payload, **kwargs):
    return {
        "status": "succeeded",
        "output": {
            "summary": "Same capability output with the same decisions and same action plan.",
            "primary_insights": [
                {"title": "Decision", "detail": "same"},
                {"title": "Evidence", "detail": "same"},
            ],
            "recommended_actions": [
                {"action": "Do the same next step", "action_plan": ["same"]},
                {"action": "Run the same checks", "next_step_checks": ["same"]},
            ],
            "scores": {"confidence": 0.9, "usefulness": 0.9, "risk": 0.1},
            "details": {
                "logic_profile_id": "continuous_response_action_planner_profile",
                "action_plan": ["same"],
                "actionability_gaps": [],
                "next_step_checks": ["same"],
                "shared_key": "same",
            },
            "progress_state": {"next_step": "Do the same next step"},
            "user_experience": {"plain_language_takeaway": "Same capability."},
            "fun_mode": {"challenge_label": "Same", "celebratory_microcopy": "Same"},
        },
        "error": "",
        "meta": {},
    }
"""
        spec = self._spec("ai_security_review_response_action_planner")
        with tempfile.TemporaryDirectory() as tmp:
            candidate = Path(tmp) / "candidate.py"
            sibling = Path(tmp) / "sibling.py"
            candidate.write_text(textwrap.dedent(source).strip() + "\n", encoding="utf-8")
            sibling.write_text(textwrap.dedent(source).strip() + "\n", encoding="utf-8")

            ok, reason = asyncio.run(
                _sibling_uniqueness_gate(candidate, spec, sibling_paths=[sibling])
            )

        self.assertFalse(ok)
        self.assertIn("too close to retained sibling", reason)

    def _run_identity(self, source: str, spec: PluginSpec) -> tuple[bool, str]:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "candidate.py"
            path.write_text(textwrap.dedent(source).strip() + "\n", encoding="utf-8")
            return asyncio.run(_capability_identity_gate(path, spec))

    def _spec(self, slug: str) -> PluginSpec:
        return PluginSpec(
            name=slug.replace("_", " ").title(),
            slug=slug,
            goal="Validate generated capability identity.",
            category="ai_safety",
            tags=["ai", "identity"],
            capability_type="scoring",
            intended_domain="AI capability validation",
        )


if __name__ == "__main__":
    unittest.main()
