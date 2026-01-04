import streamlit as st
import time
import requests

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(
    page_title="Connexion - E-Commerce Intelligence", 
    page_icon="🔒", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

# URL API
API_URL = "http://127.0.0.1:5000/api/auth/login"

# --- CSS PREMIUM & ANIMATIONS ---
st.markdown("""
<style>
    /* 1. CACHER LA NAVIGATION STREAMLIT */
    [data-testid="stSidebar"] { display: none; }
    [data-testid="stSidebarNav"] { display: none !important; }
    header[data-testid="stHeader"] { visibility: hidden; }
    .block-container { padding-top: 1rem !important; }

    /* 2. FOND ANIMÉ (Deep Space Blue) */
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

    /* 3. NAVBAR STYLISÉE */
    .nav-logo {
        font-size: 1.5rem;
        font-weight: 900;
        background: linear-gradient(90deg, #fff, #aaa);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        display: flex; align-items: center; height: 100%;
    }
    
    /* Boutons Navbar (Effet verre) */
    div[data-testid="stHorizontalBlock"] button {
        background: rgba(255,255,255,0.05) !important;
        border: 1px solid rgba(255,255,255,0.1) !important;
        color: white !important;
        border-radius: 12px !important;
        transition: all 0.3s ease;
    }
    div[data-testid="stHorizontalBlock"] button:hover {
        background: rgba(255,255,255,0.15) !important;
        border-color: white !important;
        transform: translateY(-2px);
    }

    /* 4. CARTE DE LOGIN (Le "Cadre") */
    /* On ne peut pas styler le container directement facilement, 
       donc on applique le style aux éléments internes ou via un div HTML wrapper si besoin. 
       Ici on va styler les inputs pour qu'ils ressortent bien. */

    /* Titre Gradient (Attire l'oeil) */
    .gradient-text {
        font-weight: 800;
        background: -webkit-linear-gradient(45deg, #00f260, #0575e6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3rem;
        margin-bottom: 10px;
    }

    /* Champs de saisie Modernes */
    .stTextInput > div > div > input {
        background-color: rgba(0, 0, 0, 0.3);
        color: white;
        border: 1px solid rgba(255, 255, 255, 0.15);
        border-radius: 12px;
        padding: 15px;
        font-size: 16px;
        transition: all 0.3s ease;
    }
    
    /* Lueur au focus */
    .stTextInput > div > div > input:focus {
        border-color: #0575e6;
        background-color: rgba(5, 117, 230, 0.05);
        box-shadow: 0 0 20px rgba(5, 117, 230, 0.2);
    }
    
    label { color: #cccccc !important; font-size: 0.9rem; }

    /* 5. BOUTON PRINCIPAL (CTA) */
    .stButton button {
        background: linear-gradient(90deg, #00f260, #0575e6);
        color: white !important;
        border: none;
        height: 50px;
        font-size: 18px !important;
        font-weight: 700 !important;
        border-radius: 12px !important;
        margin-top: 10px;
        box-shadow: 0 4px 15px rgba(5, 117, 230, 0.4);
        transition: all 0.3s ease;
    }
    
    .stButton button:hover {
        transform: scale(1.02);
        box-shadow: 0 6px 25px rgba(0, 242, 96, 0.5);
    }
    
    /* Animation d'apparition */
    .login-container {
        animation: fadeIn 1s ease-out;
    }
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }

</style>
""", unsafe_allow_html=True)

# --- NAVBAR ---
nav_c1, nav_c2, nav_c3, nav_c4 = st.columns([2, 5, 1, 1])

with nav_c1:
    st.markdown('<div class="nav-logo">⚡ E-ComVision</div>', unsafe_allow_html=True)

with nav_c3:
    if st.button("🏠 Home", use_container_width=True):
        st.switch_page("Home.py")

with nav_c4:
    if st.button("✨ Sign Up", use_container_width=True):
        st.switch_page("pages/register.py")

st.markdown("<hr style='border: 0; height: 1px; background: linear-gradient(to right, transparent, rgba(255,255,255,0.1), transparent); margin-bottom: 50px;'>", unsafe_allow_html=True)


# --- SECTION CENTRALE (LOGIN) ---
# On utilise des colonnes pour centrer la carte au milieu de l'écran
col_left, col_center, col_right = st.columns([1, 1.2, 1])

with col_center:
    # Conteneur visuel
    st.markdown('<div class="login-container">', unsafe_allow_html=True)
    
    # Titre accrocheur
    st.markdown('<div style="text-align: center;">', unsafe_allow_html=True)
    st.markdown('<h1 class="gradient-text">Welcome Back</h1>', unsafe_allow_html=True)
    st.markdown('<p style="color: #888; margin-bottom: 30px; font-size: 1.1rem;">Accédez à votre espace d\'analyse IA sécurisé.</p>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Formulaire
    with st.form("login_form"):
        email = st.text_input("Adresse Email", placeholder="exemple@email.com")
        password = st.text_input("Mot de passe", type="password", placeholder="••••••••")
        
        st.write("") # Espace
        
        # Le bouton prendra le style CSS "stButton button" défini plus haut
        submitted = st.form_submit_button("Se connecter 🚀", use_container_width=True)

    # Gestion de la réponse API
    if submitted:
        if not email or not password:
            st.warning("⚠️ Veuillez remplir tous les champs.")
        else:
            with st.spinner("Vérification des accès..."):
                try:
                    if 'requests_session' not in st.session_state:
                        st.session_state['requests_session'] = requests.Session()
                    
                    session = st.session_state['requests_session']
                    payload = {"email": email, "password": password}
                    
                    # Appel API
                    response = session.post(API_URL, json=payload)
                    
                    if response.status_code == 200:
                        data = response.json()
                        role = data.get("role", "user")
                        username = data.get("username", "Utilisateur")
                        
                        st.success(f"Connexion réussie ! Redirection...")
                        time.sleep(1)
                        
                        if role == "admin":
                            st.switch_page("pages/admin.py")
                        else:
                            st.switch_page("pages/dashboard.py")
                            
                    elif response.status_code == 401:
                        st.error("❌ Email ou mot de passe incorrect.")
                    else:
                        st.error(f"Erreur serveur : {response.text}")

                except Exception as e:
                    st.error(f"Impossible de joindre le serveur. Vérifiez qu'il est lancé.")

    st.markdown('</div>', unsafe_allow_html=True) # Fin login-container

    # Petit lien discret en bas de carte
    st.markdown("""
        <div style="text-align: center; margin-top: 30px; opacity: 0.6; font-size: 0.9rem;">
            Protection par chiffrement Scrypt & HTTPS
        </div>
    """, unsafe_allow_html=True)