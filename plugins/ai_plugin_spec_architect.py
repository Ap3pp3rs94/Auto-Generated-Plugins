from __future__ import annotations

"""
Auto-generated Francis plugin module.

THIS FILE IS GENERATED. Manual edits may be overwritten by the factory.

Plugin: AI Plugin Spec Architect
Slug: ai_plugin_spec_architect
"""

from typing import Any, Dict, Optional

__all__ = ["invoke", "_run_core_logic", "SkillContext"]

_PLUGIN_NAME: str = 'AI Plugin Spec Architect'
_PLUGIN_SLUG: str = 'ai_plugin_spec_architect'
_PLUGIN_CATEGORY: str = 'ai_plugin_factory'
_PLUGIN_VERSION: str = '0.1.0'
_PLUGIN_GOAL: str = 'Design precise, non-duplicate PluginSpecs for new AI plugins before generation starts.'
_PLUGIN_TAGS = ['ai', 'plugins', 'specs', 'factory', 'autonomous_factory', 'ai_progress', 'phase_1']
_PLUGIN_OWNER_ID = 'francis-factory'
_PLUGIN_CAPABILITY_TYPE = 'enrichment'
_PLUGIN_INTENDED_DOMAIN = 'AI plugin specification design and capability boundaries'
_PLUGIN_USE_CASES = ['Turn a loose plugin idea into a complete PluginSpec blueprint.', 'Define capability boundaries so the plugin does not duplicate existing plugins.', 'List required inputs, outputs, acceptance criteria, and quality signals before build.', 'Show a compact progress state for this AI capability during baseline capability.', 'Return user-facing guidance that is useful, concise, and safe to act on.', 'Avoid duplicating existing AI plugin behavior; identify what is unique about this capability.']
_PLUGIN_RESULT_SCHEMA_VERSION: str = "1.0.0"
_PLUGIN_MANIFEST = {'name': 'AI Plugin Spec Architect', 'slug': 'ai_plugin_spec_architect', 'goal': 'Design precise, non-duplicate PluginSpecs for new AI plugins before generation starts.', 'category': 'ai_plugin_factory', 'tags': ['ai', 'plugins', 'specs', 'factory', 'autonomous_factory', 'ai_progress', 'phase_1'], 'version': '0.1.0', 'capability_type': 'enrichment', 'intended_domain': 'AI plugin specification design and capability boundaries', 'owner_id': 'francis-factory', 'use_cases': ['Turn a loose plugin idea into a complete PluginSpec blueprint.', 'Define capability boundaries so the plugin does not duplicate existing plugins.', 'List required inputs, outputs, acceptance criteria, and quality signals before build.', 'Show a compact progress state for this AI capability during baseline capability.', 'Return user-facing guidance that is useful, concise, and safe to act on.', 'Avoid duplicating existing AI plugin behavior; identify what is unique about this capability.'], 'schema_version': '1.0.0'}
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
        plugin_name = 'AI Plugin Spec Architect'
        goal = 'Design precise, non-duplicate PluginSpecs for new AI plugins before generation starts.'
        domain = 'AI plugin specification design and capability boundaries'
        capability_type = 'enrichment'
        logic_profile_id = 'plugin_spec_architect_profile'
        generation_note = 'capability profile registry override'
        use_cases = ['Turn a loose plugin idea into a complete PluginSpec blueprint.', 'Define capability boundaries so the plugin does not duplicate existing plugins.', 'List required inputs, outputs, acceptance criteria, and quality signals before build.', 'Show a compact progress state for this AI capability during baseline capability.', 'Return user-facing guidance that is useful, concise, and safe to act on.', 'Avoid duplicating existing AI plugin behavior; identify what is unique about this capability.']
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
        factory_surface = ' '.join([
            def_text,
            objective_text,
            str(payload_data.get('prompt') or ''),
            ' '.join(str(item) for item in constraints),
            ' '.join(str(item) for item in source_notes),
            ' '.join(str(item) for item in candidate_outputs),
        ]).lower()
        existing_plugins = payload_data.get('existing_plugins') if isinstance(payload_data.get('existing_plugins'), list) else []
        quality_failures = payload_data.get('quality_failures') if isinstance(payload_data.get('quality_failures'), list) else []
        desired_plugin = str(payload_data.get('plugin_name') or payload_data.get('slug') or def_text[:80]).strip()
        factory_signals = []
        for label, terms in [
            ('spec_design', ['spec', 'blueprint', 'requirements', 'inputs', 'outputs', 'acceptance']),
            ('logic_design', ['logic', 'algorithm', 'deterministic', 'scoring', 'payload', 'implementation']),
            ('quality_gate', ['quality', 'semantic', 'validation', 'reject', 'pass', 'fail']),
            ('testing', ['test', 'probe', 'edge', 'regression', 'payload']),
            ('duplicate_control', ['duplicate', 'overlap', 'unique', 'random', 'merge']),
            ('repair', ['repair', 'weak', 'shallow', 'missing', 'failed']),
            ('release', ['github', 'commit', 'push', 'release', 'rollback']),
            ('backlog', ['roadmap', 'backlog', 'next', 'priority', 'dependency']),
        ]:
            hits = [term for term in terms if term in factory_surface]
            if hits:
                factory_signals.append({'category': label, 'signals': hits})
        primary_signal = factory_signals[0]['category'] if factory_signals else 'plugin_creation'
        plugin_keywords = sorted(set(
            word.strip('.,:;!?').lower()
            for word in factory_surface.split()
            if len(word.strip('.,:;!?')) > 6
        ))[:14]
        domain_signals = []
        for label, terms in [
            ('release_auth_plugin', ['auth', 'login', 'database', 'migration', 'rollback', 'production']),
            ('grounded_medical_plugin', ['medical', 'clinical', 'citation', 'source', 'unsupported', 'claim']),
            ('tool_trace_plugin', ['tool', 'trace', 'retrieval', 'mismatch', 'consistency']),
        ]:
            hits = [term for term in terms if term in factory_surface]
            if hits:
                domain_signals.append({'category': label, 'signals': hits})
        domain_signal_count = sum(len(item['signals']) for item in domain_signals)

        if logic_profile_id == 'plugin_spec_architect_profile':
            spec_blueprint = {
                'name': desired_plugin,
                'category': 'ai_plugin_factory',
                'goal': 'Create a focused plugin for ' + desired_plugin,
                'required_inputs': ['task', 'objective', 'constraints', 'existing_plugins'],
                'required_outputs': ['summary', 'primary_insights', 'recommended_actions', 'scores', 'details'],
                'acceptance_criteria': ['unique capability boundary', 'capability-specific details', 'semantic probe passes'],
            }
            uniqueness_checks = ['Compare slug and family_key with existing_plugins', 'Reject broad names that duplicate current roadmap', 'Require one unique output detail key']
            capability_boundaries = ['State what this plugin owns', 'State adjacent plugins it must not duplicate', 'Define handoff fields for downstream plugins']
            prompt_requirements = ['Goal must name the concrete capability', 'Use cases must be observable', 'Outputs must include machine-readable details']
            details_payload = {'spec_blueprint': spec_blueprint, 'uniqueness_checks': uniqueness_checks, 'capability_boundaries': capability_boundaries, 'prompt_requirements': prompt_requirements}
            next_step = 'Draft PluginSpec blueprint for ' + desired_plugin
        elif logic_profile_id == 'plugin_logic_blueprint_designer_profile':
            logic_blueprint = [
                {'phase': 'extract', 'rule': 'Read payload values for ' + desired_plugin},
                {'phase': 'analyze', 'rule': 'Compute capability-specific signals from ' + ', '.join(plugin_keywords[:5])},
                {'phase': 'construct', 'rule': 'Populate output fields from analysis, not constants'},
            ]
            deterministic_rules = ['No external calls', 'No file mutation', 'Scores derive from observed signals', 'Actions include payload-specific targets']
            data_flow = {'inputs': ['payload', 'config', 'context'], 'analysis': plugin_keywords[:8], 'outputs': ['insights', 'actions', 'scores', 'details']}
            failure_modes = ['constant recommendations', 'metadata-only relabeling', 'same scores for divergent payloads']
            details_payload = {'logic_blueprint': logic_blueprint, 'deterministic_rules': deterministic_rules, 'data_flow': data_flow, 'failure_modes': failure_modes}
            next_step = 'Implement deterministic logic blueprint for ' + desired_plugin
        elif logic_profile_id == 'plugin_quality_gate_designer_profile':
            quality_gates = ['structural import and invoke', 'required detail keys', 'semantic depth divergence', 'profile-specific probe']
            rejection_rules = ['Reject missing required outputs', 'Reject profile mismatch', 'Reject high similarity across probe payloads', 'Reject legacy semantic_repair bodies']
            semantic_probes = [
                {'name': 'release_sensitive_payload', 'signals': ['auth', 'rollback', 'database']},
                {'name': 'grounding_sensitive_payload', 'signals': ['citation', 'medical', 'unsupported']},
            ]
            pass_criteria = ['decision fields reflect payload tokens', 'scores differ across probes', 'details include capability-specific keys']
            details_payload = {'quality_gates': quality_gates, 'rejection_rules': rejection_rules, 'semantic_probes': semantic_probes, 'pass_criteria': pass_criteria}
            next_step = 'Add quality gates before accepting ' + desired_plugin
        elif logic_profile_id == 'plugin_test_payload_generator_profile':
            test_payloads = [
                {'name': 'happy_path', 'payload': {'task': desired_plugin, 'constraints': constraints[:3], 'existing_plugins': existing_plugins[:5]}},
                {'name': 'semantic_contrast', 'payload': {'task': 'release-sensitive auth plugin', 'objective': 'rollback-safe generation'}},
                {'name': 'adversarial_shallow', 'payload': {'task': 'make it better', 'objective': '', 'constraints': []}},
            ]
            edge_cases = ['missing objective', 'duplicate existing plugin', 'empty candidate output', 'high-risk release wording']
            expected_differences = ['summary names different risk domain', 'actions target different payload values', 'scores change when evidence changes']
            regression_watchlist = ['constant fun_mode only', 'details-only echoing', 'same action labels for every payload']
            details_payload = {'test_payloads': test_payloads, 'edge_cases': edge_cases, 'expected_differences': expected_differences, 'regression_watchlist': regression_watchlist}
            next_step = 'Run generated semantic probe payloads'
        elif logic_profile_id == 'plugin_duplicate_detector_profile':
            duplicate_risks = []
            for existing in existing_plugins[:12]:
                existing_text = str(existing).lower()
                overlap = [word for word in plugin_keywords[:10] if word in existing_text]
                if overlap:
                    duplicate_risks.append({'existing_plugin': str(existing)[:160], 'overlap_terms': overlap})
            uniqueness_fingerprint = sorted(set(plugin_keywords + [primary_signal, logic_profile_id]))[:16]
            comparison_targets = existing_plugins[:8]
            merge_or_reject_decision = 'redesign' if duplicate_risks else 'unique_enough_to_build'
            details_payload = {'duplicate_risks': duplicate_risks, 'uniqueness_fingerprint': uniqueness_fingerprint, 'comparison_targets': comparison_targets, 'merge_or_reject_decision': merge_or_reject_decision}
            next_step = 'Apply duplicate decision: ' + merge_or_reject_decision
        elif logic_profile_id == 'plugin_repair_strategy_planner_profile':
            weak_signals = []
            for item in quality_failures + candidate_outputs:
                text = str(item).lower()
                hits = [term for term in ['missing', 'semantic', 'shallow', 'similar', 'profile', 'runtime', 'failed'] if term in text]
                if hits:
                    weak_signals.append({'signals': hits, 'evidence': str(item)[:180]})
            capability_specific_targets = ['replace generic output keys', 'add profile-specific analyzer', 'make scores vary with payload values', 'add repair acceptance checks']
            repair_plan = [
                {'step': 1, 'action': 'Classify weak signals', 'signals': weak_signals[:5]},
                {'step': 2, 'action': 'Patch capability profile for ' + desired_plugin, 'targets': capability_specific_targets},
                {'step': 3, 'action': 'Repair only if validation and semantic depth pass'},
            ]
            acceptance_checks = ['required keys present', 'semantic probes pass', 'full quality audit clean', 'GitHub push only after repair']
            details_payload = {'repair_plan': repair_plan, 'weak_signals': weak_signals, 'capability_specific_targets': capability_specific_targets, 'acceptance_checks': acceptance_checks}
            next_step = 'Patch capability profile for ' + desired_plugin
        elif logic_profile_id == 'plugin_release_packager_profile':
            validation_summary = {'quality_failures': len(quality_failures), 'candidate_count': len(candidate_outputs), 'signals': factory_signals}
            release_package = {'title': desired_plugin, 'summary': 'Package generated plugin with validation evidence', 'files': payload_data.get('files', []), 'notes': source_notes[:5]}
            github_publish_plan = ['stage plugin and profile files', 'commit with validation summary', 'push origin main after gates pass']
            rollback_notes = ['keep backup in quality_backups', 'do not publish failed candidates', 're-run quality runner before restart']
            details_payload = {'release_package': release_package, 'validation_summary': validation_summary, 'github_publish_plan': github_publish_plan, 'rollback_notes': rollback_notes}
            next_step = 'Prepare GitHub release package for ' + desired_plugin
        else:
            backlog_items = [
                {'slug_hint': 'ai_plugin_spec_architect', 'priority': 1, 'why': 'improves future specs'},
                {'slug_hint': 'ai_plugin_quality_gate_designer', 'priority': 2, 'why': 'prevents shallow acceptance'},
                {'slug_hint': 'ai_plugin_repair_strategy_planner', 'priority': 3, 'why': 'recovers weak generated plugins'},
            ]
            priority_rationale = ['Factory leverage first', 'Quality before speed', 'No duplicate or random plugin ideas']
            dependency_order = ['spec', 'logic_blueprint', 'quality_gate', 'test_payloads', 'duplicate_check', 'repair', 'release']
            next_plugin_specs = [item['slug_hint'] for item in backlog_items]
            details_payload = {'backlog_items': backlog_items, 'priority_rationale': priority_rationale, 'dependency_order': dependency_order, 'next_plugin_specs': next_plugin_specs}
            next_step = 'Build the highest-leverage plugin factory backlog item'

        result['summary'] = plugin_name + ': created plugin-factory guidance for ' + desired_plugin + ' using focus ' + primary_signal + '.'
        result['primary_insights'] = [
            {'title': 'Factory signals', 'detail': factory_signals or primary_signal},
            {'title': 'Domain signals', 'detail': domain_signals or 'No domain-specific plugin risk signal detected.'},
            {'title': 'Plugin keywords', 'detail': plugin_keywords},
            {'title': 'Profile output', 'detail': details_payload},
        ]
        result['recommended_actions'] = [
            {'action': next_step, 'profile_id': logic_profile_id, 'signals': factory_signals},
            {'action': 'Reject random or duplicate plugin work', 'existing_plugins_checked': len(existing_plugins)},
            {'action': 'Verify with quality runner before publish', 'quality_failures_seen': len(quality_failures)},
        ]
        signal_count = sum(len(item['signals']) for item in factory_signals)
        result['scores'] = {'confidence': round(min(0.92, 0.44 + 0.03 * len(plugin_keywords) + 0.025 * signal_count + 0.013 * domain_signal_count), 2), 'factory_leverage': round(min(0.95, 0.5 + 0.06 * len(details_payload) + 0.02 * signal_count + 0.01 * domain_signal_count), 2), 'duplicate_risk': round(min(0.9, 0.08 * len(existing_plugins) + 0.06 * len(details_payload.get('duplicate_risks', []))), 2), 'domain_signal_count': domain_signal_count, 'risk': round(min(0.9, 0.16 + 0.04 * len(quality_failures) + 0.04 * len(details_payload.get('duplicate_risks', [])) + 0.025 * domain_signal_count), 2)}
        details_payload['factory_signals'] = factory_signals
        details_payload['domain_signals'] = domain_signals
        details_payload['plugin_keywords'] = plugin_keywords
        details_payload['missing_inputs'] = ['plugin_name or task'] if not desired_plugin else []
        result['details'] = details_payload
        result['details']['use_cases'] = use_cases
        result['details']['generation_note'] = generation_note
        result['details']['capability_type'] = capability_type
        result['details']['logic_profile_id'] = logic_profile_id
        result['details']['payload_warnings'] = payload_warnings
        result['progress_state'] = {
            'current_stage': logic_profile_id,
            'next_step': next_step,
            'blockers': result['details'].get('missing_inputs', [])[:4],
            'done_signals': ['capability_specific_analysis_complete', logic_profile_id],
        }
        result['user_experience'] = {
            'plain_language_takeaway': result['summary'],
            'beginner_tip': 'Use the first recommendation as the next concrete step.',
            'power_user_tip': 'Pass details and scores into the next AI capability plugin.',
            'interaction_suggestions': [item.get('action', str(item)) for item in result.get('recommended_actions', [])[:3]],
        }
        result['fun_mode'] = {
            'challenge_label': plugin_name,
            'score_badge': 'Strong Signal' if result.get('scores', {}).get('confidence', 0) >= 0.65 else 'Needs Context',
            'microcopy': result['summary'],
            'optional_next_challenge': next_step,
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
        payload = {"_value": payload}
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
