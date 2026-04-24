import streamlit as st
import base64
import os

# --- 1. STYLES SECTION ---
def inject_custom_css():
    st.markdown("""
        <style>
        /* 1. Reset & Global Styles */
        #MainMenu, footer, header, [data-testid="stSidebar"] {
            visibility: hidden;
            display: none;
        }

        .stApp {
            background: radial-gradient(
                circle at 50% 30%,
                rgba(59, 130, 246, 0.12) 0%,
                rgba(59, 130, 246, 0.11) 40%,
                rgba(0, 0, 0, 0) 70%
            );
            background-color: #0a0a0a;
            color: #f0f0f0;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
        .block-container {
            padding-top: 2rem !important;
            margin-top: 0rem !important;
        }

        .logo-wrapper {
            display: flex;
            align-items: center;
            gap: 12px;
            height: 100%;
            padding-top: 10px;
            display: block;
        }

        .navbar-logo {
            width: 38px;
            height: auto;
            object-fit: contain;
            display: block;
        }

        .logo-text {
            font-size: 25px;
            font-weight: 700;
            color: #FFFFFF;
            background: none;
            -webkit-text-fill-color: white;
            line-height: 1;
            display: inline-block;
        }

        div.stButton > button[key="nav_login"], div.stButton > button[key="nav_gs"], div.stButton > button[key="hero_cta"] {
            background-color: #3B82F6 !important;
            color: white !important;
            border: 2px solid #3B82F6 !important;
            padding: 8px 20px !important;
            transition: all 0.3s ease-in-out !important;
            margin: 0 5px !important;
        }

        div.stButton > button {
            background-color: #3B82F6 !important;
            color: white !important;
            border: 2px solid #3B82F6 !important;
            padding: 8px 30px !important;
            transition: all 0.3s ease-in-out !important;
        }

        div.stButton > button:hover {
            background-color: white !important;
            color: #3B82F6 !important;
            border: 2px solid #3B82F6 !important;
        }

        .hero-title {
    font-size: 64px !important;      
    line-height: 1.1 !important;    
    margin-bottom: 10px !important;  
    display: block !important;
}

/* Force the icon font to render correctly */
.material-icons, .material-symbols-outlined {
    font-family: 'Material Icons' !important;
    font-display: block;
}

        .hero-subtitle {
            font-size: 22px;
            color: #888888;
            margin-bottom: 40px;
            max-width: 550px;
            line-height: 1.6;
        }

        stTextInput input {
            background-color: #1a1a1a !important;
            border: 1px solid #0319a8 !important;
            color: white !important;
            padding-left: 20px !important;
            border-radius: 12px !important;
            height: 50px;
        }

        .nav-links a {
            color: #a0a0a0 !important;
            text-decoration: none;
            margin-right: 30px;
            font-weight: 500;
            transition: 0.3s;
        }

        .nav-links a:hover {
            color: #ffffff !important;
        }

        .feature-card {
            position: relative;
            background: #111111;
            border: 1px solid #222222;
            padding: 40px;
            border-radius: 20px;
            transition: transform 0.12s ease-out, box-shadow 0.2s ease;
            height: 320px;
            display: flex;
            flex-direction: column;
            z-index: 1;
            margin-top: 20px;
            margin-bottom: 20px;
            overflow: hidden;
            transform-style: preserve-3d;
        }

        .feature-card:hover {
            border-color: #3b82f6 !important;
            background: #161616;
            z-index: 20;
            transform: translateY(-15px) scale(1.03);
            box-shadow: 0px 30px 70px rgba(0,0,0,0.6);
        }

        /*.pricing-card {
            background: #111111;
            border: 1px solid #222222;
            padding: 40px;
            border-radius: 24px;
            text-align: center;
            transition: all 0.3s ease;
            height: 500px;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
        }

        .pricing-card:hover {
            border-color: #3b82f6 !important;
            box-shadow: 0px 0px 30px rgba(59, 130, 246, 0.2);
            transform: translateY(-5px);
        }*/

        /* 2. Fix your UI wrapper alignment */
.ui-preview{
    width: 100%;
    max-width: 900px;
    margin: 0 auto;
    background: rgba(20, 20, 20, 0.6);
    backdrop-filter: blur(10px);
    border: 1px solid #222;
    border-radius: 14px;
    padding: 20px;
}

/* 3. Fix top tab bar alignment */
.ui-preview div[style*="display: flex"]{
    align-items: center;
}

/* 4. Normalize link spacing & baseline alignment */
.ui-preview a{
    line-height: 1.4;
    display: inline-block;
}

/* 5. Fix chat bubble width mismatch */
.ui-preview div[style*="width: 75%"]{
    width: 70% !important;
}

/* 6. Fix right-aligned message */
.ui-preview div[style*="margin-left: 20%"]{
    margin-left: auto !important;
    width: 70% !important;
}

/* 7. Prevent layout jitter */
.ui-preview div{
    box-sizing: border-box;
}

/* 8. Tab underline border fix */
.ui-preview div[style*="border-bottom"]{
    border-color: #222 !important;
}
        .cta-card-bg {
    background: 
        radial-gradient(circle at 20% 30%, rgba(59, 130, 246, 0.25), transparent 40%),
        radial-gradient(circle at 80% 70%, rgba(99, 102, 241, 0.25), transparent 40%),
        rgba(255, 255, 255, 0.02); /* subtle glass tint */

    border: 1px solid rgba(99, 102, 241, 0.25);
    border-radius: 24px;
    padding: 60px 40px;
    text-align: center;
    margin-bottom: 30px;

    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
}
.cta-card-bg:hover {
    border: 1px solid rgba(99, 102, 241, 0.5);
    box-shadow: 0 0 40px rgba(99, 102, 241, 0.2);
    transition: all 0.3s ease;
}

        .scroll-container {
            overflow: hidden;
            white-space: nowrap;
            padding: 20px 0;
            border-top: 1px solid #1e1e1e;
            border-bottom: 1px solid #1e1e1e;
            margin: 20px 0;
        }

        .scroll-content {
            display: inline-flex;
            animation: scroll 20s linear infinite;
            gap: 40px;
        }

        .scroll-item {
            color: #555;
            font-size: 14px;
            font-weight: 500;
            padding: 5px 20px;
            border: 1px solid #222;
            border-radius: 20px;
        }

        @keyframes scroll {
            0% { transform: translateX(0); }
            100% { transform: translateX(-50%); }
        }

        .footer-heading {
            color: #ffffff;
            font-weight: 600;
            margin-bottom: 10px;
        }

        .footer-link {
            display: block;
            color: #7f8082 !important;
            font-size: 14px;
            margin-bottom: 6px;
            cursor: pointer;
            text-decoration: none !important;
        }

        .footer-link:hover {
            color: #ffffff !important;
        }

        .card-glow {
            position: absolute;
            top: 0; left: 0; right: 0; bottom: 0;
            border-radius: 20px;
            background: radial-gradient(circle at 50% 0%, rgba(59,130,246,0.08), transparent 60%);
            pointer-events: none;
        }

        .card-content .icon {
            font-size: 7rem;
            margin-bottom: 15px;
        }

        .card-content h4 {
            font-size: 18px;
            font-weight: 600;
            color: #ffffff;
            margin-bottom: 10px;
        }

        .card-content p {
            color: #888;
            font-size: 16px;
            line-height: 1.6;
        }
        </style>
    """, unsafe_allow_html=True)

