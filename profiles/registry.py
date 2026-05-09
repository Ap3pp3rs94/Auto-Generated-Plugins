from __future__ import annotations

import base64
import re
import textwrap
from typing import Any, Callable, Dict, Optional

try:
    from plugin_spec import PluginSpec
except ImportError:  # pragma: no cover
    from ..plugin_spec import PluginSpec


LOGIC_START = "# === LOGIC START ==="
LOGIC_END = "# === LOGIC END ==="


def _quote(value: Any) -> str:
    return repr(str(value or ""))


def _common_header(
    spec: PluginSpec,
    capability_type: Optional[str],
    profile_id: str,
    reason: str,
) -> str:
    use_cases = [str(item) for item in (getattr(spec, "use_cases", None) or [])[:6]]
    return f"""
plugin_name = {_quote(getattr(spec, "name", "") or "AI Roadmap Plugin")}
goal = {_quote(getattr(spec, "goal", "") or "Improve an AI workflow.")}
domain = {_quote(getattr(spec, "intended_domain", None) or "AI workflow improvement")}
capability_type = {_quote(capability_type or getattr(spec, "capability_type", None) or "data_insight")}
logic_profile_id = {_quote(profile_id)}
generation_note = {_quote(reason or "capability profile registry")}
use_cases = {use_cases!r}
payload_data = payload if isinstance(payload, dict) else {{}}
payload_warnings = [] if isinstance(payload, dict) else ['payload was not a dict; using empty payload']
def_text = str(payload_data.get('task') or payload_data.get('objective') or payload_data.get('prompt') or goal).strip()
objective_text = str(payload_data.get('objective') or goal).strip()
constraints = payload_data.get('constraints') if isinstance(payload_data.get('constraints'), list) else []
messages = payload_data.get('messages') if isinstance(payload_data.get('messages'), list) else []
candidate_outputs = payload_data.get('candidate_outputs') if isinstance(payload_data.get('candidate_outputs'), list) else []
source_notes = payload_data.get('source_notes') if isinstance(payload_data.get('source_notes'), list) else []
""".strip()


def _common_result_footer(next_step_expr: str) -> str:
    return f"""
result['details']['use_cases'] = use_cases
result['details']['generation_note'] = generation_note
result['details']['capability_type'] = capability_type
result['details']['logic_profile_id'] = logic_profile_id
result['details']['payload_warnings'] = payload_warnings
result['progress_state'] = {{
    'current_stage': logic_profile_id,
    'next_step': {next_step_expr},
    'blockers': result['details'].get('missing_inputs', [])[:4],
    'done_signals': ['capability_specific_analysis_complete', logic_profile_id],
}}
result['user_experience'] = {{
    'plain_language_takeaway': result['summary'],
    'beginner_tip': 'Use the first recommendation as the next concrete step.',
    'power_user_tip': 'Pass details and scores into the next AI capability plugin.',
    'interaction_suggestions': [item.get('action', str(item)) for item in result.get('recommended_actions', [])[:3]],
}}
result['fun_mode'] = {{
    'challenge_label': 'Capability Run',
    'score_badge': 'Strong Signal' if result.get('scores', {{}}).get('confidence', 0) >= 0.65 else 'Needs Context',
    'microcopy': 'The result is structured so another agent can pick it up cleanly.',
    'optional_next_challenge': {next_step_expr},
}}
""".strip()


