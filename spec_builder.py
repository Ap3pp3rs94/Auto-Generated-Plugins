from __future__ import annotations

"""
Spec builder for the Francis plugin factory.

This generates PluginSpecs for the autonomous AI capability roadmap.

Upgrades:
- Deterministic AI-focused plugin specs across broad real-world use cases;
  no non-AI utility rotation.
- Continuous expansion uses short numbered names plus varied concrete use cases.
- Each spec includes a small set of concrete `use_cases`.
- capability_type and intended_domain are set on PluginSpec directly.

You can use this in place of Station A when you want autonomous progress
toward AI-consumable functionality rather than generic utility generation.
"""

from dataclasses import dataclass
from typing import Dict, List, Tuple

try:
    from .plugin_spec import PluginSpec
except ImportError:  # pragma: no cover - direct local execution
    from plugin_spec import PluginSpec


@dataclass(frozen=True)
class AICapabilityBlueprint:
    slug: str
    name: str
    category: str
    goal: str
    capability_type: str
    intended_domain: str
    tags: List[str]
    use_cases: List[str]


AI_CAPABILITY_ROADMAP: Tuple[AICapabilityBlueprint, ...] = (
    AICapabilityBlueprint(
        slug="ai_prompt_refinement_engine",
        name="AI Prompt Refinement Engine",
        category="ai_prompting",
        goal="Analyze task instructions and produce clearer, safer, more testable prompts.",
        capability_type="enrichment",
        intended_domain="AI prompt engineering and instruction quality",
        tags=["ai", "prompting", "instructions", "quality"],
        use_cases=[
            "Rewrite vague prompts into specific, testable instructions.",
            "Identify missing constraints, inputs, outputs, and acceptance criteria.",
            "Suggest prompt variants for different model sizes or latency budgets.",
        ],
    ),
    AICapabilityBlueprint(
        slug="ai_agent_task_planner",
        name="AI Agent Task Planner",
        category="ai_agents",
        goal="Turn a user objective into a sequenced AI-agent work plan with checkpoints and handoffs.",
        capability_type="system_automation",
        intended_domain="AI agent planning and task decomposition",
        tags=["ai", "agents", "planning", "workflow"],
        use_cases=[
            "Break a complex AI task into ordered implementation, review, and verification steps.",
            "Separate blocking work from parallelizable side tasks.",
            "Recommend checkpoints that prevent agent drift or repeated work.",
        ],
    ),
    AICapabilityBlueprint(
        slug="ai_tool_selection_advisor",
        name="AI Tool Selection Advisor",
        category="ai_agents",
        goal="Select the best available tool or integration for an AI workflow based on task requirements.",
        capability_type="integration",
        intended_domain="AI tool routing and integration choice",
        tags=["ai", "tools", "routing", "integrations"],
        use_cases=[
            "Map task requirements to candidate tools and explain tradeoffs.",
            "Flag when no external tool is needed.",
            "Recommend tool call order for multi-step AI workflows.",
        ],
    ),
    AICapabilityBlueprint(
        slug="ai_memory_compression_synthesizer",
        name="AI Memory Compression Synthesizer",
        category="ai_memory",
        goal="Compress conversation or project history into durable memory notes without losing decisions.",
        capability_type="research_synthesizer",
        intended_domain="AI memory, context management, and long-running work",
        tags=["ai", "memory", "context", "summarization"],
        use_cases=[
            "Summarize long work sessions into concise durable memory.",
            "Extract stable preferences, constraints, and project facts.",
            "Separate decisions from transient discussion.",
        ],
    ),
    AICapabilityBlueprint(
        slug="ai_context_window_optimizer",
        name="AI Context Window Optimizer",
        category="ai_memory",
        goal="Prioritize which context should be kept, compressed, or dropped before an AI model call.",
        capability_type="data_insight",
        intended_domain="AI context packing and token budget management",
        tags=["ai", "context", "tokens", "optimization"],
        use_cases=[
            "Rank context snippets by relevance to the current task.",
            "Detect redundant or stale context.",
            "Suggest compact replacements for large repeated sections.",
        ],
    ),
    AICapabilityBlueprint(
        slug="ai_output_quality_scorer",
        name="AI Output Quality Scorer",
        category="ai_evaluation",
        goal="Score an AI response for correctness, completeness, usefulness, and instruction adherence.",
        capability_type="scoring",
        intended_domain="AI evaluation and response quality control",
        tags=["ai", "evaluation", "quality", "scoring"],
        use_cases=[
            "Grade a response against a user request and rubric.",
            "Highlight missing requirements or weak assumptions.",
            "Produce an actionable improvement checklist.",
        ],
    ),
    AICapabilityBlueprint(
        slug="ai_hallucination_risk_auditor",
        name="AI Hallucination Risk Auditor",
        category="ai_evaluation",
        goal="Inspect AI-generated claims and flag unsupported, risky, or source-sensitive statements.",
        capability_type="scoring",
        intended_domain="AI reliability, hallucination detection, and factual risk",
        tags=["ai", "hallucination", "risk", "verification"],
        use_cases=[
            "Identify claims that need citations or external verification.",
            "Classify risk by domain such as legal, medical, financial, or technical.",
            "Suggest safer rewrites for uncertain claims.",
        ],
    ),
    AICapabilityBlueprint(
        slug="ai_retrieval_query_expander",
        name="AI Retrieval Query Expander",
        category="ai_retrieval",
        goal="Generate targeted retrieval queries and filters for RAG-style knowledge lookup.",
        capability_type="research_synthesizer",
        intended_domain="AI retrieval, RAG, search planning, and knowledge grounding",
        tags=["ai", "retrieval", "rag", "search"],
        use_cases=[
            "Expand a user question into precise search queries.",
            "Suggest metadata filters and source priorities.",
            "Separate broad discovery queries from exact verification queries.",
        ],
    ),
    AICapabilityBlueprint(
        slug="ai_multi_agent_handoff_planner",
        name="AI Multi-Agent Handoff Planner",
        category="ai_agents",
        goal="Design clear handoffs between specialized AI agents without duplicated ownership.",
        capability_type="system_automation",
        intended_domain="multi-agent AI coordination and delegation",
        tags=["ai", "agents", "handoff", "coordination"],
        use_cases=[
            "Define bounded responsibilities for multiple agents.",
            "Detect overlapping write scopes or duplicated investigation.",
            "Create integration checkpoints after delegated work completes.",
        ],
    ),
    AICapabilityBlueprint(
        slug="ai_prompt_test_case_generator",
        name="AI Prompt Test Case Generator",
        category="ai_evaluation",
        goal="Generate test cases that expose whether a prompt reliably produces the intended behavior.",
        capability_type="data_insight",
        intended_domain="AI prompt testing and regression coverage",
        tags=["ai", "prompting", "tests", "regression"],
        use_cases=[
            "Create normal, edge, and adversarial cases for a prompt.",
            "Define expected behavior checks for each case.",
            "Identify prompt ambiguities that tests should cover.",
        ],
    ),
    AICapabilityBlueprint(
        slug="ai_workflow_debugger",
        name="AI Workflow Debugger",
        category="ai_agents",
        goal="Analyze failed AI workflow traces and identify likely failure stages and fixes.",
        capability_type="data_insight",
        intended_domain="AI workflow observability and debugging",
        tags=["ai", "workflow", "debugging", "traces"],
        use_cases=[
            "Summarize failed model/tool-call traces.",
            "Identify prompt, tool, data, or validation failure points.",
            "Recommend the smallest fix to retry safely.",
        ],
    ),
    AICapabilityBlueprint(
        slug="ai_response_comparator",
        name="AI Response Comparator",
        category="ai_evaluation",
        goal="Compare multiple AI responses and rank them against a task-specific rubric.",
        capability_type="scoring",
        intended_domain="AI model comparison and answer selection",
        tags=["ai", "comparison", "evaluation", "rubric"],
        use_cases=[
            "Compare candidate responses for completeness and accuracy.",
            "Explain why one output is stronger than another.",
            "Merge the best parts of multiple responses into a recommendation.",
        ],
    ),
    AICapabilityBlueprint(
        slug="ai_instruction_conflict_detector",
        name="AI Instruction Conflict Detector",
        category="ai_safety",
        goal="Detect conflicting, unsafe, or impossible instructions before an AI workflow starts.",
        capability_type="scoring",
        intended_domain="AI instruction safety and constraint analysis",
        tags=["ai", "safety", "instructions", "constraints"],
        use_cases=[
            "Find contradictions between system, developer, and user instructions.",
            "Flag requests that cannot be satisfied under current constraints.",
            "Suggest a clarified instruction set for safe execution.",
        ],
    ),
    AICapabilityBlueprint(
        slug="ai_structured_prompt_builder",
        name="AI Structured Prompt Builder",
        category="ai_prompting",
        goal="Convert informal requirements into structured prompts with roles, inputs, outputs, and checks.",
        capability_type="enrichment",
        intended_domain="AI prompt architecture and reusable prompt templates",
        tags=["ai", "prompting", "templates", "structure"],
        use_cases=[
            "Create a reusable prompt from loose notes.",
            "Add explicit output schemas and validation checks.",
            "Preserve user intent while reducing ambiguity.",
        ],
    ),
    AICapabilityBlueprint(
        slug="ai_capability_router",
        name="AI Capability Router",
        category="ai_agents",
        goal="Route incoming AI tasks to the right capability type, model style, or agent role.",
        capability_type="integration",
        intended_domain="AI task routing and capability selection",
        tags=["ai", "routing", "capabilities", "agents"],
        use_cases=[
            "Classify a task into research, coding, evaluation, planning, or retrieval.",
            "Recommend the lowest-cost capable model or workflow.",
            "Identify when a task should be split across capabilities.",
        ],
    ),
    AICapabilityBlueprint(
        slug="ai_eval_rubric_generator",
        name="AI Eval Rubric Generator",
        category="ai_evaluation",
        goal="Create practical evaluation rubrics for AI tasks, prompts, and generated artifacts.",
        capability_type="research_synthesizer",
        intended_domain="AI evaluation design and acceptance criteria",
        tags=["ai", "evaluation", "rubric", "criteria"],
        use_cases=[
            "Generate scoring criteria for a specific AI task.",
            "Separate hard failures from quality preferences.",
            "Produce a checklist usable by humans or automated evaluators.",
        ],
    ),
    AICapabilityBlueprint(
        slug="ai_automation_safety_gate",
        name="AI Automation Safety Gate",
        category="ai_safety",
        goal="Review proposed AI automation steps for side effects, missing approvals, and rollback needs.",
        capability_type="scoring",
        intended_domain="AI automation safety and operational risk",
        tags=["ai", "automation", "safety", "risk"],
        use_cases=[
            "Score automation plans before execution.",
            "Flag destructive or irreversible steps.",
            "Recommend approval, logging, and rollback controls.",
        ],
    ),
    AICapabilityBlueprint(
        slug="ai_progress_tracker",
        name="AI Progress Tracker",
        category="ai_agents",
        goal="Track AI project progress from plans, logs, and completed steps into a clear next-action state.",
        capability_type="data_insight",
        intended_domain="AI project progress and long-running agent work",
        tags=["ai", "progress", "planning", "state"],
        use_cases=[
            "Summarize completed, active, blocked, and pending AI work.",
            "Detect repeated work or stale tasks.",
            "Recommend the next concrete action to preserve momentum.",
        ],
    ),
    AICapabilityBlueprint(
        slug="ai_citation_need_detector",
        name="AI Citation Need Detector",
        category="ai_evaluation",
        goal="Detect which AI-generated claims need citations, verification, or uncertainty language.",
        capability_type="scoring",
        intended_domain="AI citation planning and factual support",
        tags=["ai", "citations", "verification", "grounding"],
        use_cases=[
            "Mark claims that require citations before a response is shipped.",
            "Separate common reasoning from source-sensitive factual claims.",
            "Recommend uncertainty language for claims without evidence.",
        ],
    ),
    AICapabilityBlueprint(
        slug="ai_model_context_budget_estimator",
        name="AI Model Context Budget Estimator",
        category="ai_memory",
        goal="Estimate context budget pressure and recommend what to keep before a model call.",
        capability_type="data_insight",
        intended_domain="AI context budgeting and model-call preparation",
        tags=["ai", "context", "tokens", "budgeting"],
        use_cases=[
            "Estimate whether a payload will fit a target context window.",
            "Flag high-value context that should survive compression.",
            "Recommend token-saving cuts without losing requirements.",
        ],
    ),
    AICapabilityBlueprint(
        slug="ai_tool_call_sequence_builder",
        name="AI Tool Call Sequence Builder",
        category="ai_agents",
        goal="Plan a safe order of tool calls for multi-step AI workflows.",
        capability_type="integration",
        intended_domain="AI tool sequencing and orchestration",
        tags=["ai", "tools", "sequence", "orchestration"],
        use_cases=[
            "Choose which tool should run first, second, and last.",
            "Flag tool calls that need approval or verification first.",
            "Explain when no external tool call is needed.",
        ],
    ),
    AICapabilityBlueprint(
        slug="ai_agent_checkpoint_generator",
        name="AI Agent Checkpoint Generator",
        category="ai_agents",
        goal="Generate checkpoints that keep autonomous AI agents from drifting or repeating work.",
        capability_type="system_automation",
        intended_domain="AI agent checkpoints and autonomous run control",
        tags=["ai", "agents", "checkpoints", "drift"],
        use_cases=[
            "Create stop-and-check moments for long-running agent work.",
            "Separate done signals from blockers and assumptions.",
            "Prepare handoff checkpoints before another agent continues.",
        ],
    ),
    AICapabilityBlueprint(
        slug="ai_user_intent_classifier",
        name="AI User Intent Classifier",
        category="ai_agents",
        goal="Classify a user request into the right AI workflow intent and execution mode.",
        capability_type="integration",
        intended_domain="AI user intent routing and workflow selection",
        tags=["ai", "intent", "routing", "classification"],
        use_cases=[
            "Classify requests into coding, research, planning, evaluation, or safety.",
            "Detect whether the user wants action, explanation, review, or brainstorming.",
            "Recommend the smallest workflow that satisfies the request.",
        ],
    ),
    AICapabilityBlueprint(
        slug="ai_acceptance_criteria_extractor",
        name="AI Acceptance Criteria Extractor",
        category="ai_evaluation",
        goal="Extract testable acceptance criteria from messy AI task descriptions.",
        capability_type="research_synthesizer",
        intended_domain="AI task acceptance criteria and done-definition design",
        tags=["ai", "criteria", "evaluation", "requirements"],
        use_cases=[
            "Turn loose requirements into measurable pass/fail criteria.",
            "Separate hard failures from polish preferences.",
            "Produce a checklist usable by humans or validation tools.",
        ],
    ),
    AICapabilityBlueprint(
        slug="ai_prompt_constraint_mapper",
        name="AI Prompt Constraint Mapper",
        category="ai_prompting",
        goal="Map prompt requirements into explicit constraints, missing inputs, and rewrite targets.",
        capability_type="enrichment",
        intended_domain="AI prompt constraints and requirement mapping",
        tags=["ai", "prompting", "constraints", "requirements"],
        use_cases=[
            "Identify hidden or missing constraints in a prompt.",
            "Convert vague prompt language into concrete requirements.",
            "Recommend prompt rewrites that preserve constraints.",
        ],
    ),
    AICapabilityBlueprint(
        slug="ai_risk_register_builder",
        name="AI Risk Register Builder",
        category="ai_safety",
        goal="Build a compact risk register for AI-generated plans, tool calls, or automation steps.",
        capability_type="scoring",
        intended_domain="AI operational risk tracking and mitigation",
        tags=["ai", "risk", "safety", "controls"],
        use_cases=[
            "List AI workflow risks with mitigation controls.",
            "Flag destructive, factual, security, or release-sensitive actions.",
            "Recommend approval and rollback controls before execution.",
        ],
    ),
    AICapabilityBlueprint(
        slug="ai_trace_signal_extractor",
        name="AI Trace Signal Extractor",
        category="ai_agents",
        goal="Extract useful failure and progress signals from AI workflow traces.",
        capability_type="data_insight",
        intended_domain="AI trace analysis and workflow observability",
        tags=["ai", "traces", "signals", "debugging"],
        use_cases=[
            "Extract failure signals from model, tool, and validation traces.",
            "Classify trace events by likely failure stage.",
            "Recommend the smallest retry checkpoint.",
        ],
    ),
    AICapabilityBlueprint(
        slug="ai_response_merge_planner",
        name="AI Response Merge Planner",
        category="ai_evaluation",
        goal="Plan how to merge the strongest parts of multiple AI responses without losing requirements.",
        capability_type="scoring",
        intended_domain="AI response comparison and synthesis planning",
        tags=["ai", "comparison", "merge", "rubric"],
        use_cases=[
            "Rank candidate responses and identify the best base.",
            "Preserve unique useful details from lower-ranked responses.",
            "Create a final merge checklist against a rubric.",
        ],
    ),
    AICapabilityBlueprint(
        slug="ai_memory_fact_extractor",
        name="AI Memory Fact Extractor",
        category="ai_memory",
        goal="Extract durable facts, user preferences, decisions, and blockers for AI memory.",
        capability_type="research_synthesizer",
        intended_domain="AI durable memory and fact extraction",
        tags=["ai", "memory", "facts", "preferences"],
        use_cases=[
            "Identify facts that should be saved across runs.",
            "Separate durable decisions from temporary conversation.",
            "Carry blockers and preferences into the next AI workflow.",
        ],
    ),
    AICapabilityBlueprint(
        slug="ai_regression_watchlist_builder",
        name="AI Regression Watchlist Builder",
        category="ai_evaluation",
        goal="Create regression watchlists for prompts, plans, and AI-generated artifacts.",
        capability_type="data_insight",
        intended_domain="AI regression detection and workflow quality control",
        tags=["ai", "regression", "tests", "watchlist"],
        use_cases=[
            "List behaviors that must not regress after a prompt or workflow change.",
            "Create normal, edge, and failure watch items.",
            "Recommend checks that future AI runs should repeat.",
        ],
    ),
    AICapabilityBlueprint(
        slug="ai_grounded_answer_planner",
        name="AI Grounded Answer Planner",
        category="ai_retrieval",
        goal="Plan how an AI answer should combine retrieved evidence, caveats, and final response structure.",
        capability_type="research_synthesizer",
        intended_domain="AI grounded answer planning and evidence use",
        tags=["ai", "grounding", "retrieval", "answers"],
        use_cases=[
            "Separate answer claims that are supported from claims that need more retrieval.",
            "Recommend source-first response structure.",
            "Create caveats for uncertain or missing evidence.",
        ],
    ),
    AICapabilityBlueprint(
        slug="ai_tool_result_consistency_checker",
        name="AI Tool Result Consistency Checker",
        category="ai_evaluation",
        goal="Compare tool results, traces, and model conclusions for consistency before final output.",
        capability_type="scoring",
        intended_domain="AI tool result consistency and trace validation",
        tags=["ai", "tools", "consistency", "traces"],
        use_cases=[
            "Detect when a model conclusion contradicts tool output.",
            "Flag missing or stale tool evidence.",
            "Recommend the smallest verification retry.",
        ],
    ),
    AICapabilityBlueprint(
        slug="ai_operator_status_brief_builder",
        name="AI Operator Status Brief Builder",
        category="ai_agents",
        goal="Turn autonomous AI run state into a concise operator-facing status brief.",
        capability_type="data_insight",
        intended_domain="AI operator visibility and run status reporting",
        tags=["ai", "status", "operators", "progress"],
        use_cases=[
            "Summarize what changed, what passed, and what is blocked.",
            "Expose current run health without noisy logs.",
            "Recommend the next operator action.",
        ],
    ),
    AICapabilityBlueprint(
        slug="ai_prompt_injection_surface_scanner",
        name="AI Prompt Injection Surface Scanner",
        category="ai_safety",
        goal="Scan prompts, retrieved text, and tool outputs for prompt-injection risk signals.",
        capability_type="scoring",
        intended_domain="AI prompt injection and instruction hierarchy safety",
        tags=["ai", "safety", "injection", "instructions"],
        use_cases=[
            "Detect text that tries to override higher-priority instructions.",
            "Flag retrieved content that should be treated as untrusted.",
            "Recommend safe handling rules before model use.",
        ],
    ),
    AICapabilityBlueprint(
        slug="ai_workflow_retry_strategy_planner",
        name="AI Workflow Retry Strategy Planner",
        category="ai_agents",
        goal="Plan safe retries for failed AI workflows without repeating the same failure.",
        capability_type="system_automation",
        intended_domain="AI workflow retry planning and failure recovery",
        tags=["ai", "retry", "workflow", "debugging"],
        use_cases=[
            "Convert failure traces into retry strategies.",
            "Change one variable at a time for safer debugging.",
            "Recommend when to stop retrying and ask for input.",
        ],
    ),
    AICapabilityBlueprint(
        slug="ai_model_selection_scorecard",
        name="AI Model Selection Scorecard",
        category="ai_agents",
        goal="Score which model style or capability tier fits a task based on cost, risk, and complexity.",
        capability_type="scoring",
        intended_domain="AI model selection and task-fit scoring",
        tags=["ai", "models", "routing", "scorecard"],
        use_cases=[
            "Choose between fast, cheap, reasoning-heavy, or tool-using workflows.",
            "Flag tasks that need stronger verification.",
            "Recommend the lowest sufficient capability tier.",
        ],
    ),
    AICapabilityBlueprint(
        slug="ai_requirement_gap_analyzer",
        name="AI Requirement Gap Analyzer",
        category="ai_evaluation",
        goal="Find missing requirements, assumptions, and open questions before an AI task starts.",
        capability_type="research_synthesizer",
        intended_domain="AI requirements analysis and task readiness",
        tags=["ai", "requirements", "gaps", "readiness"],
        use_cases=[
            "Identify missing inputs that block reliable execution.",
            "Separate hard requirements from assumptions.",
            "Recommend clarification questions only when necessary.",
        ],
    ),
    AICapabilityBlueprint(
        slug="ai_artifact_release_note_generator",
        name="AI Artifact Release Note Generator",
        category="ai_agents",
        goal="Generate concise release notes for AI-created artifacts, including validation evidence and risks.",
        capability_type="data_insight",
        intended_domain="AI artifact release notes and change communication",
        tags=["ai", "release-notes", "artifacts", "validation"],
        use_cases=[
            "Summarize generated artifact changes for users.",
            "Include validation and semantic-depth evidence.",
            "Call out known risks, limitations, and next checks.",
        ],
    ),
    AICapabilityBlueprint(
        slug="ai_data_contract_mapper",
        name="AI Data Contract Mapper",
        category="ai_evaluation",
        goal="Map expected AI capability input and output contracts from task descriptions and examples.",
        capability_type="enrichment",
        intended_domain="AI data contracts and schema planning",
        tags=["ai", "schema", "contracts", "capabilities"],
        use_cases=[
            "Extract expected payload fields and result fields.",
            "Flag schema ambiguity before implementation.",
            "Recommend validation checks for capability contracts.",
        ],
    ),
    AICapabilityBlueprint(
        slug="ai_autonomous_run_governor",
        name="AI Autonomous Run Governor",
        category="ai_safety",
        goal="Decide whether an autonomous AI run should continue, pause, repair, or ask for human input.",
        capability_type="scoring",
        intended_domain="AI autonomous run governance and stop conditions",
        tags=["ai", "autonomous", "governance", "safety"],
        use_cases=[
            "Detect when repeated failures should stop the run.",
            "Recommend pause, repair, continue, or escalate decisions.",
            "Preserve progress while preventing runaway automation.",
        ],
    ),
    AICapabilityBlueprint(
        slug="ai_plugin_spec_architect",
        name="AI Capability Spec Architect",
        category="ai_plugin_factory",
        goal="Design precise, non-duplicate capability specs for new AI capabilities before generation starts.",
        capability_type="enrichment",
        intended_domain="AI capability specification design and capability boundaries",
        tags=["ai", "capabilities", "specs", "factory"],
        use_cases=[
            "Turn a loose capability idea into a complete generation blueprint.",
            "Define capability boundaries so the module does not duplicate existing capabilities.",
            "List required inputs, outputs, acceptance criteria, and quality signals before build.",
        ],
    ),
    AICapabilityBlueprint(
        slug="ai_plugin_logic_blueprint_designer",
        name="AI Capability Logic Blueprint Designer",
        category="ai_plugin_factory",
        goal="Plan deterministic capability logic before code generation so the body performs the actual capability.",
        capability_type="system_automation",
        intended_domain="AI capability deterministic logic planning and implementation design",
        tags=["ai", "capabilities", "logic", "factory"],
        use_cases=[
            "Translate a capability spec into deterministic analysis steps.",
            "Define payload fields, scoring signals, and output constructors.",
            "Prevent generic template bodies by naming capability-specific algorithms.",
        ],
    ),
    AICapabilityBlueprint(
        slug="ai_plugin_quality_gate_designer",
        name="AI Capability Quality Gate Designer",
        category="ai_plugin_factory",
        goal="Create semantic quality gates that reject shallow, duplicate, or off-capability generated modules.",
        capability_type="scoring",
        intended_domain="AI capability validation, semantic depth, and rejection policy",
        tags=["ai", "capabilities", "quality", "validation"],
        use_cases=[
            "Define required detail keys and pass/fail rules for a capability.",
            "Generate semantic probe payloads that force output differences.",
            "Explain why a capability should be accepted, repaired, or rejected.",
        ],
    ),
    AICapabilityBlueprint(
        slug="ai_plugin_test_payload_generator",
        name="AI Capability Test Payload Generator",
        category="ai_plugin_factory",
        goal="Generate focused test payloads that prove a capability reacts to payload meaning rather than structure alone.",
        capability_type="data_insight",
        intended_domain="AI capability test design and semantic probe generation",
        tags=["ai", "capabilities", "tests", "semantic-depth"],
        use_cases=[
            "Create positive, edge, and adversarial payloads for a capability.",
            "Define expected output differences across semantically different payloads.",
            "Produce regression watchlists for future capability repairs.",
        ],
    ),
    AICapabilityBlueprint(
        slug="ai_plugin_duplicate_detector",
        name="AI Capability Duplicate Detector",
        category="ai_plugin_factory",
        goal="Detect when a proposed AI capability duplicates existing behavior and recommend merge, reject, or redesign.",
        capability_type="scoring",
        intended_domain="AI capability uniqueness, overlap analysis, and roadmap hygiene",
        tags=["ai", "capabilities", "duplicates", "roadmap"],
        use_cases=[
            "Compare a proposed capability against existing capability names, goals, and output contracts.",
            "Create uniqueness fingerprints for capability ideas.",
            "Recommend whether to merge, reject, or redesign overlapping capabilities.",
        ],
    ),
    AICapabilityBlueprint(
        slug="ai_plugin_repair_strategy_planner",
        name="AI Capability Repair Strategy Planner",
        category="ai_plugin_factory",
        goal="Plan targeted repairs for weak generated capabilities based on validation failures and semantic gaps.",
        capability_type="system_automation",
        intended_domain="AI capability repair planning and capability-specific improvement",
        tags=["ai", "capabilities", "repair", "quality"],
        use_cases=[
            "Turn quality-runner failures into a specific repair plan.",
            "Separate shallow output, missing keys, semantic similarity, and runtime errors.",
            "Define acceptance checks before a repaired capability can replace the old one.",
        ],
    ),
    AICapabilityBlueprint(
        slug="ai_plugin_release_packager",
        name="AI Capability Release Packager",
        category="ai_plugin_factory",
        goal="Package generated capability modules for GitHub release with validation evidence, user-facing notes, and rollback guidance.",
        capability_type="data_insight",
        intended_domain="AI capability release packaging, publishing, and operator visibility",
        tags=["ai", "capabilities", "release", "github"],
        use_cases=[
            "Prepare commit-ready release notes for generated capabilities.",
            "Summarize validation, semantic depth, and quality-runner evidence.",
            "Recommend publish, hold, or rollback actions for capability releases.",
        ],
    ),
    AICapabilityBlueprint(
        slug="ai_plugin_factory_backlog_planner",
        name="AI Capability Factory Backlog Planner",
        category="ai_plugin_factory",
        goal="Plan the next high-value AI capability backlog so autonomous generation keeps improving itself intentionally.",
        capability_type="research_synthesizer",
        intended_domain="AI capability factory roadmap planning and self-improvement backlog",
        tags=["ai", "capabilities", "backlog", "factory"],
        use_cases=[
            "Prioritize future capabilities by factory leverage, uniqueness, and user value.",
            "Define dependency order between spec, generation, validation, repair, and release capabilities.",
            "Generate next-capability candidates that avoid random or duplicate roadmap expansion.",
        ],
    ),
    AICapabilityBlueprint(
        slug="ai_prompt_persona_adapter",
        name="AI Prompt Persona Adapter",
        category="ai_prompting",
        goal="Adapt prompts for a target audience, role, or expertise level without changing the core task.",
        capability_type="enrichment",
        intended_domain="AI prompt persona adaptation and audience fit",
        tags=["ai", "prompting", "persona", "audience"],
        use_cases=[
            "Rewrite prompts for beginner, expert, executive, or operator audiences.",
            "Preserve task constraints while changing tone and explanation depth.",
            "Flag persona changes that would distort the original request.",
        ],
    ),
    AICapabilityBlueprint(
        slug="ai_prompt_output_schema_designer",
        name="AI Prompt Output Schema Designer",
        category="ai_prompting",
        goal="Design strict output schemas and response sections for prompts that need reliable downstream parsing.",
        capability_type="enrichment",
        intended_domain="AI prompt output schemas and structured response design",
        tags=["ai", "prompting", "schema", "outputs"],
        use_cases=[
            "Convert loose output expectations into explicit fields and sections.",
            "Recommend required, optional, and diagnostic output keys.",
            "Add validation notes that make model output easier to consume.",
        ],
    ),
    AICapabilityBlueprint(
        slug="ai_model_failure_mode_classifier",
        name="AI Model Failure Mode Classifier",
        category="ai_evaluation",
        goal="Classify model failures into prompt, context, reasoning, tool, retrieval, or validation causes.",
        capability_type="scoring",
        intended_domain="AI failure classification and model behavior debugging",
        tags=["ai", "evaluation", "failures", "debugging"],
        use_cases=[
            "Label failed outputs by likely failure mode.",
            "Separate prompt ambiguity from missing evidence or tool mismatch.",
            "Recommend the smallest repair path for each failure class.",
        ],
    ),
    AICapabilityBlueprint(
        slug="ai_evidence_gap_prioritizer",
        name="AI Evidence Gap Prioritizer",
        category="ai_retrieval",
        goal="Prioritize missing evidence that must be retrieved before an AI answer can be trusted.",
        capability_type="research_synthesizer",
        intended_domain="AI evidence gaps and retrieval prioritization",
        tags=["ai", "retrieval", "evidence", "grounding"],
        use_cases=[
            "Rank unsupported claims by risk and retrieval urgency.",
            "Separate nice-to-have sources from blocking evidence gaps.",
            "Recommend targeted retrieval questions for each gap.",
        ],
    ),
    AICapabilityBlueprint(
        slug="ai_source_trust_ranker",
        name="AI Source Trust Ranker",
        category="ai_retrieval",
        goal="Rank provided sources by likely trust, relevance, freshness, and answer usefulness.",
        capability_type="scoring",
        intended_domain="AI source evaluation and grounded answer preparation",
        tags=["ai", "sources", "trust", "retrieval"],
        use_cases=[
            "Score candidate sources before synthesis.",
            "Flag stale, weak, or unsupported source notes.",
            "Recommend which sources should anchor the final answer.",
        ],
    ),
    AICapabilityBlueprint(
        slug="ai_context_relevance_ranker",
        name="AI Context Relevance Ranker",
        category="ai_memory",
        goal="Rank context snippets by relevance, freshness, and necessity for the next model call.",
        capability_type="data_insight",
        intended_domain="AI context relevance ranking and context packing",
        tags=["ai", "context", "ranking", "memory"],
        use_cases=[
            "Choose which notes should stay in context.",
            "Flag stale or redundant snippets before prompt assembly.",
            "Explain why a context item is keep, compress, or drop.",
        ],
    ),
    AICapabilityBlueprint(
        slug="ai_memory_conflict_resolver",
        name="AI Memory Conflict Resolver",
        category="ai_memory",
        goal="Detect conflicting memory facts and recommend which version should be kept, updated, or retired.",
        capability_type="research_synthesizer",
        intended_domain="AI memory conflict detection and durable fact hygiene",
        tags=["ai", "memory", "conflicts", "facts"],
        use_cases=[
            "Compare new notes against existing durable memory.",
            "Flag contradictions in preferences, decisions, or constraints.",
            "Recommend keep, update, merge, or retire actions.",
        ],
    ),
    AICapabilityBlueprint(
        slug="ai_agent_role_boundary_mapper",
        name="AI Agent Role Boundary Mapper",
        category="ai_agents",
        goal="Define clear role boundaries for multiple AI agents so ownership does not overlap.",
        capability_type="system_automation",
        intended_domain="AI agent role design and responsibility boundaries",
        tags=["ai", "agents", "roles", "handoff"],
        use_cases=[
            "Map tasks to agent roles and ownership boundaries.",
            "Detect duplicate ownership between agents.",
            "Create handoff notes that preserve accountability.",
        ],
    ),
    AICapabilityBlueprint(
        slug="ai_parallel_work_detector",
        name="AI Parallel Work Detector",
        category="ai_agents",
        goal="Identify which parts of an AI workflow can run in parallel without blocking or duplicating work.",
        capability_type="system_automation",
        intended_domain="AI workflow parallelization and dependency planning",
        tags=["ai", "agents", "parallel", "planning"],
        use_cases=[
            "Separate blocking tasks from sidecar tasks.",
            "Detect dependency conflicts before delegating work.",
            "Recommend safe parallel work packets with checkpoints.",
        ],
    ),
    AICapabilityBlueprint(
        slug="ai_tool_permission_gate",
        name="AI Tool Permission Gate",
        category="ai_safety",
        goal="Decide when AI tool use requires approval, extra verification, or safer alternatives.",
        capability_type="scoring",
        intended_domain="AI tool permissioning and safe action control",
        tags=["ai", "tools", "permissions", "safety"],
        use_cases=[
            "Flag destructive, external, or privacy-sensitive tool calls.",
            "Recommend approval and logging requirements.",
            "Separate safe read-only tool use from risky mutation.",
        ],
    ),
    AICapabilityBlueprint(
        slug="ai_tool_argument_sanitizer",
        name="AI Tool Argument Sanitizer",
        category="ai_safety",
        goal="Inspect proposed tool arguments for unsafe paths, missing constraints, and prompt-injection contamination.",
        capability_type="scoring",
        intended_domain="AI tool argument safety and input sanitization",
        tags=["ai", "tools", "sanitization", "safety"],
        use_cases=[
            "Detect risky file paths, broad globs, or destructive flags.",
            "Flag untrusted retrieved content inside tool arguments.",
            "Recommend safer bounded arguments before execution.",
        ],
    ),
    AICapabilityBlueprint(
        slug="ai_eval_failure_classifier",
        name="AI Eval Failure Classifier",
        category="ai_evaluation",
        goal="Classify evaluation failures into blocking defects, missing evidence, polish gaps, or rubric mismatch.",
        capability_type="scoring",
        intended_domain="AI evaluation failure triage and repair routing",
        tags=["ai", "evaluation", "failures", "rubric"],
        use_cases=[
            "Group failed checks by severity and repair path.",
            "Separate hard acceptance failures from subjective quality issues.",
            "Recommend whether to repair, regenerate, or accept with caveats.",
        ],
    ),
    AICapabilityBlueprint(
        slug="ai_response_actionability_scorer",
        name="AI Response Actionability Scorer",
        category="ai_evaluation",
        goal="Score whether an AI response gives concrete, usable next actions instead of vague guidance.",
        capability_type="scoring",
        intended_domain="AI response actionability and user usefulness scoring",
        tags=["ai", "evaluation", "actionability", "quality"],
        use_cases=[
            "Identify generic advice that lacks execution detail.",
            "Score next actions by specificity and usefulness.",
            "Recommend edits that make a response immediately usable.",
        ],
    ),
    AICapabilityBlueprint(
        slug="ai_user_clarification_question_builder",
        name="AI User Clarification Question Builder",
        category="ai_prompting",
        goal="Generate the smallest useful set of clarification questions when an AI task is under-specified.",
        capability_type="enrichment",
        intended_domain="AI clarification strategy and missing input collection",
        tags=["ai", "prompting", "clarification", "requirements"],
        use_cases=[
            "Ask only questions that unblock execution.",
            "Avoid unnecessary clarification when assumptions are safe.",
            "Group questions by objective, constraints, data, and output format.",
        ],
    ),
    AICapabilityBlueprint(
        slug="ai_assumption_tracker",
        name="AI Assumption Tracker",
        category="ai_evaluation",
        goal="Extract, score, and track assumptions that an AI workflow is relying on.",
        capability_type="research_synthesizer",
        intended_domain="AI assumptions, uncertainty tracking, and task readiness",
        tags=["ai", "assumptions", "uncertainty", "requirements"],
        use_cases=[
            "List explicit and implicit assumptions in a plan or answer.",
            "Score assumptions by risk and confidence.",
            "Recommend which assumptions need user confirmation or evidence.",
        ],
    ),
    AICapabilityBlueprint(
        slug="ai_change_impact_summarizer",
        name="AI Change Impact Summarizer",
        category="ai_agents",
        goal="Summarize the user-facing, technical, and validation impact of AI-generated changes.",
        capability_type="data_insight",
        intended_domain="AI change impact analysis and release communication",
        tags=["ai", "changes", "impact", "release"],
        use_cases=[
            "Explain what changed and why it matters.",
            "Separate user-facing effects from internal implementation details.",
            "Call out validation evidence and residual risks.",
        ],
    ),
    AICapabilityBlueprint(
        slug="ai_verification_plan_builder",
        name="AI Verification Plan Builder",
        category="ai_evaluation",
        goal="Build focused verification plans for AI-generated code, answers, workflows, or artifacts.",
        capability_type="system_automation",
        intended_domain="AI verification planning and acceptance checks",
        tags=["ai", "verification", "tests", "quality"],
        use_cases=[
            "Turn acceptance criteria into concrete verification steps.",
            "Separate automated checks from human review.",
            "Recommend evidence that should be captured before release.",
        ],
    ),
    AICapabilityBlueprint(
        slug="ai_red_team_prompt_probe_builder",
        name="AI Red Team Prompt Probe Builder",
        category="ai_safety",
        goal="Create adversarial prompt probes that test instruction hierarchy, safety, and data leakage boundaries.",
        capability_type="data_insight",
        intended_domain="AI red-team prompt testing and safety probing",
        tags=["ai", "safety", "red-team", "prompting"],
        use_cases=[
            "Generate prompt probes for injection, leakage, and instruction override.",
            "Define expected safe behavior for each probe.",
            "Prioritize probes by risk and likelihood.",
        ],
    ),
    AICapabilityBlueprint(
        slug="ai_rollback_readiness_checker",
        name="AI Rollback Readiness Checker",
        category="ai_safety",
        goal="Check whether an AI-generated change has enough rollback, backup, and recovery planning.",
        capability_type="scoring",
        intended_domain="AI rollback readiness and operational safety",
        tags=["ai", "rollback", "safety", "release"],
        use_cases=[
            "Flag changes that lack rollback steps.",
            "Score backup, recovery, and blast-radius readiness.",
            "Recommend hold, proceed, or add safeguards.",
        ],
    ),
    AICapabilityBlueprint(
        slug="ai_live_run_anomaly_detector",
        name="AI Live Run Anomaly Detector",
        category="ai_agents",
        goal="Detect anomalous behavior in a live autonomous AI run from logs, progress, and repeated actions.",
        capability_type="monitoring",
        intended_domain="AI live-run monitoring and anomaly detection",
        tags=["ai", "monitoring", "anomalies", "autonomous"],
        use_cases=[
            "Detect repeated failures, loops, or unexpected output bursts.",
            "Flag stalled, noisy, or unsafe autonomous run states.",
            "Recommend continue, pause, repair, or escalate actions.",
        ],
    ),
    AICapabilityBlueprint(
        slug="ai_capability_dependency_mapper",
        name="AI Capability Dependency Mapper",
        category="ai_plugin_factory",
        goal="Map dependencies between AI capabilities so generated modules compose without overlap.",
        capability_type="data_insight",
        intended_domain="AI capability dependency mapping and composition planning",
        tags=["ai", "capabilities", "dependencies", "factory"],
        use_cases=[
            "Identify upstream and downstream capabilities for a proposed module.",
            "Flag circular or duplicate capability relationships.",
            "Recommend composition order for multi-capability workflows.",
        ],
    ),
    AICapabilityBlueprint(
        slug="ai_plugin_profile_gap_detector",
        name="AI Capability Profile Gap Detector",
        category="ai_plugin_factory",
        goal="Detect missing or weak deterministic profiles before new AI capabilities are generated.",
        capability_type="scoring",
        intended_domain="AI capability profile coverage and generation readiness",
        tags=["ai", "capabilities", "profiles", "quality"],
        use_cases=[
            "Compare roadmap specs against available deterministic profiles.",
            "Flag specs that would fall back to generic generation.",
            "Recommend profile families or new profile implementations.",
        ],
    ),
    AICapabilityBlueprint(
        slug="ai_semantic_probe_result_analyzer",
        name="AI Semantic Probe Result Analyzer",
        category="ai_plugin_factory",
        goal="Analyze semantic probe results and explain whether a generated capability is real, shallow, or off-target.",
        capability_type="scoring",
        intended_domain="AI semantic-depth evaluation and capability acceptance",
        tags=["ai", "capabilities", "semantic-depth", "validation"],
        use_cases=[
            "Compare probe outputs for meaningful behavioral differences.",
            "Identify string interpolation masquerading as analysis.",
            "Recommend accept, repair, or discard decisions with evidence.",
        ],
    ),
    AICapabilityBlueprint(
        slug="ai_release_readiness_scorecard",
        name="AI Release Readiness Scorecard",
        category="ai_plugin_factory",
        goal="Score whether an AI capability module is ready to publish based on quality, uniqueness, and validation evidence.",
        capability_type="scoring",
        intended_domain="AI capability release readiness and GitHub publishing quality",
        tags=["ai", "capabilities", "release", "scorecard"],
        use_cases=[
            "Score validation, semantic depth, uniqueness, and documentation readiness.",
            "Flag release blockers before commit and push.",
            "Recommend publish, repair, or discard with specific evidence.",
        ],
    ),
)


