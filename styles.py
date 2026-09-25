"""Visual identity for Verily.

Concept: an editor's red pen, not a chat UI. Warm paper tones, a serif
built for headlines (Fraunces), a geometric sans for UI chrome (Space
Grotesk), and Source Serif for the long-form reading text. Verdicts read
like pen marks on a manuscript: underlined, highlighted, struck through.
One staggered reveal on load; everything else stays still.
"""

LIGHT = {
    "bg": "#E4DFCF", "surface": "#FBF9F2", "sunken": "#D9D3C0",
    "ink": "#211C15", "muted": "#6C6353", "line": "#CFC7B1",
    "pencil": "#A22C1C", "pencil-soft": "#F3DAD2",
    "ok": "#38623C", "ok-bg": "#DCE7D7",
    "warn": "#8A5A12", "warn-bg": "#F2E1B8",
    "bad": "#A22C1C", "bad-bg": "#F3DAD2",
    "shadow": "20, 16, 8",
}

DARK = {
    "bg": "#16130E", "surface": "#211C15", "sunken": "#2A2318",
    "ink": "#EEE7D8", "muted": "#9C9280",
    "line": "#392F20",
    "pencil": "#FF7A5C", "pencil-soft": "#3B2019",
    "ok": "#8FCB8F", "ok-bg": "#1F3320",
    "warn": "#EEC06A", "warn-bg": "#3A2D11",
    "bad": "#FF7A5C", "bad-bg": "#3B2019",
    "shadow": "0, 0, 0",
}


def css(dark=False):
    p = DARK if dark else LIGHT
    variables = "\n".join(f"  --{k}: {v};" for k, v in p.items())
    return f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,400;0,9..144,600;0,9..144,700;1,9..144,500&family=Space+Grotesk:wght@400;500;600;700&family=Source+Serif+4:ital,opsz,wght@0,8..60,400;0,8..60,600;1,8..60,400&display=swap');

:root {{
{variables}
  --display: 'Fraunces', Georgia, serif;
  --sans: 'Space Grotesk', system-ui, sans-serif;
  --serif: 'Source Serif 4', Georgia, 'Times New Roman', serif;
}}

/* ================= reset / page ================= */
.stApp {{ background: var(--bg); color: var(--ink); font-family: var(--sans); }}
[data-testid="stHeader"] {{ background: transparent; }}
#MainMenu, footer, [data-testid="stDecoration"] {{ display: none; }}
.block-container, [data-testid="stMainBlockContainer"] {{
  max-width: 780px; padding-top: 3rem; padding-bottom: 6rem;
}}
.stApp p, .stApp li, .stApp label, .stApp div, .stApp button, .stApp input {{
  font-family: var(--sans); color: var(--ink);
}}
[data-testid="stWidgetLabel"] p {{ color: var(--muted); }}
::selection {{ background: var(--pencil-soft); color: var(--ink); }}

@media (prefers-reduced-motion: reduce) {{
  * {{ animation-duration: .001ms !important; animation-iteration-count: 1 !important; transition-duration: .001ms !important; }}
}}

/* ================= masthead ================= */
.mast-wrap {{ opacity: 0; animation: riseIn .7s cubic-bezier(.16,1,.3,1) forwards; }}
.mast {{ display: flex; align-items: center; gap: .55rem; margin: 0; }}
.mast h1 {{
  font-family: var(--display); font-weight: 600; font-style: italic;
  font-size: 3rem; letter-spacing: -0.01em; line-height: 1; margin: 0; color: var(--ink);
}}
.mast .dot {{
  width: .42rem; height: .42rem; border-radius: 50%; background: var(--pencil);
  transform: translateY(-1rem); flex-shrink: 0;
  animation: dotIn .5s cubic-bezier(.34,1.56,.64,1) .55s backwards;
}}
.rule {{ height: 2px; background: var(--pencil); width: 3.1rem; margin: .7rem 0 1.15rem;
  transform-origin: left; animation: growLine .6s cubic-bezier(.16,1,.3,1) .25s backwards; }}
.lede {{
  opacity: 0; animation: riseIn .7s cubic-bezier(.16,1,.3,1) .12s forwards;
  color: var(--muted); font-size: 1.08rem; line-height: 1.55;
  max-width: 36em; margin: 0 0 1.9rem;
}}

