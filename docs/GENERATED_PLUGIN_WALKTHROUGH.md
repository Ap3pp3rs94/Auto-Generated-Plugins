# Generated Plugin Walkthrough

This walkthrough shows the first plugin kept in this curated library:

```text
plugins/ai_prompt_refinement_engine.py
```

It was generated under the AI roadmap guide, validated by Station C, and kept as
the seed artifact for the plugin library.

## Spec

```text
Name: AI Prompt Refinement Engine
Slug: ai_prompt_refinement_engine
Category: ai_prompting
Capability: enrichment
Domain: AI prompt engineering and instruction quality
Goal: Analyze task instructions and produce clearer, safer, more testable prompts.
```

Primary use cases:

- Rewrite vague prompts into specific, testable instructions.
- Identify missing constraints, inputs, outputs, and acceptance criteria.
- Suggest prompt variants for different model sizes or latency budgets.
- Return progress state and user-facing guidance.
- Avoid duplicating existing AI plugin behavior.

## Generated Body Excerpt

Station B generated a Python logic body that is injected into the plugin
template. The plugin stores the generated body in an encoded envelope plus a
plain preview for inspection.

```python
# Validate payload is a dict and collect relevant fields
if not isinstance(payload, dict):
    result['summary'] = 'Invalid input: Payload must be a dictionary.'
else:
    task = payload.get('task')
    objective = payload.get('objective')
    prompt = payload.get('prompt')
    messages = payload.get('messages', [])
    candidate_outputs = payload.get('candidate_outputs', [])

# Build evidence notes from present fields
evidence_notes = []
if task:
    evidence_notes.append({'field': 'Task', 'value': task})
if objective:
    evidence_notes.append({'field': 'Objective', 'value': objective})
if prompt:
    evidence_notes.append({'field': 'Prompt', 'value': prompt})

# Create primary insights specific to this plugin goal
primary_insights = []
if not messages:
    primary_insights.append('No conversation history found.')
if candidate_outputs and len(candidate_outputs) > 1:
    primary_insights.append('Multiple model outputs detected.')

# Create recommended actions with clear next steps
recommended_actions = []
if task and objective:
    recommended_actions.append({
        'action': 'Rewrite prompt',
        'description': 'Use the task and objective to create a specific, testable instruction.'
    })
```

## Sample Invocation

```python
import asyncio
from plugins.ai_prompt_refinement_engine import invoke

payload = {
    "task": "Create a prompt that asks an AI coding agent to add tests before changing production code.",
    "objective": "Make the instruction specific, safe, and testable.",
    "prompt": "Make this better and don't break stuff.",
    "messages": [],
    "candidate_outputs": [
        {"id": "draft_a", "summary": "Add tests maybe."},
        {"id": "draft_b", "summary": "Write tests first, then implement."},
    ],
}

result = asyncio.run(invoke("demo-user", payload, run_id="readme-demo"))
print(result["output"]["summary"])
```

Representative output fields:

```json
{
  "summary": "AI Prompt Refinement Engine: Analyzing task instructions and producing clearer, safer, more testable prompts.",
  "primary_insights": [
    "No conversation history found.",
    "Multiple model outputs detected."
  ],
  "recommended_actions": [
    {
      "action": "Rewrite prompt",
      "description": "Use the task and objective to create a specific, testable instruction."
    },
    {
      "action": "Start conversation",
      "description": "Begin interacting with the model to gather more information."
    }
  ],
  "scores": {
    "confidence": 0.8,
    "usefulness": 0.9
  },
  "progress_state": {
    "current_stage": "Analysis",
    "next_step": "Rewrite prompt",
    "blockers": [],
    "done_signals": []
  },
  "fun_mode": {
    "challenge_label": "Clear Path",
    "score_badge": "Ready to Run"
  }
}
```

## Validation

Station C validates generated plugins before they are kept in the curated
library.

```bash
python - <<'PY'
from pathlib import Path
from station_c_validator import validate_plugin_module

ok, reason = validate_plugin_module(Path("plugins/ai_prompt_refinement_engine.py"))
print(ok)
print(reason)
PY
```

Current result:

```text
True
```

## Why This Plugin Stayed

This plugin is retained because it satisfies the current library rules:

- AI-specific capability
- deterministic Python output
- structured result shape
- user-facing progress and next actions
- optional fun mode that does not replace the serious recommendation
- no legacy random sales/data plugin behavior
- passes Station C validation
