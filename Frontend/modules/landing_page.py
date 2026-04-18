# import streamlit as st
# import base64
# import os
# # --- 1. STYLES SECTION ---
# def inject_custom_css():
#     st.markdown("""
#         <style>
#         /* 1. Reset & Global Styles */
#         #MainMenu, footer, header, [data-testid="stSidebar"] {
#             visibility: hidden;
#             display: none;
#         }

#         .stApp {
#             background: radial-gradient(
#                 circle at 50% 30%,
#                 rgba(59, 130, 246, 0.12) 0%,   /* soft blue */
#                 rgba(59, 130, 246, 0.11) 40%,
#                 rgba(0, 0, 0, 0) 70%
#             );
#             background-color: #0a0a0a;
#             color: #f0f0f0;
#             font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
#         }
#         .block-container {
#             padding-top: 2rem !important;
#             margin-top: 0rem !important;
#         }
        
#         /*.logo-container {
#             font-size: 28px;
#             font-weight: 800;
#             background: linear-gradient(90deg, #3B82F6 0%, #FFFFFF 100%);
#             -webkit-background-clip: text;
#             -webkit-text-fill-color: transparent;
#             display: flex;
#             align-items: center;
#             height: 100%; 
#             padding-top: 5px;
#         }*/
#         /* Container to align items horizontally */
# .logo-wrapper {
#     display: flex;
#     align-items: center; /* Vertical centering */
#     gap: 12px;           /* Perfect spacing between logo and text */
#     height: 100%;
#     padding-top: 10px;
#     display: block;
# }

# /* Style for the hexagonal logo */
# .navbar-logo {
#     width: 38px;
#     height: auto;
#     object-fit: contain;
#     display: block;
# }

# /* Style for the text */
# .logo-text {
#     font-size: 25px;
#     font-weight: 700;
#     color: #FFFFFF;
#     background: none;
#     -webkit-text-fill-color: white; /* Overrides previous gradient if needed */
#     line-height: 1;
#     display: inline-block;
# }
#         div.stButton > button[key="nav_login"], div.stButton > button[key="nav_gs"], div.stButton > button[key="hero_cta"] {
#             background-color: #3B82F6 !important;
#             color: white !important;
#             border: 2px solid #3B82F6 !important;
#             padding: 8px 20px !important;
#             transition: all 0.3s ease-in-out !important;
#             margin: 0 5px !important;
#         }

#         div.stButton > button {
#             background-color: #3B82F6 !important;
#             color: white !important;
#             border: 2px solid #3B82F6 !important;
#             padding: 8px 30px !important;
#             transition: all 0.3s ease-in-out !important;
#         }

#         div.stButton > button:hover {
#             background-color: white !important;
#             color: #3B82F6 !important;
#             border: 2px solid #3B82F6 !important;
#         }

#         .hero-title {
#             font-size: 72px !important;
#             font-weight: 700;
#             line-height: 1.25 !important;
#             letter-spacing: -2px;
#             margin-bottom: 20px;
#             background: linear-gradient(90deg, #FFFFFF 0%, #3B82F6 100%);
#             -webkit-background-clip: text;
#             -webkit-text-fill-color: transparent;
#         }
        
#         .hero-subtitle {
#             font-size: 22px;
#             color: #888888;
#             margin-bottom: 40px;
#             max-width: 550px;
#             line-height: 1.6;
#         }

#         stTextInput input {
#             background-color: #1a1a1a !important;
#             border: 1px solid #0319a8 !important;
#             color: white !important;
#             padding-left: 20px !important;
#             border-radius: 12px !important;
#             height: 50px;
#         }

#         .nav-links a {
#             color: #a0a0a0 !important;
#             text-decoration: none;
#             margin-right: 30px;
#             font-weight: 500;
#             transition: 0.3s;
#         }

#         .nav-links a:hover {
#             color: #ffffff !important;
#         }

