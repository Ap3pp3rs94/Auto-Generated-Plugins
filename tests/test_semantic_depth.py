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
    from factory.factory_runner import _production_quality_gate
    from factory.spec_builder import build_next_spec
except ModuleNotFoundError:
    from factory_runner import _semantic_depth_check
    from factory_runner import _production_quality_gate
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
        self.assertTrue(
            "semantic_depth" in reason or "prompt_refinement_contract" in reason,
            reason,
        )

    def test_value_dependent_generic_output_passes(self) -> None:
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
        ok, reason = self._run_check(source, spec_index=2)

        self.assertTrue(ok, reason)

    def test_prompt_refinement_without_rewrite_fails(self) -> None:
        source = """
async def invoke(user_id, payload, **kwargs):
    prompt = str(payload.get("prompt", ""))
    return {
        "status": "succeeded",
        "output": {
            "summary": "Prompt analyzed: " + prompt,
            "primary_insights": [{"title": "Prompt", "detail": prompt}],
            "recommended_actions": [{"action": "Rewrite prompt"}],
            "scores": {"confidence": 0.8, "risk": 0.2},
            "details": {"prompt": prompt},
            "progress_state": {"next_step": "Rewrite prompt"},
            "user_experience": {"plain_language_takeaway": "The prompt should be improved."},
        },
        "error": "",
        "meta": {},
    }
"""
        ok, reason = self._run_check(source, spec_index=1)

        self.assertFalse(ok)
        self.assertIn("prompt_refinement_contract", reason)

    def test_prompt_refinement_with_rewrites_passes(self) -> None:
        source = """
async def invoke(user_id, payload, **kwargs):
    prompt = str(payload.get("prompt", ""))
    task = str(payload.get("task", ""))
    objective = str(payload.get("objective", ""))
    refined = "Task: " + task + "\\nObjective: " + objective + "\\nAudience: the intended user\\nOutput format: structured checklist\\nConstraints: include verification and acceptance criteria\\nPrompt: " + prompt
    missing = [
        {"category": "audience", "suggestion": "Name the target audience."},
        {"category": "format", "suggestion": "Specify output format."},
        {"category": "constraint", "suggestion": "Add hard constraints."},
        {"category": "verification", "suggestion": "Add verification checks."},
    ]
    return {
        "status": "succeeded",
        "output": {
            "summary": "Refined prompt for " + task,
            "primary_insights": [
                {"title": "Original prompt", "detail": prompt},
                {"title": "Missing constraints", "items": missing},
            ],
            "recommended_actions": [
                {"action": "Use rewrite", "rewrite": refined},
                {"action": "Add constraints", "items": missing},
            ],
            "scores": {"confidence": min(0.9, 0.3 + len(prompt) / 200), "risk": max(0.1, 0.8 - len(objective) / 100)},
            "details": {
                "identified_vagueness": ["make it better"] if "better" in prompt.lower() else ["ambiguous objective"],
                "missing_constraints": missing,
                "rewrites": [{"label": "structured", "rewrite": refined}],
                "refined_prompt": refined,
            },
            "progress_state": {"next_step": "Review rewrite for " + objective},
            "user_experience": {"plain_language_takeaway": "Use the rewrite for " + task},
        },
        "error": "",
        "meta": {},
    }
"""
        ok, reason = self._run_check(source, spec_index=1)

        self.assertTrue(ok, reason)

    def test_production_quality_gate_rejects_sub_095_output(self) -> None:
        source = """
async def invoke(user_id, payload, **kwargs):
    return {
        "status": "succeeded",
        "output": {
            "summary": "Thin output that runs but is not production grade.",
            "primary_insights": [{"title": "One"}],
            "recommended_actions": [{"action": "Review manually"}],
            "scores": {"confidence": 0.4},
            "details": {"logic_profile_id": "thin_profile"},
        },
        "error": "",
        "meta": {},
    }
"""
        ok, reason = self._run_production_gate(source, spec_index=2)

        self.assertFalse(ok)
        self.assertIn("production_quality", reason)
        self.assertIn("< threshold 0.95", reason)

    def test_production_quality_gate_accepts_strong_output(self) -> None:
        source = """
async def invoke(user_id, payload, **kwargs):
    details = {
        "logic_profile_id": "strong_profile",
        "risk_signals": ["duplicate", "shallow"],
        "handoff_packet": {"owner": "validator"},
        "evidence": ["semantic depth passed"],
        "checklist": ["validate", "score", "publish"],
        "missing_inputs": [],
        "decision": "publish",
        "score_basis": ["details", "actions", "insights"],
        "payload_warnings": [],
        "next_probe": "quality",
    }
    return {
        "status": "succeeded",
        "output": {
            "summary": "Strong capability output with enough evidence and concrete production actions.",
            "primary_insights": [
                {"title": "Specific signal", "detail": "uses payload values"},
                {"title": "Risk", "detail": "duplicate avoided"},
                {"title": "Evidence", "detail": "semantic depth passed"},
                {"title": "Decision", "detail": "publish after validation"},
            ],
            "recommended_actions": [
                {"action": "Validate semantic depth before publishing"},
                {"action": "Compare candidate against existing capability"},
                {"action": "Keep stable family key for duplicate detection"},
                {"action": "Commit only after quality score passes threshold"},
            ],
            "scores": {"confidence": 0.92, "usefulness": 0.95, "risk": 0.12},
            "details": details,
            "progress_state": {"next_step": "Publish after validation"},
            "user_experience": {"plain_language_takeaway": "This capability has enough evidence to keep."},
            "fun_mode": {"challenge_label": "Production Ready", "score_badge": "0.95+"},
        },
        "error": "",
        "meta": {},
    }
"""
        ok, reason = self._run_production_gate(source, spec_index=2)

        self.assertTrue(ok, reason)

    def _run_check(self, source: str, *, spec_index: int = 1) -> tuple[bool, str]:
        spec, _, _ = build_next_spec(spec_index)
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "candidate.py"
            path.write_text(textwrap.dedent(source).strip() + "\n", encoding="utf-8")
            return asyncio.run(_semantic_depth_check(path, spec))

    def _run_production_gate(self, source: str, *, spec_index: int = 1) -> tuple[bool, str]:
        spec, _, _ = build_next_spec(spec_index)
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "candidate.py"
            path.write_text(textwrap.dedent(source).strip() + "\n", encoding="utf-8")
            return asyncio.run(_production_quality_gate(path, spec))


if __name__ == "__main__":
    unittest.main()
