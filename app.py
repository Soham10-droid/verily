"""Verily: a research agent that checks its own answer before showing it."""

import html
import re

import streamlit as st

from ai import AIError, get_api_key
from critic import check_claims, check_conflicts, write_final
from researcher import write_draft
from rules import apply_rules, confidence_score, trust_tier
from search import SearchError, gather_sources
from styles import GITHUB_ICON, css

st.set_page_config(page_title="Verily", page_icon="🔍", layout="centered")

REPO_URL = "https://github.com/Soham10-droid/verily"

# (chip label, actual question sent to the agent)
EXAMPLES = [
    ("🗓️ Leap Year Logic", "Why do we get leap years?"),
    ("🎧 Noise Cancellation", "How do noise-cancelling headphones work?"),
    ("🧠 10% Brain Myth", "Is it true that we only use 10% of our brain?"),
]

STEPS = [
    "Searching the web",
    "Reading the pages",
    "Checking sources for contradictions",
    "Writing a first draft",
    "Checking every claim against the sources",
    "Rewriting with only what held up",
]

TRUST_LABEL = {"high": "High-trust", "medium": "Reputable", "low": "Lower-trust"}

# ---------------------------------------------------------------- state
st.session_state.setdefault("dark", False)
st.session_state.setdefault("result", None)
st.session_state.setdefault("run_now", False)
st.session_state.setdefault("history", [])


def use_example(question):
    st.session_state.q = question
    st.session_state.run_now = True


def use_history(entry):
    st.session_state.result = entry
    st.session_state.q = entry["question"]


# ---------------------------------------------------------------- helpers
def one_line(s):
    """st.markdown treats blank lines as the end of HTML, so keep it on one line."""
    return re.sub(r"\s*\n\s*", " ", s)


def show(html_str):
    st.markdown(one_line(html_str), unsafe_allow_html=True)


def rich(text, sources):
    """Tiny, safe markdown: paragraphs, bullets, bold, and [n] citation chips."""
    by_id = {s["id"]: s for s in sources}

    def cite(match):
        chips = []
        for n in re.findall(r"\d+", match.group(0)):
            src = by_id.get(int(n))
            if src:
                tip = html.escape(src["domain"], quote=True)
                chips.append(f'<a class="cite" href="{html.escape(src["url"], quote=True)}" '
                             f'target="_blank" title="{tip}">{n}</a>')
        return "".join(chips)

    safe = html.escape(text.strip())
    safe = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", safe)
    safe = re.sub(r"(?:\[\s*\d+(?:\s*[,;]\s*\d+)*\s*\])+", cite, safe)

    out = []
    for block in re.split(r"\n\s*\n", safe):
        lines = [ln.strip() for ln in block.split("\n") if ln.strip()]
        if not lines:
            continue
        bullet = re.compile(r"^(?:[-*•]|\d+[.)])\s+")
        if all(bullet.match(ln) for ln in lines):
            items = "".join(f"<li>{bullet.sub('', ln)}</li>" for ln in lines)
            out.append(f"<ul>{items}</ul>")
        elif re.match(r"^#{1,4}\s", lines[0]):
            out.append(f"<h4>{re.sub(r'^#{1,4}\s*', '', lines[0])}</h4>")
            if lines[1:]:
                out.append(f"<p>{' '.join(lines[1:])}</p>")
        else:
            out.append(f"<p>{' '.join(lines)}</p>")
    return "".join(out)


def steps_html(active, notes):
    items = []
    for i, label in enumerate(STEPS):
        state = "done" if i < active else "active" if i == active else ""
        note = f' <span class="note">{html.escape(notes[i])}</span>' if notes.get(i) else ""
        items.append(f'<li class="{state}">{label}{note}</li>')
    return f'<ol class="steps">{"".join(items)}</ol>'


def tally_html(claims, confidence):
    if not claims:
        return ""
    n = len(claims)
    ok = sum(c["verdict"] == "supported" for c in claims)
    part = sum(c["verdict"] == "partial" for c in claims)
    bad = sum(c["verdict"] == "unsupported" for c in claims)
    bits = [f"<b>{ok} of {n}</b> claims in the first draft held up."]
    if part:
        bits.append(f"{part} {'was' if part == 1 else 'were'} reworded to match the source.")
    if bad:
        bits.append(f"{bad} {'was' if bad == 1 else 'were'} taken out.")
    conf = f' <span class="confidence">{confidence}% confidence score</span>' if confidence is not None else ""
    return f'<p class="tally">{" ".join(bits)}{conf}</p>'


def trust_badge(tier):
    if tier not in TRUST_LABEL:
        return ""  # unclassified sources get no badge — avoids guessing
    return f'<span class="trust-badge {tier}">{TRUST_LABEL[tier]}</span>'


