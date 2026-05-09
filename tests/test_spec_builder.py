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
    from factory.spec_builder import AI_CAPABILITY_ROADMAP, build_next_spec
    from factory.factory_runner import _canonical_retention_spec, _randomized_ai_expansion_indexes
    from factory.factory_runner import _upgrade_attempt_record, _upgrade_attempt_skip_reason
except ModuleNotFoundError:
    from spec_builder import AI_CAPABILITY_ROADMAP, build_next_spec
    from factory_runner import _canonical_retention_spec, _randomized_ai_expansion_indexes
    from factory_runner import _upgrade_attempt_record, _upgrade_attempt_skip_reason


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

    def test_phase_slug_is_internal_upgrade_candidate(self) -> None:
        first_spec = build_next_spec(1)[0]
        second_phase_spec = build_next_spec(len(AI_CAPABILITY_ROADMAP) + 1)[0]
        retention_spec = _canonical_retention_spec(second_phase_spec)

        self.assertNotEqual(first_spec.slug, second_phase_spec.slug)
        self.assertTrue(second_phase_spec.slug.endswith("_phase_2"))
        self.assertEqual(second_phase_spec.extra["phase"], 2)
        self.assertIn("Phase 2", second_phase_spec.name)
        self.assertEqual(retention_spec.slug, first_spec.slug)
        self.assertEqual(retention_spec.name, first_spec.name)
        self.assertEqual(retention_spec.extra["upgrade_attempt_phase"], 2)
        self.assertTrue(retention_spec.extra["discard_if_not_better"])

    def test_randomized_expansion_uses_bounded_upgrade_candidates(self) -> None:
        existing = {build_next_spec(i)[0].slug for i in range(1, len(AI_CAPABILITY_ROADMAP) + 1)}

        candidates = _randomized_ai_expansion_indexes(existing)

        self.assertGreaterEqual(len(candidates), len(AI_CAPABILITY_ROADMAP))
        sample_spec = build_next_spec(candidates[0])[0]
        retention_spec = _canonical_retention_spec(sample_spec)
        self.assertTrue(sample_spec.slug.endswith("_phase_2") or "_phase_" in sample_spec.slug)
        self.assertNotIn(sample_spec.slug, existing)
        self.assertIn(retention_spec.slug, existing)
        self.assertIn(sample_spec.extra["phase"], {2, 3})

    def test_upgrade_attempt_memory_skips_repeated_phase_under_same_knowledge(self) -> None:
        phase_spec = build_next_spec(len(AI_CAPABILITY_ROADMAP) + 1)[0]
        retention_spec = _canonical_retention_spec(phase_spec)
        state = {"completed": [], "next_directive": "", "upgrade_attempts": {}, "upgrade_attempt_order": []}

        _upgrade_attempt_record(
            state=state,
            source_spec=phase_spec,
            canonical_spec=retention_spec,
            status="rejected",
            reason="not better than canonical",
            persist=False,
        )

        reason = _upgrade_attempt_skip_reason(state, phase_spec)
        self.assertIsNotNone(reason)
        self.assertIn("already rejected", reason or "")


if __name__ == "__main__":
    unittest.main()
