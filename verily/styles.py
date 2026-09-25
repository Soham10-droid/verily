"""Visual identity for Verily.

A clean, modern research-product look: cool off-white surfaces, deep navy
text, a single blue accent reserved mostly for interaction and links, and
green/amber/red used only to mean something (verified / stretched /
unsupported) — never as decoration. One quiet reveal on load; everything
else stays still until you interact with it.
"""

LIGHT = {
    "bg": "#F8FAFC", "surface": "#FFFFFF", "sunken": "#F1F5F9",
    "ink": "#0F172A", "muted": "#64748B", "line": "#E2E8F0",
    "accent": "#2563EB", "accent-soft": "#EFF6FF", "accent-ring": "#DBEAFE",
    "accent-hover": "#1D4ED8", "accent-border": "#93C5FD",
    "ok": "#16A34A", "ok-bg": "#DCFCE7",
    "warn": "#D97706", "warn-bg": "#FEF3C7",
    "bad": "#DC2626", "bad-bg": "#FEE2E2",
    "shadow": "15, 23, 42",
}

DARK = {
    "bg": "#0B1120", "surface": "#111827", "sunken": "#151F30",
    "ink": "#F8FAFC", "muted": "#94A3B8", "line": "#1E293B",
    "accent": "#3B82F6", "accent-soft": "#16223B", "accent-ring": "#1E3A6E",
    "accent-hover": "#60A5FA", "accent-border": "#3B5C8C",
    "ok": "#22C55E", "ok-bg": "#123322",
    "warn": "#F59E0B", "warn-bg": "#3A2E10",
    "bad": "#EF4444", "bad-bg": "#3B1616",
    "shadow": "0, 0, 0",
}


def css(dark=False):
    p = DARK if dark else LIGHT
    variables = "\n".join(f"  --{k}: {v};" for k, v in p.items())
    return f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=Inter:wght@400;500;600;700&display=swap');

