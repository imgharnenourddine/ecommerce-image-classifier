import streamlit as st
import requests
from PIL import Image
import time
import io

# --- CONFIGURATION ---
st.set_page_config(
    page_title="IA Predictor - E-Commerce Intelligence",
    page_icon="🔮",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# URL API
API_URL = "http://127.0.0.1:5000/api/predict"
API_LOGOUT = "http://127.0.0.1:5000/api/auth/logout"

# --- SÉCURITÉ ---
if 'requests_session' not in st.session_state:
    st.warning("🔒 Vous devez être connecté pour accéder à l'IA.")
    time.sleep(2)
    st.switch_page("pages/login.py")

# --- CSS PREMIUM (Inchangé) ---
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
        font-family: 'Inter', sans-serif;
    }

    .nav-logo {
        font-size: 1.5rem;
        font-weight: 900;
        background: linear-gradient(90deg, #fff, #aaa);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        display: flex; align-items: center; height: 100%;
    }
    
    .nav-btn button {
        background: rgba(255,255,255,0.05) !important;
        border: 1px solid rgba(255,255,255,0.1) !important;
        color: white !important;
        border-radius: 8px !important;
    }
    
    .logout-btn button {
        background: rgba(255, 50, 50, 0.1) !important;
        border: 1px solid rgba(255, 50, 50, 0.3) !important;
        color: #ff6b6b !important;
    }

    [data-testid="stVerticalBlockBorderWrapper"] {
        background: rgba(255, 255, 255, 0.03) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 20px !important;
        padding: 30px !important;
        backdrop-filter: blur(10px);
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
    }

    .stButton button {
        background: linear-gradient(135deg, #00f260, #0575e6);
        color: white !important;
        border: none;
        border-radius: 10px;
        font-weight: 700;
        width: 100%;
    }

    .prediction-title {
        font-size: 2.5rem;
        font-weight: 800;
        color: #00f260;
        margin-bottom: 10px;
        text-transform: capitalize;
    }
</style>
""", unsafe_allow_html=True)

# --- NAVBAR ---
nav_c1, nav_c2, nav_c3 = st.columns([2, 5, 2])
with nav_c1:
    st.markdown('<div class="nav-logo">🔮 AI Predictor</div>', unsafe_allow_html=True)
with nav_c3:
    b1, b2 = st.columns(2)
    with b1:
        if st.button("📊 Dashboard", use_container_width=True):
            st.switch_page("pages/dashboard.py")
    with b2:
        if st.button("Déconnexion", use_container_width=True):
            try: st.session_state['requests_session'].post(API_LOGOUT)
            except: pass
            del st.session_state['requests_session']
            st.switch_page("pages/login.py")

st.markdown("<hr style='border: 0; height: 1px; background: rgba(255,255,255,0.1); margin-bottom: 30px;'>", unsafe_allow_html=True)

# --- CONTENU PRINCIPAL ---
st.markdown("<h1 style='text-align: center; margin-bottom: 40px;'>Nouvelle Analyse Produit</h1>", unsafe_allow_html=True)

col_left, col_right = st.columns([1, 1.2], gap="large")

with col_left:
    with st.container(border=True):
        st.subheader("📸 Image Source")
        uploaded_file = st.file_uploader("", type=["jpg", "png", "jpeg"], label_visibility="collapsed")
        
        # --- LOGIQUE DE RÉINITIALISATION ---
        if uploaded_file is not None:
            # Si c'est un nouveau fichier, on efface les anciennes données de prédiction
            if "last_file_name" not in st.session_state or st.session_state.last_file_name != uploaded_file.name:
                if 'prediction_data' in st.session_state:
                    del st.session_state['prediction_data']
                st.session_state.last_file_name = uploaded_file.name

            image = Image.open(uploaded_file)
            st.image(image, caption='Aperçu du produit', use_container_width=True)
            
            if st.button("Lancer l'Analyse IA 🚀", type="primary"):
                with st.spinner("L'IA analyse les caractéristiques..."):
                    try:
                        uploaded_file.seek(0)
                        files = {'file': uploaded_file.getvalue()}
                        session = st.session_state['requests_session']
                        response = session.post(API_URL, files=files)
                        
                        if response.status_code == 200:
                            st.session_state['prediction_data'] = response.json()
                        elif response.status_code == 401:
                            st.switch_page("pages/login.py")
                        else:
                            st.error(f"Erreur : {response.text}")
                    except Exception as e:
                        st.error(f"Erreur de connexion : {e}")
        else:
            # On efface tout si aucun fichier n'est présent
            if 'prediction_data' in st.session_state:
                del st.session_state['prediction_data']
            st.markdown('<div style="text-align: center; padding: 40px; color: #666;">☁️ Glissez une image ici</div>', unsafe_allow_html=True)

with col_right:
    with st.container(border=True):
        st.subheader("🔍 Résultats de l'analyse")
        
        # L'affichage ne se déclenche que si prediction_data existe ET correspond au fichier actuel
        if 'prediction_data' in st.session_state:
            data = st.session_state['prediction_data']
            
            # Gestion des formats (Back-end PyTorch ou Keras)
            label = data.get('resultat')
            conf = data.get('confiance', 0.0)

            st.markdown(f'<div class="prediction-title">{label}</div>', unsafe_allow_html=True)
            
            # Formatage du texte selon si conf est 0.85 ou 85
            display_conf = conf * 100 if conf <= 1.0 else conf
            st.markdown(f"<p style='color: #aaa; font-size: 1.1rem;'>Indice de confiance : <b>{display_conf:.2f}%</b></p>", unsafe_allow_html=True)
            
            # Barre de progression (Streamlit veut 0.0 à 1.0)
            progress_val = conf if conf <= 1.0 else conf / 100
            st.progress(min(float(progress_val), 1.0))
            
            st.markdown("---")
            
            if progress_val > 0.80:
                st.success("✅ Classification Très Fiable")
            elif progress_val > 0.50:
                st.warning("⚠️ Classification Moyenne")
            else:
                st.error("❌ Classification Incertaine")
        else:
            st.markdown("""
            <div style="text-align: center; padding-top: 50px; opacity: 0.5;">
                <h3>En attente d'analyse...</h3>
                <p>Chargez une image et cliquez sur le bouton pour voir les résultats.</p>
                <div style="font-size: 4rem; margin-top: 20px;">📊</div>
            </div>
            """, unsafe_allow_html=True)