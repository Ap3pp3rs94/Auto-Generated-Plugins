from __future__ import annotations

import re
import string
from typing import Any


CANONICAL_PROFILE_ID = "capability_overlap_checker_profile"

_STOPWORDS = {
    "a",
    "an",
    "and",
    "are",
    "as",
    "at",
    "be",
    "by",
    "for",
    "from",
    "in",
    "into",
    "is",
    "it",
    "new",
    "of",
    "or",
    "the",
    "this",
    "to",
    "with",
    "whether",
}
_PRESERVE_TERMS = {
    "capability",
    "plugin",
    "overlap",
    "duplicate",
    "validator",
    "registry",
    "profile",
    "semantic",
    "repair",
    "release",
    "backlog",
}


def _tokenize(value: Any) -> list[str]:
    text = str(value or "").lower().replace("_", " ").replace("-", " ")
    text = text.translate(str.maketrans("", "", string.punctuation))
    tokens = []
    for token in re.split(r"\s+", text):
        token = token.strip()
        if not token:
            continue
        if len(token) <= 2 and token not in _PRESERVE_TERMS:
            continue
        if token in _STOPWORDS and token not in _PRESERVE_TERMS:
            continue
        tokens.append(token)
    return tokens


def _plugin_text(plugin: Any) -> str:
    if isinstance(plugin, str):
        return plugin
    if not isinstance(plugin, dict):
        return str(plugin)
    parts: list[str] = []
    for key in [
        "name",
        "slug",
        "family_key",
        "goal",
        "purpose",
        "capability_boundary",
    ]:
        if plugin.get(key):
            parts.append(str(plugin.get(key)))
    for key in ["owns", "tags", "required_detail_keys"]:
        value = plugin.get(key)
        if isinstance(value, list):
            parts.extend(str(item) for item in value)
        elif value:
            parts.append(str(value))
    return " ".join(parts)


def _candidate_text(payload_data: dict[str, Any]) -> tuple[str, bool]:
    parts = []
    used_fallback_goal = False
    for key in [
        "candidate_capability",
        "plugin_name",
        "slug",
        "task",
        "objective",
        "prompt",
        "description",
        "goal",
    ]:
        value = payload_data.get(key)
        if value:
            parts.append(str(value))
    return " ".join(parts).strip(), used_fallback_goal


def _display_plugin(plugin: Any) -> str:
    if isinstance(plugin, dict):
        return str(plugin.get("slug") or plugin.get("name") or plugin)[:220]
    return str(plugin)[:220]