def _task_planner(spec: PluginSpec, capability_type: Optional[str], profile_id: str, reason: str) -> str:
    return f"""
{_common_header(spec, capability_type, profile_id, reason)}
current_plan = payload_data.get('current_plan') if isinstance(payload_data.get('current_plan'), list) else []
completed_steps = payload_data.get('completed_steps') if isinstance(payload_data.get('completed_steps'), list) else []
blocked_steps = payload_data.get('blocked_steps') if isinstance(payload_data.get('blocked_steps'), list) else []
parallel_hints = []
if 'test' in def_text.lower() or 'verify' in objective_text.lower():
    parallel_hints.append('prepare verification while implementation is planned')
if 'file' in def_text.lower() or 'code' in def_text.lower():
    parallel_hints.append('inspect affected files before editing')
sequenced_plan = []
if not objective_text:
    sequenced_plan.append({{'step': 1, 'phase': 'clarify', 'task': 'Define the objective and acceptance criteria.', 'blocking': True}})
sequenced_plan.append({{'step': len(sequenced_plan) + 1, 'phase': 'plan', 'task': 'Break work into implementation, review, and verification checkpoints for ' + def_text[:160], 'blocking': True}})
sequenced_plan.append({{'step': len(sequenced_plan) + 1, 'phase': 'execute', 'task': 'Complete the smallest reversible implementation unit.', 'blocking': False}})
sequenced_plan.append({{'step': len(sequenced_plan) + 1, 'phase': 'verify', 'task': 'Run tests or explicit checks tied to ' + objective_text[:140], 'blocking': True}})
handoff_packet = {{
    'objective': objective_text,
    'completed_steps': completed_steps,
    'blocked_steps': blocked_steps,
    'parallelizable_work': parallel_hints or ['document assumptions', 'prepare verification checklist'],
    'integration_checkpoint': 'Confirm completed work, blockers, changed files, and test evidence before the next agent starts.',
}}
coverage = 0.45 + (0.12 if objective_text else 0) + (0.1 if current_plan else 0) + (0.1 if completed_steps else 0) + (0.08 if blocked_steps else 0) + min(0.1, len(constraints) * 0.03)
result['summary'] = plugin_name + ': built a sequenced AI-agent plan with checkpoints for ' + def_text[:140] + '.'
result['primary_insights'] = [
    {{'title': 'Plan coverage', 'detail': 'Found %d existing plan step(s), %d completed step(s), and %d blocker(s).' % (len(current_plan), len(completed_steps), len(blocked_steps))}},
    {{'title': 'Blocking path', 'detail': blocked_steps[0] if blocked_steps else 'No explicit blocker was provided.'}},
    {{'title': 'Parallel work', 'detail': handoff_packet['parallelizable_work']}},
]
result['recommended_actions'] = [
    {{'action': item['task'], 'phase': item['phase'], 'blocking': item['blocking']}} for item in sequenced_plan
]
result['scores'] = {{'confidence': round(min(0.92, coverage), 2), 'plan_coverage': round(min(1.0, coverage + 0.08), 2), 'handoff_readiness': round(0.55 + min(0.35, len(handoff_packet['parallelizable_work']) * 0.08), 2), 'risk': round(max(0.12, 0.62 - coverage), 2)}}
result['details'] = {{'sequenced_plan': sequenced_plan, 'handoff_packet': handoff_packet, 'missing_inputs': [key for key in ['objective', 'current_plan', 'blocked_steps'] if not payload_data.get(key)]}}
{_common_result_footer("sequenced_plan[0]['task'] if sequenced_plan else 'Define the next planning step.'")}
""".strip()


def _tool_selection(spec: PluginSpec, capability_type: Optional[str], profile_id: str, reason: str) -> str:
    return f"""
{_common_header(spec, capability_type, profile_id, reason)}
text = ' '.join([def_text, objective_text, ' '.join(str(item) for item in constraints)]).lower()
tool_rules = [
    ('code_editor', ['code', 'repo', 'file', 'bug', 'test', 'python', 'javascript'], 'Needed for source inspection or code changes.'),
    ('terminal', ['run', 'command', 'test', 'compile', 'server', 'process'], 'Needed for local verification and process control.'),
    ('web_search', ['latest', 'current', 'price', 'news', 'docs', 'citation'], 'Needed when facts may have changed or sources are required.'),
    ('retrieval', ['search', 'knowledge', 'document', 'notes', 'memory'], 'Needed to find grounding context before generation.'),
    ('planner', ['complex', 'multi-step', 'handoff', 'agent', 'delegate'], 'Needed to sequence work and prevent duplicated effort.'),
]
recommendations = []
for name, keywords, rationale in tool_rules:
    hits = [word for word in keywords if word in text]
    if hits:
        recommendations.append({{'tool': name, 'matched_signals': hits, 'rationale': rationale, 'priority': len(hits)}})
recommendations = sorted(recommendations, key=lambda item: item['priority'], reverse=True)
if not recommendations:
    recommendations.append({{'tool': 'clarifying_prompt', 'matched_signals': [], 'rationale': 'Task lacks enough operational signals to choose a stronger tool.', 'priority': 0}})
rejected_tools = []
if 'external' in text or 'internet' in text:
    rejected_tools.append({{'tool': 'silent_offline_answer', 'reason': 'External grounding was requested or implied.'}})
if 'delete' in text or 'destructive' in text:
    rejected_tools.append({{'tool': 'automatic_mutation', 'reason': 'Potentially destructive actions require explicit confirmation.'}})
selection_confidence = min(0.93, 0.48 + 0.12 * len(recommendations) + 0.03 * sum(len(item['matched_signals']) for item in recommendations))
result['summary'] = plugin_name + ': selected ' + recommendations[0]['tool'] + ' as the first tool for ' + def_text[:140] + '.'
result['primary_insights'] = [
    {{'title': 'Top tool', 'detail': recommendations[0]}},
    {{'title': 'Tool signals', 'detail': [item['matched_signals'] for item in recommendations]}},
    {{'title': 'Rejected tools', 'detail': rejected_tools or 'No explicit rejections.'}},
]
result['recommended_actions'] = [
    {{'action': 'Use ' + item['tool'], 'why': item['rationale'], 'signals': item['matched_signals']}} for item in recommendations[:4]
]
result['scores'] = {{'confidence': round(selection_confidence, 2), 'usefulness': round(min(0.94, 0.55 + 0.1 * len(recommendations)), 2), 'routing_specificity': round(min(1.0, 0.35 + 0.08 * sum(len(item['matched_signals']) for item in recommendations)), 2), 'risk': round(0.22 + 0.08 * len(rejected_tools), 2)}}
result['details'] = {{'tool_recommendations': recommendations, 'rejected_tools': rejected_tools, 'selection_rationale': recommendations[0]['rationale'], 'missing_inputs': ['task'] if not def_text else []}}
{_common_result_footer("'Use ' + recommendations[0]['tool']")}
""".strip()