# --- 2. NAVBAR SECTION ---
def render_navbar():
    col1, col2, col3 = st.columns([2, 5, 2])
    with col1:
        st.markdown("""
            <div class="logo-wrapper">
                <span class="logo-text">Nexa<span style="color:#3B82F6;">AI</span></span>
            </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
            <div class="nav-links" style="display:flex; align-items:center; height:100%; padding-top:18px;">
                <a href="#features_section">Features</a>
                <a href="#docs_section">Docs</a>
                <a href="#about_section">About</a>
            </div>
        """, unsafe_allow_html=True)
    with col3:
        btn_col1, btn_col2 = st.columns(2)
        with btn_col1:
            if st.button("Log In", key="nav_login"):
                st.session_state.page = "login"
                st.rerun()
        with btn_col2:
            if st.button("Sign Up", key="nav_gs"):
                st.session_state.page = "register"
                st.rerun()

# --- 3. HERO SECTION ---
def render_hero():
    st.write(""); st.write("")
    left, right = st.columns([1, 1.3])

    with left:
        st.markdown("""
            <h1 class="hero-title">Learn Faster.<br>Think Deeper.<br>With AI.</h1>
            <p class="hero-subtitle">
                Your intelligent study partner. Powered by local AI for instant answers,
                personalized learning, and private data.
            </p>
        """, unsafe_allow_html=True)

        c1, c2, c3 = st.columns([1.5, 1,2])
        with c1:
            if st.button("Get Started Free", key="hero_cta", use_container_width=True):
                st.session_state.page = "register"   #  connected to register
                st.rerun()
        with c2:
            if st.button("Log In →", key="hero_login", use_container_width=True):
                st.session_state.page = "login"       #  connected to login
                st.rerun()

    with right:
        active_tab = st.query_params.get("active_tab", "learn")
        if active_tab == "learn":
            st.markdown(f"""
            <div class="ui-preview">
                <div style="border-bottom: 1px solid #222; padding-bottom: 10px; margin-bottom: 25px; display: flex; gap: 25px;">
                    <a href="/?active_tab=learn" target="_self" style="text-decoration: none; color: #3B82F6; border-bottom: 2px solid #3B82F6; padding-bottom: 10px; font-weight: 600;">EchoAI</a>
                    <a href="/?active_tab=study" target="_self" style="text-decoration: none; color: #666;">AtlasAI</a>
                </div>
                <div style="background: #1A1A1A; padding: 15px; border-radius: 10px; margin-bottom: 15px; width: 75%; font-size: 14px; border: 1px solid #222;">
                    Explain neural networks simply.
                </div>
                <div style="background: #252525; padding: 15px; border-radius: 10px; margin-left: 20%; border-left: 3px solid #3B82F6; font-size: 14px;">
                    Think of them like a digital brain...<br>
                    <span style="color: #888; font-size: 13px; display: block; margin-top: 8px;">
                    They process patterns through layers of connected nodes, much like how neurons fire in your own mind.
                    </span>
                </div>
                <div style="margin-top: 40px; width: 100%; background: #111; border: 1px solid #333; padding: 12px; border-radius: 10px; color: #444; font-size: 13px;">
                    Ask Logic Engine or Course Pilot...
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="ui-preview">
                <div style="border-bottom: 1px solid #222; padding-bottom: 10px; margin-bottom: 25px; display: flex; gap: 25px;">
                    <a href="/?active_tab=learn" target="_self" style="text-decoration: none; color: #666;">EchoAI</a>
                    <a href="/?active_tab=study" target="_self" style="text-decoration: none; color: #3B82F6; border-bottom: 2px solid #3B82F6; padding-bottom: 10px; font-weight: 600;">AtlasAI</a>
                </div>
                <div style="background: #1A1A1A; padding: 15px; border-radius: 10px; margin-bottom: 15px; width: 75%; font-size: 14px; border: 1px solid #222;">
                    Help me study CSS Box Model.
                </div>
                <div style="background: #252525; padding: 15px; border-radius: 10px; margin-left: 20%; border-left: 3px solid #3B82F6; font-size: 14px;">
                    The Box Model consists of: Margin, Border, Padding, and Content.<br>
                    <span style="color: #888; font-size: 13px; display: block; margin-top: 8px;">
                    Would you like to start a quick quiz on these concepts?
                    </span>
                </div>
                <div style="margin-top: 40px; width: 100%; background: #111; border: 1px solid #333; padding: 12px; border-radius: 10px; color: #444; font-size: 13px;">
                    Ask about specific CSS properties...
                </div>
            </div>
            """, unsafe_allow_html=True)

