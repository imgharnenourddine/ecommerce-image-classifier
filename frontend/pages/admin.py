import streamlit as st
import pandas as pd
import requests
import time

# --- CONFIGURATION ---
st.set_page_config(
    page_title="Admin Panel - E-ComVision",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# URLs API
API_BASE = "http://127.0.0.1:5000/api/dashboard"
API_ADMIN_STATS = f"{API_BASE}/admin/global-stats"
API_ADMIN_USERS = f"{API_BASE}/admin/users-list"
API_LOGOUT = "http://127.0.0.1:5000/api/auth/logout"

# --- SÉCURITÉ ---
if 'requests_session' not in st.session_state:
    st.warning("🔒 Connexion requise.")
    time.sleep(1)
    st.switch_page("pages/login.py")

# --- CSS PREMIUM (DESIGN IDENTIQUE À PREDICT) ---
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
    }

    /* DESIGN DU BOUTON LOGOUT (VERT-BLEU) */
    .stButton > button {
        background: linear-gradient(135deg, #00f260, #0575e6) !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        font-weight: 700 !important;
        height: 45px !important;
        transition: all 0.3s ease !important;
        opacity: 1 !important;
    }

    .stButton > button:hover {
        transform: scale(1.02) !important;
        box-shadow: 0 0 20px rgba(0, 242, 96, 0.4) !important;
    }

    /* CARTES KPI & TABLEAU (GLASSMORPHISM) */
    [data-testid="stVerticalBlockBorderWrapper"] {
        background: rgba(255, 255, 255, 0.03) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 20px !important;
        padding: 25px !important;
        backdrop-filter: blur(10px);
    }
    
    h1, h2, h3 { color: white !important; }
    [data-testid="stMetricValue"] { font-size: 2.2rem !important; font-weight: 800 !important; color: #00f260 !important; }
    [data-testid="stMetricLabel"] { color: #aaa !important; font-size: 1rem !important; }
</style>
""", unsafe_allow_html=True)

# --- NAVBAR ADMIN (LOGOUT UNIQUEMENT) ---
nav_c1, nav_c2, nav_c3 = st.columns([6, 2, 1.5]) 

with nav_c1:
    st.markdown("<h2 style='color:white; margin:0;'>🛡️ Panneau d'Administration</h2>", unsafe_allow_html=True)

with nav_c3:
    if st.button("Logout", use_container_width=True):
        try:
            st.session_state['requests_session'].post(API_LOGOUT)
        except: pass
        del st.session_state['requests_session']
        st.switch_page("pages/login.py")

st.markdown("<hr style='opacity:0.1; margin-bottom:30px;'>", unsafe_allow_html=True)

# --- APPELS API ---
session = st.session_state['requests_session']
try:
    resp_global = session.get(API_ADMIN_STATS)
    global_stats = resp_global.json() if resp_global.status_code == 200 else {}

    resp_users = session.get(API_ADMIN_USERS)
    all_users = resp_users.json() if resp_users.status_code == 200 else []
except:
    st.error("Erreur de connexion API")
    st.stop()

# --- TRAITEMENT DES DONNÉES ---
if all_users:
    df_all = pd.DataFrame(all_users)
    # 1. Filtre : Uniquement les utilisateurs normaux
    df_normal = df_all[df_all['role'] == "Utilisateur"]
    # 2. KPI Additionnel : Utilisateurs ayant au moins fait 1 scan
    active_users = len(df_normal[df_normal['total_scans'] > 0])
else:
    df_normal = pd.DataFrame()
    active_users = 0

# 3. KPI Additionnel : Top Catégorie
dist = global_stats.get("class_distribution", {})
top_cat = max(dist, key=dist.get) if dist else "N/A"

# --- AFFICHAGE ---

# Nouvelle Section KPI (Plus grande et plus riche)
st.markdown("### 📈 Statistiques Globales")
k1, k2, k3, k4 = st.columns(4)

with k1:
    with st.container(border=True):
        st.metric("Total Inscrits", global_stats.get("total_users", 0))
with k2:
    with st.container(border=True):
        st.metric("Scans Totaux", global_stats.get("total_predictions", 0))
with k3:
    with st.container(border=True):
        st.metric("Membres Actifs", active_users)
with k4:
    with st.container(border=True):
        st.metric("Top Catégorie", top_cat.title())

st.write("")

# Section Tableau (Plein écran)
with st.container(border=True):
    st.subheader("👤 Gestion des Comptes Utilisateurs")
    if not df_normal.empty:
        st.dataframe(
            df_normal[['id', 'username', 'email', 'total_scans']],
            use_container_width=True,
            hide_index=True,
            column_config={
                "id": st.column_config.TextColumn("ID"),
                "username": "Nom d'utilisateur",
                "email": "Adresse Email",
                "total_scans": st.column_config.NumberColumn(
                    "Images Analysées",
                    format="%d 📸",
                    help="Nombre total d'images envoyées par cet utilisateur"
                )
            }
        )
    else:
        st.info("Aucun utilisateur standard inscrit pour le moment.")

# Footer
st.markdown("<div style='text-align:center; margin-top:50px; opacity:0.3; font-size: 0.8rem;'>E-ComVision System Admin • Mise à jour en temps réel</div>", unsafe_allow_html=True)