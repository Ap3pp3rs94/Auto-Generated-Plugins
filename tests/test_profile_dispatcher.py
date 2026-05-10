from __future__ import annotations

import asyncio
import importlib.util
import tempfile
import unittest
from pathlib import Path
import sys


REPO_ROOT = Path(__file__).resolve().parents[1]
FRANCIS_ROOT = Path(__file__).resolve().parents[2]
for path in (REPO_ROOT, FRANCIS_ROOT):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

try:
    from factory.factory_runner import _render_profile_base_source
    from factory.plugin_spec import PluginSpec
    from factory.profiles import build_profile_source
    from factory.profiles.dispatcher import resolve_logic_profile, run_profile_logic
except ModuleNotFoundError:
    from factory_runner import _render_profile_base_source  # type: ignore
    from plugin_spec import PluginSpec  # type: ignore
    from profiles import build_profile_source  # type: ignore
    from profiles.dispatcher import resolve_logic_profile, run_profile_logic  # type: ignore


MANIFEST = {"name": "Test Capability", "slug": "test_capability"}


def capability_spec() -> dict:
    return {
        "name": "AI Capability Overlap Checker",
        "slug": "ai_capability_overlap_checker",
        "purpose": "Detect duplicate or overlapping capabilities.",
        "owns": ["capability boundary comparison", "duplicate risk scoring"],
        "does_not_own": ["release packaging", "backlog planning"],
        "required_inputs": ["candidate_capability", "existing_plugins"],
        "required_detail_keys": ["duplicate_risks", "merge_or_reject_decision"],
        "required_scores": ["confidence", "usefulness", "duplicate_risk"],
        "forbidden_detail_keys": ["backlog_items", "next_plugin_specs"],
        "required_behavior": "Compare a proposed capability with existing capability records.",
        "forbidden_behavior": ["produce backlog roadmaps", "package releases"],
    }


