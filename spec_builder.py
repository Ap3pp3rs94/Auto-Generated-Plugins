from __future__ import annotations

"""
Spec builder for the Francis plugin factory.

This generates PluginSpecs for the autonomous AI capability roadmap.

Upgrades:
- Deterministic AI-focused plugin specs; no random domain/category rotation.
- Each spec includes a small set of concrete `use_cases`.
- capability_type and intended_domain are set on PluginSpec directly.

You can use this in place of Station A when you want autonomous progress
toward AI functionality rather than broad/random utility generation.
"""

from dataclasses import dataclass
from typing import Dict, List, Tuple

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
        goal="Map expected AI plugin input and output contracts from task descriptions and examples.",
        capability_type="enrichment",
        intended_domain="AI data contracts and schema planning",
        tags=["ai", "schema", "contracts", "plugins"],
        use_cases=[
            "Extract expected payload fields and result fields.",
            "Flag schema ambiguity before implementation.",
            "Recommend validation checks for plugin contracts.",
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
        name="AI Plugin Spec Architect",
        category="ai_plugin_factory",
        goal="Design precise, non-duplicate PluginSpecs for new AI plugins before generation starts.",
        capability_type="enrichment",
        intended_domain="AI plugin specification design and capability boundaries",
        tags=["ai", "plugins", "specs", "factory"],
        use_cases=[
            "Turn a loose plugin idea into a complete PluginSpec blueprint.",
            "Define capability boundaries so the plugin does not duplicate existing plugins.",
            "List required inputs, outputs, acceptance criteria, and quality signals before build.",
        ],
    ),
    AICapabilityBlueprint(
        slug="ai_plugin_logic_blueprint_designer",
        name="AI Plugin Logic Blueprint Designer",
        category="ai_plugin_factory",
        goal="Plan deterministic plugin core logic before code generation so the body performs the actual capability.",
        capability_type="system_automation",
        intended_domain="AI plugin deterministic logic planning and implementation design",
        tags=["ai", "plugins", "logic", "factory"],
        use_cases=[
            "Translate a PluginSpec into deterministic analysis steps.",
            "Define payload fields, scoring signals, and output constructors.",
            "Prevent generic template bodies by naming capability-specific algorithms.",
        ],
    ),
    AICapabilityBlueprint(
        slug="ai_plugin_quality_gate_designer",
        name="AI Plugin Quality Gate Designer",
        category="ai_plugin_factory",
        goal="Create semantic quality gates that reject shallow, duplicate, or off-capability generated plugins.",
        capability_type="scoring",
        intended_domain="AI plugin validation, semantic depth, and rejection policy",
        tags=["ai", "plugins", "quality", "validation"],
        use_cases=[
            "Define required detail keys and pass/fail rules for a plugin capability.",
            "Generate semantic probe payloads that force output differences.",
            "Explain why a plugin should be accepted, repaired, or rejected.",
        ],
    ),
    AICapabilityBlueprint(
        slug="ai_plugin_test_payload_generator",
        name="AI Plugin Test Payload Generator",
        category="ai_plugin_factory",
        goal="Generate focused test payloads that prove a plugin reacts to payload meaning rather than structure alone.",
        capability_type="data_insight",
        intended_domain="AI plugin test design and semantic probe generation",
        tags=["ai", "plugins", "tests", "semantic-depth"],
        use_cases=[
            "Create positive, edge, and adversarial payloads for a plugin.",
            "Define expected output differences across semantically different payloads.",
            "Produce regression watchlists for future plugin repairs.",
        ],
    ),
    AICapabilityBlueprint(
        slug="ai_plugin_duplicate_detector",
        name="AI Plugin Duplicate Detector",
        category="ai_plugin_factory",
        goal="Detect when a proposed plugin duplicates existing plugin behavior and recommend merge, reject, or redesign.",
        capability_type="scoring",
        intended_domain="AI plugin uniqueness, overlap analysis, and roadmap hygiene",
        tags=["ai", "plugins", "duplicates", "roadmap"],
        use_cases=[
            "Compare a proposed plugin against existing plugin names, goals, and output contracts.",
            "Create uniqueness fingerprints for plugin ideas.",
            "Recommend whether to merge, reject, or redesign overlapping capabilities.",
        ],
    ),
    AICapabilityBlueprint(
        slug="ai_plugin_repair_strategy_planner",
        name="AI Plugin Repair Strategy Planner",
        category="ai_plugin_factory",
        goal="Plan targeted repairs for weak generated plugins based on validation failures and semantic gaps.",
        capability_type="system_automation",
        intended_domain="AI plugin repair planning and capability-specific improvement",
        tags=["ai", "plugins", "repair", "quality"],
        use_cases=[
            "Turn quality-runner failures into a specific repair plan.",
            "Separate shallow output, missing keys, semantic similarity, and runtime errors.",
            "Define acceptance checks before a repaired plugin can replace the old one.",
        ],
    ),
    AICapabilityBlueprint(
        slug="ai_plugin_release_packager",
        name="AI Plugin Release Packager",
        category="ai_plugin_factory",
        goal="Package generated plugins for GitHub release with validation evidence, user-facing notes, and rollback guidance.",
        capability_type="data_insight",
        intended_domain="AI plugin release packaging, publishing, and operator visibility",
        tags=["ai", "plugins", "release", "github"],
        use_cases=[
            "Prepare commit-ready release notes for generated plugins.",
            "Summarize validation, semantic depth, and quality-runner evidence.",
            "Recommend publish, hold, or rollback actions for plugin releases.",
        ],
    ),
    AICapabilityBlueprint(
        slug="ai_plugin_factory_backlog_planner",
        name="AI Plugin Factory Backlog Planner",
        category="ai_plugin_factory",
        goal="Plan the next high-value AI plugin backlog so autonomous generation keeps improving itself intentionally.",
        capability_type="research_synthesizer",
        intended_domain="AI plugin factory roadmap planning and self-improvement backlog",
        tags=["ai", "plugins", "backlog", "factory"],
        use_cases=[
            "Prioritize future plugins by factory leverage, uniqueness, and user value.",
            "Define dependency order between spec, generation, validation, repair, and release plugins.",
            "Generate next-plugin candidates that avoid random or duplicate roadmap expansion.",
        ],
    ),
)


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

