import streamlit as st
import pandas as pd
import requests
import time
from utils.styles import apply_premium_styles

# --- CONFIGURATION ---
st.set_page_config(
    page_title="Dashboard - E-Commerce Intelligence",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Apply Premium Styling & Animations
apply_premium_styles()

# URLs API
API_BASE = "http://127.0.0.1:5000/api/dashboard"
API_STATS = f"{API_BASE}/user/stats"
API_HISTORY = f"{API_BASE}/user/history"
API_LOGOUT = "http://127.0.0.1:5000/api/auth/logout"

# --- SÉCURITÉ ---
if 'requests_session' not in st.session_state:
    st.warning("🔒 You must be logged in to access the Dashboard.")
    time.sleep(2)
    st.switch_page("pages/login.py")

# --- NAVBAR ---
nav_c1, nav_c2, nav_c3 = st.columns([2, 5, 2])
with nav_c1:
    st.markdown('<div class="nav-logo">📊 Dashboard</div>', unsafe_allow_html=True)

with nav_c3:
    b1, b2 = st.columns(2)
    with b1:
        if st.button("Predict", use_container_width=True):
            st.switch_page("pages/predictions.py")
    with b2:
        if st.button("Logout", use_container_width=True):
            try: st.session_state['requests_session'].get(API_LOGOUT)
            except: pass
            del st.session_state['requests_session']
            st.switch_page("pages/login.py")

st.markdown("<hr style='border: 0; height: 1px; background: rgba(255,255,255,0.1); margin-bottom: 30px;'>", unsafe_allow_html=True)

# --- API LOGIC ---
session = st.session_state['requests_session']
try:
    resp_stats = session.get(API_STATS)
    stats = resp_stats.json() if resp_stats.status_code == 200 else {}
    resp_history = session.get(API_HISTORY)
    df = pd.DataFrame(resp_history.json()) if resp_history.status_code == 200 else pd.DataFrame()
except:
    st.error("❌ Server unreachable")
    st.stop()

st.title(f"Hello, {stats.get('username', 'User')}")

# --- METRICS ---
m1, m2, m3 = st.columns(3)
with m1:
    with st.container(border=True):
        st.metric("Total Scans", stats.get("total_scans", 0))

with m2:
    with st.container(border=True):
        raw_conf = stats.get('avg_confidence', 0)
        display_conf = raw_conf * 100 if raw_conf <= 1.0 else raw_conf
        st.metric("Average Confidence", f"{display_conf:.2f}%")

with m3:
    with st.container(border=True):
        st.metric("Top Category", stats.get("top_category", "None"))

st.write("")

# --- HISTORY AND VISUALIZATION ---
col_table, col_viz = st.columns([1.8, 1], gap="medium")
with col_table:
    with st.container(border=True):
        st.subheader("📑 Prediction History")
        if not df.empty:
            df_display = df.copy()
            df_display['preview'] = df_display['image_path'].apply(
                lambda x: f"http://127.0.0.1:5000/uploads/{x}" if x else None
            )
            df_display['confidence'] = df_display['confidence'].apply(
                lambda x: f"{x*100:.1f}%" if x <= 1.0 else f"{x:.1f}%"
            )
            st.dataframe(
                df_display[['date', 'preview', 'category', 'confidence', 'status']],
                column_config={
                    "preview": st.column_config.ImageColumn("Preview", width="small"),
                    "date": "Analysis Date",
                    "category": "Product",
                    "confidence": "Confidence",
                    "status": "Status"
                },
                use_container_width=True,
                hide_index=True
            )
        else:
            st.info("No history available.")

with col_viz:
    with st.container(border=True):
        st.subheader("📈 Distribution by Category")
        if not df.empty:
            st.bar_chart(df['category'].value_counts(), color="#0575e6")
        else:
            st.info("Visualization not available.")