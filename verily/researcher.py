"""Agent 1: writes a first draft using only the sources it found."""

from ai import ask
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