def _roadmap_position(index: int) -> Tuple[AICapabilityBlueprint, int, int]:
    """
    Map any positive index onto the deterministic AI roadmap.

    Returns:
      - blueprint: base capability family
      - roadmap_number: 1-based position within AI_CAPABILITY_ROADMAP
      - phase: 1-based pass through the roadmap
    """
    safe_index = max(int(index), 1)
    zero_index = safe_index - 1
    roadmap_size = len(AI_CAPABILITY_ROADMAP)
    roadmap_number = (zero_index % roadmap_size) + 1
    phase = (zero_index // roadmap_size) + 1
    return AI_CAPABILITY_ROADMAP[roadmap_number - 1], roadmap_number, phase


def _phase_name(base_name: str, phase: int) -> str:
    if phase <= 1:
        return base_name
    return f"{base_name} Phase {phase}"


def _phase_slug(base_slug: str, phase: int) -> str:
    if phase <= 1:
        return base_slug
    return f"{base_slug}_phase_{phase}"


def _phase_goal(blueprint: AICapabilityBlueprint, phase: int) -> str:
    if phase <= 1:
        return blueprint.goal
    return (
        f"Extend {blueprint.name} with phase {phase} behavior: preserve the original "
        "AI capability, add stronger edge-case handling, expose clearer user-facing "
        "progress signals, and produce more actionable next steps."
    )


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
    phase: int,
    global_index: int,
) -> PluginSpec:
    """
    Build a rich AI-focused PluginSpec with enough structure for Station B to
    create a useful plugin instead of a generic/random utility.
    """
    name = _phase_name(blueprint.name, phase)
    slug = _phase_slug(blueprint.slug, phase)
    goal = _phase_goal(blueprint, phase)

    phase_focus = {
        1: "baseline capability",
        2: "edge cases and robustness",
        3: "operator visibility and progress reporting",
        4: "user delight, guided coaching, and clearer scorecards",
    }.get(phase, f"advanced refinement pass {phase}")

    use_cases = list(blueprint.use_cases)
    use_cases.extend(
        [
            f"Show a compact progress state for this AI capability during {phase_focus}.",
            "Return user-facing guidance that is useful, concise, and safe to act on.",
            "Avoid duplicating existing AI plugin behavior; identify what is unique about this capability.",
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
        f"Francis needs a focused AI plugin for {blueprint.intended_domain}. The plugin must "
        "turn messy user notes, model outputs, traces, or workflow state into structured, "
        "actionable AI assistance. It should improve autonomous progress by making the next "
        "step obvious, reducing duplicated work, and exposing risks before they become failures. "
        "The plugin must stay deterministic, avoid hidden external side effects, and make its "
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
        "duplicates another AI roadmap plugin."
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
        "task": f"Improve an AI workflow using {name}.",
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

    tags = list(dict.fromkeys([*blueprint.tags, "autonomous_factory", "ai_progress", f"phase_{phase}"]))

    extra = {
        "factory_focus": "ai_functionality_and_progress",
        "roadmap_number": roadmap_number,
        "roadmap_size": len(AI_CAPABILITY_ROADMAP),
        "phase": phase,
        "phase_focus": phase_focus,
        "global_index": global_index,
        "duplicate_policy": {
            "slug_must_be_unique": True,
            "capability_must_be_distinct": True,
            "do_not_generate_random_domains": True,
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
    blueprint, roadmap_number, phase = _roadmap_position(index)
    spec = _build_huge_ai_spec(
        blueprint,
        roadmap_number=roadmap_number,
        phase=phase,
        global_index=max(int(index), 1),
    )
    return spec, spec.capability_type or "data_insight", spec.intended_domain or "AI functionality"
