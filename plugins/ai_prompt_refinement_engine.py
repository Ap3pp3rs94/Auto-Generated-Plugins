from __future__ import annotations

"""
Auto-generated Francis AI capability module.

THIS FILE IS GENERATED. Manual edits may be overwritten by the factory.

Capability: AI Prompt Refinement Engine 000001
Slug: ai_prompt_refinement_engine
"""

from typing import Any, Dict, Optional

__all__ = ["invoke", "_run_core_logic", "SkillContext"]

_PLUGIN_NAME: str = 'AI Prompt Refinement Engine 000001'
_PLUGIN_SLUG: str = 'ai_prompt_refinement_engine'
_PLUGIN_CATEGORY: str = 'ai_prompting'
_PLUGIN_VERSION: str = '0.1.0'
_PLUGIN_GOAL: str = 'Analyze task instructions and produce clearer, safer, more testable prompts.'
_PLUGIN_TAGS = ['ai', 'prompting', 'instructions', 'quality', 'autonomous_factory', 'ai_progress']
_PLUGIN_OWNER_ID = 'francis-factory'
_PLUGIN_CAPABILITY_TYPE = 'enrichment'
_PLUGIN_INTENDED_DOMAIN = 'AI prompt engineering and instruction quality'
_PLUGIN_USE_CASES = ['Rewrite vague prompts into specific, testable instructions.', 'Identify missing constraints, inputs, outputs, and acceptance criteria.', 'Suggest prompt variants for different model sizes or latency budgets.', 'Show a compact progress state for this AI capability during baseline capability.', 'Return user-facing guidance that is useful, concise, and safe to act on.', 'Avoid duplicating existing AI capability behavior; identify what is unique about this capability.']
_PLUGIN_RESULT_SCHEMA_VERSION: str = "1.0.0"
_PLUGIN_MANIFEST = {'name': 'AI Prompt Refinement Engine 000001', 'slug': 'ai_prompt_refinement_engine', 'goal': 'Analyze task instructions and produce clearer, safer, more testable prompts.', 'category': 'ai_prompting', 'tags': ['ai', 'prompting', 'instructions', 'quality', 'autonomous_factory', 'ai_progress'], 'version': '0.1.0', 'capability_type': 'enrichment', 'intended_domain': 'AI prompt engineering and instruction quality', 'owner_id': 'francis-factory', 'use_cases': ['Rewrite vague prompts into specific, testable instructions.', 'Identify missing constraints, inputs, outputs, and acceptance criteria.', 'Suggest prompt variants for different model sizes or latency budgets.', 'Show a compact progress state for this AI capability during baseline capability.', 'Return user-facing guidance that is useful, concise, and safe to act on.', 'Avoid duplicating existing AI capability behavior; identify what is unique about this capability.'], 'schema_version': '1.0.0'}
_PLUGIN_DEFAULT_CONFIG: Dict[str, Any] = {}

try:
    from learning_manager import load_plugin_profile as _load_plugin_profile  # type: ignore
except (ImportError, ModuleNotFoundError):
    _load_plugin_profile = None  # type: ignore[assignment]


class SkillContext:
    def __init__(
        self,
        *,
        user_id: str,
        run_id: Optional[str],
        plugin_slug: str,
        plugin_name: str,
        learning_profile: Optional[Dict[str, Any]] = None,
        logger: Optional[Any] = None,
        brain: Optional[Any] = None,
    ) -> None:
        self.user_id = user_id
        self.run_id = run_id
        self.plugin_slug = plugin_slug
        self.plugin_name = plugin_name
        self.learning_profile: Dict[str, Any] = learning_profile or {}
        self.logger = logger
        self.brain = brain

    def _log(self, level: str, message: str, **fields: Any) -> None:
        if self.logger is None:
            return
        try:
            log_fn = getattr(self.logger, level, None)
            if callable(log_fn):
                payload = {"message": message, "plugin_slug": self.plugin_slug, "plugin_name": self.plugin_name}
                payload.update(fields)
                log_fn(payload)
        except Exception:
            return

    def log_info(self, message: str, **fields: Any) -> None:
        self._log("info", message, **fields)

    def log_error(self, message: str, **fields: Any) -> None:
        self._log("error", message, **fields)


