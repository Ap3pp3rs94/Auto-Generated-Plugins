from __future__ import annotations

import asyncio
import base64
import importlib.util
import re
import unittest
from pathlib import Path
import sys


REPO_ROOT = Path(__file__).resolve().parents[1]
FRANCIS_ROOT = Path(__file__).resolve().parents[2]
for path in (REPO_ROOT, FRANCIS_ROOT):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

try:
    from factory.profiles import registered_profile_id
    from factory.spec_builder import AI_CAPABILITY_ROADMAP
except ModuleNotFoundError:
    from profiles import registered_profile_id
    from spec_builder import AI_CAPABILITY_ROADMAP


PROFILE_PAYLOADS = {
    "ai_agent_task_planner": {
        "task": "Add semantic profile tests",
        "objective": "ship safely",
        "current_plan": ["inspect code"],
        "blocked_steps": ["unclear ownership"],
    },
    "ai_tool_selection_advisor": {
        "task": "Debug a failing Python test in a repo",
        "objective": "choose tools",
    },
    "ai_memory_compression_synthesizer": {
        "task": "compress session",
        "messages": [{"content": "We decided plugins must land in factory/plugins. Next verify tests."}],
    },
    "ai_context_window_optimizer": {
        "task": "optimize context",
        "token_budget": 120,
        "messages": [{"content": "must keep acceptance criteria and blocked files"}, {"content": "thanks"}],
    },
    "ai_output_quality_scorer": {
        "task": "answer with tests",
        "response": "I changed the code.",
        "rubric": ["mentions tests", "states changed files"],
    },
    "ai_hallucination_risk_auditor": {
        "response": "This always works under current law and reduces cost by 40 percent.",
    },
    "ai_retrieval_query_expander": {
        "task": "Find docs for Ollama timeout behavior",
        "objective": "ground factory troubleshooting",
    },
}


class CapabilityProfileTests(unittest.TestCase):
    def test_every_ai_roadmap_slug_has_registered_profile(self) -> None:
        missing = [item.slug for item in AI_CAPABILITY_ROADMAP if not registered_profile_id(item.slug)]

        self.assertEqual(missing, [])
        self.assertEqual(
            registered_profile_id(AI_CAPABILITY_ROADMAP[0].slug + "_phase_2"),
            registered_profile_id(AI_CAPABILITY_ROADMAP[0].slug),
        )

    def test_profile_plugins_run_with_registered_profile_ids(self) -> None:
        for slug, payload in PROFILE_PAYLOADS.items():
            with self.subTest(slug=slug):
                module = self._load_plugin(slug)
                result = asyncio.run(module.invoke("profile-test", payload))

                self.assertEqual(result["status"], "succeeded", result)
                output = result["output"]
                self.assertEqual(output["details"]["logic_profile_id"], registered_profile_id(slug))
                self.assertNotEqual(output["details"]["logic_profile_id"], "semantic_repair")
                self.assertNotIn("capability_profile_error", str(output))

    def test_inlined_profile_bodies_are_not_duplicates(self) -> None:
        decoded_bodies = {
            slug: self._decode_profile_body(REPO_ROOT / "plugins" / f"{slug}.py")
            for slug in PROFILE_PAYLOADS
        }

        self.assertEqual(len(set(decoded_bodies.values())), len(decoded_bodies))
        for slug, body in decoded_bodies.items():
            self.assertIn(str(registered_profile_id(slug)), body)

    def _load_plugin(self, slug: str):
        path = REPO_ROOT / "plugins" / f"{slug}.py"
        spec = importlib.util.spec_from_file_location(slug, path)
        self.assertIsNotNone(spec)
        self.assertIsNotNone(spec.loader)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)  # type: ignore[union-attr]
        return module

    def _decode_profile_body(self, path: Path) -> str:
        source = path.read_text(encoding="utf-8")
        match = re.search(r"_profile_body_b64 = '([^']+)'", source)
        self.assertIsNotNone(match, path)
        return base64.b64decode(match.group(1).encode("ascii")).decode("utf-8")


if __name__ == "__main__":
    unittest.main()
