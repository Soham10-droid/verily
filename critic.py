"""Agent 2: checks every claim in the draft against the real source text,
then rewrites the answer keeping only what held up."""

from ai import AIError, ask, parse_json
from search import format_sources

CHECK_SYSTEM = (
    "You are a strict fact-checker. You compare claims to source text word by "
    "word and you are not persuaded by claims that merely sound right. "
    "You reply with JSON only."
)

CONFLICT_SYSTEM = (
    "You compare sources against EACH OTHER, not against any draft. You only "
    "flag a genuine factual disagreement (different numbers, dates, or "
    "direct contradictions on the same specific fact) — not differences in "
    "emphasis, wording, or topic coverage. You reply with JSON only."
)

VERDICTS = {"supported", "partial", "unsupported"}


def check_claims(question, draft, sources):
    """Return a list of {claim, sources, verdict, reason, correction}."""
    prompt = f"""Below is a draft answer to the question "{question}", followed by the
sources it cites. Split the draft into its individual factual claims (at most 8)
and check each one against the source text.

Verdicts:
- "supported": the cited source clearly says this.
- "partial": the source says something close, but the draft exaggerates, adds a detail, or overgeneralises.
- "unsupported": no source says this, or the cited source says something different.

Keep "reason" to one short phrase, 12 words or fewer. Leave "correction" as ""
unless the verdict is "partial".

Reply with JSON in exactly this shape:
{{"claims": [{{"claim": "the claim, quoted or closely paraphrased from the draft",
  "sources": [1],
  "verdict": "supported",
  "reason": "short phrase",
  "correction": ""}}]}}

Draft:
{draft}

Sources:
{format_sources(sources)}
"""
    data = parse_json(ask(prompt, system=CHECK_SYSTEM, json_mode=True,
                          temperature=0, max_tokens=3000))
    raw_claims = (data or {}).get("claims") or []

    claims = []
    for item in raw_claims:
        if not isinstance(item, dict) or not str(item.get("claim", "")).strip():
            continue
        verdict = str(item.get("verdict", "")).lower().strip()
        if verdict.startswith("partial"):
            verdict = "partial"
        if verdict not in VERDICTS:
            verdict = "unsupported"
        cited = [int(n) for n in item.get("sources") or [] if str(n).isdigit()]
        claims.append({
            "claim": str(item["claim"]).strip(),
            "sources": cited,
            "verdict": verdict,
            "reason": str(item.get("reason", "")).strip(),
            "correction": str(item.get("correction", "")).strip(),
        })
    return claims


def check_conflicts(question, sources):
    """Look for sources that directly contradict each other on a specific
    fact (e.g. different figures for the same thing). This needs real
    language understanding — spotting that two differently-worded sentences
    disagree — so unlike rules.py it's an LLM call, not a fixed rule.
    Returns [] (never raises) if the check can't complete, so a flaky model
    here never breaks the rest of the pipeline.
    """
    if len(sources) < 2:
        return []
    prompt = f"""These sources were gathered to help answer: "{question}"

Check only for DIRECT factual contradictions between sources — e.g. two
sources giving different numbers, dates, or opposite claims about the same
specific fact. Do not flag sources that simply cover different aspects or
use different wording for the same fact.

Reply with JSON in exactly this shape:
{{"conflicts": [{{"issue": "one short sentence describing the disagreement",
  "sources": [1, 2]}}]}}

If there are no real contradictions, reply {{"conflicts": []}}.

Sources:
{format_sources(sources)}
"""
    try:
        data = parse_json(ask(prompt, system=CONFLICT_SYSTEM, json_mode=True,
                              temperature=0, max_tokens=800))
    except AIError:
        return []

    out = []
    for item in (data or {}).get("conflicts") or []:
        if not isinstance(item, dict) or not str(item.get("issue", "")).strip():
            continue
        cited = [int(n) for n in item.get("sources") or [] if str(n).isdigit()]
        if len(cited) >= 2:
            out.append({"issue": str(item["issue"]).strip(), "sources": cited})
    return out


def write_final(question, draft, claims, sources):
    """Rewrite the draft so it contains only claims that held up."""
    if claims and all(c["verdict"] == "supported" for c in claims):
        return draft  # nothing to fix, save an API call

    if claims and not any(c["verdict"] != "unsupported" for c in claims):
        return ("None of the claims in the first draft held up against the "
                "sources that were found, so there's no verified answer to "
                "show. Try rephrasing the question or making it more specific.")

    review = "\n".join(
        f"- [{c['verdict'].upper()}] {c['claim']}"
        + (f"\n  Use instead: {c['correction']}" if c["correction"] else "")
        for c in claims
    )
    prompt = f"""Rewrite the draft answer to "{question}" using the fact-check below.

- Keep SUPPORTED claims as they are, with their [n] citations.
- Replace PARTIAL claims with their "Use instead" version, keeping a citation.
- Remove UNSUPPORTED claims completely. Don't mention that anything was removed.
- Keep it readable: 2 to 4 short paragraphs, plain language, no headings.
- Do not add anything new.

Draft:
{draft}

Fact-check:
{review}

Sources (for citation numbers only):
{format_sources(sources)}
"""
    return ask(prompt, temperature=0.2)