#         .feature-card {
#             position: relative;
#             background: #111111;
#             border: 1px solid #222222;
#             padding: 40px;
#             border-radius: 20px;
#             transition: transform 0.12s ease-out, box-shadow 0.2s ease;
#             height: 320px;
#             display: flex;
#             flex-direction: column;
#             z-index: 1;
#             margin-top: 20px;
#             margin-bottom: 20px;
#             overflow: hidden;
#             transform-style: preserve-3d;
#         }

#         .feature-card:hover {
#             border-color: #3b82f6 !important;
#             background: #161616;
#             z-index: 20;
#             transform: translateY(-15px) scale(1.03);
#             box-shadow: 0px 30px 70px rgba(0,0,0,0.6);
#         }

#         .pricing-card {
#             background: #111111;
#             border: 1px solid #222222;
#             padding: 40px;
#             border-radius: 24px;
#             text-align: center;
#             transition: all 0.3s ease;
#             height: 550px;
#             display: flex;
#             flex-direction: column;
#             justify-content: space-between;
#         }

#         .pricing-card:hover {
#             border-color: #3b82f6 !important;
#             box-shadow: 0px 0px 30px rgba(59, 130, 246, 0.2);
#             transform: translateY(-5px);
#         }

#         .ui-preview {
#             background: #161616;
#             border: 1px solid #333333;
#             border-radius: 24px;
#             padding: 30px !important;
#             box-shadow: 0 20px 40px rgba(0,0,0,0.4);
#             position: relative;
#             min-height: 300px;
#         }

#         .custom-btn {
#             display: inline-block;
#             width: 100%;
#             padding: 12px 0;
#             background-color: #3b82f6;
#             color: white !important;
#             border-radius: 12px;
#             text-decoration: none !important;
#             font-weight: 600;
#             border: 2px solid #3b82f6;
#             transition: all 0.3s ease;
#             margin-top: 20px;
#         }

#         .custom-btn:hover {
#             background-color: white !important;
#             color: #3b82f6 !important;
#             border: 2px solid white;
#         }

#         div.stButton > button[key="hero_cta"] {
#             box-shadow: 0 4px 15px rgba(59, 130, 246, 0.3) !important;
#             margin-top: 10px !important;
#         }

#         .cta-card-bg {
#             background: linear-gradient(145deg, #0d1117, #1c2128);
#             padding: 50px 30px 80px 30px;
#             border-radius: 20px;
#             border: 1px solid #30363d;
#             text-align: center;
#             transition: all 0.4s ease;
#         }

#         .cta-card-bg:hover {
#             border-color: #3b82f6 !important;
#             box-shadow: 0px 0px 30px rgba(59, 130, 246, 0.1);
#         }

#         div.stButton {
#             text-align: center;
#             display: flex;
#             justify-content: center;
#         }

#         /* 1. Target the button specifically and center it */
#         .stApp div.stButton > button:has(p:contains("Get Started for Free")) {
#             background-color: #3B82F6 !important;
#             color: white !important;
#             border: 2px solid #3B82F6 !important;
#             border-radius: 50px !important;
#             padding: 120px 60px !important;
#             font-size: 18px !important;
#             font-weight: 700 !important;
            
#             /* Positioning logic to overlap the border */
#             margin-top: -45px !important; 
#             z-index: 999 !important;
#             position: relative !important;
            
#             box-shadow: 0 10px 25px rgba(0, 0, 0, 0.5) !important;
#             transition: all 0.3s ease-in-out !important;
#         }

#         /* 2. Hover state using the SAME selector */
#         .stApp div.stButton > button:has(p:contains("Get Started for Free")):hover {
#             background-color: white !important;
#             color: #3B82F6 !important;
#             border: 2px solid white !important;
#             transform: scale(1.05) !important;
#             box-shadow: 0 15px 30px rgba(59, 130, 246, 0.4) !important;
#         }


#         .scroll-container {
#             overflow: hidden;
#             white-space: nowrap;
#             width: 100%;
#             padding: 20px 0;
#         }

#         .scroll-content {
#             display: inline-flex;
#             animation: scroll 30s linear infinite;
#         }

#         .scroll-item {
#             padding: 0 40px;
#             font-size: 18px;
#             font-weight: 500;
#             color: #616161;
#             text-transform: uppercase;
#             letter-spacing: 2px;
#         }

