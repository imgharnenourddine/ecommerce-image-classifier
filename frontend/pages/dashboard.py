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

# --- CSS PREMIUM ---
st.markdown("""
<style>
    [data-testid="stSidebar"] { display: none; }
    [data-testid="stSidebarNav"] { display: none !important; }
    header[data-testid="stHeader"] { visibility: hidden; }
    .block-container { padding-top: 1rem !important; }

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

    .stButton > button {
        background: linear-gradient(135deg, #00f260, #0575e6) !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        font-weight: 700 !important;
        height: 45px !important;
        width: 100% !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(0, 242, 96, 0.2);
    }

    .nav-logo {
        font-size: 1.5rem;
        font-weight: 900;
        background: linear-gradient(90deg, #fff, #aaa);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

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
            try: st.session_state['requests_session'].post(API_LOGOUT)
            except: pass
            del st.session_state['requests_session']
            st.switch_page("pages/login.py")

st.markdown("<hr style='border: 0; height: 1px; background: rgba(255,255,255,0.1); margin-bottom: 30px;'>", unsafe_allow_html=True)

# --- LOGIQUE API ---
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

# --- MÉTRIQUES CORRIGÉES ---
m1, m2, m3 = st.columns(3)
with m1:
    with st.container(border=True):
        st.metric("Analyses Totales", stats.get("total_scans", 0))

with m2:
    with st.container(border=True):
        # Correction du pourcentage : 0.85 -> 85.0%
        raw_conf = stats.get('avg_confidence', 0)
        # On vérifie si c'est un ratio (ex: 0.76) ou déjà un pourcentage (ex: 76)
        display_conf = raw_conf * 100 if raw_conf <= 1.0 else raw_conf
        st.metric("Confiance Moyenne", f"{display_conf:.2f}%")

with m3:
    with st.container(border=True):
        st.metric("Top Catégorie", stats.get("top_category", "Aucune"))

st.write("")

# --- HISTORIQUE ET VISUALISATION ---
col_table, col_viz = st.columns([1.5, 1], gap="medium")
with col_table:
    with st.container(border=True):
        st.subheader("📑 Historique")
        if not df.empty:
            df_display = df[['date', 'category', 'confidence', 'status']].copy()
            
            # Formater la colonne confiance en pourcentage pour le tableau
            # Si la valeur est 0.85, elle devient "85.0%"
            df_display['confidence'] = df_display['confidence'].apply(
                lambda x: f"{x*100:.1f}%" if x <= 1.0 else f"{x:.1f}%"
            )
            
            st.dataframe(df_display, use_container_width=True, hide_index=True)
        else:
            st.info("Aucun historique.")

with col_viz:
    with st.container(border=True):
        st.subheader("📈 Répartition")
        if not df.empty:
            # Graphique des catégories
            st.bar_chart(df['category'].value_counts(), color="#0575e6")