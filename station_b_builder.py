from __future__ import annotations

import asyncio
from textwrap import dedent
from typing import Optional
from pathlib import Path

from ollama_client import OllamaClient, OllamaError
from plugin_spec import PluginSpec
from plugin_template import (
    render_plugin_source,
    replace_logic_block,
)
from registry import plugin_path_for_spec


class StationBBuilderError(Exception):
    """Raised when Station B cannot successfully build or repair a plugin."""


def _logic_prompt_for_new(spec: PluginSpec) -> str:
    """
    Prompt for generating the BODY of a helper function named `_core_logic`.

    The model is NOT responsible for the final envelope or return from invoke().
    It ONLY writes the inside of:

        def _core_logic(payload: Dict[str, Any], context: SkillContext, user_id: str) -> Dict[str, Any]:
            <YOUR CODE HERE>

    We will wrap it.
    """
    return dedent(
        f"""
        You are STATION B2, an internal automated subsystem inside the Francis
        Autonomous Plugin Factory.

        You are NOT a chatbot.
        You do NOT talk to users.
        You ONLY output Python code that will become the BODY of a function:

            def _core_logic(payload: Dict[str, Any], context: SkillContext, user_id: str) -> Dict[str, Any]:
                <YOUR CODE HERE>

        CONTEXT:
        - The outer plugin structure (imports, SkillContext, async invoke())
          already exists and MUST NOT be modified by you.
        - You are ONLY responsible for the body of _core_logic.
        - You have access to the arguments:
            - payload: Dict[str, Any]
            - context: SkillContext
            - user_id: str
        - The plugin's purpose and domain:

            NAME      : {spec.name}
            GOAL      : {spec.goal}
            CATEGORY  : {spec.category}
            TAGS      : {", ".join(spec.tags)}

        QUALITY RULES (VERY IMPORTANT):
        - You MUST use the incoming `payload` as your primary input.
        - You MUST NOT overwrite `payload` with hard-coded example data.
          - If you need example data, put it in a separate variable
            (e.g. demo_entities, demo_graph, sample_logs).
        - If required data is missing from payload, you MAY fall back to
          a small demo example, but:
          - Only do this when payload lacks the necessary keys.
          - Clearly indicate this in the returned dict, e.g.
            {{"mode": "demo", ...}} vs {{"mode": "analysis", ...}}.
        - Design a structured result guided by the GOAL and TAGS.
          - For graph-like plugins, prefer keys like:
            - "nodes": [...], "edges": [...], "summary": {{...}}
          - For analysis plugins, use keys like:
            - "metrics", "summary", "details", "items", etc.
        - Think of the output as something another tool or UI will consume,
          not just a raw echo of payload.

        HARD RULES (MANDATORY):
        - Output ONLY valid Python code (statements).
        - NO backticks, NO markdown, NO explanation, NO comments, NO prose.
        - Do NOT define async functions.
        - Do NOT define or redefine 'invoke'.
        - Do NOT modify imports or SkillContext.
        - Do NOT reassign `payload`; treat it as read-only input.
          - You MAY create new variables derived from it
            (e.g. entities = payload.get("entities", [])).
        - The `context` argument is a SkillContext OBJECT, NOT a dict:
          - Do NOT use `"key" in context` or `context["key"]`.
          - If you need an optional helper, use:
            helper = getattr(context, "helper_name", None)
            if callable(helper):
                helper(...)
        - You MUST NOT call any function or use any class that:
          - you did not define in this logic body, AND
          - is not a Python built-in, AND
          - is not from the standard library modules that are already imported.
          Assume no third-party libraries are available.
        - You MUST NOT reference names like graph_disambiguator, client,
          session, or other helpers unless you define them yourself here.
        - Your code MUST end with a single 'return ...' statement
          returning a JSON-serializable dict with your analysis or result.
        - Handle payload like {{"ping": true}} without crashing.
          - In that case, you may return a lightweight health/status dict.
        - Prefer pure, deterministic logic (no network calls).

        REQUIRED OUTPUT:
        - ONLY the Python statements that make up the body of _core_logic.
        - No surrounding 'def', no indentation at the first column, no wrappers.
        """
    ).strip()