@dataclass(frozen=True)
class ContinuousExpansionFamily:
    slug: str
    name: str
    category: str
    goal_template: str
    capability_type: str
    intended_domain_template: str
    tags: List[str]
    use_case_templates: List[str]


@dataclass(frozen=True)
class ContinuousExpansionTarget:
    slug: str
    name: str
    domain_phrase: str
    tags: List[str]


@dataclass(frozen=True)
class ContinuousExpansionDimension:
    slug: str
    name: str
    domain_phrase: str
    tags: List[str]


BASE_CONTINUOUS_EXPANSION_TARGETS: Tuple[ContinuousExpansionTarget, ...] = (
    ContinuousExpansionTarget("coding_agent", "Coding Agent", "AI coding agents and repository work", ["coding", "agents"]),
    ContinuousExpansionTarget("research_agent", "Research Agent", "AI research, retrieval, and synthesis work", ["research", "retrieval"]),
    ContinuousExpansionTarget("customer_support", "Customer Support", "AI customer support and service workflows", ["support", "service"]),
    ContinuousExpansionTarget("sales_ops", "Sales Ops", "AI sales operations and account workflows", ["sales", "business"]),
    ContinuousExpansionTarget("clinical_admin", "Clinical Admin", "AI clinical administration and healthcare operations", ["healthcare", "clinical"]),
    ContinuousExpansionTarget("legal_review", "Legal Review", "AI legal review and compliance workflows", ["legal", "compliance"]),
    ContinuousExpansionTarget("finance_ops", "Finance Ops", "AI finance operations and risk review", ["finance", "risk"]),
    ContinuousExpansionTarget("education_tutor", "Education Tutor", "AI education, tutoring, and learning workflows", ["education", "learning"]),
    ContinuousExpansionTarget("devops_release", "DevOps Release", "AI DevOps release and infrastructure workflows", ["devops", "release"]),
    ContinuousExpansionTarget("data_analysis", "Data Analysis", "AI data analysis and analytics workflows", ["data", "analytics"]),
    ContinuousExpansionTarget("security_review", "Security Review", "AI security review and threat analysis", ["security", "safety"]),
    ContinuousExpansionTarget("product_manager", "Product Manager", "AI product planning and roadmap workflows", ["product", "planning"]),
    ContinuousExpansionTarget("content_strategy", "Content Strategy", "AI content strategy and editorial workflows", ["content", "strategy"]),
    ContinuousExpansionTarget("personal_assistant", "Personal Assistant", "AI personal productivity and scheduling workflows", ["productivity", "assistant"]),
    ContinuousExpansionTarget("operations_monitor", "Operations Monitor", "AI operations monitoring and incident response", ["operations", "monitoring"]),
    ContinuousExpansionTarget("plugin_factory", "Capability Factory", "AI capability factory and generated module operations", ["capabilities", "factory"]),
)


