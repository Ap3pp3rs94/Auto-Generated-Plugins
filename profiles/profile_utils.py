from __future__ import annotations

from typing import Any


def normalize_payload(payload: Any) -> tuple[dict[str, Any], list[str]]:
    if isinstance(payload, dict):
        warnings = list(payload.get("_payload_warnings", [])) if isinstance(payload.get("_payload_warnings"), list) else []
        non_user_keys = {"_value", "_payload_warnings"}
        if "_value" in payload and not (set(payload.keys()) - non_user_keys):
            warnings.append("payload was not a dict; invoke wrapped it in _value")
        return payload, warnings
    return {}, ["payload was not a dict; using empty payload"]


USER_INPUT_KEYS = [
    "task",
    "objective",
    "prompt",
    "instruction",
    "query",
    "question",
    "response",
    "answer",
    "messages",
    "source_notes",
    "candidate_outputs",
    "previous_results",
    "trace",
    "completed_steps",
    "current_plan",
    "expected_behavior",
    "agents",
    "workstreams",
    "ownership_scopes",
    "candidate_capability",
    "capability_spec",
    "plugin_name",
    "slug",
    "name",
    "files",
    "changed_files",
    "validation_summary",
    "quality_failures",
    "probe_results",
    "semantic_results",
]


def has_input_value(payload: dict[str, Any], key: str) -> bool:
    value = payload.get(key)
    if isinstance(value, str):
        return bool(value.strip())
    if isinstance(value, (list, tuple, set, dict)):
        return bool(value)
    return value is not None


def input_signal_keys(payload: dict[str, Any]) -> list[str]:
    return [key for key in USER_INPUT_KEYS if has_input_value(payload, key)]


def user_target_text(payload: dict[str, Any]) -> str:
    parts: list[str] = []
    for key in ["task", "objective", "prompt", "instruction", "query", "question", "response", "answer"]:
        if has_input_value(payload, key):
            parts.append(str(payload.get(key))[:300])
    for key in ["messages", "source_notes", "candidate_outputs"]:
        value = payload.get(key)
        if isinstance(value, list):
            parts.extend(str(item)[:180] for item in value[:3])
    return " ".join(part for part in parts if part).strip()


def input_signal_fingerprint(payload: dict[str, Any]) -> float:
    text = user_target_text(payload)
    return round((sum(ord(ch) for ch in text[:1000]) % 997) / 997, 3) if text else 0.0


def manifest_value(manifest: dict[str, Any], key: str, default: Any = "") -> Any:
    return manifest.get(key, default) if isinstance(manifest, dict) else default


def user_candidate_text(payload: dict[str, Any]) -> str:
    for key in [
        "candidate_capability",
        "capability_spec",
        "plugin_name",
        "slug",
        "task",
        "objective",
        "prompt",
        "description",
        "goal",
    ]:
        value = payload.get(key)
        if value:
            return str(value).strip()
    return ""


def capability_spec_payload(payload: dict[str, Any]) -> dict[str, Any]:
    spec = payload.get("capability_spec")
    if isinstance(spec, dict):
        return spec
    out: dict[str, Any] = {}
    for key in [
        "name",
        "slug",
        "family_key",
        "purpose",
        "owns",
        "does_not_own",
        "required_inputs",
        "optional_inputs",
        "required_detail_keys",
        "required_scores",
        "forbidden_detail_keys",
        "required_behavior",
        "forbidden_behavior",
    ]:
        if key in payload:
            out[key] = payload[key]
    if not out:
        candidate = user_candidate_text(payload)
        if candidate:
            out["name"] = candidate
            out["purpose"] = str(payload.get("objective") or payload.get("description") or candidate)
    return out


