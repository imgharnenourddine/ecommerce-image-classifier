import streamlit as st
import time
import requests

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(
    page_title="Inscription - E-Commerce Intelligence", 
    page_icon="📝", 
    layout="centered",
    initial_sidebar_state="collapsed" # On réduit la barre par défaut
)

# URL de votre API (Notez le 'registre' à la fin comme dans votre backend)
API_URL = "http://127.0.0.1:5000/api/auth/registre"

# --- CSS PERSONNALISÉ (Design & Cache Navigation) ---
st.markdown("""
<style>
    /* 1. CACHER LA NAVIGATION STREAMLIT (Menu Latéral) */
    [data-testid="stSidebarNav"] {
        display: none !important;
    }
    
    /* Animation du fond */
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

    /* Style des champs de saisie */
    .stTextInput > div > div > input {
        background-color: rgba(255, 255, 255, 0.05);
        color: white;
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 8px;
        padding: 10px;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #0575e6;
        box-shadow: 0 0 10px rgba(5, 117, 230, 0.3);
    }
    
    /* Conteneur "Carte" pour le formulaire */
    .register-card {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 20px;
        padding: 30px;
        backdrop-filter: blur(10px);
        margin-top: 20px;
        box-shadow: 0 20px 40px rgba(0,0,0,0.4);
    }

    /* Bouton Principal */
    .stButton button {
        background: linear-gradient(135deg, #00f260, #0575e6);
        color: white !important;
        border: none;
        border-radius: 8px;
        font-weight: bold;
        transition: transform 0.2s, box-shadow 0.2s;
    }
    .stButton button:hover {
        transform: scale(1.02);
        box-shadow: 0 0 20px rgba(0, 242, 96, 0.4);
    }
    
    /* Bouton Secondaire (Login) */
    div[data-testid="stVerticalBlock"] > div > div[data-testid="stVerticalBlock"] > div > button {
        background: transparent;
        border: 1px solid rgba(255,255,255,0.3);
    }

    /* Labels en blanc */
    label { color: #ddd !important; }
    
    /* Cacher le header Streamlit */
    header { visibility: hidden; }
    
</style>
""", unsafe_allow_html=True)

# --- EN-TÊTE ---
st.title("Créer un compte")
st.markdown("Rejoignez la plateforme pour commencer à analyser votre catalogue.")

# --- FORMULAIRE DANS UNE "BOITE" VISUELLE ---
# On utilise un container simulé par le CSS, mais ici on structure les champs
with st.container():
    
    # 1. Nom et Prénom sur la même ligne
    col1, col2 = st.columns(2)
    with col1:
        fname = st.text_input("Prénom", placeholder="Ex: Jean")
    with col2:
        lname = st.text_input("Nom", placeholder="Ex: Dupont")

    # 2. Email et Username
    email = st.text_input("Adresse Email", placeholder="email@exemple.com")
    username = st.text_input("Nom d'utilisateur", placeholder="Choisissez un pseudo")

    # 3. Mots de passe
    p1, p2 = st.columns(2)
    with p1:
        password = st.text_input("Mot de passe", type="password", placeholder="••••••••")
    with p2:
        confirm_password = st.text_input("Confirmer le mot de passe", type="password", placeholder="••••••••")

    st.write("") # Espace

    # --- BOUTON D'INSCRIPTION ---
    if st.button("S'inscrire", use_container_width=True, type="primary"):
        
        # A. Validation Locale
        if not fname or not lname or not email or not username or not password:
            st.warning("⚠️ Veuillez remplir tous les champs.")
        elif password != confirm_password:
            st.error("❌ Les mots de passe ne correspondent pas.")
        else:
            # B. Envoi au Backend
            with st.spinner("Création du compte en cours..."):
                try:
                    payload = {
                        "fname": fname,
                        "lname": lname,
                        "username": username,
                        "email": email,
                        "password": password
                    }
                    
                    response = requests.post(API_URL, json=payload)
                    
                    if response.status_code == 201:
                        st.success("✅ Compte créé avec succès ! Redirection...")
                        time.sleep(2)
                        st.switch_page("pages/login.py")
                    elif response.status_code == 400:
                        st.error(f"Erreur : {response.json().get('error', 'Données invalides')}")
                    elif response.status_code == 500:
                        st.error("Erreur serveur. Veuillez réessayer plus tard.")
                    else:
                        st.error(f"Erreur inconnue : {response.text}")
                        
                except Exception as e:
                    st.error(f"Impossible de contacter le serveur : {e}")

# --- PIED DE PAGE (Lien vers Login) ---
st.markdown("---")
col_text, col_btn = st.columns([2, 1])
with col_text:
    st.markdown("<div style='padding-top: 10px; text-align: right;'>Vous avez déjà un compte ?</div>", unsafe_allow_html=True)
with col_btn:
    if st.button("Se connecter"):
        st.switch_page("pages/login.py")