EXPANSIVE_AI_USE_CASE_TARGETS: Tuple[ContinuousExpansionTarget, ...] = (
    ContinuousExpansionTarget("agriculture_ops", "Agriculture Ops", "AI agriculture, farm operations, crop monitoring, and controlled-environment grow workflows", ["agriculture", "farming", "operations"]),
    ContinuousExpansionTarget("manufacturing_ops", "Manufacturing Ops", "AI manufacturing, production line, quality, and plant operations workflows", ["manufacturing", "quality", "operations"]),
    ContinuousExpansionTarget("warehouse_ops", "Warehouse Ops", "AI warehouse, inventory, picking, packing, and fulfillment workflows", ["warehouse", "inventory", "fulfillment"]),
    ContinuousExpansionTarget("logistics_dispatch", "Logistics Dispatch", "AI logistics, routing, fleet dispatch, and delivery coordination workflows", ["logistics", "fleet", "routing"]),
    ContinuousExpansionTarget("supply_chain", "Supply Chain", "AI supply chain planning, vendor risk, procurement, and replenishment workflows", ["supply-chain", "procurement", "planning"]),
    ContinuousExpansionTarget("construction_ops", "Construction Ops", "AI construction project, site safety, punch list, and contractor coordination workflows", ["construction", "field-ops", "safety"]),
    ContinuousExpansionTarget("real_estate_ops", "Real Estate Ops", "AI real estate listing, lease, appraisal, due diligence, and portfolio workflows", ["real-estate", "contracts", "portfolio"]),
    ContinuousExpansionTarget("insurance_claims", "Insurance Claims", "AI insurance claims, underwriting, policy review, and fraud-risk workflows", ["insurance", "claims", "risk"]),
    ContinuousExpansionTarget("banking_ops", "Banking Ops", "AI banking operations, financial controls, customer risk, and account workflow support", ["banking", "finance", "controls"]),
    ContinuousExpansionTarget("tax_accounting", "Tax Accounting", "AI tax, bookkeeping, reconciliation, and accounting workflow support", ["tax", "accounting", "finance"]),
    ContinuousExpansionTarget("public_sector", "Public Sector", "AI public-sector service, permitting, benefits, and civic operations workflows", ["government", "civic", "services"]),
    ContinuousExpansionTarget("nonprofit_ops", "Nonprofit Ops", "AI nonprofit fundraising, grant reporting, volunteer, and impact measurement workflows", ["nonprofit", "grants", "impact"]),
    ContinuousExpansionTarget("energy_utilities", "Energy Utilities", "AI energy, utility operations, grid planning, outage, and sustainability workflows", ["energy", "utilities", "sustainability"]),
    ContinuousExpansionTarget("climate_resilience", "Climate Resilience", "AI climate adaptation, environmental monitoring, resilience, and mitigation workflows", ["climate", "environment", "resilience"]),
    ContinuousExpansionTarget("healthcare_clinical", "Healthcare Clinical", "AI clinical documentation, care coordination, patient safety, and health operations workflows", ["healthcare", "clinical", "documentation"]),
    ContinuousExpansionTarget("biotech_lab", "Biotech Lab", "AI biotech, lab notebook, assay review, experiment tracking, and research operations workflows", ["biotech", "lab", "research"]),
    ContinuousExpansionTarget("pharma_regulatory", "Pharma Regulatory", "AI pharma regulatory, submission readiness, safety review, and evidence workflows", ["pharma", "regulatory", "evidence"]),
    ContinuousExpansionTarget("veterinary_ops", "Veterinary Ops", "AI veterinary clinic, case note, treatment plan, and client communication workflows", ["veterinary", "clinical", "service"]),
    ContinuousExpansionTarget("food_service", "Food Service", "AI restaurant, food safety, menu, kitchen ops, and guest-service workflows", ["food-service", "restaurant", "safety"]),
    ContinuousExpansionTarget("hospitality_travel", "Hospitality Travel", "AI hospitality, booking, itinerary, guest recovery, and travel operations workflows", ["hospitality", "travel", "service"]),
    ContinuousExpansionTarget("retail_merchandising", "Retail Merchandising", "AI retail merchandising, assortment, pricing, store ops, and customer journey workflows", ["retail", "merchandising", "pricing"]),
    ContinuousExpansionTarget("marketplace_ops", "Marketplace Ops", "AI marketplace trust, seller operations, catalog quality, and transaction workflows", ["marketplace", "trust", "catalog"]),
    ContinuousExpansionTarget("creator_economy", "Creator Economy", "AI creator workflow, audience planning, content packaging, and sponsor operations", ["creator", "content", "audience"]),
    ContinuousExpansionTarget("media_production", "Media Production", "AI media production, editorial planning, transcript, rights, and publishing workflows", ["media", "production", "publishing"]),
    ContinuousExpansionTarget("gaming_community", "Gaming Community", "AI game design, live ops, moderation, economy, and player-support workflows", ["gaming", "community", "moderation"]),
    ContinuousExpansionTarget("sports_analytics", "Sports Analytics", "AI sports analytics, scouting, training, injury-risk, and performance workflows", ["sports", "analytics", "performance"]),
    ContinuousExpansionTarget("fitness_wellness", "Fitness Wellness", "AI fitness coaching, wellness planning, habit review, and progress workflows", ["fitness", "wellness", "coaching"]),
    ContinuousExpansionTarget("home_maintenance", "Home Maintenance", "AI home repair, maintenance planning, contractor scope, and inspection workflows", ["home", "maintenance", "inspection"]),
    ContinuousExpansionTarget("automotive_service", "Automotive Service", "AI automotive diagnostics, repair intake, maintenance, and fleet service workflows", ["automotive", "maintenance", "fleet"]),
    ContinuousExpansionTarget("field_service", "Field Service", "AI field service dispatch, work order, technician handoff, and service verification workflows", ["field-service", "dispatch", "work-orders"]),
    ContinuousExpansionTarget("iot_robotics", "IoT Robotics", "AI IoT, robotics, device telemetry, autonomy review, and maintenance workflows", ["iot", "robotics", "telemetry"]),
    ContinuousExpansionTarget("education_admin", "Education Admin", "AI education administration, curriculum operations, student support, and assessment workflows", ["education", "curriculum", "student-support"]),
    ContinuousExpansionTarget("learning_design", "Learning Design", "AI instructional design, course review, practice generation, and learner feedback workflows", ["learning", "instructional-design", "assessment"]),
    ContinuousExpansionTarget("translation_localization", "Translation Localization", "AI translation, localization, cultural review, and multilingual content workflows", ["translation", "localization", "language"]),
    ContinuousExpansionTarget("accessibility_review", "Accessibility Review", "AI accessibility audit, accommodation planning, inclusive design, and content remediation workflows", ["accessibility", "inclusion", "review"]),
    ContinuousExpansionTarget("recruiting_ops", "Recruiting Ops", "AI recruiting, interview planning, candidate review, and hiring workflow support", ["recruiting", "hiring", "talent"]),
    ContinuousExpansionTarget("employee_enablement", "Employee Enablement", "AI employee onboarding, enablement, policy Q&A, and internal support workflows", ["hr", "enablement", "onboarding"]),
    ContinuousExpansionTarget("project_delivery", "Project Delivery", "AI project delivery, milestone tracking, risk review, and stakeholder update workflows", ["project", "delivery", "risk"]),
    ContinuousExpansionTarget("design_review", "Design Review", "AI product design critique, UX review, design-system, and accessibility workflows", ["design", "ux", "review"]),
    ContinuousExpansionTarget("procurement_ops", "Procurement Ops", "AI procurement intake, vendor comparison, contract handoff, and spend review workflows", ["procurement", "vendors", "contracts"]),
    ContinuousExpansionTarget("contract_ops", "Contract Ops", "AI contract operations, clause review, obligation tracking, and negotiation prep workflows", ["contracts", "legal", "obligations"]),
    ContinuousExpansionTarget("policy_governance", "Policy Governance", "AI policy governance, control mapping, audit evidence, and exception workflow support", ["policy", "governance", "audit"]),
    ContinuousExpansionTarget("privacy_ops", "Privacy Ops", "AI privacy operations, data request triage, DPIA review, and consent workflows", ["privacy", "data-governance", "compliance"]),
    ContinuousExpansionTarget("cyber_defense", "Cyber Defense", "AI cyber defense, alert triage, incident handling, and threat intelligence workflows", ["cybersecurity", "incidents", "threat-intel"]),
    ContinuousExpansionTarget("science_research", "Science Research", "AI scientific literature, experiment design, evidence synthesis, and peer-review workflows", ["science", "research", "evidence"]),
    ContinuousExpansionTarget("personal_finance", "Personal Finance", "AI personal finance planning, budgeting, debt, and financial decision workflows", ["personal-finance", "budgeting", "planning"]),
    ContinuousExpansionTarget("life_admin", "Life Admin", "AI personal administration, paperwork, appointments, and decision support workflows", ["personal-admin", "paperwork", "planning"]),
    ContinuousExpansionTarget("community_moderation", "Community Moderation", "AI community moderation, escalation, trust-and-safety, and policy workflows", ["moderation", "community", "trust-safety"]),
    ContinuousExpansionTarget("emergency_response", "Emergency Response", "AI emergency response, continuity, triage, logistics, and recovery workflows", ["emergency", "continuity", "triage"]),
)


