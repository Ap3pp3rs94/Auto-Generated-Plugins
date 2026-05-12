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
    from factory.spec_builder import CONTINUOUS_EXPANSION_CONTEXTS
    from factory.spec_builder import CONTINUOUS_EXPANSION_FAMILIES
    from factory.spec_builder import CONTINUOUS_EXPANSION_MODES
    from factory.spec_builder import CONTINUOUS_EXPANSION_SURFACES
    from factory.spec_builder import CONTINUOUS_EXPANSION_TARGETS
    from factory.spec_builder import CONTINUOUS_SHORT_SLUG_START_INDEX
    from factory.factory_runner import _anticipated_capability_candidates
    from factory.factory_runner import _capability_rejection_record, _capability_rejection_skip_reason
    from factory.factory_runner import _refresh_anticipation_state
    from factory.factory_runner import _canonical_retention_spec
    from factory.factory_runner import _roadmap_slug_index
    from factory.factory_runner import _upgrade_attempt_record, _upgrade_attempt_skip_reason
    from factory.factory_runner import _upgrade_backlog_exhausted
except ModuleNotFoundError:
    import factory_runner as runner
    from spec_builder import AI_CAPABILITY_ROADMAP, build_next_spec
    from spec_builder import CONTINUOUS_EXPANSION_CONTEXTS
    from spec_builder import CONTINUOUS_EXPANSION_FAMILIES
    from spec_builder import CONTINUOUS_EXPANSION_MODES
    from spec_builder import CONTINUOUS_EXPANSION_SURFACES
    from spec_builder import CONTINUOUS_EXPANSION_TARGETS
    from spec_builder import CONTINUOUS_SHORT_SLUG_START_INDEX
    from factory_runner import _anticipated_capability_candidates
    from factory_runner import _capability_rejection_record, _capability_rejection_skip_reason
    from factory_runner import _refresh_anticipation_state
    from factory_runner import _canonical_retention_spec
    from factory_runner import _roadmap_slug_index
    from factory_runner import _upgrade_attempt_record, _upgrade_attempt_skip_reason
    from factory_runner import _upgrade_backlog_exhausted


