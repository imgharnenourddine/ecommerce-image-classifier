import streamlit as st
import time

st.set_page_config(page_title="Register - E-Commerce Intelligence", page_icon="📝", layout="centered")

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
        background: linear-gradient(135deg, #00f260, #0575e6);
        color: white !important;
        border: none;
        width: 100%;
        padding: 0.5rem;
        transition: transform 0.2s, box-shadow 0.2s;
    }
    
    .stButton button:hover {
        transform: scale(1.02);
        box-shadow: 0 0 20px rgba(0, 242, 96, 0.6);
    }
    
    /* Make labels white */
    .stTextInput label {
        color: #ffffff !important;
    }
</style>
""", unsafe_allow_html=True)

st.title("Create Account")
st.markdown("Join the platform to start analyzing your catalog.")

email = st.text_input("Email Address", placeholder="Enter your email")
username = st.text_input("Username", placeholder="Choose a username")
password = st.text_input("Password", type="password", placeholder="Create a password")
confirm_password = st.text_input("Confirm Password", type="password", placeholder="Re-enter your password")

if st.button("Sign Up"):
    with st.spinner("Creating account..."):
        time.sleep(1)
        if password != confirm_password:
            st.error("Passwords do not match.")
        elif email and username and password:
            st.success("Account created successfully!")
            time.sleep(1)
            st.switch_page("pages/login.py")
        else:
            st.error("Please fill in all fields.")

st.markdown("---")
st.markdown("Already have an account?")
if st.button("Log In", type="secondary"):
    st.switch_page("pages/login.py")
