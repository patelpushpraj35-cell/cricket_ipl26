import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import os

# Set page configuration
st.set_page_config(
    page_title="IPL Analytics Dashboard - Cricket Analytics",
    page_icon="🏏",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom premium styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&display=swap');
    
    html, body, [data-testid="stSidebar"] {
        font-family: 'Outfit', sans-serif;
    }
    
    /* Global text color inheritance to prevent light mode issues */
    label, [data-testid="stWidgetLabel"] p, .stSlider p, [data-testid="stMarkdownContainer"] p {
        color: var(--text-color) !important;
    }
    
    /* Hide Deploy button but keep hamburger menu for sidebar */
    .stDeployButton {
        display: none !important;
    }
    [data-testid="stToolbar"] {
        visibility: hidden !important;
    }
    [data-testid="stHeader"] {
        background-color: transparent !important;
        visibility: visible !important;
        display: block !important;
    }
    [data-testid="collapsedControl"] {
        display: flex !important;
        visibility: visible !important;
        color: var(--primary-color, #10B981) !important;
        background: rgba(16, 185, 129, 0.2) !important;
        border-radius: 50% !important;
        z-index: 999999 !important;
    }
    [data-testid="collapsedControl"] svg {
        fill: var(--primary-color, #10B981) !important;
    }
    
    /* Add padding to compensate for header */
    [data-testid="block-container"] {
        padding-top: 2rem !important;
    }
    
    /* Sleek card container */
    .glass-card {
        background: var(--glass-bg, rgba(255, 255, 255, 0.04));
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border: 1px solid var(--glass-border, rgba(255, 255, 255, 0.1));
        border-radius: 16px;
        padding: 24px;
        margin-bottom: 24px;
        box-shadow: 0 8px 32px 0 var(--glass-shadow, rgba(0, 0, 0, 0.15));
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    }
    .glass-card:hover {
        border-color: var(--primary-color, #10B981);
        transform: translateY(-4px);
        box-shadow: 0 12px 40px 0 rgba(16, 185, 129, 0.2);
    }
    
    .card-title {
        color: var(--text-color);
        font-size: 1.25rem;
        font-weight: 600;
        margin-bottom: 8px;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    .card-body {
        color: var(--text-color);
        opacity: 0.9;
        font-size: 0.95rem;
        line-height: 1.5;
    }
    
    /* Metrics customization */
    div[data-testid="stMetric"] {
        background: var(--glass-bg, rgba(255, 255, 255, 0.03));
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border: 1px solid var(--glass-border, rgba(255, 255, 255, 0.1));
        border-radius: 16px;
        padding: 18px 24px;
        text-align: center;
        box-shadow: 0 4px 15px var(--glass-shadow, rgba(0, 0, 0, 0.1));
        transition: all 0.3s ease;
    }
    div[data-testid="stMetricValue"] *, div[data-testid="stMetricValue"] {
        color: var(--primary-color, #10B981) !important;
        font-weight: 700;
        font-size: 2.2rem;
    }
    div[data-testid="stMetricLabel"] *, div[data-testid="stMetricLabel"], [data-testid="stMetricLabel"] p {
        color: var(--text-color) !important;
        opacity: 0.9 !important;
        font-size: 0.9rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    /* Gradient headers */
    .gradient-header {
        color: var(--text-color);
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 5px;
    }
    .gradient-subtitle {
        color: var(--text-color);
        opacity: 0.7;
        font-size: 1.1rem;
        margin-bottom: 12px;
    }
    .header-line {
        height: 4px;
        background: linear-gradient(90deg, #10B981, #3B82F6);
        border-radius: 2px;
        margin-bottom: 25px;
    }
    
    /* Success highlight banner */
    .highlight-banner {
        background: linear-gradient(135deg, rgba(16, 185, 129, 0.1), rgba(59, 130, 246, 0.1));
        border-left: 5px solid #10B981;
        border-radius: 4px 12px 12px 4px;
        padding: 20px;
        margin: 20px 0;
    }

    /* Fun fact / tip callout box */
    .fun-fact-box {
        background: linear-gradient(135deg, rgba(251, 191, 36, 0.12), rgba(245, 158, 11, 0.06));
        border-left: 5px solid #F59E0B;
        border-radius: 4px 12px 12px 4px;
        padding: 14px 18px;
        margin: 14px 0;
        font-size: 0.95rem;
        line-height: 1.6;
        color: var(--text-color);
    }
    .fun-fact-box b { color: #F59E0B; }

    /* Plain-English "What This Means" box */
    .plain-explain {
        background: linear-gradient(135deg, rgba(59, 130, 246, 0.10), rgba(16, 185, 129, 0.06));
        border-left: 5px solid #3B82F6;
        border-radius: 4px 12px 12px 4px;
        padding: 14px 18px;
        margin: 10px 0;
        font-size: 0.92rem;
        line-height: 1.65;
        color: var(--text-color);
    }

    /* Progress bar track */
    .phase-bar-wrap { margin: 8px 0; }
    .phase-bar-label { font-size: 0.88rem; margin-bottom: 3px; }
    .phase-bar-track {
        background: rgba(128,128,128,0.15);
        border-radius: 20px;
        height: 14px;
        overflow: hidden;
        width: 100%;
    }
    .phase-bar-fill {
        height: 14px;
        border-radius: 20px;
        transition: width 0.8s ease;
    }
    .phase-bar-pct { font-size: 0.82rem; margin-top: 2px; opacity: 0.75; }
    /* Hero banner image */
    .hero-banner {
        position: relative;
        width: 100%;
        border-radius: 16px;
        overflow: hidden;
        margin-bottom: 20px;
        box-shadow: 0 8px 32px rgba(0,0,0,0.4);
        animation: fadeInUp 0.7s ease both;
    }
    .hero-banner img {
        width: 100%;
        height: 220px;
        object-fit: cover;
        object-position: center 40%;
        display: block;
        border-radius: 16px;
        transition: transform 0.6s ease;
    }
    .hero-banner:hover img {
        transform: scale(1.03);
    }
    .hero-overlay {
        position: absolute;
        inset: 0;
        background: linear-gradient(90deg,
            rgba(0,0,0,0.92) 0%,
            rgba(0,0,0,0.80) 35%,
            rgba(0,0,0,0.40) 65%,
            rgba(0,0,0,0.05) 100%);
        border-radius: 16px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        padding: 24px 32px;
    }
    .hero-overlay h1 {
        color: #FFFFFF !important;
        -webkit-text-fill-color: #FFFFFF !important;
        font-size: 2rem;
        font-weight: 700;
        margin: 0 0 6px 0;
        text-shadow: 0 2px 16px rgba(0,0,0,0.9), 0 0 40px rgba(0,0,0,0.7);
        animation: slideInLeft 0.7s ease both;
    }
    .hero-overlay p {
        color: #F0F0F0 !important;
        -webkit-text-fill-color: #F0F0F0 !important;
        font-size: 1rem;
        margin: 0;
        text-shadow: 0 1px 8px rgba(0,0,0,0.8);
        animation: slideInLeft 0.8s ease both;
        animation-delay: 0.1s;
    }
    .hero-badge {
        display: inline-block;
        background: linear-gradient(135deg, #10B981, #3B82F6);
        color: white !important;
        font-size: 0.75rem;
        font-weight: 600;
        padding: 3px 10px;
        border-radius: 20px;
        margin-bottom: 8px;
        letter-spacing: 1px;
        text-transform: uppercase;
        animation: scaleIn 0.5s ease both;
    }

    /* Stadium strip */
    .stadium-strip {
        width: 100%;
        border-radius: 12px;
        overflow: hidden;
        margin: 18px 0;
        box-shadow: 0 4px 20px rgba(0,0,0,0.3);
        animation: fadeInUp 0.6s ease both;
        position: relative;
    }
    .stadium-strip img {
        width: 100%;
        height: 130px;
        object-fit: cover;
        object-position: center 30%;
        display: block;
        border-radius: 12px;
        transition: transform 0.5s ease;
        filter: brightness(0.85);
    }
    .stadium-strip:hover img {
        transform: scale(1.02);
        filter: brightness(1.0);
    }
    .stadium-strip-overlay {
        position: absolute;
        inset: 0;
        background: linear-gradient(90deg, rgba(16,185,129,0.55) 0%, rgba(0,0,0,0.0) 100%);
        border-radius: 12px;
        display: flex;
        align-items: center;
        padding: 0 24px;
    }
    .stadium-strip-overlay span {
        color: white;
        font-size: 1.1rem;
        font-weight: 700;
        text-shadow: 0 2px 8px rgba(0,0,0,0.5);
        letter-spacing: 0.5px;
    }

    /* Sidebar logo */
    .sidebar-logo {
        width: 100%;
        border-radius: 10px;
        overflow: hidden;
        margin-bottom: 12px;
        animation: fadeInUp 0.5s ease both;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
    }
    .sidebar-logo img {
        width: 100%;
        height: 100px;
        object-fit: cover;
        object-position: center;
        display: block;
        border-radius: 10px;
        transition: transform 0.4s ease, filter 0.4s ease;
    }
    .sidebar-logo:hover img {
        transform: scale(1.04);
        filter: brightness(1.1);
    }

    /* ===================== ANIMATIONS ===================== */

    /* 1. Fade-up: used for cards, metrics, callout boxes */
    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(24px); }
        to   { opacity: 1; transform: translateY(0);    }
    }

    /* 2. Slide in from left */
    @keyframes slideInLeft {
        from { opacity: 0; transform: translateX(-30px); }
        to   { opacity: 1; transform: translateX(0);     }
    }

    /* 3. Slide in from right */
    @keyframes slideInRight {
        from { opacity: 0; transform: translateX(30px); }
        to   { opacity: 1; transform: translateX(0);    }
    }

    /* 4. Shimmer: sweeping highlight for the header gradient */
    @keyframes shimmer {
        0%   { background-position: -200% center; }
        100% { background-position:  200% center; }
    }

    /* 5. Pulse glow: for the highlight banner border */
    @keyframes pulseGlow {
        0%, 100% { box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.0); }
        50%       { box-shadow: 0 0 18px 6px rgba(16, 185, 129, 0.25); }
    }

    /* 6. Grow-in: for phase bar fill (width 0 → actual) */
    @keyframes growWidth {
        from { width: 0 !important; }
        to   { width: var(--bar-w); }
    }

    /* 7. Float: gentle up-down bob for the cricket ball emoji */
    @keyframes float {
        0%, 100% { transform: translateY(0px);  }
        50%       { transform: translateY(-6px); }
    }

    /* 8. Scale-in: pop-in for metrics */
    @keyframes scaleIn {
        from { opacity: 0; transform: scale(0.85); }
        to   { opacity: 1; transform: scale(1);    }
    }

    /* ===================== APPLY ANIMATIONS ===================== */

    /* Gradient header — animated shimmer text */
    .gradient-header {
        background: linear-gradient(90deg, #10B981, #3B82F6, #10B981, #F59E0B, #10B981);
        background-size: 300% auto;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        animation: shimmer 4s linear infinite;
    }

    /* Subtitle fades up */
    .gradient-subtitle {
        animation: fadeInUp 0.7s ease both;
        animation-delay: 0.2s;
    }

    /* Header line slides in */
    .header-line {
        animation: slideInLeft 0.8s ease both;
        animation-delay: 0.3s;
    }

    /* Glass cards: fade up on load, with stagger via nth-child */
    .glass-card {
        animation: fadeInUp 0.6s ease both;
    }
    .glass-card:hover {
        transform: translateY(-4px) scale(1.01);
        box-shadow: 0 12px 30px rgba(16, 185, 129, 0.2);
        transition: all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
    }

    /* Metric cards: scale pop-in */
    div[data-testid="stMetric"] {
        animation: scaleIn 0.5s cubic-bezier(0.34, 1.56, 0.64, 1) both;
    }
    div[data-testid="stMetric"]:nth-child(1) { animation-delay: 0.0s; }
    div[data-testid="stMetric"]:nth-child(2) { animation-delay: 0.15s; }
    div[data-testid="stMetric"]:nth-child(3) { animation-delay: 0.3s; }
    div[data-testid="stMetric"]:hover {
        transform: translateY(-3px) scale(1.03);
        border-color: var(--primary-color, #10B981) !important;
        box-shadow: 0 8px 20px rgba(16, 185, 129, 0.2) !important;
        transition: all 0.25s ease;
    }

    /* Highlight banner: pulse glow + fade up */
    .highlight-banner {
        animation: fadeInUp 0.7s ease both, pulseGlow 3s ease-in-out infinite;
        animation-delay: 0.1s, 1s;
    }

    /* Plain-explain callout: slide in from left */
    .plain-explain {
        animation: slideInLeft 0.5s ease both;
        animation-delay: 0.15s;
    }

    /* Fun-fact box: slide in from right */
    .fun-fact-box {
        animation: slideInRight 0.5s ease both;
        animation-delay: 0.2s;
    }

    /* Phase bar fills: grow from 0 */
    .phase-bar-fill {
        animation: growWidth 1.2s cubic-bezier(0.22, 1, 0.36, 1) both;
        animation-delay: 0.3s;
    }

    /* Plotly chart containers: fade up */
    [data-testid="stPlotlyChart"] {
        animation: fadeInUp 0.65s ease both;
    }

    /* Dataframe: fade in */
    [data-testid="stDataFrame"] {
        animation: fadeInUp 0.5s ease both;
    }

    /* Tab content area: smooth cross-fade */
    [data-testid="stTabsContent"] > div {
        animation: fadeInUp 0.45s ease both;
    }

    /* Tab buttons: smooth color/scale on hover */
    .stTabs [data-baseweb="tab"] {
        transition: color 0.2s ease, transform 0.2s ease;
    }
    .stTabs [data-baseweb="tab"]:hover {
        transform: translateY(-2px);
    }

    /* Sidebar items fade in */
    [data-testid="stSidebar"] .stMarkdown,
    [data-testid="stSidebar"] .stSelectbox,
    [data-testid="stSidebar"] .stSlider {
        animation: fadeInUp 0.5s ease both;
    }

    /* Selectboxes: smooth border on focus */
    div[data-baseweb="select"] > div {
        transition: border-color 0.25s ease, box-shadow 0.25s ease !important;
    }
    div[data-baseweb="select"] > div:hover {
        border-color: #10B981 !important;
        box-shadow: 0 0 0 2px rgba(16, 185, 129, 0.15) !important;
    }

    /* Subheader sections: slide in */
    h2, h3 {
        animation: slideInLeft 0.5s ease both;
    }


    /* ===================== ANIMATIONS ===================== */

    /* 1. Fade-up: used for cards, metrics, callout boxes */
    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(24px); }
        to   { opacity: 1; transform: translateY(0);    }
    }

    /* 2. Slide in from left */
    @keyframes slideInLeft {
        from { opacity: 0; transform: translateX(-30px); }
        to   { opacity: 1; transform: translateX(0);     }
    }

    /* 3. Slide in from right */
    @keyframes slideInRight {
        from { opacity: 0; transform: translateX(30px); }
        to   { opacity: 1; transform: translateX(0);    }
    }

    /* 4. Shimmer: sweeping highlight for the header gradient */
    @keyframes shimmer {
        0%   { background-position: -200% center; }
        100% { background-position:  200% center; }
    }

    /* 5. Pulse glow: for the highlight banner border */
    @keyframes pulseGlow {
        0%, 100% { box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.0); }
        50%       { box-shadow: 0 0 18px 6px rgba(16, 185, 129, 0.25); }
    }

    /* 6. Grow-in: for phase bar fill (width 0 → actual) */
    @keyframes growWidth {
        from { width: 0 !important; }
        to   { width: var(--bar-w); }
    }

    /* 7. Float: gentle up-down bob for the cricket ball emoji */
    @keyframes float {
        0%, 100% { transform: translateY(0px);  }
        50%       { transform: translateY(-6px); }
    }

    /* 8. Scale-in: pop-in for metrics */
    @keyframes scaleIn {
        from { opacity: 0; transform: scale(0.85); }
        to   { opacity: 1; transform: scale(1);    }
    }

    /* ===================== APPLY ANIMATIONS ===================== */

    /* Gradient header — animated shimmer text */
    .gradient-header {
        background: linear-gradient(90deg, #10B981, #3B82F6, #10B981, #F59E0B, #10B981);
        background-size: 300% auto;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        animation: shimmer 4s linear infinite;
    }

    /* Subtitle fades up */
    .gradient-subtitle {
        animation: fadeInUp 0.7s ease both;
        animation-delay: 0.2s;
    }

    /* Header line slides in */
    .header-line {
        animation: slideInLeft 0.8s ease both;
        animation-delay: 0.3s;
    }

    /* Glass cards: fade up on load, with stagger via nth-child */
    .glass-card {
        animation: fadeInUp 0.6s ease both;
    }
    .glass-card:hover {
        transform: translateY(-4px) scale(1.01);
        box-shadow: 0 12px 30px rgba(16, 185, 129, 0.2);
        transition: all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
    }

    /* Metric cards: scale pop-in */
    div[data-testid="stMetric"] {
        animation: scaleIn 0.5s cubic-bezier(0.34, 1.56, 0.64, 1) both;
    }
    div[data-testid="stMetric"]:nth-child(1) { animation-delay: 0.0s; }
    div[data-testid="stMetric"]:nth-child(2) { animation-delay: 0.15s; }
    div[data-testid="stMetric"]:nth-child(3) { animation-delay: 0.3s; }
    div[data-testid="stMetric"]:hover {
        transform: translateY(-3px) scale(1.03);
        border-color: var(--primary-color, #10B981) !important;
        box-shadow: 0 8px 20px rgba(16, 185, 129, 0.2) !important;
        transition: all 0.25s ease;
    }

    /* Highlight banner: pulse glow + fade up */
    .highlight-banner {
        animation: fadeInUp 0.7s ease both, pulseGlow 3s ease-in-out infinite;
        animation-delay: 0.1s, 1s;
    }

    /* Plain-explain callout: slide in from left */
    .plain-explain {
        animation: slideInLeft 0.5s ease both;
        animation-delay: 0.15s;
    }

    /* Fun-fact box: slide in from right */
    .fun-fact-box {
        animation: slideInRight 0.5s ease both;
        animation-delay: 0.2s;
    }

    /* Phase bar fills: grow from 0 */
    .phase-bar-fill {
        animation: growWidth 1.2s cubic-bezier(0.22, 1, 0.36, 1) both;
        animation-delay: 0.3s;
    }

    /* Plotly chart containers: fade up */
    [data-testid="stPlotlyChart"] {
        animation: fadeInUp 0.65s ease both;
    }

    /* Dataframe: fade in */
    [data-testid="stDataFrame"] {
        animation: fadeInUp 0.5s ease both;
    }

    /* Tab content area: smooth cross-fade */
    [data-testid="stTabsContent"] > div {
        animation: fadeInUp 0.45s ease both;
    }

    /* Tab buttons: smooth color/scale on hover */
    .stTabs [data-baseweb="tab"] {
        transition: color 0.2s ease, transform 0.2s ease;
    }
    .stTabs [data-baseweb="tab"]:hover {
        transform: translateY(-2px);
    }

    /* Sidebar items fade in */
    [data-testid="stSidebar"] .stMarkdown,
    [data-testid="stSidebar"] .stSelectbox,
    [data-testid="stSidebar"] .stSlider {
        animation: fadeInUp 0.5s ease both;
    }

    /* Selectboxes: smooth border on focus */
    div[data-baseweb="select"] > div {
        transition: border-color 0.25s ease, box-shadow 0.25s ease !important;
    }
    div[data-baseweb="select"] > div:hover {
        border-color: #10B981 !important;
        box-shadow: 0 0 0 2px rgba(16, 185, 129, 0.15) !important;
    }

    /* Subheader sections: slide in */
    h2, h3 {
        animation: slideInLeft 0.5s ease both;
    }

</style>
""", unsafe_allow_html=True)

# Helper: check for local Parquet/CSV
def find_data_path():
    import os
    candidate_paths = [
        os.path.join(os.getcwd(), "data", "ipl_data.parquet"),
        os.path.join(os.getcwd(), "ipl_data.parquet"),
        '/mount/src/cricket_ipl26/data/ipl_data.parquet',
        os.path.join(os.getcwd(), "data", "ipl_data.csv"),
        os.path.join(os.getcwd(), "ipl_data.csv"),
        '/mount/src/cricket_ipl26/data/ipl_data.csv',
    ]
    for path in candidate_paths:
        if os.path.exists(path):
            return path
    return None

@st.cache_data
def load_data(_data_source):
    if isinstance(_data_source, str) and _data_source.endswith('.parquet'):
        df = pd.read_parquet(_data_source)
    elif isinstance(_data_source, str):
        df = pd.read_csv(_data_source, low_memory=False)
    else:
        # BytesIO
        try:
            df = pd.read_parquet(_data_source)
        except:
            _data_source.seek(0)
            df = pd.read_csv(_data_source, low_memory=False)

    # Clean season column
    def clean_season(x):
        x = str(x).strip()
        if '/' in x: return int(x[:4])
        try: return int(float(x))
        except: return x

    df['season_clean'] = df['season'].apply(clean_season)

    def get_season_display(year):
        if year == 2007: return "2008"
        return str(year)

    df['season_display'] = df['season_clean'].apply(get_season_display)

    def get_phase(over):
        if over <= 5: return 'Powerplay'
        elif over <= 14: return 'Middle Overs'
        else: return 'Death Overs'

    df['phase'] = df['over'].apply(get_phase)
    return df

@st.cache_data(show_spinner=False)
def fetch_dataset():
    import io, urllib.request

    local = find_data_path()
    if local:
        return load_data(local)

    URLS = [
        "https://raw.githubusercontent.com/patelpushpraj35-cell/cricket_ipl26/main/data/ipl_data.parquet",
        "https://raw.githubusercontent.com/ritesh-ojha/IPL-Dataset/main/deliveries.csv"
    ]
    for url in URLS:
        try:
            with urllib.request.urlopen(url, timeout=30) as resp:
                raw = resp.read()
            return load_data(io.BytesIO(raw))
        except Exception as e:
            continue
    return None

# ── Auto-load dataset (no upload needed) ─────────────────────────────────────
_ph = st.empty()
with _ph.container():
    st.info("\u23f3 Loading IPL dataset\u2026 first load takes a few seconds.")
df_raw = fetch_dataset()
_ph.empty()

if df_raw is None:
    st.error("\u274c Could not load the IPL dataset automatically.")
    st.markdown("""
**To fix this**, add the dataset to the repository:
1. Download the IPL ball-by-ball CSV from Kaggle / Cricsheet.
2. Rename it to `ipl_data.csv` and place in the `data/` folder.
3. Commit & push: `git add data/ipl_data.csv && git commit -m 'Add dataset' && git push`
""")
    st.stop()

if df_raw is not None:
    # Sidebar navigation & filters
    st.sidebar.markdown("""
    <div style="text-align:center; padding: 18px 0 12px 0;">
        <div style="font-size:3rem; line-height:1;">🏏</div>
        <div style="font-weight:800; font-size:1.15rem; color:#10B981; letter-spacing:1px; margin-top:4px;">IPL Crunch '26</div>
        <div style="font-size:0.72rem; color:#6B7280; margin-top:2px; letter-spacing:0.5px;">ANALYTICS DASHBOARD</div>
    </div>
    """, unsafe_allow_html=True)
    st.sidebar.markdown("---")
    
    # Theme Selection
    st.sidebar.subheader("🎨 Theme Customization")
    theme_choice = st.sidebar.selectbox("🎨 Select Display Theme", ["Dark Mode", "Light Mode"], index=0)
    
    if theme_choice == "Dark Mode":
        theme_css = """
        <style>
            :root {
                --text-color: #FFFFFF;
                --background-color: #0E1117;
                --secondary-background-color: #1F2937;
                --primary-color: #10B981;
                --glass-bg: rgba(255, 255, 255, 0.03);
                --glass-border: rgba(255, 255, 255, 0.1);
                --glass-shadow: rgba(0, 0, 0, 0.2);
            }
            html, body, [data-testid="stAppViewContainer"], [data-testid="stSidebar"], [data-testid="stHeader"] {
                background-color: #0E1117 !important;
                color: #FFFFFF !important;
            }
            .stTabs [data-baseweb="tab"] {
                color: #FFFFFF !important;
            }
            /* Selectbox widget style */
            div[data-baseweb="select"] > div {
                color: #FFFFFF !important;
                background-color: #1F2937 !important;
            }
            div[role="listbox"] {
                background-color: #1F2937 !important;
            }
        </style>
        """
        st.markdown(theme_css, unsafe_allow_html=True)
        plotly_template = "plotly_dark"
        plotly_font_color = "#FFFFFF"
    else:
        theme_css = """
        <style>
            :root {
                --text-color: #111827;
                --background-color: #F9FAFB;
                --secondary-background-color: #FFFFFF;
                --primary-color: #10B981;
                --glass-bg: rgba(255, 255, 255, 0.6);
                --glass-border: rgba(0, 0, 0, 0.08);
                --glass-shadow: rgba(0, 0, 0, 0.05);
            }
            html, body, [data-testid="stAppViewContainer"], [data-testid="stSidebar"], [data-testid="stHeader"] {
                background-color: #F9FAFB !important;
                color: #111827 !important;
            }
            .stTabs [data-baseweb="tab"] {
                color: #111827 !important;
            }
            /* Selectbox widget style */
            div[data-baseweb="select"] > div {
                color: #111827 !important;
                background-color: #FFFFFF !important;
            }
            div[role="listbox"] {
                background-color: #FFFFFF !important;
            }
        </style>
        """
        st.markdown(theme_css, unsafe_allow_html=True)
        plotly_template = "simple_white"
        plotly_font_color = "#1E293B"
    
    # Season Multi-Select or Range Slider
    available_seasons = sorted(df_raw['season_clean'].unique())
    season_labels = [str(s) if s != 2007 else "2008" for s in available_seasons]
    
    st.sidebar.subheader("📅 Filters")
    
    # Slider for season selection
    # Map season index (1-18) to actual values
    season_idx = st.sidebar.slider(
        "📅 Select Season Range",
        min_value=1,
        max_value=len(available_seasons),
        value=(1, len(available_seasons)), # Default range from season 1 to 18 (2008 to 2026)
        format="%d"
    )
    
    selected_season_vals = [available_seasons[i - 1] for i in range(season_idx[0], season_idx[1] + 1)]
    start_disp = "2008" if selected_season_vals[0] == 2007 else str(selected_season_vals[0])
    end_disp = "2008" if selected_season_vals[-1] == 2007 else str(selected_season_vals[-1])
    st.sidebar.markdown(f"Selected: **{start_disp} to {end_disp}**")

    # Developer credit at sidebar bottom
    st.sidebar.markdown("---")
    st.sidebar.markdown("""
    <div style="text-align:center; padding: 10px 0 4px 0;">
        <p style="color: var(--text-color); opacity:0.5; font-size:0.72rem; margin:0 0 6px 0; letter-spacing:0.5px; text-transform:uppercase;">Developed by</p>
        <a href="https://www.linkedin.com/in/pushpraj-patel-16a2843b4/" target="_blank" style="text-decoration:none;">
            <div style="display:inline-flex; align-items:center; gap:8px; background:linear-gradient(135deg,rgba(16,185,129,0.12),rgba(59,130,246,0.12)); border:1px solid rgba(16,185,129,0.3); border-radius:30px; padding:8px 16px; transition:all 0.3s ease;">
                <span style="font-size:1.1rem;">👨‍💻</span>
                <span style="color:#10B981; font-weight:700; font-size:0.92rem;">Pushpraj Patel</span>
                <span style="font-size:0.75rem;">🔗</span>
            </div>
        </a>
        <p style="color: var(--text-color); opacity:0.4; font-size:0.68rem; margin:8px 0 0 0;">🏏 IPL Crunch &rsquo;26 Analytics</p>
        <a href="https://github.com/patelpushpraj35-cell/cricket_ipl26" target="_blank"
           style="color:rgba(128,128,128,0.6); font-size:0.7rem; text-decoration:none;">
           ⭐ GitHub Repo
        </a>
    </div>
    """, unsafe_allow_html=True)

    # Filter the dataset
    df_filtered = df_raw[df_raw['season_clean'].isin(selected_season_vals)]
    
    # Match level dataframe for toss analysis
    matches_filtered = df_filtered.drop_duplicates('match_id').copy()
    matches_filtered = matches_filtered[matches_filtered['winner'].notna() & (~matches_filtered['winner'].isin(['No Result', 'tie', 'abandoned']))]
    
    # Main content header
    st.markdown(f"""
    <div class="hero-banner">
        <span style="font-size:2rem;">🏏</span>
        <div class="hero-overlay">
            <div class="hero-badge">🏏 IPL CRUNCH · DATA ANALYTICS</div>
            <h1>IPL Crunch Analytics Dashboard</h1>
            <p>Crunching {len(df_filtered):,} ball-by-ball records · Seasons {start_disp} – {end_disp}</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('<div class="header-line"></div>', unsafe_allow_html=True)
    
    # Key Metrics Bar
    col1, col2, col3 = st.columns(3)
    
    total_m = len(matches_filtered)
    # Calculate toss win match win rate
    toss_win_match_win = matches_filtered[matches_filtered['toss_winner'] == matches_filtered['winner']]
    toss_win_pct = (len(toss_win_match_win) / total_m) * 100 if total_m > 0 else 0
    
    # Find most critical phase (by highest correlation)
    # Calculate correlation for filtered data
    valid_ids = matches_filtered['match_id'].unique()
    df_valid_filtered = df_filtered[df_filtered['match_id'].isin(valid_ids)]
    
    team_phase_runs = df_valid_filtered.groupby(['match_id', 'batting_team', 'phase'])['runs_total'].sum().reset_index()
    team_phase_runs = team_phase_runs.merge(matches_filtered[['match_id', 'winner', 'team1', 'team2']], on='match_id')
    
    t1_runs = team_phase_runs[team_phase_runs['batting_team'] == team_phase_runs['team1']]
    t2_runs = team_phase_runs[team_phase_runs['batting_team'] == team_phase_runs['team2']]
    
    merged_runs = pd.merge(
        t1_runs[['match_id', 'phase', 'runs_total', 'winner', 'team1', 'team2']],
        t2_runs[['match_id', 'phase', 'runs_total']],
        on=['match_id', 'phase'],
        suffixes=('_team1', '_team2')
    )
    
    def get_winner_of_phase(row):
        if row['runs_total_team1'] > row['runs_total_team2']: return row['team1']
        elif row['runs_total_team2'] > row['runs_total_team1']: return row['team2']
        return 'Tie'
        
    merged_runs['phase_winner'] = merged_runs.apply(get_winner_of_phase, axis=1)
    merged_runs['phase_winner_won_match'] = merged_runs['phase_winner'] == merged_runs['winner']
    
    phase_corrs = {}
    for phase in ['Powerplay', 'Middle Overs', 'Death Overs']:
        phase_data = merged_runs[(merged_runs['phase'] == phase) & (merged_runs['phase_winner'] != 'Tie')]
        if len(phase_data) > 0:
            phase_corrs[phase] = (phase_data['phase_winner_won_match'].sum() / len(phase_data)) * 100
        else:
            phase_corrs[phase] = 0
            
    best_phase = max(phase_corrs, key=phase_corrs.get) if phase_corrs else "N/A"
    best_phase_pct = phase_corrs[best_phase] if phase_corrs else 0
    
    with col1:
        st.metric(label="📊 Matches in Dataset", value=f"{total_m:,}", help="Unique completed matches (ties & abandoned games excluded)")
    with col2:
        st.metric(label="🪙 Does Toss = Win?", value=f"{toss_win_pct:.1f}%", help="% of matches where the toss-winning team also won the match. Near 50% = coin flip!")
    with col3:
        st.metric(label="⚡ Most Match-Deciding Phase", value=f"{best_phase}", delta=f"{best_phase_pct:.1f}% win correlation", help="The phase where scoring more runs than opponents most often leads to winning the match")
        
    # Main Tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "🪙 Q1: Toss Advantage", 
        "📈 Q2: Decisive Phase", 
        "🏆 Q3: Player Leaderboards", 
        "💡 Q4: Surprise Insights"
    ])
    
    with tab1:
        st.subheader("🪙 Q1: Does Winning the Toss Actually Help You Win the Match?")
        st.markdown('<div class="plain-explain">💡 <b>What we\'re checking:</b> In IPL, the team that wins the toss gets to choose whether to bat or field first. The big question — does that coin flip at the start give them a real advantage, or is it mostly luck after that?</div>', unsafe_allow_html=True)
        
        # Calculate toss decisions impact
        toss_field = matches_filtered[matches_filtered['toss_decision'] == 'field']
        toss_field_win = toss_field[toss_field['winner'] == toss_field['toss_winner']]
        toss_field_pct = (len(toss_field_win) / len(toss_field)) * 100 if len(toss_field) > 0 else 0
        
        toss_bat = matches_filtered[matches_filtered['toss_decision'] == 'bat']
        toss_bat_win = toss_bat[toss_bat['winner'] == toss_bat['toss_winner']]
        toss_bat_pct = (len(toss_bat_win) / len(toss_bat)) * 100 if len(toss_bat) > 0 else 0
        
        # Row for Toss Win Rate and Answer
        col_chart1, col_answer1 = st.columns([3, 2])
        
        with col_chart1:
            st.markdown('#### Chart 1: Win Rate of Toss Winners vs Toss Losers')
            
            toss_df = pd.DataFrame({
                'Toss Outcome': ['Toss Winner Wins Match', 'Toss Loser Wins Match'],
                'Percentage': [toss_win_pct, 100 - toss_win_pct]
            })
            
            fig1 = px.bar(
                toss_df,
                x='Toss Outcome',
                y='Percentage',
                color='Toss Outcome',
                color_discrete_map={
                    'Toss Winner Wins Match': '#10B981', # Emerald
                    'Toss Loser Wins Match': '#F59E0B' # Amber
                },
                text=toss_df['Percentage'].apply(lambda x: f'{x:.2f}%'),
                height=400,
                template=plotly_template
            )
            
            fig1.update_traces(textposition='outside', textfont=dict(size=12, color=plotly_font_color))
            fig1.update_layout(
                font=dict(color=plotly_font_color),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                showlegend=False,
                xaxis_title=None,
                yaxis_title='Match Win Rate (%)',
                yaxis_range=[0, 100],
                margin=dict(t=20, b=20, l=10, r=10)
            )
            fig1.update_xaxes(title_font=dict(color=plotly_font_color), tickfont=dict(color=plotly_font_color))
            fig1.update_yaxes(title_font=dict(color=plotly_font_color), tickfont=dict(color=plotly_font_color))
            
            st.plotly_chart(fig1, use_container_width=True)
            
            st.markdown('#### 📊 Chart 1B: Match Win Rate by Toss Decision (Bat vs Field)')
            decision_df = pd.DataFrame({
                'Toss Decision': ['Choose Field First', 'Choose Bat First'],
                'Win Rate (%)': [toss_field_pct, toss_bat_pct]
            })
            
            fig1b = px.bar(
                decision_df,
                x='Toss Decision',
                y='Win Rate (%)',
                color='Toss Decision',
                color_discrete_map={
                    'Choose Field First': '#3B82F6', # Blue
                    'Choose Bat First': '#EC4899' # Pink
                },
                text=decision_df['Win Rate (%)'].apply(lambda x: f'{x:.2f}%'),
                height=300,
                template=plotly_template
            )
            
            fig1b.update_traces(textposition='outside', textfont=dict(size=12, color=plotly_font_color))
            fig1b.update_layout(
                font=dict(color=plotly_font_color),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                showlegend=False,
                xaxis_title=None,
                yaxis_title='Win Rate (%)',
                yaxis_range=[0, 100],
                margin=dict(t=20, b=20, l=10, r=10)
            )
            fig1b.update_xaxes(title_font=dict(color=plotly_font_color), tickfont=dict(color=plotly_font_color))
            fig1b.update_yaxes(title_font=dict(color=plotly_font_color), tickfont=dict(color=plotly_font_color))
            
            st.plotly_chart(fig1b, use_container_width=True)

            st.markdown('#### 📈 Chart 1C: Toss Win Rate Trend — Season by Season')
            toss_season_rows = []
            for sv in available_seasons:
                m_s = df_raw[df_raw['season_clean'] == sv].drop_duplicates('match_id').copy()
                m_s = m_s[m_s['winner'].notna() & (~m_s['winner'].isin(['No Result', 'tie', 'abandoned']))]
                if len(m_s) == 0:
                    continue
                tw = m_s[m_s['toss_winner'] == m_s['winner']]
                disp = '2008' if sv == 2007 else str(sv)
                toss_season_rows.append({'Season': disp, 'Toss Win Rate (%)': (len(tw) / len(m_s)) * 100})
            toss_trend_df = pd.DataFrame(toss_season_rows)
            fig1c = go.Figure()
            fig1c.add_trace(go.Scatter(
                x=toss_trend_df['Season'],
                y=toss_trend_df['Toss Win Rate (%)'],
                mode='lines+markers+text',
                text=toss_trend_df['Toss Win Rate (%)'].apply(lambda v: f'{v:.0f}%'),
                textposition='top center',
                textfont=dict(size=10, color=plotly_font_color),
                line=dict(color='#10B981', width=3),
                marker=dict(size=9, color='#10B981', symbol='circle'),
                fill='tozeroy',
                fillcolor='rgba(16,185,129,0.08)'
            ))
            fig1c.add_hline(y=50, line_dash='dash', line_color='#F59E0B',
                            annotation_text='🪙 50% coin-flip line',
                            annotation_font_color='#F59E0B',
                            annotation_position='bottom right')
            fig1c.update_layout(
                font=dict(color=plotly_font_color),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                xaxis_title='Season',
                yaxis_title='Toss Win Rate (%)',
                yaxis_range=[30, 70],
                height=280,
                margin=dict(t=20, b=20, l=10, r=10),
                template=plotly_template
            )
            fig1c.update_xaxes(tickfont=dict(color=plotly_font_color), title_font=dict(color=plotly_font_color))
            fig1c.update_yaxes(tickfont=dict(color=plotly_font_color), title_font=dict(color=plotly_font_color))
            st.plotly_chart(fig1c, use_container_width=True)

        with col_answer1:
            st.markdown(f"""
            <div class="glass-card" style="height: 480px; overflow-y: auto;">
                                <div class="card-title">🎯 The Short Answer</div>
                <div class="card-body">
                <b>❌ No — winning the toss barely helps!</b><br><br>
                Out of all matches from {start_disp}–{end_disp}, toss winners won
                the match only <b>{toss_win_pct:.1f}%</b> of the time — nearly
                identical to the <b>{100-toss_win_pct:.1f}%</b> won by toss <i>losers</i>.
                That’s basically a coin flip! 🪙<br><br>
                <b>🏟️ Does the choice (Bat vs Field) matter?</b><br>
                ✅ <b>Field First:</b> Won <b>{toss_field_pct:.1f}%</b> of matches
                ({len(toss_field_win)} wins / {len(toss_field)} times)<br><br>
                🏏 <b>Bat First:</b> Won <b>{toss_bat_pct:.1f}%</b> of matches
                ({len(toss_bat_win)} wins / {len(toss_bat)} times)<br><br>
                <b>🧠 Plain-English Takeaway:</b><br>
                Fielding first is <i>slightly</i> smarter — likely because evening dew
                makes chasing easier. But the real game is won on the pitch, not at the toss!
                </div>
            </div>
            """, unsafe_allow_html=True)
            
    with tab2:
        st.subheader("📈 Q2: Which 'Chapter' of the Match Decides the Winner?")
        st.markdown('<div class="plain-explain">💡 <b>Think of a T20 match in 3 chapters:</b> The <b>Powerplay</b> (overs 1–6, fielding restrictions make runs easy), <b>Middle Overs</b> (overs 7–14, bowlers take control), and <b>Death Overs</b> (overs 15–20, big sixes &amp; drama). Which chapter is most critical to the final result?</div>', unsafe_allow_html=True)
        
        # Calculate runs per phase
        phase_runs_grouped = df_valid_filtered.groupby(['match_id', 'batting_team', 'phase'])['runs_total'].sum().reset_index()
        phase_runs_grouped = phase_runs_grouped.merge(matches_filtered[['match_id', 'winner']], on='match_id')
        phase_runs_grouped['is_winner'] = phase_runs_grouped['batting_team'] == phase_runs_grouped['winner']
        
        avg_phase_df = phase_runs_grouped.groupby(['phase', 'is_winner'])['runs_total'].mean().reset_index()
        avg_phase_df['Team Outcome'] = avg_phase_df['is_winner'].map({True: 'Winning Teams', False: 'Losing Teams'})
        
        phase_order = ['Powerplay', 'Middle Overs', 'Death Overs']
        avg_phase_df['phase'] = pd.Categorical(avg_phase_df['phase'], categories=phase_order, ordered=True)
        avg_phase_df = avg_phase_df.sort_values('phase')
        
        # Calculate wickets lost per phase (Parameter: Wickets Lost)
        df_valid_filtered_w = df_valid_filtered.copy()
        df_valid_filtered_w['is_wicket'] = df_valid_filtered_w['wicket_player_out'].notna().astype(int)
        phase_wickets_grouped = df_valid_filtered_w.groupby(['match_id', 'batting_team', 'phase'])['is_wicket'].sum().reset_index()
        phase_wickets_grouped = phase_wickets_grouped.merge(matches_filtered[['match_id', 'winner']], on='match_id')
        phase_wickets_grouped['is_winner'] = phase_wickets_grouped['batting_team'] == phase_wickets_grouped['winner']
        
        avg_phase_wickets = phase_wickets_grouped.groupby(['phase', 'is_winner'])['is_wicket'].mean().reset_index()
        avg_phase_wickets['Team Outcome'] = avg_phase_wickets['is_winner'].map({True: 'Winning Teams', False: 'Losing Teams'})
        avg_phase_wickets['phase'] = pd.Categorical(avg_phase_wickets['phase'], categories=phase_order, ordered=True)
        avg_phase_wickets = avg_phase_wickets.sort_values('phase')
        
        def get_avg_w(p, is_w):
            arr = avg_phase_wickets[(avg_phase_wickets['phase'] == p) & (avg_phase_wickets['is_winner'] == is_w)]['is_wicket'].values
            return arr[0] if len(arr) > 0 else 0.0
            
        pp_w_win = get_avg_w('Powerplay', True)
        pp_w_loss = get_avg_w('Powerplay', False)
        mid_w_win = get_avg_w('Middle Overs', True)
        mid_w_loss = get_avg_w('Middle Overs', False)
        death_w_win = get_avg_w('Death Overs', True)
        death_w_loss = get_avg_w('Death Overs', False)
        
        # Row for Phase Analysis Charts and Answer
        col_chart2, col_answer2 = st.columns([3, 2])
        
        with col_chart2:
            st.markdown('#### Chart 2: Average Runs per Phase (Winning vs Losing Teams)')
            fig2 = px.bar(
                avg_phase_df,
                x='phase',
                y='runs_total',
                color='Team Outcome',
                barmode='group',
                color_discrete_map={
                    'Winning Teams': '#00CC96', # Teal
                    'Losing Teams': '#FF3366' # Neon Pink
                },
                text=avg_phase_df['runs_total'].apply(lambda x: f'{x:.2f}'),
                height=300,
                template=plotly_template
            )
            
            fig2.update_traces(textposition='outside', textfont=dict(size=11, color=plotly_font_color))
            fig2.update_layout(
                font=dict(color=plotly_font_color),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                xaxis_title='Match Phase',
                yaxis_title='Average Runs Scored',
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=1.02,
                    xanchor="right",
                    x=1,
                    font=dict(color=plotly_font_color)
                ),
                margin=dict(t=20, b=20, l=10, r=10)
            )
            fig2.update_xaxes(title_font=dict(color=plotly_font_color), tickfont=dict(color=plotly_font_color))
            fig2.update_yaxes(title_font=dict(color=plotly_font_color), tickfont=dict(color=plotly_font_color))
            st.plotly_chart(fig2, use_container_width=True)
            
            st.markdown('#### 📊 Chart 2B: Average Wickets Lost per Phase (Winning vs Losing Teams)')
            fig2b = px.bar(
                avg_phase_wickets,
                x='phase',
                y='is_wicket',
                color='Team Outcome',
                barmode='group',
                color_discrete_map={
                    'Winning Teams': '#10B981', # Green
                    'Losing Teams': '#EF4444' # Red
                },
                text=avg_phase_wickets['is_wicket'].apply(lambda x: f'{x:.2f}'),
                height=300,
                template=plotly_template
            )
            
            fig2b.update_traces(textposition='outside', textfont=dict(size=11, color=plotly_font_color))
            fig2b.update_layout(
                font=dict(color=plotly_font_color),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                xaxis_title='Match Phase',
                yaxis_title='Average Wickets Lost',
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=1.02,
                    xanchor="right",
                    x=1,
                    font=dict(color=plotly_font_color)
                ),
                margin=dict(t=20, b=20, l=10, r=10)
            )
            fig2b.update_xaxes(title_font=dict(color=plotly_font_color), tickfont=dict(color=plotly_font_color))
            fig2b.update_yaxes(title_font=dict(color=plotly_font_color), tickfont=dict(color=plotly_font_color))
            st.plotly_chart(fig2b, use_container_width=True)

            st.markdown('#### ⚡ Chart 2C: Average Run-Rate by Over Number (0–19)')
            over_rr = df_valid_filtered.groupby('over')['runs_total'].mean().reset_index()
            over_rr.columns = ['Over', 'Avg Runs/Ball']
            over_rr['Avg Run-Rate'] = over_rr['Avg Runs/Ball'] * 6
            over_rr['Phase'] = over_rr['Over'].apply(
                lambda o: 'Powerplay' if o <= 5 else ('Middle Overs' if o <= 14 else 'Death Overs'))
            phase_color_map = {'Powerplay': '#3B82F6', 'Middle Overs': '#10B981', 'Death Overs': '#F59E0B'}
            fig2c = go.Figure()
            for phase_name, phase_color in phase_color_map.items():
                phase_data = over_rr[over_rr['Phase'] == phase_name]
                fig2c.add_trace(go.Bar(
                    x=phase_data['Over'] + 1,
                    y=phase_data['Avg Run-Rate'],
                    name=phase_name,
                    marker_color=phase_color,
                    text=phase_data['Avg Run-Rate'].apply(lambda v: f'{v:.1f}'),
                    textposition='outside',
                    textfont=dict(size=9, color=plotly_font_color)
                ))
            fig2c.update_layout(
                font=dict(color=plotly_font_color),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                xaxis_title='Over Number',
                yaxis_title='Avg Run-Rate (RPO)',
                barmode='stack',
                legend=dict(orientation='h', y=1.1, font=dict(color=plotly_font_color)),
                height=280,
                margin=dict(t=30, b=20, l=10, r=10),
                template=plotly_template
            )
            fig2c.update_xaxes(tickfont=dict(color=plotly_font_color), title_font=dict(color=plotly_font_color),
                                tickvals=list(range(1, 21)))
            fig2c.update_yaxes(tickfont=dict(color=plotly_font_color), title_font=dict(color=plotly_font_color))
            st.plotly_chart(fig2c, use_container_width=True)

        with col_answer2:
            # Get phase runs details dynamically
            pp_win = avg_phase_df[(avg_phase_df['phase'] == 'Powerplay') & (avg_phase_df['is_winner'] == True)]['runs_total'].values[0]
            pp_loss = avg_phase_df[(avg_phase_df['phase'] == 'Powerplay') & (avg_phase_df['is_winner'] == False)]['runs_total'].values[0]
            mid_win = avg_phase_df[(avg_phase_df['phase'] == 'Middle Overs') & (avg_phase_df['is_winner'] == True)]['runs_total'].values[0]
            mid_loss = avg_phase_df[(avg_phase_df['phase'] == 'Middle Overs') & (avg_phase_df['is_winner'] == False)]['runs_total'].values[0]
            death_win = avg_phase_df[(avg_phase_df['phase'] == 'Death Overs') & (avg_phase_df['is_winner'] == True)]['runs_total'].values[0]
            death_loss = avg_phase_df[(avg_phase_df['phase'] == 'Death Overs') & (avg_phase_df['is_winner'] == False)]['runs_total'].values[0]
            pp_pct    = phase_corrs.get('Powerplay', 0)
            mid_pct   = phase_corrs.get('Middle Overs', 0)
            death_pct = phase_corrs.get('Death Overs', 0)
            st.markdown(f"""
            <div class="glass-card" style="height: 520px; overflow-y: auto;">
                                <div class="card-title">🎯 Which Chapter Decides the Match?</div>
                <div class="card-body">
                <b>📊 If a team wins a phase, how often do they win the match?</b><br><br>
                <div class="phase-bar-wrap">
                    <div class="phase-bar-label">🟢 Middle Overs (Overs 7–14)</div>
                    <div class="phase-bar-track"><div class="phase-bar-fill" style="width:{mid_pct:.0f}%;background:#10B981;"></div></div>
                    <div class="phase-bar-pct"><b>{mid_pct:.1f}%</b> of phase winners win the match</div>
                </div>
                <div class="phase-bar-wrap">
                    <div class="phase-bar-label">🔵 Powerplay (Overs 1–6)</div>
                    <div class="phase-bar-track"><div class="phase-bar-fill" style="width:{pp_pct:.0f}%;background:#3B82F6;"></div></div>
                    <div class="phase-bar-pct"><b>{pp_pct:.1f}%</b> of phase winners win the match</div>
                </div>
                <div class="phase-bar-wrap">
                    <div class="phase-bar-label">🟡 Death Overs (Overs 15–20)</div>
                    <div class="phase-bar-track"><div class="phase-bar-fill" style="width:{death_pct:.0f}%;background:#F59E0B;"></div></div>
                    <div class="phase-bar-pct"><b>{death_pct:.1f}%</b> of phase winners win the match</div>
                </div>
                <br><b>📈 Runs gap — Winners vs Losers:</b><br>
                🟢 Middle: +{mid_win-mid_loss:.1f} runs &nbsp;|&nbsp; 🔵 Powerplay: +{pp_win-pp_loss:.1f} runs &nbsp;|&nbsp; 🟡 Death: +{death_win-death_loss:.1f} runs<br><br>
                <b>🧠 Plain-English Takeaway:</b><br>
                The quiet middle overs matter most! Teams that outscore in overs 7–14
                win <b>{mid_pct:.0f}%</b> of the time. The exciting death overs?
                Only <b>{death_pct:.0f}%</b> — barely a coin flip.
                </div>
            </div>
            """, unsafe_allow_html=True)
            
    with tab3:
        st.subheader("🏆 Q3: Who Are the Greatest IPL Players of All Time?")
        st.markdown('<div class="plain-explain">💡 <b>How to use this tab:</b> Use the dropdowns below to rank batters and bowlers by different skills. <b>Total Runs</b> = who scored the most overall. <b>Strike Rate</b> = who scored the fastest. <b>Economy Rate</b> = which bowler was hardest to hit. Pick your favourite metric and see where your favourite player ranks!</div>', unsafe_allow_html=True)
        
        # Parameter Columns for dynamic sorting
        col_param1, col_param2 = st.columns(2)
        with col_param1:
            sort_batter_by = st.selectbox(
                "Sort Batters By",
                options=["Total Runs", "Strike Rate (min 2,000 runs)", "Batting Average (min 2,000 runs)"]
            )
        with col_param2:
            sort_bowler_by = st.selectbox(
                "Sort Bowlers By",
                options=["Wickets", "Economy Rate (min 500 balls)", "Bowling Average (min 80 wickets)"]
            )
            
        # Calculations for top batters and bowlers
        # Top Batters
        top_batters_calc = df_filtered.groupby('batter')['runs_batter'].sum().reset_index()
        balls_faced = df_filtered.groupby('batter')['ball'].count().reset_index().rename(columns={'ball': 'balls'})
        outs = df_filtered[df_filtered['wicket_player_out'].notna()].groupby('wicket_player_out')['match_id'].count().reset_index().rename(columns={'wicket_player_out': 'batter', 'match_id': 'outs'})
        
        batters_merged = top_batters_calc.merge(balls_faced, on='batter')
        batters_merged = batters_merged.merge(outs, on='batter', how='left').fillna(0)
        batters_merged['strike_rate'] = (batters_merged['runs_batter'] / batters_merged['balls']) * 100
        batters_merged['average'] = batters_merged.apply(lambda r: r['runs_batter'] / r['outs'] if r['outs'] > 0 else r['runs_batter'], axis=1)
        
        # Sort & Filter Batters dynamically
        if sort_batter_by == "Strike Rate (min 2,000 runs)":
            batters_filt = batters_merged[batters_merged['runs_batter'] >= 2000]
            top_batters_final = batters_filt.sort_values(by='strike_rate', ascending=False).head(10).reset_index(drop=True)
            y_col = 'Strike Rate'
        elif sort_batter_by == "Batting Average (min 2,000 runs)":
            batters_filt = batters_merged[batters_merged['runs_batter'] >= 2000]
            top_batters_final = batters_filt.sort_values(by='average', ascending=False).head(10).reset_index(drop=True)
            y_col = 'Batting Average'
        else:
            top_batters_final = batters_merged.sort_values(by='runs_batter', ascending=False).head(10).reset_index(drop=True)
            y_col = 'Total Runs'
            
        top_batters_final.index += 1
        top_batters_final.index.name = 'Rank'
        top_batters_final = top_batters_final.rename(columns={'batter': 'Batter Name', 'runs_batter': 'Total Runs', 'balls': 'Balls Faced', 'average': 'Batting Average', 'strike_rate': 'Strike Rate'})
        
        # Top Bowlers
        bowler_wickets_kinds = ['caught', 'bowled', 'lbw', 'caught and bowled', 'stumped', 'hit wicket']
        df_bowler_wickets = df_filtered[df_filtered['wicket_kind'].isin(bowler_wickets_kinds)]
        top_bowlers_calc = df_bowler_wickets.groupby('bowler')['wicket_player_out'].count().reset_index().rename(columns={'wicket_player_out': 'wickets'})
        bowler_runs = df_filtered.groupby('bowler')['runs_total'].sum().reset_index().rename(columns={'runs_total': 'runs_conceded'})
        
        legal_deliveries = df_filtered[
            ((df_filtered['extras_wides'].isna()) | (df_filtered['extras_wides'] == 0)) & 
            ((df_filtered['extras_noballs'].isna()) | (df_filtered['extras_noballs'] == 0))
        ]
        bowler_balls = legal_deliveries.groupby('bowler')['ball'].count().reset_index().rename(columns={'ball': 'legal_balls'})
        
        bowlers_merged = top_bowlers_calc.merge(bowler_runs, on='bowler')
        bowlers_merged = bowlers_merged.merge(bowler_balls, on='bowler')
        bowlers_merged['overs_bowled'] = bowlers_merged['legal_balls'] / 6
        bowlers_merged['economy'] = bowlers_merged['runs_conceded'] / bowlers_merged['overs_bowled']
        bowlers_merged['bowling_average'] = bowlers_merged.apply(lambda r: r['runs_conceded'] / r['wickets'] if r['wickets'] > 0 else r['runs_conceded'], axis=1)
        
        # Sort & Filter Bowlers dynamically
        if sort_bowler_by == "Economy Rate (min 500 balls)":
            bowlers_filt = bowlers_merged[bowlers_merged['legal_balls'] >= 500]
            top_bowlers_final = bowlers_filt.sort_values(by='economy', ascending=True).head(10).reset_index(drop=True)
            y_bowl_col = 'Economy'
        elif sort_bowler_by == "Bowling Average (min 80 wickets)":
            bowlers_filt = bowlers_merged[bowlers_merged['wickets'] >= 80]
            top_bowlers_final = bowlers_filt.sort_values(by='bowling_average', ascending=True).head(10).reset_index(drop=True)
            y_bowl_col = 'Bowling Average'
        else:
            top_bowlers_final = bowlers_merged.sort_values(by='wickets', ascending=False).head(10).reset_index(drop=True)
            y_bowl_col = 'Wickets'
            
        top_bowlers_final.index += 1
        top_bowlers_final.index.name = 'Rank'
        top_bowlers_final = top_bowlers_final.rename(columns={'bowler': 'Bowler Name', 'wickets': 'Wickets', 'runs_conceded': 'Runs Conceded', 'overs_bowled': 'Overs Bowled', 'economy': 'Economy', 'bowling_average': 'Bowling Average'})

        col_batters, col_bowlers = st.columns(2)
        
        with col_batters:
            st.markdown(f'#### 🏏 Top Batters (Sorted by {y_col})')
            # Display Table
            st.dataframe(
                top_batters_final[['Batter Name', 'Total Runs', 'Balls Faced', 'Batting Average', 'Strike Rate']].head(5).style.format({
                    'Total Runs': '{:,}',
                    'Balls Faced': '{:,}',
                    'Batting Average': '{:.2f}',
                    'Strike Rate': '{:.2f}%'
                }),
                use_container_width=True
            )
            
            # Bar chart for batters
            fig_bat = px.bar(
                top_batters_final.head(5),
                x=y_col,
                y='Batter Name',
                orientation='h',
                color=y_col,
                color_continuous_scale='Viridis',
                text=top_batters_final.head(5)[y_col].apply(lambda x: f'{x:.1f}%' if y_col == 'Strike Rate' else (f'{x:.2f}' if y_col == 'Batting Average' else f'{x}')),
                template=plotly_template
            )
            fig_bat.update_traces(textfont=dict(color=plotly_font_color))
            fig_bat.update_layout(
                font=dict(color=plotly_font_color),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                coloraxis_showscale=False,
                xaxis_title=y_col,
                yaxis_title=None,
                margin=dict(t=10, b=10, l=10, r=10),
                height=250
            )
            fig_bat.update_xaxes(title_font=dict(color=plotly_font_color), tickfont=dict(color=plotly_font_color))
            fig_bat.update_yaxes(title_font=dict(color=plotly_font_color), tickfont=dict(color=plotly_font_color))
            st.plotly_chart(fig_bat, use_container_width=True)
            
        with col_bowlers:
            st.markdown(f'#### 🔴 Top Bowlers (Sorted by {y_bowl_col})')
            # Display Table
            st.dataframe(
                top_bowlers_final[['Bowler Name', 'Wickets', 'Overs Bowled', 'Economy', 'Bowling Average']].head(5).style.format({
                    'Wickets': '{:,}',
                    'Overs Bowled': '{:.1f}',
                    'Economy': '{:.2f}',
                    'Bowling Average': '{:.2f}'
                }),
                use_container_width=True
            )
            
            # Bar chart for bowlers
            fig_bowl = px.bar(
                top_bowlers_final.head(5),
                x=y_bowl_col,
                y='Bowler Name',
                orientation='h',
                color=y_bowl_col,
                color_continuous_scale='Cividis',
                text=top_bowlers_final.head(5)[y_bowl_col].apply(lambda x: f'{x:.2f}'),
                template=plotly_template
            )
            fig_bowl.update_traces(textfont=dict(color=plotly_font_color))
            fig_bowl.update_layout(
                font=dict(color=plotly_font_color),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                coloraxis_showscale=False,
                xaxis_title=y_bowl_col,
                yaxis_title=None,
                margin=dict(t=10, b=10, l=10, r=10),
                height=250
            )
            fig_bowl.update_xaxes(title_font=dict(color=plotly_font_color), tickfont=dict(color=plotly_font_color))
            fig_bowl.update_yaxes(title_font=dict(color=plotly_font_color), tickfont=dict(color=plotly_font_color))
            st.plotly_chart(fig_bowl, use_container_width=True)

        st.markdown('---')
        st.markdown('#### 🧠 Batter Profile: Strike Rate vs Total Runs (Top 40 qualifiers — min 500 balls)')
        st.markdown('<div class="plain-explain">💡 <b>How to read this chart:</b> Each bubble = one batter. <b>Right = more runs scored.</b> <b>Up = faster scorer.</b> Bigger bubble = more balls faced. The best all-round batters sit in the <b>top-right corner</b>!</div>', unsafe_allow_html=True)
        scatter_bat = batters_merged[batters_merged['balls'] >= 500].sort_values('runs_batter', ascending=False).head(40)
        scatter_bat = scatter_bat.rename(columns={'batter': 'Batter', 'runs_batter': 'Total Runs', 'balls': 'Balls Faced', 'strike_rate': 'Strike Rate'})
        fig_scatter = px.scatter(
            scatter_bat,
            x='Total Runs',
            y='Strike Rate',
            size='Balls Faced',
            color='Strike Rate',
            color_continuous_scale='Viridis',
            text='Batter',
            hover_data={'Batter': True, 'Total Runs': True, 'Strike Rate': ':.1f', 'Balls Faced': True},
            height=450,
            template=plotly_template
        )
        fig_scatter.update_traces(
            textposition='top center',
            textfont=dict(size=9, color=plotly_font_color),
            marker=dict(opacity=0.85, line=dict(width=1, color='rgba(255,255,255,0.3)'))
        )
        fig_scatter.update_layout(
            font=dict(color=plotly_font_color),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            xaxis_title='📈 Total Runs Scored',
            yaxis_title='⚡ Strike Rate',
            coloraxis_showscale=False,
            margin=dict(t=20, b=20, l=10, r=10)
        )
        fig_scatter.update_xaxes(tickfont=dict(color=plotly_font_color), title_font=dict(color=plotly_font_color),
                                  showgrid=True, gridcolor='rgba(128,128,128,0.1)')
        fig_scatter.update_yaxes(tickfont=dict(color=plotly_font_color), title_font=dict(color=plotly_font_color),
                                  showgrid=True, gridcolor='rgba(128,128,128,0.1)')
        st.plotly_chart(fig_scatter, use_container_width=True)

        st.markdown('---')
        st.markdown('#### 🎯 Bowler Profile: Economy Rate vs Total Wickets (Top 40 qualifiers — min 300 legal balls)')
        st.markdown('<div class="plain-explain">💡 <b>How to read this chart:</b> Each bubble = one bowler. <b>Right = more wickets taken.</b> <b>Down = more economical (harder to score off).</b> Bigger bubble = more overs bowled. The best all-round bowlers sit in the <b>bottom-right corner</b>!</div>', unsafe_allow_html=True)
        bowler_wickets_kinds_sc = ['caught', 'bowled', 'lbw', 'caught and bowled', 'stumped', 'hit wicket']
        df_bwsc_wkts = df_filtered[df_filtered['wicket_kind'].isin(bowler_wickets_kinds_sc)]
        bwsc_wkts = df_bwsc_wkts.groupby('bowler')['wicket_player_out'].count().reset_index().rename(columns={'wicket_player_out': 'Wickets'})
        bwsc_runs = df_filtered.groupby('bowler')['runs_total'].sum().reset_index().rename(columns={'runs_total': 'Runs Conceded'})
        legal_sc = df_filtered[
            ((df_filtered['extras_wides'].isna()) | (df_filtered['extras_wides'] == 0)) &
            ((df_filtered['extras_noballs'].isna()) | (df_filtered['extras_noballs'] == 0))
        ]
        bwsc_balls = legal_sc.groupby('bowler')['ball'].count().reset_index().rename(columns={'ball': 'Legal Balls'})
        scatter_bowl = bwsc_wkts.merge(bwsc_runs, on='bowler').merge(bwsc_balls, on='bowler')
        scatter_bowl['Overs Bowled'] = scatter_bowl['Legal Balls'] / 6
        scatter_bowl['Economy Rate'] = scatter_bowl['Runs Conceded'] / scatter_bowl['Overs Bowled']
        scatter_bowl = scatter_bowl[scatter_bowl['Legal Balls'] >= 300].sort_values('Wickets', ascending=False).head(40)
        scatter_bowl = scatter_bowl.rename(columns={'bowler': 'Bowler'})
        fig_scatter_bowl = px.scatter(
            scatter_bowl,
            x='Wickets',
            y='Economy Rate',
            size='Overs Bowled',
            color='Economy Rate',
            color_continuous_scale='RdYlGn_r',
            text='Bowler',
            hover_data={'Bowler': True, 'Wickets': True, 'Economy Rate': ':.2f', 'Overs Bowled': ':.1f'},
            height=450,
            template=plotly_template
        )
        fig_scatter_bowl.update_traces(
            textposition='top center',
            textfont=dict(size=9, color=plotly_font_color),
            marker=dict(opacity=0.85, line=dict(width=1, color='rgba(255,255,255,0.3)'))
        )
        fig_scatter_bowl.update_layout(
            font=dict(color=plotly_font_color),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            xaxis_title='🎯 Total Wickets Taken',
            yaxis_title='💸 Economy Rate (lower = better)',
            yaxis_autorange='reversed',
            coloraxis_showscale=False,
            margin=dict(t=20, b=20, l=10, r=10)
        )
        fig_scatter_bowl.update_xaxes(tickfont=dict(color=plotly_font_color), title_font=dict(color=plotly_font_color),
                                       showgrid=True, gridcolor='rgba(128,128,128,0.1)')
        fig_scatter_bowl.update_yaxes(tickfont=dict(color=plotly_font_color), title_font=dict(color=plotly_font_color),
                                       showgrid=True, gridcolor='rgba(128,128,128,0.1)')
        st.plotly_chart(fig_scatter_bowl, use_container_width=True)

    with tab4:
        st.subheader("💡 Q4: The Surprising Finding + How We Did the Math")
        st.markdown('''
        <div class="stadium-strip">
            <span style="font-size:2rem;">🏏</span>
            <div class="stadium-strip-overlay">
                <span>🏟️ &nbsp; 280,000+ deliveries &nbsp;·&nbsp; 1,200+ matches &nbsp;·&nbsp; Every ball. Every over. Every season.</span>
            </div>
        </div>
        ''', unsafe_allow_html=True)
        
        # Surprise Banner
        st.markdown(f"""
        <div class="highlight-banner">
            <h4 style="color:#10B981; margin-top:0; margin-bottom: 8px;">😲 The Genuinely Surprising Finding:</h4>
            <p style="color: var(--text-color); font-size:1.05rem; margin:0; line-height: 1.5;">
                "Despite the intense drama, media focus, and high pressure associated with the <b>Death Overs (Overs 15-19)</b>, 
                outscoring your opponent in the death phase is only <b>{phase_corrs.get('Death Overs', 0):.2f}%</b> correlated with winning the match—barely better than a coin flip! 
                In contrast, dominating the <b>Middle Overs (Overs 6-14)</b> yields a massive <b>{phase_corrs.get('Middle Overs', 0):.2f}%</b> match win correlation, 
                proving that steady consolidation and spin dominance are twice as critical as death-overs fireworks."
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        col_q4_chart, col_q4_text = st.columns([3, 2])
        
        with col_q4_chart:
            st.markdown('#### 📊 Chart 4: Phase Dominance vs Match Victory Correlation')
            
            corr_df = pd.DataFrame({
                'Match Phase': ['Middle Overs', 'Powerplay', 'Death Overs'],
                'Correlation (%)': [
                    phase_corrs.get('Middle Overs', 0),
                    phase_corrs.get('Powerplay', 0),
                    phase_corrs.get('Death Overs', 0)
                ]
            })
            
            fig4 = px.bar(
                corr_df,
                x='Match Phase',
                y='Correlation (%)',
                color='Match Phase',
                color_discrete_map={
                    'Middle Overs': '#10B981', # Emerald
                    'Powerplay': '#3B82F6', # Blue
                    'Death Overs': '#F59E0B' # Amber
                },
                text=corr_df['Correlation (%)'].apply(lambda x: f'{x:.2f}%'),
                height=380,
                template=plotly_template
            )
            
            fig4.update_traces(textposition='outside', textfont=dict(size=12, color=plotly_font_color))
            fig4.update_layout(
                font=dict(color=plotly_font_color),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                showlegend=False,
                xaxis_title=None,
                yaxis_title='Match Win Correlation (%)',
                yaxis_range=[0, 100],
                margin=dict(t=20, b=20, l=10, r=10)
            )
            fig4.update_xaxes(title_font=dict(color=plotly_font_color), tickfont=dict(color=plotly_font_color))
            fig4.update_yaxes(title_font=dict(color=plotly_font_color), tickfont=dict(color=plotly_font_color))
            
            st.plotly_chart(fig4, use_container_width=True)

            st.markdown('#### 📅 Chart 4B: Has IPL Scoring Increased Over the Years?')
            season_avg_rows = []
            for sv in sorted(df_raw['season_clean'].unique()):
                m_s = df_raw[df_raw['season_clean'] == sv]
                mids = m_s['match_id'].unique()
                per_match = m_s.groupby('match_id')['runs_total'].sum()
                avg_t = per_match.mean() / 2  # per innings
                disp = '2008' if sv == 2007 else str(sv)
                season_avg_rows.append({'Season': disp, 'Avg Runs/Innings': avg_t})
            season_avg_df = pd.DataFrame(season_avg_rows)
            fig4b = go.Figure()
            fig4b.add_trace(go.Scatter(
                x=season_avg_df['Season'],
                y=season_avg_df['Avg Runs/Innings'],
                mode='lines+markers+text',
                text=season_avg_df['Avg Runs/Innings'].apply(lambda v: f'{v:.0f}'),
                textposition='top center',
                textfont=dict(size=9, color=plotly_font_color),
                line=dict(color='#3B82F6', width=3),
                marker=dict(size=8, color='#3B82F6'),
                fill='tozeroy',
                fillcolor='rgba(59,130,246,0.08)'
            ))
            fig4b.update_layout(
                font=dict(color=plotly_font_color),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                xaxis_title='Season',
                yaxis_title='Avg Runs Per Innings',
                height=260,
                margin=dict(t=20, b=20, l=10, r=10),
                template=plotly_template
            )
            fig4b.update_xaxes(tickfont=dict(color=plotly_font_color), title_font=dict(color=plotly_font_color))
            fig4b.update_yaxes(tickfont=dict(color=plotly_font_color), title_font=dict(color=plotly_font_color))
            st.plotly_chart(fig4b, use_container_width=True)

        with col_q4_text:
            st.markdown("""
            <div class="glass-card" style="height: 420px; overflow-y: auto;">
                <div class="card-title">🔬 How We Did the Math (Plain English)</div>
                <div class="card-body">
                We analysed <b>every single delivery</b> in IPL history —
                over <b>280,000 balls</b> across <b>1,200+ matches</b>!<br><br>
                <b>Step 1 — Clean the Data 🧹</b><br>
                Removed abandoned matches, ties &amp; no-results.
                Grouped overs into 3 phases for easy comparison.<br><br>
                <b>Step 2 — Toss Analysis 🪙</b><br>
                For each match: did the toss-winner also win the match?
                We counted how often that’s true across all games.<br><br>
                <b>Step 3 — Phase Scoring 📊</b><br>
                Totalled runs each team scored per phase per match.
                Then averaged across all games (winners vs losers).<br><br>
                <b>Step 4 — Phase vs Win Correlation ⚡</b><br>
                Asked: <i>“If one team outscored the other in a phase,
                how often did they win the whole match?”</i><br><br>
                <b>Step 5 — Player Rankings 🏆</b><br>
                Batter runs = sum of <code>runs_batter</code>.
                Bowler wickets = only bowler dismissals (caught, bowled,
                lbw etc.) — run outs don’t count!
                </div>
            </div>
            """, unsafe_allow_html=True)

