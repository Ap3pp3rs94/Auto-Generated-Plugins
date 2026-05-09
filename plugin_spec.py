from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from typing import Any, Dict, List, TypedDict


# ---------------------------------------------------------------------------
# Constants / helpers
# ---------------------------------------------------------------------------

_VALID_CATEGORIES = {
    "system_automation",
    "utility",
    "data",
    "integration",
    "ai_prompting",
    "ai_agents",
    "ai_memory",
    "ai_evaluation",
    "ai_retrieval",
    "ai_safety",
}


def _slugify(name: str) -> str:
    """
    Convert an arbitrary name into a safe slug:

    - lowercase
    - replace non-alphanumeric with '-'
    - collapse repeated '-'
    - strip leading/trailing '-'
    """
    slug = name.strip().lower()
    slug = re.sub(r"[^a-z0-9]+", "-", slug)
    slug = re.sub(r"-{2,}", "-", slug)
    slug = slug.strip("-")
    return slug or "plugin"


class PluginSpecDict(TypedDict, total=False):
    """
    TypedDict for serialized PluginSpec objects.
    """
    name: str
    slug: str
    goal: str
    category: str
    tags: List[str]
    version: str
    author: str
    requires_internet: bool
    os_target: str
    timeout_seconds: int
    extra: Dict[str, Any]


# ---------------------------------------------------------------------------
# Core model
# ---------------------------------------------------------------------------

