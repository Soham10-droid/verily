"""Visual identity for Verily — v3.

A bespoke editorial product look (warm paper, deep charcoal ink, a serif
headline paired with a geometric sans) rather than a default Streamlit
prototype. Every native Streamlit widget (the form, the buttons, the
toggle, the expander, the download button) is reskinned in place so the
page reads as one designed surface instead of a stack of default controls.
"""

LIGHT = {
    "bg": "#FAF8F5", "surface": "#FFFFFF", "sunken": "#F2EEE6",
    "ink": "#1F2421", "muted": "#6B7570", "line": "#E8E2D6",
    "accent": "#2563EB", "accent-soft": "#EEF3FD", "accent-ring": "#D7E4FB",
    "accent-hover": "#1D4ED8", "accent-border": "#9DBBF5",
    "btn": "#1F2421", "btn-text": "#FFFFFF",
    "ok": "#16A34A", "ok-bg": "#DFF3E6",
    "warn": "#B4740E", "warn-bg": "#FBF0D9",
    "bad": "#C23B2E", "bad-bg": "#FBE6E2",
    "shadow": "31, 36, 33",
}

DARK = {
    "bg": "#1B1915", "surface": "#232019", "sunken": "#2A2620",
    "ink": "#F3EFE6", "muted": "#9A9284", "line": "#3A352C",
    "accent": "#6C93FF", "accent-soft": "#20243A", "accent-ring": "#2B3760",
    "accent-hover": "#8FACFF", "accent-border": "#4C5F99",
    "btn": "#6C93FF", "btn-text": "#10131F",
    "ok": "#5FCB86", "ok-bg": "#17301F",
    "warn": "#E8B85B", "warn-bg": "#3A2E10",
    "bad": "#F08072", "bad-bg": "#3B1C17",
    "shadow": "0, 0, 0",
}

GITHUB_ICON = (
    '<svg viewBox="0 0 16 16" width="16" height="16" fill="currentColor">'
    '<path d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 '
    '0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 '
    '1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 '
    '0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 '
    '2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 '
    '3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.01 8.01 0 0 0 16 8c0-4.42-3.58-8-8-8z"/>'
    '</svg>'
)


def css(dark=False):
    p = DARK if dark else LIGHT
    variables = "\n".join(f"  --{k}: {v};" for k, v in p.items())
    return f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Newsreader:ital,opsz,wght@0,6..72,400;0,6..72,600;1,6..72,500&family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap');

:root {{
{variables}
  --display: 'Newsreader', Georgia, serif;
  --sans: 'Plus Jakarta Sans', system-ui, -apple-system, sans-serif;
  color-scheme: {'dark' if dark else 'light'};
}}

/* ================= chrome removal ================= */
.stApp {{ background: var(--bg); color: var(--ink); font-family: var(--sans); }}
[data-testid="stHeader"] {{ background: transparent; }}
#MainMenu, footer, [data-testid="stDecoration"], [data-testid="stStatusWidget"],
.viewerBadge_container__r5tak, .viewerBadge_link__qRIco {{ display: none !important; }}
.block-container, [data-testid="stMainBlockContainer"] {{
  max-width: 720px; padding-top: 2.6rem; padding-bottom: 6rem;
}}
.stApp p, .stApp li, .stApp label, .stApp div, .stApp button, .stApp input {{
  font-family: var(--sans); color: var(--ink);
}}
[data-testid="stWidgetLabel"] p {{ color: var(--muted); }}
::selection {{ background: var(--accent-ring); color: var(--ink); }}

@media (prefers-reduced-motion: reduce) {{
  * {{ animation-duration: .001ms !important; animation-iteration-count: 1 !important; transition-duration: .001ms !important; }}
}}

