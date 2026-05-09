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
except ModuleNotFoundError:
    from spec_builder import AI_CAPABILITY_ROADMAP, build_next_spec


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

    def test_second_phase_slug_is_distinct(self) -> None:
        first_spec = build_next_spec(1)[0]
        second_phase_spec = build_next_spec(len(AI_CAPABILITY_ROADMAP) + 1)[0]

        self.assertNotEqual(first_spec.slug, second_phase_spec.slug)
        self.assertTrue(second_phase_spec.slug.endswith("_phase_2"))
        self.assertEqual(second_phase_spec.extra["phase"], 2)


if __name__ == "__main__":
    unittest.main()