def _dedupe_expansion_targets(
    *target_groups: Tuple[ContinuousExpansionTarget, ...],
) -> Tuple[ContinuousExpansionTarget, ...]:
    seen: set[str] = set()
    deduped: List[ContinuousExpansionTarget] = []
    for group in target_groups:
        for target in group:
            if target.slug in seen:
                continue
            seen.add(target.slug)
            deduped.append(target)
    return tuple(deduped)


CONTINUOUS_EXPANSION_TARGETS: Tuple[ContinuousExpansionTarget, ...] = _dedupe_expansion_targets(
    BASE_CONTINUOUS_EXPANSION_TARGETS,
    EXPANSIVE_AI_USE_CASE_TARGETS,
)


CONTINUOUS_EXPANSION_CONTEXTS: Tuple[ContinuousExpansionDimension, ...] = (
    ContinuousExpansionDimension("", "", "", []),
    ContinuousExpansionDimension("agentic_planning", "Agentic Planning", "agentic planning", ["agentic", "planning"]),
    ContinuousExpansionDimension("tool_use", "Tool Use", "AI tool use", ["tools", "tool-use"]),
    ContinuousExpansionDimension("retrieval_grounding", "Retrieval Grounding", "retrieval grounding", ["retrieval", "grounding"]),
    ContinuousExpansionDimension("memory_management", "Memory Management", "memory management", ["memory"]),
    ContinuousExpansionDimension("evaluation_feedback", "Evaluation Feedback", "evaluation feedback", ["evaluation", "feedback"]),
    ContinuousExpansionDimension("safety_controls", "Safety Controls", "safety controls", ["safety", "controls"]),
    ContinuousExpansionDimension("workflow_orchestration", "Workflow Orchestration", "workflow orchestration", ["workflow", "orchestration"]),
    ContinuousExpansionDimension("release_ops", "Release Ops", "release operations", ["release", "operations"]),
    ContinuousExpansionDimension("customer_interaction", "Customer Interaction", "customer-facing interaction", ["customer", "interaction"]),
    ContinuousExpansionDimension("data_pipeline", "Data Pipeline", "data pipeline work", ["data", "pipeline"]),
    ContinuousExpansionDimension("documentation", "Documentation", "documentation and knowledge capture", ["docs", "documentation"]),
    ContinuousExpansionDimension("compliance_review", "Compliance Review", "compliance review", ["compliance"]),
    ContinuousExpansionDimension("personalization", "Personalization", "personalization", ["personalization"]),
    ContinuousExpansionDimension("multimodal_inputs", "Multimodal Inputs", "multimodal inputs", ["multimodal"]),
    ContinuousExpansionDimension("plugin_ops", "Capability Operations", "capability operations", ["capabilities", "operations"]),
    ContinuousExpansionDimension("task_decomposition", "Task Decomposition", "task decomposition", ["tasks", "decomposition"]),
    ContinuousExpansionDimension("prompt_ops", "Prompt Operations", "prompt operations", ["prompting", "operations"]),
    ContinuousExpansionDimension("knowledge_graph", "Knowledge Graph", "knowledge graph work", ["knowledge", "graph"]),
    ContinuousExpansionDimension("live_monitoring", "Live Monitoring", "live monitoring", ["monitoring", "live"]),
    ContinuousExpansionDimension("decision_support", "Decision Support", "decision support", ["decision-support"]),
    ContinuousExpansionDimension("domain_triage", "Domain Triage", "domain triage", ["triage"]),
    ContinuousExpansionDimension("quality_control", "Quality Control", "quality control", ["quality"]),
    ContinuousExpansionDimension("case_management", "Case Management", "case management", ["cases"]),
    ContinuousExpansionDimension("resource_planning", "Resource Planning", "resource planning", ["resources", "planning"]),
    ContinuousExpansionDimension("policy_mapping", "Policy Mapping", "policy mapping", ["policy", "mapping"]),
    ContinuousExpansionDimension("field_operations", "Field Operations", "field operations", ["field-ops"]),
    ContinuousExpansionDimension("stakeholder_updates", "Stakeholder Updates", "stakeholder updates", ["stakeholders", "updates"]),
    ContinuousExpansionDimension("knowledge_extraction", "Knowledge Extraction", "knowledge extraction", ["knowledge", "extraction"]),
    ContinuousExpansionDimension("accessibility_review", "Accessibility Review", "accessibility review", ["accessibility"]),
)


