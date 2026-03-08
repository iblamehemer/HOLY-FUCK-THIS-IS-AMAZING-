"""
NovaTech AI — AI-Powered Automated Branding Assistant
CRS AI Capstone 2025-26 | Scenario 1
Single-page smooth-scroll layout inspired by waabi.ai
"""
import streamlit as st
import base64, os

st.set_page_config(
    page_title="NovaTech AI — Branding Platform",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Load logo as base64 for embedding ─────────────────────────────────────────
def _load_logo():
    p = os.path.join(os.path.dirname(__file__), "assets", "novatech-logo.svg")
    if os.path.exists(p):
        with open(p) as f: raw = f.read()
        # Make logo white for dark background
        raw = (raw.replace('fill="#1A1A1A"', 'fill="#F5F2EB"')
                  .replace("fill='#1A1A1A'", "fill='#F5F2EB'")
                  .replace('fill="#F9F9F7"/>', 'fill="#0A0A08"/>')
                  .replace('rect width="400" height="400" fill="#F9F9F7"',
                            'rect width="400" height="400" fill="none"'))
        return raw
    return ""

LOGO_SVG = _load_logo()

from utils.session import init_session
from utils.gemini  import call_gemini_json, call_gemini

init_session()

# ═══════════════════════════════════════════════════════════════════════════════
# GLOBAL CSS — Waabi-inspired: pitch black, large serif, whisper nav, smooth scroll
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,300;0,400;0,500;1,300;1,400&family=DM+Sans:wght@300;400;500&family=DM+Mono:wght@300;400&display=swap');

:root {
  --black:   #0A0A08;
  --black2:  #111110;
  --black3:  #1A1A17;
  --edge:    #222220;
  --edge2:   #2C2C29;
  --white:   #F5F2EB;
  --white2:  #C8C4BB;
  --dim:     #6A6A64;
  --dim2:    #3A3A36;
  --gold:    #C8A94A;
  --gold2:   #E2C97A;
  --serif:   'Playfair Display', Georgia, serif;
  --sans:    'DM Sans', system-ui, sans-serif;
  --mono:    'DM Mono', 'Courier New', monospace;
}

html { scroll-behavior: smooth; }

/* ── Nuke all Streamlit chrome ─────────────────────────────────── */
#MainMenu, footer, header,
[data-testid="stHeader"],
[data-testid="stDecoration"],
[data-testid="stToolbar"],
[data-testid="stSidebar"] { display: none !important; }

/* ── Full page black ────────────────────────────────────────────── */
html, body,
[data-testid="stAppViewContainer"],
[data-testid="stMain"],
section.main,
.main .block-container {
  background-color: var(--black) !important;
  color: var(--white) !important;
  font-family: var(--sans) !important;
  padding: 0 !important;
  margin: 0 !important;
  max-width: 100% !important;
}
[data-testid="block-container"] {
  padding: 0 !important;
  max-width: 100% !important;
}
[data-testid="stVerticalBlock"] > div { gap: 0 !important; }

/* ── Streamlit Tabs → thin sticky nav ──────────────────────────── */
[data-testid="stTabs"] {
  position: sticky !important;
  top: 0 !important;
  z-index: 999 !important;
  background: rgba(10,10,8,0.96) !important;
  backdrop-filter: blur(20px) !important;
  -webkit-backdrop-filter: blur(20px) !important;
  border-bottom: 1px solid var(--edge) !important;
  padding: 0 40px !important;
  margin: 0 !important;
}
[data-testid="stTabs"] button {
  background: transparent !important;
  color: var(--dim) !important;
  font-family: var(--mono) !important;
  font-size: 0.6rem !important;
  font-weight: 400 !important;
  letter-spacing: 0.14em !important;
  text-transform: uppercase !important;
  border: none !important;
  border-bottom: 1px solid transparent !important;
  padding: 1rem 1.1rem !important;
  border-radius: 0 !important;
  transition: color 0.2s !important;
  white-space: nowrap !important;
}
[data-testid="stTabs"] button:hover {
  color: var(--white) !important;
  background: transparent !important;
}
[data-testid="stTabs"] button[aria-selected="true"] {
  color: var(--white) !important;
  border-bottom: 1px solid var(--white) !important;
  background: transparent !important;
}
[data-testid="stTabsContent"] {
  border: none !important;
  padding: 0 !important;
  background: var(--black) !important;
}
/* Hide the blue underline Streamlit adds */
[data-testid="stTabs"] [data-baseweb="tab-highlight"] {
  background: transparent !important;
}

/* ── Buttons ────────────────────────────────────────────────────── */
[data-testid="stButton"] > button {
  background: transparent !important;
  color: var(--dim) !important;
  border: 1px solid var(--edge2) !important;
  border-radius: 2px !important;
  font-family: var(--mono) !important;
  font-size: 0.65rem !important;
  letter-spacing: 0.1em !important;
  text-transform: uppercase !important;
  padding: 0.55rem 1.1rem !important;
  transition: all 0.15s !important;
}
[data-testid="stButton"] > button:hover {
  border-color: var(--white2) !important;
  color: var(--white) !important;
  background: rgba(245,242,235,0.04) !important;
}
[data-testid="stButton"] > button[kind="primary"] {
  background: var(--white) !important;
  color: var(--black) !important;
  border-color: var(--white) !important;
  font-weight: 500 !important;
}
[data-testid="stButton"] > button[kind="primary"]:hover {
  background: var(--white2) !important;
}

/* ── Download ───────────────────────────────────────────────────── */
[data-testid="stDownloadButton"] > button {
  background: transparent !important;
  color: var(--gold) !important;
  border: 1px solid rgba(200,169,74,0.3) !important;
  border-radius: 2px !important;
  font-family: var(--mono) !important;
  font-size: 0.65rem !important;
  letter-spacing: 0.1em !important;
  text-transform: uppercase !important;
  transition: all 0.15s !important;
}
[data-testid="stDownloadButton"] > button:hover {
  background: rgba(200,169,74,0.07) !important;
  border-color: var(--gold) !important;
}

/* ── Inputs ─────────────────────────────────────────────────────── */
[data-testid="stTextInput"] input,
[data-testid="stTextArea"] textarea {
  background: var(--black2) !important;
  border: 1px solid var(--edge2) !important;
  border-radius: 2px !important;
  color: var(--white) !important;
  font-family: var(--sans) !important;
  font-size: 0.88rem !important;
  font-weight: 300 !important;
}
[data-testid="stTextInput"] input:focus,
[data-testid="stTextArea"] textarea:focus {
  border-color: var(--white2) !important;
  box-shadow: none !important;
}
[data-testid="stTextInput"] label,
[data-testid="stTextArea"] label,
[data-testid="stSelectbox"] label,
[data-testid="stSlider"] label,
[data-testid="stMultiSelect"] label {
  color: var(--dim) !important;
  font-family: var(--mono) !important;
  font-size: 0.58rem !important;
  letter-spacing: 0.14em !important;
  text-transform: uppercase !important;
}
[data-testid="stSelectbox"] > div > div {
  background: var(--black2) !important;
  border: 1px solid var(--edge2) !important;
  border-radius: 2px !important;
  color: var(--white) !important;
}
[data-testid="stMultiSelect"] > div > div {
  background: var(--black2) !important;
  border: 1px solid var(--edge2) !important;
}
[data-testid="stMultiSelect"] span[data-baseweb="tag"] {
  background: var(--black3) !important;
  color: var(--gold) !important;
  border: 1px solid var(--edge2) !important;
  font-family: var(--mono) !important;
  font-size: 0.65rem !important;
  border-radius: 2px !important;
}

/* ── Slider ─────────────────────────────────────────────────────── */
[data-testid="stSlider"] > div > div > div { background: var(--edge2) !important; }
[data-testid="stSlider"] > div > div > div > div { background: var(--white) !important; }

/* ── Metrics ────────────────────────────────────────────────────── */
[data-testid="stMetric"] {
  background: var(--black2) !important;
  border: 1px solid var(--edge) !important;
  border-radius: 4px !important;
  padding: 1.4rem 1.6rem !important;
}
[data-testid="stMetricLabel"] {
  color: var(--dim) !important;
  font-family: var(--mono) !important;
  font-size: 0.58rem !important;
  letter-spacing: 0.14em !important;
  text-transform: uppercase !important;
}
[data-testid="stMetricValue"] {
  color: var(--white) !important;
  font-family: var(--serif) !important;
  font-size: 2.2rem !important;
  font-weight: 300 !important;
}
[data-testid="stMetricDelta"] { color: var(--dim) !important; font-size: 0.7rem !important; }

/* ── Dataframe ──────────────────────────────────────────────────── */
[data-testid="stDataFrame"] {
  border: 1px solid var(--edge) !important;
  border-radius: 4px !important;
  overflow: hidden !important;
}

/* ── Alerts ─────────────────────────────────────────────────────── */
[data-testid="stAlert"] {
  background: var(--black2) !important;
  border-left: 2px solid var(--edge2) !important;
  color: var(--dim) !important;
  font-size: 0.82rem !important;
  border-radius: 0 2px 2px 0 !important;
}
[data-testid="stSuccess"] { border-left-color: #4a7c5a !important; }
[data-testid="stWarning"]  { border-left-color: var(--gold) !important; }

/* ── Code ───────────────────────────────────────────────────────── */
pre, [data-testid="stCode"] {
  background: #070706 !important;
  border: 1px solid var(--edge) !important;
  border-radius: 4px !important;
  font-family: var(--mono) !important;
  font-size: 0.76rem !important;
}
code { color: var(--gold2) !important; }

/* ── Expander ───────────────────────────────────────────────────── */
[data-testid="stExpander"] {
  background: transparent !important;
  border: 1px solid var(--edge) !important;
  border-radius: 2px !important;
}
[data-testid="stExpander"] summary {
  font-family: var(--mono) !important;
  font-size: 0.62rem !important;
  letter-spacing: 0.1em !important;
  text-transform: uppercase !important;
  color: var(--dim) !important;
}

/* ── Divider ────────────────────────────────────────────────────── */
hr { border: none !important; border-top: 1px solid var(--edge) !important; margin: 0 !important; }

/* ── Typography ─────────────────────────────────────────────────── */
h1, h2, h3 {
  font-family: var(--serif) !important;
  font-weight: 300 !important;
  color: var(--white) !important;
}
p { color: var(--white2) !important; font-weight: 300 !important; line-height: 1.75 !important; }

/* ── Form ───────────────────────────────────────────────────────── */
[data-testid="stForm"] {
  background: var(--black2) !important;
  border: 1px solid var(--edge) !important;
  border-radius: 4px !important;
  padding: 2rem !important;
}
[data-testid="stFormSubmitButton"] > button {
  background: var(--white) !important; color: var(--black) !important;
  border: none !important; font-family: var(--mono) !important;
  font-size: 0.65rem !important; letter-spacing: 0.1em !important;
  text-transform: uppercase !important; padding: 0.7rem 2rem !important;
  border-radius: 2px !important; width: 100% !important;
}
[data-testid="stFormSubmitButton"] > button:hover { background: var(--white2) !important; }

/* ── Chat ───────────────────────────────────────────────────────── */
[data-testid="stChatMessage"] {
  background: var(--black2) !important;
  border: 1px solid var(--edge) !important;
  border-radius: 4px !important;
}
[data-testid="stChatInput"] textarea {
  background: var(--black2) !important;
  border: 1px solid var(--edge2) !important;
  color: var(--white) !important;
  border-radius: 2px !important;
}
[data-testid="stImage"] img { border-radius: 2px !important; }
</style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# NAV — sticky, transparent, Waabi-style
# ═══════════════════════════════════════════════════════════════════════════════
company_name = st.session_state.get("company","NovaTech") or "NovaTech"
st.markdown(f"""
<div style="
  position:sticky; top:0; z-index:999;
  background:rgba(10,10,8,0.97);
  backdrop-filter:blur(20px); -webkit-backdrop-filter:blur(20px);
  border-bottom:1px solid #1A1A17;
  padding:0 48px; height:64px;
  display:flex; align-items:center; justify-content:space-between;
  font-family:'DM Mono',monospace;
">
  <!-- Wordmark + logo -->
  <div style="display:flex;align-items:center;gap:12px">
    <div style="width:32px;height:32px;overflow:hidden;display:flex;align-items:center;justify-content:center">
      {LOGO_SVG.replace('width="400"','width="32"').replace('height="400"','height="32"') if LOGO_SVG else ''}
    </div>
    <span style="font-size:0.68rem;letter-spacing:0.22em;color:#F5F2EB;text-transform:uppercase">
      {company_name}
    </span>
  </div>
  <!-- Nav links -->
  <div style="display:flex;align-items:center;gap:2.2rem">
    <a href="#configure"  style="font-size:0.58rem;letter-spacing:0.12em;color:#6A6A64;text-decoration:none;text-transform:uppercase;transition:color 0.2s">Configure</a>
    <a href="#logo"       style="font-size:0.58rem;letter-spacing:0.12em;color:#6A6A64;text-decoration:none;text-transform:uppercase">Logo &amp; Font</a>
    <a href="#slogans"    style="font-size:0.58rem;letter-spacing:0.12em;color:#6A6A64;text-decoration:none;text-transform:uppercase">Slogans</a>
    <a href="#colour"     style="font-size:0.58rem;letter-spacing:0.12em;color:#6A6A64;text-decoration:none;text-transform:uppercase">Colour</a>
    <a href="#animation"  style="font-size:0.58rem;letter-spacing:0.12em;color:#6A6A64;text-decoration:none;text-transform:uppercase">Animation</a>
    <a href="#campaign"   style="font-size:0.58rem;letter-spacing:0.12em;color:#6A6A64;text-decoration:none;text-transform:uppercase">Campaign</a>
    <a href="#kit"        style="font-size:0.58rem;letter-spacing:0.12em;color:#F5F2EB;text-decoration:none;text-transform:uppercase;border:1px solid #2C2C29;padding:0.45rem 1rem;border-radius:2px">Brand Kit ↓</a>
  </div>
</div>
""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
# HERO — full-bleed cinematic opener
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown(f"""
<section style="
  min-height:95vh; background:#0A0A08;
  display:flex; flex-direction:column; justify-content:flex-end;
  padding:0 48px 80px; position:relative; overflow:hidden;
">
  <!-- Grain overlay -->
  <div style="
    position:absolute; inset:0; pointer-events:none; opacity:0.018;
    background-image:url('data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 width=%22200%22 height=%22200%22><filter id=%22n%22><feTurbulence type=%22fractalNoise%22 baseFrequency=%220.9%22 numOctaves=%224%22/></filter><rect width=%22200%22 height=%22200%22 filter=%22url(%23n)%22/></svg>');
  "></div>
  <!-- Large logo centred -->
  <div style="
    position:absolute; top:50%; left:50%;
    transform:translate(-50%,-60%);
    opacity:0.04; pointer-events:none;
    width:600px; height:600px;
    display:flex; align-items:center; justify-content:center;
  ">
    {LOGO_SVG.replace('width="400"','width="600"').replace('height="400"','height="600"')}
  </div>
  <!-- Eyebrow -->
  <div style="
    font-family:'DM Mono',monospace; font-size:0.6rem;
    letter-spacing:0.18em; color:#6A6A64; text-transform:uppercase;
    margin-bottom:24px;
  ">✦ &nbsp; CRS AI Capstone 2025–26 · Scenario 1</div>
  <!-- Headline -->
  <h1 style="
    font-family:'Playfair Display',Georgia,serif;
    font-size:clamp(3.5rem,7vw,7rem); font-weight:300;
    color:#F5F2EB; line-height:1.0; letter-spacing:-0.03em;
    margin:0 0 32px; max-width:900px;
  ">Build your brand<br>with <em style='color:#C8A94A'>intelligence</em>.</h1>
  <!-- Sub -->
  <p style="
    font-family:'DM Sans',sans-serif; font-size:1.05rem; font-weight:300;
    color:#6A6A64; max-width:480px; line-height:1.7; margin:0 0 48px;
  ">
    CNN · KNN · KMeans · Random Forest · Gemini AI.<br>
    From logo to launch in one platform.
  </p>
  <!-- CTA row -->
  <div style="display:flex;gap:16px;align-items:center">
    <a href="#configure" style="
      font-family:'DM Mono',monospace; font-size:0.62rem; letter-spacing:0.1em;
      text-transform:uppercase; color:#0A0A08; background:#F5F2EB;
      padding:0.75rem 2rem; border-radius:2px; text-decoration:none;
      transition:background 0.15s;
    ">Get started</a>
    <a href="#logo" style="
      font-family:'DM Mono',monospace; font-size:0.62rem; letter-spacing:0.1em;
      text-transform:uppercase; color:#6A6A64;
      padding:0.75rem 0; text-decoration:none; border-bottom:1px solid #3A3A36;
    ">See the platform ↓</a>
  </div>
  <!-- Scroll hint -->
  <div style="
    position:absolute; bottom:32px; right:48px;
    font-family:'DM Mono',monospace; font-size:0.55rem;
    letter-spacing:0.16em; color:#2C2C29; text-transform:uppercase;
    writing-mode:vertical-rl;
  ">Scroll to explore</div>
</section>
""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
# PLATFORM STRIP — 5 pillars
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<section style="background:#111110;border-top:1px solid #1A1A17;border-bottom:1px solid #1A1A17;padding:0 48px">
  <div style="display:grid;grid-template-columns:repeat(5,1fr)">
    <div style="padding:36px 24px;border-right:1px solid #1A1A17">
      <div style="font-family:'DM Mono',monospace;font-size:0.55rem;letter-spacing:0.14em;color:#3A3A36;text-transform:uppercase;margin-bottom:10px">Week 02–03</div>
      <div style="font-family:'Playfair Display',serif;font-size:1.05rem;font-weight:300;color:#F5F2EB;margin-bottom:6px">Logo &amp; Typography</div>
      <div style="font-size:0.78rem;color:#3A3A36;font-weight:300;line-height:1.5">CNN classification · KNN font engine</div>
    </div>
    <div style="padding:36px 24px;border-right:1px solid #1A1A17">
      <div style="font-family:'DM Mono',monospace;font-size:0.55rem;letter-spacing:0.14em;color:#3A3A36;text-transform:uppercase;margin-bottom:10px">Week 04</div>
      <div style="font-family:'Playfair Display',serif;font-size:1.05rem;font-weight:300;color:#F5F2EB;margin-bottom:6px">Slogans &amp; Copy</div>
      <div style="font-size:0.78rem;color:#3A3A36;font-weight:300;line-height:1.5">Gemini API · NLTK preprocessing</div>
    </div>
    <div style="padding:36px 24px;border-right:1px solid #1A1A17">
      <div style="font-family:'DM Mono',monospace;font-size:0.55rem;letter-spacing:0.14em;color:#3A3A36;text-transform:uppercase;margin-bottom:10px">Week 05–06</div>
      <div style="font-family:'Playfair Display',serif;font-size:1.05rem;font-weight:300;color:#F5F2EB;margin-bottom:6px">Colour &amp; Animation</div>
      <div style="font-size:0.78rem;color:#3A3A36;font-weight:300;line-height:1.5">KMeans extraction · GIF storyboard</div>
    </div>
    <div style="padding:36px 24px;border-right:1px solid #1A1A17">
      <div style="font-family:'DM Mono',monospace;font-size:0.55rem;letter-spacing:0.14em;color:#3A3A36;text-transform:uppercase;margin-bottom:10px">Week 07–08</div>
      <div style="font-family:'Playfair Display',serif;font-size:1.05rem;font-weight:300;color:#F5F2EB;margin-bottom:6px">Campaign &amp; Global</div>
      <div style="font-size:0.78rem;color:#3A3A36;font-weight:300;line-height:1.5">Random Forest · 10+ languages</div>
    </div>
    <div style="padding:36px 24px">
      <div style="font-family:'DM Mono',monospace;font-size:0.55rem;letter-spacing:0.14em;color:#3A3A36;text-transform:uppercase;margin-bottom:10px">Week 10</div>
      <div style="font-family:'Playfair Display',serif;font-size:1.05rem;font-weight:300;color:#F5F2EB;margin-bottom:6px">Brand Kit</div>
      <div style="font-size:0.78rem;color:#3A3A36;font-weight:300;line-height:1.5">ZIP export · Streamlit Cloud deploy</div>
    </div>
  </div>
</section>
""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
# SECTION HELPER
# ═══════════════════════════════════════════════════════════════════════════════
def section_open(anchor, eyebrow, headline, sub="", bg="#0A0A08", light_sep=True):
    border = "border-top:1px solid #1A1A17;" if light_sep else ""
    st.markdown(f"""
<section id="{anchor}" style="background:{bg};{border}padding:96px 48px 64px">
  <div style="max-width:1100px;margin:0 auto">
    <div style="font-family:'DM Mono',monospace;font-size:0.58rem;letter-spacing:0.16em;
      color:#3A3A36;text-transform:uppercase;margin-bottom:20px">{eyebrow}</div>
    <h2 style="font-family:'Playfair Display',Georgia,serif;font-size:clamp(2rem,4vw,3.4rem);
      font-weight:300;color:#F5F2EB;letter-spacing:-0.02em;line-height:1.1;margin:0 0 20px">
      {headline}</h2>
    {'<p style="font-size:0.95rem;color:#6A6A64;font-weight:300;max-width:560px;line-height:1.75;margin:0 0 48px">'+sub+'</p>' if sub else '<div style="height:48px"></div>'}
  </div>
  <div style="max-width:1100px;margin:0 auto">
""", unsafe_allow_html=True)

def section_close():
    st.markdown("</div></section>", unsafe_allow_html=True)

def field_label(text):
    st.markdown(f"""<div style="font-family:'DM Mono',monospace;font-size:0.58rem;
      letter-spacing:0.14em;text-transform:uppercase;color:#6A6A64;
      margin-bottom:4px;margin-top:20px">{text}</div>""", unsafe_allow_html=True)

def week_tag(n, title, tools=""):
    st.markdown(f"""
<div style="padding:0 0 28px;margin-bottom:32px;border-bottom:1px solid #1A1A17">
  <div style="font-family:'DM Mono',monospace;font-size:0.58rem;color:#3A3A36;
    letter-spacing:0.14em;text-transform:uppercase;margin-bottom:10px">
    Week {n:02d}{(' · '+tools) if tools else ''}
  </div>
  <div style="font-family:'Playfair Display',serif;font-size:1.8rem;font-weight:300;
    color:#F5F2EB;letter-spacing:-0.01em">{title}</div>
</div>""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
# CONFIGURE BRAND — Section 1
# ═══════════════════════════════════════════════════════════════════════════════
section_open("configure", "Step 01 · Foundation",
    "Configure your brand.",
    "Everything NovaTech AI generates is tailored to your company, industry, and tone of voice.")

INDUSTRIES = ["Technology","Finance","Healthcare","Retail","Education",
              "Food & Beverage","Real Estate","Fashion","Travel","Sustainability"]
TONES      = ["Minimalist","Bold","Luxury","Playful","Professional",
              "Innovative","Trustworthy","Creative"]

col1, col2 = st.columns([1,1], gap="large")
with col1:
    field_label("Company Name")
    company = st.text_input("company", value=st.session_state.get("company","NovaTech"),
                             placeholder="e.g. NovaTech", label_visibility="collapsed")
    st.session_state.company = company

    field_label("Target Audience")
    audience = st.text_input("audience", value=st.session_state.get("audience",""),
                              placeholder="e.g. B2B SaaS founders, 28–45",
                              label_visibility="collapsed")
    st.session_state.audience = audience

    field_label("Target Region")
    region = st.text_input("region", value=st.session_state.get("region",""),
                            placeholder="e.g. India, Europe, Global",
                            label_visibility="collapsed")
    st.session_state.region = region

with col2:
    field_label("Product / Service Description")
    desc = st.text_area("description", value=st.session_state.get("description",""),
                         placeholder="Describe what your brand does in 2–3 sentences…",
                         height=156, label_visibility="collapsed")
    st.session_state.description = desc

st.markdown("<div style='height:32px'></div>", unsafe_allow_html=True)
field_label("Industry")
ind_cols = st.columns(5, gap="small")
for i, ind in enumerate(INDUSTRIES):
    with ind_cols[i % 5]:
        active = st.session_state.get("industry") == ind
        if st.button(ind, key=f"ind_{ind}", use_container_width=True,
                     type="primary" if active else "secondary"):
            st.session_state.industry = ind
            st.rerun()

st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)
field_label("Brand Tone")
tone_cols = st.columns(4, gap="small")
for i, tone in enumerate(TONES):
    with tone_cols[i % 4]:
        active = st.session_state.get("tone") == tone
        if st.button(tone, key=f"tone_{tone}", use_container_width=True,
                     type="primary" if active else "secondary"):
            st.session_state.tone = tone
            st.rerun()

# Ready state
if st.session_state.get("company") and st.session_state.get("industry") and st.session_state.get("tone"):
    st.markdown(f"""
<div style="margin-top:36px;display:flex;align-items:center;gap:14px;
  padding:20px 24px;background:#111110;border:1px solid #1A1A17;border-radius:2px">
  <div style="width:6px;height:6px;background:#F5F2EB;border-radius:50%;flex-shrink:0"></div>
  <div>
    <div style="font-family:'Playfair Display',serif;font-size:1rem;font-weight:300;color:#F5F2EB">
      {st.session_state.company} is configured and ready.
    </div>
    <div style="font-family:'DM Mono',monospace;font-size:0.58rem;color:#3A3A36;
      letter-spacing:0.1em;margin-top:4px">
      {st.session_state.industry} · {st.session_state.tone} · {st.session_state.get('region','Global')}
    </div>
  </div>
  <div style="margin-left:auto;font-family:'DM Mono',monospace;font-size:0.58rem;
    color:#6A6A64;letter-spacing:0.1em">Scroll to begin ↓</div>
</div>""", unsafe_allow_html=True)

section_close()


# ═══════════════════════════════════════════════════════════════════════════════
# LOGO & FONT — Section 2
# ═══════════════════════════════════════════════════════════════════════════════
section_open("logo", "Step 02–03 · Identity",
    "Logo studio &amp; typography.",
    "CNN-powered logo classification with PCA clusters. KNN font pairing trained on 2,400 samples.",
    bg="#0D0D0B")
from modules.week2_logo import render_logo
from modules.week3_font import render_font
render_logo()
st.markdown("<div style='height:48px'></div>", unsafe_allow_html=True)
render_font()
section_close()


# ═══════════════════════════════════════════════════════════════════════════════
# SLOGANS — Section 3
# ═══════════════════════════════════════════════════════════════════════════════
section_open("slogans", "Step 04 · Voice",
    "Slogans &amp; taglines.",
    "Gemini API generation with NLTK preprocessing. Download TXT + JSON.")
from modules.week4_slogan import render_slogan
render_slogan()
section_close()


# ═══════════════════════════════════════════════════════════════════════════════
# COLOUR — Section 4
# ═══════════════════════════════════════════════════════════════════════════════
section_open("colour", "Step 05 · Palette",
    "Colour palette engine.",
    "KMeans pixel extraction from logo datasets. Industry-mapped colour psychology.",
    bg="#0D0D0B")
from modules.week5_colour import render_colour
render_colour()
section_close()


# ═══════════════════════════════════════════════════════════════════════════════
# ANIMATION — Section 5
# ═══════════════════════════════════════════════════════════════════════════════
section_open("animation", "Step 06 · Motion",
    "Animation studio.",
    "Matplotlib FuncAnimation storyboards. Export GIF with one click.")
from modules.week6_animation import render_animation
render_animation()
section_close()


# ═══════════════════════════════════════════════════════════════════════════════
# CAMPAIGN — Section 6
# ═══════════════════════════════════════════════════════════════════════════════
section_open("campaign", "Step 07–08 · Reach",
    "Campaign analytics &amp; global copy.",
    "Random Forest + Gradient Boosting predict CTR, ROI, engagement. Gemini API translates to 10+ languages.",
    bg="#0D0D0B")
from modules.week7_campaign  import render_campaign
from modules.week8_multilang import render_multilang
render_campaign()
st.markdown("<div style='height:56px'></div>", unsafe_allow_html=True)
render_multilang()
section_close()


# ═══════════════════════════════════════════════════════════════════════════════
# FEEDBACK — Section 7 (inline, no full-bleed header needed)
# ═══════════════════════════════════════════════════════════════════════════════
section_open("feedback", "Step 09 · Refinement",
    "Feedback &amp; model tuning.",
    "VADER sentiment analysis on your ratings. Radar chart. Model refinement plan.")
from modules.week9_feedback import render_feedback
render_feedback()
section_close()


# ═══════════════════════════════════════════════════════════════════════════════
# BRAND KIT — Section 8
# ═══════════════════════════════════════════════════════════════════════════════
section_open("kit", "Step 10 · Export",
    "Your brand kit.",
    "Everything generated — logo variants, fonts, palette, slogans, campaign copy — in one ZIP.",
    bg="#0D0D0B")
from modules.week10_kit import render_kit
render_kit()
section_close()


# ═══════════════════════════════════════════════════════════════════════════════
# AI ASSISTANT — floating chat at bottom
# ═══════════════════════════════════════════════════════════════════════════════
section_open("chat", "Optional · AI Assistant",
    "Ask NovaTech AI anything.",
    "Gemini-powered assistant with full brand context.")
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [{"role":"assistant",
        "content":"Hi — I'm the NovaTech AI assistant. Ask me anything about your brand strategy, the AI models, or where to go next."}]
for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
if user_input := st.chat_input("Ask NovaTech AI…"):
    st.session_state.chat_history.append({"role":"user","content":user_input})
    with st.chat_message("user"):
        st.markdown(user_input)
    with st.chat_message("assistant"):
        with st.spinner(""):
            ctx = (f"Brand: {st.session_state.get('company','NovaTech')}, "
                   f"Industry: {st.session_state.get('industry','—')}, "
                   f"Tone: {st.session_state.get('tone','—')}.")
            reply = call_gemini(user_input, system=(
                f"You are NovaTech AI, an expert branding assistant. Context: {ctx} "
                "Be concise, helpful, and speak with authority about branding and AI."),
                temperature=0.7, max_tokens=400)
            st.markdown(reply)
            st.session_state.chat_history.append({"role":"assistant","content":reply})
section_close()


# ═══════════════════════════════════════════════════════════════════════════════
# FOOTER
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown(f"""
<footer style="
  background:#080807; border-top:1px solid #1A1A17;
  padding:48px; display:flex; align-items:center; justify-content:space-between;
">
  <div style="display:flex;align-items:center;gap:12px">
    <div style="width:24px;height:24px;overflow:hidden">
      {LOGO_SVG.replace('width="400"','width="24"').replace('height="400"','height="24"') if LOGO_SVG else ''}
    </div>
    <span style="font-family:'DM Mono',monospace;font-size:0.6rem;letter-spacing:0.18em;
      color:#3A3A36;text-transform:uppercase">NovaTech AI</span>
  </div>
  <div style="font-family:'DM Mono',monospace;font-size:0.55rem;letter-spacing:0.1em;
    color:#2C2C29;text-transform:uppercase">CRS AI Capstone 2025–26 · Scenario 1</div>
  <div style="font-family:'DM Mono',monospace;font-size:0.55rem;letter-spacing:0.1em;
    color:#2C2C29">Built with Streamlit · Gemini API · scikit-learn</div>
</footer>
""", unsafe_allow_html=True)
