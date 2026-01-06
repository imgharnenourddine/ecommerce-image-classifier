import streamlit as st
import streamlit.components.v1 as components

def apply_premium_styles():
    """Applies the premium CSS and proximity-based animations to the current page."""
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
            font-family: 'Inter', sans-serif;
        }

        /* Hide Sidebar and Header by default */
        [data-testid="stSidebar"] { display: none; }
        [data-testid="stSidebarNav"] { display: none !important; }
        header[data-testid="stHeader"] { visibility: hidden; }
        .block-container { 
            padding-top: 1rem !important; 
            overflow: visible !important;
        }
        
        /* Container for cards to avoid clipping */
        [data-testid="column"] { overflow: visible !important; }

        /* Headings */
        h1, h2, h3 { font-family: 'Inter', sans-serif; color: #ffffff; }
        h1 {
            font-weight: 900;
            font-size: 3rem !important;
            background: linear-gradient(180deg, #fff, #a5a5a5);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            line-height: 1.1;
        }

       
        

        /* Bento Card & Button Styling */
        .bento-card, [data-testid="stVerticalBlockBorderWrapper"], .stButton > button {
            background: rgba(255, 255, 255, 0.03) !important;
            border: 1px solid rgba(255, 255, 255, 0.08) !important;
            border-radius: 32px !important;
            padding: 40px !important;
            backdrop-filter: blur(20px) !important;
            transition: transform 0.4s cubic-bezier(0.2, 0.8, 0.2, 1), box-shadow 0.4s ease !important;
            position: relative !important;
            overflow: visible !important;
            display: flex !important;
            flex-direction: column !important;
            color: #ffffff !important;
        }

        /* Specialty styling for buttons */
        .stButton > button {
            background: rgba(255, 255, 255, 0.1) !important; /* Slightly lighter/greyer glass */
            padding: 16px 24px !important;
            justify-content: center !important;
            align-items: center !important;
            font-weight: 700 !important;
            font-size: 16px !important;
            height: auto !important;
            width: 100% !important;
        }

        /* Stroke Animation - Proximity for cards, Hover only for buttons */
        .bento-card::after, [data-testid="stVerticalBlockBorderWrapper"]::after {
            content: "" !important;
            position: absolute !important;
            inset: 0 !important;
            border-radius: 32px !important;
            padding: 2px !important;
            background: radial-gradient(circle at var(--mouse-x, 50%) var(--mouse-y, 50%), #0575e6 0%, #00f260 25%, #0575e6 50%, transparent 70%) !important;
            -webkit-mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0) !important;
            mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0) !important;
            -webkit-mask-composite: xor !important;
            mask-composite: exclude !important;
            pointer-events: none !important;
            opacity: var(--stroke-opacity, 0) !important;
            transition: opacity 0.3s ease !important;
            z-index: 1 !important;
        }

        .stButton > button::after {
            content: "" !important;
            position: absolute !important;
            inset: 0 !important;
            border-radius: 32px !important;
            padding: 2px !important;
            background: radial-gradient(circle at var(--mouse-x, 50%) var(--mouse-y, 50%), #0575e6 0%, #00f260 25%, #0575e6 50%, transparent 70%) !important;
            -webkit-mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0) !important;
            mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0) !important;
            -webkit-mask-composite: xor !important;
            mask-composite: exclude !important;
            pointer-events: none !important;
            opacity: 0 !important;
            transition: opacity 0.3s ease !important;
            z-index: 1 !important;
        }

        .stButton > button:hover::after {
            opacity: 1 !important;
        }

        /* Glow Effect - Proximity for cards, Hover only for buttons */
        .bento-card::before, [data-testid="stVerticalBlockBorderWrapper"]::before {
            content: "" !important;
            position: absolute !important;
            inset: -100px !important;
            background: radial-gradient(circle at var(--mouse-x, 50%) var(--mouse-y, 50%), rgba(5, 117, 230, 0.15) 0%, rgba(0, 242, 96, 0.09) 30%, transparent 60%) !important;
            filter: blur(60px) !important;
            opacity: var(--glow-opacity, 0) !important;
            transition: opacity 0.3s ease !important;
            pointer-events: none !important;
            z-index: -1 !important;
        }

        .stButton > button::before {
            content: "" !important;
            position: absolute !important;
            inset: -50px !important;
            background: radial-gradient(circle at var(--mouse-x, 50%) var(--mouse-y, 50%), rgba(5, 117, 230, 0.2) 0%, transparent 60%) !important;
            filter: blur(30px) !important;
            opacity: 0 !important;
            transition: opacity 0.3s ease !important;
            pointer-events: none !important;
            z-index: -1 !important;
        }

        .stButton > button:hover::before {
            opacity: 1 !important;
        }
        
        .bento-card:hover, [data-testid="stVerticalBlockBorderWrapper"]:hover, .stButton > button:hover { 
            transform: translateY(-5px) scale(1.01) !important; 
            box-shadow: 0 20px 40px rgba(0,0,0,0.4) !important; 
            background: rgba(255, 255, 255, 0.06) !important;
            color: #ffffff !important;
        }

        /* Workflow Line Animation */
        .workflow-line {
            flex: 1;
            min-width: 30px;
            height: 2px;
            background: linear-gradient(90deg, rgba(255, 255, 255, 0.1) 0%, #0575e6 50%, rgba(255, 255, 255, 0.1) 100%);
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

        /* Navbar Styles */
        .nav-logo {
            font-family: 'Inter', sans-serif;
            font-weight: 900;
            font-size: 1.5rem;
            background: linear-gradient(90deg, #fff, #aaa);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            letter-spacing: -1px;
            display: flex; align-items: center; height: 100%;
        }

        .nav-btn button {
            padding: 8px 16px !important;
            font-size: 14px !important;
            background: rgba(255,255,255,0.1) !important;
            color: white !important;
            border: 1px solid rgba(255,255,255,0.2) !important;
        }

    </style>
    """, unsafe_allow_html=True)

    # JavaScript for proximity effects and scroll animations
    components.html("""
    <script>
    (function() {
        let globalMouseX = 0;
        let globalMouseY = 0;
        let cards = [];
        
        function findCards() {
            try {
                const parentDoc = window.parent.document;
                const manualCards = parentDoc.querySelectorAll('.bento-card');
                const nativeCards = parentDoc.querySelectorAll('[data-testid="stVerticalBlockBorderWrapper"]');
                const buttons = parentDoc.querySelectorAll('.stButton > button');
                cards = [...manualCards, ...nativeCards, ...buttons];
                return cards.length > 0;
            } catch (e) { return false; }
        }
        
        function updateEffects() {
            cards.forEach(card => {
                const rect = card.getBoundingClientRect();
                const xPercent = ((globalMouseX - rect.left) / rect.width) * 100;
                const yPercent = ((globalMouseY - rect.top) / rect.height) * 100;
                
                const isButton = card.tagName.toLowerCase() === 'button';
                
                const cardCenterX = rect.left + rect.width / 2;
                const cardCenterY = rect.top + rect.height / 2;
                const distance = Math.sqrt(Math.pow(globalMouseX - cardCenterX, 2) + Math.pow(globalMouseY - cardCenterY, 2));
                
                card.style.setProperty('--mouse-x', xPercent + '%');
                card.style.setProperty('--mouse-y', yPercent + '%');

                if (!isButton) {
                    const glowOpacity = Math.max(0, 1 - (distance / 600));
                    const strokeOpacity = Math.max(0, 1 - (distance / 450));
                    card.style.setProperty('--glow-opacity', glowOpacity.toFixed(2));
                    card.style.setProperty('--stroke-opacity', strokeOpacity.toFixed(2));
                }
            });
        }

        function init() {
            findCards();
            const parentDoc = window.parent.document;
            
            parentDoc.addEventListener('mousemove', (e) => {
                globalMouseX = e.clientX;
                globalMouseY = e.clientY;
                updateEffects();
            });

            // Scroll animations
            const observer = new IntersectionObserver((entries) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) entry.target.classList.add('active');
                });
            }, { threshold: 0.1, rootMargin: '0px 0px -50px 0px' });

            parentDoc.querySelectorAll('.animate-on-scroll').forEach(el => observer.observe(el));
        }
        
        if (document.readyState === 'complete') setTimeout(init, 500);
        else window.addEventListener('load', () => setTimeout(init, 500));

        setInterval(() => { findCards(); }, 2000);
    })();
    </script>
    """, height=0)