/* ================= header row ================= */
.mast-wrap {{ opacity: 0; animation: riseIn .6s cubic-bezier(.16,1,.3,1) forwards; }}
.mast {{ display: flex; align-items: center; gap: .9rem; flex-wrap: wrap; margin: 0; }}
.mast h1 {{
  font-family: var(--display); font-style: italic; font-weight: 500;
  font-size: 2.6rem; letter-spacing: -0.01em; line-height: 1; margin: 0; color: var(--ink);
}}
.status-pill {{
  display: inline-flex; align-items: center; gap: .45rem; font-family: var(--sans);
  font-size: .76rem; font-weight: 600; color: var(--ok); background: var(--ok-bg);
  border-radius: 999px; padding: .3rem .75rem .3rem .62rem;
}}
.status-dot {{ width: .42rem; height: .42rem; border-radius: 50%; background: var(--ok);
  animation: statusPulse 2.2s ease-in-out infinite; }}
@keyframes statusPulse {{ 0%, 100% {{ opacity: 1; }} 50% {{ opacity: .35; }} }}

.gh-link {{
  display: inline-flex; align-items: center; justify-content: center; width: 2.1rem; height: 2.1rem;
  border-radius: 10px; color: var(--muted); border: 1px solid var(--line); background: var(--surface);
  transition: color .15s, border-color .15s; text-decoration: none;
}}
.gh-link:hover {{ color: var(--ink); border-color: var(--accent-border); }}

@keyframes riseIn {{ from {{ opacity: 0; transform: translateY(8px); }} to {{ opacity: 1; transform: translateY(0); }} }}

/* ================= stage flow (replaces the intro paragraph) ================= */
.stage-flow {{
  opacity: 0; animation: riseIn .6s cubic-bezier(.16,1,.3,1) .1s forwards;
  display: flex; align-items: center; gap: .6rem; flex-wrap: wrap; margin: 1.3rem 0 1.7rem;
}}
.stage {{
  font-family: var(--sans); font-weight: 500; font-size: .82rem; color: var(--ink);
  background: var(--surface); border: 1px solid var(--line); border-radius: 999px;
  padding: .38rem .9rem;
}}
.stage b {{ color: var(--accent); font-weight: 700; margin-right: .3rem; }}
.stage-flow .arrow {{ color: var(--muted); font-size: 1rem; }}

[data-testid="stExpander"] {{
  opacity: 0; animation: riseIn .6s ease .16s forwards;
  border: 1px solid var(--line) !important; border-radius: 14px !important;
  background: var(--surface) !important; margin-bottom: 1.8rem;
}}
[data-testid="stExpander"] summary {{ font-family: var(--sans); font-weight: 600; color: var(--ink); }}
[data-testid="stExpander"] p {{ font-size: .96rem; line-height: 1.65; color: var(--muted); }}
[data-testid="stExpander"] b {{ color: var(--ink); font-weight: 600; }}
[data-testid="stExpander"] code {{ background: var(--sunken); color: var(--ink); padding: .05rem .35rem; border-radius: 4px; }}

/* ================= fused search card ================= */
[data-testid="stForm"] {{
  border: 1px solid var(--line) !important; border-radius: 22px !important;
  background: var(--surface) !important; padding: .5rem .5rem .5rem 1.3rem !important;
  box-shadow: 0 10px 30px rgba(var(--shadow), .07); transition: box-shadow .2s, border-color .2s;
}}
[data-testid="stForm"]:focus-within {{
  border-color: var(--accent-border) !important;
  box-shadow: 0 10px 30px rgba(var(--shadow), .07), 0 0 0 4px var(--accent-ring);
}}
[data-testid="stForm"] [data-testid="stHorizontalBlock"] {{ align-items: center; gap: .5rem; }}
[data-testid="stForm"] [data-baseweb="input"], [data-testid="stForm"] [data-baseweb="base-input"] {{
  background: transparent !important; border: none !important; box-shadow: none !important;
}}
[data-testid="stForm"] [data-testid="stTextInput"] input {{
  background: transparent !important; color: var(--ink) !important; -webkit-text-fill-color: var(--ink);
  caret-color: var(--accent); font-family: var(--sans); font-size: 1.1rem; padding: .7rem .2rem;
}}
[data-testid="stForm"] [data-testid="stTextInput"] input::placeholder {{ color: var(--muted); opacity: .7; }}