def _build_effective_config(payload: Dict[str, Any], runtime_config: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    cfg: Dict[str, Any] = dict(_PLUGIN_DEFAULT_CONFIG)
    if isinstance(payload.get("customer_config"), dict):
        cfg.update(payload["customer_config"])
    if isinstance(payload.get("config"), dict):
        cfg.update(payload["config"])
    if isinstance(runtime_config, dict):
        cfg.update(runtime_config)
    return cfg


def _load_learning_profile() -> Dict[str, Any]:
    if _load_plugin_profile is None:
        return {}
    try:
        prof = _load_plugin_profile(_PLUGIN_SLUG)
        return prof if isinstance(prof, dict) else {}
    except Exception:
        return {}


def _run_core_logic(context: SkillContext, payload: Dict[str, Any], config: Dict[str, Any]) -> Dict[str, Any]:
    # === LOGIC START ===
    # Auto-generated readable capability-profile core logic. Edits may be overwritten by the factory.
    try:
        from schema_tools import infer_tabular_schema, pick_numeric_field
    except Exception:  # pragma: no cover
        def infer_tabular_schema(data):
            return {}
        def pick_numeric_field(schema, hints=None):
            return None
    try:
        if hasattr(context, 'log_info'):
            context.log_info('Executing capability-profile core logic.', plugin_slug=_PLUGIN_SLUG)
    except Exception:
        pass
    result = {
        'summary': '',
        'primary_insights': [],
        'recommended_actions': [],
        'scores': {'confidence': 0.0},
        'details': {},
    }
    schema = infer_tabular_schema(payload.get('data') if isinstance(payload, dict) else None)
    try:
        plugin_name = 'AI Prompt Refinement Engine 000001'
        goal = 'Analyze task instructions and produce clearer, safer, more testable prompts.'
        domain = 'AI prompt engineering and instruction quality'
        capability_type = 'enrichment'
        logic_profile_id = 'prompt_refinement_profile'
        generation_note = 'capability profile registry override'
        use_cases = ['Rewrite vague prompts into specific, testable instructions.', 'Identify missing constraints, inputs, outputs, and acceptance criteria.', 'Suggest prompt variants for different model sizes or latency budgets.', 'Show a compact progress state for this AI capability during baseline capability.', 'Return user-facing guidance that is useful, concise, and safe to act on.', 'Avoid duplicating existing AI capability behavior; identify what is unique about this capability.']
        payload_data = payload if isinstance(payload, dict) else {}
        payload_warnings = [] if isinstance(payload, dict) else ['payload was not a dict; using empty payload']
        task_text = str(payload_data.get('task') or '').strip()
        explicit_objective_text = str(payload_data.get('objective') or '').strip()
        def_text = str(task_text or explicit_objective_text or payload_data.get('prompt') or goal).strip()
        objective_text = str(explicit_objective_text or goal).strip()
        constraints = payload_data.get('constraints') if isinstance(payload_data.get('constraints'), list) else []
        messages = payload_data.get('messages') if isinstance(payload_data.get('messages'), list) else []
        candidate_outputs = payload_data.get('candidate_outputs') if isinstance(payload_data.get('candidate_outputs'), list) else []
        source_notes = payload_data.get('source_notes') if isinstance(payload_data.get('source_notes'), list) else []
        raw_prompt = str(payload_data.get('prompt') or payload_data.get('instruction') or def_text).strip()
        prompt_lower = raw_prompt.lower()
        vague_markers = ['make it better', 'good', 'nice', 'stuff', 'something', 'things', 'fix it', 'do it', 'help me']
        identified_vagueness = [marker for marker in vague_markers if marker in prompt_lower]
        if raw_prompt and len(raw_prompt.split()) < 8:
            identified_vagueness.append('too short to communicate constraints')
        missing_constraints = []
        if not explicit_objective_text:
            missing_constraints.append({'category': 'objective', 'suggestion': 'State the concrete outcome.'})
        if not payload_data.get('audience') and not payload_data.get('user_level'):
            missing_constraints.append({'category': 'audience', 'suggestion': 'Name the target audience or operator.'})
        if not payload_data.get('output_format') and not payload_data.get('format'):
            missing_constraints.append({'category': 'format', 'suggestion': 'Specify required sections or schema.'})
        if not constraints:
            missing_constraints.append({'category': 'acceptance_criteria', 'suggestion': 'Add success criteria and hard constraints.'})
        if 'verify' not in prompt_lower and 'test' not in prompt_lower:
            missing_constraints.append({'category': 'verification', 'suggestion': 'Say how the output should be checked.'})
        refined_prompt = 'Task: ' + def_text + '\nObjective: ' + (explicit_objective_text or 'define the concrete outcome before execution') + '\nAudience: ' + str(payload_data.get('audience') or payload_data.get('user_level') or 'intended user') + '\nOutput format: ' + str(payload_data.get('output_format') or payload_data.get('format') or 'structured checklist') + '\nConstraints: ' + ('; '.join(str(item) for item in constraints) if constraints else 'list assumptions, include acceptance criteria, include verification') + '\nOriginal request: ' + raw_prompt
        rewrites = [
            {'label': 'structured_refinement', 'rewrite': refined_prompt},
            {'label': 'strict_execution', 'rewrite': refined_prompt + '\nDo not begin until missing inputs are listed.'},
            {'label': 'clarifying_mode', 'rewrite': 'Ask only for missing objective, audience, format, constraints, or verification before answering: ' + raw_prompt},
        ]
        verification_checklist = [
            'Objective is explicit',
            'Audience is named',
            'Output format is specified',
            'Acceptance criteria are testable',
            'Verification method is included',
        ]
        specificity = round(max(0.1, 0.95 - 0.09 * len(missing_constraints) - 0.07 * len(identified_vagueness)), 2)
        result['summary'] = plugin_name + ': refined a prompt and produced ' + str(len(rewrites)) + ' concrete rewrite(s).'
        result['primary_insights'] = [
            {'title': 'Vague phrases', 'detail': identified_vagueness},
            {'title': 'Missing constraints', 'detail': missing_constraints},
            {'title': 'Refined prompt', 'detail': refined_prompt},
            {'title': 'Verification checklist', 'detail': verification_checklist},
        ]
        result['recommended_actions'] = [
            {'action': 'Use structured rewrite', 'rewrite': rewrites[0]['rewrite']},
            {'action': 'Resolve missing constraints', 'items': missing_constraints},
            {'action': 'Choose execution mode', 'modes': [item['label'] for item in rewrites]},
            {'action': 'Run verification checklist', 'items': verification_checklist},
        ]
        result['scores'] = {'confidence': round(0.55 + min(0.35, len(raw_prompt.split()) / 80), 2), 'usefulness': 0.93, 'specificity': specificity, 'rewrite_count': len(rewrites), 'risk': round(1 - specificity, 2)}
        result['details'] = {'original_prompt': raw_prompt, 'identified_vagueness': identified_vagueness, 'missing_constraints': missing_constraints, 'rewrites': rewrites, 'refined_prompt': refined_prompt, 'verification_checklist': verification_checklist, 'rewrite_modes': [item['label'] for item in rewrites], 'constraint_count': len(constraints), 'missing_inputs': [item['category'] for item in missing_constraints]}
        result['details']['use_cases'] = use_cases
        result['details']['generation_note'] = generation_note
        result['details']['capability_type'] = capability_type
        result['details']['logic_profile_id'] = logic_profile_id
        result['details']['payload_warnings'] = payload_warnings
        result['progress_state'] = {
            'current_stage': logic_profile_id,
            'next_step': 'Use structured rewrite',
            'blockers': result['details'].get('missing_inputs', [])[:4],
            'done_signals': ['capability_specific_analysis_complete', logic_profile_id],
        }
        result['user_experience'] = {
            'plain_language_takeaway': result['summary'],
            'beginner_tip': 'Use the first recommendation as the next concrete step.',
            'power_user_tip': 'Pass details and scores into the next AI capability module.',
            'interaction_suggestions': [item.get('action', str(item)) for item in result.get('recommended_actions', [])[:3]],
        }
        result['fun_mode'] = {
            'challenge_label': plugin_name,
            'score_badge': 'Strong Signal' if result.get('scores', {}).get('confidence', 0) >= 0.65 else 'Needs Context',
            'microcopy': result['summary'],
            'optional_next_challenge': 'Use structured rewrite',
        }
    except Exception as _exc:
        result = {
            'summary': 'Capability profile failed; fallback applied.',
            'primary_insights': [],
            'recommended_actions': ['Review payload and capability profile.'],
            'scores': {'confidence': 0.0},
            'details': {'error': str(_exc), 'logic_profile_id': 'capability_profile_error'},
        }
    if not isinstance(result, dict):
        result = {'summary': 'Capability profile returned non-dict output.', 'primary_insights': [], 'recommended_actions': [], 'scores': {'confidence': 0.0}, 'details': {}}
    result.setdefault('summary', 'Capability profile completed.')
    result.setdefault('primary_insights', [])
    result.setdefault('recommended_actions', [])
    result.setdefault('scores', {'confidence': 0.0})
    result.setdefault('details', {})
    if isinstance(result.get('scores'), dict):
        result['scores'].setdefault('confidence', 0.0)
        if 'usefulness' not in result['scores']:
            try:
                result['scores']['usefulness'] = round(min(0.95, max(0.0, float(result['scores'].get('confidence', 0.0)))), 2)
            except Exception:
                result['scores']['usefulness'] = 0.0
    if isinstance(result.get('fun_mode'), dict):
        result['fun_mode'].setdefault('microcopy', result.get('summary', 'Capability profile completed.'))
        result['fun_mode'].setdefault('celebratory_microcopy', result['fun_mode'].get('microcopy', result.get('summary', 'Capability profile completed.')))
    else:
        result['fun_mode'] = {
            'challenge_label': result.get('details', {}).get('logic_profile_id', 'Capability Run') if isinstance(result.get('details'), dict) else 'Capability Run',
            'score_badge': 'Ready',
            'microcopy': result.get('summary', 'Capability profile completed.'),
            'celebratory_microcopy': result.get('summary', 'Capability profile completed.'),
        }
    if not isinstance(result.get('diagnostics'), dict):
        result['diagnostics'] = {}
    result['diagnostics'].setdefault('logic_profile_id', result.get('details', {}).get('logic_profile_id', 'capability_profile') if isinstance(result.get('details'), dict) else 'capability_profile')
    return result
# === LOGIC END ===


async def invoke(
    user_id: str,
    payload: Dict[str, Any],
    *,
    run_id: Optional[str] = None,
    brain: Optional[Any] = None,
    logger: Optional[Any] = None,
    config: Optional[Dict[str, Any]] = None,
    **kwargs: Any,
) -> Dict[str, Any]:
    if not isinstance(payload, dict):
        payload = {
            "_value": payload,
            "_payload_warnings": ["payload was not a dict; invoke wrapped it in _value"],
        }
    context = SkillContext(
        user_id=user_id,
        run_id=run_id,
        plugin_slug=_PLUGIN_SLUG,
        plugin_name=_PLUGIN_NAME,
        learning_profile=_load_learning_profile(),
        logger=logger,
        brain=brain,
    )
    status = "failed"
    error_msg = ""
    core_output: Optional[Dict[str, Any]] = None
    try:
        core_output = _run_core_logic(context, payload, _build_effective_config(payload, config))
        if not isinstance(core_output, dict):
            raise TypeError("_run_core_logic must return a dict")
        status = "succeeded"
    except Exception as exc:
        context.log_error("Core logic raised an exception.", error=str(exc), exception_type=type(exc).__name__)
        error_msg = str(exc)
    meta = {
        "plugin_name": _PLUGIN_NAME,
        "plugin_slug": _PLUGIN_SLUG,
        "plugin_category": _PLUGIN_CATEGORY,
        "plugin_version": _PLUGIN_VERSION,
        "user_id": user_id,
        "run_id": run_id,
        "owner_id": _PLUGIN_OWNER_ID,
        "capability_type": _PLUGIN_CAPABILITY_TYPE,
        "intended_domain": _PLUGIN_INTENDED_DOMAIN,
        "schema_version": _PLUGIN_RESULT_SCHEMA_VERSION,
        "plugin_manifest": _PLUGIN_MANIFEST,
    }
    return {"status": status, "output": core_output if status == "succeeded" else None, "error": error_msg, "meta": meta}
