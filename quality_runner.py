from __future__ import annotations

"""
Francis factory quality runner.

Audits generated AI capability modules already in factory/plugins and repairs
weak artifacts back to the current deterministic capability-profile standard.
"""

import argparse
import asyncio
import importlib.util
import inspect
import json
import logging
import os
import shutil
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, Iterable, Optional, Sequence

try:
    from factory.factory_runner import (
        FACTORY_DIR,
        PLUGINS_DIR,
        PRODUCTION_QUALITY_THRESHOLD,
        _build_registered_profile_result,
        _capability_quality_score,
        _capability_promotion_gate,
        _extract_output_payload,
        _git_run,
        _semantic_depth_check,
        _validate_plugin_file,
    )
    from factory.profiles import build_profile_source, registered_profile_id
    from factory.spec_builder import AI_CAPABILITY_ROADMAP, build_next_spec, legacy_continuous_expansion_slug
    from factory.factory_os.capability_specs import get_capability_spec
    from factory.factory_os.logic_profiles import get_logic_profile, normalize_logic_profile_id
    from factory.factory_os.promotion_gate import evaluate_for_promotion
    from factory.factory_os.semantic_contracts import get_semantic_contract
    from factory.factory_os.semantic_validator import run_semantic_contract_async
    from factory.factory_os.a_plus_certification import certify_plugin_callable as certify_a_plus_plugin
    from factory.factory_os.a_plus_certification import summarize_a_plus_result
except (ImportError, ModuleNotFoundError):  # pragma: no cover - direct sidecar execution
    from factory_runner import (  # type: ignore
        FACTORY_DIR,
        PLUGINS_DIR,
        PRODUCTION_QUALITY_THRESHOLD,
        _build_registered_profile_result,
        _capability_quality_score,
        _capability_promotion_gate,
        _extract_output_payload,
        _git_run,
        _semantic_depth_check,
        _validate_plugin_file,
    )
    from profiles import build_profile_source, registered_profile_id  # type: ignore
    from spec_builder import AI_CAPABILITY_ROADMAP, build_next_spec, legacy_continuous_expansion_slug  # type: ignore
    from factory_os.capability_specs import get_capability_spec  # type: ignore
    from factory_os.logic_profiles import get_logic_profile, normalize_logic_profile_id  # type: ignore
    from factory_os.promotion_gate import evaluate_for_promotion  # type: ignore
    from factory_os.semantic_contracts import get_semantic_contract  # type: ignore
    from factory_os.semantic_validator import run_semantic_contract_async  # type: ignore
    from factory_os.a_plus_certification import certify_plugin_callable as certify_a_plus_plugin  # type: ignore
    from factory_os.a_plus_certification import summarize_a_plus_result  # type: ignore


LOG = logging.getLogger(__name__)

QUALITY_CANDIDATES_DIR = FACTORY_DIR / ".quality_candidates"
QUALITY_LOCK_PATH = FACTORY_DIR / ".quality_runner.lock"
QUALITY_BACKUP_DIR = FACTORY_DIR.parent / "junk_plugins" / "quality_backups"


GITHUB_FACTORY_PAYLOAD: Dict[str, Any] = {
    "task": "Ship an AI capability factory change that pushes generated modules to GitHub without duplicates.",
    "objective": "Keep production safe and make phone-visible GitHub progress.",
    "prompt": "make it better and do not break production auth or database migrations",
    "constraints": [
        "No duplicate capabilities",
        "Reject shallow output",
        "Push only after validation",
        "Include rollback checks",
    ],
    "current_plan": ["generate candidate", "validate plugin", "semantic depth check", "commit and push"],
    "completed_steps": ["added staged candidate folder", "pushed roadmap extension"],
    "blocked_steps": ["need proof capabilities are high quality"],
    "candidate_outputs": [
        {"summary": "This answer claims the current latest model is safe without citation."},
        {"summary": "A better answer includes verification and rollback evidence."},
    ],
    "messages": [{"content": "User wants continuous autonomous capability generation with no randoms."}],
    "source_notes": ["Factory must land capability modules in factory/plugins only after all gates pass."],
    "trace": [
        {"error": "semantic_depth failed because outputs were too similar"},
        {"message": "git push succeeded"},
    ],
    "rubric": ["must mention validation", "must avoid duplicates", "must show GitHub push evidence"],
    "response": "The system works and always produces correct current claims. It pushed plugins but lacks citation proof.",
    "token_budget": 512,
}