/* inner wrappers Streamlit/BaseWeb paint with the theme's own colour */
[data-testid="stForm"] [data-baseweb="input"] > div,
[data-testid="stForm"] [data-baseweb="base-input"] > div,
[data-testid="stForm"] [data-testid="stTextInputRootElement"] {{
  background: transparent !important; background-color: transparent !important;
}}

/* browser autofill paints the box light blue and hides dark-mode text */
[data-testid="stForm"] input:-webkit-autofill,
[data-testid="stForm"] input:-webkit-autofill:hover,
[data-testid="stForm"] input:-webkit-autofill:focus {{
  -webkit-box-shadow: 0 0 0 1000px var(--surface) inset !important;
  -webkit-text-fill-color: var(--ink) !important;
  caret-color: var(--accent);
  transition: background-color 9999s ease-in-out 0s;
}}

/* hide Streamlit's "Press Enter to submit form" hint */
[data-testid="InputInstructions"] {{ display: none !important; }}

/* belt-and-braces: force the typed text and box colours on EVERY state of
   EVERY text input, so no theme default, focus style or autofill can win */
.stApp [data-testid="stTextInput"] input,
.stApp [data-testid="stTextInput"] input:focus,
.stApp [data-testid="stTextInput"] input:active,
.stApp [data-testid="stTextInput"] input:hover {{
  background-color: var(--surface) !important;
  color: var(--ink) !important;
  -webkit-text-fill-color: var(--ink) !important;
  opacity: 1 !important;
}}
.stApp [data-testid="stTextInput"] div {{ background-color: transparent !important; }}

[data-testid="stFormSubmitButton"] button {{
  width: 100%; height: 2.95rem; border-radius: 16px; border: none; white-space: nowrap;
  background: var(--btn); color: var(--btn-text); font-family: var(--sans);
  font-weight: 600; font-size: .98rem; padding: 0 1.3rem; transition: background .18s;
}}
[data-testid="stFormSubmitButton"] button p {{ color: var(--btn-text) !important; }}
[data-testid="stFormSubmitButton"] button:hover {{ background: var(--accent-hover); }}
[data-testid="stFormSubmitButton"] button:focus-visible {{ outline: 3px solid var(--accent); outline-offset: 2px; }}

/* ================= chips (examples + history) ================= */
.stButton button {{
  background: var(--surface); border: 1px solid var(--line); border-radius: 999px;
  color: var(--ink); font-family: var(--sans); font-weight: 500; font-size: .88rem;
  padding: .5rem 1.05rem; min-height: 0; white-space: nowrap;
  transition: transform .15s cubic-bezier(.34,1.56,.64,1), border-color .15s, background .15s, box-shadow .15s;
}}
.stButton button p {{ white-space: nowrap !important; overflow: visible !important; text-overflow: unset !important; }}
.stButton button:hover {{
  transform: translateY(-2px); border-color: var(--accent-border); background: var(--accent-soft);
  box-shadow: 0 8px 16px -6px rgba(var(--shadow), .18);
}}
.stButton button:hover p {{ color: var(--accent-hover) !important; }}
.stApp p.chip-label {{ font-size: .78rem; color: var(--muted); margin: .9rem 0 .45rem .2rem; font-weight: 600; letter-spacing: .01em; }}

