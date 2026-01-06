import streamlit as st
import pandas as pd
import requests
import time
from utils.styles import apply_premium_styles

# --- CONFIGURATION ---
st.set_page_config(
    page_title="Admin Panel - E-ComVision",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Apply Premium Styling & Animations
apply_premium_styles()

# API URLs
API_ADMIN_STATS = "http://127.0.0.1:5000/api/dashboard/admin/global-stats"
API_ADMIN_USERS = "http://127.0.0.1:5000/api/dashboard/admin/users-list"

# --- NAVBAR ---
nav_c1, nav_c2, nav_c3 = st.columns([2, 5, 2])
with nav_c1:
    st.markdown('<div class="nav-logo">🛡️ Admin Panel</div>', unsafe_allow_html=True)

with nav_c3:
    if st.button("🏠 Dashboard", use_container_width=True):
        st.switch_page("pages/dashboard.py")

st.markdown("<hr style='border: 0; height: 1px; background: rgba(255,255,255,0.1); margin-bottom: 30px;'>", unsafe_allow_html=True)

# --- ADMIN SECURITY ---
if 'requests_session' not in st.session_state:
    st.error("Login required.")
    st.stop()

# --- LOADING LOGIC ---
session = st.session_state['requests_session']
try:
    resp_stats = session.get(API_ADMIN_STATS)
    stats = resp_stats.json() if resp_stats.status_code == 200 else {}
    
    resp_users = session.get(API_ADMIN_USERS)
    users_df = pd.DataFrame(resp_users.json()) if resp_users.status_code == 200 else pd.DataFrame()
except:
    st.error("Server unreachable")
    st.stop()

# --- KPI SECTION ---
st.markdown("### 📊 System Status")
k1, k2, k3, k4 = st.columns(4)

with k1:
    with st.container(border=True):
        st.metric("Users", stats.get("total_users", 0))

with k2:
    with st.container(border=True):
        st.metric("Total Scans", stats.get("total_predictions", 0))

with k3:
    with st.container(border=True):
        # active_models derived from distribution length
        st.metric("AI Classes", len(stats.get("class_distribution", {})))

with k4:
    with st.container(border=True):
        st.metric("Uptime", "99.9%", "+0.1%")

st.write("")

# --- USER MANAGEMENT ---
with st.container(border=True):
    st.subheader("👥 User Account Management")
    if not users_df.empty:
        st.dataframe(
            users_df[['id', 'username', 'email', 'total_scans', 'role']],
            use_container_width=True,
            hide_index=True
        )
    else:
        st.info("No users found.")