def finalize_profile_result(
    result: dict[str, Any],
    *,
    profile_id: str,
    payload_warnings: list[str],
    manifest: dict[str, Any],
    payload_data: dict[str, Any] | None = None,
) -> dict[str, Any]:
    payload_data = payload_data if isinstance(payload_data, dict) else {}
    signals = input_signal_keys(payload_data)
    has_user_input = bool(signals)
    used_goal_fallback = not has_user_input

    result.setdefault("summary", "Capability profile completed.")
    result.setdefault("primary_insights", [])
    result.setdefault("recommended_actions", [])
    result.setdefault("scores", {})
    result.setdefault("details", {})
    result.setdefault("progress_state", {})
    result.setdefault("user_experience", {})
    result.setdefault("fun_mode", {})
    result.setdefault("diagnostics", {})

    scores = result["scores"] if isinstance(result["scores"], dict) else {}
    scores.setdefault("confidence", 0.0)
    scores.setdefault("usefulness", 0.0)
    scores.setdefault("input_signal_variance", input_signal_fingerprint(payload_data))
    result["scores"] = scores

    details = result["details"] if isinstance(result["details"], dict) else {}
    details.setdefault("logic_profile_id", profile_id)
    existing_warnings = details.get("payload_warnings", [])
    if isinstance(existing_warnings, str):
        existing_warnings = [existing_warnings]
    elif not isinstance(existing_warnings, list):
        existing_warnings = []
    merged_warnings: list[str] = []
    for warning in list(existing_warnings) + list(payload_warnings):
        if warning and warning not in merged_warnings:
            merged_warnings.append(str(warning))
    details["payload_warnings"] = merged_warnings
    details.setdefault("missing_inputs", [])
    if isinstance(details["missing_inputs"], str):
        details["missing_inputs"] = [details["missing_inputs"]]
    elif not isinstance(details["missing_inputs"], list):
        details["missing_inputs"] = []
    if not has_user_input and "user-provided payload values" not in details["missing_inputs"]:
        details["missing_inputs"].append("user-provided payload values")
    details.setdefault("has_user_input", has_user_input)
    details.setdefault("used_goal_fallback", used_goal_fallback)
    details.setdefault("input_signals", signals)
    details.setdefault("input_signal_fingerprint", input_signal_fingerprint(payload_data))
    result["details"] = details

    progress = result["progress_state"] if isinstance(result["progress_state"], dict) else {}
    progress.setdefault("current_stage", profile_id)
    progress.setdefault("next_step", result["recommended_actions"][0]["action"] if result["recommended_actions"] and isinstance(result["recommended_actions"][0], dict) else "Review capability result.")
    progress.setdefault("blockers", details.get("missing_inputs", []))
    if details.get("missing_inputs") and not progress.get("blockers"):
        progress["blockers"] = details.get("missing_inputs", [])
    progress.setdefault("done_signals", [profile_id])
    result["progress_state"] = progress

    user_experience = result["user_experience"] if isinstance(result["user_experience"], dict) else {}
    user_experience.setdefault("plain_language_takeaway", str(result.get("summary") or "Capability profile completed."))
    user_experience.setdefault("interaction_suggestions", [])
    result["user_experience"] = user_experience

    fun = result["fun_mode"] if isinstance(result["fun_mode"], dict) else {}
    fun.setdefault("challenge_label", str(manifest_value(manifest, "name", "Capability Run")))
    fun.setdefault("score_badge", "Ready")
    fun.setdefault("microcopy", str(result.get("summary") or "Capability profile completed."))
    fun.setdefault("celebratory_microcopy", fun.get("microcopy", "Capability profile completed."))
    result["fun_mode"] = fun

    diagnostics = result["diagnostics"] if isinstance(result["diagnostics"], dict) else {}
    diagnostics.setdefault("logic_profile_id", profile_id)
    diagnostics.setdefault("used_goal_fallback", used_goal_fallback)
    diagnostics.setdefault("has_user_input", has_user_input)
    diagnostics.setdefault("input_signal_count", len(signals))
    diagnostics.setdefault("missing_inputs_count", len(details.get("missing_inputs", [])) if isinstance(details.get("missing_inputs"), list) else 0)
    diagnostics["payload_warning_count"] = len(details.get("payload_warnings", [])) if isinstance(details.get("payload_warnings"), list) else 0
    diagnostics.setdefault("profile_output_keys", sorted(result.keys()))
    diagnostics.setdefault("semantic_probe_ready", bool(has_user_input and not details.get("missing_inputs")))
    diagnostics.setdefault("manifest_slug", manifest_value(manifest, "slug", ""))
    result["diagnostics"] = diagnostics
    return result
