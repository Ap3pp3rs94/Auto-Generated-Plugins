from __future__ import annotations

import asyncio
import importlib.util
import textwrap
import tempfile
import unittest
from pathlib import Path

from factory_os.draft_plugin_repair_surgeon import (
    analyze_draft_plugin,
    plan_repairs,
    repair_draft_plugin,
    repair_plugin_tree,
)


def buggy_plugin_source() -> str:
    return textwrap.dedent(
        '''
        from __future__ import annotations

        from typing import Any, Dict, Optional

        _PLUGIN_NAME = "AI Draft Plugin Repair Target"
        _PLUGIN_SLUG = "ai_draft_plugin_repair_target_000001"
        _PLUGIN_CATEGORY = "ai_prompting"
        _PLUGIN_VERSION = "0.1.0"
        _PLUGIN_GOAL = "Analyze task instructions and produce clearer, safer, more testable prompts."
        _PLUGIN_MANIFEST = {"slug": _PLUGIN_SLUG}


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


        def _run_core_logic(context: SkillContext, payload: Dict[str, Any], config: Dict[str, Any]) -> Dict[str, Any]:
            # === LOGIC START ===
            plugin_name = "AI Draft Plugin Repair Target"
            goal = "Analyze task instructions and produce clearer, safer, more testable prompts."
            capability_type = "enrichment"
            logic_profile_id = "prompt_refinement_profile"
            payload_data = payload if isinstance(payload, dict) else {}
            payload_warnings = [] if isinstance(payload, dict) else ["payload was not a dict; using empty payload"]
            task_text = str(payload_data.get('task') or '').strip()
            explicit_objective_text = str(payload_data.get('objective') or '').strip()
            def_text = str(task_text or explicit_objective_text or payload_data.get('prompt') or goal).strip()
            objective_text = str(explicit_objective_text or goal).strip()
            missing_inputs = []
            if not def_text:
                missing_inputs.append("task")
            result = {
                "summary": plugin_name + ": processed " + def_text[:80],
                "primary_insights": [{"title": "Target", "detail": def_text}],
                "recommended_actions": [{"action": "Use output", "objective": objective_text}],
                "scores": {"confidence": 0.5},
                "details": {
                    "logic_profile_id": logic_profile_id,
                    "missing_inputs": missing_inputs,
                    "payload_warnings": payload_warnings,
                },
                "progress_state": {"current_stage": logic_profile_id, "next_step": "Use output", "blockers": missing_inputs},
                "user_experience": {"plain_language_takeaway": "Processed draft."},
                "fun_mode": {"microcopy": "Draft processed."},
                "diagnostics": {"logic_profile_id": logic_profile_id},
            }
            return result
            # === LOGIC END ===


        async def invoke(
            user_id: str,
            payload: Dict[str, Any],
            *,
            run_id: Optional[str] = None,
            brain: Optional[Any] = None,
            logger: Optional[Any] = None,
            config: Optional[Dict[str, Any]] = None,
            **kwargs: Any,
        ) -> Dict[str, Any]:
            if not isinstance(payload, dict):
                payload = {"_value": payload}
            context = SkillContext(
                user_id=user_id,
                run_id=run_id,
                plugin_slug=_PLUGIN_SLUG,
                plugin_name=_PLUGIN_NAME,
                logger=logger,
                brain=brain,
            )
            try:
                core_output = _run_core_logic(context, payload, config or {})
                return {"status": "succeeded", "output": core_output, "error": "", "meta": {"plugin_slug": _PLUGIN_SLUG}}
            except Exception as exc:
                return {"status": "failed", "output": None, "error": str(exc), "meta": {"plugin_slug": _PLUGIN_SLUG}}
        '''
    )


def old_multi_profile_source() -> str:
    return textwrap.dedent(
        '''
        _PLUGIN_NAME = "Old Branch Table"
        _PLUGIN_SLUG = "old_branch_table"
        def _run_core_logic(context, payload, config):
            # === LOGIC START ===
            logic_profile_id = "plugin_spec_architect_profile"
            if logic_profile_id == "plugin_spec_architect_profile":
                result = {}
            elif logic_profile_id == "plugin_logic_blueprint_designer_profile":
                result = {}
            elif logic_profile_id == "plugin_quality_gate_designer_profile":
                result = {}
            elif logic_profile_id == "plugin_test_payload_generator_profile":
                result = {}
            elif logic_profile_id == "plugin_duplicate_detector_profile":
                result = {}
            return result
            # === LOGIC END ===
        '''
    )


