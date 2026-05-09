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
    from factory.factory_runner import _semantic_depth_check
    from factory.spec_builder import build_next_spec
except ModuleNotFoundError:
    from factory_runner import _semantic_depth_check
    from spec_builder import build_next_spec


class SemanticDepthTests(unittest.TestCase):
    def test_shallow_stock_output_fails(self) -> None:
        source = """
async def invoke(user_id, payload, **kwargs):
    return {
        "status": "succeeded",
        "output": {
            "summary": "Generic analysis complete.",
            "primary_insights": ["No conversation history found."],
            "recommended_actions": [{"action": "Rewrite prompt"}],
            "scores": {"confidence": 0.8, "usefulness": 0.9},
            "details": [{"value": payload}],
            "progress_state": {"next_step": "Rewrite prompt"},
            "user_experience": {"plain_language_takeaway": "Next step is clear."},
        },
        "error": "",
        "meta": {},
    }
"""
        ok, reason = self._run_check(source)

        self.assertFalse(ok)
        self.assertIn("semantic_depth", reason)

    def test_value_dependent_output_passes(self) -> None:
        source = """
async def invoke(user_id, payload, **kwargs):
    task = str(payload.get("task", "missing task"))
    objective = str(payload.get("objective", "missing objective"))
    blocked = str((payload.get("blocked_steps") or ["no blocker"])[0])
    return {
        "status": "succeeded",
        "output": {
            "summary": "Plan for " + task,
            "primary_insights": [
                {"title": "Task", "detail": task},
                {"title": "Objective", "detail": objective},
                {"title": "Blocker", "detail": blocked},
            ],
            "recommended_actions": [
                {"action": "Verify " + objective},
                {"action": "Resolve " + blocked},
            ],
            "scores": {"confidence": min(0.9, 0.3 + len(task) / 200), "risk": min(0.9, len(blocked) / 100)},
            "details": {"task": task, "objective": objective},
            "progress_state": {"next_step": "Verify " + objective},
            "user_experience": {"plain_language_takeaway": "Focus on " + task},
        },
        "error": "",
        "meta": {},
    }
"""
        ok, reason = self._run_check(source)

        self.assertTrue(ok, reason)

    def _run_check(self, source: str) -> tuple[bool, str]:
        spec, _, _ = build_next_spec(1)
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "candidate.py"
            path.write_text(textwrap.dedent(source).strip() + "\n", encoding="utf-8")
            return asyncio.run(_semantic_depth_check(path, spec))


if __name__ == "__main__":
    unittest.main()