PROFILE_REQUIRED_DETAIL_KEYS: Dict[str, set[str]] = {
    "prompt_refinement_profile": {"identified_vagueness", "missing_constraints", "rewrites", "refined_prompt"},
    "prompt_constraint_mapper_profile": {"identified_vagueness", "missing_constraints", "rewrites", "refined_prompt"},
    "task_planner_profile": {"sequenced_plan", "handoff_packet", "risk_signals"},
    "agent_checkpoint_generator_profile": {"sequenced_plan", "handoff_packet", "risk_signals"},
    "multi_agent_handoff_profile": {"sequenced_plan", "handoff_packet", "ownership_boundaries"},
    "tool_selection_profile": {"tool_recommendations", "selection_rationale"},
    "tool_call_sequence_builder_profile": {"tool_recommendations", "selection_rationale"},
    "memory_compression_profile": {"memory_summary", "durable_facts", "open_threads"},
    "memory_fact_extractor_profile": {"memory_summary", "durable_facts", "open_threads"},
    "context_window_optimizer_profile": {"kept_context", "compressed_context", "dropped_context"},
    "model_context_budget_estimator_profile": {"kept_context", "compressed_context", "dropped_context"},
    "output_quality_scorer_profile": {"covered_requirements", "missing_requirements", "improvement_checklist"},
    "hallucination_risk_auditor_profile": {"claims", "high_risk_claims", "safer_rewrites"},
    "citation_need_detector_profile": {"claims", "high_risk_claims", "safer_rewrites"},
    "retrieval_query_expander_profile": {"expanded_queries", "facet_terms", "grounding_plan"},
    "prompt_test_case_generator_profile": {"test_cases", "ambiguities", "risk_tags"},
    "regression_watchlist_builder_profile": {"test_cases", "ambiguities", "risk_tags"},
    "workflow_debugger_profile": {"failure_points", "signals_by_stage", "retry_plan"},
    "trace_signal_extractor_profile": {"failure_points", "signals_by_stage", "retry_plan"},
    "response_comparator_profile": {"ranked_responses", "winner", "merge_plan"},
    "response_merge_planner_profile": {"ranked_responses", "winner", "merge_plan"},
    "instruction_conflict_detector_profile": {"instruction_sources", "conflicts", "clarified_instruction"},
    "structured_prompt_builder_profile": {"structured_prompt", "output_schema", "checklist"},
    "capability_router_profile": {"routes", "selected_route", "split_needed"},
    "user_intent_classifier_profile": {"routes", "selected_route", "split_needed"},
    "eval_rubric_generator_profile": {"rubric", "hard_failures", "scoring_scale"},
    "acceptance_criteria_extractor_profile": {"rubric", "hard_failures", "scoring_scale"},
    "automation_safety_gate_profile": {"risk_findings", "controls", "approval_required"},
    "risk_register_builder_profile": {"risk_findings", "controls", "approval_required"},
    "progress_tracker_profile": {"completed", "active", "blocked", "next_action"},
    "grounded_answer_planner_profile": {"supported_claims", "unsupported_claims", "evidence_map", "answer_plan", "caveats"},
    "tool_result_consistency_checker_profile": {"tool_evidence", "model_conclusions", "consistency_findings", "retry_plan", "consistency_score"},
    "operator_status_brief_builder_profile": {"status_brief", "operator_actions", "run_health", "validation_evidence"},
    "prompt_injection_surface_scanner_profile": {"injection_findings", "trust_boundaries", "handling_rules", "sanitized_context_plan"},
    "workflow_retry_strategy_planner_profile": {"retry_strategy", "failure_clusters", "retry_decision", "stop_conditions"},
    "model_selection_scorecard_profile": {"model_scorecard", "selected_model_style", "cost_risk_tradeoffs", "escalation_triggers"},
    "requirement_gap_analyzer_profile": {"requirement_gaps", "assumptions", "clarification_questions", "readiness_decision"},
    "artifact_release_note_generator_profile": {"release_notes", "validation_evidence", "changed_artifacts", "known_risks"},
    "data_contract_mapper_profile": {"input_contract", "output_contract", "validation_rules", "schema_gaps"},
    "autonomous_run_governor_profile": {"governance_decision", "run_signals", "stop_conditions", "allowed_next_actions"},
    "plugin_spec_architect_profile": {"spec_blueprint", "uniqueness_checks", "capability_boundaries", "prompt_requirements"},
    "plugin_logic_blueprint_designer_profile": {"logic_blueprint", "deterministic_rules", "data_flow", "failure_modes"},
    "plugin_quality_gate_designer_profile": {"quality_gates", "rejection_rules", "semantic_probes", "pass_criteria"},
    "plugin_test_payload_generator_profile": {"test_payloads", "edge_cases", "expected_differences", "regression_watchlist"},
    "capability_overlap_checker_profile": {"duplicate_risks", "uniqueness_fingerprint", "comparison_targets", "merge_or_reject_decision", "max_similarity", "missing_inputs"},
    "continuous_tool_argument_checker_profile": {"argument_risks", "unsafe_arguments", "sanitized_arguments", "argument_safety_decision"},
    "continuous_output_completeness_grader_profile": {"completeness_findings", "missing_sections", "completeness_score"},
    "continuous_response_action_planner_profile": {"action_plan", "actionability_gaps", "next_step_checks"},
    "continuous_verification_checklist_builder_profile": {"verification_checklist", "automated_checks", "human_review_checks"},
    "continuous_rollback_guard_builder_profile": {"rollback_plan", "rollback_readiness", "blast_radius", "missing_rollback_controls"},
    "plugin_duplicate_detector_profile": {"duplicate_risks", "uniqueness_fingerprint", "comparison_targets", "merge_or_reject_decision", "max_similarity", "missing_inputs"},
    "plugin_repair_strategy_planner_profile": {"repair_plan", "weak_signals", "capability_specific_targets", "acceptance_checks"},
    "plugin_release_packager_profile": {"release_package", "validation_summary", "github_publish_plan", "rollback_notes"},
    "plugin_factory_backlog_planner_profile": {"backlog_items", "priority_rationale", "dependency_order", "next_plugin_specs"},
    "plugin_profile_gap_detector_profile": {"profile_gaps", "missing_profile_slugs", "alias_gaps", "coverage_summary"},
    "semantic_probe_result_analyzer_profile": {"probe_failures", "contrast_findings", "repair_targets", "promotion_recommendation"},
    "release_readiness_scorecard_profile": {"readiness_checks", "blocking_findings", "release_decision", "evidence_summary"},
}