@keyframes riseIn {{ from {{ opacity: 0; transform: translateY(10px); }} to {{ opacity: 1; transform: translateY(0); }} }}
@keyframes dotIn {{ from {{ opacity: 0; transform: translateY(-1rem) scale(.3); }} to {{ opacity: 1; transform: translateY(0) scale(1); }} }}
@keyframes growLine {{ from {{ transform: scaleX(0); }} to {{ transform: scaleX(1); }} }}

/* ================= input row ================= */
[data-testid="stTextInput"] input {{
  background: var(--surface) !important; color: var(--ink) !important;
  -webkit-text-fill-color: var(--ink); caret-color: var(--pencil);
  font-family: var(--serif); font-size: 1.12rem; padding: .85rem 1rem;
}}
[data-testid="stTextInput"] input::placeholder {{ color: var(--muted); opacity: .75; font-style: italic; }}
[data-baseweb="input"], [data-baseweb="base-input"] {{
  background: var(--surface) !important; border-color: var(--line) !important;
  border-radius: 3px !important; transition: border-color .2s, box-shadow .2s;
}}
[data-baseweb="input"]:focus-within {{
  border-color: var(--pencil) !important; box-shadow: 0 0 0 3px var(--pencil-soft) !important;
}}

[data-testid="stFormSubmitButton"] button {{
  width: 100%; height: 3.15rem; border-radius: 3px; border: 1.5px solid var(--ink);
  background: var(--ink); color: var(--bg); font-family: var(--sans);
  font-weight: 600; font-size: 1rem; transition: transform .18s cubic-bezier(.34,1.56,.64,1), background .18s, box-shadow .18s;
}}
[data-testid="stFormSubmitButton"] button p {{ color: var(--bg) !important; }}
[data-testid="stFormSubmitButton"] button:hover {{
  background: var(--pencil); border-color: var(--pencil); transform: translateY(-2px);
  box-shadow: 0 6px 14px rgba(var(--shadow), .22);
}}
[data-testid="stFormSubmitButton"] button:active {{ transform: translateY(0); }}
[data-testid="stFormSubmitButton"] button:focus-visible {{ outline: 3px solid var(--pencil); outline-offset: 2px; }}

.stButton button {{
  background: transparent; border: 1px solid var(--line); border-radius: 3px;
  color: var(--muted); font-family: var(--serif); font-style: italic; font-size: .92rem;
  padding: .32rem .75rem; min-height: 0; transition: border-color .18s, color .18s, transform .18s;
}}
.stButton button p {{ color: var(--muted) !important; font-family: var(--serif); font-style: italic; }}
.stButton button:hover {{ border-color: var(--pencil); color: var(--pencil); transform: translateY(-1px); }}
.stButton button:hover p {{ color: var(--pencil) !important; }}

/* ================= progress ================= */
.steps {{ list-style: none; padding: 0; margin: 1.6rem 0 0; counter-reset: s; }}
.steps li {{
  counter-increment: s; display: flex; gap: .8rem; align-items: baseline;
  padding: .34rem 0; color: var(--muted); font-size: .98rem;
  opacity: 0; animation: riseIn .4s ease forwards;
}}
.steps li:nth-child(1) {{ animation-delay: .02s; }}
.steps li:nth-child(2) {{ animation-delay: .06s; }}
.steps li:nth-child(3) {{ animation-delay: .10s; }}
.steps li:nth-child(4) {{ animation-delay: .14s; }}
.steps li:nth-child(5) {{ animation-delay: .18s; }}
.steps li::before {{
  content: counter(s); flex: 0 0 1.6rem; height: 1.6rem; line-height: 1.5rem;
  text-align: center; border-radius: 50%; border: 1.5px solid var(--line);
  font-family: var(--sans); font-size: .8rem; font-weight: 600;
}}
.steps li.active {{ color: var(--ink); font-weight: 600; }}
.steps li.active::before {{ border-color: var(--pencil); color: var(--pencil); animation: pulse 1.3s ease-in-out infinite; }}
.steps li.done {{ color: var(--muted); }}
.steps li.done::before {{ content: "✓"; background: var(--ok-bg); border-color: var(--ok-bg); color: var(--ok); }}
.steps .note {{ font-weight: 400; font-style: italic; font-family: var(--serif); color: var(--muted); font-size: .92rem; }}
@keyframes pulse {{ 50% {{ box-shadow: 0 0 0 6px var(--pencil-soft); }} }}

