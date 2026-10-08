# Verily

A research agent that checks its own answer before showing it to you —
named for the old word for "in truth," which is exactly what the checking
pass is looking for.

You ask a question. The app searches the web, reads the top pages, and
writes a first draft with numbered citations. It then runs that draft
through two different kinds of checking — a model-based one and a
rule-based one — before showing you a corrected final answer, a full
claim-by-claim audit trail, and a confidence score.

## How it works

1. **Search** — DuckDuckGo finds pages; they're opened in parallel and their main text is extracted.
2. **Conflict check** — before anything is written, an LLM compares the sources *against each other*, flagging any that directly disagree (different numbers, dates, etc.) on the same fact.
3. **Draft (Agent 1)** — an LLM answers using only those pages, citing each sentence as [1], [2]...
4. **Claim check (Agent 2)** — the same LLM, with a fact-checker's instructions, returns a structured verdict for every claim: supported, partial, or unsupported.
5. **Rule engine** — a small, fixed set of hand-written rules (`rules.py`) then runs over those verdicts: a source-trust tier list downgrades claims backed only by lower-trust domains, and a numeric-verification check downgrades claims whose exact figures don't appear in the cited source text. This part makes no LLM call — it's plain, auditable Python, which is why every adjustment it makes is shown with the specific rule that fired.
6. **Rewrite** — the answer is rebuilt from supported and corrected claims only, and a 0-100 confidence score is computed from the final verdicts (cross-verified claims — backed by 2+ sources — count more than single-source ones).

The interface shows the verified answer, a confidence score, any source
conflicts, the full claim-by-claim check (each with a trust badge and a
rule trace where relevant), the original unedited draft, and the sources —
and the whole thing can be downloaded as a Markdown file.

### Why two kinds of checking, not just one bigger prompt

The claim checker (step 4) and the conflict checker (step 2) both need real
language understanding — judging whether two differently-worded sentences
actually agree — so both are LLM calls. The rule engine (step 5) is the
opposite on purpose: fixed logic with no model involved, so its behaviour
is 100% predictable and explainable, the way a classical expert system's
rules are. Keeping those two kinds of checking separate in the code (rather
than asking one big prompt to "also consider source trust") means the
rule-based part can't drift or hallucinate, and its reasoning can always be
shown verbatim in the UI.

## Tech (all free)

Groq API (free tier) for the LLM calls, `ddgs` for search, `requests` +
BeautifulSoup for reading pages, and Streamlit for the interface, with a
hand-built light/dark theme.

## Run it

1. Get a free API key at https://console.groq.com/keys
2. Open `.env` and paste it after `GROQ_API_KEY=`
3. On Windows, double-click `run.bat`. Or in a terminal:

```
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

## Files

| File | What it does |
| --- | --- |
| `app.py` | The page: input, progress, results, history, export |
| `search.py` | Web search and page reading |
| `researcher.py` | Agent 1, writes the cited draft |
| `critic.py` | Agent 2 (claim checking) and the source-conflict checker |
| `rules.py` | The rule engine / knowledge base — source trust tiers, numeric verification, confidence scoring |
| `ai.py` | Talks to Groq, with fallback models and clear error messages |
| `styles.py` | Light and dark themes |

## Limits

The model-based checks are themselves LLMs, so they can make mistakes too —
nothing here guarantees a perfect answer. The rule engine's source-trust
list is small and deliberately conservative: an unfamiliar site is left
"unclassified" rather than guessed at, so it won't unfairly flag a
legitimate source it simply doesn't recognise. Some sites also block
automated reading, in which case only the search summary is used and the
source is marked as such. Session history and the Markdown export only
cover the current browser session — nothing is saved to a database.