def run_capability_overlap_checker(payload: Any, config: dict[str, Any] | None = None) -> dict[str, Any]:
    config = config or {}
    payload_warnings: list[str] = []
    if isinstance(payload, dict):
        payload_data = payload
        wrapped_warnings = payload_data.get("_payload_warnings")
        if isinstance(wrapped_warnings, list):
            payload_warnings.extend(str(item) for item in wrapped_warnings if item)
        non_user_keys = {"_value", "_payload_warnings"}
        if "_value" in payload_data and not (set(payload_data.keys()) - non_user_keys) and not isinstance(payload_data.get("_value"), dict):
            payload_warnings.append("payload was not a dict; invoke wrapped it in _value")
    else:
        payload_data = {}
        payload_warnings.append("payload was not a dict; using empty payload")

    candidate, used_fallback_goal = _candidate_text(payload_data)
    existing_plugins_raw = payload_data.get("existing_plugins")
    existing_plugins = existing_plugins_raw if isinstance(existing_plugins_raw, list) else []
    if existing_plugins_raw is None:
        payload_warnings.append("no existing_plugins comparison set was provided")
    elif not isinstance(existing_plugins_raw, list):
        payload_warnings.append("existing_plugins was not a list and was ignored")
    elif not existing_plugins:
        payload_warnings.append("existing_plugins was empty; duplicate risk is limited")

    missing_inputs: list[str] = []
    if not candidate:
        missing_inputs.append("candidate capability name, task, objective, prompt, or slug")

    candidate_tokens = set(_tokenize(candidate))
    comparison_targets = [_display_plugin(item) for item in existing_plugins[:25]]
    duplicate_risks: list[dict[str, Any]] = []
    max_similarity = 0.0
    exact_match = False

    candidate_slug = str(payload_data.get("slug") or "").lower()
    candidate_family = str(payload_data.get("family_key") or "").lower()
    candidate_name = str(payload_data.get("plugin_name") or payload_data.get("candidate_capability") or "").lower()

    for plugin in existing_plugins[:50]:
        plugin_text = _plugin_text(plugin)
        plugin_tokens = set(_tokenize(plugin_text))
        shared = sorted(candidate_tokens & plugin_tokens)
        union = candidate_tokens | plugin_tokens
        similarity = (len(shared) / len(union)) if union else 0.0
        reason_parts = []
        if isinstance(plugin, dict):
            existing_slug = str(plugin.get("slug") or "").lower()
            existing_family = str(plugin.get("family_key") or "").lower()
            existing_name = str(plugin.get("name") or "").lower()
            existing_keys = set(_tokenize(plugin.get("required_detail_keys", [])))
            candidate_keys = set(_tokenize(payload_data.get("required_detail_keys", [])))
            owns_tokens = set(_tokenize(plugin.get("owns", [])))
            if candidate_slug and existing_slug and candidate_slug == existing_slug:
                similarity += 0.45
                exact_match = True
                reason_parts.append("exact slug match")
            if candidate_family and existing_family and candidate_family == existing_family:
                similarity += 0.35
                exact_match = True
                reason_parts.append("exact family_key match")
            if candidate_name and existing_name and candidate_name == existing_name:
                similarity += 0.35
                exact_match = True
                reason_parts.append("same normalized name")
            elif candidate_name and existing_name and (
                candidate_name in existing_name or existing_name in candidate_name
            ):
                similarity += 0.22
                reason_parts.append("name containment match")
            if existing_keys and candidate_keys:
                key_overlap = existing_keys & candidate_keys
                if key_overlap:
                    similarity += min(0.12, 0.03 * len(key_overlap))
                    reason_parts.append("shared required detail keys")
            if owns_tokens:
                owns_overlap = owns_tokens & candidate_tokens
                if owns_overlap:
                    similarity += min(0.10, 0.02 * len(owns_overlap))
                    reason_parts.append("shared ownership terms")
        similarity = round(min(0.95, similarity), 3)
        max_similarity = max(max_similarity, similarity)
        if shared or similarity >= 0.12:
            duplicate_risks.append(
                {
                    "existing_plugin": _display_plugin(plugin),
                    "overlap_terms": shared[:20],
                    "similarity": similarity,
                    "reason": "; ".join(reason_parts) if reason_parts else "shared capability terms",
                }
            )

    duplicate_risks = sorted(duplicate_risks, key=lambda item: item["similarity"], reverse=True)[:10]
    max_similarity = round(max_similarity, 3)

    if missing_inputs:
        decision = "insufficient_input"
    elif exact_match or max_similarity >= 0.45:
        decision = "merge_or_reject"
    elif max_similarity >= 0.18 or duplicate_risks:
        decision = "redesign_boundary"
    else:
        decision = "generate_new"

    duplicate_risk = 0.0 if missing_inputs else min(0.95, max_similarity + (0.08 if exact_match else 0.0))
    confidence = 0.28
    if candidate:
        confidence += 0.32
    if existing_plugins:
        confidence += 0.24
    if duplicate_risks:
        confidence += 0.08
    usefulness = 0.42 + (0.24 if candidate else 0.0) + (0.22 if existing_plugins else 0.0) + (0.08 if comparison_targets else 0.0)
    if missing_inputs:
        usefulness = min(usefulness, 0.55)

    uniqueness_fingerprint = sorted(candidate_tokens)[:24]
    next_step = {
        "insufficient_input": "Provide a candidate capability name, task, objective, prompt, or slug.",
        "merge_or_reject": "Merge with or reject against the closest existing capability.",
        "redesign_boundary": "Redesign the boundary to make the capability uniquely owned.",
        "generate_new": "Generate a new canonical capability slot.",
    }[decision]
    summary = (
        f"Capability overlap decision: {decision} "
        f"(max similarity {max_similarity:.2f}, checked {len(existing_plugins)} existing plugin(s))."
    )

    return {
        "summary": summary,
        "primary_insights": [
            {"title": "Decision", "detail": decision},
            {"title": "Highest similarity", "detail": max_similarity},
            {"title": "Duplicate risks", "detail": duplicate_risks or "No meaningful overlap found."},
        ],
        "recommended_actions": [
            {"action": next_step, "decision": decision, "duplicate_risk": round(duplicate_risk, 2)},
            {"action": "Review closest comparison targets", "targets": comparison_targets[:5]},
        ],
        "scores": {
            "confidence": round(min(0.94, confidence), 2),
            "usefulness": round(min(0.94, usefulness), 2),
            "duplicate_risk": round(duplicate_risk, 2),
        },
        "details": {
            "duplicate_risks": duplicate_risks,
            "uniqueness_fingerprint": uniqueness_fingerprint,
            "comparison_targets": comparison_targets,
            "merge_or_reject_decision": decision,
            "max_similarity": max_similarity,
            "missing_inputs": missing_inputs,
            "payload_warnings": payload_warnings,
            "logic_profile_id": CANONICAL_PROFILE_ID,
        },
        "progress_state": {
            "current_stage": CANONICAL_PROFILE_ID,
            "next_step": next_step,
            "blockers": missing_inputs,
            "done_signals": ["capability_overlap_checked", decision],
        },
        "user_experience": {
            "plain_language_takeaway": summary,
            "interaction_suggestions": [
                "Compare duplicate_risks before creating a new module",
                "Use redesign_boundary when the idea is close but still useful",
                "Reject metadata-only relabeling",
            ],
        },
        "fun_mode": {
            "challenge_label": "Capability Boundary Check",
            "score_badge": "Duplicate Risk " + str(round(duplicate_risk, 2)),
            "microcopy": "The capability got a boundary check before promotion.",
            "celebratory_microcopy": "The capability got a boundary check before promotion.",
        },
        "diagnostics": {
            "logic_profile_id": CANONICAL_PROFILE_ID,
            "existing_plugins_checked": len(existing_plugins),
            "candidate_keywords_count": len(candidate_tokens),
            "duplicate_risks_count": len(duplicate_risks),
            "used_fallback_goal": used_fallback_goal,
        },
    }
