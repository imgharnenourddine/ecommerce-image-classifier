import streamlit as st
import pandas as pd
import time

# Page Configuration
st.set_page_config(
    page_title="Admin Management - E-Commerce Intelligence",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Admin Dashboard
st.markdown("""
<style>

    .stApp {
        background-color: #050505;
        background-image: 
            radial-gradient(at 0% 0%, rgba(5, 117, 230, 0.1) 0px, transparent 50%),
            radial-gradient(at 100% 0%, rgba(0, 242, 96, 0.05) 0px, transparent 50%);
        color: #ffffff;
        
    }
     [data-testid="stSidebar"] {
        background-color: #353942 !important;
        border-right: 1px solid rgba(255,255,255,0.1);
    }
    header[data-testid="stHeader"] {
        background-color: rgba(0,0,0,0) !important;
    }
   

    /* Metric Cards */
    div[data-testid="stMetricValue"] {
        font-size: 2.5rem;
        font-weight: 800;
        background: linear-gradient(135deg, #00f260, #0575e6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .admin-card {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 20px;
        padding: 24px;
        backdrop-filter: blur(10px);
        margin-bottom: 20px;
    }

    h1, h2, h3 {
        color: white;
        font-weight: 700;
    }

    .status-active { color: #00f260; font-weight: bold; }
    .status-pending { color: #ffa500; font-weight: bold; }
    .role-admin { background: rgba(5, 117, 230, 0.2); padding: 2px 8px; border-radius: 4px; color: #0575e6; }
    .role-user { background: rgba(255, 255, 255, 0.1); padding: 2px 8px; border-radius: 4px; color: #ccc; }

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

    /* Custom Table Styling */
    .stDataFrame {
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 10px;
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

# Sidebar Navigation
with st.sidebar:
    st.title("🛡️ Admin Panel")
    st.markdown("Management & Monitoring")
    st.markdown("---")
    menu = st.radio("Navigation", ["Overview", "User Management", "System Logs", "Settings"])
    st.markdown("---")
    if st.button("Logout"):
        st.switch_page("Home.py")

# Mock User Data
mock_users = [
    {"ID": "USR001", "Username": "noureddine", "Email": "noureddine@example.com", "Role": "Admin", "Status": "Active", "Joined": "2026-01-01"},
    {"ID": "USR002", "Username": "john_doe", "Email": "john@example.com", "Role": "User", "Status": "Active", "Joined": "2026-01-02"},
    {"ID": "USR003", "Username": "sarah_w", "Email": "sarah@example.com", "Role": "User", "Status": "Pending", "Joined": "2026-01-03"},
    {"ID": "USR004", "Username": "mike_tech", "Email": "mike@example.com", "Role": "User", "Status": "Active", "Joined": "2026-01-03"},
    {"ID": "USR005", "Username": "emma_d", "Email": "emma@example.com", "Role": "User", "Status": "Inactive", "Joined": "2026-01-04"},
]

if menu == "Overview":
    st.markdown('<div class="animate-on-scroll">', unsafe_allow_html=True)
    st.title("Admin Overview")
    
    # Stats Row
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric("Total Users", "1,284", "+12%")
    with c2:
        st.metric("Active Sessions", "42", "-3%")
    with c3:
        st.metric("API Requests", "12.5k", "+24%")
    with c4:
        st.metric("Storage Used", "85%", "+2%")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("---")
    
    col_left, col_right = st.columns([2, 1])
    
    with col_left:
        st.markdown('<div class="animate-on-scroll">', unsafe_allow_html=True)
        st.subheader("📈 User Growth")
        chart_data = pd.DataFrame({
            'Day': ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
            'New Users': [10, 23, 15, 45, 32, 56, 78]
        })
        st.line_chart(chart_data.set_index('Day'))
        st.markdown('</div>', unsafe_allow_html=True)

    with col_right:
        st.markdown('<div class="animate-on-scroll">', unsafe_allow_html=True)
        st.subheader("🔔 Recent Activity")
        activities = [
            "🟢 USR004 logged in",
            "🟡 USR003 requested password reset",
            "🔴 Failed login attempt from 192.168.1.1",
            "🟢 USR002 uploaded 24 images",
            "🔵 System update completed"
        ]
        for act in activities:
            st.markdown(f"<div class='admin-card' style='padding: 10px; margin-bottom: 5px; font-size: 0.9rem;'>{act}</div>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

elif menu == "User Management":
    st.markdown('<div class="animate-on-scroll">', unsafe_allow_html=True)
    st.title("👥 User Management")
    st.markdown("Monitor and manage access for all registered users.")

    # KPI Row for Users
    k1, k2, k3 = st.columns(3)
    k1.metric("Active Users", "1.1k")
    k2.metric("Pending Approval", "12")
    k3.metric("Banned/Inactive", "24")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("---")

    # Search and Filter Bar
    st.markdown('<div class="animate-on-scroll">', unsafe_allow_html=True)
    sc1, sc2, sc3 = st.columns([2, 1, 1])
    with sc1:
        search = st.text_input("🔍 Search Database", placeholder="Search by username, email, or ID...")
    with sc2:
        filter_role = st.selectbox("Filter Role", ["All", "Admin", "User"])
    with sc3:
        filter_status = st.selectbox("Filter Status", ["All", "Active", "Pending", "Inactive"])
    st.markdown('</div>', unsafe_allow_html=True)

    # User Table Data Processing
    df = pd.DataFrame(mock_users)
    
    # Add some more specific data for "all users" view
    df['Last Login'] = ["2026-01-04 12:45", "2026-01-04 11:20", "2026-01-03 09:15", "2026-01-04 13:02", "2026-01-02 22:30"]
    df['Plan'] = ["Enterprise", "Basic", "Basic", "Pro", "Basic"]
    df['API Key'] = ["****-4921", "****-8812", "****-3390", "****-1102", "****-9928"]
    
    if search:
        df = df[df['Username'].str.contains(search, case=False) | 
                df['Email'].str.contains(search, case=False) | 
                df['ID'].str.contains(search, case=False)]
    
    if filter_role != "All":
        df = df[df['Role'] == filter_role]
        
    if filter_status != "All":
        df = df[df['Status'] == filter_status]

    # Display Table with custom styles
    st.dataframe(
        df, 
        use_container_width=True, 
        hide_index=True,
        column_config={
            "Status": st.column_config.SelectboxColumn(
                "Status",
                help="User account status",
                options=["Active", "Pending", "Inactive"],
                required=True,
            ),
            "Role": st.column_config.SelectboxColumn(
                "Role",
                help="User permissions level",
                options=["Admin", "User"],
                required=True,
            ),
            "API Key": st.column_config.TextColumn("API Key", width="small")
        }
    )

    # Detailed Action Panel
    with st.expander("🛠️ Advanced User Controls"):
        sel_user = st.selectbox("Select User to Modify", df['Username'].tolist())
        target_user = df[df['Username'] == sel_user].iloc[0]
        
        ac1, ac2 = st.columns(2)
        with ac1:
            st.info(f"Modifying: **{target_user['Username']}** ({target_user['ID']})")
            new_role = st.radio("Update Role", ["Admin", "User"], index=0 if target_user['Role'] == "Admin" else 1, horizontal=True)
            new_status = st.radio("Update Status", ["Active", "Pending", "Inactive"], index=["Active", "Pending", "Inactive"].index(target_user['Status']), horizontal=True)
        
        with ac2:
            st.warning("Danger Zone")
            if st.button("🔒 Suspend Account", use_container_width=True):
                st.snow()
                st.toast(f"Account {sel_user} suspended!")
            if st.button("🗑️ Permanent Delete", use_container_width=True, type="primary"):
                st.error(f"Waiting for confirmation to delete {sel_user}...")
        
        if st.button("💾 Save User Changes"):
            st.success(f"Changes saved for {sel_user}!")

    # Action Buttons
    st.markdown("### Actions")
    ac1, ac2, ac3 = st.columns(3)
    with ac1:
        if st.button("➕ Add New User"):
            st.toast("Feature coming soon!")
    with ac2:
        if st.button("📥 Export User List (CSV)"):
            st.toast("Exporting...")
    with ac3:
        if st.button("🔒 Bulk Permission Update"):
            st.toast("Feature coming soon!")

elif menu == "System Logs":
    st.markdown('<div class="animate-on-scroll">', unsafe_allow_html=True)
    st.title("System Logs")
    st.text_area("Console Output", value="[INFO] 2026-01-04 12:00:01 - Server started\n[DEBUG] 2026-01-04 12:05:22 - Cache cleared\n[WARN] 2026-01-04 12:10:05 - Connection spike detected\n[INFO] 2026-01-04 12:45:00 - Backup successful", height=400)
    st.markdown('</div>', unsafe_allow_html=True)

elif menu == "Settings":
    st.markdown('<div class="animate-on-scroll">', unsafe_allow_html=True)
    st.title("Admin Settings")
    st.checkbox("Enable Public Registration", value=True)
    st.checkbox("Force Two-Factor Authentication", value=False)
    st.slider("Session Timeout (minutes)", 10, 120, 30)
    st.button("Save Changes")
    st.markdown('</div>', unsafe_allow_html=True)