class ProfileDispatcherTests(unittest.TestCase):
    def test_empty_payload_reports_missing_inputs_and_blockers(self) -> None:
        output = run_profile_logic("plugin_quality_gate_designer_profile", None, {}, {}, MANIFEST)

        self.assertTrue(output["details"]["missing_inputs"], output)
        self.assertTrue(output["progress_state"]["blockers"], output)
        self.assertLess(output["scores"]["confidence"], 0.8)

    def test_non_dict_payload_exposes_warning(self) -> None:
        output = run_profile_logic("plugin_quality_gate_designer_profile", None, "make me a plugin", {}, MANIFEST)

        self.assertTrue(
            any("not a dict" in warning for warning in output["details"]["payload_warnings"]),
            output,
        )

    def test_quality_gate_designer_outputs_machine_readable_gates(self) -> None:
        output = run_profile_logic(
            "plugin_quality_gate_designer_profile",
            None,
            {"capability_spec": capability_spec()},
            {},
            MANIFEST,
        )

        gates = output["details"]["quality_gates"]
        self.assertTrue(gates)
        self.assertTrue(all(isinstance(gate, dict) for gate in gates))
        self.assertTrue(all("gate_id" in gate for gate in gates))
        self.assertNotIsInstance(gates[0], str)

    def test_logic_blueprint_derives_stages_from_capability_spec(self) -> None:
        output = run_profile_logic(
            "plugin_logic_blueprint_designer_profile",
            None,
            {"capability_spec": capability_spec()},
            {},
            MANIFEST,
        )

        blueprint_text = repr(output["details"]["logic_blueprint"])
        self.assertIn("candidate_capability", blueprint_text)
        self.assertIn("duplicate risk scoring", blueprint_text)
        self.assertIn("duplicate_risks", blueprint_text)

    def test_test_payload_generator_derives_probes_from_behavior_contract(self) -> None:
        output = run_profile_logic(
            "plugin_test_payload_generator_profile",
            None,
            {"capability_spec": capability_spec()},
            {},
            MANIFEST,
        )

        payload_text = repr(output["details"]["test_payloads"])
        self.assertIn("Compare a proposed capability", payload_text)
        self.assertIn("produce backlog roadmaps", payload_text)
        self.assertIn("backlog_items", payload_text)

    def test_overlap_aliases_resolve_to_canonical_dispatch_profile(self) -> None:
        for alias in [
            "capability_overlap_checker_profile",
            "continuous_capability_overlap_checker_profile",
            "plugin_duplicate_detector_profile",
            "ai_capability_overlap_checker",
        ]:
            with self.subTest(alias=alias):
                self.assertEqual(resolve_logic_profile(alias), "capability_overlap_checker_profile")

    def test_generated_dispatch_sources_do_not_embed_unrelated_profile_branches(self) -> None:
        for slug, profile_id in [
            ("ai_plugin_spec_architect", "plugin_spec_architect_profile"),
            ("ai_plugin_quality_gate_designer", "plugin_quality_gate_designer_profile"),
            ("ai_plugin_logic_blueprint_designer", "plugin_logic_blueprint_designer_profile"),
            ("ai_plugin_test_payload_generator", "plugin_test_payload_generator_profile"),
            ("ai_plugin_duplicate_detector", "capability_overlap_checker_profile"),
            ("ai_plugin_repair_strategy_planner", "plugin_repair_strategy_planner_profile"),
            ("ai_plugin_release_packager", "plugin_release_packager_profile"),
            ("ai_plugin_factory_backlog_planner", "plugin_factory_backlog_planner_profile"),
            ("ai_plugin_profile_gap_detector", "plugin_profile_gap_detector_profile"),
            ("ai_semantic_probe_result_analyzer", "semantic_probe_result_analyzer_profile"),
            ("ai_release_readiness_scorecard", "release_readiness_scorecard_profile"),
        ]:
            with self.subTest(slug=slug):
                spec = PluginSpec(
                    name=slug.replace("_", " ").title(),
                    slug=slug,
                    category="ai_plugin_factory",
                    goal="Test dispatcher source generation.",
                    tags=["ai", "factory"],
                    use_cases=["test dispatcher"],
                )
                source = build_profile_source(
                    _render_profile_base_source(spec),
                    spec,
                    "system_automation",
                    profile_id,
                    reason="test dispatcher",
                )
                self.assertIsNotNone(source)
                source = str(source)
                self.assertIn("run_profile_logic", source)
                self.assertNotIn("elif logic_profile_id ==", source)
                self.assertNotIn("if logic_profile_id ==", source)
                self.assertNotIn("backlog_items", source)
                self.assertNotIn("next_plugin_specs", source)

    def test_generated_invoke_preserves_non_dict_payload_warning(self) -> None:
        spec = PluginSpec(
            name="AI Plugin Quality Gate Designer",
            slug="ai_plugin_quality_gate_designer",
            category="ai_plugin_factory",
            goal="Design gates.",
            tags=["ai", "factory"],
            use_cases=["design gates"],
        )
        source = build_profile_source(
            _render_profile_base_source(spec),
            spec,
            "system_automation",
            "plugin_quality_gate_designer_profile",
            reason="test dispatcher",
        )
        self.assertIsNotNone(source)
        temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(temp_dir.cleanup)
        path = Path(temp_dir.name) / "generated_plugin.py"
        path.write_text(str(source), encoding="utf-8")
        module_spec = importlib.util.spec_from_file_location("generated_plugin", path)
        self.assertIsNotNone(module_spec)
        self.assertIsNotNone(module_spec.loader)
        module = importlib.util.module_from_spec(module_spec)
        module_spec.loader.exec_module(module)  # type: ignore[union-attr]

        result = asyncio.run(module.invoke("tester", "make me gates"))

        warnings = result["output"]["details"]["payload_warnings"]
        self.assertTrue(any("not a dict" in warning for warning in warnings), result)


if __name__ == "__main__":
    unittest.main()