CONTINUOUS_EXPANSION_MODES: Tuple[ContinuousExpansionDimension, ...] = (
    ContinuousExpansionDimension("", "", "", []),
    ContinuousExpansionDimension("detect", "Detection", "detecting signals", ["detect"]),
    ContinuousExpansionDimension("score", "Scoring", "scoring decisions", ["scoring"]),
    ContinuousExpansionDimension("plan", "Planning", "planning next actions", ["planning"]),
    ContinuousExpansionDimension("compose", "Composition", "composing capability outputs", ["composition"]),
    ContinuousExpansionDimension("verify", "Verification", "verifying outcomes", ["verification"]),
    ContinuousExpansionDimension("route", "Routing", "routing work", ["routing"]),
    ContinuousExpansionDimension("summarize", "Summarization", "summarizing evidence", ["summary"]),
    ContinuousExpansionDimension("refactor", "Refactoring", "refactoring workflows", ["refactor"]),
    ContinuousExpansionDimension("simulate", "Simulation", "simulating outcomes", ["simulation"]),
    ContinuousExpansionDimension("recover", "Recovery", "recovering from failures", ["recovery"]),
    ContinuousExpansionDimension("optimize", "Optimization", "optimizing decisions", ["optimization"]),
    ContinuousExpansionDimension("classify", "Classification", "classifying inputs", ["classification"]),
    ContinuousExpansionDimension("prioritize", "Prioritization", "prioritizing work", ["prioritization"]),
    ContinuousExpansionDimension("extract", "Extraction", "extracting structured signals", ["extraction"]),
    ContinuousExpansionDimension("compare", "Comparison", "comparing options", ["comparison"]),
    ContinuousExpansionDimension("forecast", "Forecasting", "forecasting likely outcomes", ["forecasting"]),
    ContinuousExpansionDimension("recommend", "Recommendation", "recommending next moves", ["recommendation"]),
    ContinuousExpansionDimension("audit", "Audit", "auditing readiness", ["audit"]),
    ContinuousExpansionDimension("normalize", "Normalization", "normalizing messy inputs", ["normalization"]),
    ContinuousExpansionDimension("map", "Mapping", "mapping relationships", ["mapping"]),
)