# --- 4. FEATURES SECTION ---
# --- 4. FEATURES SECTION ---
def render_features():
    st.write(""); st.write(""); st.write("")
    st.markdown('<span id="features_section"></span>', unsafe_allow_html=True)
    st.markdown("<h2 style='text-align: center; font-size: 40px;'>Engineered for Students</h2>", unsafe_allow_html=True)
    st.write("")

    # Removed "icon" from the data structure
    features = [
    {
        "title": "Teaching Assistant",
        "desc": "Delivers accurate answers grounded in structured course content using a RAG pipeline, ensuring responses stay relevant to your learning material."
    },
    {
        "title": "EchoAI",
        "desc": "Interact with AI through natural conversations to understand concepts, solve problems, and get clear explanations powered by local LLMs."
    },
    {
        "title": "Preloaded Knowledge System",
        "desc": "Uses curated and pre-processed course data as its knowledge base, allowing the AI to respond with context-aware and reliable information."
    },
    {
        "title": "Model Switching",
        "desc": "Choose between models like Phi3 and Llama3 to balance speed, accuracy, and reasoning depth based on your task."
    },
    {
        "title": "Chat History",
        "desc": "Keeps track of your previous conversations so you can revisit, continue discussions, and maintain learning continuity."
    },
    {
        "title": "Local AI Processing",
        "desc": "Runs AI models locally via Ollama, providing faster responses while keeping your data private and under your control."
    }
]

    with st.container():
        rows = [features[i:i+3] for i in range(0, len(features), 3)]
        for row in rows:
            cols = st.columns([1, 3, 3, 3, 1])
            for i, feature in enumerate(row):
                with cols[i+1]:
                    # Removed the <div class="icon"> line entirely
                    st.markdown(f"""
                        <div class="feature-card">
                            <div class="card-glow"></div>
                            <div class="card-content">
                                <h4>{feature['title']}</h4>
                                <p>{feature['desc']}</p>
                            </div>
                        </div>
                    """, unsafe_allow_html=True)