def _memory_compression(spec: PluginSpec, capability_type: Optional[str], profile_id: str, reason: str) -> str:
    return f"""
{_common_header(spec, capability_type, profile_id, reason)}
raw_items = []
for item in messages + source_notes + candidate_outputs:
    if isinstance(item, dict):
        raw_items.append(str(item.get('content') or item.get('text') or item.get('summary') or item)[:500])
    else:
        raw_items.append(str(item)[:500])
if payload_data.get('previous_results'):
    raw_items.append(str(payload_data.get('previous_results'))[:700])
joined = ' '.join(raw_items).strip()
sentences = [part.strip() for part in joined.replace('\\n', '. ').split('.') if part.strip()]
durable_facts = [sentence for sentence in sentences if any(token in sentence.lower() for token in ['decided', 'completed', 'uses', 'must', 'constraint', 'blocked', 'owner', 'path'])]
open_threads = [sentence for sentence in sentences if any(token in sentence.lower() for token in ['todo', 'next', 'blocked', 'unknown', 'question', 'needs'])]
discard_candidates = [sentence for sentence in sentences if len(sentence.split()) < 4 or sentence.lower() in ['ok', 'thanks', 'done']]
memory_summary = '; '.join((durable_facts or sentences or [def_text])[:4])[:700]
original_tokens = max(1, len(joined) // 4)
compressed_tokens = max(1, len(memory_summary) // 4)
compression_ratio = round(compressed_tokens / original_tokens, 2)
confidence = min(0.92, 0.42 + 0.08 * len(durable_facts[:5]) + 0.05 * len(open_threads[:3]))
result['summary'] = plugin_name + ': compressed context into durable memory with ratio ' + str(compression_ratio) + '.'
result['primary_insights'] = [
    {{'title': 'Memory summary', 'detail': memory_summary}},
    {{'title': 'Durable facts', 'detail': durable_facts[:6]}},
    {{'title': 'Open threads', 'detail': open_threads[:5]}},
]
result['recommended_actions'] = [
    {{'action': 'Persist memory summary', 'memory_summary': memory_summary}},
    {{'action': 'Carry open threads forward', 'open_threads': open_threads[:5]}},
    {{'action': 'Drop low-value chatter', 'discard_candidates': discard_candidates[:5]}},
]
result['scores'] = {{'confidence': round(confidence, 2), 'compression_ratio': compression_ratio, 'retention_value': round(min(0.95, 0.45 + 0.08 * len(durable_facts[:5])), 2), 'risk': round(max(0.12, 0.55 - confidence), 2)}}
result['details'] = {{'memory_summary': memory_summary, 'durable_facts': durable_facts[:10], 'open_threads': open_threads[:10], 'discard_candidates': discard_candidates[:10], 'original_token_estimate': original_tokens, 'compressed_token_estimate': compressed_tokens, 'missing_inputs': ['messages or source_notes'] if not raw_items else []}}
{_common_result_footer("'Persist memory summary'")}
""".strip()


