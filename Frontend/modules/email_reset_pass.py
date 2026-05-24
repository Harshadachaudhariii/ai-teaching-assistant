# modules/email_reset_pass.py

import streamlit as st
import time
import requests

from helpers import validate_email, go_to, set_step

BACKEND_URL = "http://localhost:8000"

# -------------------- MAIN ORCHESTRATOR --------------------
def render_forgot_password_flow():
    """
    3-Step Password Reset Flow — ALL CONNECTED TO BACKEND:
    Step 1: Email Input      → POST /auth/forgot-password 
    Step 2: OTP Verification → POST /auth/verify-otp      
    Step 3: New Password     → POST /auth/reset-password   
    """
    if "reset_step" not in st.session_state:
        st.session_state.reset_step = "email"
    if "otp_timer" not in st.session_state:
        st.session_state.otp_timer = 0

    step = st.session_state.reset_step

    if step == "email":
        render_email_step()
    elif step == "otp":
        render_otp_step()
    elif step == "new_password":
        render_new_password_step()


# ==========================================
# STEP 1: EMAIL INPUT
# POST /auth/forgot-password
# ==========================================
def render_email_step():
    st.title("Forgot Password")
    st.caption("Enter your email to receive a 6-digit verification code.")

    with st.container(border=True):
        email = st.text_input("Email Address", placeholder="name@gmail.com")

        if st.button("Send OTP", type="primary", use_container_width=True):
            if not validate_email(email):
                st.error("Invalid email format")
                return

            with st.spinner("Sending OTP to your email..."):
                try:
                    res = requests.post(
                        f"{BACKEND_URL}/auth/forgot-password",
                        json={"email": email},
                        timeout=10
                    )

                    if res.status_code == 200:
                        st.session_state.reset_email = email
                        st.session_state.otp_timer   = time.time() + 50
                        st.success("OTP sent! Check your email.")
                        time.sleep(1)
                        set_step("otp")

                    elif res.status_code == 404:
                        st.error("No account found with this email.")
                    else:
                        err = res.json().get("detail", "Failed to send OTP")
                        st.error(err)

                except requests.exceptions.Timeout:
                    st.error("Server timeout. Try again.")
                except Exception as e:
                    st.error(f"Error: {str(e)}")

    if st.button("Back to Login", type="tertiary"):
        go_to("login")


# ==========================================
# STEP 2: OTP VERIFICATION
#  POST /auth/verify-otp
# ==========================================
def render_otp_step():
    st.title("Verify OTP")
    st.caption(f"We've sent a 6-digit code to **{st.session_state.reset_email}**")

    with st.container(border=True):
        otp = st.text_input(
            "6-Digit Code",
            placeholder="000000",
            help="Enter the 6-digit code sent to your email"
        )

        if st.button("Verify OTP", type="primary", use_container_width=True):
            if len(otp) != 6:
                st.error("Please enter a valid 6-digit code")
                return

            with st.spinner("Verifying OTP..."):
                try:
                    res = requests.post(
                        f"{BACKEND_URL}/auth/verify-otp",
                        json={
                            "email": st.session_state.reset_email,
                            "otp":   otp
                        },
                        timeout=5
                    )

                    if res.status_code == 200:
                        st.success("OTP verified!")
                        time.sleep(1)
                        set_step("new_password")

                    elif res.status_code == 400:
                        err = res.json().get("detail", "Incorrect or expired OTP")
                        st.error(err)
                    else:
                        st.error("Verification failed. Try again.")

                except requests.exceptions.Timeout:
                    st.error("Server timeout. Try again.")
                except Exception as e:
                    st.error(f"Error: {str(e)}")

        # -------- Resend Timer --------
        remaining = int(st.session_state.otp_timer - time.time())

        if remaining > 0:
            st.button(
                f"Resend OTP in {remaining}s",
                disabled=True,
                use_container_width=True
            )
            time.sleep(1)
            st.rerun()
        else:
            if st.button("Resend OTP", use_container_width=True):
                with st.spinner("Resending OTP..."):
                    try:
                        res = requests.post(
                            f"{BACKEND_URL}/auth/forgot-password",
                            json={"email": st.session_state.reset_email},
                            timeout=10
                        )
                        if res.status_code == 200:
                            st.session_state.otp_timer = time.time() + 50
                            st.toast("New OTP sent to your email!")
                            st.rerun()
                        else:
                            st.error("Failed to resend OTP")
                    except Exception as e:
                        st.error(f"Error: {str(e)}")


# ==========================================
# STEP 3: RESET PASSWORD
#  POST /auth/reset-password
# ==========================================
def render_new_password_step():
    st.title("Reset Password")
    st.caption("Choose a strong password with at least 8 characters.")

    with st.container(border=True):
        new_pass  = st.text_input("New Password", type="password")
        conf_pass = st.text_input("Confirm Password", type="password")

        # Strength indicator
        if new_pass:
            strength = "Strong" if len(new_pass) >= 8 else "Weak"
            color    = "green"  if strength == "Strong" else "red"
            st.markdown(
                f"Strength: <span style='color:{color}'>{strength}</span>",
                unsafe_allow_html=True
            )

        if st.button("Update Password", type="primary", use_container_width=True):
            if len(new_pass) < 8:
                st.error("Password must be at least 8 characters")
                return
            if new_pass != conf_pass:
                st.error("Passwords do not match")
                return

            with st.spinner("Updating password..."):
                try:
                    res = requests.post(
                        f"{BACKEND_URL}/auth/reset-password",
                        json={
                            "email":        st.session_state.reset_email,
                            "new_password": new_pass
                        },
                        timeout=5
                    )

                    if res.status_code == 200:
                        st.success("Password updated successfully!")
                        time.sleep(1)
                        st.session_state.reset_step = "email"
                        go_to("login")
                    else:
                        err = res.json().get("detail", "Password reset failed")
                        st.error(err)

                except requests.exceptions.Timeout:
                    st.error("Server timeout. Try again.")
                except Exception as e:
                    st.error(f"Error: {str(e)}")
