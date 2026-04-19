import streamlit as st
from email_reset_pass import render_forgot_password_flow

# Initialize page state
if "page" not in st.session_state:
    st.session_state.page = "forgot"

# Routing
if st.session_state.page == "forgot":
    render_forgot_password_flow()

elif st.session_state.page == "login":
    st.title("Login Page")
    st.write("Redirected after password reset")