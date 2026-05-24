# Frontend/app.py
import streamlit as st
from datetime import date
import sys
import os
import requests
from PIL import Image
from utils.cookies import cookies

# -------------------- PAGE CONFIG --------------------
current_dir = os.path.dirname(os.path.abspath(__file__))
logo_path   = os.path.join(current_dir, "assets", "logo.png")

try:
    logo_img = Image.open(logo_path)
    st.set_page_config(page_title="NexaAI", page_icon=logo_img, layout="wide",
                       initial_sidebar_state="collapsed")
except FileNotFoundError:
    st.set_page_config(page_title="NexaAI", page_icon="🎓", layout="wide",
                       initial_sidebar_state="collapsed")



# -------------------- PATH SETUP --------------------
sys.path.append(os.path.join(os.path.dirname(__file__), "modules"))

from modules.login           import render_auth_system
from modules.llm_ui          import render_nexus_app
from modules.email_reset_pass import render_forgot_password_flow

BACKEND_URL = "http://localhost:8000"


# ============================================================
#4 — Token Validation Helper
# ============================================================
def _validate_token(token: str) -> dict | None:
    """
    Calls /auth/me to verify token is still valid.
    Returns user dict on success, None on failure.
    Cached in session_state so we only call once per session.
    """
    try:
        res = requests.get(
            f"{BACKEND_URL}/auth/me",
            headers={"Authorization": f"Bearer {token}"},
            timeout=4,
        )
        if res.status_code == 200:
            return res.json()
    except Exception:
        pass
    return None

def inject_icon_library():
    st.markdown('<link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined" rel="stylesheet">',
                unsafe_allow_html=True)

# ============================================================
# MAIN
# ============================================================
def main():
    inject_icon_library()

    # ── Session defaults ──
    if "page" not in st.session_state:
        st.session_state.page = "llm_ui"

    if "token" not in st.session_state:
        st.session_state.token = None

    if "user" not in st.session_state:
        st.session_state.user = {}

    if "token_valid" not in st.session_state:
        st.session_state.token_valid = False


    # ============================================================
    # LOAD TOKEN FROM COOKIES AFTER REFRESH
    # ============================================================
    if not st.session_state.token:

        saved_token = cookies.get("token")

        if saved_token:
            st.session_state.token = saved_token


    # ============================================================
    #  LOGIN REDIRECT
    # Runs on every page load before rendering anything.
    # If token is present and valid → skip login → go to llm_ui.
    # ============================================================
    token = st.session_state.get("token")
    if token and not st.session_state.get("token_valid"):
        user_data = _validate_token(token)
        if user_data:
            # Token valid — sync user data and redirect
            # Token valid — sync user data and redirect
            st.session_state.token_valid = True
            st.session_state.user = user_data

            # Restore sidebar profile after refresh
            st.session_state.profile_data = {
                "name": user_data.get("name", ""),
                "email": user_data.get("email", "")
}
            # Only redirect if user is on a public page (not already in app)
            if st.session_state.page in ("login", "register", "reset"):
                st.session_state.page = "llm_ui"
                st.rerun()
        else:
            # Token expired or invalid — clear and show login
            st.session_state.token       = None
            st.session_state.token_valid = False
            st.session_state.page        = "login"
    

    # ── Public pages (no sidebar) ──
    if st.session_state.page in ("login", "register", "reset", "forgot_password"):
        st.markdown("""
            <style>
                [data-testid="stSidebar"] { display: none !important; }
                [data-testid="stSidebarNav"] { display: none !important; }
            </style>
        """, unsafe_allow_html=True)

        if st.session_state.page in ("login","register","reset"): render_auth_system()
        elif st.session_state.page == "forgot_password": render_forgot_password_flow()

    # ── Private pages ──
    elif st.session_state.page == "llm_ui":
        render_nexus_app()
 
if __name__ == "__main__":
    main()
    
    



