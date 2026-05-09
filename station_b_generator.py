from __future__ import annotations

import re
from typing import Any, Dict, Optional

from pathlib import Path

try:
    from .plugin_spec import PluginSpec
    from .plugin_template import render_plugin_source
    from .ollama_client import generate_code_block
except ImportError:  # pragma: no cover - direct script/local-folder import
    from plugin_spec import PluginSpec
    from plugin_template import render_plugin_source
    from ollama_client import generate_code_block

_LOGIC_START = "# === LOGIC START ==="
_LOGIC_END = "# === LOGIC END ==="


# ======================================================================
# Station B – Generate plugin logic
# ======================================================================

class StationBError(Exception):
    """Raised when Station B (logic generator) fails."""


async def _extract_logic_block(raw_code: str) -> str:
    """
    Ensure the model returns ONLY Python logic (inside the logic block).
    Removes Markdown backticks and trims whitespace.
    """
    # Strip code fences ```python ... ```
    code = raw_code.strip()

    fence_pattern = r"```(?:python)?(.*?)```"
    match = re.search(fence_pattern, code, flags=re.DOTALL | re.IGNORECASE)
    if match:
        code = match.group(1).strip()

    return code


def _inject_logic(template: str, logic: str) -> str:
    """
    Insert the generated logic into the template between the defined markers.
    Uses regex to ensure clean replacement even across linebreak variations.
    """
    if _LOGIC_START not in template or _LOGIC_END not in template:
        raise StationBError("Template missing logic region markers.")

    pattern = (
        rf"{re.escape(_LOGIC_START)}.*?{re.escape(_LOGIC_END)}"
    )

    replacement = f"{_LOGIC_START}\n{logic}\n{_LOGIC_END}"

    new_source, count = re.subn(pattern, replacement, template, flags=re.DOTALL)
    if count == 0:
        raise StationBError("Failed to inject logic block into template.")

    return new_source


# ======================================================================
# Prompt builders
# ======================================================================

def _build_logic_prompt(spec: PluginSpec) -> str:
    """
    Create the instructions for Ollama -> produce pure Python logic
    placed inside the plugin's logic block.
    """
    return f"""
You are Station B of the Francis Plugin Factory.

Your job:
- Generate correct, executable, Python logic for a plugin.
- The plugin must satisfy:
    Name: {spec.name}
    Goal: {spec.goal}
    Category: {spec.category}
    Tags: {', '.join(spec.tags)}

Rules:
- Output ONLY valid Python code.
- DO NOT include imports; the plugin header handles those.
- DO NOT include comments, Markdown, or explanations.
- Logic must be deterministic, safe, and fully self-contained inside the logic block.
"""


# ======================================================================
# Station B – Generator entrypoint
# ======================================================================

async def generate_plugin_logic(
    spec: PluginSpec,
    *,
    temperature: float = 0.25,
    model: str = "llama3",
) -> str:
    """
    Generate pure Python logic for the plugin.

    Returns the final full plugin Python source code as a string.
    """
    # Render base template
    template = render_plugin_source(spec)

    # Produce logic block from LLM
    prompt = _build_logic_prompt(spec)
    raw_logic = await generate_code_block(
        system_prompt="You generate only valid Python code for a Francis plugin.",
        user_prompt=prompt,
        temperature=temperature,
        model=model,
    )

    logic = await _extract_logic_block(raw_logic)

    if not logic.strip():
        raise StationBError("LLM returned empty logic block.")

    # Inject logic block into template
    full_source = _inject_logic(template, logic)
    return full_source


# ======================================================================
# Save output
# ======================================================================

def write_plugin_file(path: Path, source: str) -> None:
    """
    Write the final plugin source to disk.
    Directory is created if missing.
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(source, encoding="utf-8")


# ======================================================================
# Orchestrator convenience API
# ======================================================================

async def station_b_generate(
    spec: PluginSpec,
    *,
    temperature: float = 0.25,
    model: str = "llama3",
) -> str:
    """
    Station B frontend used by factory orchestrator.
    Returns the full plugin source text.
    """
    try:
        return await generate_plugin_logic(
            spec,
            temperature=temperature,
            model=model,
        )
    except Exception as e:
        raise StationBError(f"Station B failed: {e}") from e
