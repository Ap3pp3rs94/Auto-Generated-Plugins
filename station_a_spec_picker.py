from __future__ import annotations

import asyncio
import re
from textwrap import dedent
from typing import Any, Dict, List

from ollama_client import OllamaClient, OllamaError
from plugin_spec import PluginSpec
from registry import has_duplicate_capability, entry_exists_for_slug


class StationASpecError(Exception):
    """Raised when Station A cannot produce a valid, unique PluginSpec."""


_ALLOWED_CATEGORIES = {"system_automation", "utility", "data", "integration"}


def _normalize_category(raw: Any) -> str:
    """
    Take whatever Ollama gave us for `category` and normalize it
    to a single allowed value if possible.

    Examples:
    - "system_automation | utility" → "system_automation"
    - "utility | data"              → "utility"
    - "Utility"                     → "utility"
    """
    if raw is None:
        return "utility"

    text = str(raw).strip().lower()

    # If it's already valid, keep it.
    if text in _ALLOWED_CATEGORIES:
        return text

    # Split on common separators like | , /
    parts = re.split(r"[|,/]", text)
    for part in parts:
        part = part.strip()
        if part in _ALLOWED_CATEGORIES:
            return part

    # Last resort: default to utility
    return "utility"


def _normalize_spec_dict(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Clean / normalize the raw JSON from Ollama into something
    PluginSpec.from_dict can safely consume.
    """
    normalized = dict(data)

    # Category: ensure a single allowed value
    normalized["category"] = _normalize_category(normalized.get("category"))

    # Tags: ensure list[str]
    tags = normalized.get("tags", [])
    if isinstance(tags, str):
        # e.g. "files, cleanup" → ["files", "cleanup"]
        tags = [t.strip() for t in tags.split(",") if t.strip()]
    elif isinstance(tags, list):
        tags = [str(t) for t in tags]
    else:
        tags = []
    normalized["tags"] = tags

    # Version default
    if "version" not in normalized or not normalized["version"]:
        normalized["version"] = "0.1.0"

    # Author default
    if "author" not in normalized or not normalized["author"]:
        normalized["author"] = "francis-factory"

    # requires_internet default
    normalized["requires_internet"] = bool(normalized.get("requires_internet", False))

    # os_target default
    if "os_target" not in normalized or not normalized["os_target"]:
        normalized["os_target"] = "any"

    # timeout_seconds default
    try:
        normalized["timeout_seconds"] = int(normalized.get("timeout_seconds", 30))
    except (TypeError, ValueError):
        normalized["timeout_seconds"] = 30

    # extra default
    extra = normalized.get("extra")
    if not isinstance(extra, dict):
        extra = {}
    normalized["extra"] = extra

    return normalized


def _spec_prompt(existing_slugs: List[str]) -> str:
    """
    Prompt Ollama to generate a new PluginSpec-like JSON object.
    """
    existing_slugs_str = ", ".join(existing_slugs) if existing_slugs else "[]"
    return dedent(
        f"""
        You are STATION A, an internal spec generator for the Francis
        Autonomous Plugin Factory.

        You are NOT a chatbot.
        You do NOT talk to humans.
        You ONLY output JSON.

        TASK:
        - Invent a NEW plugin idea that is useful for automation, utility,
          data processing, or integration.
        - The plugin must be meaningfully different from existing slugs:
          {existing_slugs_str}

        OUTPUT:
        - Respond ONLY with a single JSON object with these fields:

          {{
            "name": "Human-friendly name of the plugin",
            "slug": "kebab-case-unique-slug",
            "goal": "One-sentence description of what the plugin does",
            "category": "system_automation",
            "tags": ["list", "of", "short", "tags"],
            "version": "0.1.0",
            "author": "francis-factory",
            "requires_internet": false,
            "os_target": "any",
            "timeout_seconds": 30,
            "extra": {{}}
          }}

        HARD RULES:
        - The JSON MUST be valid and contain ALL the fields above.
        - "category" MUST be EXACTLY ONE of these strings:
          "system_automation", "utility", "data", "integration"
          (no pipes, no combinations, no extra words).
        - "slug" MUST be kebab-case using [a-z0-9-] only.
        - "tags" MUST be a JSON array of strings.
        - Do NOT include explanations or any text outside the JSON object.
        """
    ).strip()


async def generate_unique_spec(
    *,
    client: OllamaClient | None = None,
    max_attempts: int = 5,
) -> PluginSpec:
    """
    Station A: generate a new, unique PluginSpec.

    - Asks Ollama for a candidate JSON spec.
    - Normalizes the dict (category, tags, etc.).
    - Validates it into PluginSpec.
    - Ensures no duplicate capability / slug collisions.

    Raises StationASpecError if it cannot produce a valid spec.
    """
    if client is None:
        client = OllamaClient()

    existing_slugs: List[str] = []

    for attempt in range(1, max_attempts + 1):
        prompt = _spec_prompt(existing_slugs)
        try:
            raw_data: Dict[str, Any] = await client.generate_json(prompt)
        except OllamaError as e:
            raise StationASpecError(f"Ollama error while generating spec: {e}") from e

        normalized = _normalize_spec_dict(raw_data)

        try:
            spec = PluginSpec.from_dict(normalized)
        except Exception as e:
            if attempt == max_attempts:
                raise StationASpecError(
                    f"Failed to construct PluginSpec from Ollama JSON: {e}"
                ) from e
            # Try again with a fresh prompt on next loop
            continue

        # Check for duplicates
        if has_duplicate_capability(spec) or entry_exists_for_slug(spec.slug):
            existing_slugs.append(spec.slug)
            if attempt == max_attempts:
                raise StationASpecError(
                    "Generated spec appears to be a duplicate or near-duplicate."
                )
            continue

        return spec

    raise StationASpecError("Unable to generate a unique PluginSpec.")


async def station_a_demo() -> None:
    client = OllamaClient()
    print("Station A: Generating a new unique PluginSpec...")
    spec = await generate_unique_spec(client=client)
    print("\nGenerated PluginSpec:")
    print(spec.to_json(indent=2))


if __name__ == "__main__":
    asyncio.run(station_a_demo())