def _context_optimizer(spec: PluginSpec, capability_type: Optional[str], profile_id: str, reason: str) -> str:
    return f"""
{_common_header(spec, capability_type, profile_id, reason)}
token_budget = int(payload_data.get('token_budget') or payload_data.get('max_context_tokens') or 2048)
items = []
for key in ['prompt', 'task', 'objective', 'current_plan', 'previous_results', 'trace', 'rubric']:
    value = payload_data.get(key)
    if value not in (None, '', [], {{}}):
        items.append({{'source': key, 'text': str(value), 'tokens': max(1, len(str(value)) // 4)}})
for idx, item in enumerate(messages + source_notes + candidate_outputs):
    text = str(item.get('content') or item.get('text') or item if isinstance(item, dict) else item)
    items.append({{'source': 'item_%d' % idx, 'text': text, 'tokens': max(1, len(text) // 4)}})
for item in items:
    lower = item['text'].lower()
    item['priority'] = 1
    if any(word in lower for word in ['must', 'constraint', 'objective', 'error', 'blocked', 'acceptance']):
        item['priority'] += 3
    if any(word in lower for word in ['done', 'thanks', 'maybe', 'chatter']):
        item['priority'] -= 1
items = sorted(items, key=lambda item: (item['priority'], -item['tokens']), reverse=True)
kept = []
compressed = []
dropped = []
used = 0
for item in items:
    if used + item['tokens'] <= token_budget:
        kept.append(item)
        used += item['tokens']
    elif item['priority'] >= 3:
        compact = dict(item)
        compact['compressed_text'] = item['text'][:240]
        compressed.append(compact)
        used += min(item['tokens'], 80)
    else:
        dropped.append(item)
fit = used <= token_budget
result['summary'] = plugin_name + ': optimized context to about ' + str(used) + ' tokens against budget ' + str(token_budget) + '.'
result['primary_insights'] = [
    {{'title': 'Kept context', 'detail': [item['source'] for item in kept]}},
    {{'title': 'Compressed context', 'detail': [item['source'] for item in compressed]}},
    {{'title': 'Dropped context', 'detail': [item['source'] for item in dropped]}},
]
result['recommended_actions'] = [
    {{'action': 'Keep high-priority context', 'items': [item['source'] for item in kept[:8]]}},
    {{'action': 'Compress oversized but important context', 'items': [item['source'] for item in compressed[:8]]}},
    {{'action': 'Drop low-signal context', 'items': [item['source'] for item in dropped[:8]]}},
]
result['scores'] = {{'confidence': round(min(0.92, 0.45 + 0.08 * len(items[:5])), 2), 'token_budget_fit': 1.0 if fit else round(token_budget / max(1, used), 2), 'context_retention': round(len(kept) / max(1, len(items)), 2), 'risk': round(0.18 + (0.18 if not fit else 0) + 0.03 * len(dropped), 2)}}
result['details'] = {{'kept_context': kept[:10], 'compressed_context': compressed[:10], 'dropped_context': dropped[:10], 'token_budget': token_budget, 'estimated_tokens': used, 'missing_inputs': ['context items'] if not items else []}}
{_common_result_footer("'Use kept_context, then compressed_context, and omit dropped_context.'")}
""".strip()


