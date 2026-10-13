"""Agent 1: writes a first draft using only the sources it found."""

from ai import AIError, ask, parse_json
from search import format_sources

SYSTEM = (
    "You are a careful research assistant. You only state things the "
    "provided sources say. You never add facts from memory."
)


def write_draft(question, sources):
    prompt = f"""Answer the question using ONLY the numbered sources below.

Rules:
- After every factual sentence, cite its source number in square brackets, like [2] or [1][3].
- Write 2 to 4 short paragraphs in plain language. Use a bullet list only if it truly helps.
- If the sources don't fully answer the question, say what's missing.
- Do not mention "the sources" in every sentence; just write the answer and cite.

Question: {question}

Sources:
{format_sources(sources)}
"""
    return ask(prompt, system=SYSTEM, temperature=0.3)


def standalone_question(turns, followup):
    """Rewrite a follow-up such as "when was it founded?" into a full,
    searchable question ("When was ISRO founded?") using the earlier turns.
    A follow-up searched on its own would return unrelated pages. Falls back
    to the follow-up as typed if the model call fails."""
    context = []
    for t in turns[-3:]:
        if "error" in t:
            context.append(f"Q: {t['question']}")
        else:
            context.append(f"Q: {t['question']}\nA: {t['final'][:600]}")
    history = "\n\n".join(context)
    prompt = f"""Conversation so far:
{history}

Follow-up question: {followup}

Rewrite the follow-up as ONE standalone question that makes sense with no
conversation history. Replace words like "it", "they" or "that" with what they
refer to. If it is already standalone, return it unchanged. Reply with the
question only, with no quotes and no explanation."""
    try:
        reply = ask(prompt, temperature=0, max_tokens=120).strip()
    except AIError:
        return followup
    if not reply:
        return followup
    question = reply.splitlines()[0].strip().strip('"').strip("'").strip()
    return question[:300] or followup


def suggest_followups(question, answer):
    """Three short follow-up questions to show as clickable suggestions.
    Returns [] if the model call fails, so suggestions never block an answer."""
    prompt = f"""A user asked: "{question}"
They got this answer:
{answer[:1500]}

Suggest 3 natural follow-up questions they might ask next. Each must be
under 12 words, specific to this topic, and answerable with a web search.

Reply with JSON in exactly this shape: {{"questions": ["...", "...", "..."]}}"""
    try:
        data = parse_json(ask(prompt, json_mode=True, temperature=0.4, max_tokens=300))
    except AIError:
        return []
    raw = (data or {}).get("questions") or []
    return [str(q).strip() for q in raw if str(q).strip()][:3]
