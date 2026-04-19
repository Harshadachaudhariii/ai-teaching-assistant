import re
import time
import streamlit as st

# -------------------- VALIDATION --------------------
def validate_email(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)

# -------------------- NAVIGATION --------------------
def go_to(page):
    st.session_state.page = page
    st.rerun()

def set_step(step):
    st.session_state.reset_step = step
    st.rerun()

# -------------------- MOCK LOGIC --------------------
def mock_send_otp(email):
    time.sleep(1)
    return True

def mock_verify_otp(otp):
    time.sleep(1)
    return otp == "123456"

def mock_reset_password():
    time.sleep(1)
    return True