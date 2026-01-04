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

# --- CSS PREMIUM (Deep Blue Theme & Layout Fix) ---
st.markdown("""
<style>
    /* 1. CACHER LA SIDEBAR NATIVE */
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
        font-family: 'Inter', sans-serif;
    }

    /* 3. NAVBAR */
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
        transition: all 0.3s ease;
    }
    .nav-btn button:hover {
        background: rgba(255,255,255,0.15) !important;
        border-color: white !important;
    }
    
    .logout-btn button {
        background: rgba(255, 50, 50, 0.1) !important;
        border: 1px solid rgba(255, 50, 50, 0.3) !important;
        color: #ff6b6b !important;
    }
    .logout-btn button:hover {
        background: rgba(255, 50, 50, 0.2) !important;
    }

    /* 4. LE FIX DU DESIGN (GLASS CARD) */
    /* On cible le conteneur avec bordure de Streamlit */
    [data-testid="stVerticalBlockBorderWrapper"] {
        background: rgba(255, 255, 255, 0.03) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 20px !important;
        padding: 30px !important;
        backdrop-filter: blur(10px);
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
    }
    /* On enlève le padding interne par défaut pour que le texte colle bien */
    [data-testid="stVerticalBlockBorderWrapper"] > div {
        gap: 1rem; 
    }

    /* 5. UPLOAD STYLING */
    .stFileUploader > div > div {
        background-color: rgba(0,0,0,0.2);
        border: 2px dashed rgba(255,255,255,0.2);
        border-radius: 15px;
        padding: 20px;
    }
    
    /* 6. BOUTONS */
    .stButton button {
        background: linear-gradient(135deg, #00f260, #0575e6);
        color: white !important;
        border: none;
        border-radius: 10px;
        font-weight: 700;
        padding: 10px 20px;
        transition: transform 0.2s;
    }
    .stButton button:hover {
        transform: scale(1.02);
        box-shadow: 0 0 15px rgba(0, 242, 96, 0.4);
    }

    /* Result Text */
    .prediction-title {
        font-size: 2rem;
        font-weight: 800;
        color: #00f260;
        margin-bottom: 0;
    }
    
    h3 {
        color: #f0f0f0 !important;
        font-weight: 600;
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
        st.markdown('<div class="nav-btn">', unsafe_allow_html=True)
        if st.button("📊 Dashboard", use_container_width=True):
            st.switch_page("pages/dashboard.py")
        st.markdown('</div>', unsafe_allow_html=True)
        
    with b2:
        st.markdown('<div class="logout-btn">', unsafe_allow_html=True)
        if st.button("Déconnexion", use_container_width=True):
            try:
                st.session_state['requests_session'].post(API_LOGOUT)
            except:
                pass
            del st.session_state['requests_session']
            st.switch_page("pages/login.py")
        st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<hr style='border: 0; height: 1px; background: rgba(255,255,255,0.1); margin-bottom: 30px;'>", unsafe_allow_html=True)


# --- CONTENU PRINCIPAL ---
st.markdown("<h1 style='text-align: center; margin-bottom: 40px;'>Nouvelle Analyse Produit</h1>", unsafe_allow_html=True)

col_left, col_right = st.columns([1, 1.2], gap="large")

# --- COLONNE GAUCHE : UPLOAD ---
with col_left:
    # --- MODIFICATION IMPORTANTE : Utilisation de st.container(border=True) ---
    # Le CSS cible [data-testid="stVerticalBlockBorderWrapper"] pour appliquer le style "Glass"
    with st.container(border=True):
        st.subheader("📸 Image Source")
        st.write("Formats supportés: JPG, PNG")
        
        uploaded_file = st.file_uploader("", type=["jpg", "png", "jpeg"], label_visibility="collapsed")
        
        if uploaded_file is not None:
            image = Image.open(uploaded_file)
            st.image(image, caption='Aperçu de l\'image', use_container_width=True)
            
            st.write("") 
            
            if st.button("Lancer l'Analyse IA 🚀", use_container_width=True, type="primary"):
                with st.spinner("Traitement en cours par le modèle..."):
                    try:
                        uploaded_file.seek(0)
                        files = {'file': uploaded_file.getvalue()}
                        session = st.session_state['requests_session']
                        
                        response = session.post(API_URL, files=files)
                        
                        if response.status_code == 200:
                            st.session_state['prediction_data'] = response.json()
                            st.success("Analyse terminée avec succès !")
                        elif response.status_code == 401:
                            st.error("Session expirée.")
                            time.sleep(1)
                            st.switch_page("pages/login.py")
                        else:
                            st.error(f"Erreur API : {response.text}")
                            
                    except Exception as e:
                        st.error(f"Erreur de connexion : {e}")
        
        else:
            st.markdown("""
            <div style="text-align: center; padding: 40px; color: #666;">
                <div style="font-size: 3rem; margin-bottom: 10px;">☁️</div>
                Glissez une image ici ou cliquez pour parcourir.
            </div>
            """, unsafe_allow_html=True)


# --- COLONNE DROITE : RÉSULTATS ---
with col_right:
    # --- MODIFICATION IMPORTANTE : Même chose ici ---
    with st.container(border=True):
        st.subheader("🔍 Résultats de l'analyse")
        
        if 'prediction_data' in st.session_state and uploaded_file is not None:
            data = st.session_state['prediction_data']
            
            pred_label = data.get('resultat') or (data.get('predictions')[0]['class'] if data.get('predictions') else "Inconnu")
            confidence = data.get('confiance') or (data.get('predictions')[0]['confidence'] if data.get('predictions') else 0.0)
            
            st.markdown(f'<div class="prediction-title">{str(pred_label).title()}</div>', unsafe_allow_html=True)
            st.markdown(f"<p style='color: #aaa; font-size: 1.1rem;'>Confiance du modèle : <b>{confidence*100:.2f}%</b></p>", unsafe_allow_html=True)
            
            st.progress(confidence)
            
            st.markdown("---")
            
            if confidence > 0.85:
                st.success("✅ Classification Très Fiable")
                st.markdown("Le modèle est quasiment certain de ce résultat.")
            elif confidence > 0.60:
                st.warning("⚠️ Classification Moyenne")
                st.markdown("Le modèle a un doute raisonnable. Vérification conseillée.")
            else:
                st.error("❌ Classification Incertaine")
                st.markdown("Le modèle ne reconnaît pas bien cet objet.")

            if st.checkbox("Voir les données brutes"):
                st.json(data)

        else:
            st.markdown("""
            <div style="text-align: center; padding-top: 50px; opacity: 0.5;">
                <h3>En attente...</h3>
                <p>Les résultats s'afficheront ici après l'analyse.</p>
                <div style="font-size: 4rem; margin-top: 20px;">📊</div>
            </div>
            """, unsafe_allow_html=True)