class SpecBuilderTests(unittest.TestCase):
    def test_first_specs_are_ai_focused_and_unique(self) -> None:
        specs = [build_next_spec(i)[0] for i in range(1, 4)]

        self.assertEqual(len({spec.slug for spec in specs}), 3)
        for spec in specs:
            self.assertRegex(spec.name, r"^AI .+ \d{6}$")
            self.assertRegex(spec.slug, r"^ai_[a-z_]+_\d{6}$")
            self.assertRegex(spec.extra["display_number"], r"^\d{6}$")
            self.assertIn("canonical_name", spec.extra)
            self.assertIn("canonical_slug", spec.extra)
            self.assertIn("ai", spec.tags)
            self.assertGreaterEqual(len(spec.use_cases), 6)
            self.assertEqual(spec.extra["factory_focus"], "ai_functionality_and_progress")
            self.assertTrue(spec.extra["duplicate_policy"]["slug_must_be_unique"])
            self.assertIn("fun_mode", spec.extra["expected_result_shape"])

    def test_roadmap_contains_distinct_continuous_backlog(self) -> None:
        slugs = [build_next_spec(i)[0].slug for i in range(1, len(AI_CAPABILITY_ROADMAP) + 1)]

        self.assertEqual(len(slugs), len(set(slugs)))
        self.assertGreaterEqual(len(slugs), 40)
        self.assertIn("ai_citation_need_detector_000019", slugs)
        self.assertIn("ai_regression_watchlist_builder_000030", slugs)
        self.assertIn("ai_autonomous_run_governor_000040", slugs)
        self.assertIn("ai_plugin_spec_architect_000041", slugs)
        self.assertIn("ai_plugin_quality_gate_designer_000043", slugs)
        self.assertIn("ai_plugin_factory_backlog_planner_000048", slugs)

    def test_post_roadmap_index_is_new_canonical_capability(self) -> None:
        existing = {build_next_spec(i)[0].slug for i in range(1, len(AI_CAPABILITY_ROADMAP) + 1)}
        expansion_spec = build_next_spec(len(AI_CAPABILITY_ROADMAP) + 1)[0]

        self.assertNotIn(expansion_spec.slug, existing)
        self.assertEqual(expansion_spec.extra["generation_round"], 1)
        self.assertTrue(expansion_spec.extra["continuous_expansion"])
        self.assertEqual(expansion_spec.slug, f"ai_prompt_contract_designer_{len(AI_CAPABILITY_ROADMAP) + 1:06d}")
        self.assertEqual(expansion_spec.name, f"AI Prompt Contract Designer {len(AI_CAPABILITY_ROADMAP) + 1:06d}")
        self.assertIn("Coding Agent", expansion_spec.use_cases[0])
        self.assertIn("coding agent", expansion_spec.intended_domain.lower())

    def test_continuous_expansion_capacity_supports_large_unique_goal(self) -> None:
        capacity = (
            len(CONTINUOUS_EXPANSION_TARGETS)
            * len(CONTINUOUS_EXPANSION_FAMILIES)
            * len(CONTINUOUS_EXPANSION_CONTEXTS)
            * len(CONTINUOUS_EXPANSION_MODES)
            * len(CONTINUOUS_EXPANSION_SURFACES)
        )

        self.assertGreaterEqual(capacity, 500_000)

    def test_continuous_expansion_can_target_broad_ai_use_cases(self) -> None:
        target_slugs = {target.slug for target in CONTINUOUS_EXPANSION_TARGETS}
        self.assertIn("agriculture_ops", target_slugs)
        self.assertIn("manufacturing_ops", target_slugs)
        self.assertIn("home_maintenance", target_slugs)
        self.assertIn("gaming_community", target_slugs)

        agriculture_index = next(
            index
            for index, target in enumerate(CONTINUOUS_EXPANSION_TARGETS)
            if target.slug == "agriculture_ops"
        )
        spec_index = (
            len(AI_CAPABILITY_ROADMAP)
            + agriculture_index * len(CONTINUOUS_EXPANSION_FAMILIES)
            + 1
        )
        spec = build_next_spec(spec_index)[0]

        self.assertTrue(spec.extra["continuous_expansion"])
        self.assertIn("Agriculture Ops", spec.use_cases[0])
        self.assertIn("ai agriculture", spec.intended_domain.lower())
        self.assertTrue(spec.extra["duplicate_policy"]["plugin_must_serve_ai_workflow"])
        self.assertTrue(spec.extra["duplicate_policy"]["allow_expansive_ai_use_case_domains"])
        self.assertTrue(spec.extra["duplicate_policy"]["do_not_generate_non_ai_utilities"])

    def test_second_continuous_wave_keeps_use_case_in_metadata_not_slug(self) -> None:
        first_wave_size = len(CONTINUOUS_EXPANSION_TARGETS) * len(CONTINUOUS_EXPANSION_FAMILIES)
        next_wave_spec = build_next_spec(len(AI_CAPABILITY_ROADMAP) + first_wave_size + 1)[0]

        self.assertTrue(next_wave_spec.extra["continuous_expansion"])
        self.assertRegex(next_wave_spec.slug, r"^ai_[a-z_]+_[0-9]{6}$")
        self.assertNotIn("agentic_planning", next_wave_spec.slug)
        self.assertNotIn("_set_", next_wave_spec.slug)
        self.assertIn("agentic planning", next_wave_spec.intended_domain.lower())

    def test_future_continuous_expansion_uses_short_numbered_use_case_names(self) -> None:
        spec = build_next_spec(CONTINUOUS_SHORT_SLUG_START_INDEX)[0]

        self.assertTrue(spec.extra["continuous_expansion"])
        self.assertEqual(spec.extra["continuous_expansion_source"], "short_numbered_use_case_matrix")
        self.assertRegex(spec.slug, r"^ai_[a-z_]+_[0-9]{6}$")
        self.assertLessEqual(len(spec.slug.split("_")), 6)
        self.assertNotIn("agentic_planning", spec.slug)
        self.assertIn("distinct use case", spec.use_cases[0].lower())
        self.assertEqual(spec.extra["use_case_seed"], CONTINUOUS_SHORT_SLUG_START_INDEX)

    def test_legacy_set_slugs_do_not_advance_forward_cursor(self) -> None:
        self.assertIsNone(_roadmap_slug_index("ai_coding_agent_prompt_contract_designer_set_2"))

    def test_anticipation_candidates_skip_existing_and_describe_next_work(self) -> None:
        existing = {build_next_spec(i)[0].slug for i in range(1, len(AI_CAPABILITY_ROADMAP) + 1)}
        first_expansion = build_next_spec(len(AI_CAPABILITY_ROADMAP) + 1)[0]
        existing.add(first_expansion.slug)

        with tempfile.TemporaryDirectory() as tmp:
            old_plugins_dir = runner.PLUGINS_DIR
            try:
                runner.PLUGINS_DIR = Path(tmp)
                anticipated = _anticipated_capability_candidates(
                    existing,
                    start_index=len(AI_CAPABILITY_ROADMAP) + 1,
                    limit=3,
                )
            finally:
                runner.PLUGINS_DIR = old_plugins_dir

        self.assertEqual(len(anticipated), 3)
        self.assertNotIn(first_expansion.slug, {item["slug"] for item in anticipated})
        self.assertTrue(all(item["continuous_expansion"] for item in anticipated))
        self.assertTrue(all(item["reason"] for item in anticipated))

    def test_refresh_anticipation_state_persists_forward_context_without_plugins(self) -> None:
        existing = {build_next_spec(i)[0].slug for i in range(1, len(AI_CAPABILITY_ROADMAP) + 1)}
        state = {"completed": [], "next_directive": ""}

        with tempfile.TemporaryDirectory() as tmp:
            old_plugins_dir = runner.PLUGINS_DIR
            try:
                runner.PLUGINS_DIR = Path(tmp)
                anticipated = _refresh_anticipation_state(
                    state,
                    existing,
                    start_index=len(AI_CAPABILITY_ROADMAP) + 1,
                    persist=False,
                )
            finally:
                runner.PLUGINS_DIR = old_plugins_dir

        self.assertEqual(state["anticipated_next_capabilities"], anticipated)
        self.assertEqual(
            anticipated[0]["slug"],
            f"ai_prompt_contract_designer_{len(AI_CAPABILITY_ROADMAP) + 1:06d}",
        )
        self.assertEqual(anticipated[0]["reason"], "fresh canonical capability after current installed set")

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

    def test_rejected_capability_memory_skips_repeated_generation_under_same_knowledge(self) -> None:
        spec = copy.deepcopy(build_next_spec(len(AI_CAPABILITY_ROADMAP) + 1)[0])
        state = {"completed": [], "next_directive": "", "rejected_capabilities": {}, "rejected_capability_order": []}

        _capability_rejection_record(
            state=state,
            spec=spec,
            reason="production_quality: score 0.9300 < threshold 0.95",
            persist=False,
        )

        reason = _capability_rejection_skip_reason(state, spec)

        self.assertIsNotNone(reason)
        self.assertIn("already rejected", reason or "")

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
        legacy_slug = AI_CAPABILITY_ROADMAP[0].slug
        slug = build_next_spec(1)[0].slug
        state = {"completed": [], "next_directive": "", "upgrade_attempts": {}, "upgrade_attempt_order": []}

        with tempfile.TemporaryDirectory() as tmp:
            old_plugins_dir = runner.PLUGINS_DIR
            old_registered_profile_id = runner._registered_profile_id
            try:
                runner.PLUGINS_DIR = Path(tmp)
                runner._registered_profile_id = lambda candidate: (
                    "prompt_refinement_profile" if candidate in {slug, legacy_slug} else None
                )
                (Path(tmp) / f"{legacy_slug}.py").write_text(
                    "logic_profile_id = 'prompt_refinement_profile'\n",
                    encoding="utf-8",
                )

                seeded = runner._seed_retained_canonical_upgrade_memory(
                    state,
                    {legacy_slug},
                    persist=False,
                )
            finally:
                runner.PLUGINS_DIR = old_plugins_dir
                runner._registered_profile_id = old_registered_profile_id

        self.assertEqual(seeded, 1)
        self.assertTrue(_upgrade_backlog_exhausted(state, {legacy_slug}))
        record = state["upgrade_attempts"][slug]
        self.assertEqual(record["status"], "retained")
        self.assertIn("metadata-only retry is not an improvement", record["reason"])


if __name__ == "__main__":
    unittest.main()