CONTINUOUS_PROFILE_REQUIRED_KEY_FALLBACKS: tuple[tuple[str, str], ...] = (
    ("continuous_prompt_contract_designer_profile", "structured_prompt_builder_profile"),
    ("continuous_prompt_clarity_auditor_profile", "prompt_refinement_profile"),
    ("continuous_evidence_gap_detector_profile", "grounded_answer_planner_profile"),
    ("continuous_source_quality_ranker_profile", "grounded_answer_planner_profile"),
    ("continuous_context_noise_filter_profile", "context_window_optimizer_profile"),
    ("continuous_memory_update_recommender_profile", "memory_compression_profile"),
    ("continuous_agent_handoff_checker_profile", "multi_agent_handoff_profile"),
    ("continuous_parallelization_planner_profile", "task_planner_profile"),
    ("continuous_tool_safety_reviewer_profile", "automation_safety_gate_profile"),
    ("continuous_tool_argument_checker_profile", "prompt_injection_surface_scanner_profile"),
    ("continuous_output_completeness_grader_profile", "output_quality_scorer_profile"),
    ("continuous_response_action_planner_profile", "output_quality_scorer_profile"),
    ("continuous_assumption_risk_mapper_profile", "requirement_gap_analyzer_profile"),
    ("continuous_verification_checklist_builder_profile", "prompt_test_case_generator_profile"),
    ("continuous_rollback_guard_builder_profile", "automation_safety_gate_profile"),
    ("continuous_anomaly_watch_builder_profile", "autonomous_run_governor_profile"),
    ("continuous_capability_overlap_checker_profile", "capability_overlap_checker_profile"),
    ("continuous_release_evidence_summarizer_profile", "artifact_release_note_generator_profile"),
    ("continuous_trace_failure_router_profile", "workflow_debugger_profile"),
    ("continuous_retrieval_query_planner_profile", "retrieval_query_expander_profile"),
    ("continuous_citation_priority_scorer_profile", "hallucination_risk_auditor_profile"),
    ("continuous_model_fit_triage_profile", "model_selection_scorecard_profile"),
    ("continuous_instruction_hierarchy_checker_profile", "instruction_conflict_detector_profile"),
    ("continuous_data_contract_validator_profile", "data_contract_mapper_profile"),
    ("prompt_persona_adapter_profile", "prompt_refinement_profile"),
    ("prompt_output_schema_designer_profile", "structured_prompt_builder_profile"),
    ("model_failure_mode_classifier_profile", "workflow_debugger_profile"),
    ("evidence_gap_prioritizer_profile", "grounded_answer_planner_profile"),
    ("source_trust_ranker_profile", "grounded_answer_planner_profile"),
    ("context_relevance_ranker_profile", "context_window_optimizer_profile"),
    ("memory_conflict_resolver_profile", "memory_compression_profile"),
    ("agent_role_boundary_mapper_profile", "multi_agent_handoff_profile"),
    ("parallel_work_detector_profile", "task_planner_profile"),
    ("tool_permission_gate_profile", "automation_safety_gate_profile"),
    ("tool_argument_sanitizer_profile", "prompt_injection_surface_scanner_profile"),
    ("eval_failure_classifier_profile", "output_quality_scorer_profile"),
    ("response_actionability_scorer_profile", "output_quality_scorer_profile"),
    ("user_clarification_question_builder_profile", "prompt_refinement_profile"),
    ("assumption_tracker_profile", "requirement_gap_analyzer_profile"),
    ("change_impact_summarizer_profile", "artifact_release_note_generator_profile"),
    ("verification_plan_builder_profile", "prompt_test_case_generator_profile"),
    ("red_team_prompt_probe_builder_profile", "prompt_injection_surface_scanner_profile"),
    ("rollback_readiness_checker_profile", "automation_safety_gate_profile"),
    ("live_run_anomaly_detector_profile", "autonomous_run_governor_profile"),
    ("capability_dependency_mapper_profile", "data_contract_mapper_profile"),
)