def claims_html(claims):
    label = {"supported": "Holds up", "partial": "Stretched", "unsupported": "Not in sources"}
    rows = []
    for c in claims:
        srcs = ", ".join(f"[{n}]" for n in c["sources"])
        reason = c["reason"].rstrip()
        if reason and reason[-1] not in ".!?":
            reason += "."
        bits = [html.escape(reason)] if reason else []
        if srcs:
            bits.append(f"Checked against {srcs}.")
        if c["verdict"] == "supported":
            bits.append("Cross-verified by multiple sources."
                        if c.get("cross_verified") else "Backed by a single source.")
        for note in c.get("rule_notes", []):
            bits.append(html.escape(note))
        why = " ".join(bits)
        fix = ""
        if c["verdict"] == "partial" and c["correction"]:
            fix = f'<div class="fix">{html.escape(c["correction"])}</div>'
        rows.append(
            f'<div class="claim {c["verdict"]}">'
            f'<div class="text"><span class="verdict">{label[c["verdict"]]}</span>'
            f'{trust_badge(c.get("trust"))}'
            f'<span class="c">{html.escape(c["claim"])}</span></div>'
            f'<div class="why">{why}</div>{fix}</div>'
        )
    return f'<div class="claim-list">{"".join(rows)}</div>'


def conflicts_html(conflicts):
    if not conflicts:
        return ""
    rows = []
    for c in conflicts:
        srcs = ", ".join(f"[{n}]" for n in c["sources"])
        rows.append(f'<div class="conflict-item">{html.escape(c["issue"])}'
                    f' <span class="conflict-src">Sources {srcs}.</span></div>')
    return ('<div class="conflict-box"><b>\u26a0 Sources disagree with each other</b>'
            f'{"".join(rows)}</div>')


def sources_html(sources):
    rows = []
    for s in sources:
        extra = " \u00b7 search summary only, page couldn't be opened" if s["snippet_only"] else ""
        rows.append(
            f'<li><span class="n">{s["id"]}</span>'
            f'<div class="title-row"><a href="{html.escape(s["url"], quote=True)}" target="_blank">'
            f'{html.escape(s["title"])}</a>{trust_badge(trust_tier(s["domain"]))}</div>'
            f'<span class="dom">{html.escape(s["domain"])}{extra}</span></li>'
        )
    return f'<ol class="sources">{"".join(rows)}</ol>'


def notice(title, body):
    show(f'<div class="notice"><b>{title}</b><br>{body}</div>')


def build_markdown(result):
    """A plain-text export of the result — question, verified answer, the
    claim-by-claim check, any source conflicts, and the source list."""
    lines = [f"# {result['question']}", "", result["final"], ""]
    if result.get("confidence") is not None:
        lines.append(f"**Confidence score: {result['confidence']}%**\n")
    if result.get("claims"):
        lines.append("## Claim-by-claim check")
        for c in result["claims"]:
            lines.append(f"- **{c['verdict'].upper()}** — {c['claim']}")
            if c.get("reason"):
                lines.append(f"  - {c['reason']}")
            for note in c.get("rule_notes", []):
                lines.append(f"  - Rule: {note}")
        lines.append("")
    if result.get("conflicts"):
        lines.append("## Possible source conflicts")
        for cf in result["conflicts"]:
            srcs = ", ".join(str(n) for n in cf["sources"])
            lines.append(f"- {cf['issue']} (sources {srcs})")
        lines.append("")
    lines.append("## Sources")
    for s in result["sources"]:
        lines.append(f"{s['id']}. [{s['title']}]({s['url']}) — {s['domain']}")
    return "\n".join(lines)


# ---------------------------------------------------------------- pipeline
def run(question, progress):
    notes = {}
    progress.markdown(one_line(steps_html(0, notes)), unsafe_allow_html=True)

    sources = gather_sources(question)
    if not sources:
        return {"question": question, "error": (
            "No readable pages turned up",
            "The search found nothing the agent could read. Try wording the question differently.")}
    notes[0] = f"found {len(sources)} usable pages"
    notes[1] = ", ".join(s["domain"] for s in sources)
    progress.markdown(one_line(steps_html(2, notes)), unsafe_allow_html=True)

    try:
        conflicts = check_conflicts(question, sources)
    except AIError:
        conflicts = []
    notes[2] = (f"{len(conflicts)} possible conflict(s)" if conflicts else "no conflicts between sources")
    progress.markdown(one_line(steps_html(3, notes)), unsafe_allow_html=True)

    draft = write_draft(question, sources)
    progress.markdown(one_line(steps_html(4, notes)), unsafe_allow_html=True)

    # If fact-checking has trouble (a flaky model, a busy free tier), still
    # show the draft rather than losing everything the research step found.
    try:
        claims = check_claims(question, draft, sources)
    except AIError:
        claims = []
        notes[4] = "checking didn't complete — showing the draft as-is"
    else:
        notes[4] = f"{len(claims)} claims checked" if claims else "couldn't split into claims"
    claims = apply_rules(claims, sources)  # the rule-engine layer, on top of the LLM's verdicts
    confidence = confidence_score(claims)
    progress.markdown(one_line(steps_html(5, notes)), unsafe_allow_html=True)

    if claims:
        try:
            final = write_final(question, draft, claims, sources)
        except AIError:
            final = draft
    else:
        final = draft
    progress.empty()
    return {"question": question, "draft": draft, "claims": claims, "final": final,
            "sources": sources, "conflicts": conflicts, "confidence": confidence}


