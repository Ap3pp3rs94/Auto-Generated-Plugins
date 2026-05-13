# Generated Capability Walkthrough

This walkthrough describes the current retention standard for generated
capability modules. The exact plugin inventory changes over time, so examples
use the numbered module convention instead of naming one stale artifact as the
permanent seed.

Current generated modules live under:

```text
plugins/<capability_family>_<number>.py
```

Example shape:

```text
plugins/ai_capability_overlap_checker_000833.py
```

## Spec

Every retained module starts from a capability spec. The spec defines the
capability boundary, required inputs, required detail keys, required scores,
forbidden fields, logic profile ids, and semantic probes.

For an overlap-checking capability, the spec must require behavior like:

- comparing a proposed capability against existing plugin records
- computing duplicate risks and max similarity
- producing a uniqueness fingerprint
- choosing `generate_new`, `redesign_boundary`, `merge_or_reject`, or
  `insufficient_input`
- avoiding unrelated backlog, release-package, or repair-plan fields

## Generated Body

Generated files should not carry the old universal multi-profile branch table.
They preserve the Station C envelope and call the profile dispatcher or a
profile-specific body. The body must use real payload input, not the plugin's
own goal text, when deciding whether the request is complete.

Required behaviors include:

- empty payloads return `missing_inputs` and progress blockers
- non-dict payloads preserve `_payload_warnings`
- `scores` includes at least `confidence` and `usefulness`
- top-level `diagnostics` records profile id, input signals, warning counts,
  and semantic-probe readiness
- `fun_mode` includes `celebratory_microcopy` while keeping backward-compatible
  microcopy fields when present

## Sample Invocation

```python
import asyncio
from plugins.ai_capability_overlap_checker_000833 import invoke

payload = {
    "plugin_name": "AI Capability Overlap Checker",
    "objective": "Check whether a proposed AI capability overlaps existing modules.",
    "existing_plugins": [
        {
            "name": "AI Capability Overlap Checker 000100",
            "slug": "ai_capability_overlap_checker_000100",
            "family_key": "ai_plugin_factory::capability_overlap_checker",
            "owns": [
                "capability boundary comparison",
                "duplicate risk scoring",
                "merge or reject recommendation",
            ],
        }
    ],
}

result = asyncio.run(invoke("demo-user", payload, run_id="walkthrough-demo"))
print(result["output"]["details"]["merge_or_reject_decision"])
```

Representative output fields:

```json
{
  "summary": "AI Capability Overlap Checker: compared the proposed capability against existing plugin records.",
  "scores": {
    "confidence": 0.86,
    "usefulness": 0.91,
    "duplicate_risk": 0.72
  },
  "details": {
    "duplicate_risks": [],
    "uniqueness_fingerprint": [],
    "comparison_targets": [],
    "merge_or_reject_decision": "merge_or_reject",
    "max_similarity": 0.72,
    "missing_inputs": []
  },
  "diagnostics": {
    "logic_profile_id": "capability_overlap_checker_profile",
    "has_user_input": true,
    "input_signal_count": 2,
    "semantic_probe_ready": true
  }
}
```

## Validation

Station C validates generated modules before they are kept:

```bash
python - <<'PY'
from pathlib import Path
from station_c_validator import validate_plugin_module

path = next(Path("plugins").glob("ai_capability_overlap_checker_*.py"))
ok, reason = validate_plugin_module(path)
print(path)
print(ok)
print(reason)
PY
```

Quality gates then check semantic depth, profile contracts, promotion decisions,
and the `0.95` production threshold.

## Why A Plugin Stays

A generated module is retained only when it satisfies the current library rules:

- AI-consumable capability behavior
- deterministic Python output
- preserved Station C async `invoke` envelope
- required profile-specific detail keys and scores
- missing-input behavior that does not use goal fallback as input
- non-dict payload warnings preserved into output details
- semantic contrast across different payloads
- no metadata-only relabeling
- no unrelated multi-profile branch table
- no duplicate canonical capability unless the new module is a measured upgrade
