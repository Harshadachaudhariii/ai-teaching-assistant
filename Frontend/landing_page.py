import streamlit as st

# --- 1. STYLES SECTION ---
def inject_custom_css():
    """
    Injects the CSS logic exactly as provided.
    """
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
                rgba(59, 130, 246, 0.12) 0%,   /* soft blue */
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
        
        .logo-container {
            font-size: 28px;
            font-weight: 800;
            background: linear-gradient(90deg, #3B82F6 0%, #FFFFFF 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            display: flex;
            align-items: center;
            height: 100%; 
            padding-top: 5px;
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
            font-size: 72px !important;
            font-weight: 700;
            line-height: 1.25 !important;
            letter-spacing: -2px;
            margin-bottom: 20px;
            background: linear-gradient(90deg, #FFFFFF 0%, #3B82F6 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
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

        .pricing-card {
            background: #111111;
            border: 1px solid #222222;
            padding: 40px;
            border-radius: 24px;
            text-align: center;
            transition: all 0.3s ease;
            height: 550px;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
        }

        .pricing-card:hover {
            border-color: #3b82f6 !important;
            box-shadow: 0px 0px 30px rgba(59, 130, 246, 0.2);
            transform: translateY(-5px);
        }

        .ui-preview {
            background: #161616;
            border: 1px solid #333333;
            border-radius: 24px;
            padding: 30px !important;
            box-shadow: 0 20px 40px rgba(0,0,0,0.4);
            position: relative;
            min-height: 300px;
        }

        .custom-btn {
            display: inline-block;
            width: 100%;
            padding: 12px 0;
            background-color: #3b82f6;
            color: white !important;
            border-radius: 12px;
            text-decoration: none !important;
            font-weight: 600;
            border: 2px solid #3b82f6;
            transition: all 0.3s ease;
            margin-top: 20px;
        }

        .custom-btn:hover {
            background-color: white !important;
            color: #3b82f6 !important;
            border: 2px solid white;
        }

        div.stButton > button[key="hero_cta"] {
            box-shadow: 0 4px 15px rgba(59, 130, 246, 0.3) !important;
            margin-top: 10px !important;
        }

        .cta-card-bg {
            background: linear-gradient(145deg, #0d1117, #1c2128);
            padding: 50px 30px 80px 30px;
            border-radius: 20px;
            border: 1px solid #30363d;
            text-align: center;
            transition: all 0.4s ease;
        }

        .cta-card-bg:hover {
            border-color: #3b82f6 !important;
            box-shadow: 0px 0px 30px rgba(59, 130, 246, 0.1);
        }

        div.stButton {
            text-align: center;
            display: flex;
            justify-content: center;
        }

        div.stButton > button[key="cta_btn"] {
            background-color: #007bff !important;
            color: white !important;
            border: 2px solid #007bff !important;
            border-radius: 50px !important;
            padding: 10px 40px !important;
            font-size: 18px !important;
            font-weight: 700 !important;
            transition: all 0.3s ease-in-out !important;
            margin-top: -50px !important; 
            box-shadow: 0 4px 15px rgba(0,0,0,0.3) !important;
        }

        div.stButton > button[key="cta_btn"]:hover {
            background-color: white !important;
            color: #007bff !important;
            border: 2px solid white !important;
            transform: scale(1.05) !important;
        }

        .scroll-container {
            overflow: hidden;
            white-space: nowrap;
            width: 100%;
            padding: 20px 0;
        }

        .scroll-content {
            display: inline-flex;
            animation: scroll 30s linear infinite;
        }

        .scroll-item {
            padding: 0 40px;
            font-size: 18px;
            font-weight: 500;
            color: #616161;
            text-transform: uppercase;
            letter-spacing: 2px;
        }

        @keyframes scroll {
            0% { transform: translateX(0); }
            100% { transform: translateX(-50%); }
        }

        .footer-heading {
            color: #ddd;
            font-weight: 600;
            margin-bottom: 10px;
        }

        .footer-link {
            text-decoration: none !important;
            color: #aaa !important;
            font-size: 13px;
            display: block;
            margin-bottom: 3px;
            transition: color 0.2s ease;
        }

        .footer-link:hover {
            color: #ffffff !important;
        }

        .card-glow {
            position: absolute;
            width: 280px;
            height: 280px;
            background: radial-gradient(circle, rgba(59,130,246,0.08), transparent 65%);
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            pointer-events: none;
            opacity: 0;
            transition: opacity 0.2s;
        }

        .feature-card:hover .card-glow {
            opacity: 1;
        }

        [data-testid="column"] {
            overflow: visible !important;
            margin-bottom: 30px;
        }
        </style>
        """, unsafe_allow_html=True)

# --- 2. NAVIGATION SECTION ---
def render_navbar():
    nav_col1, nav_col2, nav_col3 = st.columns([2.5, 4.5, 3])
    with nav_col1:
        st.markdown('<div class="logo-container">⚡ LearnAI</div>', unsafe_allow_html=True)
    with nav_col2:
        st.markdown("<div class='nav-links' style='margin-top: 15px; text-align: center;'><a href='#features'>Features</a><a href='#pricing'>Pricing</a><a href='#about'>About</a></div>", unsafe_allow_html=True)
    with nav_col3:
        st.write('<div style="margin-top: 8px;">', unsafe_allow_html=True)
        n_c1, n_c2 = st.columns(2)
        if n_c1.button("Login", key="nav_login"):
            st.session_state.focus_trigger = True 
        with n_c2: st.button("Get Started", key="nav_gs")

# --- 3. HERO SECTION ---
def render_hero():
    st.write("") 
    hero_left, hero_right = st.columns([5, 5])
    with hero_left:
        st.markdown('<p style="color: #3B82F6; font-weight: 600; margin-bottom: -10px;etter-spacing: 1px;">PROXIMITY LEARNING 2.0</p>', unsafe_allow_html=True)
        st.markdown('<h1 class="hero-title">Think faster,<br>learn smarter</h1>', unsafe_allow_html=True)
        st.markdown('<p class="hero-subtitle">The first AI Teaching Assistant built specifically for your curriculum. Transform static study materials into an interactive knowledge base.</p>', unsafe_allow_html=True)
        
        st.text_input("Enter your email", placeholder="name@university.edu", label_visibility="collapsed", key="hero_email")
        st.button("Continue", key="hero_cta")
        st.markdown("<div style='display: flex; gap: 20px; color: #555; font-size: 13px; margin-top: 25px;'><span>✓ No Credit Card Required</span><span>✓ Student Focused</span><span>✓ Privacy First</span></div>", unsafe_allow_html=True)

    with hero_right:
        st.markdown("""
        <div class="ui-preview">
            <div style="border-bottom: 1px solid #222; padding-bottom: 10px; margin-bottom: 25px; display: flex; gap: 25px;">
                <span class="tab-active",>LearnAI</span>
                <span class="tab-inactive">Study Buddy</span>
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

# --- 4. FEATURES SECTION ---
def render_features():
    st.write(""); st.write(""); st.write("")
    st.markdown("<h2 style='text-align: center; font-size: 40px;' id='features'>Engineered for Students</h2>", unsafe_allow_html=True)
    st.write("")

    features = [
        {"icon": "💬", "title": "ChatStream AI", "desc": "Ask anything to the General AI. Powered by Ollama for instant local responses."},
        {"icon": "🎓", "title": "Teaching Assistant", "desc": "Answers strictly from your uploaded course data using advanced RAG systems."},
        {"icon": "📈", "title": "AI Insights", "desc": "Get personalized recommendations based on your learning patterns and gaps."},
        {"icon": "🎯", "title": "Learning Progress", "desc": "Visually track your goals and performance across different subjects."},
        {"icon": "📝", "title": "Smart Notes", "desc": "Automated lecture summaries and key takeaway extractions."},
        {"icon": "🧪", "title": "Exam Lab", "desc": "Generate practice quizzes and mock interviews based on your specific study history."}
    ]

    with st.container():
        rows = [features[i:i+3] for i in range(0, len(features), 3)]
        for row in rows:
            cols = st.columns([1, 3, 3, 3, 1])
            for i, feature in enumerate(row):
                with cols[i+1]:
                    st.markdown(f"""
                        <div class="feature-card">
                            <div class="card-glow"></div>
                            <div class="card-content">
                                <div class="icon">{feature['icon']}</div>
                                <h4>{feature['title']}</h4>
                                <p>{feature['desc']}</p>
                            </div>
                        </div>
                    """, unsafe_allow_html=True)

# --- 5. PRICING SECTION ---
def render_pricing():
    st.write(""); st.write(""); st.write("")
    st.markdown("<h2 style='text-align: center; font-size: 40px;' id='pricing'>Explore Plans</h2>", unsafe_allow_html=True)
    st.write("")

    plans = [
        {"title": "Free", "price": "$0", "subtitle": "For curious learners", "features": ["✓ Basic AI usage", "✓ Limited RAG queries", "✓ Community support"], "btn_text": "Start for Free"},
        {"title": "Pro", "price": "$12", "subtitle": "For serious students", "features": ["✓ Unlimited AI queries", "✓ Advanced AI Insights", "✓ Faster response times", "✓ PDF & Video Analysis"], "btn_text": "Get Pro Now"},
        {"title": "Premium", "price": "$29", "subtitle": "For institutions", "features": ["✓ Advanced Analytics", "✓ Priority AI access", "✓ Personalized Learning Path", "✓ API Access"], "btn_text": "Contact Sales"}
    ]

    cols = st.columns(3)
    for i, plan in enumerate(plans):
        with cols[i]:
            features_html = "".join([f"<p style='margin: 8px 0;'>{f}</p>" for f in plan['features']])
            st.markdown(f"""
                <div class="pricing-card">
                    <div>
                        <h3 style="color: {'#3b82f6' if plan['title'] == 'Pro' else '#888'};">{plan['title']}</h3>
                        <h1 style="margin: 20px 0; color: white;">{plan['price']}</h1>
                        <p style="color: #666; margin-bottom: 30px;">{plan['subtitle']}</p>
                        <div style="text-align: left; color: #aaa; font-size: 14px; border-top: 1px solid #222; padding-top: 20px;">
                            {features_html}
                        </div>
                    </div>
                    <a href="#" class="custom-btn">{plan['btn_text']}</a>
                </div>
            """, unsafe_allow_html=True)

# --- 6. CTA & SCROLLER SECTION ---
def render_cta_and_scroller():
    st.write(""); st.write(""); st.write(""); st.write(""); st.write("")
    _, col, _ = st.columns([1, 8, 1])
    with col:
        st.markdown("""
        <div class="cta-card-bg">
            <h2 style="font-size: 42px; font-weight: 700; margin-bottom: 20px; color: #ffffff;">Ready to transform your study workflow?</h2>
            <p style="color: #8b949e; font-size: 18px; margin-bottom: 40px; max-width: 600px; margin-left: auto; margin-right: auto;">
                Join thousands of students using <b>ChatStream</b> for instant logic and <b>Data AI</b> for mastering material.
            </p>
            <div style="display: flex; justify-content: center; gap: 25px; color: #ffffff; opacity: 0.7; font-size: 14px;">
                <span>✓ No credit card</span><span>✓ 2 minute setup</span><span>✓ Privacy first</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Get Started for Free", key="cta_btn"):
            st.balloons()
            
    st.markdown("""
    <div class="scroll-container">
        <div class="scroll-content">
            <div class="scroll-item">⚡ Instant Responses</div><div class="scroll-item">🔒 Local Data Privacy</div>
            <div class="scroll-item">📚 Course Integration</div><div class="scroll-item">🎯 Personalized Learning</div>
            <div class="scroll-item">🚀 Powered by Ollama</div><div class="scroll-item">📝 Smart Summaries</div>
            <div class="scroll-item">⚡ Instant Responses</div><div class="scroll-item">🔒 Local Data Privacy</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# --- 7. FOOTER SECTION ---
def render_footer():
    st.write(""); st.write(""); st.write(""); st.write("")
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
        render_pricing()
        render_cta_and_scroller()
        render_footer()

def main():
    st.set_page_config(
        page_title="AI Teaching Assistant | Learn Faster",
        page_icon="🧠",
        layout="wide",
        initial_sidebar_state="collapsed"
    )
    render_landing_page()

if __name__ == "__main__":
    main()