#         @keyframes scroll {
#             0% { transform: translateX(0); }
#             100% { transform: translateX(-50%); }
#         }

#         .footer-heading {
#             color: #ddd;
#             font-weight: 600;
#             margin-bottom: 10px;
#         }

#         .footer-link {
#             text-decoration: none !important;
#             color: #aaa !important;
#             font-size: 13px;
#             display: block;
#             margin-bottom: 3px;
#             transition: color 0.2s ease;
#         }

#         .footer-link:hover {
#             color: #ffffff !important;
#         }

#         .card-glow {
#             position: absolute;
#             width: 280px;
#             height: 280px;
#             background: radial-gradient(circle, rgba(59,130,246,0.08), transparent 65%);
#             top: 50%;
#             left: 50%;
#             transform: translate(-50%, -50%);
#             pointer-events: none;
#             opacity: 0;
#             transition: opacity 0.2s;
#         }

#         .feature-card:hover .card-glow {
#             opacity: 1;
#         }

#         [data-testid="column"] {
#             overflow: visible !important;
#             margin-bottom: 30px;
#         }
#         /* 1. Target the deepest input level */
#         .stTextInput > div > div > input {
#             background-color: #1a1a1a !important;
#             color: white !important;
#             padding-left: 20px !important;
#             height: 50px;
#             transition: all 0.2s ease-in-out !important;
#         }

#         /* 2. COMPLETELY REMOVE STREAMLIT'S RED BORDER/GLOW */
#         /* This targets the wrapper divs that cause the red hover effect */
#         .stTextInput div[data-baseweb="input"] {
#             border: none !important;
#             background-color: transparent !important;
#         }

#         /* 3. Hover State - Forces Blue, Kills Red */
#         .stTextInput > div > div > input:hover {
#             border-color: #3B82F6 !important;
#             box-shadow: none !important;
#         }

#         /* 4. Focus State - Blue glow instead of red */
#         .stTextInput > div > div > input:focus {
#             border-color: #60a5fa !important;
#             box-shadow: 0 0 10px rgba(59, 130, 246, 0.4) !important;
#             outline: none !important;
#         }

#         /* 5. Final safety: remove any red borders from focused parent containers */
#         .stTextInput > div > div:focus-within {
#             border-color: transparent !important;
#             box-shadow: none !important;
#         }
#         </style>
    
#         """, unsafe_allow_html=True)

# # --- 2. NAVIGATION SECTION ---
# def get_base64_of_bin_file(bin_file):
#     with open(bin_file, 'rb') as f:
#         data = f.read()
#     return base64.b64encode(data).decode()

# def render_navbar():
#     current_dir = os.path.dirname(os.path.abspath(__file__)) # points to Frontend/modules
#     logo_path = os.path.join(current_dir, "..", "assets", "logo.png")
    
#     # 2. Convert logo to base64 string
#     logo_base64 = get_base64_of_bin_file(logo_path)
#     nav_col1, nav_col2, nav_col3 = st.columns([2.5, 4.5, 3])
#     with nav_col1:
#         # This replaces the text with your logo image
#         st.markdown(f'''
#             <div class="logo-container">
#                 <img src="data:image/png;base64,{logo_base64}" width="40" style="margin-right:5px; vertical-align: middle;"> 
#                 <span class="logo-text">NexaAI</span>
#             </div>
#         ''', unsafe_allow_html=True)
#     with nav_col2:
#         # Keep your exact HTML logic
#         st.markdown("""
#             <div class='nav-links' style='margin-top: 15px; text-align: center;'>
#                 <a href='#features_section'>Features</a>
#                 <a href='#pricing_section'>Pricing</a>
#                 <a href='#about_section'>About</a>
#             </div>
#         """, unsafe_allow_html=True)
#     with nav_col3:
#         st.write('<div style="margin-top: 8px;">', unsafe_allow_html=True)
#         n_c1, n_c2 = st.columns(2)
#         if n_c1.button("Login", key="nav_login"):
#             st.session_state.page = "login"
#             st.rerun()
#         with n_c2: 
#             if st.button("Get Started", key="nav_gs"):
#                 st.session_state.page = "login" # Or "signup" if you have a separate view
#                 st.rerun()
        
