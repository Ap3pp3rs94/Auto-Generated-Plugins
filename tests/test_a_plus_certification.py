from __future__ import annotations

import asyncio
import unittest

from factory_os.a_plus_certification import (
    A_PLUS_MIN_SCORE,
    certify_plugin_callable,
    summarize_a_plus_result,
)


async def a_plus_plugin(user_id: str, payload, **kwargs):
    if not isinstance(payload, dict):
        payload = {
            "_value": payload,
            "_payload_warnings": ["payload was not a dict; invoke wrapped it in _value"],
        }
    text = " ".join(str(value) for value in payload.values()).lower()
    is_empty = not (set(payload.keys()) - {"_value", "_payload_warnings"})
    is_medical = "medical" in text or "clinical" in text or "dosage" in text or "citation mismatch" in text
    profile_id = "continuous_trace_failure_router_profile"
    missing_inputs = ["trace"] if is_empty else []
    details = {
        "logic_profile_id": profile_id,
        "payload_warnings": list(payload.get("_payload_warnings", [])),
        "missing_inputs": missing_inputs,
        "failure_points": [{"stage": "retrieval" if is_medical else "release", "issue": "citation mismatch" if is_medical else "rollback gap"}],
        "signals_by_stage": {"retrieval" if is_medical else "release": ["citation" if is_medical else "auth"]},
        "retry_plan": [{"step": "verify citation" if is_medical else "run auth rollback check"}],
    }
    diagnostics = {
        "logic_profile_id": profile_id,
        "has_user_input": not is_empty,
        "used_goal_fallback": is_empty,
        "input_signal_count": 0 if is_empty else 5,
        "missing_inputs_count": len(missing_inputs),
        "payload_warning_count": len(details["payload_warnings"]),
        "profile_output_keys": sorted(details.keys()),
        "semantic_probe_ready": bool(not is_empty and not missing_inputs),
    }
    output = {
        "summary": (
            "AI Trace Failure Router: medical citation risk retry plan with source verification."
            if is_medical
            else "AI Trace Failure Router: release validation retry plan with rollback evidence."
        ),
        "primary_insights": [
            {"title": "Failure point", "detail": details["failure_points"]},
            {"title": "Signals", "detail": details["signals_by_stage"]},
        ],
        "recommended_actions": [
            {"action": "Verify citation grounding before final answer" if is_medical else "Run rollback and login regression checks"},
            {"action": "Escalate unsupported claim" if is_medical else "Assign release owner for rollback evidence"},
        ],
        "scores": {
            "confidence": 0.82 if is_medical else 0.88,
            "usefulness": 0.86 if is_medical else 0.9,
            "risk": 0.64 if is_medical else 0.38,
        },
        "details": details,
        "progress_state": {
            "current_stage": profile_id,
            "next_step": "Provide trace input." if is_empty else ("verify citations" if is_medical else "verify rollback"),
            "blockers": missing_inputs,
        },
        "user_experience": {"plain_language_takeaway": "The next retry path is explicit and checkable."},
        "fun_mode": {"microcopy": "Route sharpened.", "celebratory_microcopy": "Route sharpened."},
        "diagnostics": diagnostics,
    }
    return {"status": "succeeded", "output": output, "error": "", "meta": {"user_id": user_id}}


async def generic_shell_plugin(user_id: str, payload, **kwargs):
    output = {
        "summary": "AI Plugin: processed the request and produced a useful result.",
        "primary_insights": [{"title": "Generic", "detail": "Use the capability."}],
        "recommended_actions": [{"action": "Use first recommendation"}],
        "scores": {"confidence": 0.9},
        "details": {"logic_profile_id": "continuous_trace_failure_router_profile"},
        "progress_state": {"next_step": "Continue", "blockers": []},
        "user_experience": {"plain_language_takeaway": "Processed."},
        "fun_mode": {"microcopy": "Done."},
        "diagnostics": {"logic_profile_id": "continuous_trace_failure_router_profile"},
    }
    return {"status": "succeeded", "output": output, "error": "", "meta": {"user_id": user_id}}


class APlusCertificationTests(unittest.TestCase):
    def test_a_plus_plugin_certifies(self) -> None:
        result = asyncio.run(
            certify_plugin_callable(
                a_plus_plugin,
                metadata={
                    "slug": "ai_trace_failure_router_999999",
                    "name": "AI Trace Failure Router 999999",
                    "logic_profile_id": "continuous_trace_failure_router_profile",
                },
            )
        )

        self.assertTrue(result.passed, summarize_a_plus_result(result))
        self.assertGreaterEqual(result.score, A_PLUS_MIN_SCORE)
        self.assertEqual(result.recommended_action, "certify")

    def test_generic_shell_does_not_certify(self) -> None:
        result = asyncio.run(
            certify_plugin_callable(
                generic_shell_plugin,
                metadata={
                    "slug": "ai_trace_failure_router_999998",
                    "name": "AI Trace Failure Router 999998",
                    "logic_profile_id": "continuous_trace_failure_router_profile",
                },
            )
        )

        self.assertFalse(result.passed)
        self.assertIn(result.recommended_action, {"repair", "regenerate"})
        self.assertTrue(any(finding.code in {"thin_diagnostics", "missing_confidence_usefulness"} for finding in result.findings))

    def test_summary_reports_failure_action(self) -> None:
        result = asyncio.run(certify_plugin_callable(generic_shell_plugin))
        summary = summarize_a_plus_result(result)

        self.assertIn("a_plus:", summary)
        self.assertIn("action=", summary)


if __name__ == "__main__":
    unittest.main()
