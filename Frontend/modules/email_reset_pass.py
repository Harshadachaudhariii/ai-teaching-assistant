# modules/email_reset_pass.py

import streamlit as st
import time
import re
import requests

# -------------------- BACKEND URL --------------------
BACKEND_URL = "http://localhost:8000"

# -------------------- HELPERS --------------------
def go_to(page):
    st.session_state.page = page
    st.rerun()

def validate_email(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)

# -------------------- MAIN FLOW --------------------
def render_forgot_password_flow():
    """
    3-Step Password Reset Flow:
    Step 1: Email Input      → POST /auth/forgot-password   [⚠️ NEEDS BACKEND]
    Step 2: OTP Verification → POST /auth/verify-otp        [⚠️ NEEDS BACKEND]
    Step 3: New Password     → POST /auth/reset-password    [✅ CONNECTED]
    """

    # Initialize step state
    if "reset_step" not in st.session_state:
        st.session_state.reset_step = "email"
    if "otp_timer" not in st.session_state:
        st.session_state.otp_timer = 0

    # ==========================================
    # STEP 1: EMAIL INPUT
    # ==========================================
    if st.session_state.reset_step == "email":
        st.title("Forgot Password")
        st.caption("Enter your email to receive a 6-digit verification code.")

        with st.container(border=True):
            email = st.text_input("Email Address", placeholder="name@company.com")

            if st.button("Send OTP", type="primary", use_container_width=True):
                if not validate_email(email):
                    st.error("Invalid email format")
                else:
                    with st.spinner("Sending OTP..."):
                        # ⚠️ STEP 1 NEEDS BACKEND:
                        # When backend OTP endpoint is ready, replace time.sleep with:
                        #
                        # res = requests.post(
                        #     f"{BACKEND_URL}/auth/forgot-password",
                        #     json={"email": email},
                        #     timeout=5
                        # )
                        # if res.status_code == 200:
                        #     st.session_state.reset_email = email
                        #     st.session_state.reset_step = "otp"
                        #     st.session_state.otp_timer = time.time() + 30
                        #     st.rerun()
                        # else:
                        #     st.error(res.json().get("detail", "Email not found"))
                        #
                        # ---- MOCK (remove when backend ready) ----
                        time.sleep(1.5)
                        st.session_state.reset_email = email
                        st.session_state.reset_step = "otp"
                        st.session_state.otp_timer = time.time() + 30
                        st.rerun()
                        # ---- END MOCK ----

        if st.button("Back to Login", type="tertiary"):
            go_to("login")

    # ==========================================
    # STEP 2: OTP VERIFICATION
    # ==========================================
    elif st.session_state.reset_step == "otp":
        st.title("Verify OTP")
        st.caption(f"We've sent a code to **{st.session_state.reset_email}**")

        with st.container(border=True):
            otp_code = st.text_input(
                "6-Digit Code",
                placeholder="000000",
                help="Enter the 6-digit code sent to your email"
            )

            if st.button("Verify OTP", type="primary", use_container_width=True):
                if len(otp_code) != 6:
                    st.error("Please enter a valid 6-digit code")
                else:
                    with st.spinner("Verifying..."):
                        # ⚠️ STEP 2 NEEDS BACKEND:
                        # When backend OTP verify endpoint is ready, replace mock with:
                        #
                        # res = requests.post(
                        #     f"{BACKEND_URL}/auth/verify-otp",
                        #     json={
                        #         "email": st.session_state.reset_email,
                        #         "otp": otp_code
                        #     },
                        #     timeout=5
                        # )
                        # if res.status_code == 200:
                        #     st.session_state.reset_step = "new_password"
                        #     st.rerun()
                        # else:
                        #     st.error("Incorrect or expired OTP")
                        #
                        # ---- MOCK (remove when backend ready) ----
                        if otp_code != "123456":
                            st.error("Incorrect OTP")
                        else:
                            time.sleep(1)
                            st.session_state.reset_step = "new_password"
                            st.rerun()
                        # ---- END MOCK ----

            # Resend Timer Logic
            current_time = time.time()
            if current_time < st.session_state.otp_timer:
                remaining = int(st.session_state.otp_timer - current_time)
                st.button(
                    f"Resend OTP in {remaining}s",
                    disabled=True,
                    use_container_width=True
                )
                time.sleep(1)
                st.rerun()
            else:
                if st.button("Resend OTP", use_container_width=True):
                    # ⚠️ RESEND ALSO NEEDS BACKEND (same as Step 1 endpoint)
                    st.session_state.otp_timer = time.time() + 30
                    st.toast("New OTP sent!")
                    st.rerun()

    # ==========================================
    # STEP 3: RESET PASSWORD
    # ✅ CONNECTED TO BACKEND
    # ==========================================
    elif st.session_state.reset_step == "new_password":
        st.title("Reset Password")
        st.caption("Choose a strong password with at least 8 characters.")

        with st.container(border=True):
            new_pass = st.text_input("New Password", type="password")
            conf_pass = st.text_input("Confirm Password", type="password")

            # Simple Strength Indicator
            if new_pass:
                strength = "Strong" if len(new_pass) >= 8 else "Weak"
                color = "green" if strength == "Strong" else "red"
                st.markdown(
                    f"Strength: <span style='color:{color}'>{strength}</span>",
                    unsafe_allow_html=True
                )

            if st.button("Update Password", type="primary", use_container_width=True):
                if len(new_pass) < 8:
                    st.error("Password must be at least 8 characters")
                elif new_pass != conf_pass:
                    st.error("Passwords do not match")
                else:
                    with st.spinner("Updating password..."):
                        try:
                            # ✅ STEP 3 — CONNECTED TO BACKEND
                            # NOTE: This endpoint needs to be created in backend
                            # api/auth.py → POST /auth/reset-password
                            res = requests.post(
                                f"{BACKEND_URL}/auth/reset-password",
                                json={
                                    "email": st.session_state.reset_email,
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
                            # ---- FALLBACK if backend not ready ----
                            st.warning("Backend not connected. Password reset simulated.")
                            time.sleep(1)
                            st.session_state.reset_step = "email"
                            go_to("login")