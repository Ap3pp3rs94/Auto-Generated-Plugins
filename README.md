# Auto-Generated Plugins Factory

Autonomous factory subsystem for generating, validating, and iterating AI-focused
Francis plugins.

This repository is the factory codebase for:

- deterministic AI plugin specs
- Station B model-driven plugin generation
- Station C structural validation
- duplicate and fallback rejection
- AI roadmap handoffs between generated plugins
- local Ollama-based plugin production
- future quality scoring, telemetry, repair, and learning hooks

The active GitHub remote is:

```text
github.com/Ap3pp3rs94/Auto-Generated-Plugins
```

Do not push this repository to a Francis app remote unless that is explicitly
intended.

## Current Goal

The factory is tuned to produce plugins specifically for AI functionality and AI
workflow progress. It should not wander into random categories just because it
can generate code.

Legacy plugins created before these guides are intentionally not part of the
current tracked plugin library. The repository should only keep generated
plugins that were produced under the AI roadmap, handoff, duplicate-control, and
user-experience standards described here.

The intended output is a growing library of complementary AI capabilities such
as:

- prompt refinement
- agent task planning
- tool selection
- memory compression
- context optimization
- output quality scoring
- hallucination risk checks
- retrieval query expansion
- multi-agent handoffs
- prompt test generation
- workflow debugging
- response comparison
- instruction conflict detection
- structured prompt building
- capability routing
- evaluation rubric generation

Each generated plugin should advance the roadmap instead of recreating a
previous plugin under a new name.

## How It Works

The factory runner is the main orchestrator:

```bash
cd /home/peppera091/francis
./.venv/bin/python -m factory.factory_runner
```

The runner performs this loop:

1. Load existing plugins from `/home/peppera091/francis/plugins`.
2. Load existing capability signatures from the plugin registry when available.
3. Load or seed the AI roadmap handoff state.
4. Choose the next deterministic AI capability from `spec_builder.py`.
5. Skip duplicate slugs, duplicate files, and duplicate capability signatures.
6. Attach handoff context from previous AI roadmap plugins.
7. Ask Station B to generate real plugin logic through Ollama.
8. Reject timeout/error fallback output for AI roadmap plugins.
9. Write the plugin into the parent project's `plugins/` directory.
10. Validate the plugin with Station C.
11. Optionally evaluate or repair through Station D hooks if available.
12. Record the completed plugin and prepare a directive for the next plugin.
13. Sleep and continue.

## Repository Boundary

This repo lives at:

```text
/home/peppera091/francis/factory
```

The factory writes generated plugins to the parent project:

```text
/home/peppera091/francis/plugins
```

That split is intentional:

- `factory/` contains the machinery.
- `plugins/` contains produced plugin artifacts.
- `registry/ai_roadmap_state.json` tracks roadmap continuity in the parent
  project.

The Git repository for this factory was created inside `factory/`, not at the
parent Francis project root.

Tracked plugin artifacts in this repository should be curated. If an old plugin
was not produced under the current AI roadmap guide, remove it instead of
letting it define the quality bar for future generation.

## Important Files

| File | Purpose |
| --- | --- |
| `factory_runner.py` | Main production loop and station orchestration. |
| `spec_builder.py` | Deterministic AI capability roadmap. |
| `plugin_spec.py` | Plugin specification data model. |
| `station_b_generator.py` | Lightweight Station B logic generation helper. |
| `ollama_client.py` | Async Ollama HTTP helpers. |
| `station_c_validator.py` | Structural validation for generated plugins. |
| `plugin_template.py` | Base source template used for plugin output. |
| `registry.py` / `plugin_registry.py` | Registry helpers and duplicate awareness. |
| `learning/` | Dataset and learning collection hooks. |

## Ollama Requirements

The default runner configuration uses:

```text
llama3.1:8b
```

Start Ollama in one terminal:

```bash
ollama serve
```

Then run the factory from the parent Francis project in another terminal:

```bash
cd /home/peppera091/francis
./.venv/bin/python -m factory.factory_runner
```

The runner currently uses:

```text
model: llama3.1:8b
temperature: 0.25
max tokens: 1024
timeout: 240 seconds
retries: 1
sleep: 15 seconds
loop: forever
```

These defaults are intentionally conservative for a CPU-bound local Ollama
setup. On machines without GPU acceleration, an 8B model can still take several
minutes per plugin.

## Production Configuration