/* ================= the answer ================= */
.asked {{
  opacity: 0; animation: riseIn .5s cubic-bezier(.16,1,.3,1) forwards;
  margin: 2.5rem 0 1rem; font-family: var(--display); font-style: italic; font-weight: 500;
  font-size: 1.65rem; letter-spacing: -0.01em; line-height: 1.3; color: var(--ink);
}}
.answer-wrap {{
  position: relative; opacity: 0; animation: riseIn .55s cubic-bezier(.16,1,.3,1) .06s forwards;
}}
.answer {{
  background: var(--surface); border: 1px solid var(--line); border-left: 3px solid var(--pencil);
  border-radius: 2px 12px 12px 2px; padding: 1.5rem 1.7rem 1.3rem;
  box-shadow: 0 1px 2px rgba(var(--shadow), .06), 0 10px 24px -14px rgba(var(--shadow), .28);
}}
.answer p, .answer li {{
  font-family: var(--serif); font-size: 1.14rem; line-height: 1.7; color: var(--ink); margin: 0 0 .9rem;
}}
.answer ul {{ margin: 0 0 .9rem 1.15rem; padding: 0; }}
.answer h4 {{ font-family: var(--display); font-weight: 600; font-size: 1.15rem; margin: 1rem 0 .4rem; color: var(--ink); }}
.cite {{
  font-family: var(--sans); font-size: .66em; font-weight: 700; color: var(--pencil);
  background: var(--pencil-soft); border-radius: 3px; padding: 0 .32em; margin-left: .12em;
  text-decoration: none; vertical-align: super; line-height: 1; transition: background .15s, color .15s;
}}
.cite:hover {{ background: var(--pencil); color: var(--surface) !important; }}

.stamp {{
  position: absolute; top: -.7rem; right: 1.1rem; font-family: var(--display); font-style: italic;
  font-weight: 600; font-size: .82rem; color: var(--ok); background: var(--surface);
  border: 1.5px solid var(--ok); border-radius: 999px; padding: .25rem .8rem;
  transform: rotate(-4deg) scale(0); animation: stampIn .45s cubic-bezier(.34,1.56,.64,1) .5s forwards;
}}
@keyframes stampIn {{ to {{ transform: rotate(-4deg) scale(1); }} }}

.tally {{ margin: .85rem .1rem 0; color: var(--muted); font-family: var(--serif); font-style: italic; font-size: .98rem; }}
.tally b {{ color: var(--ink); font-weight: 600; font-style: normal; }}

/* ================= claim markup ================= */
.section-title {{
  font-family: var(--display); font-weight: 600; font-size: 1.2rem; margin: 3rem 0 .3rem; color: var(--ink);
}}
.section-sub {{ color: var(--muted); font-size: .93rem; margin: 0 0 .3rem; }}
.claim-list {{ margin-top: .7rem; }}
.claim {{
  padding: 1rem 0 1.05rem; border-top: 1px solid var(--line);
  opacity: 0; animation: riseIn .45s cubic-bezier(.16,1,.3,1) forwards;
}}
.claim-list .claim:nth-child(1) {{ animation-delay: .04s; }}
.claim-list .claim:nth-child(2) {{ animation-delay: .09s; }}
.claim-list .claim:nth-child(3) {{ animation-delay: .14s; }}
.claim-list .claim:nth-child(4) {{ animation-delay: .19s; }}
.claim-list .claim:nth-child(5) {{ animation-delay: .24s; }}
.claim-list .claim:nth-child(6) {{ animation-delay: .29s; }}
.claim-list .claim:nth-child(7) {{ animation-delay: .34s; }}
.claim-list .claim:nth-child(8) {{ animation-delay: .39s; }}
.claim-list .claim:nth-child(9) {{ animation-delay: .44s; }}
.claim-list .claim:nth-child(10) {{ animation-delay: .49s; }}
.claim:last-child {{ border-bottom: 1px solid var(--line); }}
.claim .text {{ font-family: var(--serif); font-size: 1.05rem; line-height: 1.6; color: var(--ink); }}
.claim.supported .text .c {{ background-image: linear-gradient(var(--ok), var(--ok)); background-repeat: no-repeat; background-position: 0 100%; background-size: 0% 2px; animation: sweep .5s ease .15s forwards; }}
.claim.partial .text .c {{ background: var(--warn-bg); box-decoration-break: clone; -webkit-box-decoration-break: clone; padding: .04em .15em; border-radius: 2px; }}
.claim.unsupported .text .c {{ text-decoration: line-through; text-decoration-color: var(--bad); text-decoration-thickness: 2px; color: var(--muted); }}
@keyframes sweep {{ to {{ background-size: 100% 2px; }} }}
.claim .verdict {{
  display: inline-block; font-family: var(--sans); font-size: .76rem; font-weight: 700;
  border-radius: 3px; padding: .1rem .5rem; margin-right: .5rem; transform: rotate(-1.5deg);
}}
.claim.supported .verdict {{ background: var(--ok-bg); color: var(--ok); }}
.claim.partial .verdict {{ background: var(--warn-bg); color: var(--warn); }}
.claim.unsupported .verdict {{ background: var(--bad-bg); color: var(--bad); }}
.claim .why {{ margin-top: .5rem; font-size: .92rem; color: var(--muted); line-height: 1.5; }}
.claim .fix {{ margin-top: .5rem; font-size: .96rem; color: var(--ink); padding-left: .85rem; border-left: 2px solid var(--pencil); line-height: 1.5; font-family: var(--serif); }}

