import streamlit as st
import pandas as pd
import requests
import time

# --- CONFIGURATION ---
st.set_page_config(
    page_title="Dashboard - E-Commerce Intelligence",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# URLs API
API_BASE = "http://127.0.0.1:5000/api/dashboard"
API_STATS = f"{API_BASE}/user/stats"
API_HISTORY = f"{API_BASE}/user/history"
API_LOGOUT = "http://127.0.0.1:5000/api/auth/logout"

# --- SÉCURITÉ ---
if 'requests_session' not in st.session_state:
    st.warning("🔒 Vous devez être connecté pour accéder au Dashboard.")
    time.sleep(2)
    st.switch_page("pages/login.py")

# --- CSS PREMIUM (IDENTIQUE À PREDICT) ---
st.markdown("""
<style>
    /* 1. INTERFACE */
    [data-testid="stSidebar"] { display: none; }
    [data-testid="stSidebarNav"] { display: none !important; }
    header[data-testid="stHeader"] { visibility: hidden; }
    .block-container { padding-top: 1rem !important; }

    /* 2. FOND ANIMÉ */
    @keyframes gradientMove {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    .stApp {
        background-color: #000000;
        background-image: radial-gradient(circle at center, #0a1033 0%, #000000 100%);
        background-size: 200% 200%;
        animation: gradientMove 15s ease infinite;
        color: white;
    }

    /* 3. DESIGN DES BOUTONS (COULEUR PREDICT) */
    /* Ciblage précis des boutons pour forcer le dégradé vert/bleu */
    .stButton > button {
        background: linear-gradient(135deg, #00f260, #0575e6) !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        font-weight: 700 !important;
        height: 45px !important;
        width: 100% !important;
        transition: all 0.3s ease !important;
        opacity: 1 !important;
        box-shadow: 0 4px 15px rgba(0, 242, 96, 0.2);
    }

    .stButton > button:hover {
        transform: scale(1.02) !important;
        box-shadow: 0 0 20px rgba(0, 242, 96, 0.4) !important;
        color: white !important;
    }

    /* Logo et titres */
    .nav-logo {
        font-size: 1.5rem;
        font-weight: 900;
        background: linear-gradient(90deg, #fff, #aaa);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    /* 4. CARTES GLASSMORPHISM */
    [data-testid="stVerticalBlockBorderWrapper"] {
        background: rgba(255, 255, 255, 0.03) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 20px !important;
        padding: 25px !important;
        backdrop-filter: blur(10px);
    }
</style>
""", unsafe_allow_html=True)

# --- NAVBAR ---
nav_c1, nav_c2, nav_c3 = st.columns([2, 5, 2])

with nav_c1:
    st.markdown('<div class="nav-logo">📊 Dashboard</div>', unsafe_allow_html=True)

with nav_c3:
    b1, b2 = st.columns(2)
    with b1:
        if st.button("🔮 Predict", use_container_width=True):
            st.switch_page("pages/predictions.py")
        
    with b2:
        if st.button("Logout", use_container_width=True):
            try:
                st.session_state['requests_session'].post(API_LOGOUT)
            except: pass
            del st.session_state['requests_session']
            st.switch_page("pages/login.py")

st.markdown("<hr style='border: 0; height: 1px; background: rgba(255,255,255,0.1); margin-bottom: 30px;'>", unsafe_allow_html=True)

# --- RESTE DU CODE (LOGIQUE API) ---
session = st.session_state['requests_session']
try:
    resp_stats = session.get(API_STATS)
    stats = resp_stats.json() if resp_stats.status_code == 200 else {}
    resp_history = session.get(API_HISTORY)
    df = pd.DataFrame(resp_history.json()) if resp_history.status_code == 200 else pd.DataFrame()
except:
    st.error("❌ Serveur inaccessible")
    st.stop()

st.title(f"Bonjour, {stats.get('username', 'Utilisateur')} 👋")

m1, m2, m3 = st.columns(3)
with m1:
    with st.container(border=True):
        st.metric("Analyses Totales", stats.get("total_scans", 0))
with m2:
    with st.container(border=True):
        st.metric("Confiance Moyenne", f"{stats.get('avg_confidence', 0)}%")
with m3:
    with st.container(border=True):
        st.metric("Top Catégorie", stats.get("top_category", "Aucune"))

st.write("")

col_table, col_viz = st.columns([1.5, 1], gap="medium")
with col_table:
    with st.container(border=True):
        st.subheader("📑 Historique")
        if not df.empty:
            df_display = df[['date', 'category', 'confidence', 'status']].copy()
            st.dataframe(df_display, use_container_width=True, hide_index=True)
        else:
            st.info("Aucun historique.")

with col_viz:
    with st.container(border=True):
        st.subheader("📈 Répartition")
        if not df.empty:
            st.bar_chart(df['category'].value_counts(), color="#0575e6")