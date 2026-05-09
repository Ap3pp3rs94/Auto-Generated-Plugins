from __future__ import annotations

import unittest
from pathlib import Path
import sys
import tempfile
import copy


REPO_ROOT = Path(__file__).resolve().parents[1]
FRANCIS_ROOT = Path(__file__).resolve().parents[2]
for path in (REPO_ROOT, FRANCIS_ROOT):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

try:
    from factory import factory_runner as runner
    from factory.spec_builder import AI_CAPABILITY_ROADMAP, build_next_spec
    from factory.factory_runner import _canonical_retention_spec
    from factory.factory_runner import _upgrade_attempt_record, _upgrade_attempt_skip_reason
    from factory.factory_runner import _upgrade_backlog_exhausted
except ModuleNotFoundError:
    import factory_runner as runner
    from spec_builder import AI_CAPABILITY_ROADMAP, build_next_spec
    from factory_runner import _canonical_retention_spec
    from factory_runner import _upgrade_attempt_record, _upgrade_attempt_skip_reason
    from factory_runner import _upgrade_backlog_exhausted


class SpecBuilderTests(unittest.TestCase):
    def test_first_specs_are_ai_focused_and_unique(self) -> None:
        specs = [build_next_spec(i)[0] for i in range(1, 4)]

        self.assertEqual(len({spec.slug for spec in specs}), 3)
        for spec in specs:
            self.assertIn("ai", spec.tags)
            self.assertGreaterEqual(len(spec.use_cases), 6)
            self.assertEqual(spec.extra["factory_focus"], "ai_functionality_and_progress")
            self.assertTrue(spec.extra["duplicate_policy"]["slug_must_be_unique"])
            self.assertIn("fun_mode", spec.extra["expected_result_shape"])

    def test_roadmap_contains_distinct_continuous_backlog(self) -> None:
        slugs = [build_next_spec(i)[0].slug for i in range(1, len(AI_CAPABILITY_ROADMAP) + 1)]

        self.assertEqual(len(slugs), len(set(slugs)))
        self.assertGreaterEqual(len(slugs), 40)
        self.assertIn("ai_citation_need_detector", slugs)
        self.assertIn("ai_regression_watchlist_builder", slugs)
        self.assertIn("ai_autonomous_run_governor", slugs)
        self.assertIn("ai_plugin_spec_architect", slugs)
        self.assertIn("ai_plugin_quality_gate_designer", slugs)
        self.assertIn("ai_plugin_factory_backlog_planner", slugs)

    def test_post_roadmap_index_is_new_canonical_capability(self) -> None:
        existing = {build_next_spec(i)[0].slug for i in range(1, len(AI_CAPABILITY_ROADMAP) + 1)}
        expansion_spec = build_next_spec(len(AI_CAPABILITY_ROADMAP) + 1)[0]

        self.assertNotIn(expansion_spec.slug, existing)
        self.assertEqual(expansion_spec.extra["generation_round"], 1)
        self.assertTrue(expansion_spec.extra["continuous_expansion"])
        self.assertEqual(expansion_spec.slug, "ai_coding_agent_prompt_contract_designer")

    def test_upgrade_attempt_memory_skips_repeated_retry_under_same_knowledge(self) -> None:
        upgrade_spec = copy.deepcopy(build_next_spec(1)[0])
        upgrade_spec.extra = dict(upgrade_spec.extra)
        upgrade_spec.extra["generation_round"] = 2
        later_upgrade_spec = copy.deepcopy(upgrade_spec)
        later_upgrade_spec.extra = dict(later_upgrade_spec.extra)
        later_upgrade_spec.extra["generation_round"] = 3
        retention_spec = _canonical_retention_spec(upgrade_spec)
        state = {"completed": [], "next_directive": "", "upgrade_attempts": {}, "upgrade_attempt_order": []}

        _upgrade_attempt_record(
            state=state,
            source_spec=upgrade_spec,
            canonical_spec=retention_spec,
            status="rejected",
            reason="not better than canonical",
            persist=False,
        )

        reason = _upgrade_attempt_skip_reason(state, upgrade_spec)
        self.assertIsNotNone(reason)
        self.assertIn("already rejected", reason or "")
        later_reason = _upgrade_attempt_skip_reason(state, later_upgrade_spec)
        self.assertIsNotNone(later_reason)
        self.assertIn("already rejected", later_reason or "")

    def test_upgrade_backlog_exhausted_after_all_canonical_attempts_remembered(self) -> None:
        existing = {blueprint.slug for blueprint in AI_CAPABILITY_ROADMAP}
        state = {"completed": [], "next_directive": "", "upgrade_attempts": {}, "upgrade_attempt_order": []}

        self.assertFalse(_upgrade_backlog_exhausted(state, existing))

        for position, _blueprint in enumerate(AI_CAPABILITY_ROADMAP, start=1):
            upgrade_spec = copy.deepcopy(build_next_spec(position)[0])
            upgrade_spec.extra = dict(upgrade_spec.extra)
            upgrade_spec.extra["generation_round"] = 2
            retention_spec = _canonical_retention_spec(upgrade_spec)
            _upgrade_attempt_record(
                state=state,
                source_spec=upgrade_spec,
                canonical_spec=retention_spec,
                status="rejected",
                reason="not better",
                persist=False,
            )

        self.assertTrue(_upgrade_backlog_exhausted(state, existing))

    def test_existing_registered_profile_can_seed_upgrade_memory(self) -> None:
        slug = AI_CAPABILITY_ROADMAP[0].slug
        state = {"completed": [], "next_directive": "", "upgrade_attempts": {}, "upgrade_attempt_order": []}

        with tempfile.TemporaryDirectory() as tmp:
            old_plugins_dir = runner.PLUGINS_DIR
            old_registered_profile_id = runner._registered_profile_id
            try:
                runner.PLUGINS_DIR = Path(tmp)
                runner._registered_profile_id = lambda candidate: (
                    "prompt_refinement_profile" if candidate == slug else None
                )
                (Path(tmp) / f"{slug}.py").write_text(
                    "logic_profile_id = 'prompt_refinement_profile'\n",
                    encoding="utf-8",
                )

                seeded = runner._seed_retained_canonical_upgrade_memory(
                    state,
                    {slug},
                    persist=False,
                )
            finally:
                runner.PLUGINS_DIR = old_plugins_dir
                runner._registered_profile_id = old_registered_profile_id

        self.assertEqual(seeded, 1)
        self.assertTrue(_upgrade_backlog_exhausted(state, {slug}))
        record = state["upgrade_attempts"][slug]
        self.assertEqual(record["status"], "retained")
        self.assertIn("metadata-only retry is not an improvement", record["reason"])


if __name__ == "__main__":
    unittest.main()
