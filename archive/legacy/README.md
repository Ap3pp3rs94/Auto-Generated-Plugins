# Legacy Station Experiments

These files are preserved for historical reference only.

They are not the canonical production path:

- `station_a_spec_picker.py` was an older Ollama-driven random spec picker.
- `station_a_spec_creator.py` is an empty early placeholder.
- `station_b_builder.py` was an older Station B body builder.
- `production_line.py` was an older queue runner and no longer matches the
  current `factory_runner.py` API.
- `library_qc.py` validated the older `plugin_index.json` library shape; the
  active path is `quality_runner.py`.

The current pipeline uses:

- `spec_builder.py` for the deterministic AI capability roadmap.
- `station_b_generator.py` for the lightweight sidecar Station B fallback.
- the parent Francis `station_b.py` runtime when the full Francis project is
  available.
- `factory_runner.py` as the production orchestrator.
- `quality_runner.py` for current retained-plugin auditing and repair.
