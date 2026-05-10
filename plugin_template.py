from __future__ import annotations

from typing import Any, Dict, List
try:
    from .plugin_spec import PluginSpec
except ImportError:  # pragma: no cover - direct script/local-folder import
    from plugin_spec import PluginSpec

_LOGIC_START = "# === LOGIC START ==="
_LOGIC_END = "# === LOGIC END ==="


def render_plugin_source(spec: PluginSpec, logic_block: str | None = None) -> str:
    """
    Render a complete Francis plugin Python file.

    If `logic_block` is provided, it replaces the default placeholder
    `_run_logic` function inside the logic markers.
    """

    header = (
        "# Auto-generated Francis plugin skill.\n"
        "# DO NOT EDIT THIS HEADER BY HAND.\n"
        f"# Title      : {spec.name}\n"
        f"# File       : {spec.slug}.py\n"
        f"# Description: {spec.goal}\n"
        f"# Goal       : {spec.goal}\n"
        f"# Category   : {spec.category}\n"
        f"# Tags       : {', '.join(spec.tags)}\n"
        f"# Version    : {spec.version}\n"
    )

    # NOTE: this is a normal triple-quoted string with .format(),
    # NOT an f-string, so all {} inside are safe.
    body = """
from __future__ import annotations
from typing import Any, Dict, Optional, List


PLUGIN_NAME = "{name}"
PLUGIN_SLUG = "{slug}"
PLUGIN_DESCRIPTION = "{goal}"
PLUGIN_CATEGORY = "{category}"
PLUGIN_TAGS = {tags}
PLUGIN_VERSION = "{version}"


class SkillContext:
    \"\"\"Context passed to the plugin's logic.\"\"\"
    def __init__(
        self,
        user_id: str,
        run_id: Optional[Any] = None,
        brain: Optional[Any] = None,
        logger: Optional[Any] = None,
        **extra: Any,
    ) -> None:
        self.user_id = user_id
        self.run_id = run_id
        self.brain = brain
        self.logger = logger
        self.extra = dict(extra or {})


def _safe_log_exception(ctx: SkillContext, msg: str, exc: BaseException) -> None:
    \"\"\"Safely logs an exception if a logger is available.\"\"\"
    lg = getattr(ctx, "logger", None)
    if lg is None:
        return
    try:
        if hasattr(lg, "exception"):
            lg.exception(msg)
        elif hasattr(lg, "error"):
            lg.error(f"{msg}: {exc!r}")
    except Exception:
        pass


{logic_start}
async def _run_logic(ctx: SkillContext, payload: Dict[str, Any]) -> Dict[str, Any]:
    return {{
        "ok": True,
        "note": "placeholder logic",
        "payload_echo": payload,
    }}
{logic_end}


async def invoke(user_id: str, payload: Dict[str, Any], **kwargs: Any) -> Dict[str, Any]:
    \"\"\"Entry point for all Francis plugins.\"\"\"
    if not isinstance(payload, dict):
        payload = {
            "_value": payload,
            "_payload_warnings": ["payload was not a dict; invoke wrapped it in _value"],
        }

    ctx = SkillContext(
        user_id=user_id,
        run_id=kwargs.get("run_id"),
        brain=kwargs.get("brain"),
        logger=kwargs.get("logger"),
        **kwargs,
    )

    meta = {{
        "plugin_name": PLUGIN_NAME,
        "plugin_slug": PLUGIN_SLUG,
        "plugin_category": PLUGIN_CATEGORY,
        "plugin_tags": PLUGIN_TAGS,
        "plugin_version": PLUGIN_VERSION,
        "factory": "francis",
    }}

    try:
        result = await _run_logic(ctx, payload)
        return {{
            "status": "succeeded",
            "output": {{
                "ok": True,
                "result": result,
            }},
            "error": None,
            "meta": meta,
        }}

    except Exception as exc:
        _safe_log_exception(ctx, "plugin exception", exc)
        return {{
            "status": "succeeded",
            "output": {{
                "ok": False,
                "reason": "exception in logic",
                "exception_name": type(exc).__name__,
                "exception_message": str(exc),
            }},
            "error": None,
            "meta": {{**meta, "internal_error": True}},
        }}
""".format(
        name=spec.name,
        slug=spec.slug,
        goal=spec.goal,
        category=spec.category,
        tags=list(spec.tags),
        version=spec.version,
        logic_start=_LOGIC_START,
        logic_end=_LOGIC_END,
    )

    if logic_block:
        return header + body.replace(
            f"{_LOGIC_START}\nasync def _run_logic(ctx: SkillContext, payload: Dict[str, Any]) -> Dict[str, Any]:",
            f"{_LOGIC_START}\n{logic_block.strip()}",
        )

    return header + body
