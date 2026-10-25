"""Shared responsive design system for the Slow & Steady apps."""
import streamlit as st


LIGHT = {
    "bg": "#f5f7f5", "surface": "#ffffff", "surface2": "#edf2ee",
    "text": "#172b25", "muted": "#5c6d65", "border": "#dce5df",
    "accent": "#176b52", "accent_hover": "#105640", "accent_text": "#ffffff",
    "input": "#ffffff", "shadow": "0 8px 28px rgba(21, 45, 35, .06)",
}
DARK = {
    "bg": "#0c1311", "surface": "#131e19", "surface2": "#1b2a23",
    "text": "#e8f1eb", "muted": "#a3b5aa", "border": "#2b4035",
    "accent": "#75d6ac", "accent_hover": "#9be7c4", "accent_text": "#082016",
    "input": "#101a15", "shadow": "0 10px 32px rgba(0, 0, 0, .18)",
}


def configure_page(title: str, icon: str, description: str) -> None:
    st.set_page_config(
        page_title=f"{title} · Slow & Steady", page_icon=icon,
        layout="wide", initial_sidebar_state="collapsed",
    )
    theme_key = "slow_steady_dark_mode"
    if theme_key not in st.session_state:
        st.session_state[theme_key] = False
    dark = st.toggle("Dark theme", key=theme_key, help="Switch between light and dark appearance")
    c = DARK if dark else LIGHT
    st.markdown(
        f"""
        <style>
        :root {{ color-scheme: {'dark' if dark else 'light'}; }}
        .stApp {{ background: {c['bg']}; color: {c['text']}; }}
        [data-testid="stHeader"] {{ background: {c['bg']}; }}
        [data-testid="stToolbar"] {{ right: 1rem; }}
        .block-container {{ max-width: 1180px; padding: 1.3rem 1.5rem 3.5rem; }}
        .brand-row {{ display:flex; align-items:center; gap:.7rem; margin:.35rem 0 1.4rem; }}
        .brand-mark {{ display:inline-flex; align-items:center; justify-content:center; width:2.55rem; height:2.55rem; border-radius:.9rem; background:{c['accent']}; color:{c['accent_text']}; font-size:1.15rem; box-shadow:{c['shadow']}; }}
        .brand-name {{ color:{c['text']}; font-size:.92rem; font-weight:850; letter-spacing:.04em; }}
        .brand-sub {{ color:{c['muted']}; font-size:.76rem; font-weight:550; letter-spacing:.08em; }}
        .eyebrow, .section-label {{ color:{c['accent']}; font-size:.72rem; text-transform:uppercase; letter-spacing:.14em; font-weight:800; margin-bottom:.5rem; }}
        h1 {{ color:{c['text']} !important; letter-spacing:-.055em; font-weight:820 !important; line-height:1.04 !important; margin:.1rem 0 .55rem !important; }}
        h2, h3, h4 {{ color:{c['text']} !important; letter-spacing:-.025em; }}
        p, li, label, [data-testid="stMarkdownContainer"] {{ color:{c['text']}; }}
        .hero-copy {{ color:{c['muted']}; font-size:1.04rem; line-height:1.7; max-width:790px; margin-bottom:1.5rem; }}
        div[data-testid="stVerticalBlockBorderWrapper"], div[data-testid="stForm"] {{ border:1px solid {c['border']}; border-radius:18px; background:{c['surface']}; box-shadow:{c['shadow']}; }}
        div[data-testid="stVerticalBlockBorderWrapper"] {{ padding:1.1rem 1.15rem; }}
        div.stButton > button, div.stDownloadButton > button {{ border-radius:11px; min-height:2.7rem; font-weight:700; border:1px solid {c['border']}; background:{c['surface']}; color:{c['text']}; transition:transform .15s ease, border-color .15s ease, background .15s ease; }}
        div.stButton > button:hover, div.stDownloadButton > button:hover {{ border-color:{c['accent']}; transform:translateY(-1px); }}
        div.stButton > button[kind="primary"] {{ background:{c['accent']}; border-color:{c['accent']}; color:{c['accent_text']}; }}
        div.stButton > button[kind="primary"]:hover {{ background:{c['accent_hover']}; border-color:{c['accent_hover']}; color:{c['accent_text']}; }}
        [data-testid="stMetric"] {{ background:{c['surface']}; border:1px solid {c['border']}; padding:1rem 1.05rem; border-radius:15px; }}
        [data-testid="stMetricLabel"], [data-testid="stCaptionContainer"] {{ color:{c['muted']} !important; }}
        [data-testid="stDataFrame"], [data-testid="stTable"] {{ border:1px solid {c['border']}; border-radius:13px; overflow:hidden; }}
        textarea, input, [data-baseweb="select"] > div {{ border-radius:10px !important; }}
        [data-baseweb="input"] > div, [data-baseweb="textarea"] > div, [data-baseweb="select"] > div {{ background:{c['input']}; border-color:{c['border']}; }}
        [data-testid="stExpander"] {{ border:1px solid {c['border']}; border-radius:13px; background:{c['surface']}; }}
        .privacy-note {{ color:{c['muted']}; background:{c['surface2']}; border:1px solid {c['border']}; padding:.9rem 1rem; border-radius:12px; font-size:.88rem; line-height:1.55; }}
        .footer {{ margin-top:2.5rem; border-top:1px solid {c['border']}; padding-top:1rem; color:{c['muted']}; font-size:.8rem; }}
        [data-testid="stAlert"] {{ border-radius:12px; }}
        :focus-visible {{ outline:2px solid {c['accent']}; outline-offset:2px; }}
        @media (max-width: 700px) {{ .block-container {{ padding:.8rem .8rem 2.5rem; }} .hero-copy {{ font-size:.96rem; }} .brand-sub {{ display:block; margin-top:.15rem; }} }}
        @media (prefers-reduced-motion: reduce) {{ *, *::before, *::after {{ transition:none !important; animation:none !important; scroll-behavior:auto !important; }} }}
        </style>
        """,
        unsafe_allow_html=True,
    )
    st.markdown(
        f'<div class="brand-row"><span class="brand-mark">{icon}</span><span><span class="brand-name">SLOW &amp; STEADY</span><br><span class="brand-sub">LOCAL AI TOOLKIT</span></span></div>',
        unsafe_allow_html=True,
    )
    st.markdown(f'<div class="eyebrow">{title} / WORKSPACE</div>', unsafe_allow_html=True)
    st.title(title)
    st.markdown(f'<div class="hero-copy">{description}</div>', unsafe_allow_html=True)


def footer() -> None:
    st.markdown(
        '<div class="footer">Built for deliberate, local-first workflows · Review AI output before acting · Your files are never modified automatically.</div>',
        unsafe_allow_html=True,
    )