def _required_detail_keys(profile_id: str) -> set[str]:
    normalized = normalize_logic_profile_id(profile_id) or profile_id
    profile_id = normalized
    required = PROFILE_REQUIRED_DETAIL_KEYS.get(profile_id)
    if required is not None:
        return required
    for continuous_profile, base_profile in CONTINUOUS_PROFILE_REQUIRED_KEY_FALLBACKS:
        if profile_id == continuous_profile:
            return PROFILE_REQUIRED_DETAIL_KEYS.get(base_profile, set())
    return set()


@dataclass
class QualityIssue:
    code: str
    message: str


@dataclass
class AuditResult:
    slug: str
    path: Path
    profile_id: Optional[str]
    passed: bool
    issues: list[QualityIssue] = field(default_factory=list)
    repaired: bool = False
    repair_path: Optional[Path] = None

    def add(self, code: str, message: str) -> None:
        self.issues.append(QualityIssue(code=code, message=message))
        self.passed = False

    @property
    def summary(self) -> str:
        if self.passed:
            return f"{self.slug}: PASS"
        return f"{self.slug}: FAIL " + "; ".join(f"{i.code}={i.message}" for i in self.issues)


@dataclass
class QualityConfig:
    repair: bool = True
    github_publish_enabled: bool = True
    github_remote: str = "origin"
    github_branch: str = "main"
    loop_forever: bool = False
    sleep_seconds: float = 300.0
    slugs: list[str] = field(default_factory=list)


def _pid_is_running(pid: int) -> bool:
    if pid <= 0:
        return False
    try:
        os.kill(pid, 0)
    except ProcessLookupError:
        return False
    except PermissionError:
        return True
    return True


def _acquire_quality_lock() -> None:
    existing = None
    try:
        existing = int(QUALITY_LOCK_PATH.read_text(encoding="utf-8").strip())
    except Exception:
        existing = None
    if existing and existing != os.getpid() and _pid_is_running(existing):
        raise RuntimeError(f"Quality runner already appears to be running as PID {existing}.")
    QUALITY_LOCK_PATH.write_text(str(os.getpid()), encoding="utf-8")


def _release_quality_lock() -> None:
    try:
        if QUALITY_LOCK_PATH.read_text(encoding="utf-8").strip() == str(os.getpid()):
            QUALITY_LOCK_PATH.unlink(missing_ok=True)
    except Exception:
        return


