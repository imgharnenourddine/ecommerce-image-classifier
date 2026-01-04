import streamlit as st
import pandas as pd
import numpy as np
import datetime
import random

# Page Configuration
st.set_page_config(
    page_title="Predictions - E-Commerce Intelligence",
    page_icon="🔮",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .stApp {
        background-color: #050505;
        color: #ffffff;
    }
    
     [data-testid="stSidebar"] {
        background-color: #353942 !important;
        border-right: 1px solid rgba(255,255,255,0.1);
    }
    header[data-testid="stHeader"] {
        background-color: rgba(0,0,0,0) !important;
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

    .prediction-card {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 15px;
        padding: 20px;
        margin-bottom: 10px;
    }

    .confidence-high { color: #00f260; }
    .confidence-med { color: #ffa500; }
    .confidence-low { color: #ff4b4b; }
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
    st.markdown("🔮 Prediction Insights")
    st.markdown("---")
    if st.button("📊 Dashboard"):
        st.switch_page("pages/dashboard.py")
    if st.button("🛡️ Admin Panel"):
        st.switch_page("pages/admin.py")

# Mock Data Generation
categories = ["Electronics", "Clothing", "Home & Kitchen", "Beauty", "Sports", "Books"]
status_options = ["Success", "Uncertain", "Failed"]

def generate_mock_data(n=100):
    data = []
    base_date = datetime.datetime.now()
    for i in range(n):
        cat = random.choice(categories)
        conf = random.uniform(0.4, 0.99)
        status = "Success" if conf > 0.7 else ("Uncertain" if conf > 0.5 else "Failed")
        data.append({
            "Timestamp": (base_date - datetime.timedelta(minutes=random.randint(0, 10000))).strftime("%Y-%m-%d %H:%M"),
            "Product ID": f"PRD-{random.randint(1000, 9999)}",
            "Category": cat,
            "Confidence": round(conf * 100, 2),
            "Status": status
        })
    return pd.DataFrame(data)

df = generate_mock_data(150)

# Dashboard Layout
st.markdown('<div class="animate-on-scroll">', unsafe_allow_html=True)
st.title("🔮 Prediction Analytics")
st.markdown("In-depth analysis of AI categorization performance across all product lines.")
st.markdown('</div>', unsafe_allow_html=True)

# Key Metrics
st.markdown('<div class="animate-on-scroll">', unsafe_allow_html=True)
m1, m2, m3, m4 = st.columns(4)
m1.metric("Total Predictions", len(df), "+14%")
m2.metric("Avg. Confidence", f"{df['Confidence'].mean():.1f}%", "+2.4%")
m3.metric("Top Category", df['Category'].mode()[0])
m4.metric("Accuracy Rate", "94.2%", "+0.5%")
st.markdown('</div>', unsafe_allow_html=True)

st.markdown("---")

# Visualizations
c1, c2 = st.columns([2, 1])

with c1:
    st.markdown('<div class="animate-on-scroll">', unsafe_allow_html=True)
    st.subheader("📈 Prediction Volume by Category")
    cat_counts = df['Category'].value_counts()
    st.bar_chart(cat_counts)
    st.markdown('</div>', unsafe_allow_html=True)

with c2:
    st.markdown('<div class="animate-on-scroll">', unsafe_allow_html=True)
    st.subheader("🎯 Confidence Distribution")
    # Histogram of confidence
    hist_values = np.histogram(df['Confidence'], bins=10, range=(40, 100))[0]
    st.area_chart(hist_values)
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("---")

# Detailed Table
st.markdown('<div class="animate-on-scroll">', unsafe_allow_html=True)
st.subheader("📑 Global Prediction History")

# Filters
f1, f2 = st.columns([2, 1])
with f1:
    search_q = st.text_input("🔍 Search by Product ID or Category", placeholder="Enter product details...")
with f2:
    status_filter = st.multiselect("Filter by Status", status_options, default=status_options)

# Apply Filters
filtered_df = df[df['Status'].isin(status_filter)]
if search_q:
    filtered_df = filtered_df[
        filtered_df['Product ID'].str.contains(search_q, case=False) | 
        filtered_df['Category'].str.contains(search_q, case=False)
    ]

st.dataframe(
    filtered_df,
    use_container_width=True,
    hide_index=True,
    column_config={
        "Confidence": st.column_config.ProgressColumn(
            "Confidence %",
            help="Prediction confidence level",
            min_value=0,
            max_value=100,
            format="%f%%"
        ),
        "Status": st.column_config.SelectboxColumn(
            "Status",
            options=status_options,
            required=True
        )
    }
)
st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("""
<div style="text-align: center; margin-top: 50px; color: #666; font-size: 0.8rem;">
    Powered by E-ComVision AI Engine • Last Updated: {}
</div>
""".format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")), unsafe_allow_html=True)
