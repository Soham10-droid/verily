# Verily

A research agent that checks its own answer before showing it to you —
named for the old word for "in truth," which is exactly what the second
pass is checking for.

You ask a question. The app searches the web, reads the top pages, and writes
a first draft with numbered citations. A second pass then goes through the
draft claim by claim, compares each one with the page it cited, and marks it
as holding up, stretched, or not in the sources. The final answer keeps only
what held up, rewords what was stretched, and drops the rest.

## How it works

1. **Search** — DuckDuckGo finds pages; they're opened in parallel and their main text is extracted.
2. **Draft (Agent 1)** — an LLM answers using only those pages, citing each sentence as [1], [2]...
3. **Check (Agent 2)** — the same LLM, with a fact-checker's instructions, returns a structured verdict for every claim.
4. **Rewrite** — the answer is rebuilt from supported and corrected claims only.

The interface shows the verified answer, the full claim-by-claim check, the original
draft, and the sources, so you can see exactly what changed and why.

## Tech (all free)

Groq API (free tier) for the LLM, `ddgs` for search, `requests` + BeautifulSoup for
reading pages, and Streamlit for the interface, with a hand-built light and dark theme.

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
| `app.py` | The page: input, progress, results |
| `search.py` | Web search and page reading |
| `researcher.py` | Agent 1, writes the cited draft |
| `critic.py` | Agent 2, checks claims and rewrites the answer |
| `ai.py` | Talks to Groq, with fallback models and clear error messages |
| `styles.py` | Light and dark themes |

## Limits

The checker is itself an LLM, so it can make mistakes too. It reduces unsupported
claims; it doesn't guarantee a perfect answer. Some sites block automated reading,
in which case only the search summary is used and the source is marked as such.