def _roadmap_specs_by_slug() -> Dict[str, Any]:
    specs: Dict[str, Any] = {}
    for index in range(1, len(AI_CAPABILITY_ROADMAP) + 1):
        spec, capability_type, intended_domain = build_next_spec(index)
        spec.capability_type = capability_type
        spec.intended_domain = intended_domain
        specs[spec.slug] = spec
    return specs


def _roadmap_spec_from_slug(slug: str) -> Optional[Any]:
    roadmap_size = len(AI_CAPABILITY_ROADMAP)
    for position, blueprint in enumerate(AI_CAPABILITY_ROADMAP, start=1):
        if slug == blueprint.slug:
            spec, capability_type, intended_domain = build_next_spec(position)
            spec.capability_type = capability_type
            spec.intended_domain = intended_domain
            return spec
    for index in range(roadmap_size + 1, roadmap_size + 10000):
        spec, capability_type, intended_domain = build_next_spec(index)
        if spec.slug == slug:
            spec.capability_type = capability_type
            spec.intended_domain = intended_domain
            return spec
        if legacy_continuous_expansion_slug(index) == slug:
            spec.slug = slug
            spec.capability_type = capability_type
            spec.intended_domain = intended_domain
            return spec
    return None


def _candidate_plugin_paths(slugs: Iterable[str]) -> list[Path]:
    requested = {slug.strip() for slug in slugs if slug.strip()}
    paths = sorted(path for path in PLUGINS_DIR.glob("*.py") if path.name != "__init__.py")
    if requested:
        paths = [path for path in paths if path.stem in requested]
    return paths


def _load_module_from_path(path: Path, slug: str) -> Any:
    module_name = f"quality_probe_{slug}".replace("-", "_")
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)  # type: ignore[call-arg]
    return module


async def _invoke(path: Path, slug: str, payload: Dict[str, Any]) -> Dict[str, Any]:
    module = _load_module_from_path(path, slug)
    invoke = getattr(module, "invoke", None)
    if not callable(invoke):
        raise RuntimeError("plugin has no callable invoke")
    result = invoke("factory-quality-runner", payload, run_id=f"quality-{slug}")
    if inspect.isawaitable(result):
        result = await result
    if isinstance(result, dict) and result.get("status") == "failed":
        raise RuntimeError(str(result.get("error") or "plugin returned failed status"))
    return _extract_output_payload(result)


def _json_text(value: Any) -> str:
    try:
        return json.dumps(value, sort_keys=True, default=str).lower()
    except Exception:
        return str(value).lower()


def _profile_specific_checks(result: AuditResult, output: Dict[str, Any]) -> None:
    profile_id = normalize_logic_profile_id(result.profile_id or "") or (result.profile_id or "")
    details = output.get("details") if isinstance(output.get("details"), dict) else {}
    scores = output.get("scores") if isinstance(output.get("scores"), dict) else {}

    actual_profile = details.get("logic_profile_id")
    normalized_actual = normalize_logic_profile_id(str(actual_profile or "")) or actual_profile
    if profile_id and normalized_actual != profile_id:
        result.add("profile_mismatch", f"expected {profile_id!r}, got {actual_profile!r}")

    required = _required_detail_keys(profile_id)
    missing = sorted(key for key in required if key not in details)
    if missing:
        result.add("missing_detail_keys", ", ".join(missing))

    confidence = scores.get("confidence")
    if not isinstance(confidence, (int, float)) or confidence <= 0:
        result.add("bad_confidence", f"confidence={confidence!r}")

    text = _json_text(output)
    if "capability profile failed" in text or "capability_profile_error" in text:
        result.add("profile_runtime_error", "plugin fell back to capability_profile_error")
    if "semantic_repair" in text:
        result.add("legacy_semantic_repair", "plugin still carries legacy semantic_repair output")

    if profile_id in {"tool_selection_profile", "tool_call_sequence_builder_profile"}:
        tool_text = _json_text(details.get("tool_recommendations", []))
        if "git_github" not in tool_text:
            result.add("weak_tool_routing", "GitHub factory payload did not recommend git_github")
        if "validator" not in tool_text:
            result.add("weak_tool_routing", "GitHub factory payload did not recommend validator")

    if profile_id in {"capability_router_profile", "user_intent_classifier_profile"}:
        selected = str(details.get("selected_route") or "")
        if selected != "github_publish_agent":
            result.add("weak_intent_routing", f"GitHub factory payload selected {selected!r}")


