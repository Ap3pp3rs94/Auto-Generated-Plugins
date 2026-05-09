from __future__ import annotations

import json
from typing import Any, Dict, List, Optional

try:
    import aiohttp
except ModuleNotFoundError:  # pragma: no cover - depends on local environment
    aiohttp = None  # type: ignore[assignment]


BASE_URL = "http://localhost:11434"
DEFAULT_MODEL = "llama3.1:8b"


# =====================================================================
# Low-level HTTP helpers
# =====================================================================


async def _ollama_chat(
    messages: List[Dict[str, str]],
    *,
    model: str = DEFAULT_MODEL,
    temperature: float = 0.2,
) -> str:
    """
    Prefer the /api/chat endpoint. If the server responds 404 (older Ollama),
    gracefully fall back to /api/generate by concatenating messages into a prompt.
    """
    if aiohttp is None:
        raise RuntimeError("aiohttp is required for Ollama HTTP calls. Install project requirements first.")

    async with aiohttp.ClientSession() as session:
        payload = {
            "model": model,
            "messages": messages,
            "stream": False,
            "options": {
                "temperature": temperature,
            },
        }

        # First attempt: /api/chat
        try:
            async with session.post(f"{BASE_URL}/api/chat", json=payload) as resp:
                if resp.status == 404:
                    # Fallback to /api/generate for older Ollama servers
                    return await _ollama_generate(
                        messages=messages,
                        model=model,
                        temperature=temperature,
                        session=session,
                    )

                resp.raise_for_status()
                data = await resp.json()
                # Newer Ollama chat responses: { "message": { "content": "..." }, ... }
                msg = data.get("message") or {}
                content = msg.get("content")
                if not isinstance(content, str):
                    raise RuntimeError(f"Unexpected /api/chat response structure: {data}")
                return content

        except aiohttp.ClientResponseError as e:
            # If we hit a 404 for some other reason, still try generate()
            if e.status == 404:
                return await _ollama_generate(
                    messages=messages,
                    model=model,
                    temperature=temperature,
                    session=session,
                )
            raise

        except aiohttp.ClientError as e:
            raise RuntimeError(f"Ollama /api/chat request failed: {e}") from e


async def _ollama_generate(
    messages: List[Dict[str, str]],
    *,
    model: str = DEFAULT_MODEL,
    temperature: float = 0.2,
    session: Optional[aiohttp.ClientSession] = None,
) -> str:
    """
    Fallback path for older Ollama versions that only expose /api/generate.

    We join system + user messages into a single prompt.
    """
    if aiohttp is None:
        raise RuntimeError("aiohttp is required for Ollama HTTP calls. Install project requirements first.")

    # Build a single prompt from messages
    parts: List[str] = []
    for msg in messages:
        role = msg.get("role", "user")
        content = msg.get("content", "")
        parts.append(f"[{role.upper()}]\n{content}\n")
    prompt = "\n".join(parts)

    close_session = False
    if session is None:
        session = aiohttp.ClientSession()
        close_session = True

    try:
        payload = {
            "model": model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": temperature,
            },
        }
        async with session.post(f"{BASE_URL}/api/generate", json=payload) as resp:
            resp.raise_for_status()
            data = await resp.json()
            # /api/generate returns: { "response": "..." , ... }
            content = data.get("response")
            if not isinstance(content, str):
                raise RuntimeError(f"Unexpected /api/generate response structure: {data}")
            return content
    except aiohttp.ClientError as e:
        raise RuntimeError(f"Ollama /api/generate request failed: {e}") from e
    finally:
        if close_session:
            await session.close()


def _strip_markdown_fences(text: str) -> str:
    """
    Remove ```...``` code fences if present. Keeps raw code / JSON inside.
    """
    text = text.strip()
    if text.startswith("```"):
        # Remove leading ```lang? and trailing ```
        lines = text.splitlines()
        if len(lines) >= 2 and lines[0].startswith("```"):
            # Drop first fence line and possible last fence line
            if lines[-1].strip().startswith("```"):
                lines = lines[1:-1]
            else:
                lines = lines[1:]
            return "\n".join(lines).strip()
    return text


# =====================================================================
# High-level helpers used by the factory
# =====================================================================


async def generate_json(
    *,
    system_prompt: str,
    user_prompt: str,
    model: str = DEFAULT_MODEL,
    temperature: float = 0.2,
) -> Dict[str, Any]:
    """
    Call Ollama and parse the response as JSON.

    Used by Station A for spec generation.
    """
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]

    text = await _ollama_chat(messages, model=model, temperature=temperature)
    text = _strip_markdown_fences(text)

    # Try strict JSON parse first
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        # Last resort: attempt to recover by trimming text around first/last braces
        start = text.find("{")
        end = text.rfind("}")
        if start != -1 and end != -1 and end > start:
            candidate = text[start : end + 1]
            try:
                return json.loads(candidate)
            except json.JSONDecodeError:
                pass
        raise RuntimeError(f"Failed to parse Ollama JSON response:\n{text}")


async def generate_code_block(
    system_prompt: str,
    user_prompt: str,
    *,
    model: str = DEFAULT_MODEL,
    temperature: float = 0.2,
) -> str:
    """
    Call Ollama and return a Python code block (used for _run_logic generation).

    Station B uses this and expects:
    - pure Python code
    - ideally, a single async def _run_logic(...)
    """
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]

    text = await _ollama_chat(messages, model=model, temperature=temperature)
    text = _strip_markdown_fences(text)
    return text.strip()
