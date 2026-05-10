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
) -> dict[str, Any]:
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
    result["scores"] = scores

    details = result["details"] if isinstance(result["details"], dict) else {}
    details.setdefault("logic_profile_id", profile_id)
    details.setdefault("payload_warnings", payload_warnings)
    details.setdefault("missing_inputs", [])
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
    diagnostics.setdefault("payload_warning_count", len(payload_warnings))
    diagnostics.setdefault("manifest_slug", manifest_value(manifest, "slug", ""))
    result["diagnostics"] = diagnostics
    return result
