import streamlit as st
import time

st.set_page_config(page_title="Login - E-Commerce Intelligence", page_icon="🔒", layout="centered")

# Styling (reusing some bits for consistency)
st.markdown("""
<style>
    @keyframes gradientMove {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    .stApp {
        background-color: #000000;
        /* Animated Deep Blue Gradient */
        background-image: radial-gradient(circle at center, #0a1033 0%, #000000 100%);
        background-size: 200% 200%;
        animation: gradientMove 15s ease infinite;
        color: white;
    }

    [data-testid="stSidebar"] {
        background-color: #353942 !important;
        border-right: 1px solid rgba(255,255,255,0.1);
    }

    header[data-testid="stHeader"] {
        background-color: rgba(0,0,0,0) !important;
    }
    
    .stTextInput > div > div > input {
        background-color: #1a1a1a;
        color: white;
        border: 1px solid #333;
        transition: all 0.3s ease;
    }
    
    .stTextInput > div > div > input:hover {
        border-color: #0575e6;
        background-color: #222;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #0575e6;
        box-shadow: 0 0 15px rgba(5, 117, 230, 0.5);
    }

    .stButton button {
        background: linear-gradient(135deg, #0575e6, #021b79);
        color: white !important;
        border: none;
        width: 100%;
        padding: 0.5rem;
        transition: transform 0.2s, box-shadow 0.2s;
    }
    
    .stButton button:hover {
        transform: scale(1.02);
        box-shadow: 0 0 20px rgba(5, 117, 230, 0.6);
    }
    
    /* Make lEmailite */
    .stTextInput label {
        color: #ffffff !important;
    }
</style>
""", unsafe_allow_html=True)

st.title("Welcome Back")
st.markdown("Enter your credentials to access the dashboard.")

username = st.text_input("Email", placeholder="Enter your email")
password = st.text_input("Password", type="password", placeholder="Enter your password")

if st.button("Log In"):
    with st.spinner("Authenticating..."):
        time.sleep(1) # Simulate API call
        if username and password:
            st.success("Login successful!")
            time.sleep(0.5)
            st.switch_page("pages/dashboard.py")
        else:
            st.error("Please fill in all fields.")

st.markdown("---")
st.markdown("Don't have an account?")
if st.button("Create Account", type="secondary"):
    st.switch_page("pages/register.py")