async def _semantic_contract_checks(result: AuditResult, path: Path, spec: Any) -> None:
    cap_spec = get_capability_spec(str(getattr(spec, "slug", "") or ""))
    if cap_spec is None:
        return
    profile_id = normalize_logic_profile_id(result.profile_id or "") or result.profile_id
    profile = get_logic_profile(profile_id or "")
    contract = get_semantic_contract(cap_spec.slug)
    if profile is None or contract is None:
        result.add("semantic_contract_missing", f"missing profile/contract for {cap_spec.slug}")
        return
    try:
        module = _load_module_from_path(path, result.slug)
        semantic_result = await run_semantic_contract_async(module.invoke, cap_spec, profile, contract)
        first_output = await _invoke(path, result.slug, contract.probes[0].payload if contract.probes else {})
        decision = evaluate_for_promotion(first_output, cap_spec, profile, semantic_result)
    except Exception as exc:
        result.add("semantic_contract_crash", str(exc))
        return
    if not semantic_result.passed:
        finding_text = "; ".join(f"{finding.code}: {finding.message}" for finding in semantic_result.findings[:8])
        result.add("semantic_contract", finding_text or "semantic contract failed")
    if decision.decision != "promote":
        result.add("promotion_gate", f"{decision.decision}: {decision.reason}")


async def _promotion_gate_checks(result: AuditResult, path: Path, spec: Any) -> None:
    try:
        promotion_ok, promotion_reason = await _capability_promotion_gate(path, spec)
    except Exception as exc:
        result.add("promotion_gate_crash", str(exc))
        return
    if not promotion_ok:
        result.add("promotion_gate", promotion_reason)


async def _a_plus_checks(result: AuditResult, path: Path, spec: Any) -> None:
    try:
        module = _load_module_from_path(path, result.slug)
        invoke = getattr(module, "invoke", None)
        if not callable(invoke):
            result.add("a_plus_certification", "plugin has no callable invoke")
            return
        a_plus_result = await certify_a_plus_plugin(
            invoke,
            metadata={
                "slug": getattr(spec, "slug", ""),
                "name": getattr(spec, "name", ""),
                "category": getattr(spec, "category", ""),
                "capability_type": getattr(spec, "capability_type", ""),
                "intended_domain": getattr(spec, "intended_domain", ""),
                "use_cases": list(getattr(spec, "use_cases", []) or []),
            },
        )
    except Exception as exc:
        result.add("a_plus_certification_crash", str(exc))
        return
    if not a_plus_result.passed:
        result.add("a_plus_certification", summarize_a_plus_result(a_plus_result))


async def audit_plugin_path(path: Path, spec: Any) -> AuditResult:
    profile_id = registered_profile_id(spec.slug)
    result = AuditResult(slug=spec.slug, path=path, profile_id=profile_id, passed=True)

    ok, reason = await _validate_plugin_file(path, spec)
    if not ok:
        result.add("structural_validation", reason)
        return result

    semantic_ok, semantic_reason = await _semantic_depth_check(path, spec)
    if not semantic_ok:
        result.add("semantic_depth", semantic_reason)

    try:
        output = await _invoke(path, spec.slug, GITHUB_FACTORY_PAYLOAD)
    except Exception as exc:
        result.add("probe_crash", str(exc))
        return result

    if not isinstance(output, dict):
        result.add("bad_output", f"expected dict output, got {type(output).__name__}")
        return result

    if not output.get("summary"):
        result.add("missing_summary", "summary is empty")
    if not output.get("primary_insights"):
        result.add("missing_insights", "primary_insights is empty")
    if not output.get("recommended_actions"):
        result.add("missing_actions", "recommended_actions is empty")

    production_score = _capability_quality_score(output)
    if production_score < PRODUCTION_QUALITY_THRESHOLD:
        result.add(
            "production_quality",
            f"score {production_score:.4f} < threshold {PRODUCTION_QUALITY_THRESHOLD:.2f}",
        )

    _profile_specific_checks(result, output)
    await _semantic_contract_checks(result, path, spec)
    await _promotion_gate_checks(result, path, spec)
    await _a_plus_checks(result, path, spec)
    return result