def overlap_mismatch_source() -> str:
    return textwrap.dedent(
        '''
        _PLUGIN_NAME = "AI Capability Overlap Checker"
        _PLUGIN_SLUG = "ai_capability_overlap_checker_000999"
        def _run_core_logic(context, payload, config):
            # === LOGIC START ===
            logic_profile_id = "continuous_capability_overlap_checker_profile"
            if logic_profile_id == "plugin_spec_architect_profile":
                result = {"details": {"backlog_items": []}}
            elif logic_profile_id == "plugin_duplicate_detector_profile":
                result = {"details": {"duplicate_risks": []}}
            else:
                result = {"details": {"backlog_items": []}}
            return result
            # === LOGIC END ===
        '''
    )


def windows_temp_path_source() -> str:
    return textwrap.dedent(
        '''
        from __future__ import annotations

        from pathlib import Path

        _PLUGIN_NAME = "Windows Temp Path Target"
        _PLUGIN_SLUG = "windows_temp_path_target"

        def _run_core_logic(context, payload, config):
            # === LOGIC START ===
            logic_profile_id = "task_planner_profile"
            temp_path = Path("/tmp/francis/plugin.txt")
            result = {
                "summary": str(temp_path),
                "primary_insights": [],
                "recommended_actions": [],
                "scores": {"confidence": 0.7, "usefulness": 0.7},
                "details": {"logic_profile_id": logic_profile_id},
                "progress_state": {"blockers": []},
                "user_experience": {},
                "fun_mode": {"celebratory_microcopy": "ok"},
                "diagnostics": {"logic_profile_id": logic_profile_id},
            }
            return result
            # === LOGIC END ===
        '''
    )


def windows_home_path_source() -> str:
    return textwrap.dedent(
        '''
        _PLUGIN_NAME = "Windows Home Path Target"
        _PLUGIN_SLUG = "windows_home_path_target"
        def _run_core_logic(context, payload, config):
            # === LOGIC START ===
            logic_profile_id = "task_planner_profile"
            repo_path = "/home/peppera091/francis/factory"
            result = {"summary": repo_path, "details": {"logic_profile_id": logic_profile_id}}
            return result
            # === LOGIC END ===
        '''
    )


def shell_command_source() -> str:
    return textwrap.dedent(
        '''
        _PLUGIN_NAME = "Shell Command Target"
        _PLUGIN_SLUG = "shell_command_target"
        def _run_core_logic(context, payload, config):
            # === LOGIC START ===
            import subprocess
            logic_profile_id = "task_planner_profile"
            subprocess.run("echo one && echo two", shell=True)
            result = {"summary": "done", "details": {"logic_profile_id": logic_profile_id}}
            return result
            # === LOGIC END ===
        '''
    )


def context_noise_filter_weak_source() -> str:
    return textwrap.dedent(
        '''
        from __future__ import annotations

        _PLUGIN_NAME = "AI Context Noise Filter Test"
        _PLUGIN_SLUG = "ai_context_noise_filter_test"

        class SkillContext:
            def __init__(self, **kwargs):
                self.__dict__.update(kwargs)

        def _run_core_logic(context, payload, config):
            # === LOGIC START ===
            plugin_name = "AI Context Noise Filter Test"
            logic_profile_id = "continuous_context_noise_filter_profile"
            messages = payload.get("messages", []) if isinstance(payload, dict) else []
            kept = []
            dropped = []
            for idx, item in enumerate(messages):
                kept.append({"source": "item_%d" % idx, "text": str(item), "preview": str(item), "reason_tags": []})
            result = {
                "summary": "kept everything",
                "primary_insights": [{"title": "Kept context", "detail": kept}],
                "recommended_actions": [{"action": "Keep high-priority context", "items": kept}],
                "scores": {"confidence": 0.7, "usefulness": 0.7, "context_retention": 1.0},
                "details": {
                    "logic_profile_id": logic_profile_id,
                    "kept_context": kept,
                    "compressed_context": [],
                    "dropped_context": dropped,
                    "priority_reason_counts": {},
                    "missing_inputs": [],
                },
                "progress_state": {"blockers": []},
                "user_experience": {},
                "fun_mode": {"celebratory_microcopy": "ok"},
                "diagnostics": {"logic_profile_id": logic_profile_id},
            }
            return result
            # === LOGIC END ===

        async def invoke(user_id, payload, **kwargs):
            if not isinstance(payload, dict):
                payload = {"_value": payload, "_payload_warnings": ["payload was not a dict; invoke wrapped it in _value"]}
            return {"status": "succeeded", "output": _run_core_logic(SkillContext(user_id=user_id), payload, kwargs.get("config") or {}), "error": "", "meta": {"plugin_slug": _PLUGIN_SLUG}}
        '''
    )