# # --- 3. HERO SECTION ---
# def render_hero():
#     # Check current active tab from URL state, default to 'learn'
#     if "active_tab" not in st.query_params:
#         st.query_params["active_tab"] = "learn"
    
#     active = st.query_params["active_tab"]

#     st.write("") 
#     hero_left, hero_right = st.columns([5, 5])
    
#     # --- LEFT SIDE (Unchanged) ---
#     with hero_left:
        
#         st.markdown('<h1 class="hero-title">Think faster,<br>learn smarter</h1>', unsafe_allow_html=True)
#         st.markdown('<p class="hero-subtitle">The first AI Teaching Assistant built specifically for your courses. Transform static study materials into an interactive knowledge base.</p>', unsafe_allow_html=True)
#         left_gap, center_col, right_gap = st.columns([1, 8, 1])
        
#         with center_col:
#             # The CSS above will automatically color this border blue
#             st.text_input("Enter your email", 
#                          placeholder="name@university.edu", 
#                          label_visibility="collapsed", 
#                          key="hero_email")
            
#             st.button("Continue with Email", key="hero_cta", use_container_width=True)
            
#             st.markdown("<p style='text-align: center; color: #555; margin: 10px 0; font-size: 14px;'>— OR —</p>", unsafe_allow_html=True)
            
#             st.button("Continue with Google", key="hero_google", use_container_width=True)

#     # --- RIGHT SIDE (Internal Tab Logic) ---
#     with hero_right:
#         if active == "learn":
#             st.markdown(f"""
#             <div class="ui-preview">
#                 <div style="border-bottom: 1px solid #222; padding-bottom: 10px; margin-bottom: 25px; display: flex; gap: 25px;">
#                     <a href="/?active_tab=learn" target="_self" style="text-decoration: none; color: #3B82F6; border-bottom: 2px solid #3B82F6; padding-bottom: 10px; font-weight: 600;">EchoAI</a>
#                     <a href="/?active_tab=study" target="_self" style="text-decoration: none; color: #666;">AtlasAI</a>
#                 </div>
#                 <div style="background: #1A1A1A; padding: 15px; border-radius: 10px; margin-bottom: 15px; width: 75%; font-size: 14px; border: 1px solid #222;">
#                     Explain neural networks simply.
#                 </div>
#                 <div style="background: #252525; padding: 15px; border-radius: 10px; margin-left: 20%; border-left: 3px solid #3B82F6; font-size: 14px;">
#                     Think of them like a digital brain...<br>
#                     <span style="color: #888; font-size: 13px; display: block; margin-top: 8px;">
#                     They process patterns through layers of connected nodes, much like how neurons fire in your own mind.
#                     </span>
#                 </div>
#                 <div style="margin-top: 40px; width: 100%; background: #111; border: 1px solid #333; padding: 12px; border-radius: 10px; color: #444; font-size: 13px;">
#                     Ask Logic Engine or Course Pilot...
#                 </div>
#             </div>
#             """, unsafe_allow_html=True)
        
#         else:
#             st.markdown(f"""
#             <div class="ui-preview">
#                 <div style="border-bottom: 1px solid #222; padding-bottom: 10px; margin-bottom: 25px; display: flex; gap: 25px;">
#                     <a href="/?active_tab=learn" target="_self" style="text-decoration: none; color: #666;">EchoAI</a>
#                     <a href="/?active_tab=study" target="_self" style="text-decoration: none; color: #3B82F6; border-bottom: 2px solid #3B82F6; padding-bottom: 10px; font-weight: 600;">AtlasAI</a>
#                 </div>
#                 <div style="background: #1A1A1A; padding: 15px; border-radius: 10px; margin-bottom: 15px; width: 75%; font-size: 14px; border: 1px solid #222;">
#                     Help me study CSS Box Model.
#                 </div>
#                 <div style="background: #252525; padding: 15px; border-radius: 10px; margin-left: 20%; border-left: 3px solid #3B82F6; font-size: 14px;">
#                     The Box Model consists of: Margin, Border, Padding, and Content.<br>
#                     <span style="color: #888; font-size: 13px; display: block; margin-top: 8px;">
#                     Would you like to start a quick quiz on these concepts?
#                     </span>
#                 </div>
#                 <div style="margin-top: 40px; width: 100%; background: #111; border: 1px solid #333; padding: 12px; border-radius: 10px; color: #444; font-size: 13px;">
#                     Ask about specific CSS properties...
#                 </div>
#             </div>
#             """, unsafe_allow_html=True)

