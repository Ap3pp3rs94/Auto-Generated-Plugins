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
template. The first generated body was structurally valid but too shallow, so
the semantic-depth gate repaired it into value-dependent logic before packaging.

```python
task_preview = str(payload_data.get('task') or payload_data.get('objective') or payload_data.get('prompt'))[:180]
objective_preview = str(payload_data.get('objective') or goal)[:180]
blocker_preview = str((payload_data.get('blocked_steps') or missing_keys[:2])[0])[:160]

primary_insights.append({
    'title': 'Capability focus',
    'detail': 'Apply ' + plugin_name + ' to: ' + task_preview,
    'domain': domain
})
primary_insights.append({
    'title': 'Available context',
    'detail': 'Use objective: ' + objective_preview,
    'fields': present_keys
})
primary_insights.append({
    'title': 'Key blocker or uncertainty',
    'detail': blocker_preview
})

recommended_actions.append({
    'action': 'Define the next AI workflow step for ' + task_preview,
    'why': 'Keeps autonomous progress concrete and testable.'
})
recommended_actions.append({
    'action': 'Separate blocking work around ' + blocker_preview + ' from parallel work',
    'why': 'Prevents duplicated agent effort and drift.'
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

Semantic-depth result:

```text
semantic_depth: payload values influenced decision fields
```

## Why This Plugin Stayed

This plugin is retained because it satisfies the current library rules:

- AI-specific capability
- deterministic Python output
- structured result shape
- semantic-depth gate passes on contrasting payloads
- user-facing progress and next actions
- optional fun mode that does not replace the serious recommendation
- no legacy random sales/data plugin behavior
- passes Station C validation