def source_quality_ranker_grounded_answer_source() -> str:
    return textwrap.dedent(
        '''
        from __future__ import annotations

        _PLUGIN_NAME = "AI Source Quality Ranker Test"
        _PLUGIN_SLUG = "ai_source_quality_ranker_test"

        class SkillContext:
            def __init__(self, **kwargs):
                self.__dict__.update(kwargs)

        def _run_core_logic(context, payload, config):
            # === LOGIC START ===
            plugin_name = "AI Source Quality Ranker Test"
            logic_profile_id = "continuous_source_quality_ranker_profile"
            supported_claims = []
            unsupported_claims = [{"claim": "All plugins are useful", "matched_evidence_terms": []}]
            answer_plan = [{"section": "answer", "instruction": "State only supported claims."}]
            result = {
                "summary": plugin_name + ": planned a grounded answer with 0 supported and 1 unsupported claim(s).",
                "primary_insights": [{"title": "Answer plan", "detail": answer_plan}],
                "recommended_actions": [{"action": "Draft general_grounding answer from plan", "answer_plan": answer_plan}],
                "scores": {"confidence": 0.5, "grounding_score": 0.0, "usefulness": 0.5},
                "details": {
                    "logic_profile_id": logic_profile_id,
                    "supported_claims": supported_claims,
                    "unsupported_claims": unsupported_claims,
                    "answer_plan": answer_plan,
                    "missing_inputs": [],
                },
                "progress_state": {"blockers": []},
                "user_experience": {},
                "fun_mode": {"celebratory_microcopy": "ok"},
                "diagnostics": {"logic_profile_id": logic_profile_id},
            }
            return result
            # === LOGIC END ===

        async def invoke(user_id, payload, **kwargs):
            if not isinstance(payload, dict):
                payload = {"_value": payload, "_payload_warnings": ["payload was not a dict; invoke wrapped it in _value"]}
            return {"status": "succeeded", "output": _run_core_logic(SkillContext(user_id=user_id), payload, kwargs.get("config") or {}), "error": "", "meta": {"plugin_slug": _PLUGIN_SLUG}}
        '''
    )


