from __future__ import annotations

import asyncio
import sys
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace

REPO_ROOT = Path(__file__).resolve().parents[1]
FRANCIS_ROOT = Path(__file__).resolve().parents[2]
for path in (REPO_ROOT, FRANCIS_ROOT):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

try:
    from factory import factory_runner
    from factory.plugin_spec import PluginSpec
    from factory.profiles import build_profile_source
except (ImportError, ModuleNotFoundError):  # pragma: no cover
    import factory_runner  # type: ignore
    from plugin_spec import PluginSpec  # type: ignore
    from profiles import build_profile_source  # type: ignore


class FactoryRunnerPromotionGateTests(unittest.TestCase):
    def test_repair_surgeon_regenerate_blocks_candidate_staging(self) -> None:
        temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(temp_dir.cleanup)
        root = Path(temp_dir.name)

        old_repair = factory_runner._repair_draft_plugin_file
        old_candidate_dir = factory_runner.CANDIDATE_PLUGINS_DIR
        old_root = factory_runner.ROOT_DIR
        factory_runner.CANDIDATE_PLUGINS_DIR = root / "candidates"
        factory_runner.ROOT_DIR = root

        def fake_repair(_path: Path, *, dry_run: bool, validate: bool):
            return SimpleNamespace(
                applied_patches=[],
                remaining_findings=["multi_profile_branch_table"],
                recommended_next_action="regenerate",
                repair_recipe={"generator_feedback": ["regenerate with profile dispatcher"]},
            )

        factory_runner._repair_draft_plugin_file = fake_repair
        self.addCleanup(setattr, factory_runner, "_repair_draft_plugin_file", old_repair)
        self.addCleanup(setattr, factory_runner, "CANDIDATE_PLUGINS_DIR", old_candidate_dir)
        self.addCleanup(setattr, factory_runner, "ROOT_DIR", old_root)

        with self.assertRaises(factory_runner.DraftRepairGateError) as ctx:
            factory_runner._write_candidate_plugin_file("ai_bad_candidate_999999", "x = 1\n")

        self.assertEqual(ctx.exception.action, "regenerate")
        self.assertIsNotNone(ctx.exception.quarantine_path)
        self.assertTrue(ctx.exception.quarantine_path.exists())
        self.assertTrue(ctx.exception.quarantine_path.with_suffix(".py.reason.txt").exists())

    def test_unknown_profile_no_longer_gets_free_promotion_pass(self) -> None:
        spec = PluginSpec(
            name="AI Unknown Capability 999999",
            slug="ai_unknown_capability_999999",
            goal="Do something unknown.",
            category="ai_agents",
            tags=["ai"],
        )
        ok, reason = asyncio.run(factory_runner._capability_promotion_gate(Path("does_not_need_to_exist.py"), spec))

        self.assertFalse(ok)
        self.assertIn("missing registered logic profile", reason)

    def test_registered_profile_without_handwritten_spec_uses_generic_contract(self) -> None:
        spec = PluginSpec(
            name="AI Prompt Contract Designer 999999",
            slug="ai_prompt_contract_designer_999999",
            goal="Design a prompt contract with constraints, outputs, and verification checks.",
            category="ai_prompting",
            tags=["ai", "prompting"],
            use_cases=["Design prompt contracts."],
        )
        source = build_profile_source(
            factory_runner._render_profile_base_source(spec),
            spec,
            "enrichment",
            "continuous_prompt_contract_designer_profile",
            reason="generic promotion contract test",
        )
        self.assertIsNotNone(source)

        temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(temp_dir.cleanup)
        path = Path(temp_dir.name) / "ai_prompt_contract_designer_999999.py"
        path.write_text(str(source), encoding="utf-8")

        ok, reason = asyncio.run(factory_runner._capability_promotion_gate(path, spec))

        self.assertTrue(ok, reason)
        self.assertIn("generic CapabilitySpec contract passed", reason)


if __name__ == "__main__":
    unittest.main()
