import streamlit as st
import requests
import time
import io
from streamlit_cropper import st_cropper
from utils.styles import apply_premium_styles

# --- CONFIGURATION ---
st.set_page_config(
    page_title="AI Predictor - E-Commerce Intelligence",
    page_icon="🔮",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Apply Premium Styling & Animations
apply_premium_styles()

# URLs API
API_PREDICT = "http://127.0.0.1:5000/api/predict"
API_LOGOUT = "http://127.0.0.1:5000/api/logout"

# --- SECURITY ---
if 'requests_session' not in st.session_state:
    st.warning("🔒 You must be logged in to access the AI.")
    time.sleep(2)
    st.switch_page("pages/login.py")

# Temporary list for multi-objects
if 'temp_list' not in st.session_state:
    st.session_state['temp_list'] = []

# --- NAV BAR ---
nav_c1, nav_c2, nav_c3 = st.columns([2.5, 4.5, 3]) 
with nav_c1:
    st.markdown('<div class="nav-logo">🔮 AI Predictor</div>', unsafe_allow_html=True)

with nav_c3:
    b1, b2 = st.columns(2)
    with b1:
        if st.button("📊 Dashboard", use_container_width=True):
            st.switch_page("pages/dashboard.py")
    with b2:
        st.markdown('<div class="logout-btn">', unsafe_allow_html=True)
        if st.button("Logout", use_container_width=True):
            try: st.session_state['requests_session'].post(API_LOGOUT)
            except: pass
            st.session_state.clear()
            st.switch_page("pages/login.py")
        st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<hr style='border: 0; height: 1px; background: rgba(255,255,255,0.1); margin-bottom: 30px;'>", unsafe_allow_html=True)

# --- MAIN SECTION ---
col_left, col_right = st.columns([1.5, 1], gap="large")

with col_left:
    with st.container(border=True):
        st.subheader("📸 Image Source")
        uploaded_file = st.file_uploader("", type=["jpg", "png", "jpeg"], label_visibility="collapsed")
        
        if uploaded_file:
            from PIL import Image as PILImage
            if st.session_state.get('last_fn') != uploaded_file.name:
                st.session_state.temp_list = []
                st.session_state.last_fn = uploaded_file.name

            img_raw = PILImage.open(uploaded_file)
            
            # --- FIX IMAGE SIZE ---
            target_w = 800
            ratio = target_w / float(img_raw.size[0])
            img_disp = img_raw.resize((target_w, int(img_raw.size[1] * ratio)), PILImage.Resampling.LANCZOS)
            
            st.info("💡 Frame an object and click 'Analyze this zone'")
            
            crop = st_cropper(img_disp, realtime_update=True, box_color='#00f260', aspect_ratio=None)
            
            if st.button("Start Zone Analysis 🚀", type="primary"):
                with st.spinner("AI is analyzing the zone..."):
                    buf = io.BytesIO()
                    crop.save(buf, format="JPEG")
                    files = {'file': ('crop.jpg', buf.getvalue(), 'image/jpeg')}
                    
                    res = st.session_state['requests_session'].post(f"{API_PREDICT}?mode=temp", files=files)
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
        st.subheader("🎯 Analysis Results")
        
        if not st.session_state.temp_list:
            st.markdown("""
            <div style="text-align: center; padding-top: 50px; opacity: 0.5;">
                <h3>Waiting for analysis...</h3>
                <p>Frame an object on the left and analyze it.</p>
                <div style="font-size: 4rem; margin-top: 20px;">📊</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            for item in st.session_state.temp_list:
                res_c1, res_c2 = st.columns([1, 3])
                res_c1.image(item['crop'], use_container_width=True)
                
                label = item['label']
                conf = item['conf']
                display_conf = conf * 100 if conf <= 1.0 else conf
                
                with res_c2:
                    st.markdown(f'<div style="font-size:1.2rem; font-weight:700; color:#00f260;">{label}</div>', unsafe_allow_html=True)
                    st.markdown(f"<p style='color: #aaa; margin-bottom:0;'>Confidence: <b>{display_conf:.2f}%</b></p>", unsafe_allow_html=True)
                    st.progress(min(float(conf if conf <= 1.0 else conf/100), 1.0))
                st.divider()
            
            if st.button("✅ Save Total Analysis", use_container_width=True):
                unique = {}
                for x in st.session_state.temp_list:
                    if x['label'] not in unique or x['conf'] > unique[x['label']]['s']:
                        unique[x['label']] = {'s': x['conf'], 't': f"{x['conf']*100:.1f}%"}
                
                f_labels = ", ".join(unique.keys())
                f_confs = ", ".join([v['t'] for v in unique.values()])
                
                uploaded_file.seek(0)
                files = {'file': (uploaded_file.name, uploaded_file.read(), uploaded_file.type)}
                payload = {"final_labels": f_labels, "final_confs": f_confs}
                
                resp = st.session_state['requests_session'].post(f"{API_PREDICT}?mode=final", files=files, data=payload)
                if resp.status_code == 200:
                    st.session_state.temp_list = []
                    st.success("Saved successfully!")
                    time.sleep(1)
                    st.switch_page("pages/dashboard.py")

    if st.button("🗑️ Reset All", key="reset", use_container_width=True):
        st.session_state.temp_list = []
        st.rerun()