/* ================= draft + sources ================= */
details.draft {{ margin-top: 1.6rem; border: 1px solid var(--line); border-radius: 8px; background: var(--sunken); }}
details.draft summary {{ cursor: pointer; padding: .8rem 1.05rem; color: var(--muted); font-weight: 600; font-size: .93rem; list-style: none; }}
details.draft summary::-webkit-details-marker {{ display: none; }}
details.draft summary::before {{ content: "→ "; color: var(--pencil); }}
details.draft[open] summary::before {{ content: "↓ "; }}
details.draft summary:focus-visible {{ outline: 3px solid var(--pencil); border-radius: 8px; }}
details.draft .body {{ padding: 0 1.15rem .6rem; }}
details.draft .body p, details.draft .body li {{ font-family: var(--serif); color: var(--muted); font-size: 1rem; line-height: 1.6; }}

.sources {{ list-style: none; padding: 0; margin: 0; }}
.sources li {{
  display: grid; grid-template-columns: 1.9rem 1fr; gap: .18rem .6rem; padding: .75rem 0;
  border-top: 1px solid var(--line);
}}
.sources .n {{ font-family: var(--display); font-style: italic; color: var(--pencil); font-weight: 600; font-size: 1rem; }}
.sources a {{ color: var(--ink) !important; font-weight: 600; text-decoration: none; line-height: 1.35; transition: color .15s; }}
.sources a:hover {{ color: var(--pencil) !important; text-decoration: underline; }}
.sources .dom {{ grid-column: 2; color: var(--muted); font-size: .85rem; }}

/* ================= messages ================= */
.notice {{
  margin-top: 1.7rem; padding: 1.05rem 1.25rem; border-radius: 8px; background: var(--bad-bg);
  color: var(--ink); line-height: 1.55; border-left: 3px solid var(--bad);
}}
.notice b {{ color: var(--bad); }}
.notice code {{ background: var(--surface); color: var(--ink); padding: .06rem .38rem; border-radius: 4px; font-size: .92em; }}
.how {{
  opacity: 0; animation: riseIn .6s ease .18s forwards;
  margin-top: 2.8rem; padding-top: 1.6rem; border-top: 1px solid var(--line);
  color: var(--muted); font-family: var(--serif); font-size: 1rem; line-height: 1.65; max-width: 38em;
}}
.how b {{ color: var(--ink); font-weight: 600; font-family: var(--sans); }}

/* dark-mode toggle */
[data-testid="stToggle"] label p, .stCheckbox label p {{ color: var(--muted) !important; font-size: .88rem; }}

@media (max-width: 640px) {{
  .mast h1 {{ font-size: 2.3rem; }}
  .answer {{ padding: 1.2rem 1.2rem 1.05rem; }}
  .answer p, .answer li {{ font-size: 1.06rem; }}
  .stamp {{ position: static; display: inline-block; margin-top: .6rem; transform: rotate(-4deg) scale(1); animation: none; }}
}}
</style>
"""