# # --- 4. FEATURES SECTION ---
# def render_features():
#     st.write(""); st.write(""); st.write("")
#     st.markdown('<span id="features_section"></span>', unsafe_allow_html=True)
#     # id="features" allows the navbar link to jump here
#     st.markdown("<h2 style='text-align: center; font-size: 40px;'>Engineered for Students</h2>", unsafe_allow_html=True)
#     st.write("")
    
#     features = [
#         {"icon": "💬", "title": "ChatStream AI", "desc": "Ask anything to the General AI. Powered by Ollama for instant local responses."},
#         {"icon": "🎓", "title": "Teaching Assistant", "desc": "Answers strictly from your uploaded course data using advanced RAG systems."},
#         {"icon": "📈", "title": "AI Insights", "desc": "Get personalized recommendations based on your learning patterns and gaps."},
#         {"icon": "🎯", "title": "Learning Progress", "desc": "Visually track your goals and performance across different subjects."},
#         {"icon": "📝", "title": "Smart Notes", "desc": "Automated lecture summaries and key takeaway extractions."},
#         {"icon": "🧪", "title": "Exam Lab", "desc": "Generate practice quizzes and mock interviews based on your specific study history."}
#     ]

#     with st.container():
#         rows = [features[i:i+3] for i in range(0, len(features), 3)]
#         for row in rows:
#             cols = st.columns([1, 3, 3, 3, 1])
#             for i, feature in enumerate(row):
#                 with cols[i+1]:
#                     st.markdown(f"""
#                         <div class="feature-card">
#                             <div class="card-glow"></div>
#                             <div class="card-content">
#                                 <div class="icon">{feature['icon']}</div>
#                                 <h4>{feature['title']}</h4>
#                                 <p>{feature['desc']}</p>
#                             </div>
#                         </div>
#                     """, unsafe_allow_html=True)
                    
# # --- 5. PRICING SECTION ---
# def render_pricing():
#     st.write(""); st.write(""); st.write("")
#     st.markdown('<span id="pricing_section"></span>', unsafe_allow_html=True)
#     # id="pricing" allows the navbar link to jump here
#     st.markdown("<h2 style='text-align: center; font-size: 40px;'>Engineered for Students</h2>", unsafe_allow_html=True)
#     st.write("")

#     plans = [
#         {"title": "Free", "price": "$0", "subtitle": "For curious learners", "features": ["✓ Basic AI usage", "✓ Limited RAG queries", "✓ Community support"], "btn_text": "Start for Free"},
#         {"title": "Pro", "price": "$12", "subtitle": "For serious students", "features": ["✓ Unlimited AI queries", "✓ Advanced AI Insights", "✓ Faster response times", "✓ PDF & Video Analysis"], "btn_text": "Get Pro Now"},
#         {"title": "Premium", "price": "$29", "subtitle": "For institutions", "features": ["✓ Advanced Analytics", "✓ Priority AI access", "✓ Personalized Learning Path", "✓ API Access"], "btn_text": "Contact Sales"}
#     ]

#     cols = st.columns(3)
#     for i, plan in enumerate(plans):
#         with cols[i]:
#             features_html = "".join([f"<p style='margin: 8px 0;'>{f}</p>" for f in plan['features']])
#             st.markdown(f"""
#                 <div class="pricing-card">
#                     <div>
#                         <h3 style="color: {'#3b82f6' if plan['title'] == 'Pro' else '#888'};">{plan['title']}</h3>
#                         <h1 style="margin: 20px 0; color: white;">{plan['price']}</h1>
#                         <p style="color: #666; margin-bottom: 30px;">{plan['subtitle']}</p>
#                         <div style="text-align: left; color: #aaa; font-size: 14px; border-top: 1px solid #222; padding-top: 20px;">
#                             {features_html}
#                         </div>
#                     </div>
#                     <a href="#" class="custom-btn">{plan['btn_text']}</a>
#                 </div>
#             """, unsafe_allow_html=True)

