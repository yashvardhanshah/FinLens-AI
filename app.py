import streamlit as st
import os
import sys
from dotenv import load_dotenv

load_dotenv()

BASE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE)

st.set_page_config(
    page_title="FinLens · Stock Research Made Simple",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── GLOBAL STYLES ────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;700;800&family=Inter:wght@400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif !important;
    background-color: #0a0d12 !important;
    color: #e8edf2 !important;
    font-size: 18px !important;
}
.stMarkdown p { font-size: 1.08rem !important; line-height: 1.8 !important; }
#MainMenu, footer, header { visibility: hidden; }
[data-testid="collapsedControl"] { display: none !important; }
[data-testid="stSidebarCollapseButton"] { display: none !important; }
[data-testid="stSidebarHeader"] { display: none !important; }
[data-testid="stAppViewContainer"] {
    background-color: #0a0d12 !important;
    gap: 0 !important;
}
[data-testid="stAppViewContainer"] > .main {
    margin-left: 0 !important;
}
.block-container { padding: 3rem 3.5rem !important; max-width: 100% !important; }

@media (prefers-reduced-motion: reduce) {
    *, *::before, *::after { animation-duration: 0.01ms !important; animation-iteration-count: 1 !important; transition-duration: 0.01ms !important; }
}

section[data-testid="stSidebar"] {
    background-color: #0d1117 !important;
    border-right: 1px solid #2a3240 !important;
    box-shadow: 2px 0 18px rgba(0,0,0,0.4) !important;
    width: 280px !important;
    min-width: 280px !important;
    margin-right: 0 !important;
}
section[data-testid="stSidebar"] > div:first-child {
    padding-right: 0.6rem !important;
}
section[data-testid="stSidebar"] * {
    font-family: 'Inter', sans-serif !important;
}
.stTextInput input {
    background-color: #131820 !important;
    border: 1px solid #232b38 !important;
    color: #e8edf2 !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 1.05rem !important;
    border-radius: 8px !important;
    padding: 0.75rem 1rem !important;
}
.stTextInput input:focus {
    border-color: #2dd4a7 !important;
    box-shadow: 0 0 0 3px rgba(45,212,167,0.15) !important;
}
.stTextInput label, .stFileUploader label {
    font-size: 1rem !important;
    color: #c2cbd6 !important;
    font-weight: 500 !important;
}
.stButton > button {
    background: #2dd4a7 !important;
    border: 1px solid #2dd4a7 !important;
    color: #07120f !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.95rem !important;
    font-weight: 700 !important;
    letter-spacing: 0.01em !important;
    border-radius: 8px !important;
    padding: 0.7rem 1.6rem !important;
    transition: transform 0.15s ease, box-shadow 0.15s ease !important;
}
.stButton > button:hover {
    background: #3ee6b8 !important;
    border-color: #3ee6b8 !important;
    color: #07120f !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 20px rgba(45,212,167,0.25) !important;
}
/* sidebar nav buttons should stay quiet, not green */
section[data-testid="stSidebar"] .stButton > button {
    background: transparent !important;
    border: none !important;
    color: #8b96a5 !important;
    font-weight: 500 !important;
    text-align: left !important;
    justify-content: flex-start !important;
    padding: 0.65rem 0.8rem !important;
    font-size: 0.98rem !important;
    box-shadow: none !important;
}
section[data-testid="stSidebar"] .stButton > button:hover {
    background: #161c26 !important;
    color: #2dd4a7 !important;
    transform: none !important;
    box-shadow: none !important;
}
.stFileUploader {
    background: #131820 !important;
    border: 1px solid #232b38 !important;
    border-radius: 8px !important;
}
.stFileUploader section {
    background: transparent !important;
}
.stSuccess { background: rgba(45,212,167,0.08) !important; border-left: 3px solid #2dd4a7 !important; border-radius: 6px !important; font-size: 1rem !important; }
.stWarning { border-left: 3px solid #f5b942 !important; border-radius: 6px !important; font-size: 1rem !important; }
.stError { border-left: 3px solid #f06868 !important; border-radius: 6px !important; font-size: 1rem !important; }
.stDownloadButton > button {
    font-size: 1rem !important;
    padding: 0.7rem 1.6rem !important;
    border-radius: 8px !important;
    font-weight: 700 !important;
}
.stAlert p { font-size: 1.05rem !important; }
[data-testid="stFileUploaderDropzone"] div, [data-testid="stFileUploaderDropzone"] span {
    font-size: 1rem !important;
}
.stSpinner > div { border-top-color: #2dd4a7 !important; }
.stSpinner p { font-size: 1.05rem !important; color: #c2cbd6 !important; }
h1, h2, h3 { font-family: 'Syne', sans-serif !important; color: #f3f6f9 !important; }

@keyframes fadeUp {
    from { opacity: 0; transform: translateY(18px); }
    to { opacity: 1; transform: translateY(0); }
}
@keyframes fadeIn {
    from { opacity: 0; }
    to { opacity: 1; }
}
@keyframes floatGlow {
    0%, 100% { opacity: 0.55; }
    50% { opacity: 0.9; }
}
@keyframes drift {
    0% { transform: translate(0,0); }
    50% { transform: translate(-10px,-14px); }
    100% { transform: translate(0,0); }
}

/* ── Custom component classes ── */
.fl-eyebrow {
    font-size: 0.95rem;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: #2dd4a7;
    font-weight: 600;
    display: flex;
    align-items: center;
    gap: 0.6rem;
    margin-bottom: 0.8rem;
    animation: fadeUp 0.6s ease both;
}
.fl-eyebrow::before {
    content: '';
    display: inline-block;
    width: 22px;
    height: 2px;
    background: #2dd4a7;
    border-radius: 2px;
}
.fl-hero-title {
    font-family: 'Syne', sans-serif;
    font-size: 3.2rem;
    font-weight: 800;
    line-height: 1.12;
    color: #f3f6f9;
    letter-spacing: -0.02em;
    margin-bottom: 1.2rem;
    animation: fadeUp 0.7s ease 0.05s both;
}
.fl-hero-title em { color: #2dd4a7; font-style: normal; position: relative; }
.fl-sub {
    font-size: 1.18rem;
    color: #aab4c2;
    line-height: 1.75;
    margin-bottom: 1.8rem;
    max-width: 560px;
    animation: fadeUp 0.7s ease 0.15s both;
}
.fl-section-title {
    font-family: 'Syne', sans-serif;
    font-size: 2rem;
    font-weight: 800;
    color: #f3f6f9;
    letter-spacing: -0.015em;
    margin-bottom: 0.6rem;
}
.fade-section {
    animation: fadeUp 0.7s ease both;
}
.ticker-bar {
    background: #0d1117;
    border: 1px solid #1f2530;
    border-radius: 10px;
    padding: 0.85rem 1.1rem;
    overflow: hidden;
    white-space: nowrap;
    margin-bottom: 2.8rem;
    animation: fadeIn 0.5s ease both;
}
.ticker-inner {
    display: inline-flex;
    gap: 2.8rem;
    animation: tick 32s linear infinite;
}
.ticker-item { font-size: 0.98rem; color: #8b96a5; font-weight: 500; }
.ticker-item .sym { color: #e8edf2; font-weight: 700; }
.ticker-item .up { color: #2dd4a7; }
.ticker-item .dn { color: #f06868; }
@keyframes tick { 0%{transform:translateX(0)} 100%{transform:translateX(-50%)} }

.stat-box {
    background: #11151c;
    border: 1px solid #1f2530;
    border-radius: 12px;
    padding: 1.7rem 1.3rem;
    text-align: center;
    transition: transform 0.25s ease, border-color 0.25s ease;
}
.stat-box:hover {
    transform: translateY(-3px);
    border-color: #2dd4a7;
}
.stat-val {
    font-family: 'Syne', sans-serif;
    font-size: 2.1rem;
    font-weight: 800;
    color: #f3f6f9;
    display: block;
}
.stat-val em { color: #2dd4a7; font-style: normal; }
.stat-lbl {
    font-size: 0.98rem;
    letter-spacing: 0.04em;
    color: #aab4c2;
    display: block;
    margin-top: 0.5rem;
    font-weight: 500;
}
.feat-card {
    background: #11151c;
    border: 1px solid #1f2530;
    border-radius: 14px;
    padding: 1.8rem;
    height: 100%;
    transition: transform 0.25s ease, border-color 0.25s ease, box-shadow 0.25s ease;
    animation: fadeUp 0.6s ease both;
}
.feat-card:hover {
    transform: translateY(-4px);
    border-color: #2dd4a7;
    box-shadow: 0 12px 30px rgba(0,0,0,0.35);
}
.feat-icon {
    font-size: 1.9rem;
    margin-bottom: 1rem;
    display: inline-block;
}
.feat-title {
    font-family: 'Syne', sans-serif;
    font-size: 1.22rem;
    font-weight: 700;
    color: #f3f6f9;
    margin-bottom: 0.6rem;
}
.feat-desc { font-size: 1.02rem; color: #9aa4b2; line-height: 1.75; }
.step-box {
    background: #11151c;
    border: 1px solid #1f2530;
    border-left: 3px solid #2dd4a7;
    border-radius: 12px;
    padding: 1.7rem;
    transition: transform 0.25s ease;
    animation: fadeUp 0.6s ease both;
}
.step-box:hover { transform: translateY(-3px); }
.step-num {
    font-family: 'Syne', sans-serif;
    font-size: 2.1rem;
    font-weight: 800;
    color: #232b38;
    line-height: 1;
    margin-bottom: 0.7rem;
}
.step-title {
    font-family: 'Syne', sans-serif;
    font-size: 1.12rem;
    font-weight: 700;
    color: #f3f6f9;
    margin-bottom: 0.5rem;
}
.step-desc { font-size: 0.98rem; color: #9aa4b2; line-height: 1.75; }
.terminal {
    background: #11151c;
    border: 1px solid #1f2530;
    border-radius: 14px;
    overflow: hidden;
    margin-bottom: 2rem;
    animation: fadeUp 0.7s ease 0.2s both;
    box-shadow: 0 20px 50px rgba(0,0,0,0.3);
}
.term-bar {
    background: #161c26;
    border-bottom: 1px solid #1f2530;
    padding: 0.7rem 1.1rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}
.term-dot {
    display: inline-block;
    width: 9px;
    height: 9px;
    border-radius: 50%;
}
.term-title { font-size: 0.92rem; color: #8b96a5; margin-left: auto; font-weight: 500; }
.term-body { padding: 1.5rem 1.6rem; font-size: 1.05rem; line-height: 2.15; }
.term-prompt { color: #2dd4a7; font-weight: 700; }
.term-cmd { color: #f3f6f9; font-weight: 600; }
.term-out { color: #6b7585; }
.term-out.hi { color: #2dd4a7; font-weight: 500; }
.term-out.warn { color: #f5b942; }
.term-cursor {
    display: inline-block; width: 8px; height: 14px;
    background: #2dd4a7;
    animation: blink 1s step-end infinite;
    vertical-align: middle;
    border-radius: 1px;
}
@keyframes blink { 50%{opacity:0} }

.divider { border: none; border-top: 1px solid #1f2530; margin: 3rem 0; }

.report-box {
    background: #11151c;
    border: 1px solid #1f2530;
    border-left: 4px solid #2dd4a7;
    padding: 1.8rem 2.1rem;
    font-size: 1.02rem;
    line-height: 1.9;
    white-space: pre-wrap;
    font-family: 'Inter', sans-serif;
    color: #dce3eb;
    border-radius: 12px;
    animation: fadeUp 0.5s ease both;
}
.cta-banner {
    background: linear-gradient(135deg, #11151c 0%, #131b1a 100%);
    border: 1px solid #1f2530;
    border-radius: 16px;
    padding: 3.4rem 2rem;
    text-align: center;
    margin: 2rem 0;
    position: relative;
    overflow: hidden;
}
.cta-banner::before {
    content: '';
    position: absolute;
    top: -60px; right: -60px;
    width: 220px; height: 220px;
    background: radial-gradient(circle, rgba(45,212,167,0.18), transparent 70%);
    animation: floatGlow 4s ease-in-out infinite;
}
.cta-title {
    font-family: 'Syne', sans-serif;
    font-size: 1.9rem;
    font-weight: 800;
    color: #f3f6f9;
    margin-bottom: 0.6rem;
    position: relative;
}
.cta-sub { font-size: 1.05rem; color: #9aa4b2; margin-bottom: 1.8rem; position: relative; }

/* Docs page */
.doc-h2 {
    font-family: 'Syne', sans-serif;
    font-size: 1.5rem;
    font-weight: 700;
    color: #f3f6f9;
    border-top: 1px solid #1f2530;
    padding-top: 1.6rem;
    margin-top: 2.2rem;
    margin-bottom: 0.9rem;
}
.doc-p { font-size: 1.05rem; color: #9aa4b2; line-height: 1.85; margin-bottom: 1rem; }
.doc-li {
    font-size: 1.02rem;
    color: #9aa4b2;
    line-height: 1.8;
    padding-left: 1.3rem;
    position: relative;
    margin-bottom: 0.4rem;
}
.doc-li::before { content: '✓'; color: #2dd4a7; position: absolute; left: 0; font-size: 1rem; top: 0.3rem; }
.info-box {
    background: #11151c;
    border: 1px solid #1f2530;
    border-left: 3px solid #2dd4a7;
    border-radius: 10px;
    padding: 1.1rem 1.4rem;
    font-size: 1.02rem;
    color: #9aa4b2;
    line-height: 1.85;
    margin: 1rem 0;
}
.info-box strong {
    color: #2dd4a7;
    font-size: 0.82rem;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    display: block;
    margin-bottom: 0.4rem;
}

/* About page */
.principle-card {
    background: #11151c;
    border: 1px solid #1f2530;
    border-radius: 12px;
    padding: 1.5rem;
    margin-bottom: 1.1rem;
    transition: transform 0.25s ease, border-color 0.25s ease;
    animation: fadeUp 0.6s ease both;
}
.principle-card:hover { transform: translateY(-2px); border-color: #2dd4a7; }
.principle-role {
    font-size: 0.95rem;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: #2dd4a7;
    margin-bottom: 0.5rem;
    font-weight: 600;
}
.principle-name {
    font-family: 'Syne', sans-serif;
    font-size: 1.18rem;
    font-weight: 700;
    color: #f3f6f9;
    margin-bottom: 0.6rem;
}
.principle-desc { font-size: 1rem; color: #9aa4b2; line-height: 1.8; }
.trust-pill {
    display: inline-block;
    border: 1px solid #1f2530;
    background: #11151c;
    border-radius: 20px;
    padding: 0.5rem 1.1rem;
    font-size: 1rem;
    font-weight: 500;
    color: #c2cbd6;
    margin: 0.3rem;
}
.blockquote {
    border-left: 4px solid #2dd4a7;
    padding: 1.5rem 1.8rem;
    background: #11151c;
    border-top: 1px solid #1f2530;
    border-right: 1px solid #1f2530;
    border-bottom: 1px solid #1f2530;
    border-radius: 12px;
    margin: 1.8rem 0;
    animation: fadeUp 0.6s ease both;
}
.blockquote q {
    font-family: 'Syne', sans-serif;
    font-size: 1.35rem;
    font-weight: 700;
    color: #f3f6f9;
    line-height: 1.5;
    display: block;
    margin-bottom: 0.8rem;
}
.blockquote cite { font-size: 0.98rem; letter-spacing: 0.04em; color: #8b96a5; font-weight: 500; }

/* FAQ */
.faq-row {
    border-bottom: 1px solid #1f2530;
    padding: 1.5rem 0;
    transition: background 0.2s ease;
}
.faq-q { font-family: 'Syne', sans-serif; font-size: 1.12rem; font-weight: 700; color: #f3f6f9; margin-bottom: 0.6rem; }
.faq-a { font-size: 1.02rem; color: #9aa4b2; line-height: 1.85; }
</style>
""", unsafe_allow_html=True)

# ─── SESSION STATE ─────────────────────────────────────────────────────────────
if "page" not in st.session_state:
    st.session_state.page = "home"
if "vectorstore" not in st.session_state:
    st.session_state.vectorstore = None
if "brief" not in st.session_state:
    st.session_state.brief = None
if "last_company" not in st.session_state:
    st.session_state.last_company = ""
if "last_ticker" not in st.session_state:
    st.session_state.last_ticker = ""

# ─── SIDEBAR NAV ───────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="padding:1.4rem 0 1.4rem;border-bottom:1px solid #1f2530;margin-bottom:1.3rem;">
        <span style="font-family:'Syne',sans-serif;font-size:1.55rem;font-weight:800;color:#2dd4a7;">Fin</span><span style="font-family:'Syne',sans-serif;font-size:1.55rem;font-weight:800;color:#8b96a5;">Lens</span>
        <div style="font-size:0.95rem;color:#9aa4b2;margin-top:0.3rem;">Stock research made simple</div>
    </div>
    <div style="font-size:0.92rem;color:#9aa4b2;letter-spacing:0.06em;text-transform:uppercase;margin-bottom:0.8rem;font-weight:600;">Menu</div>
    """, unsafe_allow_html=True)

    pages = {
        "home":     "🏠  Home",
        "research": "🔍  Get a Report",
        "docs":     "❓  How It Works",
        "about":    "ℹ️  About",
    }
    for key, label in pages.items():
        if st.sidebar.button(label, key=f"nav_{key}", use_container_width=True):
            st.session_state.page = key
            st.rerun()

    st.markdown("""
    <hr style="border:none;border-top:1px solid #1f2530;margin:1.4rem 0;">
    <div style="background:#11151c;border:1px solid #1f2530;border-radius:10px;padding:1rem 1.1rem;">
        <div style="font-size:0.95rem;color:#2dd4a7;font-weight:600;margin-bottom:0.5rem;">💡 Tip</div>
        <div style="font-size:1rem;color:#c2cbd6;line-height:1.7;">Don't know a ticker symbol? Just search the company name + "stock symbol" on Google first.</div>
    </div>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE: HOME
# ══════════════════════════════════════════════════════════════════════════════
def page_home():
    # Ticker tape
    st.markdown("""
    <div class="ticker-bar"><div class="ticker-inner">
        <span class="ticker-item"><span class="sym">AAPL</span> 213.49 <span class="up">+1.24 (+0.58%)</span></span>
        <span class="ticker-item"><span class="sym">MSFT</span> 429.11 <span class="up">+3.72 (+0.87%)</span></span>
        <span class="ticker-item"><span class="sym">GOOGL</span> 178.44 <span class="dn">-0.93 (-0.52%)</span></span>
        <span class="ticker-item"><span class="sym">NVDA</span> 134.25 <span class="up">+5.18 (+4.01%)</span></span>
        <span class="ticker-item"><span class="sym">TSLA</span> 248.33 <span class="dn">-4.11 (-1.63%)</span></span>
        <span class="ticker-item"><span class="sym">AMZN</span> 215.70 <span class="up">+2.05 (+0.96%)</span></span>
        <span class="ticker-item"><span class="sym">META</span> 573.22 <span class="up">+8.44 (+1.49%)</span></span>
        <span class="ticker-item"><span class="sym">JPM</span> 241.87 <span class="dn">-1.32 (-0.54%)</span></span>
        <span class="ticker-item"><span class="sym">NFLX</span> 718.44 <span class="up">+11.23 (+1.59%)</span></span>
        <span class="ticker-item"><span class="sym">AMD</span> 162.88 <span class="dn">-3.41 (-2.05%)</span></span>
        <span class="ticker-item"><span class="sym">AAPL</span> 213.49 <span class="up">+1.24 (+0.58%)</span></span>
        <span class="ticker-item"><span class="sym">MSFT</span> 429.11 <span class="up">+3.72 (+0.87%)</span></span>
        <span class="ticker-item"><span class="sym">GOOGL</span> 178.44 <span class="dn">-0.93 (-0.52%)</span></span>
        <span class="ticker-item"><span class="sym">NVDA</span> 134.25 <span class="up">+5.18 (+4.01%)</span></span>
        <span class="ticker-item"><span class="sym">TSLA</span> 248.33 <span class="dn">-4.11 (-1.63%)</span></span>
        <span class="ticker-item"><span class="sym">AMZN</span> 215.70 <span class="up">+2.05 (+0.96%)</span></span>
        <span class="ticker-item"><span class="sym">META</span> 573.22 <span class="up">+8.44 (+1.49%)</span></span>
        <span class="ticker-item"><span class="sym">JPM</span> 241.87 <span class="dn">-1.32 (-0.54%)</span></span>
    </div></div>
    """, unsafe_allow_html=True)

    # Hero — speaks to the outcome, not the technology
    col_left, col_right = st.columns([1.1, 1], gap="large")
    with col_left:
        st.markdown('<div class="fl-eyebrow">Know before you invest</div>', unsafe_allow_html=True)
        st.markdown('<h1 class="fl-hero-title">Understand any stock in <em>plain English.</em></h1>', unsafe_allow_html=True)
        st.markdown('<p class="fl-sub">Type in a company name and get back a clear, easy-to-read report — current price, what\'s happening in the news, and what it all means. No finance degree required.</p>', unsafe_allow_html=True)
        if st.button("▶  Get My First Report", key="hero_cta"):
            st.session_state.page = "research"
            st.rerun()

    with col_right:
        st.markdown("""
        <div class="terminal">
            <div class="term-bar">
                <span class="term-dot" style="background:#f06868;"></span>
                <span class="term-dot" style="background:#f5b942;"></span>
                <span class="term-dot" style="background:#4ade80;"></span>
                <span class="term-title">Live preview</span>
            </div>
            <div class="term-body">
                <span style="display:block"><span class="term-prompt">●</span> <span class="term-cmd">Looking up Apple Inc (AAPL)</span></span>
                <span style="display:block" class="term-out">Checking today's price and key numbers...</span>
                <span style="display:block" class="term-out hi">✓ Price: $213.49 · steady performance this week</span>
                <span style="display:block" class="term-out">Scanning the latest headlines...</span>
                <span style="display:block" class="term-out hi">✓ 8 recent stories found, last 3 days</span>
                <span style="display:block" class="term-out">Reading any documents you've shared...</span>
                <span style="display:block" class="term-out hi">✓ Key sections found and summarized</span>
                <span style="display:block" class="term-out">Putting it all into a clear report...</span>
                <span style="display:block" class="term-out warn">▶ Almost ready...</span>
                <span style="display:block">&nbsp;</span>
                <span style="display:block" class="term-out hi">✓ Your report is ready <span class="term-cursor"></span></span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Stats strip — outcomes, not specs
    st.markdown('<hr class="divider">', unsafe_allow_html=True)
    s1, s2, s3, s4 = st.columns(4)
    for col, val, lbl in [
        (s1, "<em>&lt;</em>30s",  "To get your report"),
        (s2, "0",                "Jargon you need to know"),
        (s3, "<em>Any</em>",     "Public company"),
        (s4, "<em>Free</em>",    "To try it out"),
    ]:
        col.markdown(f'<div class="stat-box"><span class="stat-val">{val}</span><span class="stat-lbl">{lbl}</span></div>', unsafe_allow_html=True)
    st.markdown('<hr class="divider">', unsafe_allow_html=True)

    # Features — framed as customer benefits
    st.markdown('<div class="fl-eyebrow">What you get</div>', unsafe_allow_html=True)
    st.markdown('<h2 class="fl-section-title">Everything you need, nothing you don\'t</h2>', unsafe_allow_html=True)
    st.markdown('<p class="fl-sub">No charts to decode. No spreadsheets to build. Just a straight answer about the company you\'re curious about.</p>', unsafe_allow_html=True)

    feats = [
        ("💵", "Today's price, explained",  "See exactly what a stock costs right now, how it's been trending, and what the key numbers actually mean — written in everyday language."),
        ("📰", "Catch up on the news",       "We read through the latest headlines about the company so you don't have to — earnings, leadership changes, big announcements, all summarized."),
        ("📂", "Upload a report, get answers", "Have an annual report or filing sitting in a PDF? Drop it in and we'll pull out the parts that actually matter to your decision."),
        ("✍️", "Written like a person wrote it", "Every report reads like a knowledgeable friend explaining things over coffee — not a wall of financial jargon."),
        ("⚡", "Done in under 30 seconds",   "No waiting around. Type in a company, hit one button, and your report is ready before you've finished your sentence."),
        ("⬇️", "Yours to keep",              "Download every report as a simple text file. Save it, email it to a friend, or print it out for later."),
    ]
    r1 = st.columns(3, gap="medium")
    r2 = st.columns(3, gap="medium")
    for i, (icon, title, desc) in enumerate(feats):
        col = (r1 + r2)[i]
        col.markdown(f"""
        <div class="feat-card" style="animation-delay:{i*0.05}s;">
            <span class="feat-icon">{icon}</span>
            <div class="feat-title">{title}</div>
            <div class="feat-desc">{desc}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('<hr class="divider">', unsafe_allow_html=True)

    # How It Works — customer steps
    st.markdown('<div class="fl-eyebrow">Getting started</div>', unsafe_allow_html=True)
    st.markdown('<h2 class="fl-section-title">From a company name to a full report in four steps</h2>', unsafe_allow_html=True)
    st.markdown('<p class="fl-sub">No setup, no account, nothing to install. Just open the Report page and go.</p>', unsafe_allow_html=True)

    steps = [
        ("01", "Type the company name",  "Just the name and its stock symbol. Have a report or filing as a PDF? You can add that too, but it's totally optional."),
        ("02", "We do the digging",      "We check today's price, scan recent news, and read through anything you uploaded — all happening in the background."),
        ("03", "Your report comes together", "Everything gets pulled into one clear, easy-to-read summary that explains what's going on and why it matters."),
        ("04", "Read it, save it, share it", "Your report shows up right on screen. Download it whenever you want a copy to keep or send along."),
    ]
    cols = st.columns(4, gap="medium")
    for i, (col, (num, title, desc)) in enumerate(zip(cols, steps)):
        col.markdown(f"""
        <div class="step-box" style="animation-delay:{i*0.06}s;">
            <div class="step-num">{num}</div>
            <div class="step-title">{title}</div>
            <div class="step-desc">{desc}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('<hr class="divider">', unsafe_allow_html=True)

    # Trust strip — replaces the old "Stack" tech section
    st.markdown('<div class="fl-eyebrow">Why people trust it</div>', unsafe_allow_html=True)
    st.markdown('<h2 class="fl-section-title">Built to be accurate, not impressive-sounding</h2>', unsafe_allow_html=True)
    sc1, sc2 = st.columns(2, gap="medium")
    sc3, sc4 = st.columns(2, gap="medium")
    trust = [
        (sc1, "🔒", "Your documents stay private",  "Anything you upload is only used to build your report. It isn't stored, shared, or used for anything else."),
        (sc2, "📊", "Real numbers, every time",      "Prices and figures come from live market data — never guessed, never made up. If we don't know something, we won't pretend to."),
        (sc3, "🌍", "Always current",                "News and prices are checked fresh every single time you ask, so you're never looking at old information."),
        (sc4, "🆓", "No catches",                     "No account required, no hidden steps. Open the app, type a name, get your report."),
    ]
    for col, icon, name, desc in trust:
        col.markdown(f"""
        <div class="stack-card" style="background:#11151c;border:1px solid #1f2530;border-left:3px solid #2dd4a7;border-radius:12px;padding:1.6rem;">
            <div style="font-size:1.6rem;margin-bottom:0.6rem;">{icon}</div>
            <div style="font-family:'Syne',sans-serif;font-size:1.15rem;font-weight:700;color:#f3f6f9;margin-bottom:0.5rem;">{name}</div>
            <div style="font-size:1rem;color:#9aa4b2;line-height:1.8;">{desc}</div>
        </div>
        """, unsafe_allow_html=True)

    # CTA
    st.markdown('<hr class="divider">', unsafe_allow_html=True)
    st.markdown("""
    <div class="cta-banner">
        <div class="cta-title">Curious about a stock? Find out now.</div>
        <div class="cta-sub">Type in a name. Get a clear answer in under 30 seconds.</div>
    </div>
    """, unsafe_allow_html=True)
    col_cta, _, _ = st.columns([1, 2, 2])
    with col_cta:
        if st.button("▶  Get My First Report", key="bottom_cta"):
            st.session_state.page = "research"
            st.rerun()


# ══════════════════════════════════════════════════════════════════════════════
# PAGE: RESEARCH APP
# ══════════════════════════════════════════════════════════════════════════════
def page_research():
    try:
        from rag.rag_pipeline import build_vectorstore
        from agent.tools import set_vectorstore
        from agent.agent import run_agent
        agent_available = True
    except ImportError:
        agent_available = False

    st.markdown('<div class="fl-eyebrow">Get a Report</div>', unsafe_allow_html=True)
    st.markdown('<h1 style="font-family:\'Syne\',sans-serif;font-size:2.3rem;font-weight:800;color:#f3f6f9;letter-spacing:-0.02em;margin-bottom:0.4rem;">Tell us who you\'re curious about</h1>', unsafe_allow_html=True)
    st.markdown('<p style="font-size:1.08rem;color:#9aa4b2;margin-bottom:2.2rem;">Type in a company and its stock symbol below, and we\'ll put together a clear report for you.</p>', unsafe_allow_html=True)

    if not agent_available:
        st.markdown("""
        <div class="info-box">
            <strong>One more step needed</strong>
            This app isn't fully set up yet. If you're the site owner, make sure all required project files are in place and try again.
        </div>
        """, unsafe_allow_html=True)
        return

    col1, col2 = st.columns(2, gap="medium")
    with col1:
        company_name = st.text_input("Company Name", placeholder="e.g. Apple Inc")
    with col2:
        ticker = st.text_input("Stock Symbol", placeholder="e.g. AAPL")

    st.markdown('<p style="font-size:1.05rem;color:#aab4c2;font-weight:600;border-bottom:1px solid #1f2530;padding-bottom:0.5rem;margin-top:1rem;font-weight:500;">Have a report or filing as a PDF? Add it here (optional)</p>', unsafe_allow_html=True)
    uploaded_pdf = st.file_uploader("Upload PDF", type=["pdf"], label_visibility="collapsed")

    if uploaded_pdf:
        pdf_key = (uploaded_pdf.name, uploaded_pdf.size)
        if st.session_state.get("pdf_key") != pdf_key:
            with st.spinner("Reading your document..."):
                st.session_state.vectorstore = build_vectorstore(uploaded_pdf)
                st.session_state.pdf_key = pdf_key
        st.success("Got it — your document is ready to use.")
    else:
        st.session_state.vectorstore = None
        st.session_state.pdf_key = None

    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("▶  Create My Report", key="gen_brief"):
        if not company_name or not ticker:
            st.warning("Please fill in both the company name and stock symbol.")
        else:
            set_vectorstore(st.session_state.get("vectorstore"))
            st.session_state.last_company = company_name
            st.session_state.last_ticker = ticker.upper()
            with st.spinner(f"Putting together your report on {company_name}... this takes about 20–30 seconds"):
                try:
                    brief = run_agent(company_name, ticker)
                    st.session_state.brief = brief
                except Exception as e:
                    st.error(f"Something went wrong: {str(e)}")

    if st.session_state.brief:
        st.markdown('<p style="font-size:1.05rem;color:#aab4c2;font-weight:600;border-bottom:1px solid #1f2530;padding-bottom:0.5rem;margin-top:2rem;font-weight:500;">Your Report</p>', unsafe_allow_html=True)
        safe_brief = st.session_state.brief.replace("$", "\\$")
        with st.container(border=True):
            st.markdown(safe_brief)
        st.markdown("<br>", unsafe_allow_html=True)
        st.download_button(
            label="⬇  Save This Report",
            data=st.session_state.brief,
            file_name=f"{st.session_state.last_ticker}_FinLens_Report.txt",
            mime="text/plain",
        )


# ══════════════════════════════════════════════════════════════════════════════
# PAGE: HOW IT WORKS (USER-FACING)
# ══════════════════════════════════════════════════════════════════════════════
def page_docs():
    st.markdown('<div class="fl-eyebrow">How It Works</div>', unsafe_allow_html=True)
    st.markdown('<h1 style="font-family:\'Syne\',sans-serif;font-size:2.4rem;font-weight:800;color:#f3f6f9;letter-spacing:-0.02em;margin-bottom:0.6rem;">Your report, ready in under 30 seconds.</h1>', unsafe_allow_html=True)
    st.markdown('<p style="font-size:1.12rem;color:#9aa4b2;line-height:1.85;max-width:680px;margin-bottom:2.6rem;">FinLens checks today\'s price, scans the latest news, and reads through any document you share — then writes you a clean, easy-to-follow report. No copy-pasting. No tab-switching. Just answers.</p>', unsafe_allow_html=True)

    st.markdown('<hr class="divider">', unsafe_allow_html=True)

    # Step by step
    st.markdown('<div class="fl-eyebrow">Step by Step</div>', unsafe_allow_html=True)
    st.markdown('<h2 class="fl-section-title" style="margin-bottom:0.5rem;">Using FinLens</h2>', unsafe_allow_html=True)
    st.markdown('<p style="font-size:1.05rem;color:#9aa4b2;margin-bottom:1.6rem;">Follow these four steps every time you want a report.</p>', unsafe_allow_html=True)

    for num, title, desc in [
        ("01", "Type in the company",
         "Enter the full company name — for example, <em style='color:#dce3eb;'>Apple Inc</em> or <em style='color:#dce3eb;'>Tesla</em>. Then enter its stock symbol in the second box — for example, <em style='color:#dce3eb;'>AAPL</em> or <em style='color:#dce3eb;'>TSLA</em>. Not sure of the symbol? A quick Google search for the company name plus \"stock symbol\" will give it to you instantly."),
        ("02", "Add a document (optional)",
         "If you have the company's annual report or any financial document as a PDF, you can upload it. FinLens will read through it and pull the most useful parts into your report. This is completely optional — skip it and you'll still get a full report using live prices and the latest news."),
        ("03", "Click Create My Report",
         "Hit the <strong style='color:#f3f6f9;'>▶ Create My Report</strong> button. FinLens will check the current price, look for recent news, and read your document if you added one. This usually takes 20–30 seconds, with a loading message to let you know it's working."),
        ("04", "Read and save",
         "Your report appears on screen, covering the company's current standing, recent news, and key numbers. Use the <strong style='color:#f3f6f9;'>⬇ Save This Report</strong> button to keep it as a text file — ready to share or hang on to."),
    ]:
        st.markdown(f"""
        <div style="display:flex;gap:1.6rem;border-bottom:1px solid #1f2530;padding:1.6rem 0;align-items:flex-start;">
            <div style="font-family:'Syne',sans-serif;font-size:2.1rem;font-weight:800;color:#232b38;min-width:50px;line-height:1;">{num}</div>
            <div>
                <div style="font-family:'Syne',sans-serif;font-size:1.18rem;font-weight:700;color:#f3f6f9;margin-bottom:0.5rem;">{title}</div>
                <div style="font-size:1.02rem;color:#9aa4b2;line-height:1.85;">{desc}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('<hr class="divider">', unsafe_allow_html=True)

    # What's in a report
    st.markdown('<div class="fl-eyebrow">What You Get</div>', unsafe_allow_html=True)
    st.markdown('<h2 class="fl-section-title" style="margin-bottom:0.5rem;">What\'s inside every report</h2>', unsafe_allow_html=True)
    st.markdown('<p style="font-size:1.05rem;color:#9aa4b2;margin-bottom:1.6rem;">Every report FinLens puts together covers the same key areas.</p>', unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3, gap="medium")
    for col, icon, title, desc in [
        (c1, "📈", "Today's price, plain and simple",
         "Current stock price, how big the company is, and the everyday numbers people use to judge a stock — all pulled in real time and explained clearly."),
        (c2, "📰", "What's been happening lately",
         "A summary of the company's recent news — earnings, product launches, leadership changes, and anything else worth knowing about, written in plain language."),
        (c3, "📄", "The important parts of your document",
         "If you shared a report or filing, FinLens pulls out the most relevant parts and works them into your report — so you don't have to read all 200 pages yourself."),
    ]:
        col.markdown(f"""
        <div class="feat-card" style="text-align:center;padding:2.2rem 1.5rem;">
            <div style="font-size:2.2rem;margin-bottom:1.1rem;">{icon}</div>
            <div class="feat-title">{title}</div>
            <div class="feat-desc">{desc}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('<hr class="divider">', unsafe_allow_html=True)

    # FAQ
    st.markdown('<div class="fl-eyebrow">Common Questions</div>', unsafe_allow_html=True)
    st.markdown('<h2 class="fl-section-title" style="margin-bottom:1.6rem;">Frequently asked</h2>', unsafe_allow_html=True)

    faqs = [
        ("Do I need to create an account?",
         "No. FinLens is free to try with no sign-up required. Just open the app and start exploring."),
        ("What format should my document be in?",
         "PDF only. Annual reports, official filings, earnings transcripts, investor presentations — anything in PDF form works. Files up to around 200MB are fine."),
        ("How up to date is the information?",
         "Prices and figures are checked fresh every time you create a report. News comes from the last few days. If something major happened recently, it'll be included."),
        ("Can I look up any company?",
         "Any publicly traded company with a stock symbol — that covers all the major US markets and most international ones too. Private companies aren't included since they don't have public stock data."),
        ("How long does it take?",
         "Usually 20–30 seconds. If you added a large document, it might take a few extra seconds to read through before you click the button."),
        ("Can I save or share my report?",
         "Yes. Use the Save This Report button to download it as a text file. From there you can email it, paste it somewhere, or keep it for later."),
    ]
    for q, a in faqs:
        st.markdown(f"""
        <div class="faq-row">
            <div class="faq-q">{q}</div>
            <div class="faq-a">{a}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('<hr class="divider">', unsafe_allow_html=True)
    st.markdown("""
    <div class="cta-banner">
        <div class="cta-title">Ready to try it?</div>
        <div class="cta-sub">Enter a company name and get your report in under 30 seconds.</div>
    </div>
    """, unsafe_allow_html=True)
    col_btn, _, _ = st.columns([1, 2, 2])
    with col_btn:
        if st.button("▶  Start Now", key="docs_cta"):
            st.session_state.page = "research"
            st.rerun()


# ══════════════════════════════════════════════════════════════════════════════
# PAGE: ABOUT
# ══════════════════════════════════════════════════════════════════════════════
def page_about():
    st.markdown('<div class="fl-eyebrow">About</div>', unsafe_allow_html=True)
    st.markdown('<h1 style="font-family:\'Syne\',sans-serif;font-size:2.4rem;font-weight:800;color:#f3f6f9;letter-spacing:-0.02em;max-width:700px;line-height:1.18;margin-bottom:1.1rem;">Understanding a stock shouldn\'t require a finance degree.</h1>', unsafe_allow_html=True)
    st.markdown('<p class="fl-sub" style="max-width:640px;font-size:1.15rem;">Professional investors have teams of analysts and expensive tools at their fingertips. FinLens brings that same depth of insight to everyday people — in seconds, in plain language, for free.</p>', unsafe_allow_html=True)

    st.markdown("""
    <div class="blockquote">
        <q>"Anyone curious about a company should be able to get a real, trustworthy answer — not a vague summary, not financial jargon, just a clear picture backed by real data."</q>
        <cite>— FinLens · Our Mission</cite>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<hr class="divider">', unsafe_allow_html=True)

    col_left, col_right = st.columns(2, gap="large")

    with col_left:
        st.markdown('<h2 style="font-family:\'Syne\',sans-serif;font-size:1.4rem;font-weight:800;color:#f3f6f9;margin-bottom:1.1rem;">What We Built</h2>', unsafe_allow_html=True)
        for para in [
            "FinLens was built from the ground up for one job: turning scattered financial information into something a regular person can actually read and use. It's not a general chatbot wearing a finance costume — every part of it is purpose-built for understanding companies and stocks.",
            "FinLens adapts to what you're researching. Share a document and it digs deeper into that. Ask about a company that's been in the news and it leans on the latest headlines. You don't have to tell it how to do its job — it figures that out.",
            "Your privacy matters here. Anything you upload is used only to build your report, never stored or shared beyond what's needed to answer your question.",
        ]:
            st.markdown(f'<p class="doc-p">{para}</p>', unsafe_allow_html=True)

        st.markdown('<h2 style="font-family:\'Syne\',sans-serif;font-size:1.3rem;font-weight:800;color:#f3f6f9;margin:1.6rem 0 0.9rem;">What you can count on</h2>', unsafe_allow_html=True)
        pills = ["Real-time prices", "Fresh news, every time", "Private by design", "No account needed", "Free to try", "Plain-language reports"]
        st.markdown("".join(f'<span class="trust-pill">{p}</span>' for p in pills), unsafe_allow_html=True)

    with col_right:
        st.markdown('<h2 style="font-family:\'Syne\',sans-serif;font-size:1.4rem;font-weight:800;color:#f3f6f9;margin-bottom:1.1rem;">What We Stand For</h2>', unsafe_allow_html=True)
        principles = [
            ("Principle 01", "Fast, without cutting corners",  "We chose technology that's quick enough to feel instant, without sacrificing the depth of thinking it takes to actually understand a company well."),
            ("Principle 02", "Grounded in real facts",          "Every number and claim in a FinLens report comes from an actual data check — live prices, real news, your real documents. Nothing is ever made up or guessed."),
            ("Principle 03", "Your information stays yours",    "Documents you share are read locally to build your report and nothing more. We don't keep copies, sell your data, or hand it off to anyone else."),
            ("Principle 04", "Built to be useful, not flashy",  "Every choice we make is about getting you a clearer answer, faster — not about sounding impressive. If a feature doesn't help you make a better decision, it doesn't make the cut."),
        ]
        for role, name, desc in principles:
            st.markdown(f"""
            <div class="principle-card">
                <div class="principle-role">{role}</div>
                <div class="principle-name">{name}</div>
                <div class="principle-desc">{desc}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown('<hr class="divider">', unsafe_allow_html=True)
    st.markdown("""
    <div class="cta-banner">
        <div class="cta-title">Ready to try it?</div>
        <div class="cta-sub">See how it works for yourself — it only takes a minute.</div>
    </div>
    """, unsafe_allow_html=True)
    col_btn, _, _ = st.columns([1, 2, 2])
    with col_btn:
        if st.button("▶  See How It Works", key="about_docs_cta"):
            st.session_state.page = "docs"
            st.rerun()


# ─── ROUTER ───────────────────────────────────────────────────────────────────
if st.session_state.page == "home":
    page_home()
elif st.session_state.page == "research":
    page_research()
elif st.session_state.page == "docs":
    page_docs()
elif st.session_state.page == "about":
    page_about()