import streamlit as st
import requests
import pandas as pd
import io
from PIL import Image

# Configuration
API_URL = "http://127.0.0.1:5000/api/predict"

st.set_page_config(
    page_title="E-ComVision AI",
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Premium Look
st.markdown("""
    <style>
    .main {
        background-color: #0e1117;
        color: #ffffff;
    }
    .stButton>button {
        width: 100%;
        border-radius: 10px;
        background: linear-gradient(45deg, #FF4B4B, #FF914D);
        color: white;
        border: none;
        padding: 0.5rem 1rem;
        font-weight: bold;
    }
    [data-testid="stSidebar"] {
        background-color: #353942 !important;
        border-right: 1px solid rgba(255,255,255,0.1);
    }
    header[data-testid="stHeader"] {
        background-color: rgba(0,0,0,0) !important;
    }
    .stButton>button:hover {
        background: linear-gradient(45deg, #FF914D, #FF4B4B);
        border: none;
    }
    h1 {
        font-family: 'Inter', sans-serif;
        font-weight: 800;
        background: -webkit-linear-gradient(45deg, #FF4B4B, #FF914D);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .css-1d391kg {
        padding-top: 1rem;
    }
    .stProgress > div > div > div > div {
        background-color: #FF4B4B;
    }

    /* Scroll Animation Utility */
    .animate-on-scroll {
        opacity: 0;
        transform: translateY(20px);
        transition: opacity 0.6s ease-out, transform 0.6s ease-out;
    }
    
    .animate-on-scroll.active {
        opacity: 1;
        transform: translateY(0);
    }
    </style>
    """, unsafe_allow_html=True)

import streamlit.components.v1 as components
components.html("""
<script>
(function() {
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
    
    initScrollAnimations();
    setTimeout(initScrollAnimations, 500);
    setTimeout(initScrollAnimations, 1000);
    setTimeout(initScrollAnimations, 2000);
})();
</script>
""", height=0)

# Sidebar
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3081/3081559.png", width=100)
    st.title("E-ComVision")
    st.markdown("Automated Product Recognition System")
    st.markdown("---")
    st.markdown("### ⚙️ Settings")
    st.slider("Confidence Threshold", 0.0, 1.0, 0.2)
    st.markdown("---")
    st.info("Upload a product image to classify it automatically.")
    st.markdown("---")
    if st.button("🛡️ Admin Panel"):
        st.switch_page("pages/admin.py")

# Main Content
st.markdown('<div class="animate-on-scroll">', unsafe_allow_html=True)
st.title("Product Classification Dashboard")
st.markdown("### 📸 Upload Product Image")

uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "png", "jpeg"])
st.markdown('</div>', unsafe_allow_html=True)

if uploaded_file is not None:
    col1, col2 = st.columns([1, 2])
    
    with col1:
        image = Image.open(uploaded_file)
        st.image(image, caption='Uploaded Product', use_container_width=True)
    
    with col2:
        st.markdown('<div class="animate-on-scroll">', unsafe_allow_html=True)
        st.markdown("### 🔍 Analysis Results")
        with st.spinner('Analysing image with AI...'):
            try:
                # Prepare file for API
                # Reset pointer to start because Image.open might have moved it? 
                # Actually uploaded_file is a BytesIO-like object. 
                # Accessing .getvalue() is safer for requests.
                files = {'file': uploaded_file.getvalue()}
                response = requests.post(API_URL, files=files)
                
                if response.status_code == 200:
                    data = response.json()
                    predictions = data.get('predictions', [])
                    
                    if predictions:
                        # Top Prediction Highlighting
                        top_pred = predictions[0]
                        st.success(f"**Identified Category:** {top_pred['class'].replace('_', ' ').title()}")
                        st.metric("Confidence Score", f"{top_pred['confidence']*100:.2f}%")
                        
                        # Data for Chart
                        df = pd.DataFrame(predictions)
                        df['class'] = df['class'].str.replace('_', ' ').str.title()
                        df['confidence'] = df['confidence'] * 100
                        
                        st.markdown("#### Confidence Distribution")
                        st.bar_chart(df.set_index('class')['confidence'])
                        
                        # Export Option
                        st.markdown("### 📥 Export Data")
                        csv = df.to_csv(index=False).encode('utf-8')
                        st.download_button(
                            "Download Analysis as CSV",
                            csv,
                            "product_analysis.csv",
                            "text/csv",
                            key='download-csv'
                        )
                    else:
                        st.warning("No predictions returned.")
                else:
                    st.error(f"Error from API: {response.text}")
            except Exception as e:
                st.error(f"Connection Error: {e}")
                st.markdown("*Make sure the Flask Backend is running!*")
        st.markdown('</div>', unsafe_allow_html=True)

else:
    st.markdown("""
    <div style='text-align: center; padding: 50px; background-color: #262730; border-radius: 10px;'>
        <h3>Waiting for upload...</h3>
        <p>Supported formats: JPG, PNG</p>
    </div>
    """, unsafe_allow_html=True)
