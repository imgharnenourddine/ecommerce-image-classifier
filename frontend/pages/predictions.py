import streamlit as st
import requests
from PIL import Image
import time
import io
from streamlit_cropper import st_cropper

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

# Liste temporaire pour le multi-objets
if 'temp_list' not in st.session_state:
    st.session_state['temp_list'] = []

# --- CSS PREMIUM (TON STYLE EXACT + FIX ALIGNEMENT) ---
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
        display: flex; 
        align-items: center; 
        height: 42px; /* Aligné sur la hauteur des boutons */
    }
    
    /* Boutons de la Navbar */
    .stButton button {
        background: linear-gradient(135deg, #00f260, #0575e6);
        color: white !important;
        border: none;
        border-radius: 10px;
        font-weight: 700;
        width: 100%;
        height: 42px !important; /* Hauteur fixe pour l'équilibre */
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

    .prediction-title {
        font-size: 2.5rem;
        font-weight: 800;
        color: #00f260;
        margin-bottom: 10px;
        text-transform: capitalize;
    }
</style>
""", unsafe_allow_html=True)

# --- NAVBAR RÉÉQUILIBRÉE ---
nav_c1, nav_c2, nav_c3 = st.columns([2.5, 4.5, 3]) 
with nav_c1:
    st.markdown('<div class="nav-logo">🔮 AI Predictor</div>', unsafe_allow_html=True)

with nav_c3:
    # Deux colonnes internes strictement égales
    b1, b2 = st.columns(2)
    with b1:
        if st.button("📊 Dashboard", use_container_width=True):
            st.switch_page("pages/dashboard.py")
    with b2:
        st.markdown('<div class="logout-btn">', unsafe_allow_html=True)
        if st.button("Déconnexion", use_container_width=True):
            try: st.session_state['requests_session'].post(API_LOGOUT)
            except: pass
            st.session_state.clear()
            st.switch_page("pages/login.py")
        st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<hr style='border: 0; height: 1px; background: rgba(255,255,255,0.1); margin-bottom: 30px;'>", unsafe_allow_html=True)

# --- CONTENU PRINCIPAL ---
st.markdown("<h1 style='text-align: center; margin-bottom: 40px;'>Nouvelle Analyse Produit</h1>", unsafe_allow_html=True)

col_left, col_right = st.columns([1.5, 1], gap="large")

with col_left:
    with st.container(border=True):
        st.subheader("📸 Image Source")
        uploaded_file = st.file_uploader("", type=["jpg", "png", "jpeg"], label_visibility="collapsed")
        
        if uploaded_file:
            if st.session_state.get('last_fn') != uploaded_file.name:
                st.session_state.temp_list = []
                st.session_state.last_fn = uploaded_file.name

            img_raw = Image.open(uploaded_file)
            
            # --- FIX TAILLE IMAGE ---
            target_w = 800
            ratio = target_w / float(img_raw.size[0])
            img_disp = img_raw.resize((target_w, int(img_raw.size[1] * ratio)), Image.Resampling.LANCZOS)
            
            st.info("💡 Cadrez un objet et cliquez sur 'Analyser cette zone'")
            
            crop = st_cropper(img_disp, realtime_update=True, box_color='#00f260', aspect_ratio=None)
            
            if st.button("Lancer l'Analyse de la zone 🚀", type="primary"):
                with st.spinner("L'IA analyse la zone..."):
                    buf = io.BytesIO()
                    crop.save(buf, format="JPEG")
                    files = {'file': ('crop.jpg', buf.getvalue(), 'image/jpeg')}
                    
                    res = st.session_state['requests_session'].post(f"{API_URL}?mode=temp", files=files)
                    if res.status_code == 200:
                        data = res.json()
                        st.session_state.temp_list.append({
                            "crop": crop,
                            "label": data['resultat'],
                            "conf": data['confiance']
                        })
                        st.rerun()

with col_right:
    with st.container(border=True):
        st.subheader("🔍 Résultats de l'analyse")
        
        if not st.session_state.temp_list:
            st.markdown("""
            <div style="text-align: center; padding-top: 50px; opacity: 0.5;">
                <h3>En attente d'analyse...</h3>
                <p>Cadrez un objet à gauche et analysez-le.</p>
                <div style="font-size: 4rem; margin-top: 20px;">📊</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            for item in st.session_state.temp_list:
                c1, c2 = st.columns([1, 3])
                c1.image(item['crop'], use_container_width=True)
                
                label = item['label']
                conf = item['conf']
                display_conf = conf * 100 if conf <= 1.0 else conf
                
                with c2:
                    st.markdown(f'<div style="font-size:1.5rem; font-weight:700; color:#00f260;">{label}</div>', unsafe_allow_html=True)
                    st.markdown(f"<p style='color: #aaa; margin-bottom:0;'>Confiance : <b>{display_conf:.2f}%</b></p>", unsafe_allow_html=True)
                    st.progress(min(float(conf if conf <= 1.0 else conf/100), 1.0))
                st.divider()
            
            if st.button("✅ Enregistrer l'Analyse Totale"):
                unique = {}
                for x in st.session_state.temp_list:
                    if x['label'] not in unique or x['conf'] > unique[x['label']]['s']:
                        unique[x['label']] = {'s': x['conf'], 't': f"{x['conf']*100:.1f}%"}
                
                f_labels = ", ".join(unique.keys())
                f_confs = ", ".join([v['t'] for v in unique.values()])
                
                uploaded_file.seek(0)
                files = {'file': (uploaded_file.name, uploaded_file.read(), uploaded_file.type)}
                payload = {"final_labels": f_labels, "final_confs": f_confs}
                
                resp = st.session_state['requests_session'].post(f"{API_URL}?mode=final", files=files, data=payload)
                if resp.status_code == 200:
                    st.session_state.temp_list = []
                    st.success("Enregistré avec succès !")
                    time.sleep(1)
                    st.switch_page("pages/dashboard.py")

if st.button("🗑️ Réinitialiser tout", key="reset"):
    st.session_state.temp_list = []
    st.rerun()