def _logic_prompt_for_fix(
    spec: PluginSpec,
    existing_logic_body: str,
    error_report: str,
) -> str:
    """
    Prompt for repairing the BODY of the _core_logic function, using Station C
    error feedback.
    """
    return dedent(
        f"""
        You are STATION B2, an internal automated subsystem in the Francis
        Autonomous Plugin Factory.

        You are NOT a chatbot.
        You do NOT talk to users.
        You ONLY output Python code that will become the BODY of a function:

            def _core_logic(payload: Dict[str, Any], context: SkillContext, user_id: str) -> Dict[str, Any]:
                <YOUR CODE HERE>

        Your job:
        - FIX the existing logic so that validation passes.
        - IMPROVE QUALITY where possible while staying aligned with the plugin's goal.
        - Use the validator error report as guidance.

        PLUGIN SPEC (JSON):
        {spec.to_json(indent=2)}

        CURRENT _core_logic BODY:
        {existing_logic_body}

        VALIDATOR ERRORS:
        {error_report}

        QUALITY RULES (VERY IMPORTANT):
        - You MUST use the incoming `payload` as your primary input.
        - You MUST NOT overwrite `payload` with hard-coded example data.
          - If you need example data, put it in a separate variable
            (e.g. demo_entities, demo_graph, sample_logs).
        - If required data is missing from payload, you MAY fall back to
          a small demo example, but:
          - Only do this when payload lacks the necessary keys.
          - Clearly indicate this in the returned dict, e.g.
            {{"mode": "demo", ...}} vs {{"mode": "analysis", ...}}.
        - Design a structured result guided by the GOAL and TAGS:
            NAME      : {spec.name}
            GOAL      : {spec.goal}
            CATEGORY  : {spec.category}
            TAGS      : {", ".join(spec.tags)}
        - Think about the next consumer: output should be clean, structured,
          and easy to visualize or inspect.

        HARD RULES (MANDATORY):
        - Output ONLY valid Python code (statements).
        - NO backticks, NO markdown, NO explanation, NO comments, NO prose.
        - DO NOT change the function signature.
        - DO NOT define or redefine 'invoke'.
        - DO NOT modify imports or SkillContext.
        - DO NOT reassign `payload`.
        - The `context` argument is a SkillContext OBJECT, NOT a dict:
          - Do NOT use `"key" in context` or `context["key"]`.
          - If you need an optional helper, use:
            helper = getattr(context, "helper_name", None)
            if callable(helper):
                helper(...)
        - You MUST NOT call any function or use any class that:
          - you did not define in this logic body, AND
          - is not a Python built-in, AND
          - is not from the standard library modules that are already imported.
          Assume no third-party libraries are available.
        - You MUST NOT reference names like graph_disambiguator, client,
          session, or other helpers unless you define them yourself here.
        - Your code MUST end with a single 'return ...' statement
          returning a JSON-serializable dict with your analysis or result.
        - You MUST handle payload like {{"ping": true}} without crashing.

        REQUIRED OUTPUT:
        - ONLY the corrected Python statements for the BODY of _core_logic.
        """
    ).strip()


def _sanitize_ollama_code(raw: str) -> str:
    """
    Clean up raw text from Ollama:
    - Strip leading/trailing whitespace.
    - Remove markdown code fences like ``` or ```python.
    """
    text = raw.strip()
    if not text:
        return ""

    lines = text.splitlines()
    cleaned: list[str] = []
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("```"):
            # Drop any kind of markdown fence.
            continue
        cleaned.append(line)

    return "\n".join(cleaned).strip()


