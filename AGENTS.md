# Factory Coding-Agent Instructions

- Preserve the Station C async `invoke` envelope and the `{status, output, error, meta}` result shape.
- Do not accept a generated plugin based only on runtime/import success.
- Every capability must have a `CapabilitySpec`.
- Every generated plugin must map to a known `LogicProfile`.
- Every canonical plugin must pass structural and semantic validation.
- Every newly promoted plugin must pass A+ certification after production quality and identity gates.
- Repair good shells before rejecting them when the failure is semantic routing or shallow logic.
- Never let metadata-only relabeling count as real capability behavior.
- Continuous expansion may target any practical domain, but every retained module must be an AI-consumable capability that turns payload data into structured, deterministic assistance.
- Broad target/domain variation belongs in the spec, use cases, tags, details, and behavior; keep installable slugs short and numbered.
- Tests must include semantic contrast payloads, not only smoke tests.
- Keep generated plugin artifacts inside `factory/plugins` and commit only after promotion gates pass.
- Do not remove backward-compatible logic profile aliases; normalize them to canonical profile ids.