CONTINUOUS_EXPANSION_SURFACES: Tuple[ContinuousExpansionDimension, ...] = (
    ContinuousExpansionDimension("", "", "", []),
    ContinuousExpansionDimension("payloads", "Payload", "payload fields", ["payloads"]),
    ContinuousExpansionDimension("traces", "Trace", "tool traces and execution logs", ["traces"]),
    ContinuousExpansionDimension("conversations", "Conversation", "conversation history", ["conversation"]),
    ContinuousExpansionDimension("artifacts", "Artifact", "generated artifacts", ["artifacts"]),
    ContinuousExpansionDimension("scorecards", "Scorecard", "scorecards and rubrics", ["scorecards"]),
    ContinuousExpansionDimension("documents", "Document", "documents and files", ["documents"]),
    ContinuousExpansionDimension("forms", "Form", "forms and intake fields", ["forms"]),
    ContinuousExpansionDimension("tickets", "Ticket", "tickets and queues", ["tickets"]),
    ContinuousExpansionDimension("records", "Record", "records and case files", ["records"]),
    ContinuousExpansionDimension("policies", "Policy", "policies and controls", ["policies"]),
    ContinuousExpansionDimension("contracts", "Contract", "contracts and obligations", ["contracts"]),
    ContinuousExpansionDimension("telemetry", "Telemetry", "sensor readings and telemetry", ["telemetry"]),
)


CONTINUOUS_EXPANSION_FAMILIES: Tuple[ContinuousExpansionFamily, ...] = (
    ContinuousExpansionFamily(
        "prompt_contract_designer",
        "Prompt Contract Designer",
        "ai_prompting",
        "Design prompt contracts for {target_domain} with explicit inputs, outputs, constraints, and checks.",
        "enrichment",
        "{target_domain} prompt contracts and structured instruction design",
        ["prompting", "contracts", "schemas"],
        [
            "Turn loose {target_name} requests into strict prompt contracts.",
            "Name required inputs, outputs, constraints, and validation checks.",
            "Flag contract gaps before the prompt is sent to a model.",
        ],
    ),
    ContinuousExpansionFamily(
        "prompt_clarity_auditor",
        "Prompt Clarity Auditor",
        "ai_prompting",
        "Audit prompts for {target_domain} and identify ambiguity, weak wording, and missing execution detail.",
        "enrichment",
        "{target_domain} prompt clarity and ambiguity reduction",
        ["prompting", "clarity", "audit"],
        [
            "Find vague wording in {target_name} prompts.",
            "Recommend sharper language without changing the user's intent.",
            "Separate blocking ambiguity from polish improvements.",
        ],
    ),
    ContinuousExpansionFamily(
        "evidence_gap_detector",
        "Evidence Gap Detector",
        "ai_retrieval",
        "Detect missing evidence that blocks trustworthy answers in {target_domain}.",
        "research_synthesizer",
        "{target_domain} evidence gaps and retrieval readiness",
        ["retrieval", "evidence", "grounding"],
        [
            "List unsupported claims in {target_name} work.",
            "Rank evidence gaps by risk and retrieval priority.",
            "Suggest focused retrieval questions for each missing source.",
        ],
    ),
    ContinuousExpansionFamily(
        "source_quality_ranker",
        "Source Quality Ranker",
        "ai_retrieval",
        "Rank provided sources for {target_domain} by trust, relevance, freshness, and answer usefulness.",
        "scoring",
        "{target_domain} source quality and grounded answer preparation",
        ["sources", "trust", "grounding"],
        [
            "Score source notes before synthesis.",
            "Flag stale, weak, or low-relevance evidence.",
            "Recommend which sources should anchor the final output.",
        ],
    ),
    ContinuousExpansionFamily(
        "context_noise_filter",
        "Context Noise Filter",
        "ai_memory",
        "Filter noisy or redundant context before model calls for {target_domain}.",
        "data_insight",
        "{target_domain} context filtering and token-budget control",
        ["context", "tokens", "noise"],
        [
            "Classify context as keep, compress, or drop.",
            "Detect redundant notes that waste context budget.",
            "Preserve constraints and decisions while reducing noise.",
        ],
    ),
    ContinuousExpansionFamily(
        "memory_update_recommender",
        "Memory Update Recommender",
        "ai_memory",
        "Recommend durable memory updates from {target_domain} sessions without saving transient chatter.",
        "research_synthesizer",
        "{target_domain} durable memory and preference extraction",
        ["memory", "facts", "preferences"],
        [
            "Extract durable decisions and preferences.",
            "Separate temporary conversation from reusable memory.",
            "Recommend add, update, merge, or ignore actions.",
        ],
    ),
    ContinuousExpansionFamily(
        "agent_handoff_checker",
        "Agent Handoff Checker",
        "ai_agents",
        "Check {target_domain} agent handoffs for missing context, ownership overlap, and unsafe next steps.",
        "system_automation",
        "{target_domain} agent handoff quality and coordination",
        ["agents", "handoff", "coordination"],
        [
            "Validate handoff packets before another agent starts.",
            "Detect duplicated ownership and missing changed-file context.",
            "Recommend handoff fixes and integration checkpoints.",
        ],
    ),
    ContinuousExpansionFamily(
        "parallelization_planner",
        "Parallelization Planner",
        "ai_agents",
        "Identify safe parallel work packets for {target_domain} without duplicating or blocking work.",
        "system_automation",
        "{target_domain} parallel AI workflow planning",
        ["agents", "parallel", "planning"],
        [
            "Split work into blocking and parallelizable paths.",
            "Detect dependency conflicts before delegation.",
            "Create bounded sidecar tasks with merge checkpoints.",
        ],
    ),
    ContinuousExpansionFamily(
        "tool_safety_reviewer",
        "Tool Safety Reviewer",
        "ai_safety",
        "Review proposed tool use for {target_domain} for side effects, permissions, and rollback needs.",
        "scoring",
        "{target_domain} AI tool safety and approval control",
        ["tools", "safety", "permissions"],
        [
            "Score tool calls by mutation, exposure, and reversibility risk.",
            "Flag actions that need approval or extra verification.",
            "Recommend safer tool-use boundaries.",
        ],
    ),
    ContinuousExpansionFamily(
        "tool_argument_checker",
        "Tool Argument Checker",
        "ai_safety",
        "Inspect tool arguments for {target_domain} for unsafe scope, missing bounds, or injected instructions.",
        "scoring",
        "{target_domain} tool argument safety and sanitization",
        ["tools", "arguments", "safety"],
        [
            "Detect broad paths, destructive flags, and untrusted text.",
            "Recommend bounded arguments before execution.",
            "Separate safe read-only calls from risky mutations.",
        ],
    ),
    ContinuousExpansionFamily(
        "output_completeness_grader",
        "Output Completeness Grader",
        "ai_evaluation",
        "Grade {target_domain} AI outputs for completeness against task requirements and acceptance criteria.",
        "scoring",
        "{target_domain} output completeness and acceptance scoring",
        ["evaluation", "completeness", "quality"],
        [
            "Identify missing sections or unmet requirements.",
            "Score completeness using task-specific signals.",
            "Recommend edits that close blocking gaps.",
        ],
    ),
    ContinuousExpansionFamily(
        "response_action_planner",
        "Response Action Planner",
        "ai_evaluation",
        "Convert {target_domain} AI responses into concrete next actions with owners, checks, and risks.",
        "data_insight",
        "{target_domain} response actionability and next-step planning",
        ["evaluation", "actions", "planning"],
        [
            "Find vague advice that needs executable next steps.",
            "Create action items with checks and risk notes.",
            "Score whether the response is ready to act on.",
        ],
    ),
    ContinuousExpansionFamily(
        "assumption_risk_mapper",
        "Assumption Risk Mapper",
        "ai_evaluation",
        "Map assumptions in {target_domain} work and score which ones need evidence or user confirmation.",
        "research_synthesizer",
        "{target_domain} assumption tracking and readiness scoring",
        ["assumptions", "risk", "readiness"],
        [
            "Extract explicit and implicit assumptions.",
            "Rank assumptions by risk and reversibility.",
            "Recommend evidence or clarification for risky assumptions.",
        ],
    ),
    ContinuousExpansionFamily(
        "verification_checklist_builder",
        "Verification Checklist Builder",
        "ai_evaluation",
        "Build verification checklists for {target_domain} AI artifacts before release or handoff.",
        "system_automation",
        "{target_domain} verification planning and acceptance checks",
        ["verification", "tests", "checklists"],
        [
            "Turn acceptance criteria into concrete checks.",
            "Separate automated checks from human review.",
            "Record evidence needed before publish or handoff.",
        ],
    ),
    ContinuousExpansionFamily(
        "rollback_guard_builder",
        "Rollback Guard Builder",
        "ai_safety",
        "Check rollback readiness for {target_domain} AI changes before they are applied or published.",
        "scoring",
        "{target_domain} rollback safety and recovery planning",
        ["rollback", "safety", "release"],
        [
            "Detect missing rollback and backup details.",
            "Score blast radius and recovery readiness.",
            "Recommend proceed, hold, or add safeguards.",
        ],
    ),
    ContinuousExpansionFamily(
        "anomaly_watch_builder",
        "Anomaly Watch Builder",
        "ai_agents",
        "Build anomaly watch rules for live {target_domain} AI runs from logs, traces, and repeated actions.",
        "monitoring",
        "{target_domain} live-run monitoring and anomaly detection",
        ["monitoring", "anomalies", "autonomous"],
        [
            "Detect loops, repeated failures, and unusual output bursts.",
            "Score stalled or unsafe run states.",
            "Recommend continue, pause, repair, or escalate.",
        ],
    ),
    ContinuousExpansionFamily(
        "capability_overlap_checker",
        "Capability Overlap Checker",
        "ai_plugin_factory",
        "Check whether proposed {target_domain} capabilities overlap existing modules or deserve a new canonical slot.",
        "scoring",
        "{target_domain} capability uniqueness and roadmap hygiene",
        ["capabilities", "duplicates", "factory"],
        [
            "Compare proposed capability behavior against existing modules.",
            "Recommend merge, reject, or generate-new decisions.",
            "Explain uniqueness using capability boundaries.",
        ],
    ),
    ContinuousExpansionFamily(
        "release_evidence_summarizer",
        "Release Evidence Summarizer",
        "ai_plugin_factory",
        "Summarize validation and release evidence for {target_domain} AI capability artifacts.",
        "data_insight",
        "{target_domain} release evidence and publishing readiness",
        ["release", "evidence", "factory"],
        [
            "Summarize what passed and what remains risky.",
            "Package validation evidence for GitHub visibility.",
            "Recommend publish, hold, or repair.",
        ],
    ),
    ContinuousExpansionFamily(
        "trace_failure_router",
        "Trace Failure Router",
        "ai_agents",
        "Route {target_domain} trace failures to the most likely repair path.",
        "data_insight",
        "{target_domain} trace failure classification and repair routing",
        ["traces", "failures", "debugging"],
        [
            "Classify failures by prompt, context, tool, retrieval, or validation cause.",
            "Recommend the smallest retry strategy.",
            "Preserve useful progress from failed runs.",
        ],
    ),
    ContinuousExpansionFamily(
        "retrieval_query_planner",
        "Retrieval Query Planner",
        "ai_retrieval",
        "Plan focused retrieval queries for {target_domain} when evidence is missing or stale.",
        "research_synthesizer",
        "{target_domain} retrieval query planning and grounding",
        ["retrieval", "queries", "grounding"],
        [
            "Generate exact and broad discovery queries.",
            "Recommend filters, source types, and freshness needs.",
            "Separate blocking retrieval from optional enrichment.",
        ],
    ),
    ContinuousExpansionFamily(
        "citation_priority_scorer",
        "Citation Priority Scorer",
        "ai_evaluation",
        "Score which {target_domain} claims most urgently need citations or uncertainty language.",
        "scoring",
        "{target_domain} citation priority and factual-risk scoring",
        ["citations", "claims", "risk"],
        [
            "Rank claims by citation need.",
            "Flag high-stakes factual statements.",
            "Recommend safer wording for unsupported claims.",
        ],
    ),
    ContinuousExpansionFamily(
        "model_fit_triage",
        "Model Fit Triage",
        "ai_agents",
        "Triage which model tier or workflow style fits {target_domain} tasks based on risk and complexity.",
        "scoring",
        "{target_domain} model selection and capability fit",
        ["models", "routing", "triage"],
        [
            "Score whether a task needs fast, cheap, reasoning-heavy, or tool-using flow.",
            "Flag tasks that need stronger verification.",
            "Recommend the lowest sufficient capability tier.",
        ],
    ),
    ContinuousExpansionFamily(
        "instruction_hierarchy_checker",
        "Instruction Hierarchy Checker",
        "ai_safety",
        "Check {target_domain} instructions for hierarchy conflicts, unsafe overrides, and impossible constraints.",
        "scoring",
        "{target_domain} instruction hierarchy and conflict safety",
        ["instructions", "hierarchy", "safety"],
        [
            "Find conflicts between instruction layers.",
            "Flag unsafe or impossible requirements.",
            "Recommend a clarified instruction set.",
        ],
    ),
    ContinuousExpansionFamily(
        "data_contract_validator",
        "Data Contract Validator",
        "ai_evaluation",
        "Validate expected input and output contracts for {target_domain} AI capabilities.",
        "enrichment",
        "{target_domain} data contract validation and schema readiness",
        ["schema", "contracts", "validation"],
        [
            "Extract expected payload and result fields.",
            "Flag schema ambiguity before implementation.",
            "Recommend validation checks for downstream consumers.",
        ],
    ),
)