def _wrap_core_logic_body(body: str) -> str:
    """
    Given the BODY of _core_logic (unindented, no def line), construct the
    full logic block to be injected between LOGIC START/END markers.

    The generated block will:
    - define _core_logic(...)
    - call it safely
    - populate 'result'
    - return 'result'
    """
    if not body.strip():
        body = "return {'status': 'ok', 'echo': payload}"

    body_lines = body.splitlines()
    indented_body = "\n".join(
        ("    " + line if line.strip() else "") for line in body_lines
    )

    logic_block = f"""def _core_logic(payload: Dict[str, Any], context: SkillContext, user_id: str) -> Dict[str, Any]:
{indented_body}

try:
    core_output = _core_logic(payload, context, user_id)
    core_error = None
    core_status = "succeeded"
except Exception as e:
    core_output = {{
        "error": str(e),
        "exception_type": type(e).__name__,
        "payload_keys": list(payload.keys()) if isinstance(payload, dict) else None,
    }}
    core_error = str(e)
    core_status = "failed"

# Populate the result envelope expected by Station C.
result["status"] = core_status
result["output"] = core_output
result["error"] = core_error

meta = result.get("meta") or {{}}
meta.setdefault("mode", "generated_logic")
meta.setdefault("user_id", user_id)
result["meta"] = meta

return result
"""
    return logic_block


async def _apply_logic_with_ollama(
    spec: PluginSpec,
    source: str,
    client: OllamaClient,
    *,
    error_feedback: Optional[str] = None,
) -> str:
    """
    Ask Ollama to generate or fix the BODY of _core_logic, then wrap it into a
    full logic block that guarantees:

    - invoke() ALWAYS returns a dict.
    - invoke() ALWAYS returns via `return result`.
    - Station C ALWAYS sees a dict it can normalize.
    """
    if error_feedback:
        prompt = _logic_prompt_for_fix(
            spec,
            "<existing body unavailable>",
            error_feedback,
        )
    else:
        prompt = _logic_prompt_for_new(spec)

    try:
        raw_body = await client.generate_text(prompt)
    except OllamaError as e:
        raise StationBBuilderError(f"Ollama error: {e}") from e

    body = _sanitize_ollama_code(raw_body)
    logic_block = _wrap_core_logic_body(body)

    try:
        updated = replace_logic_block(source, logic_block)
    except Exception as e:
        raise StationBBuilderError(f"Failed to inject new logic block: {e}") from e

    return updated


async def build_or_repair_plugin(
    spec: PluginSpec,
    *,
    client: Optional[OllamaClient] = None,
    existing_source: Optional[str] = None,
    error_feedback: Optional[str] = None,
) -> str:
    """
    Main Station B entrypoint.

    - If existing_source is None:
        Use the template to render a new plugin, then populate the logic block.
    - If existing_source is provided:
        Repair the logic block based on error_feedback.
    """
    if client is None:
        client = OllamaClient()

    if existing_source is None:
        source = render_plugin_source(spec)
    else:
        source = existing_source

    updated_source = await _apply_logic_with_ollama(
        spec=spec,
        source=source,
        client=client,
        error_feedback=error_feedback,
    )

    return updated_source


def write_plugin_to_disk(spec: PluginSpec, source: str) -> str:
    """
    Write the plugin source to its canonical location based on category/slug.
    """
    path = plugin_path_for_spec(spec)
    path.write_text(source, encoding="utf-8")
    return str(path)


async def build_plugin_file_for_spec(spec: PluginSpec, attempt: int) -> Path:
    """
    Station B hook used by the factory runner.

    - Builds (or repairs) the plugin for this spec.
    - Writes it to disk in the canonical location.
    - Returns the Path to the .py file.

    `attempt` is accepted so we can later:
    - adjust prompts for retries
    - incorporate error feedback from Station C.
    """
    client = OllamaClient()
    # For now we always build fresh; later we can pass existing_source/error_feedback
    source = await build_or_repair_plugin(spec, client=client)

    path_str = write_plugin_to_disk(spec, source)
    return Path(path_str)


async def station_b_demo() -> None:
    """
    Simple demo: build a 'Demo Plugin' using Station B and write it to disk.
    """
    spec = PluginSpec.new(
        name="Demo Plugin",
        goal="Demonstrate Station B",
        category="utility",
        tags=["demo"],
    )

    client = OllamaClient()
    print("Station B demo: building plugin...")

    src = await build_or_repair_plugin(spec, client=client)
    path = write_plugin_to_disk(spec, src)

    print("Plugin written to:", path)


if __name__ == "__main__":
    asyncio.run(station_b_demo())