/* ================= progress ================= */
.steps {{ list-style: none; padding: 0; margin: 1.6rem 0 0; counter-reset: s; }}
.steps li {{
  counter-increment: s; display: flex; gap: .8rem; align-items: baseline;
  padding: .34rem 0; color: var(--muted); font-size: .96rem;
  opacity: 0; animation: riseIn .4s ease forwards;
}}
.steps li:nth-child(1) {{ animation-delay: .02s; }}
.steps li:nth-child(2) {{ animation-delay: .06s; }}
.steps li:nth-child(3) {{ animation-delay: .10s; }}
.steps li:nth-child(4) {{ animation-delay: .14s; }}
.steps li:nth-child(5) {{ animation-delay: .18s; }}
.steps li:nth-child(6) {{ animation-delay: .22s; }}
.steps li::before {{
  content: counter(s); flex: 0 0 1.55rem; height: 1.55rem; line-height: 1.45rem;
  text-align: center; border-radius: 50%; border: 1.5px solid var(--line);
  font-family: var(--sans); font-size: .78rem; font-weight: 600;
}}
.steps li.active {{ color: var(--ink); font-weight: 600; }}
.steps li.active::before {{ border-color: var(--accent); color: var(--accent); animation: pulse 1.3s ease-in-out infinite; }}
.steps li.done {{ color: var(--muted); }}
.steps li.done::before {{ content: "✓"; background: var(--ok-bg); border-color: var(--ok-bg); color: var(--ok); }}
.steps .note {{ font-weight: 400; color: var(--muted); font-size: .9rem; }}
@keyframes pulse {{ 50% {{ box-shadow: 0 0 0 6px var(--accent-ring); }} }}

/* ================= the answer ================= */
.asked {{
  opacity: 0; animation: riseIn .5s cubic-bezier(.16,1,.3,1) forwards;
  margin: 2.4rem 0 1rem; font-family: var(--display); font-style: italic; font-weight: 500;
  font-size: 1.55rem; letter-spacing: -0.005em; line-height: 1.3; color: var(--ink);
}}
.answer-wrap {{
  position: relative; opacity: 0; animation: riseIn .5s cubic-bezier(.16,1,.3,1) .06s forwards;
}}
.answer {{
  background: var(--surface); border: 1px solid var(--line); border-left: 3px solid var(--accent);
  border-radius: 18px; padding: 1.5rem 1.7rem 1.3rem;
  box-shadow: 0 10px 30px rgba(var(--shadow), .06);
}}
.answer p, .answer li {{
  font-family: var(--sans); font-size: 1.05rem; line-height: 1.68; color: var(--ink); margin: 0 0 .9rem;
}}
.answer ul {{ margin: 0 0 .9rem 1.15rem; padding: 0; }}
.answer h4 {{ font-family: var(--sans); font-weight: 600; font-size: 1.05rem; margin: 1rem 0 .4rem; color: var(--ink); }}
.cite {{
  font-family: var(--sans); font-size: .66em; font-weight: 700; color: var(--accent);
  background: var(--accent-soft); border-radius: 4px; padding: 0 .32em; margin-left: .12em;
  text-decoration: none; vertical-align: super; line-height: 1; transition: background .15s, color .15s;
}}
.cite:hover {{ background: var(--accent); color: var(--surface) !important; }}

.stamp {{
  position: absolute; top: -.65rem; right: 1.1rem; font-family: var(--sans);
  font-weight: 600; font-size: .78rem; color: var(--ok); background: var(--surface);
  border: 1.5px solid var(--ok-bg); border-radius: 999px; padding: .28rem .85rem;
  box-shadow: 0 2px 6px rgba(var(--shadow), .08);
  transform: scale(0); animation: stampIn .4s cubic-bezier(.34,1.56,.64,1) .45s forwards;
}}
@keyframes stampIn {{ to {{ transform: scale(1); }} }}

.stApp p.tally {{ margin: .85rem .1rem 0; color: var(--muted); font-family: var(--sans); font-size: .95rem; }}
.tally b {{ color: var(--ink); font-weight: 600; }}
.tally .confidence {{
  display: inline-block; margin-left: .5rem; padding: .08rem .55rem; border-radius: 999px;
  background: var(--accent-soft); color: var(--accent); font-weight: 600; font-size: .82rem;
}}

/* ================= trust badges + conflicts ================= */
.trust-badge {{
  display: inline-block; font-family: var(--sans); font-size: .68rem; font-weight: 600;
  border-radius: 999px; padding: .06rem .5rem; margin: 0 .4rem; vertical-align: middle;
}}
.trust-badge.high {{ background: var(--ok-bg); color: var(--ok); }}
.trust-badge.medium {{ background: var(--accent-soft); color: var(--accent); }}
.trust-badge.low {{ background: var(--warn-bg); color: var(--warn); }}