# # --- 5. PRICING SECTION ---
# def render_pricing():
#     # Finalized Launch Pricing: 149/mo and 1,499/yr
#     PLANS = {
#         "Free": {
#             "price": "₹0",
#             "period": "Forever free",
#             "subtitle": "Basic access for students",
#             "features": [
#                 "✓ AtlasAI — Course-based RAG (Full Access)",
#                 "✓ EchoAI — Limited 10 queries/day",
#                 "✓ Basic AI Insights",
#                 "✓ Profile & Activity Log",
#             ],
#             "btn_text": "Current Plan" if st.session_state.get('user_plan') == 'Free' else "Get Started",
#             "btn_key": "price_free"
#         },
#         "Plus": {
#             "price": "₹149",
#             "period": "per month",
#             "subtitle": "For serious learners",
#             "features": [
#                 "✓ Everything in Free, plus:",
#                 "✓ AtlasAI — Unlimited RAG queries",
#                 "✓ EchoAI — 100 queries/day (all speeds)",
#                 "✓ Advanced AI Insights",
#                 "✓ Priority Support",
#                 "✓ Profile Insights Analytics",
#             ],
#             "btn_text": "Upgrade to Plus",
#             "btn_key": "price_plus"
#         },
#         "Pro": {
#             "price": "₹1,499",
#             "period": "per year",
#             "subtitle": "For power users",
#             "features": [
#                 "✓ Everything in Plus, plus:",
#                 "✓ EchoAI — Unlimited queries (all speeds)",
#                 "✓ Smart Mode — Full Access",
#                 "✓ Early Access to New AI Features",
#                 "✓ Dedicated Support",
#                 "✓ Annual billing — 2 Months Free",
#             ],
#             "btn_text": "Upgrade to Pro",
#             "btn_key": "price_pro"
#         }
#     }

#     st.write(""); st.write(""); st.write("")
#     st.markdown('<span id="pricing_section"></span>', unsafe_allow_html=True)
#     st.markdown("<h2 style='text-align: center; font-size: 40px;'>Explore Plans</h2>", unsafe_allow_html=True)

#     cols = st.columns(3)
    
#     for i, (plan_name, plan_data) in enumerate(PLANS.items()):
#         with cols[i]:
#             features_html = "".join([f"<p style='margin: 8px 0;'>{f}</p>" for f in plan_data['features']])

#             # Highlight the Pro plan as the best value
#             card_border = "#3b82f6" if plan_name == "Pro" else "#333"