# The first live continuous-expansion waves were published with verbose slugs
# such as ai_content_strategy_agentic_planning_capability_overlap_checker.  Keep
# recognizing those legacy slugs for lookup/cursor continuity, but generate all
# new continuous capabilities with short numbered names whose distinctness lives
# in the use-case scenario and manifest metadata.
CONTINUOUS_SHORT_SLUG_START_INDEX = len(AI_CAPABILITY_ROADMAP) + 1


def numbered_capability_slug(base_slug: str, index: int) -> str:
    """Return the installable slug cadence for a deterministic capability slot."""
    return f"{str(base_slug or '').strip('_')}_{max(int(index), 1):06d}"


@dataclass(frozen=True)
class CategoryProfile:
    name: str
    weight: int
    default_tags: List[str]
    goal: str
    capability_type: str
    intended_domain: str


CATEGORY_PROFILES: Dict[str, CategoryProfile] = {
    "system_automation": CategoryProfile(
        name="system_automation",
        weight=14,
        default_tags=["system", "automation", "files", "processes"],
        goal="Automate a useful system-level task based on the payload.",
        capability_type="system_automation",
        intended_domain="system automation and OS-level utilities",
    ),
    "data": CategoryProfile(
        name="data",
        weight=14,
        default_tags=["data", "analysis", "transformation"],
        goal="Analyze or transform structured/unstructured data into useful insights or cleaned output.",
        capability_type="data_insight",
        intended_domain="general data processing and analytics",
    ),
    "monitoring": CategoryProfile(
        name="monitoring",
        weight=10,
        default_tags=["monitoring", "alerts", "logs"],
        goal="Monitor inputs (logs, events, metrics) for anomalies or conditions and emit structured alerts.",
        capability_type="monitoring",
        intended_domain="monitoring and observability",
    ),
    "security": CategoryProfile(
        name="security",
        weight=8,
        default_tags=["security", "compliance", "checks"],
        goal="Inspect payload data/configurations for security or compliance issues and report findings.",
        capability_type="security",
        intended_domain="security and compliance checks",
    ),
    "research": CategoryProfile(
        name="research",
        weight=10,
        default_tags=["research", "summarization", "synthesis"],
        goal="Synthesize and summarize research-style content from the payload.",
        capability_type="research_synthesizer",
        intended_domain="research and knowledge work",
    ),
    "ecommerce": CategoryProfile(
        name="ecommerce",
        weight=8,
        default_tags=["ecommerce", "catalog", "inventory"],
        goal="Support ecommerce operations such as catalog cleanup, inventory checks, or bundle suggestions.",
        capability_type="business_ops",
        intended_domain="ecommerce and business operations",
    ),
    "devops": CategoryProfile(
        name="devops",
        weight=8,
        default_tags=["devops", "infra", "deploy"],
        goal="Help with DevOps-style tasks using structured payload data (configs, deployment plans, logs).",
        capability_type="system_automation",
        intended_domain="DevOps and infrastructure support",
    ),
    "smarthome": CategoryProfile(
        name="smarthome",
        weight=6,
        default_tags=["iot", "smart_home", "automation"],
        goal="Interpret or plan smart-home/IoT behaviors based on sensor or event payloads.",
        capability_type="ai_orchestration",
        intended_domain="smart home and IoT orchestration",
    ),
    "utility": CategoryProfile(
        name="utility",
        weight=10,
        default_tags=["utility", "helper", "tool"],
        goal="Provide a generally useful helper or utility behavior driven by the payload.",
        capability_type="data_insight",
        intended_domain="general-purpose utilities",
    ),
    "business_analytics": CategoryProfile(
        name="business_analytics",
        weight=6,
        default_tags=["business", "analytics"],
        goal="Analyze business-related data (operations, finance, or sales) to produce structured insights.",
        capability_type="data_insight",
        intended_domain="business analytics and operations",
    ),
}


# ---------------------------------------------------------------------
# Category -> naming fragments and example use cases
# ---------------------------------------------------------------------

_NAME_FRAGMENTS: Dict[str, Dict[str, List[str]]] = {
    "system_automation": {
        "prefixes": ["System", "Ops", "Runtime", "Process"],
        "themes": ["Flow", "Task", "Job", "Routine", "Orchestration", "Lifecycle"],
        "roles": ["Orchestrator", "Automator", "Controller", "Coordinator", "Optimizer"],
    },
    "data": {
        "prefixes": ["Data", "Insight", "Pattern", "Signal"],
        "themes": ["Cascade", "Lens", "Profile", "Stream", "Atlas", "Matrix", "Pulse"],
        "roles": ["Analyzer", "Explorer", "Engine", "Scanner", "Summarizer"],
    },
    "monitoring": {
        "prefixes": ["Service", "Telemetry", "Ops", "Signal"],
        "themes": ["Watch", "Pulse", "Horizon", "Sentinel", "Radar"],
        "roles": ["Monitor", "Observer", "Guard", "Scanner"],
    },
    "security": {
        "prefixes": ["Security", "Risk", "Shield", "Guard"],
        "themes": ["Surface", "Matrix", "Insight", "Posture", "Policy"],
        "roles": ["Analyzer", "Inspector", "Auditor", "Advisor"],
    },
    "research": {
        "prefixes": ["Research", "Knowledge", "Context", "Brief"],
        "themes": ["Digest", "Synthesis", "Outline", "Summary"],
        "roles": ["Engine", "Assistant", "Compiler", "Synthesizer"],
    },
    "ecommerce": {
        "prefixes": ["Commerce", "Catalog", "Product", "Storefront"],
        "themes": ["Flow", "Funnel", "Inventory", "Bundle", "Merch"],
        "roles": ["Optimizer", "Analyzer", "Planner", "Advisor"],
    },
    "devops": {
        "prefixes": ["Deploy", "Release", "Infra", "Pipeline"],
        "themes": ["Flow", "Stream", "Health", "Change"],
        "roles": ["Advisor", "Planner", "Monitor", "Assistant"],
    },
    "smarthome": {
        "prefixes": ["Smart Home", "IoT", "Home"],
        "themes": ["Routine", "Scene", "Trigger", "Pattern"],
        "roles": ["Orchestrator", "Planner", "Coordinator", "Assistant"],
    },
    "utility": {
        "prefixes": ["Utility", "Helper", "Toolkit", "Workbench"],
        "themes": ["Assist", "Bridge", "Adapter", "Companion"],
        "roles": ["Tool", "Assistant", "Manager", "Helper"],
    },
    "business_analytics": {
        "prefixes": ["Business", "Ops", "Revenue", "Performance"],
        "themes": ["Trend", "Segment", "Cohort", "Drift", "Signal"],
        "roles": ["Analyzer", "Dashboard", "Insight Engine", "Advisor"],
    },
}

_USE_CASE_TEMPLATES: Dict[str, List[str]] = {
    "system_automation": [
        "Automate repetitive filesystem maintenance tasks based on a structured payload.",
        "Interpret job definitions and propose a safe execution order.",
        "Classify incoming tasks into immediate actions vs scheduled jobs.",
    ],
    "data": [
        "Summarize the structure and key statistics of a tabular dataset.",
        "Detect outliers and anomalies in numeric metrics.",
        "Cluster records into simple segments for downstream targeting.",
    ],
    "monitoring": [
        "Detect spikes or drops in service metrics for alerting.",
        "Summarize log batches into a small set of incident candidates.",
        "Highlight noisy vs meaningful signals in monitoring payloads.",
    ],
    "security": [
        "Flag misconfigurations or risky settings in a security policy payload.",
        "Summarize audit logs into a prioritized list of potential issues.",
        "Score entities by approximate risk level for human review.",
    ],
    "research": [
        "Summarize long-form research notes into action-ready briefs.",
        "Extract key arguments and counter-arguments from research text.",
        "Cluster related topics across multiple research documents.",
    ],
    "ecommerce": [
        "Analyze product catalog exports for missing or low-quality attributes.",
        "Suggest bundles or cross-sell opportunities based on product metadata.",
        "Flag inventory issues such as low stock or inconsistent pricing.",
    ],
    "devops": [
        "Summarize deployment plans and highlight risky changes.",
        "Analyze infra logs for recurring failure patterns.",
        "Suggest rollout or rollback actions based on recent events.",
    ],
    "smarthome": [
        "Propose automation routines based on recent IoT events.",
        "Suggest quiet hours or energy-saving scenes from sensor history.",
        "Detect unusual device behavior for notification.",
    ],
    "utility": [
        "Normalize mixed-format payloads into a clean, consistent structure.",
        "Extract key fields from heterogeneous JSON blobs.",
        "Provide general-purpose summarization of arbitrary payloads.",
    ],
    "business_analytics": [
        "Highlight key trends in operational or financial metrics.",
        "Identify segments that show unusual performance patterns.",
        "Surface leading indicators for churn or expansion.",
    ],
}


# ---------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------

