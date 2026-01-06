import streamlit as st
import time
import requests
from utils.styles import apply_premium_styles

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Sign Up - E-Commerce Intelligence", 
    page_icon="📝", 
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Apply Premium Styling & Animations
apply_premium_styles()

# API URL
API_URL = "http://127.0.0.1:5000/api/auth/register"

# --- NAVBAR (SIMPLIFIED) ---
nav_c1, nav_c2 = st.columns([3, 1])
with nav_c1:
    st.markdown('<div class="nav-logo">⚡ E-ComVision</div>', unsafe_allow_html=True)
with nav_c2:
    if st.button("🏠 Home", use_container_width=True):
        st.switch_page("Home.py")

st.markdown("<hr style='border: 0; height: 1px; background: linear-gradient(to right, transparent, rgba(255,255,255,0.1), transparent); margin-bottom: 30px;'>", unsafe_allow_html=True)

# --- HEADER ---
st.markdown("<h1 style='text-align: center;'>Create an Account</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #888;'>Join the platform to start analyzing your catalog.</p>", unsafe_allow_html=True)

# --- FORM IN A VISUAL "BOX" ---
with st.container(border=True):
    col1, col2 = st.columns(2)
    with col1:
        fname = st.text_input("First Name", placeholder="e.g. John")
    with col2:
        lname = st.text_input("Last Name", placeholder="e.g. Doe")

    email = st.text_input("Email Address", placeholder="email@example.com")
    username = st.text_input("Username", placeholder="Choose a username")

    p1, p2 = st.columns(2)
    with p1:
        password = st.text_input("Mot de passe", type="password", placeholder="••••••••")
    with p2:
        confirm_password = st.text_input("Confirm Password", type="password", placeholder="••••••••")

    st.write("") # Espace

    if st.button("Sign Up", use_container_width=True):
        if not fname or not lname or not email or not username or not password:
            st.warning("⚠️ Please fill in all fields.")
        elif password != confirm_password:
            st.error("❌ Passwords do not match.")
        else:
            with st.spinner("Creating account..."):
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
                        st.success("✅ Account created successfully! Redirecting...")
                        time.sleep(2)
                        st.switch_page("pages/login.py")
                    elif response.status_code == 400:
                        st.error(f"Error: {response.json().get('error', 'Invalid data')}")
                    else:
                        st.error(f"Error: {response.text}")
                except Exception as e:
                    st.error(f"Unable to contact the server: {e}")

# --- FOOTER ---
st.markdown("---")
col_text, col_btn = st.columns([2, 1])
with col_text:
    st.markdown("<div style='padding-top: 10px; text-align: right;'>Already have an account?</div>", unsafe_allow_html=True)
with col_btn:
    if st.button("Login"):
        st.switch_page("pages/login.py")
