from __future__ import annotations

import asyncio
import importlib.util
import json
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
    from factory.factory_runner import _render_profile_base_source
    from factory.profiles import build_profile_source, registered_profile_id
    from factory.quality_runner import _required_detail_keys
    from factory.spec_builder import AI_CAPABILITY_ROADMAP, build_next_spec
except ModuleNotFoundError:
    from factory_runner import _render_profile_base_source  # type: ignore
    from profiles import build_profile_source, registered_profile_id  # type: ignore
    from quality_runner import _required_detail_keys  # type: ignore
    from spec_builder import AI_CAPABILITY_ROADMAP, build_next_spec  # type: ignore


RICH_PAYLOAD_A = {
    "task": "Plan a multi-agent refactor of authentication middleware without breaking login.",
    "objective": "Separate database migration, API changes, test coverage, and rollback checks.",
    "prompt": "Fix auth and add tests without losing session safety.",
    "instruction": "Produce a verified implementation plan.",
    "query": "auth middleware rollback test plan",
    "question": "Which tool should verify the login regression risk?",
    "expected_behavior": "Return normal, edge, and adversarial checks with clear pass criteria.",
    "audience": "senior engineer",
    "output_format": "structured checklist",
    "evidence_policy": "include validation evidence and rollback checks",
    "response": "I changed auth middleware and added login tests, but rollback evidence is missing.",
    "answer": "The safest path is to verify migration, API, and login regression evidence.",
    "messages": [{"content": "We decided auth changes need rollback checks and database owner review."}],
    "source_notes": ["Production release requires explicit validation evidence."],
    "candidate_outputs": [
        {"id": "plan_a", "summary": "Change middleware first"},
        {"id": "plan_b", "summary": "Write login tests before code changes"},
    ],
    "trace": [{"tool": "pytest", "status": "failed", "error": "login regression timeout"}],
    "current_plan": ["Inspect auth middleware", "Add login regression tests"],
    "completed_steps": ["Mapped current session flow"],
    "blocked_steps": ["Need database migration owner"],
    "constraints": ["No production outage", "Keep rollback explicit"],
    "rubric": ["mentions tests", "states changed files", "includes rollback"],
    "previous_results": {"decision": "hold release until checks pass"},
    "token_budget": 512,
    "agents": ["builder", "database reviewer", "test owner"],
    "workstreams": ["middleware refactor", "migration review", "login regression tests"],
    "ownership_scopes": ["code changes", "schema safety", "test coverage"],
    "requirements": ["include validation", "avoid duplicate capability behavior"],
    "inputs": ["task", "trace", "constraints"],
    "output_schema": {"summary": "string", "checks": "list"},
    "files": ["plugins/ai_agent_task_planner.py"],
    "changed_files": ["profiles/registry.py"],
    "validation_summary": {"ok": True, "semantic_ok": True},
    "quality_failures": ["prior candidate had identical scores"],
    "probe_results": ["duplicate probe passed", "unique probe passed"],
    "existing_plugins": [{"name": "AI Agent Task Planner", "slug": "ai_agent_task_planner"}],
}


RICH_PAYLOAD_B = {
    "task": "Choose tools for verifying hallucination risk in a retrieved medical-summary answer.",
    "objective": "Decide whether to browse sources, inspect citations, or run local consistency checks.",
    "prompt": "Is this claim grounded enough to show the user?",
    "instruction": "Produce citation-first verification checks.",
    "query": "medical answer citation verification",
    "question": "Does the retrieved source support this dosage claim?",
    "expected_behavior": "Flag unsupported claims and require source-backed caveats.",
    "audience": "clinical review operator",
    "output_format": "claim table with caveats",
    "evidence_policy": "cite source support or mark unsupported",
    "response": "This dosage always works and reduces symptoms by 40 percent without citation.",
    "answer": "The answer needs source grounding before it is safe to show.",
    "messages": [{"content": "A retrieved medical summary has citation mismatch and unsupported dosage."}],
    "source_notes": ["Source snippet does not support the dosage claim."],
    "candidate_outputs": [
        {"id": "answer_a", "summary": "States an unsupported dosage claim"},
        {"id": "answer_b", "summary": "Flags missing source support"},
    ],
    "trace": [{"tool": "retrieval", "status": "partial", "issue": "citation mismatch"}],
    "current_plan": ["Compare answer claims to source snippets"],
    "completed_steps": ["Collected candidate answer"],
    "blocked_steps": ["Need citation verification"],
    "constraints": ["Do not invent clinical facts", "Escalate uncertain claims"],
    "rubric": ["marks unsupported claims", "uses citations", "adds caveats"],
    "previous_results": {"decision": "do not publish without source support"},
    "token_budget": 768,
    "agents": ["researcher", "citation reviewer", "answer editor"],
    "workstreams": ["retrieval review", "citation matching", "safe rewrite"],
    "ownership_scopes": ["source grounding", "unsupported claim audit", "user-facing answer"],
    "requirements": ["cite sources", "flag unsupported facts"],
    "inputs": ["answer", "source_notes", "trace"],
    "output_schema": {"claims": "list", "caveats": "list"},
    "files": ["plugins/ai_hallucination_risk_auditor.py"],
    "changed_files": ["profiles/registry.py"],
    "validation_summary": {"ok": True, "semantic_ok": True},
    "quality_failures": ["prior answer lacked citation proof"],
    "probe_results": ["grounding probe passed", "empty payload probe passed"],
    "existing_plugins": [{"name": "AI Hallucination Risk Auditor", "slug": "ai_hallucination_risk_auditor"}],
}


class GeneratedProfileInputContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.temp_dir = tempfile.TemporaryDirectory()
        cls.modules = []
        cls.sources = {}
        base = Path(cls.temp_dir.name)
        for index in range(1, len(AI_CAPABILITY_ROADMAP) + 1):
            spec, capability_type, _domain = build_next_spec(index)
            profile_id = registered_profile_id(spec.slug)
            source = build_profile_source(
                _render_profile_base_source(spec),
                spec,
                capability_type,
                profile_id,
                reason="test generated input contracts",
            )
            if source is None:
                raise AssertionError(f"No generated source for {spec.slug}")
            source_text = str(source)
            cls.sources[spec.slug] = source_text
            path = base / f"{index}_{spec.slug}.py"
            path.write_text(source_text, encoding="utf-8")
            module_spec = importlib.util.spec_from_file_location(f"generated_contract_{index}", path)
            if module_spec is None or module_spec.loader is None:
                raise AssertionError(f"Could not load {path}")
            module = importlib.util.module_from_spec(module_spec)
            module_spec.loader.exec_module(module)  # type: ignore[union-attr]
            cls.modules.append((spec, profile_id, module))

    @classmethod
    def tearDownClass(cls) -> None:
        cls.temp_dir.cleanup()

    def test_empty_payload_reports_missing_inputs_and_does_not_count_goal(self) -> None:
        for spec, profile_id, module in self.modules:
            with self.subTest(slug=spec.slug, profile_id=profile_id):
                output = self._invoke(module, {})
                details = output["details"]
                diagnostics = output["diagnostics"]

                self.assertTrue(details["missing_inputs"], output)
                self.assertTrue(output["progress_state"]["blockers"], output)
                self.assertFalse(diagnostics["has_user_input"], output)
                self.assertTrue(diagnostics["used_goal_fallback"], output)
                self.assertGreater(diagnostics["missing_inputs_count"], 0, output)

    def test_non_dict_payload_preserves_payload_warning(self) -> None:
        for spec, profile_id, module in self.modules:
            with self.subTest(slug=spec.slug, profile_id=profile_id):
                output = self._invoke(module, "make me a capability")
                warnings = output["details"].get("payload_warnings", [])

                self.assertTrue(any("not a dict" in warning for warning in warnings), output)
                self.assertGreater(output["diagnostics"]["payload_warning_count"], 0, output)

    def test_useful_payload_produces_profile_specific_detail_keys(self) -> None:
        for spec, profile_id, module in self.modules:
            expected_keys = _required_detail_keys(profile_id or "")
            with self.subTest(slug=spec.slug, profile_id=profile_id):
                output = self._invoke(module, RICH_PAYLOAD_A)
                details = output["details"]

                self.assertTrue(expected_keys, f"No expected detail keys registered for {profile_id}")
                self.assertTrue(expected_keys <= set(details.keys()), (expected_keys, details.keys()))
                self.assertTrue(output["diagnostics"]["semantic_probe_ready"], output)

    def test_contrast_payloads_change_details_and_scores(self) -> None:
        for spec, profile_id, module in self.modules:
            with self.subTest(slug=spec.slug, profile_id=profile_id):
                output_a = self._invoke(module, RICH_PAYLOAD_A)
                output_b = self._invoke(module, RICH_PAYLOAD_B)

                self.assertNotEqual(self._stable_json(output_a["details"]), self._stable_json(output_b["details"]))
                self.assertNotEqual(output_a["scores"], output_b["scores"])

    def test_multi_agent_handoff_requires_handoff_specific_inputs(self) -> None:
        module = next(module for spec, _profile_id, module in self.modules if spec.slug == "ai_multi_agent_handoff_planner")

        weak = self._invoke(module, {"task": "Plan work", "objective": "Ship safely"})
        strong = self._invoke(module, RICH_PAYLOAD_A)

        self.assertIn("agents, workstreams, or ownership_scopes", weak["details"]["missing_inputs"])
        self.assertEqual(weak["details"]["handoff_overlap_decision"], "repair_or_merge")
        self.assertTrue(strong["details"]["ownership_boundaries"])
        self.assertNotEqual(strong["details"]["handoff_overlap_decision"], "repair_or_merge")

    def test_generated_source_has_no_unrelated_profile_branches(self) -> None:
        forbidden_fragments = [
            "elif logic_profile_id ==",
            "if logic_profile_id ==",
            "plugin_duplicate_detector_profile",
            "continuous_capability_overlap_checker_profile",
        ]
        for spec, profile_id, _module in self.modules:
            with self.subTest(slug=spec.slug, profile_id=profile_id):
                source = self.sources[spec.slug]
                for fragment in forbidden_fragments:
                    if fragment == profile_id:
                        continue
                    self.assertNotIn(fragment, source)

    def _invoke(self, module, payload):
        envelope = asyncio.run(module.invoke("contract-test", payload))
        self.assertEqual(envelope["status"], "succeeded", envelope)
        self.assertIsInstance(envelope["output"], dict, envelope)
        return envelope["output"]

    def _stable_json(self, value) -> str:
        return json.dumps(value, sort_keys=True, default=str)


if __name__ == "__main__":
    unittest.main()