# # --- 6. CTA & SCROLLER SECTION ---
# def render_cta_and_scroller():
#     st.write(""); st.write(""); st.write(""); st.write(""); st.write("")
#     _, col, _ = st.columns([1, 8, 1])
#     with col:
#         st.markdown("""
#         <div class="cta-card-bg">
#             <h2 style="font-size: 42px; font-weight: 700; margin-bottom: 20px; color: #ffffff;">Ready to transform your study workflow?</h2>
#             <p style="color: #8b949e; font-size: 18px; margin-bottom: 40px; max-width: 600px; margin-left: auto; margin-right: auto;">
#                 Join thousands of students using <b>ChatStream</b> for instant logic and <b>Data AI</b> for mastering material.
#             </p>
#             <div style="display: flex; justify-content: center; gap: 25px; color: #ffffff; opacity: 0.7; font-size: 14px;">
#                 <span>✓ No credit card</span><span>✓ 2 minute setup</span><span>✓ Privacy first</span>
#             </div>
#         </div>
#         """, unsafe_allow_html=True)
#         if st.button("Get Started for Free", key="cta_btn"):
#             st.balloons()
#             st.session_state.page = "login" # Or "signup" if you have a separate view
#             st.rerun()
            
#     st.markdown("""
#     <div class="scroll-container">
#         <div class="scroll-content">
#             <div class="scroll-item">⚡ Instant Responses</div><div class="scroll-item">🔒 Local Data Privacy</div>
#             <div class="scroll-item">📚 Course Integration</div><div class="scroll-item">🎯 Personalized Learning</div>
#             <div class="scroll-item">🚀 Powered by Ollama</div><div class="scroll-item">📝 Smart Summaries</div>
#             <div class="scroll-item">⚡ Instant Responses</div><div class="scroll-item">🔒 Local Data Privacy</div>
#         </div>
#     </div>
#     """, unsafe_allow_html=True)

# # --- 7. FOOTER SECTION ---
# def render_footer():
#     st.write(""); st.write(""); st.write(""); st.write("")
#     # id="about" target for the navbar
#     st.markdown('<span id="about_section"></span>', unsafe_allow_html=True)
#     st.divider()
#     foot_col1, foot_col2, foot_col3, foot_col4 = st.columns(4)
#     with foot_col1:
#         st.markdown('<div class="footer-heading">Product</div><a class="footer-link">Features</a><a class="footer-link">Pricing</a>', unsafe_allow_html=True)
#     with foot_col2:
#         st.markdown('<div class="footer-heading">Company</div><a class="footer-link">About</a><a class="footer-link">Contact</a>', unsafe_allow_html=True)
#     with foot_col3:
#         st.markdown('<div class="footer-heading">Resources</div><a class="footer-link">Docs</a><a class="footer-link">Help</a>', unsafe_allow_html=True)
#     with foot_col4:
#         st.markdown('<div class="footer-heading">Legal</div><a class="footer-link">Privacy</a><a class="footer-link">Terms</a>', unsafe_allow_html=True)
#     st.markdown("<p style='text-align: center; color: #666; font-size: 12px;'>AI Teaching Assistant • Built using Streamlit & Ollama • © 2026</p>", unsafe_allow_html=True)

# # --- MAIN RENDERER ---
# def render_landing_page():
#     inject_custom_css()
#     with st.container():
#         render_navbar()
#         render_hero()
#         render_features()
#         render_pricing()
#         render_cta_and_scroller()
#         render_footer()

# def main():
#     st.set_page_config(
#         page_title="NexaAI",
#         page_icon="D:/data scientists/Ai Teaching Assistance/ai-teaching-assistant/Frontend/assets/logo.png",
#         layout="wide",
#         initial_sidebar_state="collapsed"
#     )
#     render_landing_page()