def _continuous_expansion_parts(index: int) -> tuple[
    ContinuousExpansionFamily,
    ContinuousExpansionTarget,
    ContinuousExpansionDimension,
    ContinuousExpansionDimension,
    ContinuousExpansionDimension,
    int,
]:
    offset = max(int(index), len(AI_CAPABILITY_ROADMAP) + 1) - len(AI_CAPABILITY_ROADMAP) - 1
    family_count = len(CONTINUOUS_EXPANSION_FAMILIES)
    target_count = len(CONTINUOUS_EXPANSION_TARGETS)
    context_count = len(CONTINUOUS_EXPANSION_CONTEXTS)
    mode_count = len(CONTINUOUS_EXPANSION_MODES)
    surface_count = len(CONTINUOUS_EXPANSION_SURFACES)

    family = CONTINUOUS_EXPANSION_FAMILIES[offset % family_count]
    target_index = (offset // family_count) % target_count
    variant_index = offset // (family_count * target_count)
    context = CONTINUOUS_EXPANSION_CONTEXTS[variant_index % context_count]
    mode = CONTINUOUS_EXPANSION_MODES[(variant_index // context_count) % mode_count]
    surface = CONTINUOUS_EXPANSION_SURFACES[(variant_index // (context_count * mode_count)) % surface_count]
    cycle = variant_index // (context_count * mode_count * surface_count)
    target = CONTINUOUS_EXPANSION_TARGETS[target_index]
    return family, target, context, mode, surface, cycle


def legacy_continuous_expansion_slug(index: int) -> str | None:
    if int(index) <= len(AI_CAPABILITY_ROADMAP):
        return None
    family, target, context, mode, surface, cycle = _continuous_expansion_parts(index)
    slug_parts = [
        "ai",
        target.slug,
        context.slug,
        mode.slug,
        surface.slug,
        family.slug,
    ]
    slug = "_".join(part for part in slug_parts if part)
    if cycle:
        slug = f"{slug}_cycle_{cycle + 1}"
    return slug


def _continuous_expansion_blueprint(index: int) -> AICapabilityBlueprint:
    """
    Build a deterministic canonical capability after the curated roadmap ends.

    These are not stage upgrades or numbered clone batches. They are fresh,
    named capabilities generated from a controlled matrix of AI workflow
    targets, use contexts, operating modes, surfaces, and capability families.
    """
    family, target, context, mode, surface, cycle = _continuous_expansion_parts(index)

    if int(index) < CONTINUOUS_SHORT_SLUG_START_INDEX:
        slug = legacy_continuous_expansion_slug(index) or f"ai_{family.slug}_{int(index):06d}"
        name_parts = [
            "AI",
            target.name,
            context.name,
            mode.name,
            surface.name,
            family.name,
        ]
        name = " ".join(part for part in name_parts if part)
        if cycle:
            name = f"{name} Cycle {cycle + 1}"
    else:
        slug = f"ai_{family.slug}_{int(index):06d}"
        name = f"AI {family.name}"

    domain_parts = [
        target.domain_phrase,
        context.domain_phrase,
        mode.domain_phrase,
        surface.domain_phrase,
    ]
    target_domain = " for ".join(part for part in domain_parts if part)
    target_name = " ".join(
        part for part in [target.name, context.name, mode.name, surface.name] if part
    )
    scenario_label = target_name or target.name
    tags = list(
        dict.fromkeys(
            [
                *target.tags,
                *context.tags,
                *mode.tags,
                *surface.tags,
                *family.tags,
                "continuous_backlog",
                "use_case_seeded",
            ]
        )
    )

    return AICapabilityBlueprint(
        slug=slug,
        name=name,
        category=family.category,
        goal=family.goal_template.format(
            target_name=target_name,
            target_domain=target_domain,
        ),
        capability_type=family.capability_type,
        intended_domain=family.intended_domain_template.format(
            target_name=target_name,
            target_domain=target_domain,
        ),
        tags=tags,
        use_cases=[
            f"Apply this capability to the distinct use case: {scenario_label}.",
            *[
                item.format(target_name=target_name, target_domain=target_domain)
                for item in family.use_case_templates
            ],
        ],
    )


def _roadmap_position(index: int) -> Tuple[AICapabilityBlueprint, int, int]:
    """
    Map any positive index onto the deterministic AI roadmap.

    Returns:
      - blueprint: base capability family
      - roadmap_number: deterministic global capability index
      - generation_round: 1 for canonical capability generation
    """
    safe_index = max(int(index), 1)
    roadmap_size = len(AI_CAPABILITY_ROADMAP)
    if safe_index <= roadmap_size:
        return AI_CAPABILITY_ROADMAP[safe_index - 1], safe_index, 1
    return _continuous_expansion_blueprint(safe_index), safe_index, 1


def _capability_semantics(blueprint: AICapabilityBlueprint) -> Dict[str, object]:
    if blueprint.slug != "ai_prompt_refinement_engine":
        return {}
    return {
        "capability_output_semantics": {
            "details.identified_vagueness": "list of vague phrases extracted from payload['prompt'] or payload['task']",
            "details.missing_constraints": "list of category/suggestion objects for missing audience, format, length, tone, constraints, acceptance criteria, and verification",
            "details.rewrites": "list of concrete prompt rewrites, each with a label and rewrite text",
            "details.refined_prompt": "the primary rewritten prompt, not generic advice",
            "recommended_actions[*].rewrite": "recommended actions should include actual rewritten prompt text when useful",
        },
        "worked_examples": [
            {
                "input": {
                    "task": "Write a blog post about cats.",
                    "objective": "Increase newsletter signups.",
                    "prompt": "Make it good.",
                },
                "expected": {
                    "identified_vagueness": ["Make it good"],
                    "missing_constraints": ["audience", "length", "tone", "format", "acceptance_criteria"],
                    "rewrite_should_include": [
                        "newsletter signups",
                        "target audience",
                        "blog post length or section format",
                        "call to action",
                        "success criteria",
                    ],
                },
            },
            {
                "input": {
                    "task": "Ask an AI coding agent to add tests before changing production code.",
                    "objective": "Prevent regressions.",
                    "prompt": "Make this better and don't break stuff.",
                },
                "expected": {
                    "identified_vagueness": ["Make this better", "don't break stuff"],
                    "missing_constraints": ["test scope", "files/modules", "acceptance criteria", "rollback or verification"],
                    "rewrite_should_include": [
                        "write or update tests first",
                        "name files or modules",
                        "run verification",
                        "avoid unrelated refactors",
                    ],
                },
            },
        ],
        "semantic_depth_contract": {
            "must_fail_if": [
                "Output only says to rewrite the prompt without producing a rewrite.",
                "details does not include identified_vagueness and missing_constraints.",
                "Two different prompts produce the same refined_prompt.",
            ],
            "must_pass_if": [
                "The plugin extracts vague phrases from the input prompt.",
                "The plugin names missing constraints by category.",
                "The plugin returns concrete rewritten prompt variants.",
            ],
        },
    }


def _build_huge_ai_spec(
    blueprint: AICapabilityBlueprint,
    *,
    roadmap_number: int,
    generation_round: int,
    global_index: int,
) -> PluginSpec:
    """
    Build a rich AI-focused PluginSpec with enough structure for Station B to
    create a useful AI capability instead of a generic/random utility.
    """
    display_number = f"{global_index:06d}"
    canonical_name = blueprint.name
    name = f"{canonical_name} {display_number}"
    if global_index <= len(AI_CAPABILITY_ROADMAP):
        slug = numbered_capability_slug(blueprint.slug, global_index)
    else:
        slug = blueprint.slug
    goal = blueprint.goal

    progress_focus = {
        1: "baseline capability",
        2: "edge cases and robustness",
        3: "operator visibility and progress reporting",
        4: "user delight, guided coaching, and clearer scorecards",
    }.get(generation_round, f"advanced refinement pass {generation_round}")

    use_cases = list(blueprint.use_cases)
    use_cases.extend(
        [
            f"Show a compact progress state for this AI capability during {progress_focus}.",
            "Return user-facing guidance that is useful, concise, and safe to act on.",
            "Avoid duplicating existing AI capability behavior; identify what is unique about this capability.",
        ]
    )

    example_use_cases = [
        f"A user asks Francis to improve an AI workflow related to {blueprint.intended_domain}.",
        "A long-running autonomous run needs a checkpoint summary and the next best action.",
        "An operator wants a scorecard that separates hard failures from polish improvements.",
        "A beginner wants the result explained in plain language without losing technical accuracy.",
        "A power user wants structured JSON they can pipe into another agent or dashboard.",
    ]

    problem_statement = (
        f"Francis needs a focused AI capability for {blueprint.intended_domain}. The generated module must "
        "turn messy user notes, model outputs, traces, or workflow state into structured, "
        "actionable AI assistance. It should improve autonomous progress by making the next "
        "step obvious, reducing duplicated work, and exposing risks before they become failures. "
        "The capability must stay deterministic, avoid hidden external side effects, and make its "
        "reasoning inspectable through concise details and scores."
    )

    primary_inputs = (
        "A payload dict that may contain task, objective, prompt, conversation, artifacts, "
        "candidate_outputs, traces, rubric, constraints, user_level, current_plan, completed_steps, "
        "blocked_steps, source_notes, and optional customer_config."
    )

    primary_outputs = (
        "A normalized result dict with summary, primary_insights, recommended_actions, scores, "
        "details, progress_state, user_experience, fun_mode, and machine-readable diagnostics."
    )

    constraints = (
        "Do not execute tools, browse, mutate files, call external APIs, or claim facts not present "
        "in the payload. Prefer deterministic analysis. If data is missing, say what is missing and "
        "return a useful fallback. Keep recommendations concrete. Avoid creating a capability that "
        "duplicates another AI roadmap capability."
    )

    io_contract = (
        "Input: payload is a dict. Important optional keys include 'task', 'objective', 'prompt', "
        "'conversation', 'messages', 'candidate_outputs', 'trace', 'rubric', 'constraints', "
        "'progress', 'current_plan', 'completed_steps', 'blocked_steps', 'user_level', and "
        "'customer_config'. Output: return a dict containing summary: str, primary_insights: list, "
        "recommended_actions: list, scores: dict with confidence and usefulness, details: dict, "
        "progress_state: dict with current_stage/next_step/blockers, user_experience: dict with "
        "plain_language_takeaway and interaction_suggestions, and fun_mode: dict with optional "
        "challenge_label, score_badge, and celebratory_microcopy. Fun fields must never replace "
        "the serious recommendation."
    )

    example_payload = {
        "task": f"Improve an AI workflow using {canonical_name}.",
        "objective": blueprint.goal,
        "user_level": "mixed",
        "current_plan": [
            "Collect relevant context.",
            "Ask the model for an initial result.",
            "Evaluate and refine the result.",
        ],
        "completed_steps": ["Collected rough notes and candidate output."],
        "blocked_steps": ["Need a sharper next action and risk check."],
        "candidate_outputs": [
            {
                "id": "draft_a",
                "summary": "A first-pass model response or workflow plan.",
                "known_issues": ["May be vague", "May duplicate prior work"],
            }
        ],
        "constraints": [
            "No external side effects.",
            "Return structured JSON-compatible output.",
            "Prioritize AI functionality and autonomous progress.",
        ],
        "customer_config": {
            "tone": "clear, direct, helpful",
            "include_fun_mode": True,
            "max_recommended_actions": 5,
        },
    }

    tags = list(dict.fromkeys([*blueprint.tags, "autonomous_factory", "ai_progress"]))

    extra = {
        "factory_focus": "ai_functionality_and_progress",
        "roadmap_number": roadmap_number,
        "roadmap_size": len(AI_CAPABILITY_ROADMAP),
        "display_number": display_number,
        "canonical_name": canonical_name,
        "canonical_slug": blueprint.slug,
        "generation_round": generation_round,
        "progress_focus": progress_focus,
        "global_index": global_index,
        "installable_naming_policy": "all installable AI capabilities use a six-digit numbered slug suffix",
        "duplicate_policy": {
            "slug_must_be_unique": True,
            "capability_must_be_distinct": True,
            "plugin_must_serve_ai_workflow": True,
            "allow_expansive_ai_use_case_domains": True,
            "do_not_generate_non_ai_utilities": True,
            "do_not_generate_random_domains": False,
            "avoid_equivalent_prompt_memory_eval_retrieval_agent_safety_plugins": True,
        },
        "expected_result_shape": {
            "summary": "string",
            "primary_insights": "list[str|dict]",
            "recommended_actions": "list[str|dict]",
            "scores": {
                "confidence": "float 0..1",
                "usefulness": "float 0..1",
                "novelty": "float 0..1",
                "risk": "float 0..1",
            },
            "details": "dict",
            "progress_state": {
                "current_stage": "string",
                "next_step": "string",
                "blockers": "list",
                "done_signals": "list",
            },
            "user_experience": {
                "plain_language_takeaway": "string",
                "beginner_tip": "string",
                "power_user_tip": "string",
                "interaction_suggestions": "list",
            },
            "fun_mode": {
                "challenge_label": "string",
                "score_badge": "string",
                "microcopy": "string",
                "optional_next_challenge": "string",
            },
        },
        "fun_user_features": [
            "Score badge for the result, such as Clear Path, Needs Proof, or Ready to Run.",
            "A small challenge label that makes the next step feel approachable.",
            "Beginner and power-user tips in the same output.",
            "Progress language that helps the user see what changed since the previous step.",
            "Friendly microcopy that stays secondary to the serious recommendation.",
        ],
        "station_b_guidance": [
            "Build real analysis logic around the provided payload keys.",
            "Keep behavior deterministic and transparent.",
            "Prefer structured scorecards, checklists, and next-action summaries.",
            "Include fun user-facing affordances only as optional metadata.",
            "Never invent external facts or pretend to run tools.",
        ],
    }
    if global_index > len(AI_CAPABILITY_ROADMAP):
        extra["continuous_expansion"] = True
        extra["continuous_expansion_source"] = (
            "short_numbered_use_case_matrix"
            if global_index >= CONTINUOUS_SHORT_SLUG_START_INDEX
            else "target_family_matrix"
        )
        extra["use_case_seed"] = global_index
        extra["naming_policy"] = (
            "short numbered slug; use-case scenario carries target/context variation"
            if global_index >= CONTINUOUS_SHORT_SLUG_START_INDEX
            else "legacy descriptive slug retained for already-published compatibility"
        )
    extra.update(_capability_semantics(blueprint))

    return PluginSpec(
        name=name,
        slug=slug,
        goal=goal,
        category=blueprint.category,
        tags=tags,
        version="0.1.0",
        capability_type=blueprint.capability_type,
        intended_domain=blueprint.intended_domain,
        use_cases=use_cases,
        primary_use_case=use_cases[0] if use_cases else None,
        example_payload=example_payload,
        problem_statement=problem_statement,
        primary_inputs=primary_inputs,
        primary_outputs=primary_outputs,
        constraints=constraints,
        example_use_cases=example_use_cases,
        io_contract=io_contract,
        extra=extra,
    )


# ---------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------

def build_next_spec(index: int) -> Tuple[PluginSpec, str, str]:
    """
    Build the next AI-focused PluginSpec plus capability_type and intended_domain.

    Returns: (spec, capability_type, intended_domain)
    """
    blueprint, roadmap_number, generation_round = _roadmap_position(index)
    spec = _build_huge_ai_spec(
        blueprint,
        roadmap_number=roadmap_number,
        generation_round=generation_round,
        global_index=max(int(index), 1),
    )
    return spec, spec.capability_type or "data_insight", spec.intended_domain or "AI functionality"