def _output_quality(spec: PluginSpec, capability_type: Optional[str], profile_id: str, reason: str) -> str:
    return f"""
{_common_header(spec, capability_type, profile_id, reason)}
response_text = str(payload_data.get('response') or payload_data.get('answer') or (candidate_outputs[0] if candidate_outputs else '')).strip()
rubric = payload_data.get('rubric') if isinstance(payload_data.get('rubric'), list) else []
requirements = rubric or constraints or [objective_text, def_text]
missing_requirements = []
covered_requirements = []
lower_response = response_text.lower()
for requirement in requirements:
    req = str(requirement).strip()
    keywords = [word.strip('.,:;!?').lower() for word in req.split() if len(word.strip('.,:;!?')) > 4][:5]
    hits = [word for word in keywords if word in lower_response]
    if hits:
        covered_requirements.append({{'requirement': req, 'matched_terms': hits}})
    else:
        missing_requirements.append(req)
clarity_flags = []
if len(response_text.split()) < 20:
    clarity_flags.append('response is very short')
if any(marker in lower_response for marker in ['maybe', 'probably', 'i think', 'not sure']):
    clarity_flags.append('uncertainty is not resolved')
if 'test' not in lower_response and 'verify' not in lower_response and 'check' not in lower_response:
    clarity_flags.append('verification step is missing')
coverage = len(covered_requirements) / max(1, len(requirements))
quality_score = round(min(0.95, 0.35 + 0.45 * coverage + (0.12 if not clarity_flags else 0)), 2)
improvement_checklist = []
for req in missing_requirements[:5]:
    improvement_checklist.append('Address requirement: ' + req[:140])
for flag in clarity_flags:
    improvement_checklist.append('Fix quality issue: ' + flag)
if not improvement_checklist:
    improvement_checklist.append('Preserve covered requirements and add evidence for the strongest claim.')
result['summary'] = plugin_name + ': scored output quality at ' + str(quality_score) + ' for ' + def_text[:130] + '.'
result['primary_insights'] = [
    {{'title': 'Covered requirements', 'detail': covered_requirements[:6]}},
    {{'title': 'Missing requirements', 'detail': missing_requirements[:6]}},
    {{'title': 'Clarity flags', 'detail': clarity_flags or 'No major clarity flags.'}},
]
result['recommended_actions'] = [{{'action': item}} for item in improvement_checklist[:6]]
result['scores'] = {{'confidence': round(0.45 + min(0.4, 0.08 * len(requirements)), 2), 'quality': quality_score, 'coverage': round(coverage, 2), 'risk': round(0.18 + 0.1 * len(missing_requirements[:4]) + 0.05 * len(clarity_flags), 2)}}
result['details'] = {{'covered_requirements': covered_requirements, 'missing_requirements': missing_requirements, 'clarity_flags': clarity_flags, 'improvement_checklist': improvement_checklist, 'missing_inputs': ['response or candidate_outputs'] if not response_text else []}}
{_common_result_footer("improvement_checklist[0] if improvement_checklist else 'Keep the output as-is.'")}
""".strip()


def _hallucination(spec: PluginSpec, capability_type: Optional[str], profile_id: str, reason: str) -> str:
    return f"""
{_common_header(spec, capability_type, profile_id, reason)}
text = str(payload_data.get('response') or payload_data.get('answer') or (candidate_outputs[0] if candidate_outputs else '')).strip()
sentences = [part.strip() for part in text.replace('\\n', '. ').split('.') if part.strip()]
risk_terms = ['always', 'never', 'guaranteed', 'latest', 'current', 'law', 'legal', 'medical', 'financial', 'price', 'study', 'research', 'statistic', 'percent']
claims = []
for sentence in sentences:
    lower = sentence.lower()
    signals = [term for term in risk_terms if term in lower]
    has_citation = 'http' in lower or '[' in sentence or 'source' in lower or 'citation' in lower
    if signals or any(ch.isdigit() for ch in sentence):
        claims.append({{'claim': sentence[:220], 'risk_signals': signals, 'has_citation': has_citation, 'needs_verification': bool(signals) and not has_citation}})
high_risk = [claim for claim in claims if claim['needs_verification']]
safer_rewrites = []
for claim in high_risk[:5]:
    safer_rewrites.append({{'original': claim['claim'], 'rewrite': 'Verify before relying on this claim: ' + claim['claim']}})
risk_score = round(min(0.95, 0.18 + 0.12 * len(high_risk) + 0.04 * len(claims)), 2)
result['summary'] = plugin_name + ': found ' + str(len(high_risk)) + ' claim(s) needing verification.'
result['primary_insights'] = [
    {{'title': 'Claims needing verification', 'detail': high_risk[:6]}},
    {{'title': 'Citation coverage', 'detail': str(len([c for c in claims if c['has_citation']])) + ' cited of ' + str(len(claims)) + ' flagged claims'}},
    {{'title': 'Risk domains', 'detail': sorted(set(term for claim in claims for term in claim['risk_signals']))}},
]
result['recommended_actions'] = [
    {{'action': 'Verify claim', 'claim': claim['claim'], 'signals': claim['risk_signals']}} for claim in high_risk[:5]
]
if safer_rewrites:
    result['recommended_actions'].append({{'action': 'Use safer rewrites', 'rewrites': safer_rewrites}})
result['scores'] = {{'confidence': round(0.5 + min(0.35, 0.06 * len(sentences)), 2), 'hallucination_risk': risk_score, 'citation_coverage': round(len([c for c in claims if c['has_citation']]) / max(1, len(claims)), 2), 'risk': risk_score}}
result['details'] = {{'claims': claims, 'high_risk_claims': high_risk, 'safer_rewrites': safer_rewrites, 'missing_inputs': ['response or candidate_outputs'] if not text else []}}
{_common_result_footer("'Verify the highest-risk uncited claim.'")}
""".strip()


