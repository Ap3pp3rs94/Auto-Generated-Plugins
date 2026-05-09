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
    from factory.factory_runner import _randomized_ai_expansion_indexes
except ModuleNotFoundError:
    from spec_builder import AI_CAPABILITY_ROADMAP, build_next_spec
    from factory_runner import _randomized_ai_expansion_indexes


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

    def test_second_phase_slug_is_available_for_explicit_expansion(self) -> None:
        first_spec = build_next_spec(1)[0]
        second_phase_spec = build_next_spec(len(AI_CAPABILITY_ROADMAP) + 1)[0]

        self.assertNotEqual(first_spec.slug, second_phase_spec.slug)
        self.assertTrue(second_phase_spec.slug.endswith("_phase_2"))
        self.assertEqual(second_phase_spec.extra["phase"], 2)
        self.assertIn("Phase 2", second_phase_spec.name)

    def test_randomized_expansion_uses_bounded_phase_variants(self) -> None:
        existing = {build_next_spec(i)[0].slug for i in range(1, len(AI_CAPABILITY_ROADMAP) + 1)}

        candidates = _randomized_ai_expansion_indexes(existing)

        self.assertGreaterEqual(len(candidates), len(AI_CAPABILITY_ROADMAP))
        sample_spec = build_next_spec(candidates[0])[0]
        self.assertTrue(sample_spec.slug.endswith("_phase_2") or "_phase_" in sample_spec.slug)
        self.assertNotIn(sample_spec.slug, existing)
        self.assertIn(sample_spec.extra["phase"], {2, 3})


if __name__ == "__main__":
    unittest.main()