.conflict-box {{
  margin-top: 1.1rem; padding: .95rem 1.2rem; border-radius: 14px;
  background: var(--warn-bg); border-left: 3px solid var(--warn); color: var(--ink);
}}
.conflict-box b {{ color: var(--warn); display: block; margin-bottom: .3rem; font-size: .95rem; }}
.conflict-item {{ font-size: .92rem; line-height: 1.5; margin-top: .3rem; }}
.conflict-src {{ color: var(--muted); }}

/* ================= claim markup ================= */
.section-title {{
  font-family: var(--sans); font-weight: 600; font-size: 1.1rem; margin: 2.8rem 0 .3rem; color: var(--ink);
}}
.stApp p.section-sub {{ color: var(--muted); font-size: .92rem; margin: 0 0 .3rem; }}
.claim-list {{ margin-top: .6rem; }}
.claim {{
  padding: 1rem 0 1.05rem; border-top: 1px solid var(--line);
  opacity: 0; animation: riseIn .4s cubic-bezier(.16,1,.3,1) forwards;
}}
.claim-list .claim:nth-child(1) {{ animation-delay: .04s; }}
.claim-list .claim:nth-child(2) {{ animation-delay: .09s; }}
.claim-list .claim:nth-child(3) {{ animation-delay: .14s; }}
.claim-list .claim:nth-child(4) {{ animation-delay: .19s; }}
.claim-list .claim:nth-child(5) {{ animation-delay: .24s; }}
.claim-list .claim:nth-child(6) {{ animation-delay: .29s; }}
.claim-list .claim:nth-child(7) {{ animation-delay: .34s; }}
.claim-list .claim:nth-child(8) {{ animation-delay: .39s; }}
.claim:last-child {{ border-bottom: 1px solid var(--line); }}
.claim .text {{ font-family: var(--sans); font-size: 1rem; line-height: 1.6; color: var(--ink); }}
.claim.supported .text .c {{ background-image: linear-gradient(var(--ok), var(--ok)); background-repeat: no-repeat; background-position: 0 100%; background-size: 0% 2px; animation: sweep .5s ease .15s forwards; }}
.claim.partial .text .c {{ background: var(--warn-bg); box-decoration-break: clone; -webkit-box-decoration-break: clone; padding: .04em .15em; border-radius: 3px; }}
.claim.unsupported .text .c {{ text-decoration: line-through; text-decoration-color: var(--bad); text-decoration-thickness: 2px; color: var(--muted); }}
@keyframes sweep {{ to {{ background-size: 100% 2px; }} }}
.claim .verdict {{
  display: inline-block; font-family: var(--sans); font-size: .74rem; font-weight: 600;
  border-radius: 999px; padding: .12rem .6rem; margin-right: .5rem;
}}
.claim.supported .verdict {{ background: var(--ok-bg); color: var(--ok); }}
.claim.partial .verdict {{ background: var(--warn-bg); color: var(--warn); }}
.claim.unsupported .verdict {{ background: var(--bad-bg); color: var(--bad); }}
.claim .why {{ margin-top: .5rem; font-size: .9rem; color: var(--muted); line-height: 1.5; }}
.claim .fix {{ margin-top: .5rem; font-size: .95rem; color: var(--ink); padding-left: .85rem; border-left: 2px solid var(--accent); line-height: 1.5; }}

/* ================= draft + sources ================= */
details.draft {{ margin-top: 1.5rem; border: 1px solid var(--line); border-radius: 14px; background: var(--sunken); }}
details.draft summary {{ cursor: pointer; padding: .8rem 1.05rem; color: var(--muted); font-weight: 600; font-size: .92rem; list-style: none; }}
details.draft summary::-webkit-details-marker {{ display: none; }}
details.draft summary::before {{ content: "→ "; color: var(--accent); }}
details.draft[open] summary::before {{ content: "↓ "; }}
details.draft summary:focus-visible {{ outline: 3px solid var(--accent); border-radius: 10px; }}
details.draft .body {{ padding: 0 1.15rem .6rem; }}
details.draft .body p, details.draft .body li {{ font-family: var(--sans); color: var(--muted); font-size: .98rem; line-height: 1.6; }}