async def _build_repair_candidate(spec: Any, existing_path: Path, reason: str) -> Optional[Path]:
    clean_reason = reason.replace("semantic_repair", "legacy semantic body")
    repair_reason = "quality_runner_repair: " + clean_reason[:500]
    try:
        existing_source = existing_path.read_text(encoding="utf-8")
    except Exception:
        existing_source = ""

    source = None
    if existing_source:
        source = build_profile_source(
            existing_source,
            spec,
            getattr(spec, "capability_type", None),
            registered_profile_id(spec.slug),
            reason=repair_reason,
        )

    if not source:
        repair = _build_registered_profile_result(
            spec=spec,
            capability_type=getattr(spec, "capability_type", None),
            reason=repair_reason,
        )
        if repair is None or not repair.source:
            return None
        source = repair.source

    QUALITY_CANDIDATES_DIR.mkdir(parents=True, exist_ok=True)
    candidate = QUALITY_CANDIDATES_DIR / f"{spec.slug}.py"
    candidate.write_text(str(source), encoding="utf-8")
    return candidate


async def repair_plugin(path: Path, spec: Any, failed: AuditResult) -> AuditResult:
    reason = "; ".join(f"{issue.code}: {issue.message}" for issue in failed.issues)
    candidate = await _build_repair_candidate(spec, path, reason)
    if candidate is None:
        failed.add("repair_unavailable", "no registered deterministic profile repair exists")
        return failed

    repaired_audit = await audit_plugin_path(candidate, spec)
    if not repaired_audit.passed:
        failed.issues.extend(
            QualityIssue("repair_failed_" + issue.code, issue.message)
            for issue in repaired_audit.issues
        )
        failed.passed = False
        return failed

    QUALITY_BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    backup = QUALITY_BACKUP_DIR / f"{path.stem}.{os.getpid()}.py"
    shutil.copy2(path, backup)
    candidate.replace(path)
    repaired_audit.path = path
    repaired_audit.repaired = True
    repaired_audit.repair_path = path
    return repaired_audit


def _publish_repaired_plugins(paths: Sequence[Path], config: QualityConfig) -> bool:
    if not config.github_publish_enabled or not paths:
        return True
    rels = []
    for path in paths:
        try:
            rels.append(path.resolve().relative_to(FACTORY_DIR.resolve()).as_posix())
        except ValueError:
            LOG.error("Refusing to publish repaired plugin outside factory repo: %s", path)
            return False

    add_result = _git_run(["add", "--", *rels])
    if add_result.returncode != 0:
        LOG.error("Git add failed for repaired plugins: %s", (add_result.stderr or add_result.stdout).strip())
        return False

    diff_result = _git_run(["diff", "--cached", "--quiet", "--", *rels])
    if diff_result.returncode == 0:
        LOG.info("No repaired plugin diff to publish.")
    elif diff_result.returncode == 1:
        commit_result = _git_run(["commit", "-m", "Quality repair generated capabilities", "--", *rels])
        if commit_result.returncode != 0:
            LOG.error("Git commit failed for repaired plugins: %s", (commit_result.stderr or commit_result.stdout).strip())
            return False
        LOG.info("Committed %d repaired plugin(s).", len(rels))
    else:
        LOG.error("Git diff failed for repaired plugins: %s", (diff_result.stderr or diff_result.stdout).strip())
        return False

    push_result = _git_run(["push", config.github_remote, config.github_branch], timeout_seconds=300)
    if push_result.returncode != 0:
        LOG.error("GitHub push failed for repaired plugins: %s", (push_result.stderr or push_result.stdout).strip())
        return False
    LOG.info("GitHub updated for quality repairs via %s/%s.", config.github_remote, config.github_branch)
    return True


async def run_quality_pass(config: QualityConfig) -> list[AuditResult]:
    specs = _roadmap_specs_by_slug()
    results: list[AuditResult] = []
    repaired_paths: list[Path] = []

    for path in _candidate_plugin_paths(config.slugs):
        spec = specs.get(path.stem) or _roadmap_spec_from_slug(path.stem)
        if spec is None:
            LOG.info("Skipping non-roadmap plugin %s", path.name)
            continue

        audit = await audit_plugin_path(path, spec)
        if audit.passed:
            LOG.info("Quality PASS: %s", path.stem)
            results.append(audit)
            continue

        LOG.warning("Quality FAIL: %s", audit.summary)
        if config.repair:
            audit = await repair_plugin(path, spec, audit)
            if audit.repaired:
                LOG.info("Quality REPAIRED: %s", path.stem)
                repaired_paths.append(path)
            else:
                LOG.error("Quality repair did not pass for %s: %s", path.stem, audit.summary)
        results.append(audit)

    if repaired_paths:
        _publish_repaired_plugins(repaired_paths, config)
    return results


