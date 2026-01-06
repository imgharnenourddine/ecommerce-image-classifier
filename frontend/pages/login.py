import streamlit as st
import time
import requests
from utils.styles import apply_premium_styles

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Login - E-Commerce Intelligence", 
    page_icon="🔒", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

# URL API
API_URL = "http://127.0.0.1:5000/api/auth/login"

# --- CSS PREMIUM & ANIMATIONS ---

# Apply Premium Styling & Animations
apply_premium_styles()

# --- NAVBAR ---
nav_c1, nav_c2, nav_c3, nav_c4 = st.columns([2, 5, 1, 1])

with nav_c1:
    st.markdown('<div class="nav-logo">⚡ E-ComVision</div>', unsafe_allow_html=True)

with nav_c3:
    if st.button("🏠 Home", use_container_width=True):
        st.switch_page("Home.py")

with nav_c4:
    if st.button("Sign Up", use_container_width=True):
        st.switch_page("pages/register.py")

st.markdown("<hr style='border: 0; height: 1px; background: linear-gradient(to right, transparent, rgba(255,255,255,0.1), transparent); margin-bottom: 50px;'>", unsafe_allow_html=True)


# --- CENTRAL SECTION (LOGIN) ---
# Use columns to center the card on the screen
col_left, col_center, col_right = st.columns([1, 1.2, 1])

with col_center:
    # Native Bento Card Visual Container
    with st.container(border=True):
        # Catchy Title
        st.markdown('<div style="text-align: center;">', unsafe_allow_html=True)
        st.markdown('<h1>Welcome Back</h1>', unsafe_allow_html=True)
        st.markdown('<p style="color: #888; margin-bottom: 30px; font-size: 1.1rem;">Access your secure AI analysis space.</p>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        # Form
        username = st.text_input("Email", placeholder="Enter your email")
        password = st.text_input("Password", type="password", placeholder="••••••••")

        st.write("") # Space

        # Styled button
        if st.button("Login", use_container_width=True):
            if not username or not password:
                st.warning("⚠️ Please fill in all fields.")
            else:
                with st.spinner("Authenticating..."):
                    try:
                        if 'requests_session' not in st.session_state:
                            st.session_state['requests_session'] = requests.Session()
                        
                        session = st.session_state['requests_session']
                        payload = {"username": username, "password": password}
                        
                        # API Call
                        response = session.post(API_URL, json=payload)
                        
                        if response.status_code == 200:
                            data = response.json()
                            role = data.get("role", "user")
                            
                            st.success(f"Login successful! Redirecting...")
                            time.sleep(1)
                            
                            if role == "admin":
                                st.switch_page("pages/admin.py")
                            else:
                                st.switch_page("pages/dashboard.py")
                                
                        elif response.status_code == 401:
                            st.error("❌ Invalid credentials.")
                        else:
                            st.error(f"Error: {response.text}")
                            
                    except Exception as e:
                        st.error(f"Unable to reach the server. Check if it's running.")

    # Small discrete link at bottom of card
    st.markdown("""
        <div style="text-align: center; margin-top: 30px; opacity: 0.6; font-size: 0.9rem;">
            Protected by Scrypt encryption & HTTPS
        </div>
    """, unsafe_allow_html=True)