def _retrieval_query(spec: PluginSpec, capability_type: Optional[str], profile_id: str, reason: str) -> str:
    return f"""
{_common_header(spec, capability_type, profile_id, reason)}
base = ' '.join([def_text, objective_text]).strip()
noise = ['please', 'help', 'make', 'better', 'stuff', 'things', 'very']
tokens = [word.strip('.,:;!?').lower() for word in base.split()]
keywords = []
for token in tokens:
    if len(token) > 3 and token not in noise and token not in keywords:
        keywords.append(token)
facet_terms = {{
    'implementation': [word for word in keywords if word in ['code', 'python', 'api', 'plugin', 'test', 'error']],
    'evaluation': [word for word in keywords if word in ['quality', 'rubric', 'score', 'verify', 'citation']],
    'planning': [word for word in keywords if word in ['agent', 'workflow', 'handoff', 'task', 'plan']],
}}
expanded_queries = []
core = ' '.join(keywords[:8]) or base[:120] or goal
expanded_queries.append(core)
expanded_queries.append(core + ' examples implementation')
expanded_queries.append(core + ' best practices validation')
if objective_text:
    expanded_queries.append(core + ' ' + objective_text[:80])
negative_terms = [word for word in noise if word in tokens]
grounding_plan = [
    'Search broad query first: ' + expanded_queries[0],
    'Then search implementation-specific query if code or plugin signals appear.',
    'Prefer primary documentation or direct source artifacts over summaries.',
]
result['summary'] = plugin_name + ': expanded retrieval into ' + str(len(expanded_queries)) + ' grounded queries.'
result['primary_insights'] = [
    {{'title': 'Core query', 'detail': core}},
    {{'title': 'Facet terms', 'detail': facet_terms}},
    {{'title': 'Noise removed', 'detail': negative_terms}},
]
result['recommended_actions'] = [
    {{'action': 'Run retrieval query', 'query': query}} for query in expanded_queries
]
result['scores'] = {{'confidence': round(min(0.9, 0.42 + 0.05 * len(keywords)), 2), 'query_specificity': round(min(0.95, 0.3 + 0.06 * len(keywords)), 2), 'grounding_value': round(0.58 + min(0.3, 0.06 * len(expanded_queries)), 2), 'risk': round(0.22 + (0.12 if len(keywords) < 3 else 0), 2)}}
result['details'] = {{'core_query': core, 'expanded_queries': expanded_queries, 'facet_terms': facet_terms, 'negative_terms': negative_terms, 'grounding_plan': grounding_plan, 'missing_inputs': ['task or objective'] if not base else []}}
{_common_result_footer("'Run retrieval query: ' + expanded_queries[0]")}
""".strip()


def _handoff(spec: PluginSpec, capability_type: Optional[str], profile_id: str, reason: str) -> str:
    body = _task_planner(spec, capability_type, profile_id, reason)
    return body.replace(
        "built a sequenced AI-agent plan with checkpoints",
        "built a multi-agent handoff plan with ownership boundaries",
    ).replace(
        "'handoff_packet': handoff_packet",
        "'handoff_packet': handoff_packet, 'ownership_boundaries': [{'agent': 'implementer', 'owns': 'code changes'}, {'agent': 'reviewer', 'owns': 'risk review'}, {'agent': 'verifier', 'owns': 'test evidence'}]",
    )