# if __name__ == "__main__":
#     main()

# Frontend/landing_page.py

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
            height: 500px;
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
            border: 1px solid #222;
            border-radius: 16px;
            padding: 25px;
            height: 320px;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
        }

        .cta-card-bg {
            background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 100%);
            border: 1px solid #312e81;
            border-radius: 24px;
            padding: 60px 40px;
            text-align: center;
            margin-bottom: 30px;
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
            font-size: 2rem;
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
            font-size: 14px;
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
                <a href="#pricing_section">Pricing</a>
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
    left, right = st.columns([1.2, 1])

    with left:
        st.markdown("""
            <h1 class="hero-title">Learn Faster.<br>Think Deeper.<br>With AI.</h1>
            <p class="hero-subtitle">
                Your intelligent study partner. Powered by local AI for instant answers,
                personalized learning, and private data.
            </p>
        """, unsafe_allow_html=True)

        c1, c2 = st.columns([1, 1])
        with c1:
            if st.button("🚀 Get Started Free", key="hero_cta", use_container_width=True):
                st.session_state.page = "register"   # ✅ connected to register
                st.rerun()
        with c2:
            if st.button("Log In →", key="hero_login", use_container_width=True):
                st.session_state.page = "login"       # ✅ connected to login
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
def render_features():
    st.write(""); st.write(""); st.write("")
    st.markdown('<span id="features_section"></span>', unsafe_allow_html=True)
    st.markdown("<h2 style='text-align: center; font-size: 40px;'>Engineered for Students</h2>", unsafe_allow_html=True)
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
    st.markdown('<span id="pricing_section"></span>', unsafe_allow_html=True)
    st.markdown("<h2 style='text-align: center; font-size: 40px;'>Simple Pricing</h2>", unsafe_allow_html=True)
    st.write("")

    plans = [
        {
            "title": "Free",
            "price": "$0",
            "subtitle": "For curious learners",
            "features": ["✓ Basic AI usage", "✓ Limited RAG queries", "✓ Community support"],
            "btn_text": "Start for Free",
            "btn_key": "price_free"
        },
        {
            "title": "Pro",
            "price": "$5",
            "subtitle": "For serious students",
            "features": ["✓ Unlimited AI queries", "✓ Advanced AI Insights", "✓ Faster response times", "✓ PDF & Video Analysis"],
            "btn_text": "Get Pro Now",
            "btn_key": "price_pro"
        },
        {
            "title": "Premium",
            "price": "$10",
            "subtitle": "For institutions",
            "features": ["✓ Advanced Analytics", "✓ Priority AI access", "✓ Personalized Learning Path", "✓ API Access"],
            "btn_text": "Contact Sales",
            "btn_key": "price_premium"
        }
    ]

    cols = st.columns(3)
    for i, plan in enumerate(plans):
        with cols[i]:
            features_html = "".join([f"<p style='margin: 8px 0;'>{f}</p>" for f in plan['features']])

            # ✅ Pricing card UI unchanged
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
                </div>
            """, unsafe_allow_html=True)

            # ✅ Real Streamlit buttons — connected to login/profile
            if plan['btn_key'] == "price_free":
                if st.button(plan['btn_text'], key=plan['btn_key'], use_container_width=True):
                    st.session_state.page = "register"   # ✅ goes to register
                    st.rerun()

            elif plan['btn_key'] == "price_pro":
                if st.button(plan['btn_text'], key=plan['btn_key'], use_container_width=True):
                    st.session_state.page = "login"      # ✅ login first then billing
                    st.session_state.redirect_to = "billing"
                    st.rerun()

            elif plan['btn_key'] == "price_premium":
                if st.button(plan['btn_text'], key=plan['btn_key'], use_container_width=True):
                    st.session_state.page = "login"      # ✅ login first then billing
                    st.session_state.redirect_to = "billing"
                    st.rerun()

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

        # ✅ Connected to register page
        if st.button("Get Started for Free", key="cta_btn", use_container_width=True):
            st.balloons()
            st.session_state.page = "register"
            st.rerun()

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
        render_pricing()
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