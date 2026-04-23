# Frontend/app.py

import streamlit as st
from datetime import datetime, date
import sys
import os
from PIL import Image
# -------------------- PAGE CONFIG --------------------
current_dir = os.path.dirname(os.path.abspath(__file__))
logo_path = os.path.join(current_dir, "assets", "logo.png")

try:
    logo_img = Image.open(logo_path)
    st.set_page_config(
        page_title="NexaAI",
        page_icon=logo_img,
        layout="wide",
        initial_sidebar_state="collapsed"  # ✅ Fix — sidebar collapsed on public pages
    )
except FileNotFoundError:
    st.set_page_config(
        page_title="NexaAI",
        page_icon="🎓",
        layout="wide",
        initial_sidebar_state="collapsed"
    )
    
def inject_icon_library():
    st.markdown(
        """
        <link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined" rel="stylesheet">
        """,
        unsafe_allow_html=True
    )

if "ui_init" not in st.session_state:
    st.session_state.ui_init = True

# -------------------- PATH SETUP --------------------
sys.path.append(os.path.join(os.path.dirname(__file__), "modules"))

from modules.landing_page import render_landing_page
from modules.login import render_auth_system
from modules.llm_ui import render_nexus_app
from modules.user_profile import render_app as render_profile
from modules.user_profile import apply_theme, apply_font
from modules.email_reset_pass import render_forgot_password_flow
# -------------------- MAIN --------------------
def main():
    inject_icon_library()
    st.markdown("""
<style>
/* Fix sidebar icon fallback issue */
[data-testid="stSidebar"] button {
    font-family: inherit !important;
    text-transform: none !important;
}

/* Force correct font rendering */
html, body, [class*="css"] {
    font-size: 16px !important;
}
</style>
""", unsafe_allow_html=True)
    # -------------------- SESSION INIT --------------------
    if "page" not in st.session_state:
        st.session_state.page = "landing"

    if "token" not in st.session_state:
        st.session_state.token = None

    if "user" not in st.session_state:
        st.session_state.user = {}

    # ✅ Full profile_data initialization
    if "profile_data" not in st.session_state:
        st.session_state.profile_data = {
            "name": "User",
            "email": "",
            "qualification": "",
            "mobile": "",
            "dob": date(2000, 1, 1),
            "country": "India",
            "username": "",
            "gender": "Other",
            "goal": "",
            "level": "Beginner",
            "interest": [],
        }

    # -------------------- PUBLIC PAGES (NO SIDEBAR) --------------------
    if st.session_state.page in ["landing", "login", "register", "reset","forgot_password"]:
        st.markdown("""
            <style>
                [data-testid="stSidebar"] { display: none !important; }
                [data-testid="stSidebarNav"] { display: none !important; }
            </style>
        """, unsafe_allow_html=True)

        if st.session_state.page == "landing":
            render_landing_page()

        elif st.session_state.page == "login":
            render_auth_system()

        elif st.session_state.page == "register":
            render_auth_system()
        elif st.session_state.page == "reset":
            render_auth_system()
        elif st.session_state.page == "forgot_password":
            render_forgot_password_flow()

    # -------------------- PRIVATE PAGES (SIDEBAR ALLOWED) --------------------
    elif st.session_state.page == "llm_ui":
        # ✅ Guard — redirect to login if no token
        if not st.session_state.get("token"):
            st.session_state.page = "login"
            st.rerun()
        render_nexus_app()

    elif st.session_state.page == "profile":
        # ✅ Guard — redirect to login if no token
        if not st.session_state.get("token"):
            st.session_state.page = "login"
            st.rerun()
        render_profile()
    elif "theme_loaded" not in st.session_state:
        apply_theme()
        apply_font()
        st.session_state.theme_loaded = True

if __name__ == "__main__":
    main()