@dataclass
class PluginSpec:
    """
    Single source of truth for plugin metadata.

    This object is used by:
    - Station A (idea + spec generator)
    - Station B (template + logic builder)
    - Station C (validator + registry)
    """

    name: str
    slug: str
    goal: str
    category: str
    tags: List[str]
    version: str = "0.1.0"
    capability_type: str | None = None
    intended_domain: str | None = None
    author: str = "francis-factory"
    owner_id: str | None = None
    requires_internet: bool = False
    os_target: str = "any"
    timeout_seconds: int = 30
    use_cases: List[str] = field(default_factory=list)
    primary_use_case: str | None = None
    example_payload: Any | None = None
    problem_statement: str | None = None
    primary_inputs: str | None = None
    primary_outputs: str | None = None
    constraints: str | None = None
    example_use_cases: List[str] = field(default_factory=list)
    io_contract: str | None = None
    extra: Dict[str, Any] = field(default_factory=dict)

    # ---------- Construction helpers ----------

    @classmethod
    def new(
        cls,
        name: str,
        goal: str,
        category: str,
        tags: List[str],
        *,
        slug: str | None = None,
        version: str = "0.1.0",
        capability_type: str | None = None,
        intended_domain: str | None = None,
        author: str = "francis-factory",
        owner_id: str | None = None,
        requires_internet: bool = False,
        os_target: str = "any",
        timeout_seconds: int = 30,
        use_cases: List[str] | None = None,
        primary_use_case: str | None = None,
        example_payload: Any | None = None,
        problem_statement: str | None = None,
        primary_inputs: str | None = None,
        primary_outputs: str | None = None,
        constraints: str | None = None,
        example_use_cases: List[str] | None = None,
        io_contract: str | None = None,
        extra: Dict[str, Any] | None = None,
    ) -> "PluginSpec":
        """
        Convenience constructor that:
        - auto-slugifies the name if no slug is provided
        - normalizes category/tags
        - validates the resulting spec
        """
        if slug is None:
            slug = _slugify(name)

        if extra is None:
            extra = {}

        # Normalize category and tags early so validation sees final values.
        norm_category = category.strip().lower()
        norm_tags: List[str] = []
        for t in tags:
            if not isinstance(t, str):
                continue
            cleaned = t.strip()
            if cleaned:
                norm_tags.append(cleaned)

        spec = cls(
            name=name.strip(),
            slug=slug,
            goal=goal.strip(),
            category=norm_category,
            tags=norm_tags,
            version=version.strip() if isinstance(version, str) else "0.1.0",
            capability_type=capability_type.strip() if isinstance(capability_type, str) else None,
            intended_domain=intended_domain.strip() if isinstance(intended_domain, str) else None,
            author=author.strip() if isinstance(author, str) else "francis-factory",
            owner_id=owner_id.strip() if isinstance(owner_id, str) else None,
            requires_internet=bool(requires_internet),
            os_target=os_target.strip() if isinstance(os_target, str) else "any",
            timeout_seconds=int(timeout_seconds),
            use_cases=[str(item).strip() for item in (use_cases or []) if str(item).strip()],
            primary_use_case=primary_use_case.strip() if isinstance(primary_use_case, str) else None,
            example_payload=example_payload,
            problem_statement=problem_statement.strip() if isinstance(problem_statement, str) else None,
            primary_inputs=primary_inputs.strip() if isinstance(primary_inputs, str) else None,
            primary_outputs=primary_outputs.strip() if isinstance(primary_outputs, str) else None,
            constraints=constraints.strip() if isinstance(constraints, str) else None,
            example_use_cases=[
                str(item).strip() for item in (example_use_cases or []) if str(item).strip()
            ],
            io_contract=io_contract.strip() if isinstance(io_contract, str) else None,
            extra=dict(extra),
        )
        spec.validate()
        return spec

    # ---------- Validation ----------

    def validate(self) -> None:
        """
        Validate core fields and raise ValueError on any invalid state.
        """
        # name
        if not self.name or not isinstance(self.name, str):
            raise ValueError("PluginSpec.name must be a non-empty string.")

        # slug
        if not isinstance(self.slug, str):
            raise ValueError("PluginSpec.slug must be a string.")

        if not re.fullmatch(r"[a-z0-9_-]+", self.slug):
            raise ValueError(
                f"PluginSpec.slug '{self.slug}' must match [a-z0-9_-]+."
            )

        # goal
        if not self.goal or not isinstance(self.goal, str):
            raise ValueError("PluginSpec.goal must be a non-empty string.")

        # category
        if not isinstance(self.category, str):
            raise ValueError("PluginSpec.category must be a string.")

        if self.category not in _VALID_CATEGORIES:
            raise ValueError(
                f"PluginSpec.category '{self.category}' must be one of: "
                f"{sorted(_VALID_CATEGORIES)}"
            )

        # tags
        if not isinstance(self.tags, list) or not all(
            isinstance(t, str) for t in self.tags
        ):
            raise ValueError("PluginSpec.tags must be a list of strings.")

        # timeout
        if not isinstance(self.timeout_seconds, int) or self.timeout_seconds <= 0:
            raise ValueError("PluginSpec.timeout_seconds must be a positive integer.")

        # basic sanity on extra
        if not isinstance(self.extra, dict):
            raise ValueError("PluginSpec.extra must be a dict.")

    # ---------- Convenience properties ----------

    @property
    def display_name(self) -> str:
        """
        A human-oriented display name, useful for logs / UIs.
        """
        return self.name

    @property
    def short_goal(self) -> str:
        """
        A shortened version of the goal for prompts / logs.
        """
        goal = self.goal.strip()
        if len(goal) <= 160:
            return goal
        return goal[:157].rstrip() + "..."

    # ---------- Serialization ----------

    def to_dict(self) -> PluginSpecDict:
        """
        Serialize to a plain dict suitable for JSON, logging, etc.
        """
        return {
            "name": self.name,
            "slug": self.slug,
            "goal": self.goal,
            "category": self.category,
            "tags": list(self.tags),
            "version": self.version,
            "capability_type": self.capability_type,
            "intended_domain": self.intended_domain,
            "author": self.author,
            "owner_id": self.owner_id,
            "requires_internet": self.requires_internet,
            "os_target": self.os_target,
            "timeout_seconds": self.timeout_seconds,
            "use_cases": list(self.use_cases),
            "primary_use_case": self.primary_use_case,
            "example_payload": self.example_payload,
            "problem_statement": self.problem_statement,
            "primary_inputs": self.primary_inputs,
            "primary_outputs": self.primary_outputs,
            "constraints": self.constraints,
            "example_use_cases": list(self.example_use_cases),
            "io_contract": self.io_contract,
            "extra": dict(self.extra),
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "PluginSpec":
        """
        Rehydrate a PluginSpec from a dict, then validate it.
        Unknown keys are ignored; missing keys use safe defaults.
        """
        extra = data.get("extra") or {}
        spec = cls(
            name=data["name"],
            slug=data["slug"],
            goal=data["goal"],
            category=data["category"],
            tags=list(data.get("tags", [])),
            version=data.get("version", "0.1.0"),
            capability_type=data.get("capability_type"),
            intended_domain=data.get("intended_domain"),
            author=data.get("author", "francis-factory"),
            owner_id=data.get("owner_id"),
            requires_internet=bool(data.get("requires_internet", False)),
            os_target=data.get("os_target", "any"),
            timeout_seconds=int(data.get("timeout_seconds", 30)),
            use_cases=list(data.get("use_cases", [])),
            primary_use_case=data.get("primary_use_case"),
            example_payload=data.get("example_payload"),
            problem_statement=data.get("problem_statement"),
            primary_inputs=data.get("primary_inputs"),
            primary_outputs=data.get("primary_outputs"),
            constraints=data.get("constraints"),
            example_use_cases=list(data.get("example_use_cases", [])),
            io_contract=data.get("io_contract"),
            extra=extra,
        )
        spec.validate()
        return spec

    def to_json(self, indent: int | None = None) -> str:
        """
        Serialize this spec to a JSON string.
        """
        return json.dumps(self.to_dict(), indent=indent)

    @classmethod
    def from_json(cls, text: str) -> "PluginSpec":
        """
        Parse a JSON string into a PluginSpec.
        """
        data = json.loads(text)
        return cls.from_dict(data)
