"""Verily: a research agent that checks its own answer before showing it."""

import html
import re

import streamlit as st

from ai import AIError, get_api_key
from critic import check_claims, write_final
from researcher import write_draft
from search import SearchError, gather_sources
from styles import css

st.set_page_config(page_title="Verily", page_icon="🔍", layout="centered")

EXAMPLES = [
    "Why do we get leap years?",
    "How do noise-cancelling headphones work?",
    "Is it true that we only use 10% of our brain?",
]

STEPS = [
    "Searching the web",
    "Reading the pages",
    "Writing a first draft",
    "Checking every claim against the sources",
    "Rewriting with only what held up",
]

# ---------------------------------------------------------------- state
st.session_state.setdefault("dark", False)
st.session_state.setdefault("result", None)
st.session_state.setdefault("run_now", False)


def use_example(q):
    st.session_state.q = q
    st.session_state.run_now = True


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


def tally_html(claims):
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
    return f'<p class="tally">{" ".join(bits)}</p>'


def claims_html(claims):
    label = {"supported": "Holds up", "partial": "Stretched", "unsupported": "Not in sources"}
    rows = []
    for c in claims:
        srcs = ", ".join(f"[{n}]" for n in c["sources"])
        reason = c["reason"].rstrip()
        if reason and reason[-1] not in ".!?":
            reason += "."
        why = html.escape(reason) + (f" Checked against {srcs}." if srcs else "")
        fix = ""
        if c["verdict"] == "partial" and c["correction"]:
            fix = f'<div class="fix">{html.escape(c["correction"])}</div>'
        rows.append(
            f'<div class="claim {c["verdict"]}">'
            f'<div class="text"><span class="verdict">{label[c["verdict"]]}</span>'
            f'<span class="c">{html.escape(c["claim"])}</span></div>'
            f'<div class="why">{why}</div>{fix}</div>'
        )
    return f'<div class="claim-list">{"".join(rows)}</div>'


def sources_html(sources):
    rows = []
    for s in sources:
        extra = " (search summary only; the page couldn't be opened)" if s["snippet_only"] else ""
        rows.append(
            f'<li><span class="n">{s["id"]}</span>'
            f'<a href="{html.escape(s["url"], quote=True)}" target="_blank">{html.escape(s["title"])}</a>'
            f'<span class="dom">{html.escape(s["domain"])}{extra}</span></li>'
        )
    return f'<ol class="sources">{"".join(rows)}</ol>'


def notice(title, body):
    show(f'<div class="notice"><b>{title}</b><br>{body}</div>')


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

    draft = write_draft(question, sources)
    progress.markdown(one_line(steps_html(3, notes)), unsafe_allow_html=True)

    # If fact-checking has trouble (a flaky model, a busy free tier), still
    # show the draft rather than losing everything the research step found.
    try:
        claims = check_claims(question, draft, sources)
    except AIError:
        claims = []
        notes[3] = "checking didn't complete — showing the draft as-is"
    else:
        notes[3] = f"{len(claims)} claims checked" if claims else "couldn't split into claims"
    progress.markdown(one_line(steps_html(4, notes)), unsafe_allow_html=True)

    if claims:
        try:
            final = write_final(question, draft, claims, sources)
        except AIError:
            final = draft
    else:
        final = draft
    progress.empty()
    return {"question": question, "draft": draft, "claims": claims,
            "final": final, "sources": sources}


# ---------------------------------------------------------------- page
show(css(st.session_state.dark))

top_left, top_right = st.columns([4, 1.3], vertical_alignment="bottom")
with top_left:
    show('<div class="mast-wrap"><div class="mast"><h1>Verily</h1>'
         '<span class="dot"></span></div><div class="rule"></div></div>')
with top_right:
    st.toggle("Dark mode", key="dark")

show('<p class="lede">Ask a question. It searches the web, writes an answer, then '
     'checks each claim against the pages it read and removes anything the sources '
     "don't back up.</p>")

if not get_api_key():
    notice("Add your Groq API key to start",
           "Open the <code>.env</code> file in this folder and paste your key after "
           "<code>GROQ_API_KEY=</code>. You can get one free at console.groq.com/keys. "
           "Then save the file and refresh this page.")
    st.stop()

with st.form("ask", border=False, clear_on_submit=False):
    col_q, col_b = st.columns([4, 1.3], vertical_alignment="bottom")
    with col_q:
        st.text_input("Your question", key="q", label_visibility="collapsed",
                      placeholder="What do you want to know?")
    with col_b:
        submitted = st.form_submit_button("Look it up")

if not st.session_state.result:
    ex_cols = st.columns(len(EXAMPLES))
    for col, q in zip(ex_cols, EXAMPLES):
        col.button(q, on_click=use_example, args=(q,), use_container_width=True)

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
        stamp = '<div class="stamp">every claim checked</div>' if clean else ""
        show(f'<div class="answer-wrap">{stamp}'
             f'<div class="answer">{rich(result["final"], sources)}</div></div>'
             + tally_html(claims))

        if result["claims"]:
            show('<div class="section-title">How the draft was checked</div>'
                 '<p class="section-sub">Each claim from the first draft, compared with '
                 "the page it cited.</p>" + claims_html(result["claims"]))

        show('<details class="draft"><summary>Show the first draft, before checking</summary>'
             f'<div class="body">{rich(result["draft"], sources)}</div></details>')

        show('<div class="section-title">Sources</div>' + sources_html(sources))
else:
    show('<p class="how"><b>Why two passes?</b> AI writing tools sometimes state things '
         "confidently that their sources never said. Here, a second pass reads the draft "
         "like an editor with the source pages open, and only what it can confirm reaches "
         "the answer above.</p>")