class DraftPluginRepairSurgeonTests(unittest.TestCase):
    def test_repair_detects_goal_fallback_bug(self) -> None:
        analysis = analyze_draft_plugin(buggy_plugin_source())

        self.assertTrue(analysis.has_goal_fallback_input_bug)
        self.assertEqual(analysis.recommended_action, "repair")

    def test_repair_patches_payload_warning_preservation(self) -> None:
        result = repair_draft_plugin(buggy_plugin_source())

        self.assertIn("preserve_payload_warnings", result.applied_patches)
        self.assertIn("_payload_warnings", result.patched_source)
        self.assertNotIn("payload_warnings = [] if isinstance(payload, dict) else", result.patched_source)

    def test_repair_adds_enriched_diagnostics(self) -> None:
        result = repair_draft_plugin(buggy_plugin_source())

        self.assertIn("add_profile_missing_input_and_diagnostics_finalizer", result.applied_patches)
        self.assertIn("'has_user_input'", result.patched_source)
        self.assertIn("'input_signal_count'", result.patched_source)
        self.assertIn("'semantic_probe_ready'", result.patched_source)

    def test_empty_payload_after_repair_reports_missing_inputs_and_blockers(self) -> None:
        module = self._load_repaired_module()
        envelope = asyncio.run(module.invoke("tester", {}))

        self.assertEqual(envelope["status"], "succeeded", envelope)
        output = envelope["output"]
        self.assertTrue(output["details"]["missing_inputs"], output)
        self.assertIn("prompt or instruction", output["details"]["missing_inputs"])
        self.assertTrue(output["progress_state"]["blockers"], output)
        self.assertFalse(output["diagnostics"]["has_user_input"], output)
        self.assertTrue(output["diagnostics"]["used_goal_fallback"], output)

    def test_non_dict_payload_after_repair_preserves_payload_warnings(self) -> None:
        module = self._load_repaired_module()
        envelope = asyncio.run(module.invoke("tester", "make this better"))

        self.assertEqual(envelope["status"], "succeeded", envelope)
        output = envelope["output"]
        warnings = output["details"]["payload_warnings"]
        self.assertTrue(any("not a dict" in warning for warning in warnings), output)
        self.assertGreater(output["diagnostics"]["payload_warning_count"], 0, output)

    def test_old_multi_profile_branch_table_is_classified_as_regenerate(self) -> None:
        analysis = analyze_draft_plugin(old_multi_profile_source())
        plan = plan_repairs(analysis)

        self.assertTrue(analysis.has_multi_profile_branch_table)
        self.assertEqual(analysis.recommended_action, "regenerate")
        self.assertEqual(plan.risk_level, "high")
        self.assertEqual(plan.repair_steps, [])

    def test_overlap_checker_routing_mismatch_is_detected(self) -> None:
        analysis = analyze_draft_plugin(overlap_mismatch_source())

        self.assertTrue(analysis.has_profile_routing_mismatch)

    def test_overlap_checker_routing_mismatch_is_patched_without_full_regeneration(self) -> None:
        analysis = analyze_draft_plugin(overlap_mismatch_source())
        plan = plan_repairs(analysis)
        result = repair_draft_plugin(overlap_mismatch_source())

        self.assertIn("patch_overlap_profile_alias_routing", [step.patch_id for step in plan.repair_steps])
        self.assertIn("patch_overlap_profile_alias_routing", result.applied_patches)
        self.assertIn("capability_overlap_checker_profile", result.patched_source)
        self.assertIn("continuous_capability_overlap_checker_profile", result.patched_source)
        self.assertNotIn("profile_routing_mismatch", result.remaining_findings)
        self.assertEqual(result.recommended_next_action, "retest")

    def test_patched_source_still_imports_and_invoke_returns_station_c_envelope(self) -> None:
        module = self._load_repaired_module()
        envelope = asyncio.run(module.invoke("tester", {"prompt": "Make this better", "objective": "Ship safely"}))

        self.assertEqual(envelope["status"], "succeeded", envelope)
        self.assertIsInstance(envelope["output"], dict)
        self.assertEqual(envelope["meta"]["plugin_slug"], "ai_draft_plugin_repair_target_000001")
        self.assertIn("output", envelope)
        self.assertIn("error", envelope)
        self.assertIn("meta", envelope)

    def test_windows_temp_path_literals_are_normalized(self) -> None:
        result = repair_draft_plugin(windows_temp_path_source())

        self.assertIn("normalize_patchable_posix_temp_paths", result.applied_patches)
        self.assertIn("tempfile.gettempdir()", result.patched_source)
        self.assertNotIn('Path("/tmp/francis/plugin.txt")', result.patched_source)
        compile(result.patched_source, "windows_temp_path_target.py", "exec")

    def test_hardcoded_home_path_is_not_blindly_patched(self) -> None:
        analysis = analyze_draft_plugin(windows_home_path_source())
        plan = plan_repairs(analysis)

        self.assertTrue(analysis.has_windows_path_literal_bug)
        self.assertFalse(analysis.has_patchable_windows_temp_path_bug)
        self.assertEqual(plan.risk_level, "high")
        self.assertEqual(plan.repair_steps, [])

    def test_shell_command_is_classified_for_regeneration(self) -> None:
        analysis = analyze_draft_plugin(shell_command_source())
        plan = plan_repairs(analysis)

        self.assertTrue(analysis.has_windows_shell_command_bug)
        self.assertTrue(analysis.has_windows_subprocess_shell_bug)
        self.assertEqual(analysis.recommended_action, "regenerate")
        self.assertEqual(plan.risk_level, "high")

    def test_repair_plugin_tree_dry_run_and_apply(self) -> None:
        temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(temp_dir.cleanup)
        root = Path(temp_dir.name)
        plugin_path = root / "windows_temp_path_target.py"
        plugin_path.write_text(windows_temp_path_source(), encoding="utf-8")

        dry_run_reports = repair_plugin_tree(root, dry_run=True)
        self.assertEqual(len(dry_run_reports), 1)
        self.assertTrue(dry_run_reports[0].changed)
        self.assertIn('Path("/tmp/francis/plugin.txt")', plugin_path.read_text(encoding="utf-8"))

        apply_reports = repair_plugin_tree(root, dry_run=False)
        self.assertEqual(len(apply_reports), 1)
        self.assertTrue(apply_reports[0].changed)
        self.assertIn("tempfile.gettempdir()", plugin_path.read_text(encoding="utf-8"))

    def test_context_noise_filter_repair_drops_explicit_noise(self) -> None:
        result = repair_draft_plugin(context_noise_filter_weak_source())
        self.assertIn("add_context_noise_filter_semantic_finalizer", result.applied_patches)
        module = self._load_module_from_source(result.patched_source, "context_noise_filter_repaired")

        envelope = asyncio.run(
            module.invoke(
                "tester",
                {
                    "messages": [
                        "important: factory running in tmux",
                        "irrelevant: lunch plans",
                    ]
                },
            )
        )

        output = envelope["output"]
        kept_text = " ".join(str(item) for item in output["details"]["kept_context"]).lower()
        dropped_text = " ".join(str(item) for item in output["details"]["dropped_context"]).lower()
        self.assertNotIn("lunch plans", kept_text)
        self.assertIn("lunch plans", dropped_text)
        self.assertTrue(output["diagnostics"]["context_noise_repair_applied"])

    def test_source_quality_ranker_repair_outputs_ranked_sources(self) -> None:
        result = repair_draft_plugin(source_quality_ranker_grounded_answer_source())
        self.assertIn("add_source_quality_ranker_semantic_finalizer", result.applied_patches)
        module = self._load_module_from_source(result.patched_source, "source_quality_ranker_repaired")

        envelope = asyncio.run(
            module.invoke(
                "tester",
                {
                    "objective": "Rank evidence for whether plugins run on Windows.",
                    "source_notes": [
                        {"title": "local test output", "type": "command_log", "content": "Windows py_compile ok and 78 tests OK"},
                        {"title": "unverified blog", "type": "blog", "content": "claims the system is perfect"},
                    ],
                },
            )
        )

        output = envelope["output"]
        self.assertIn("ranked_sources", output["details"])
        self.assertGreaterEqual(len(output["details"]["ranked_sources"]), 2)
        self.assertIn("source_quality", output["scores"])
        self.assertNotEqual(output["recommended_actions"][0]["action"], "Draft general_grounding answer from plan")
        self.assertTrue(output["diagnostics"]["source_quality_repair_applied"])

    def test_source_quality_ranker_repair_changes_decision_surface_by_payload(self) -> None:
        result = repair_draft_plugin(source_quality_ranker_grounded_answer_source())
        module = self._load_module_from_source(result.patched_source, "source_quality_ranker_contrast")

        auth_output = asyncio.run(
            module.invoke(
                "tester",
                {
                    "objective": "Rank release evidence for auth middleware and database rollback safety.",
                    "candidate_outputs": [
                        {"summary": "Change authentication middleware first."},
                        {"summary": "Add rollback checks before production release."},
                    ],
                },
            )
        )["output"]
        citation_output = asyncio.run(
            module.invoke(
                "tester",
                {
                    "objective": "Rank evidence for hallucination risk in a medical citation answer.",
                    "trace": [{"tool": "retrieval", "issue": "citation mismatch"}],
                    "candidate_outputs": [
                        {"summary": "States an unsupported dosage claim."},
                        {"summary": "Flags missing source support."},
                    ],
                },
            )
        )["output"]

        self.assertIn("release_auth_source_ranking", auth_output["summary"])
        self.assertIn("citation_safety_source_ranking", citation_output["summary"])
        self.assertNotEqual(auth_output["recommended_actions"][0]["action"], citation_output["recommended_actions"][0]["action"])
        self.assertNotEqual(auth_output["scores"], citation_output["scores"])

    def _load_repaired_module(self):
        result = repair_draft_plugin(buggy_plugin_source())
        self.assertEqual(result.recommended_next_action, "retest", result)
        temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(temp_dir.cleanup)
        path = Path(temp_dir.name) / "repaired_plugin.py"
        path.write_text(result.patched_source, encoding="utf-8")
        spec = importlib.util.spec_from_file_location("repaired_plugin", path)
        self.assertIsNotNone(spec)
        self.assertIsNotNone(spec.loader)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)  # type: ignore[union-attr]
        return module

    def _load_module_from_source(self, source: str, module_name: str):
        temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(temp_dir.cleanup)
        path = Path(temp_dir.name) / (module_name + ".py")
        path.write_text(source, encoding="utf-8")
        spec = importlib.util.spec_from_file_location(module_name, path)
        self.assertIsNotNone(spec)
        self.assertIsNotNone(spec.loader)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)  # type: ignore[union-attr]
        return module


if __name__ == "__main__":
    unittest.main()