The runner can be configured with CLI flags or `FRANCIS_FACTORY_*` environment
variables. CLI flags are best for manual runs; the env file is better for a
side-project service.

Print the resolved config without generating anything:

```bash
cd /home/peppera091/francis
./.venv/bin/python -m factory.factory_runner --print-config --once
```

Run one plugin and stop:

```bash
cd /home/peppera091/francis
./.venv/bin/python -m factory.factory_runner --once
```

Run a finite batch:

```bash
cd /home/peppera091/francis
./.venv/bin/python -m factory.factory_runner --max-plugins 3
```

Run continuously with explicit model settings:

```bash
cd /home/peppera091/francis
./.venv/bin/python -m factory.factory_runner \
  --loop \
  --model llama3.1:8b \
  --max-tokens 1024 \
  --timeout-seconds 240 \
  --sleep-seconds 15
```

The example production environment file is:

```text
factory/production.env.example
```

Copy it to `factory/production.env`, tune values, and keep the real env file out
of git.

Important environment variables:

| Variable | Purpose |
| --- | --- |
| `FRANCIS_FACTORY_LOOP` | Run continuously when true. |
| `FRANCIS_FACTORY_MAX_PLUGINS` | Finite batch size. |
| `FRANCIS_FACTORY_SLEEP_SECONDS` | Delay between attempts. |
| `FRANCIS_FACTORY_MODEL` | Ollama model for Station B. |
| `FRANCIS_FACTORY_MAX_TOKENS` | Station B output token cap. |
| `FRANCIS_FACTORY_TIMEOUT_SECONDS` | LLM timeout. |
| `FRANCIS_FACTORY_EVALUATION_ENABLED` | Enables optional Station D evaluation. |
| `FRANCIS_FACTORY_LOG_LEVEL` | Logging level for unattended runs. |

## Side-Project Service

A systemd user service template is included:

```text
factory/ops/francis-factory.service
```

Typical install path:

```bash
mkdir -p ~/.config/systemd/user
cp /home/peppera091/francis/factory/ops/francis-factory.service ~/.config/systemd/user/
systemctl --user daemon-reload
systemctl --user enable francis-factory.service
systemctl --user start francis-factory.service
```

View logs:

```bash
journalctl --user -u francis-factory.service -f
```

Keep Ollama running separately. The service assumes `ollama serve` is already
available on `127.0.0.1:11434`.

## Timeout Behavior

If Station B times out, the factory does not accept fake success for AI roadmap
plugins.

Expected timeout flow:

```text
Factory Station B LLM call timed out
Rejecting AI roadmap plugin because Station B returned fallback output
AI roadmap generation did not produce real model logic; retrying same spec
```

This is good behavior. It means the factory refused to write a placeholder or
fallback plugin and will retry the same roadmap item.

If Ollama eventually returns HTTP 200 with real generated logic, the plugin can
be written and validated.

## Prompt Truncation

Ollama may log something like:

```text
truncating input prompt limit=4096 prompt=4743
```

That means the model context window configured for the running Ollama request is
smaller than the prompt. The current factory keeps Station B output capped at
1024 tokens and passes compact roadmap context to reduce this risk.

If truncation keeps causing poor output:

- reduce handoff/context text
- reduce `llm_max_tokens`
- increase Ollama context length if your machine can handle it
- use a smaller or faster model for local iteration
- keep only the most recent AI roadmap completions in handoff context

## Duplicate Controls

The factory avoids duplicates at multiple levels:

- slug already exists in `plugins/`
- plugin file already exists on disk
- capability signature already exists in registry metadata
- AI roadmap index skips completed roadmap plugins
- Station B receives memory context listing existing plugin slugs
- AI handoff context tells each plugin what prior plugins already own

This means new plugins should be complementary, not renamed duplicates.

## Roadmap Handoffs

AI roadmap plugins are not generated as isolated one-offs. After a plugin
validates, the runner records a completion entry and writes a next directive.

The next plugin receives context like:

```text
Use this to build forward instead of reinventing prior plugins.
Current task must be complementary.
Read previous_results, roadmap_state, progress_state, or completed_plugins when
present.
```

Generated plugins should expose useful output fields that future plugins can
consume, such as:

- `summary`
- `progress_state`
- `recommended_actions`
- `previous_results`
- `user_experience`
- `fun_mode`
- `completed_plugins`
- `roadmap_state`