:root {{
{variables}
  --display: 'DM Serif Display', Georgia, serif;
  --sans: 'Inter', system-ui, -apple-system, sans-serif;
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
::selection {{ background: var(--accent-ring); color: var(--ink); }}

@media (prefers-reduced-motion: reduce) {{
  * {{ animation-duration: .001ms !important; animation-iteration-count: 1 !important; transition-duration: .001ms !important; }}
}}

/* ================= masthead ================= */
.mast-wrap {{ opacity: 0; animation: riseIn .6s cubic-bezier(.16,1,.3,1) forwards; }}
.mast {{ display: flex; align-items: center; gap: .5rem; margin: 0; }}
.mast h1 {{
  font-family: var(--display); font-style: italic; font-weight: 400;
  font-size: 2.75rem; letter-spacing: -0.01em; line-height: 1; margin: 0; color: var(--ink);
}}
.mast .dot {{
  width: .4rem; height: .4rem; border-radius: 50%; background: var(--accent);
  transform: translateY(-1rem); flex-shrink: 0;
  animation: dotIn .45s cubic-bezier(.34,1.56,.64,1) .5s backwards;
}}
.rule {{ height: 2px; background: var(--accent); width: 2.75rem; margin: .65rem 0 1.15rem;
  border-radius: 2px; transform-origin: left; animation: growLine .55s cubic-bezier(.16,1,.3,1) .2s backwards; }}
.lede {{
  opacity: 0; animation: riseIn .6s cubic-bezier(.16,1,.3,1) .1s forwards;
  color: var(--muted); font-size: 1.05rem; line-height: 1.55;
  max-width: 36em; margin: 0 0 1.9rem;
}}

@keyframes riseIn {{ from {{ opacity: 0; transform: translateY(8px); }} to {{ opacity: 1; transform: translateY(0); }} }}
@keyframes dotIn {{ from {{ opacity: 0; transform: translateY(-1rem) scale(.3); }} to {{ opacity: 1; transform: translateY(0) scale(1); }} }}
@keyframes growLine {{ from {{ transform: scaleX(0); }} to {{ transform: scaleX(1); }} }}

/* ================= input row ================= */
[data-testid="stTextInput"] input {{
  background: var(--surface) !important; color: var(--ink) !important;
  -webkit-text-fill-color: var(--ink); caret-color: var(--accent);
  font-family: var(--sans); font-size: 1.08rem; padding: .85rem 1rem;
}}
[data-testid="stTextInput"] input::placeholder {{ color: var(--muted); opacity: .75; }}
[data-baseweb="input"], [data-baseweb="base-input"] {{
  background: var(--surface) !important; border-color: #CBD5E1 !important;
  border-radius: 12px !important; transition: border-color .18s, box-shadow .18s;
}}
[data-baseweb="input"]:focus-within {{
  border-color: var(--accent) !important; box-shadow: 0 0 0 3px var(--accent-ring) !important;
}}

[data-testid="stFormSubmitButton"] button {{
  width: 100%; height: 3.05rem; border-radius: 10px; border: none;
  background: var(--ink); color: var(--bg); font-family: var(--sans);
  font-weight: 600; font-size: 1rem; transition: background .18s, opacity .18s;
}}
[data-testid="stFormSubmitButton"] button p {{ color: var(--bg) !important; }}
[data-testid="stFormSubmitButton"] button:hover {{ background: var(--accent-hover); }}
[data-testid="stFormSubmitButton"] button:focus-visible {{ outline: 3px solid var(--accent); outline-offset: 2px; }}

.stButton button {{
  background: var(--surface); border: 1px solid var(--line); border-radius: 10px;
  color: #475569; font-family: var(--sans); font-size: .92rem;
  padding: .34rem .8rem; min-height: 0; transition: border-color .16s, color .16s, background .16s;
}}
.stButton button p {{ color: #475569 !important; }}
.stButton button:hover {{ background: var(--accent-soft); border-color: var(--accent-border); }}
.stButton button:hover p {{ color: var(--accent-hover) !important; }}

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
  margin: 2.4rem 0 1rem; font-family: var(--display); font-style: italic; font-weight: 400;
  font-size: 1.55rem; letter-spacing: -0.005em; line-height: 1.3; color: var(--ink);
}}
.answer-wrap {{
  position: relative; opacity: 0; animation: riseIn .5s cubic-bezier(.16,1,.3,1) .06s forwards;
}}
.answer {{
  background: var(--surface); border: 1px solid var(--line); border-left: 3px solid var(--accent);
  border-radius: 14px; padding: 1.5rem 1.7rem 1.3rem;
  box-shadow: 0 1px 2px rgba(var(--shadow), .04), 0 10px 22px -16px rgba(var(--shadow), .18);
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

.tally {{ margin: .85rem .1rem 0; color: var(--muted); font-family: var(--sans); font-size: .95rem; }}
.tally b {{ color: var(--ink); font-weight: 600; }}

/* ================= claim markup ================= */
.section-title {{
  font-family: var(--sans); font-weight: 600; font-size: 1.1rem; margin: 2.8rem 0 .3rem; color: var(--ink);
}}
.section-sub {{ color: var(--muted); font-size: .92rem; margin: 0 0 .3rem; }}
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
details.draft {{ margin-top: 1.5rem; border: 1px solid var(--line); border-radius: 10px; background: var(--sunken); }}
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
.sources a {{ color: var(--ink) !important; font-weight: 600; text-decoration: none; line-height: 1.35; transition: color .15s; }}
.sources a:hover {{ color: var(--accent) !important; text-decoration: underline; }}
.sources .dom {{ grid-column: 2; color: var(--muted); font-size: .85rem; }}

/* ================= messages ================= */
.notice {{
  margin-top: 1.7rem; padding: 1.05rem 1.25rem; border-radius: 10px; background: var(--bad-bg);
  color: var(--ink); line-height: 1.55; border-left: 3px solid var(--bad);
}}
.notice b {{ color: var(--bad); }}
.notice code {{ background: var(--surface); color: var(--ink); padding: .06rem .38rem; border-radius: 4px; font-size: .92em; }}
.how {{
  opacity: 0; animation: riseIn .6s ease .18s forwards;
  margin-top: 2.8rem; padding-top: 1.6rem; border-top: 1px solid var(--line);
  color: var(--muted); font-family: var(--sans); font-size: .98rem; line-height: 1.65; max-width: 38em;
}}
.how b {{ color: var(--ink); font-weight: 600; }}

/* dark-mode toggle */
[data-testid="stToggle"] label p, .stCheckbox label p {{ color: var(--muted) !important; font-size: .88rem; }}

@media (max-width: 640px) {{
  .mast h1 {{ font-size: 2.2rem; }}
  .answer {{ padding: 1.2rem 1.2rem 1.05rem; }}
  .answer p, .answer li {{ font-size: 1rem; }}
  .stamp {{ position: static; display: inline-block; margin-top: .6rem; transform: scale(1); animation: none; }}
}}
</style>
"""