# ---------------------------------------------------------------- page
show(css(st.session_state.dark))

top_left, top_right = st.columns([4, 1.5], vertical_alignment="center")
with top_left:
    show('<div class="mast-wrap"><div class="mast"><h1>Verily</h1>'
         '<span class="status-pill"><span class="status-dot"></span>'
         'Verified Engine Active</span></div></div>')
with top_right:
    gh_col, toggle_col = st.columns([1, 2.4], vertical_alignment="center")
    with gh_col:
        show(f'<a class="gh-link" href="{REPO_URL}" target="_blank" '
             f'title="View source on GitHub">{GITHUB_ICON}</a>')
    with toggle_col:
        st.toggle("Dark mode", key="dark")

show('<div class="stage-flow"><span class="stage">1. Web Extraction</span>'
     '<span class="arrow">➔</span><span class="stage">2. Source-Audited Verification</span>'
     '</div>')

with st.expander("How Verily verifies sources"):
    show('<p><b>Why two passes?</b> AI writing tools sometimes state things confidently '
         "that their sources never said. Here, a second pass reads the draft like an "
         "editor with the source pages open, and only what it can confirm reaches the "
         "final answer.</p>"
         '<p>Before drafting, Verily also checks whether the sources it found actually '
         "agree with each other, and flags it if they don't. After the draft is checked "
         'claim by claim, a small rule engine (see <code>rules.py</code>) applies fixed, '
         "non-AI checks on top — a source-trust tier list and a numeric-verification "
         "check — so some of what you see wasn't decided by a model at all.</p>")

if not get_api_key():
    notice("Add your Groq API key to start",
           "Open the <code>.env</code> file in this folder and paste your key after "
           "<code>GROQ_API_KEY=</code>. You can get one free at console.groq.com/keys. "
           "Then save the file and refresh this page.")
    st.stop()

with st.form("ask", border=False, clear_on_submit=False):
    col_q, col_b = st.columns([4, 1.3], vertical_alignment="center")
    with col_q:
        st.text_input("Your question", key="q", label_visibility="collapsed",
                      placeholder="What do you want to know?", autocomplete="off")
    with col_b:
        submitted = st.form_submit_button("Look it up")

if st.session_state.history:
    show('<p class="chip-label">Recent</p>')
    recent = st.session_state.history[:4]
    hist_cols = st.columns(len(recent))
    for col, entry in zip(hist_cols, recent):
        label = entry["question"] if len(entry["question"]) <= 30 else entry["question"][:29] + "…"
        col.button(label, on_click=use_history, args=(entry,),
                  use_container_width=True, key=f"hist-{id(entry)}")
elif not st.session_state.result:
    show('<p class="chip-label">Try one</p>')
    ex_cols = st.columns(len(EXAMPLES))
    for col, (label, question_text) in zip(ex_cols, EXAMPLES):
        col.button(label, on_click=use_example, args=(question_text,), use_container_width=True)

question = (st.session_state.get("q") or "").strip()
if (submitted or st.session_state.run_now) and question:
    st.session_state.run_now = False
    progress = st.empty()
    try:
        st.session_state.result = run(question, progress)
    except (SearchError, AIError) as exc:
        progress.empty()
        st.session_state.result = {"question": question,
                                   "error": ("That didn't work", html.escape(str(exc)))}
    except Exception as exc:  # anything unexpected: show it instead of crashing
        progress.empty()
        st.session_state.result = {"question": question, "error": (
            "Something went wrong", html.escape(f"{type(exc).__name__}: {exc}"))}
    else:
        if "error" not in st.session_state.result:
            st.session_state.history = (
                [st.session_state.result]
                + [h for h in st.session_state.history if h["question"] != question]
            )[:8]
elif submitted:
    notice("Type a question first", "The box is empty.")

result = st.session_state.result
if result:
    show(f'<div class="asked">{html.escape(result["question"])}</div>')
    if "error" in result:
        notice(*result["error"])
    else:
        sources = result["sources"]
        claims = result["claims"]
        clean = bool(claims) and all(c["verdict"] == "supported" for c in claims)
        stamp = '<div class="stamp">✓ Verified</div>' if clean else ""
        show(f'<div class="answer-wrap">{stamp}'
             f'<div class="answer">{rich(result["final"], sources)}</div></div>'
             + tally_html(claims, result.get("confidence")))

        show(conflicts_html(result.get("conflicts")))

        if claims:
            show('<div class="section-title">How the draft was checked</div>'
                 '<p class="section-sub">Each claim from the first draft, compared with '
                 "the page it cited and the trust rules in rules.py.</p>" + claims_html(claims))

        show('<details class="draft"><summary>Show the first draft, before checking</summary>'
             f'<div class="body">{rich(result["draft"], sources)}</div></details>')

        show('<div class="section-title">Sources</div>' + sources_html(sources))

        st.download_button("Download this answer as Markdown", data=build_markdown(result),
                           file_name="verily-answer.md", mime="text/markdown")