#             st.markdown(f"""
#                 <div class="pricing-card" style="border: 1px solid {card_border}; padding: 20px; border-radius: 10px; height: 100%; background-color: #0d1117;">
#                     <h3 style="color: #8B949E;">{plan_name}</h3>
#                     <h1 style="margin: 10px 0; color: white;">{plan_data['price']}</h1>
#                     <p style="color: #666; margin-bottom: 5px; font-size: 14px;">{plan_data['period']}</p>
#                     <p style="color: #888; margin-bottom: 20px;">{plan_data['subtitle']}</p>
#                     <div style="text-align: left; color: #aaa; font-size: 14px; border-top: 1px solid #222; padding-top: 20px; min-height: 250px;">
#                         {features_html}
#                     </div>
#                 </div>
#             """, unsafe_allow_html=True)

#             # Button Logic
#             if st.button(plan_data['btn_text'], key=plan_data['btn_key'], use_container_width=True):
#                 if plan_name == "Free":
#                     st.session_state.page = "register"
#                 else:
#                     st.session_state.page = "login"
#                     st.session_state.redirect_to = "billing"
#                 st.rerun()
# --- 6. CTA & SCROLLER SECTION ---
def render_cta_and_scroller():
    st.write(""); st.write(""); st.write(""); st.write(""); st.write("")
    _, col, _ = st.columns([1, 8, 1])
    with col:
        st.markdown("""
        <div class="cta-card-bg">
            <h2 style="font-size: 42px; font-weight: 700; margin-bottom: 20px; color: #ffffff;">Ready to transform your study workflow?</h2>
            <p style="color: #8b949e; font-size: 18px; margin-bottom: 40px; max-width: 600px; margin-left: auto; margin-right: auto;">
                Get clear answers with short explanations, along with the exact video and timestamp from your course.
            </p>
            <div style="display: flex; justify-content: center; gap: 25px; color: #ffffff; opacity: 0.7; font-size: 14px;">
                <span>✓ No credit card</span><span>✓ 2 minute setup</span><span>✓ Privacy first</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        #  Connected to register page
        if st.button("Get Started for Free", key="cta_btn", use_container_width=True):
            st.balloons()
            st.session_state.page = "register"
            st.rerun()

    st.markdown("""
    <div class="scroll-container">
        <div class="scroll-content">
            <div class="scroll-item">Instant Responses</div><div class="scroll-item">Local Data Privacy</div>
            <div class="scroll-item">Course Integration</div><div class="scroll-item">Personalized Learning</div>
            <div class="scroll-item">Powered by Ollama</div><div class="scroll-item">Smart Summaries</div>
            <div class="scroll-item">Instant Responses</div><div class="scroll-item">Local Data Privacy</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# --- 7. FOOTER SECTION ---
def render_footer():
    st.write(""); st.write(""); st.write(""); st.write("")
    st.markdown('<span id="about_section"></span>', unsafe_allow_html=True)
    st.divider()
    foot_col1, foot_col2, foot_col3, foot_col4 = st.columns(4)
    with foot_col1:
        st.markdown('<div class="footer-heading">Product</div><a class="footer-link">Features</a><a class="footer-link">Pricing</a>', unsafe_allow_html=True)
    with foot_col2:
        st.markdown('<div class="footer-heading">Company</div><a class="footer-link">About</a><a class="footer-link">Contact</a>', unsafe_allow_html=True)
    with foot_col3:
        st.markdown('<div class="footer-heading">Resources</div><a class="footer-link">Docs</a><a class="footer-link">Help</a>', unsafe_allow_html=True)
    with foot_col4:
        st.markdown('<div class="footer-heading">Legal</div><a class="footer-link">Privacy</a><a class="footer-link">Terms</a>', unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #666; font-size: 12px;'>AI Teaching Assistant • Built using Streamlit & Ollama • © 2026</p>", unsafe_allow_html=True)

# --- MAIN RENDERER ---
def render_landing_page():
    inject_custom_css()
    with st.container():
        render_navbar()
        render_hero()
        render_features()
        render_cta_and_scroller()
        render_footer()

def main():
    st.set_page_config(
        page_title="NexaAI",
        page_icon="🎓",
        layout="wide",
        initial_sidebar_state="collapsed"
    )
    render_landing_page()

if __name__ == "__main__":
    main()