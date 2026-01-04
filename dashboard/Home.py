import streamlit as st
import streamlit.components.v1 as components
import random

# Page Configuration
st.set_page_config(
    page_title="E-Commerce AI Classifier",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS Injection
st.markdown("""
<style>
    /* Fonts: Inter for that clean SaaS look */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;900&display=swap');

    /* Global Reset & Body */
    .stApp {
        background-color: #050505;
        background-image: 
            radial-gradient(at 0% 0%, rgba(5, 117, 230, 0.15) 0px, transparent 50%),
            radial-gradient(at 100% 0%, rgba(0, 242, 96, 0.1) 0px, transparent 50%);
        color: #ffffff;
        
    }

     [data-testid="stSidebar"] {
        background-color: #353942 !important;
        border-right: 1px solid rgba(255,255,255,0.1);
    }
    header[data-testid="stHeader"] {
        background-color: rgba(0,0,0,0) !important;
    }
    
    /* Global Glow Vignette (Dayos Style) */
    .stApp::after {
        content: "";
        position: fixed;
        top: 0; left: 0;
        width: 100%; height: 100%;
        background: radial-gradient(circle at 50% 120%, rgba(5, 117, 230, 0.1), transparent 70%);
        pointer-events: none;
        z-index: 0;
    }

    /* Headings */
    h1, h2, h3 {
        font-family: 'Inter', sans-serif;
        letter-spacing: -0.03em; /* Tight kerning like Dayos */
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

    h2 {
        font-size: 2.5rem;
        margin-bottom: 1rem;
    }

    /* Scroll Animation Utility */
    .animate-on-scroll {
        opacity: 0;
        transform: translateY(30px);
        transition: opacity 0.8s ease-out, transform 0.8s ease-out;
    }
    
    .animate-on-scroll.active {
        opacity: 1;
        transform: translateY(0);
    }

    /* Bento Grid Card */
    .bento-card {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 32px;
        padding: 40px;
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        transition: transform 0.4s cubic-bezier(0.2, 0.8, 0.2, 1), box-shadow 0.4s ease;
        height: 100%;
        position: relative;
        overflow: visible; /* Changed to visible to allow blur to extend outside */
        display: flex;
        flex-direction: column;
    }

    /* Blurred blob light background effect */
    .bento-card::before {
        content: "";
        position: absolute;
        inset: -100px; /* Extend beyond card boundaries */
        background: radial-gradient(
            circle at var(--mouse-x, 50%) var(--mouse-y, 50%),
            rgba(5, 117, 230, 0.15) 0%,
            rgba(0, 242, 96, 0.09) 30%,
            transparent 60%
        );
        filter: blur(60px);
        opacity: calc(var(--glow-opacity, 0) * 1.0); /* Use proximity-based opacity - increased visibility */
        transition: opacity 0.3s ease;
        pointer-events: none;
        z-index: -1;
    }

    .bento-card-wide {
        grid-column: span 2;
    }

    /* Blob elements for mouse tracking */
    .blob {
        position: absolute;
        z-index: 1;
        top: 0;
        left: 0;
        width: 300px;
        height: 300px;
        border-radius: 50%;
        background: radial-gradient(
            circle,
            rgba(5, 117, 230, 0.6) 0%,
            rgba(0, 242, 96, 0.3) 40%,
            transparent 70%
        );
        opacity: calc(var(--glow-opacity, 0) * 1); /* Use proximity-based opacity */
        pointer-events: none;
        transform: translate(-50%, -50%);
        filter: blur(40px);
        transition: opacity 0.3s ease;
    }

    .fakeblob {
        display: block;
        position: absolute;
        z-index: -1;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        border-radius: 32px;
        opacity: 0;
        pointer-events: none;
    }

    /* Dynamic border glow that follows mouse */
    .bento-card::after {
        content: "";
        position: absolute;
        inset: 0;
        border-radius: 32px;
        padding: 1px; /* Minimized stroke */
        background: radial-gradient(
            500px circle at var(--mouse-x, 50%) var(--mouse-y, 50%),
            rgba(5, 117, 230, 1.0) 0%,
            rgba(0, 242, 96, 1.0) 40%,
            transparent 70%
        );
        -webkit-mask: 
            linear-gradient(#fff 0 0) content-box, 
            linear-gradient(#fff 0 0);
        -webkit-mask-composite: xor;
        mask-composite: exclude;
        opacity: calc(var(--glow-opacity, 0) * 1.5);
        filter: drop-shadow(0 0 8px rgba(0, 242, 96, 0.8)); /* Subtle bloom for fine line */
        transition: opacity 0.3s ease;
        pointer-events: none;
        z-index: 2;
    }

    .bento-card:hover {
        transform: translateY(-5px) scale(1.01);
        box-shadow: 0 20px 40px rgba(0,0,0,0.4);
    }

    /* Metric Card Special */
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

    /* Feature Icon */
    .feature-icon {
        background: linear-gradient(135deg, #0575e6, #021b79);
        width: 60px; height: 60px;
        border-radius: 16px;
        display: flex; align-items: center; justify-content: center;
        font-size: 24px;
        margin-bottom: 24px;
        box-shadow: 0 10px 20px rgba(5, 117, 230, 0.3);
    }

    /* Workflow Viz */
    .workflow-step {
        display: flex; align-items: center;
    }
    .workflow-line {
        flex-grow: 1; height: 2px; background: #333; margin: 0 15px; position: relative;
        overflow: hidden; /* Prevent animation overflow */
    }
    .workflow-line::after {
        content: ""; position: absolute; left: -50%; top: 0; height: 100%; width: 50%;
        background: linear-gradient(90deg, transparent, #0575e6, transparent);
        animation: activeLine 3s infinite linear;
    }
    @keyframes activeLine { 
        0% { left: -50%; } 
        100% { left: 150%; } 
    }

    /* Buttons */
    .stButton button {
        background: #ffffff !important;
        color: #000000 !important;
        border: none !important;
        border-radius: 99px !important;
        padding: 12px 32px !important;
        font-weight: 600 !important;
        font-size: 16px !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 0 20px rgba(255,255,255,0.1);
    }
    
    .stButton button:hover {
        transform: scale(1.05);
        box-shadow: 0 0 30px rgba(255,255,255,0.3);
    }
    
    /* Footer */
    .footer-section {
        border-top: 1px solid rgba(255,255,255,0.1);
        padding-top: 50px;
        margin-top: 100px;
        color: #666;
    }

    /* HTML Nav Buttons */
    .nav-button {
        display: inline-block;
        background: #ffffff !important;
        color: #000000 !important;
        border-radius: 99px !important;
        padding: 12px 32px !important;
        font-weight: 600 !important;
        font-size: 16px !important;
        text-decoration: none !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 0 20px rgba(255,255,255,0.1);
        margin-bottom: 10px;
    }
    
    .nav-button:hover {
        transform: scale(1.05);
        box-shadow: 0 0 30px rgba(255,255,255,0.3);
        color: #000 !important;
    }

    .nav-button-secondary {
        display: inline-block;
        background: rgba(255,255,255,0.1) !important;
        color: #ffffff !important;
        border: 1px solid rgba(255,255,255,0.2) !important;
        border-radius: 99px !important;
        padding: 8px 24px !important;
        font-weight: 500 !important;
        font-size: 0.9rem !important;
        text-decoration: none !important;
        transition: all 0.3s ease !important;
    }

    .nav-button-secondary:hover {
        background: rgba(255,255,255,0.2) !important;
        transform: scale(1.05);
    }

    /* Hide Streamlit Chrome */
    #MainMenu, header, footer {visibility: hidden;}
    .block-container {padding-top: 2rem;}

</style>
""", unsafe_allow_html=True)

# JavaScript for global mouse-tracking with proximity-based glow
components.html("""
<script>
(function() {
    let globalMouseX = 0;
    let globalMouseY = 0;
    
    function initProximityGlow() {
        const parentDoc = window.parent.document;
        const cards = parentDoc.querySelectorAll('.bento-card');
        
        // Track global mouse position
        parentDoc.addEventListener('mousemove', function(e) {
            globalMouseX = e.clientX;
            globalMouseY = e.clientY;
            
            // Update all cards based on proximity
            cards.forEach(card => {
                const rect = card.getBoundingClientRect();
                
                // Calculate local mouse position relative to card
                const localX = globalMouseX - rect.left;
                const localY = globalMouseY - rect.top;
                
                // Convert to percentage
                const xPercent = (localX / rect.width) * 100;
                const yPercent = (localY / rect.height) * 100;
                
                // Calculate distance from mouse to card center
                const cardCenterX = rect.left + rect.width / 2;
                const cardCenterY = rect.top + rect.height / 2;
                const distance = Math.sqrt(
                    Math.pow(globalMouseX - cardCenterX, 2) + 
                    Math.pow(globalMouseY - cardCenterY, 2)
                );
                
                // Calculate opacity based on distance (closer = brighter)
                // Max distance for effect: 400px
                const maxDistance = 400;
                const opacity = Math.max(0, 1 - (distance / maxDistance));
                
                // Update CSS variables
                card.style.setProperty('--mouse-x', xPercent + '%');
                card.style.setProperty('--mouse-y', yPercent + '%');
                card.style.setProperty('--glow-opacity', opacity);
            });
        });
    }
    
    function initScrollAnimations() {
        const parentDoc = window.parent.document;
        const observerOptions = {
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px'
        };

        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('active');
                }
            });
        }, observerOptions);

        const animatedElements = parentDoc.querySelectorAll('.animate-on-scroll');
        animatedElements.forEach(el => observer.observe(el));
    }
    
    // Initialize immediately
    initProximityGlow();
    initScrollAnimations();
    
    // Re-initialize after delays to catch dynamic content
    setTimeout(() => { initProximityGlow(); initScrollAnimations(); }, 500);
    setTimeout(() => { initProximityGlow(); initScrollAnimations(); }, 1000);
    setTimeout(() => { initProximityGlow(); initScrollAnimations(); }, 2000);
})();
</script>
""", height=0)

# --- Hero Section ---
c1, c2 = st.columns([1, 1], gap="large")

with c1:
    st.markdown('<div class="animate-on-scroll" style="margin-top: 80px;">', unsafe_allow_html=True)
    st.markdown("<h1>E-Commerce <br> Intelligence .<br><span style='font-size: 0.5em; opacity: 1; color: #888; font-weight: 400;'>Automated Recognition</span></h1>", unsafe_allow_html=True)
    st.markdown('<p class="desc-text" style="color: #ccc; font-size: 1.2rem; margin: 30px 0; line-height: 1.6;">Leverage our enterprise-grade computer vision pipeline to automate product tagging, defect detection, and catalog organization. Built for high-volume e-commerce operations, our solution processes millions of images daily with 99.8% accuracy, freeing your team to focus on strategy rather than manual moderation.</p>', unsafe_allow_html=True)
    
    st.markdown('<a href="/login" target="_self" class="nav-button">Access Dashboard →</a>', unsafe_allow_html=True)
    st.markdown('<a href="/admin" target="_self" class="nav-button">🛡️ Admin Portal</a>', unsafe_allow_html=True)

    st.markdown('<div style="text-align: left; margin-top: 20px;">', unsafe_allow_html=True)
    st.caption("Don't have an account?")
    st.markdown('<a href="/register" target="_self" class="nav-button-secondary">Create Account</a>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with c2:
    st.markdown('<div class="animate-on-scroll" style="margin-top: 50px; display: flex; justify-content: center;">', unsafe_allow_html=True)
    st.html("""
        <div style="width: 100%; height: 450px; position: relative;">
            <!-- Abstract Dashboard UI Mockup -->
            <div style="
                position: absolute; top: 0; left: 5%; width: 90%; height: 100%;
                background: #0f0f0f; border: 1px solid #333; border-radius: 20px;
                box-shadow: 0 50px 100px rgba(0,0,0,0.8);
                overflow: hidden;
            ">
                <!-- Header -->
                <div style="height: 50px; border-bottom: 1px solid #333; display: flex; align-items: center; padding: 0 20px;">
                    <div style="width: 12px; height: 12px; background: #ff5f56; border-radius: 50%; margin-right: 8px;"></div>
                    <div style="width: 12px; height: 12px; background: #ffbd2e; border-radius: 50%; margin-right: 8px;"></div>
                    <div style="width: 12px; height: 12px; background: #27c93f; border-radius: 50%;"></div>
                </div>
                <!-- Body -->
                <div style="padding: 20px;">
                    <div style="width: 60%; height: 20px; background: #333; border-radius: 4px; margin-bottom: 10px;"></div>
                    <div style="width: 40%; height: 20px; background: #222; border-radius: 4px; margin-bottom: 30px;"></div>
                    
                    <div style="display: flex; gap: 10px;">
                        <div style="flex: 1; height: 150px; background: linear-gradient(180deg, rgba(5,117,230,0.1), transparent); border: 1px solid #333; border-radius: 8px;"></div>
                        <div style="flex: 1; height: 150px; background: linear-gradient(180deg, rgba(0,242,96,0.1), transparent); border: 1px solid #333; border-radius: 8px;"></div>
                    </div>
                </div>
            </div>
            <!-- Floating Element -->
            <div style="
                position: absolute; bottom: 50px; right: 0; width: 200px; padding: 20px;
                background: rgba(15,15,15,0.9); border: 1px solid #00f260; border-radius: 16px;
                backdrop-filter: blur(10px);
                box-shadow: 0 20px 40px rgba(0,0,0,0.5);
                animation: float 6s ease-in-out infinite;
            ">
                <div style="font-size: 0.8rem; color: #888;">System Status</div>
                <div style="font-size: 1.2rem; color: #00f260; font-weight: bold;">● Active</div>
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
            <p style="color: #aaa; margin-top: 10px; line-height: 1.6;">Our proprietary ensemble models combine Convolutional Neural Networks (CNNs) and Vision Transformers (ViTs) to achieve human-level understanding. Trained on a diverse proprietary dataset of over 50 million e-commerce images, the system robustly handles varying lighting conditions, angles, and occlusions to deliver precise classification tags and bounding boxes.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

with r1c2:
    st.markdown("""
    <div class="animate-on-scroll h-full">
        <div class="bento-card">
            <div style="font-size: 3rem;">📂</div>
            <h3>Export Data</h3>
            <p style="color: #aaa; line-height: 1.6;">Integrate directly with your existing PIM or ERP systems. We support real-time webhooks, RESTful API endpoints for on-demand access, and scheduled batch exports in CSV, JSON, and Parquet formats. Sync directly to your Data Warehouse including Snowflake, BigQuery, and Redshift.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

with r1c3:
    st.markdown("""
    <div class="animate-on-scroll h-full">
        <div class="bento-card">
            <h3>Visual Dashboards</h3>
            <div style="margin-top: 20px; height: 60px; display: flex; align-items: flex-end; gap: 5px;">
                <div style="width: 20%; height: 40%; background: #333; border-radius: 4px;"></div>
                <div style="width: 20%; height: 70%; background: #0575e6; border-radius: 4px;"></div>
                <div style="width: 20%; height: 50%; background: #00f260; border-radius: 4px;"></div>
                <div style="width: 20%; height: 90%; background: #333; border-radius: 4px;"></div>
            </div>
            <p style="color: #aaa; margin-top: 15px; line-height: 1.6;">Gain deep visibility into your catalog's health. Monitor processing throughput, accuracy confidence intervals, and category distributions in real-time. Drill down into specific SKU-level performance and identify anomalies instantly with our interactive, granular analytics suite.</p>
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
            <h3>Tech Stack</h3>
             <p style="color: #aaa; margin: 10px 0; font-size: 0.9rem; line-height: 1.5;">Built on a rock-solid foundation of modern open-source technologies designed for speed and scalability.</p>
            <div style="display: flex; flex-wrap: wrap; gap: 10px; margin-top: 20px;">
                <span style="padding: 5px 15px; background: #222; border-radius: 20px; font-size: 0.8rem;">TensorFlow</span>
                <span style="padding: 5px 15px; background: #222; border-radius: 20px; font-size: 0.8rem;">Python</span>
                <span style="padding: 5px 15px; background: #222; border-radius: 20px; font-size: 0.8rem;">Streamlit</span>
                <span style="padding: 5px 15px; background: #222; border-radius: 20px; font-size: 0.8rem;">Pandas</span>
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
                    <p style="font-size: 0.7rem; color: #888; max-width: 80px;">Secure ingest via API or UI</p>
                </div>
                <div class="workflow-line"></div>
                <div style="text-align: center;">
                    <div style="background: rgba(5,117,230,0.2); border: 1px solid #0575e6; width: 50px; height: 50px; border-radius: 50%; display: flex; align-items: center; justify-content: center; margin: auto;">2</div>
                    <p style="font-size: 0.8rem; margin-top: 10px; font-weight: bold;">Process</p>
                    <p style="font-size: 0.7rem; color: #888; max-width: 80px;">Parallel GPU Inference</p>
                </div>
                <div class="workflow-line"></div>
                <div style="text-align: center;">
                    <div style="background: rgba(0,242,96,0.2); width: 50px; height: 50px; border-radius: 50%; display: flex; align-items: center; justify-content: center; margin: auto;">3</div>
                    <p style="font-size: 0.8rem; margin-top: 10px; font-weight: bold;">Result</p>
                    <p style="font-size: 0.7rem; color: #888; max-width: 80px;">Actionable Metadata</p>
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
        <div style="display: flex; gap: 20px;">
            <a href="#" style="color: #666; text-decoration: none;">Privacy</a>
            <a href="#" style="color: #666; text-decoration: none;">Terms</a>
            <a href="#" style="color: #666; text-decoration: none;">Twitter</a>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)
