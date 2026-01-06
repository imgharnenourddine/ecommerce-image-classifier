import streamlit as st
import streamlit.components.v1 as components

# Page Configuration
st.set_page_config(
    page_title="E-Commerce AI Classifier",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- MODERN CSS & ENLARGED BUTTONS ---
st.markdown("""
<style>
    /* Fonts: Inter */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;900&display=swap');

    /* Global Reset & Body */
    .stApp {
        background-color: #050505;
        background-image: 
            radial-gradient(at 0% 0%, rgba(5, 117, 230, 0.15) 0px, transparent 50%),
            radial-gradient(at 100% 0%, rgba(0, 242, 96, 0.1) 0px, transparent 50%);
        color: #ffffff;
    }

    /* --- MODIFICATION HERE: HIDING SIDEBAR --- */
    [data-testid="stSidebar"] {
        display: none;
    }
    
    /* Hide default Streamlit header */
    header[data-testid="stHeader"] {
        background-color: transparent !important;
        visibility: hidden;
    }
    
    /* Padding correction for navbar at the top */
    .block-container {
        padding-top: 1rem !important;
        overflow: visible !important;
    }

    /* Container for cards to avoid clipping */
    [data-testid="column"] {
        overflow: visible !important;
    }

    /* Style du Logo dans la Navbar */
    .nav-logo {
        font-family: 'Inter', sans-serif;
        font-weight: 900;
        font-size: 1.5rem;
        background: linear-gradient(90deg, #fff, #aaa);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: -1px;
        display: flex;
        align-items: center;
        height: 100%;
    }
    
    /* Global Glow Vignette */
    .stApp::after {
        content: "";
        position: fixed;
        top: 0; left: 0;
        width: 100%; height: 100%;
        background: radial-gradient(circle at 50% 120%, rgba(5, 117, 230, 0.1), transparent 50%);
        pointer-events: none;
        z-index: 0;
    }

    /* Headings */
    h1, h2, h3 {
        font-family: 'Inter', sans-serif;
        color: #ffffff;
    }
    
    h1 {
        font-weight: 900;
        font-size: 4rem !important;
        background: linear-gradient(180deg, #fff, #a5a5a5);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        line-height: 1.1;
    }

    h2 { font-size: 2.5rem; margin-bottom: 1rem; }

    /* Scroll Animation */
   

    /* Bento Card Styling */
    .bento-card {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 32px;
        padding: 40px;
        backdrop-filter: blur(20px);
        transition: transform 0.4s cubic-bezier(0.2, 0.8, 0.2, 1), box-shadow 0.4s ease;
        height: 100%;
        position: relative;
        overflow: visible;
        display: flex;
        flex-direction: column;
    }

    /* Border Beam / Stroke Animation */
    .bento-card::after {
        content: "";
        position: absolute;
        inset: 0;
        border-radius: 32px;
        padding: 2px; /* Stroke width increased */
        background: radial-gradient(circle at var(--mouse-x, 50%) var(--mouse-y, 50%), #0575e6 0%, #00f260 25%, #0575e6 50%, transparent 70%);
        -webkit-mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
        mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
        -webkit-mask-composite: xor;
        mask-composite: exclude;
        pointer-events: none;
        opacity: var(--stroke-opacity, 0);
        transition: opacity 0.3s ease;
    }

    /* Card Glow Effect (Pseudo-element before) */
    .bento-card::before {
        content: "";
        position: absolute;
        inset: -100px;
        background: radial-gradient(circle at var(--mouse-x, 50%) var(--mouse-y, 50%), rgba(5, 117, 230, 0.15) 0%, rgba(0, 242, 96, 0.09) 30%, transparent 60%);
        filter: blur(60px);
        opacity: var(--glow-opacity, 0);
        transition: opacity 0.3s ease;
        pointer-events: none;
        z-index: -1;
    }
    
    .bento-card:hover {
        transform: translateY(-5px) scale(1.01);
        box-shadow: 0 20px 40px rgba(0,0,0,0.4);
    }

    /* Metric Card */
    .metric-value {
        font-size: 3.5rem;
        font-weight: 800;
        background: linear-gradient(135deg, #00f260, #0575e6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .metric-label {
        color: #888;
        text-transform: uppercase;
        letter-spacing: 1px;
        font-size: 0.9rem;
    }

    .feature-icon {
        background: linear-gradient(135deg, #0575e6, #021b79);
        width: 60px; height: 60px;
        border-radius: 16px;
        display: flex; align-items: center; justify-content: center;
        font-size: 24px;
        margin-bottom: 24px;
        box-shadow: 0 10px 20px rgba(5, 117, 230, 0.3);
    }

    /* --- NOUVEAU STYLE DES BOUTONS (LARGE & PREMIUM - GLASSMORPHISM) --- */
    .stButton button {
        background: rgba(255, 255, 255, 0.04) !important;
        backdrop-filter: blur(16px) saturate(180%) !important;
        -webkit-backdrop-filter: blur(16px) saturate(180%) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        color: #ffffff !important;
        border-radius: 12px !important;
        padding: 16px 24px !important;
        font-weight: 700 !important;
        font-size: 18px !important;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275) !important;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
        width: 100%;
        position: relative;
        overflow: hidden;
    }
    
    .stButton button:hover {
        transform: translateY(-4px) scale(1.02);
        background: rgba(255, 255, 255, 0.08) !important;
        border-color: rgba(255, 255, 255, 0.3) !important;
        box-shadow: 
            0 15px 35px rgba(5, 117, 230, 0.5), 
            0 5px 15px rgba(0, 242, 96, 0.4),
            0 0 50px rgba(5, 117, 230, 0.3) !important;
        color: #ffffff !important;
    }

    .stButton button:active {
        transform: translateY(-1px) scale(0.98);
    }
    
    /* Boutons de la Navbar (Glassmorphism compact) */
    .nav-btn button {
        padding: 8px 20px !important;
        font-size: 14px !important;
        background: rgba(255,255,255,0.05) !important;
        backdrop-filter: blur(10px) !important;
        color: white !important;
        border: 1px solid rgba(255,255,255,0.15) !important;
        border-radius: 10px !important;
    }
    
    .nav-btn button:hover {
        background: rgba(255,255,255,0.12) !important;
        border-color: rgba(255,255,255,0.4) !important;
        box-shadow: 0 0 20px rgba(5, 117, 230, 0.4) !important;
    }


    /* Footer */
    .footer-section {
        border-top: 1px solid rgba(255,255,255,0.1);
        padding-top: 50px;
        margin-top: 100px;
        color: #666;
    }
    /* Workflow Line Animation */
    .workflow-line {
        flex: 1;
        min-width: 30px;
        height: 2px;
        background: linear-gradient(90deg, 
            rgba(255, 255, 255, 0.1) 0%, 
            #0575e6 50%, 
            rgba(255, 255, 255, 0.1) 100%
        );
        background-size: 200% 100%;
        margin: 0 15px;
        position: relative;
        align-self: center;
        animation: workflow-flow 2s linear infinite;
        border-radius: 1px;
    }

    @keyframes workflow-flow {
        0% { background-position: 200% 0; }
        100% { background-position: 0% 0; }
    }
    /* Tech Stack Badges */
    .tech-badge {
        padding: 8px 16px;
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 20px;
        font-size: 0.85rem;
        transition: all 0.3s ease;
        cursor: default;
    }
    .tech-badge:hover {
        background: rgba(255, 255, 255, 0.1);
        border-color: #0575e6;
        transform: translateY(-2px);
    }

    /* Chart Bar Animation */
    .chart-bar {
        width: 20%;
        border-radius: 4px;
        transition: height 1s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    }
    .active .chart-bar {
        height: var(--bar-height) !important;
    }

    /* Float Animation */
    @keyframes float {
        0% { transform: translateY(0px); }
        50% { transform: translateY(-20px); }
        100% { transform: translateY(0px); }
    }

    /* Status Pulse */
    @keyframes pulse {
        0% { opacity: 1; }
        50% { opacity: 0.4; }
        100% { opacity: 1; }
    }
    .status-dot {
        animation: pulse 2s infinite;
    }

    /* Hide Streamlit Chrome */
    #MainMenu, header, footer {visibility: hidden;}

</style>
""", unsafe_allow_html=True)

# JavaScript for global mouse-tracking & robust init
components.html("""
<script>
(function() {
    let globalMouseX = 0;
    let globalMouseY = 0;
    let cards = [];
    
    function findCards() {
        try {
            const parentDoc = window.parent.document;
            cards = parentDoc.querySelectorAll('.bento-card');
            return cards.length > 0;
        } catch (e) {
            console.error("Access to parent document denied or failed:", e);
            return false;
        }
    }
    
    function updateGlow() {
        cards.forEach(card => {
            const rect = card.getBoundingClientRect();
            const xPercent = ((globalMouseX - rect.left) / rect.width) * 100;
            const yPercent = ((globalMouseY - rect.top) / rect.height) * 100;
            
            const cardCenterX = rect.left + rect.width / 2;
            const cardCenterY = rect.top + rect.height / 2;
            const distance = Math.sqrt(Math.pow(globalMouseX - cardCenterX, 2) + Math.pow(globalMouseY - cardCenterY, 2));
            
            const maxDistance = 600;
            const glowOpacity = Math.max(0, 1 - (distance / maxDistance));
            const strokeOpacity = Math.max(0, 1 - (distance / (maxDistance * 0.75)));
            
            card.style.setProperty('--mouse-x', xPercent + '%');
            card.style.setProperty('--mouse-y', yPercent + '%');
            card.style.setProperty('--glow-opacity', glowOpacity.toFixed(2));
            card.style.setProperty('--stroke-opacity', strokeOpacity.toFixed(2));
        });
    }

    function init() {
        const hasCards = findCards();
        const parentDoc = window.parent.document;
        
        parentDoc.addEventListener('mousemove', function(e) {
            globalMouseX = e.clientX;
            globalMouseY = e.clientY;
            updateGlow();
        });

        // Scroll animations init
        const observerOptions = { threshold: 0.1, rootMargin: '0px 0px -50px 0px' };
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) entry.target.classList.add('active');
            });
        }, observerOptions);

        const animatedElements = parentDoc.querySelectorAll('.animate-on-scroll');
        animatedElements.forEach(el => observer.observe(el));
    }
    
    // Initial wait to ensure parent DOM is ready
    if (document.readyState === 'complete') {
        setTimeout(init, 500);
    } else {
        window.addEventListener('load', () => setTimeout(init, 500));
    }
    
    // Fallback polling for dynamically rendered content
    let attempts = 0;
    const pollInterval = setInterval(() => {
        if (findCards() || attempts > 10) clearInterval(pollInterval);
        attempts++;
    }, 1000);
})();
</script>
""", height=0)

# --- NAVBAR SECTION (ADDED) ---
# Create 3 columns: Logo left, Space middle, Buttons right
nav_c1, nav_c2, nav_c3 = st.columns([2, 6, 2])

with nav_c1:
    st.markdown('<div class="nav-logo">⚡ E-ComVision</div>', unsafe_allow_html=True)

with nav_c3:
    # Sub-columns for Login and Sign Up buttons
    b1, b2 = st.columns(2)
    with b1:
        st.markdown('<div class="nav-btn">', unsafe_allow_html=True)
        if st.button("Log In", use_container_width=True):
            st.switch_page("pages/login.py")
        st.markdown('</div>', unsafe_allow_html=True)
    with b2:
        st.markdown('<div class="nav-btn">', unsafe_allow_html=True)
        if st.button("Sign Up", use_container_width=True):
            st.switch_page("pages/register.py")
        st.markdown('</div>', unsafe_allow_html=True)

# Subtle separation line
st.markdown("<hr style='border: 0; height: 1px; background-image: linear-gradient(to right, rgba(0, 0, 0, 0), rgba(255, 255, 255, 0.1), rgba(0, 0, 0, 0)); margin-bottom: 30px;'>", unsafe_allow_html=True)


# --- Hero Section (ORIGINAL - UNMODIFIED) ---
c1, c2 = st.columns([1.2, 1], gap="large")

with c1:
    st.markdown('<div class="animate-on-scroll" style="margin-top: 60px;">', unsafe_allow_html=True)
    st.markdown("<h1>E-Commerce <br> Intelligence .<br><span style='font-size: 0.5em; opacity: 1; color: #888; font-weight: 400;'>Automated Recognition</span></h1>", unsafe_allow_html=True)
    st.markdown('<p class="desc-text" style="color: #ccc; font-size: 1.2rem; margin: 30px 0; line-height: 1.6;">Leverage our enterprise-grade computer vision pipeline to automate product tagging, defect detection, and catalog organization. Built for high-volume e-commerce operations.</p>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # --- ACTION BUTTONS (MODIFIED) ---
    st.write("") 
    
    # Aligned main buttons
    btn_col1, btn_col2 = st.columns([1, 1], gap="medium")

    with btn_col1:
        # Redirect to Login to start
        if st.button("🚀 Let's Predict", type="primary", use_container_width=True):
            st.switch_page("pages/login.py")

    with btn_col2:
        # Redirect to Login (security) for admins
        if st.button("🛡️ Admin Portal", use_container_width=True):
            st.switch_page("pages/login.py")

    st.write("") # Vertical space
    
    # Account Creation Section
    st.markdown('<div class="animate-on-scroll" style="margin-top: 20px;">', unsafe_allow_html=True)
    st.caption("Don't have an account?")
    if st.button("✨ Create Free Account", use_container_width=True):
        st.switch_page("pages/register.py")
    st.markdown('</div>', unsafe_allow_html=True)


with c2:
    st.markdown('<div class="animate-on-scroll" style="margin-top: 50px; display: flex; justify-content: center;">', unsafe_allow_html=True)
    st.html("""
        <div style="width: 100%; height: 450px; position: relative;">
            <div style="
                position: absolute; top: 0; left: 5%; width: 90%; height: 100%;
                background: #0f0f0f; border: 1px solid #333; border-radius: 20px;
                box-shadow: 0 50px 100px rgba(0,0,0,0.8);
                overflow: hidden;
            ">
                <div style="height: 50px; border-bottom: 1px solid #333; display: flex; align-items: center; padding: 0 20px;">
                    <div style="width: 12px; height: 12px; background: #ff5f56; border-radius: 50%; margin-right: 8px;"></div>
                    <div style="width: 12px; height: 12px; background: #ffbd2e; border-radius: 50%; margin-right: 8px;"></div>
                    <div style="width: 12px; height: 12px; background: #27c93f; border-radius: 50%;"></div>
                </div>
                <div style="padding: 20px;">
                    <div style="width: 60%; height: 20px; background: #333; border-radius: 4px; margin-bottom: 10px;"></div>
                    <div style="width: 40%; height: 20px; background: #222; border-radius: 4px; margin-bottom: 30px;"></div>
                    
                    <div style="display: flex; gap: 10px;">
                        <div style="flex: 1; height: 150px; background: linear-gradient(180deg, rgba(5,117,230,0.1), transparent); border: 1px solid #333; border-radius: 8px;"></div>
                        <div style="flex: 1; height: 150px; background: linear-gradient(180deg, rgba(0,242,96,0.1), transparent); border: 1px solid #333; border-radius: 8px;"></div>
                    </div>
                </div>
            </div>
            <div style="
                position: absolute; bottom: 50px; right: 0; width: 200px; padding: 20px;
                background: rgba(15,15,15,0.9); border: 1px solid #00f260; border-radius: 16px;
                backdrop-filter: blur(10px);
                box-shadow: 0 20px 40px rgba(0,0,0,0.5);
                animation: float 6s ease-in-out infinite;
            ">
                <div style="font-size: 0.8rem; color: #888;">System Status</div>
                <div style="font-size: 1.2rem; color: #00f260; font-weight: bold;">
                    <span class="status-dot">●</span> Active
                </div>
                <div style="font-size: 0.8rem; color: #666; margin-top: 5px;">Latency: 45ms</div>
            </div>
        </div>
        <style>@keyframes float { 0% {transform: translateY(0px);} 50% {transform: translateY(-20px);} 100% {transform: translateY(0px);} }</style>
    """)
    st.markdown('</div>', unsafe_allow_html=True)

# --- Stats Section ---
st.markdown('<div class="animate-on-scroll" style="margin: 100px 0;">', unsafe_allow_html=True)
col1, col2, col3 = st.columns(3)
stats = [
    {"value": "99.8%", "label": "Accuracy Rate"},
    {"value": "<50ms", "label": "Processing Time"},
    {"value": "10k+", "label": "Images Analyzed"}
]
for i, stat in enumerate(stats):
    with [col1, col2, col3][i]:
        st.markdown(f"""
        <div style="text-align: center; border-left: 1px solid #333;">
            <div class="metric-value">{stat['value']}</div>
            <div class="metric-label">{stat['label']}</div>
        </div>
        """, unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# --- Bento Grid Features ---
st.markdown('<div class="animate-on-scroll"><h2>Platform Capabilities</h2></div>', unsafe_allow_html=True)
st.write("")

# Row 1
r1c1, r1c2, r1c3 = st.columns([1.5, 1, 1])

with r1c1:
    st.markdown("""
    <div class="animate-on-scroll h-full">
        <div class="bento-card">
            <div class="feature-icon">🔍</div>
            <h3>Advanced Recognition</h3>
            <p style="color: #aaa; margin-top: 10px; line-height: 1.6;">Our proprietary ensemble models combine Convolutional Neural Networks (CNNs) and Vision Transformers (ViTs) to achieve human-level understanding.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

with r1c2:
    st.markdown("""
    <div class="animate-on-scroll h-full">
        <div class="bento-card">
            <div class="feature-icon" style="background: linear-gradient(135deg, #00f260, #0575e6);">📂</div>
            <h3>Export Data</h3>
            <p style="color: #aaa; line-height: 1.6;">Integrate directly with your existing PIM or ERP systems. We support real-time webhooks and RESTful API endpoints.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

with r1c3:
    st.markdown("""
    <div class="animate-on-scroll h-full">
        <div class="bento-card">
            <h3>Visual Dashboards</h3>
            <div style="margin-top: 20px; height: 60px; display: flex; align-items: flex-end; gap: 5px;">
                <div class="chart-bar" style="height: 10%; background: #333; --bar-height: 40%;"></div>
                <div class="chart-bar" style="height: 10%; background: #0575e6; --bar-height: 70%;"></div>
                <div class="chart-bar" style="height: 10%; background: #00f260; --bar-height: 50%;"></div>
                <div class="chart-bar" style="height: 10%; background: #333; --bar-height: 90%;"></div>
            </div>
            <p style="color: #aaa; margin-top: 15px; line-height: 1.6;">Gain deep visibility into your catalog's health with our interactive analytics suite.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

st.write("")

# Row 2 (Workflow)
r2c1, r2c2 = st.columns([1, 2], gap="medium")

with r2c1:
    st.markdown("""
    <div class="animate-on-scroll h-full">
        <div class="bento-card">
            <div class="feature-icon" style="background: linear-gradient(135deg, #667eea, #764ba2);">🛠️</div>
            <h3>Tech Stack</h3>
             <p style="color: #aaa; margin: 10px 0; font-size: 0.9rem; line-height: 1.5;">Built on a rock-solid foundation.</p>
            <div style="display: flex; flex-wrap: wrap; gap: 10px; margin-top: 20px;">
                <span class="tech-badge">TensorFlow</span>
                <span class="tech-badge">Python</span>
                <span class="tech-badge">Streamlit</span>
                <span class="tech-badge">Pandas</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

with r2c2:
    st.markdown("""
    <div class="animate-on-scroll">
        <div class="bento-card">
            <h3>How It Works</h3>
            <div style="display: flex; align-items: center; justify-content: space-between; margin-top: 30px;">
                <div style="text-align: center;">
                    <div style="background: rgba(255,255,255,0.1); width: 50px; height: 50px; border-radius: 50%; display: flex; align-items: center; justify-content: center; margin: auto;">1</div>
                    <p style="font-size: 0.8rem; margin-top: 10px; font-weight: bold;">Upload</p>
                </div>
                <div class="workflow-line"></div>
                <div style="text-align: center;">
                    <div style="background: rgba(5,117,230,0.2); border: 1px solid #0575e6; width: 50px; height: 50px; border-radius: 50%; display: flex; align-items: center; justify-content: center; margin: auto;">2</div>
                    <p style="font-size: 0.8rem; margin-top: 10px; font-weight: bold;">Process</p>
                </div>
                <div class="workflow-line"></div>
                <div style="text-align: center;">
                    <div style="background: rgba(0,242,96,0.2); width: 50px; height: 50px; border-radius: 50%; display: flex; align-items: center; justify-content: center; margin: auto;">3</div>
                    <p style="font-size: 0.8rem; margin-top: 10px; font-weight: bold;">Result</p>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# --- Footer ---
st.markdown("""
<div class="footer-section animate-on-scroll">
    <div style="display: flex; justify-content: space-between; align-items: center;">
        <div>
            <h3 style="margin:0;">E-Commerce Intelligence</h3>
            <p style="font-size: 0.8rem; opacity: 0.5;">© 2026 Solutions. All rights reserved.</p>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)