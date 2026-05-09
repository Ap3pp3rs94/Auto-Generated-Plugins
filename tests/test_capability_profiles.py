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
    from factory.profiles import build_profile_source, registered_profile_id
    from factory.spec_builder import AI_CAPABILITY_ROADMAP
except ModuleNotFoundError:
    from profiles import build_profile_source, registered_profile_id
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
    "ai_plugin_spec_architect": {
        "task": "Create a plugin that designs plugin specs",
        "objective": "avoid random duplicate generated plugins",
        "existing_plugins": ["ai_prompt_refinement_engine", "ai_plugin_quality_gate_designer"],
        "constraints": ["must include unique output keys", "must define acceptance criteria"],
    },
    "ai_plugin_quality_gate_designer": {
        "task": "Design quality gates for generated plugin bodies",
        "objective": "reject shallow output before GitHub push",
        "quality_failures": ["semantic_depth: outputs too similar", "missing_detail_keys"],
        "constraints": ["repair only after validation", "push only passing plugins"],
    },
    "ai_plugin_factory_backlog_planner": {
        "task": "Plan next plugin factory backlog",
        "objective": "make plugins that create better plugins intentionally",
        "existing_plugins": ["ai_plugin_spec_architect"],
        "constraints": ["no duplicates", "no random filler"],
    },
}


BASE_PLUGIN_SOURCE = '''
from __future__ import annotations

from typing import Any, Dict, Optional

_PLUGIN_NAME = "Generated Test Plugin"
_PLUGIN_SLUG = "generated_test_plugin"
_PLUGIN_CATEGORY = "ai_test"
_PLUGIN_VERSION = "0.0.0"
_PLUGIN_OWNER_ID = "test"
_PLUGIN_CAPABILITY_TYPE = "test"
_PLUGIN_INTENDED_DOMAIN = "test"
_PLUGIN_RESULT_SCHEMA_VERSION = "1.0.0"
_PLUGIN_MANIFEST = {}


class SkillContext:
    def __init__(
        self,
        *,
        user_id: str,
        run_id: Optional[str],
        plugin_slug: str,
        plugin_name: str,
        learning_profile: Optional[Dict[str, Any]] = None,
        logger: Optional[Any] = None,
        brain: Optional[Any] = None,
    ) -> None:
        self.user_id = user_id
        self.run_id = run_id
        self.plugin_slug = plugin_slug
        self.plugin_name = plugin_name
        self.learning_profile = learning_profile or {}
        self.logger = logger
        self.brain = brain

    def log_info(self, *args: Any, **kwargs: Any) -> None:
        return None


def _run_core_logic(context: SkillContext, payload: Dict[str, Any], config: Dict[str, Any]) -> Dict[str, Any]:
    # === LOGIC START ===
    return {"summary": "placeholder", "primary_insights": [], "recommended_actions": [], "scores": {"confidence": 0.0}, "details": {}}
    # === LOGIC END ===


async def invoke(user_id: str, payload: Dict[str, Any], **kwargs: Any) -> Dict[str, Any]:
    context = SkillContext(
        user_id=user_id,
        run_id=kwargs.get("run_id"),
        plugin_slug=_PLUGIN_SLUG,
        plugin_name=_PLUGIN_NAME,
    )
    return {
        "status": "succeeded",
        "output": _run_core_logic(context, payload if isinstance(payload, dict) else {"_value": payload}, {}),
        "error": "",
        "meta": {"plugin_slug": _PLUGIN_SLUG},
    }
'''


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
                module = self._build_and_load_profile_plugin(slug)
                result = asyncio.run(module.invoke("profile-test", payload))

                self.assertEqual(result["status"], "succeeded", result)
                output = result["output"]
                self.assertEqual(output["details"]["logic_profile_id"], registered_profile_id(slug))
                self.assertNotEqual(output["details"]["logic_profile_id"], "semantic_repair")
                self.assertNotIn("capability_profile_error", str(output))

    def test_profile_sources_are_readable_and_not_base64_exec_blobs(self) -> None:
        sources = {
            slug: self._build_profile_source_for_slug(slug)
            for slug in PROFILE_PAYLOADS
        }

        for slug, source in sources.items():
            with self.subTest(slug=slug):
                self.assertIn("# Auto-generated readable capability-profile core logic", source)
                self.assertIn(str(registered_profile_id(slug)), source)
                self.assertNotIn("_profile_body_b64", source)
                self.assertNotIn("base64.b64decode", source)
                self.assertNotIn("exec(", source)

    def _build_profile_source_for_slug(self, slug: str) -> str:
        spec = next(item for item in AI_CAPABILITY_ROADMAP if item.slug == slug)
        source = build_profile_source(
            BASE_PLUGIN_SOURCE,
            spec,
            spec.capability_type,
            None,
            reason="test readable profile generation",
        )
        self.assertIsNotNone(source)
        return str(source)

    def _build_and_load_profile_plugin(self, slug: str):
        source = self._build_profile_source_for_slug(slug)
        temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(temp_dir.cleanup)
        path = Path(temp_dir.name) / f"{slug}.py"
        path.write_text(source, encoding="utf-8")
        spec = importlib.util.spec_from_file_location(slug, path)
        self.assertIsNotNone(spec)
        self.assertIsNotNone(spec.loader)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)  # type: ignore[union-attr]
        return module


if __name__ == "__main__":
    unittest.main()