async def run_quality_runner(config: QualityConfig) -> None:
    _acquire_quality_lock()
    try:
        while True:
            results = await run_quality_pass(config)
            failed = [item for item in results if not item.passed]
            repaired = [item for item in results if item.repaired]
            LOG.info(
                "Quality pass complete: checked=%d repaired=%d failed=%d",
                len(results),
                len(repaired),
                len(failed),
            )
            if failed:
                for item in failed:
                    LOG.error(item.summary)
            if not config.loop_forever:
                break
            await asyncio.sleep(config.sleep_seconds)
    finally:
        _release_quality_lock()


def _env(name: str, default: Optional[str] = None) -> Optional[str]:
    value = os.environ.get(name)
    return default if value is None or value == "" else value


def _env_bool(name: str, default: bool = False) -> bool:
    value = os.environ.get(name)
    if value is None or value == "":
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


def _env_float(name: str, default: float) -> float:
    value = os.environ.get(name)
    if value is None or value == "":
        return default
    return float(value)


def _build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Audit and repair generated Francis plugins.")
    parser.add_argument("--once", action="store_true", help="Run one quality pass and exit.")
    parser.add_argument(
        "--loop",
        action="store_true",
        default=_env_bool("FRANCIS_QUALITY_LOOP", False),
        help="Run quality passes continuously.",
    )
    parser.add_argument(
        "--sleep-seconds",
        type=float,
        default=_env_float("FRANCIS_QUALITY_SLEEP_SECONDS", 300.0),
        help="Seconds between continuous quality passes.",
    )
    parser.add_argument(
        "--no-repair",
        action="store_true",
        default=_env_bool("FRANCIS_QUALITY_NO_REPAIR", False),
        help="Audit only; do not rewrite weak plugins.",
    )
    parser.add_argument(
        "--no-github-publish",
        action="store_true",
        default=_env_bool("FRANCIS_QUALITY_NO_GITHUB_PUBLISH", False),
        help="Do not commit/push repaired plugin artifacts.",
    )
    parser.add_argument(
        "--github-remote",
        default=_env("FRANCIS_QUALITY_GITHUB_REMOTE", "origin"),
        help="Git remote used when publishing repairs.",
    )
    parser.add_argument(
        "--github-branch",
        default=_env("FRANCIS_QUALITY_GITHUB_BRANCH", "main"),
        help="Git branch pushed after repair commits.",
    )
    parser.add_argument("--slug", action="append", default=[], help="Limit audit to one plugin slug. Repeatable.")
    parser.add_argument(
        "--log-level",
        default=_env("FRANCIS_QUALITY_LOG_LEVEL", "INFO"),
        help="Python logging level.",
    )
    return parser


def build_config_from_args(argv: Optional[Sequence[str]] = None) -> tuple[QualityConfig, str]:
    args = _build_arg_parser().parse_args(argv)
    loop_forever = bool(args.loop)
    if args.once:
        loop_forever = False
    config = QualityConfig(
        repair=not args.no_repair,
        github_publish_enabled=not args.no_github_publish,
        github_remote=str(args.github_remote or "origin"),
        github_branch=str(args.github_branch or "main"),
        loop_forever=loop_forever,
        sleep_seconds=float(args.sleep_seconds),
        slugs=[str(item) for item in args.slug],
    )
    return config, str(args.log_level).upper()


def main(argv: Optional[Sequence[str]] = None) -> int:
    try:
        config, log_level = build_config_from_args(argv)
        logging.basicConfig(
            level=getattr(logging, log_level, logging.INFO),
            format="[%(asctime)s] [%(levelname)s] %(message)s",
        )
        asyncio.run(run_quality_runner(config))
    except KeyboardInterrupt:
        LOG.info("Quality runner interrupted.")
        return 130
    except Exception as exc:
        logging.basicConfig(level=logging.INFO, format="[%(asctime)s] [%(levelname)s] %(message)s")
        LOG.exception("Quality runner failed: %s", exc)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
