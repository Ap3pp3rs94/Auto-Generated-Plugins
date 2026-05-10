from __future__ import annotations

from typing import Any

try:
    from factory.factory_os.profiles.overlap_checker import run_capability_overlap_checker
except Exception:  # pragma: no cover
    from factory_os.profiles.overlap_checker import run_capability_overlap_checker

from .profile_utils import finalize_profile_result, normalize_payload


PROFILE_ID = "capability_overlap_checker_profile"


def run(context: Any, payload: Any, config: dict[str, Any] | None, manifest: dict[str, Any]) -> dict[str, Any]:
    payload_data, warnings = normalize_payload(payload)
    result = run_capability_overlap_checker(payload, config)
    return finalize_profile_result(result, profile_id=PROFILE_ID, payload_warnings=warnings, manifest=manifest, payload_data=payload_data)