.sources {{ list-style: none; padding: 0; margin: 0; }}
.sources li {{
  display: grid; grid-template-columns: 1.9rem 1fr; gap: .18rem .6rem; padding: .75rem 0;
  border-top: 1px solid var(--line);
}}
.sources .n {{ font-family: var(--sans); color: var(--accent); font-weight: 700; font-size: .95rem; }}
.sources .title-row {{ display: flex; align-items: center; flex-wrap: wrap; }}
.sources a {{ color: var(--ink) !important; font-weight: 600; text-decoration: none; line-height: 1.35; transition: color .15s; }}
.sources a:hover {{ color: var(--accent) !important; text-decoration: underline; }}
.sources .dom {{ grid-column: 2; color: var(--muted); font-size: .85rem; }}

[data-testid="stDownloadButton"] button {{
  background: var(--surface); border: 1px solid var(--line); border-radius: 14px;
  color: var(--ink); font-family: var(--sans); font-weight: 600; font-size: .92rem;
  margin-top: 1.6rem; transition: border-color .16s, background .16s;
}}
[data-testid="stDownloadButton"] button p {{ color: var(--ink) !important; }}
[data-testid="stDownloadButton"] button:hover {{ background: var(--accent-soft); border-color: var(--accent-border); }}

/* ================= messages ================= */
.notice {{
  margin-top: 1.7rem; padding: 1.05rem 1.25rem; border-radius: 14px; background: var(--bad-bg);
  color: var(--ink); line-height: 1.55; border-left: 3px solid var(--bad);
}}
.notice b {{ color: var(--bad); }}
.notice code {{ background: var(--surface); color: var(--ink); padding: .06rem .38rem; border-radius: 4px; font-size: .92em; }}

/* ================= expander: kill Streamlit's pale default header ================= */
[data-testid="stExpander"] details {{ border: none !important; background: transparent !important; }}
[data-testid="stExpander"] summary, [data-testid="stExpanderHeader"] {{
  background: var(--surface) !important; border-radius: 14px !important; padding: .85rem 1.1rem !important;
}}
[data-testid="stExpander"] summary:hover {{ background: var(--sunken) !important; }}
[data-testid="stExpander"] summary p, [data-testid="stExpander"] summary span {{
  color: var(--ink) !important; font-weight: 600 !important; font-size: .93rem !important;
}}
[data-testid="stExpander"] summary svg {{ color: var(--muted) !important; fill: var(--muted) !important; }}
[data-testid="stExpanderDetails"] {{ background: transparent !important; }}

/* ================= search input: no box-inside-a-box ================= */
[data-testid="stForm"] [data-testid="stTextInput"] *,
[data-testid="stForm"] [data-testid="stTextInput"] *:focus,
[data-testid="stForm"] [data-testid="stTextInput"] *:focus-within {{
  border: none !important; box-shadow: none !important; outline: none !important;
}}
[data-testid="stForm"] [data-testid="stTextInput"] input {{ background-color: transparent !important; }}

/* dark-mode toggle */
[data-testid="stToggle"] label p, .stCheckbox label p {{ color: var(--muted) !important; font-size: .85rem; }}
[data-testid="stToggle"] {{ display: flex; justify-content: flex-end; }}

@media (max-width: 640px) {{
  .mast h1 {{ font-size: 2.1rem; }}
  .answer {{ padding: 1.2rem 1.2rem 1.05rem; }}
  .answer p, .answer li {{ font-size: 1rem; }}
  .stamp {{ position: static; display: inline-block; margin-top: .6rem; transform: scale(1); animation: none; }}
  [data-testid="stForm"] {{ padding: .5rem !important; border-radius: 18px !important; }}
}}
</style>
"""
