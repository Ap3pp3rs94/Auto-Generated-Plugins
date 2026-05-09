from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional

from .collector import iter_events


# These must match plugin_template.py
_LOGIC_START = "# === LOGIC START ==="
_LOGIC_END = "# === LOGIC END ==="

PROJECT_ROOT = Path(__file__).resolve().parents[1]
LEARNING_DIR = Path(__file__).resolve().parent
LOG_PATH = LEARNING_DIR / "plugins_log.jsonl"
TRAIN_DATA_PATH = LEARNING_DIR / "training_data.jsonl"


def _read_file(path: Path) -> Optional[str]:
    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError:
        return None
    except OSError:
        return None


def _extract_logic_block(source: str) -> Optional[str]:
    """
    Extract the _run_logic function between logic markers.
    Falls back to None if markers are missing or malformed.
    """
    s = source.find(_LOGIC_START)
    e = source.find(_LOGIC_END)
    if s == -1 or e == -1 or e <= s:
        return None

    segment = source[s + len(_LOGIC_START) : e]
    return segment.strip() or None


def _build_prompt_from_spec(
    spec_dict: Dict[str, Any],
    error_context: Optional[str] = None,
) -> str:
    """
    Build a training prompt that mirrors the real Station B instruction style.
    """
    name = spec_dict.get("name") or "<unknown>"
    goal = spec_dict.get("goal") or "<no goal>"
    category = spec_dict.get("category") or "<uncategorized>"
    tags = spec_dict.get("tags") or []

    tag_str = ", ".join(tags)

    prompt = [
        "You are Francis-Station-B (Logic Generator).",
        "You ONLY write the async function `_run_logic` for a Francis plugin.",
        "",
        "PluginSpec:",
        f"- name: {name}",
        f"- goal: {goal}",
        f"- category: {category}",
        f"- tags: {tag_str}",
        "",
        "Write exactly:",
        "async def _run_logic(ctx: SkillContext, payload: Dict[str, Any]) -> Dict[str, Any]:",
        "",
        "Rules:",
        "- MUST be async.",
        "- MUST NOT raise exceptions intentionally.",
        "- MUST return a JSON-serializable dict.",
        "- MUST accomplish the plugin's goal.",
        "- MUST NOT define anything outside this function.",
        "- MUST NOT include markdown fences.",
    ]

    if error_context:
        prompt.extend(
            [
                "",
                "The following validator feedback should be taken into account:",
                error_context,
            ]
        )

    return "\n".join(prompt)


def _build_spec_dict_from_event(ev: Any) -> Dict[str, Any]:
    """
    Convert PluginEvent-like object into a spec-like dict.
    """
    return {
        "name": ev.plugin_name,
        "goal": ev.goal,
        "category": ev.category,
        "tags": list(ev.tags),
        "version": ev.version,
        "slug": ev.plugin_slug,
    }


def build_training_records() -> List[Dict[str, Any]]:
    """
    Build a list of {input, output, meta} training records based on successful
    plugins from plugins_log.jsonl.
    """
    events = iter_events()
    records: List[Dict[str, Any]] = []

    for ev in events:
        # Only use successful, validator-passing plugins
        if ev.status != "success":
            continue
        if ev.validator_ok is False:
            continue
        if not ev.code_path:
            continue

        code_path = Path(ev.code_path)
        source = _read_file(code_path)
        if not source:
            continue

        logic = _extract_logic_block(source)
        if not logic:
            continue

        spec_dict = _build_spec_dict_from_event(ev)

        # Build error context (if any warnings or errors were recorded)
        error_context_parts: List[str] = []
        if ev.validator_errors:
            error_context_parts.append("Errors:\n" + "\n".join(f"- {e}" for e in ev.validator_errors))
        if ev.validator_warnings:
            error_context_parts.append("Warnings:\n" + "\n".join(f"- {w}" for w in ev.validator_warnings))

        error_context = "\n\n".join(error_context_parts) if error_context_parts else None

        prompt = _build_prompt_from_spec(spec_dict, error_context=error_context)

        record = {
            "input": prompt,
            "output": logic,
            "meta": {
                "plugin_name": ev.plugin_name,
                "plugin_slug": ev.plugin_slug,
                "category": ev.category,
                "tags": list(ev.tags),
                "version": ev.version,
                "code_path": ev.code_path,
            },
        }
        records.append(record)

    return records


def write_training_jsonl(path: Path = TRAIN_DATA_PATH) -> int:
    """
    Build and write training_data.jsonl.
    Returns the number of records written.
    """
    records = build_training_records()
    if not records:
        print("[dataset_builder] No usable records found in plugins_log.jsonl")
        return 0

    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open("w", encoding="utf-8") as f:
        for rec in records:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")

    print(
        f"[dataset_builder] Wrote {len(records)} training records to {path}"
    )
    return len(records)


if __name__ == "__main__":
    count = write_training_jsonl()
    print(f"[dataset_builder] Done. Total records: {count}")