PROFILE_BUILDERS: Dict[str, tuple[str, Callable[[PluginSpec, Optional[str], str, str], str]]] = {
    "ai_agent_task_planner": ("task_planner_profile", _task_planner),
    "ai_tool_selection_advisor": ("tool_selection_profile", _tool_selection),
    "ai_memory_compression_synthesizer": ("memory_compression_profile", _memory_compression),
    "ai_context_window_optimizer": ("context_window_optimizer_profile", _context_optimizer),
    "ai_output_quality_scorer": ("output_quality_scorer_profile", _output_quality),
    "ai_hallucination_risk_auditor": ("hallucination_risk_auditor_profile", _hallucination),
    "ai_retrieval_query_expander": ("retrieval_query_expander_profile", _retrieval_query),
    "ai_multi_agent_handoff_planner": ("multi_agent_handoff_profile", _handoff),
}


def registered_profile_id(slug: str) -> Optional[str]:
    item = PROFILE_BUILDERS.get(slug)
    return item[0] if item else None


def build_profile_logic_body(
    spec: PluginSpec,
    capability_type: Optional[str],
    logic_profile_id: Optional[str],
    *,
    reason: str,
) -> Optional[str]:
    item = PROFILE_BUILDERS.get(str(getattr(spec, "slug", "") or ""))
    if not item:
        return None
    profile_id, builder = item
    return builder(spec, capability_type, profile_id or logic_profile_id or "capability_profile", reason)


def wrap_logic_body(logic_body: str) -> str:
    body = textwrap.dedent(logic_body).strip()
    encoded = base64.b64encode(body.encode("utf-8", errors="replace")).decode("ascii")
    return f"""
# Auto-generated capability-profile core logic envelope. Edits may be overwritten by the factory.
import base64
try:
    from schema_tools import infer_tabular_schema, pick_numeric_field
except Exception:  # pragma: no cover
    def infer_tabular_schema(data):
        return {{}}
    def pick_numeric_field(schema, hints=None):
        return None
try:
    if hasattr(context, 'log_info'):
        context.log_info('Executing capability-profile core logic.', plugin_slug=_PLUGIN_SLUG)
except Exception:
    pass
_profile_body_b64 = {encoded!r}
try:
    _profile_body_source = base64.b64decode(_profile_body_b64.encode('ascii')).decode('utf-8')
except Exception:
    _profile_body_source = ''
result = {{
    'summary': '',
    'primary_insights': [],
    'recommended_actions': [],
    'scores': {{'confidence': 0.0}},
    'details': {{}},
}}
schema = infer_tabular_schema(payload.get('data') if isinstance(payload, dict) else None)
local_vars = {{
    'context': context,
    'payload': payload,
    'config': config,
    'schema': schema,
    'pick_numeric_field': pick_numeric_field,
    'result': result,
}}
if _profile_body_source.strip():
    try:
        exec(_profile_body_source, local_vars, local_vars)
        if isinstance(local_vars.get('result'), dict):
            result = local_vars['result']
    except Exception as _exc:
        result = {{
            'summary': 'Capability profile failed; fallback applied.',
            'primary_insights': [],
            'recommended_actions': ['Review payload and capability profile.'],
            'scores': {{'confidence': 0.0}},
            'details': {{'error': str(_exc), 'logic_profile_id': 'capability_profile_error'}},
        }}
if not isinstance(result, dict):
    result = {{'summary': 'Capability profile returned non-dict output.', 'primary_insights': [], 'recommended_actions': [], 'scores': {{'confidence': 0.0}}, 'details': {{}}}}
result.setdefault('summary', 'Capability profile completed.')
result.setdefault('primary_insights', [])
result.setdefault('recommended_actions', [])
result.setdefault('scores', {{'confidence': 0.0}})
result.setdefault('details', {{}})
return result
""".strip()


def update_logic_region(base_source: str, new_logic_body: str) -> str:
    pattern = rf"{re.escape(LOGIC_START)}.*?{re.escape(LOGIC_END)}"
    replacement = f"{LOGIC_START}\n{textwrap.indent(new_logic_body.strip(), '    ')}\n{LOGIC_END}"
    updated, count = re.subn(pattern, replacement, base_source, flags=re.DOTALL)
    if count != 1:
        raise ValueError("Expected exactly one plugin logic region.")
    return updated


def build_profile_source(
    source: str,
    spec: PluginSpec,
    capability_type: Optional[str],
    logic_profile_id: Optional[str],
    *,
    reason: str,
) -> Optional[str]:
    body = build_profile_logic_body(
        spec,
        capability_type,
        logic_profile_id,
        reason=reason,
    )
    if not body:
        return None
    return update_logic_region(source, wrap_logic_body(body))
