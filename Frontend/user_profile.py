import streamlit as st

# 1. Page Config
st.set_page_config(layout="wide", page_title="Streamlit SaaS UI")

# 2. State Management
if 'page' not in st.session_state:
    st.session_state.page = "Profile"

# 3. Enhanced CSS for Default BG and Red Hover Rules
st.markdown(f"""
    <style>
    /* Profile Image Styling */
    .profile-container {{
        text-align: center;
        padding-bottom: 20px;
    }}
    .circular-img {{
        width: 120px; height: 120px;
        border-radius: 50%; object-fit: cover;
        border: 3px solid #ff4b4b;
    }}

    /* RULE: Standard Buttons (White-ish bg, Red text on hover) */
    div.stButton > button {{
        width: 100%;
        border-radius: 8px;
        transition: 0.3s;
    }}
    div.stButton > button:hover {{
        background-color: rgba(255, 255, 255, 0.1) !important;
        color: #ff4b4b !important;
        border-color: #ff4b4b !important;
    }}

    /* RULE: Logout Button (Solid Red bg on hover) */
    .logout-container div.stButton > button:hover {{
        background-color: #ff4b4b !important;
        color: white !important;
        border-color: #ff4b4b !important;
    }}

    /* Layout Spacing */
    .main-card {{
        padding: 20px;
        border-radius: 15px;
        border: 1px solid rgba(49, 51, 63, 0.2);
    }}
    </style>
""", unsafe_allow_html=True)

# 4. Top Navigation (Right Aligned Avatar Simulation)
col_empty, col_nav = st.columns([10, 1])
with col_nav:
    if st.button("👤"):
        st.session_state.page = "Settings"

# 5. Sidebar Logic
with st.sidebar:
    st.markdown('<div class="profile-container">', unsafe_allow_html=True)
    st.markdown('<img src="https://w3schools.com" class="circular-img">', unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center;'>Alex Johnson</h3>", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    st.divider()
    
    if st.button("Profile Interface"): st.session_state.page = "Profile"
    if st.button("Settings Interface"): st.session_state.page = "Settings"
    
    st.markdown('<div class="logout-container">', unsafe_allow_html=True)
    if st.button("Log Out"): st.info("Logged out successfully")
    st.markdown('</div>', unsafe_allow_html=True)

# 6. Page Rendering
if st.session_state.page == "Profile":
    st.title("User Profile")
    with st.container():
        c1, c2 = st.columns(2)
        with c1:
            st.text_input("Name", value="Alex Johnson")
            st.text_input("Qualification", value="Bachelor of Design")
            st.date_input("Date of Birth")
            st.text_input("Username", value="alex_designer")
        with c2:
            st.text_input("Email ID", value="alex@example.com")
            st.text_input("Mobile Number", value="+1 987 654 321")
            st.selectbox("Country", ["USA", "India", "UK", "Germany"])
            st.radio("Gender", ["Male", "Female", "Other"], horizontal=True)
        
        st.write("---")
        # Edit Button with Red Hover
        col_e1, col_e2 = st.columns([8, 2])
        with col_e2:
            st.button("Edit Profile")

elif st.session_state.page == "Settings":
    st.title("System Settings")
    tab1, tab2 = st.tabs(["Appearance", "Help & FAQ"])
    
    with tab1:
        st.write("### Theme Selection")
        t1, t2, t3 = st.columns(3)
        t1.button("Light Mode")
        t2.button("Dark Mode")
        t3.button("System Default")
        
        st.write("### Color Accents")
        st.color_picker("Choose Accent", "#ff4b4b")
        
        st.write("### Typography")
        st.selectbox("Font Family", ["Sans Serif", "Serif", "Monospace"])
        st.slider("Font Size", 12, 24, 16)

    with tab2:
        st.help(st.write)
        st.write("**Version:** 2.0.4-stable")