The point is to create a chain of AI functionality where each plugin adds a new
capability and can use prior work.

## User-Facing Plugin Expectations

Generated AI plugins should be practical for real users, not just internal test
objects. A good plugin should generally provide:

- clear analysis
- direct next actions
- compact progress state
- useful defaults
- safe assumptions
- structured outputs
- a short explanation of what changed or what was found
- optional fun mode or playful user-facing touches when appropriate

Fun features should never replace the core AI capability. They should add a
pleasant user experience layer such as:

- achievement-style progress labels
- friendly task names
- creative prompt variants
- lightweight challenge modes
- interesting summaries
- user-selectable tone or style options

## Station B Prompting Standard

Station B should produce plugin logic that is:

- executable Python
- deterministic
- safe on missing or malformed payload data
- self-contained inside the plugin template
- structured enough for future plugins to consume
- specific to the current AI roadmap capability
- aware of previous roadmap handoffs
- not a duplicate of existing plugin behavior

Station B should not:

- return Markdown
- return explanation instead of code
- import unexpected libraries inside generated logic
- write network-dependent behavior unless the spec requires it
- create random unrelated plugin ideas
- hide timeout fallback output inside a plugin
- regenerate a prior plugin with new wording

## Running One Production Session

1. Start Ollama:

```bash
ollama serve
```

2. Confirm the model is available:

```bash
ollama list
```

3. Run the factory:

```bash
cd /home/peppera091/francis
./.venv/bin/python -m factory.factory_runner
```

4. Watch for these successful log lines:

```text
Proposed PluginSpec
HTTP Request: POST http://127.0.0.1:11434/api/chat "HTTP/1.1 200 OK"
Station B generation completed
Plugin built
Plugin validation OK
AI roadmap handoff updated
```

5. Stop with `Ctrl+C` when you have enough output.

## Locking

The runner writes a process lock at:

```text
/home/peppera091/francis/.factory_runner.lock
```

This prevents accidentally running multiple autonomous factories at once. If the
runner says another factory is active, check whether that PID is still running
before deleting the lock.

## Troubleshooting

### It Looks Frozen

If the terminal stops after `Proposed PluginSpec`, the model is probably still
generating. On CPU-only Ollama, the first model load and a single plugin request
can take several minutes.

Check the Ollama terminal for:

```text
POST /api/chat
loading model
truncating input prompt
```

### Station B Times Out

Timeouts are expected on slower hardware. The factory should retry and reject
fallback output. If every attempt times out, reduce prompt/context size or use a
faster local model.

### A Plugin Was Built After a Timeout

This is only acceptable if the final attempt returned a real model response.
The AI roadmap fallback rejection exists to prevent timeout placeholders from
being written as successful plugins.

### It Keeps Proposing the Same Plugin

That usually means the current roadmap item timed out or failed before it could
be written and recorded. The runner intentionally retries the same spec until it
gets real logic or you stop it.

### It Skips a Plugin

The runner skips a plugin when the slug, file, or capability signature already
exists. This protects the library from duplicates.

## Development Notes

Keep factory changes focused on production quality:

- improve specs in `spec_builder.py`
- improve orchestration in `factory_runner.py`
- improve prompt boundaries in Station B
- improve validation in Station C
- improve duplicate screening before model calls
- improve handoff state so generated plugins compose better

Avoid broad rewrites unless the station boundary genuinely needs to change.

Run the focused sidecar tests from the parent Francis project:

```bash
cd /home/peppera091/francis
./.venv/bin/python -m unittest discover -s factory/tests
```

## Git Workflow

The factory repo should track factory code and any intentionally merged plugin
library content from:

```text
git@github.com:Ap3pp3rs94/Auto-Generated-Plugins.git
```

Useful commands:

```bash
cd /home/peppera091/francis/factory
git status --short --branch
git remote -v
git log --oneline --decorate -5
```

Push factory changes with:

```bash
git push origin main
```

Do not push to any unrelated Francis application remote unless that is the
explicit task.

## Current Production Philosophy

This factory should behave like a careful autonomous plugin line:

- deterministic enough to audit
- flexible enough to keep expanding
- strict enough to reject bad model output
- aware enough to avoid duplicates
- user-focused enough to make plugins enjoyable
- structured enough that future plugins can build on previous plugins

The target is not "many files fast." The target is a growing AI plugin library
that gets more capable over time without drifting into random output.
