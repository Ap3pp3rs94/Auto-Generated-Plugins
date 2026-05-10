from __future__ import annotations

from typing import Any

from .profile_utils import capability_spec_payload, finalize_profile_result, normalize_payload, user_candidate_text, user_target_text


PROFILE_ID = "plugin_profile_gap_detector_profile"


def _as_list(value: Any) -> list[Any]:
    if isinstance(value, list):
        return value
    if value in (None, "", {}, ()):
        return []
    return [value]


def _slug(value: Any) -> str:
    if isinstance(value, dict):
        return str(value.get("slug") or value.get("name") or value).strip()
    return str(value).strip()


def run(context: Any, payload: Any, config: dict[str, Any] | None, manifest: dict[str, Any]) -> dict[str, Any]:
    payload_data, warnings = normalize_payload(payload)
    spec = capability_spec_payload(payload_data)
    focus = user_candidate_text(payload_data)
    target_text = user_target_text(payload_data)
    target_lower = target_text.lower()
    existing_plugins = _as_list(payload_data.get("existing_plugins"))
    registered_profiles = _as_list(payload_data.get("registered_profiles"))
    generated_plugins = _as_list(payload_data.get("generated_plugins"))
    candidates = generated_plugins or existing_plugins
    missing = []
    if not candidates and not spec and not focus:
        missing.append("existing_plugins, generated_plugins, capability_spec, or task")
    focus_terms = sorted(
        {
            word.strip(".,:;!?()[]{}").lower()
            for word in target_text.split()
            if len(word.strip(".,:;!?()[]{}")) > 5
        }
    )[:12]
    if any(term in target_lower for term in ["auth", "authentication", "login", "middleware", "migration", "rollback", "database"]):
        inferred_profile_family = {
            "family": "release_safety_profile_family",
            "matched_signals": [term for term in ["auth", "authentication", "login", "middleware", "migration", "rollback", "database"] if term in target_lower],
            "recommended_profile": "release_safety_regression_profile",
            "required_behavior": "inspect rollback, migration owner, and login-regression evidence",
        }
    elif any(term in target_lower for term in ["medical", "citation", "source", "claim", "retrieval", "hallucination", "unsupported"]):
        inferred_profile_family = {
            "family": "grounded_answer_profile_family",
            "matched_signals": [term for term in ["medical", "citation", "source", "claim", "retrieval", "hallucination", "unsupported"] if term in target_lower],
            "recommended_profile": "claim_source_grounding_profile",
            "required_behavior": "inspect claims, citation support, source gaps, and caveats",
        }
    elif any(term in target_lower for term in ["tool", "permission", "argument", "api", "browser", "workflow"]):
        inferred_profile_family = {
            "family": "tool_safety_profile_family",
            "matched_signals": [term for term in ["tool", "permission", "argument", "api", "browser", "workflow"] if term in target_lower],
            "recommended_profile": "tool_permission_argument_profile",
            "required_behavior": "inspect tool permissions, argument safety, and execution ordering",
        }
    else:
        inferred_profile_family = {
            "family": "generic_capability_profile_family",
            "matched_signals": focus_terms[:5],
            "recommended_profile": "capability_contract_profile",
            "required_behavior": "inspect declared inputs, outputs, details, scores, and semantic probes",
        }

    registered_ids = {_slug(item) for item in registered_profiles}
    missing_profile_slugs = []
    duplicate_profile_ids: dict[str, int] = {}
    seen_profiles: dict[str, int] = {}
    alias_gaps = []
    for item in candidates:
        if isinstance(item, dict):
            slug = str(item.get("slug") or item.get("name") or "").strip()
            profile_id = str(item.get("logic_profile_id") or item.get("profile_id") or "").strip()
            aliases = item.get("aliases") if isinstance(item.get("aliases"), list) else []
        else:
            slug = str(item).strip()
            profile_id = ""
            aliases = []
        if slug and registered_ids and slug not in registered_ids and profile_id not in registered_ids:
            missing_profile_slugs.append(slug)
        if profile_id:
            seen_profiles[profile_id] = seen_profiles.get(profile_id, 0) + 1
        if profile_id and not aliases:
            alias_gaps.append({"slug": slug, "logic_profile_id": profile_id, "gap": "no aliases declared"})
    for profile_id, count in seen_profiles.items():
        if count > 1:
            duplicate_profile_ids[profile_id] = count

    profile_gaps = []
    for slug in missing_profile_slugs[:20]:
        profile_gaps.append({"slug": slug, "gap": "no registered reusable profile found"})
    for gap in alias_gaps[:20]:
        profile_gaps.append(gap)
    if not candidates and focus:
        profile_gaps.append(
            {
                "slug": str(spec.get("slug") or focus).strip()[:120],
                "gap": "no candidate inventory supplied; inferred required profile family from payload focus",
                "recommended_profile": inferred_profile_family["recommended_profile"],
                "matched_signals": inferred_profile_family["matched_signals"],
            }
        )
    coverage_summary = {
        "candidate_count": len(candidates),
        "registered_profile_count": len(registered_profiles),
        "missing_profile_count": len(missing_profile_slugs),
        "alias_gap_count": len(alias_gaps),
        "duplicate_profile_ids": duplicate_profile_ids,
        "inferred_profile_family": inferred_profile_family["family"],
        "focus_terms": focus_terms,
    }
    profile_recommendations = [
        {
            "action": "Create or register inferred profile family",
            "profile_family": inferred_profile_family["family"],
            "recommended_profile": inferred_profile_family["recommended_profile"],
            "required_behavior": inferred_profile_family["required_behavior"],
            "matched_signals": inferred_profile_family["matched_signals"],
        },
        {
            "action": "Collect candidate inventory for profile coverage check",
            "needed_fields": ["existing_plugins", "generated_plugins", "registered_profiles"],
            "focus_terms": focus_terms[:8],
        },
    ]
    result = {
        "summary": (
            "Profile gap check for "
            + (focus or "missing focus")
            + ": inferred "
            + inferred_profile_family["family"]
            + " from "
            + (", ".join(inferred_profile_family["matched_signals"][:5]) or "no strong signal")
            + "."
        ),
        "primary_insights": [
            {"title": "Inferred profile family", "detail": inferred_profile_family},
            {"title": "Focus terms", "detail": focus_terms},
            {"title": "Coverage summary", "detail": coverage_summary},
            {"title": "Profile gaps", "detail": profile_gaps or "No profile coverage gaps found in supplied data."},
        ],
        "recommended_actions": [
            profile_recommendations[0],
            profile_recommendations[1],
            {"action": "Register reusable profile modules for missing slugs", "slugs": missing_profile_slugs[:10]},
            {"action": "Add backward-compatible aliases", "alias_gaps": alias_gaps[:10]},
        ],
        "scores": {
            "confidence": round(min(0.92, 0.36 + 0.04 * len(candidates[:10]) + 0.1 * bool(registered_profiles) + 0.04 * bool(focus_terms)), 2),
            "usefulness": 0.87 if candidates else 0.42,
            "coverage": round(1.0 - (len(missing_profile_slugs) / max(1, len(candidates))), 2),
            "profile_family_specificity": round(min(0.94, 0.45 + 0.05 * len(inferred_profile_family["matched_signals"]) + 0.02 * len(focus_terms)), 2),
        },
        "details": {
            "profile_gaps": profile_gaps,
            "missing_profile_slugs": missing_profile_slugs,
            "alias_gaps": alias_gaps,
            "coverage_summary": coverage_summary,
            "inferred_profile_family": inferred_profile_family,
            "profile_recommendations": profile_recommendations,
            "focus_terms": focus_terms,
            "missing_inputs": missing,
        },
        "progress_state": {
            "current_stage": PROFILE_ID,
            "next_step": "Register " + inferred_profile_family["recommended_profile"],
            "blockers": missing,
            "done_signals": ["profile_gap_checked", inferred_profile_family["family"]],
        },
    }
    return finalize_profile_result(result, profile_id=PROFILE_ID, payload_warnings=warnings, manifest=manifest, payload_data=payload_data)
