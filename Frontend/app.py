
import streamlit as st
from datetime import datetime, date
import sys
import os
st.set_page_config(
    page_title="Nexus AI",
    page_icon="🎓",
    layout="wide", # This ensures full width for ALL pages
    initial_sidebar_state="collapsed"
)
# 1. ADD PAGES TO PATH
sys.path.append(os.path.join(os.path.dirname(__file__), "modules"))

from landing_page import render_landing_page
from login import render_auth_system
from llm_ui import render_nexus_app
from user_profile import render_app as render_profile

def main():
    if "page" not in st.session_state:
        st.session_state.page = "landing"
    # Initialize profile_data here so it's available everywhere
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
    # --- PUBLIC PAGES (NO SIDEBAR) ---
    if st.session_state.page in ["landing", "login", "register", "reset"]:
        # Direct CSS injection to kill the sidebar space entirely
        st.markdown("""
            <style>
                [data-testid="stSidebar"] { display: none !important; }
                [data-testid="stSidebarNav"] { display: none !important; }
            </style>
        """, unsafe_allow_html=True)
        
        if st.session_state.page == "landing":
            render_landing_page()
        else:
            render_auth_system()

    # --- PRIVATE PAGES (SIDEBAR ALLOWED) ---
    elif st.session_state.page == "llm_ui":
        render_nexus_app()

    elif st.session_state.page == "profile":
        render_profile()

if __name__ == "__main__":
    main()