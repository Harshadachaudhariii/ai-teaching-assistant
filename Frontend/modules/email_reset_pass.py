# # # modules/email_reset_pass.py

# # import streamlit as st
# # import time
# # import re
# # import requests

# # # -------------------- BACKEND URL --------------------
# # BACKEND_URL = "http://localhost:8000"

# # # -------------------- HELPERS --------------------
# # def go_to(page):
# #     st.session_state.page = page
# #     st.rerun()

# # def validate_email(email):
# #     return re.match(r"[^@]+@[^@]+\.[^@]+", email)

# # # -------------------- MAIN FLOW --------------------
# # def render_forgot_password_flow():
# #     """
# #     3-Step Password Reset Flow:
# #     Step 1: Email Input      → POST /auth/forgot-password   [⚠️ NEEDS BACKEND]
# #     Step 2: OTP Verification → POST /auth/verify-otp        [⚠️ NEEDS BACKEND]
# #     Step 3: New Password     → POST /auth/reset-password    [✅ CONNECTED]
# #     """

# #     # Initialize step state
# #     if "reset_step" not in st.session_state:
# #         st.session_state.reset_step = "email"
# #     if "otp_timer" not in st.session_state:
# #         st.session_state.otp_timer = 0

# #     # ==========================================
# #     # STEP 1: EMAIL INPUT
# #     # ==========================================
# #     if st.session_state.reset_step == "email":
# #         st.title("Forgot Password")
# #         st.caption("Enter your email to receive a 6-digit verification code.")

# #         with st.container(border=True):
# #             email = st.text_input("Email Address", placeholder="name@company.com")

# #             if st.button("Send OTP", type="primary", use_container_width=True):
# #                 if not validate_email(email):
# #                     st.error("Invalid email format")
# #                 else:
# #                     with st.spinner("Sending OTP..."):
# #                         # ⚠️ STEP 1 NEEDS BACKEND:
# #                         # When backend OTP endpoint is ready, replace time.sleep with:
# #                         #
# #                         # res = requests.post(
# #                         #     f"{BACKEND_URL}/auth/forgot-password",
# #                         #     json={"email": email},
# #                         #     timeout=5
# #                         # )
# #                         # if res.status_code == 200:
# #                         #     st.session_state.reset_email = email
# #                         #     st.session_state.reset_step = "otp"
# #                         #     st.session_state.otp_timer = time.time() + 30
# #                         #     st.rerun()
# #                         # else:
# #                         #     st.error(res.json().get("detail", "Email not found"))
# #                         #
# #                         # ---- MOCK (remove when backend ready) ----
# #                         time.sleep(1.5)
# #                         st.session_state.reset_email = email
# #                         st.session_state.reset_step = "otp"
# #                         st.session_state.otp_timer = time.time() + 30
# #                         st.rerun()
# #                         # ---- END MOCK ----

# #         if st.button("Back to Login", type="tertiary"):
# #             go_to("login")

# #     # ==========================================
# #     # STEP 2: OTP VERIFICATION
# #     # ==========================================
# #     elif st.session_state.reset_step == "otp":
# #         st.title("Verify OTP")
# #         st.caption(f"We've sent a code to **{st.session_state.reset_email}**")

# #         with st.container(border=True):
# #             otp_code = st.text_input(
# #                 "6-Digit Code",
# #                 placeholder="000000",
# #                 help="Enter the 6-digit code sent to your email"
# #             )

# #             if st.button("Verify OTP", type="primary", use_container_width=True):
# #                 if len(otp_code) != 6:
# #                     st.error("Please enter a valid 6-digit code")
# #                 else:
# #                     with st.spinner("Verifying..."):
# #                         # ⚠️ STEP 2 NEEDS BACKEND:
# #                         # When backend OTP verify endpoint is ready, replace mock with:
# #                         #
# #                         # res = requests.post(
# #                         #     f"{BACKEND_URL}/auth/verify-otp",
# #                         #     json={
# #                         #         "email": st.session_state.reset_email,
# #                         #         "otp": otp_code
# #                         #     },
# #                         #     timeout=5
# #                         # )
# #                         # if res.status_code == 200:
# #                         #     st.session_state.reset_step = "new_password"
# #                         #     st.rerun()
# #                         # else:
# #                         #     st.error("Incorrect or expired OTP")
# #                         #
# #                         # ---- MOCK (remove when backend ready) ----
# #                         if otp_code != "123456":
# #                             st.error("Incorrect OTP")
# #                         else:
# #                             time.sleep(1)
# #                             st.session_state.reset_step = "new_password"
# #                             st.rerun()
# #                         # ---- END MOCK ----

# #             # Resend Timer Logic
# #             current_time = time.time()
# #             if current_time < st.session_state.otp_timer:
# #                 remaining = int(st.session_state.otp_timer - current_time)
# #                 st.button(
# #                     f"Resend OTP in {remaining}s",
# #                     disabled=True,
# #                     use_container_width=True
# #                 )
# #                 time.sleep(1)
# #                 st.rerun()
# #             else:
# #                 if st.button("Resend OTP", use_container_width=True):
# #                     # ⚠️ RESEND ALSO NEEDS BACKEND (same as Step 1 endpoint)
# #                     st.session_state.otp_timer = time.time() + 30
# #                     st.toast("New OTP sent!")
# #                     st.rerun()

# #     # ==========================================
# #     # STEP 3: RESET PASSWORD
# #     # ✅ CONNECTED TO BACKEND
# #     # ==========================================
# #     elif st.session_state.reset_step == "new_password":
# #         st.title("Reset Password")
# #         st.caption("Choose a strong password with at least 8 characters.")

# #         with st.container(border=True):
# #             new_pass = st.text_input("New Password", type="password")
# #             conf_pass = st.text_input("Confirm Password", type="password")

# #             # Simple Strength Indicator
# #             if new_pass:
# #                 strength = "Strong" if len(new_pass) >= 8 else "Weak"
# #                 color = "green" if strength == "Strong" else "red"
# #                 st.markdown(
# #                     f"Strength: <span style='color:{color}'>{strength}</span>",
# #                     unsafe_allow_html=True
# #                 )

# #             if st.button("Update Password", type="primary", use_container_width=True):
# #                 if len(new_pass) < 8:
# #                     st.error("Password must be at least 8 characters")
# #                 elif new_pass != conf_pass:
# #                     st.error("Passwords do not match")
# #                 else:
# #                     with st.spinner("Updating password..."):
# #                         try:
# #                             # ✅ STEP 3 — CONNECTED TO BACKEND
# #                             # NOTE: This endpoint needs to be created in backend
# #                             # api/auth.py → POST /auth/reset-password
# #                             res = requests.post(
# #                                 f"{BACKEND_URL}/auth/reset-password",
# #                                 json={
# #                                     "email": st.session_state.reset_email,
# #                                     "new_password": new_pass
# #                                 },
# #                                 timeout=5
# #                             )

# #                             if res.status_code == 200:
# #                                 st.success("Password updated successfully!")
# #                                 time.sleep(1)
# #                                 st.session_state.reset_step = "email"
# #                                 go_to("login")
# #                             else:
# #                                 err = res.json().get("detail", "Password reset failed")
# #                                 st.error(err)

# #                         except requests.exceptions.Timeout:
# #                             st.error("Server timeout. Try again.")
# #                         except Exception as e:
# #                             # ---- FALLBACK if backend not ready ----
# #                             st.warning("Backend not connected. Password reset simulated.")
# #                             time.sleep(1)
# #                             st.session_state.reset_step = "email"
# #                             go_to("login")


# import streamlit as st
# import time
# import requests

# from helpers import (
#     validate_email,
#     go_to,
#     set_step,
#     mock_send_otp,
#     mock_verify_otp,
#     mock_reset_password
# )

# BACKEND_URL = "http://localhost:8000"

# # -------------------- MAIN FLOW --------------------
# def render_forgot_password_flow():

#     if "reset_step" not in st.session_state:
#         st.session_state.reset_step = "email"

#     if "otp_timer" not in st.session_state:
#         st.session_state.otp_timer = 0

#     step = st.session_state.reset_step

#     if step == "email":
#         render_email_step()

#     elif step == "otp":
#         render_otp_step()

#     elif step == "new_password":
#         render_new_password_step()


# # ==========================================
# # STEP 1: EMAIL
# # ==========================================
# def render_email_step():
#     st.title("Forgot Password")
#     st.caption("Enter your email to receive a 6-digit verification code.")

#     with st.container(border=True):
#         email = st.text_input("Email Address")

#         if st.button("Send OTP", type="primary", use_container_width=True):
#             if not validate_email(email):
#                 st.error("Invalid email format")
#                 return

#             with st.spinner("Sending OTP..."):
#                 mock_send_otp(email)

#                 st.session_state.reset_email = email
#                 st.session_state.otp_timer = time.time() + 30
#                 set_step("otp")

#     if st.button("Back to Login"):
#         go_to("login")


# # ==========================================
# # STEP 2: OTP
# # ==========================================
# def render_otp_step():
#     st.title("Verify OTP")
#     st.caption(f"Code sent to **{st.session_state.reset_email}**")

#     with st.container(border=True):

#         otp = st.text_input("Enter 6-digit OTP")

#         if st.button("Verify OTP", type="primary", use_container_width=True):
#             if len(otp) != 6:
#                 st.error("Enter valid OTP")
#                 return

#             with st.spinner("Verifying..."):
#                 if mock_verify_otp(otp):
#                     set_step("new_password")
#                 else:
#                     st.error("Incorrect OTP")

#     # -------- Timer (no rerun loop) --------
#     remaining = int(st.session_state.otp_timer - time.time())

#     if remaining > 0:
#         st.info(f"Resend OTP in {remaining}s")
#     else:
#         if st.button("Resend OTP", use_container_width=True):
#             st.session_state.otp_timer = time.time() + 30
#             st.toast("OTP Sent Again")


# # ==========================================
# # STEP 3: NEW PASSWORD
# # ==========================================
# def render_new_password_step():
#     st.title("Reset Password")
#     st.caption("Minimum 8 characters")

#     with st.container(border=True):

#         new_pass = st.text_input("New Password", type="password")
#         conf_pass = st.text_input("Confirm Password", type="password")

#         # Strength indicator
#         if new_pass:
#             strength = "Strong" if len(new_pass) >= 8 else "Weak"
#             color = "green" if strength == "Strong" else "red"
#             st.markdown(
#                 f"<span style='color:{color}'>Strength: {strength}</span>",
#                 unsafe_allow_html=True
#             )

#         if st.button("Update Password", type="primary", use_container_width=True):

#             if len(new_pass) < 8:
#                 st.error("Password too short")
#                 return

#             if new_pass != conf_pass:
#                 st.error("Passwords do not match")
#                 return

#             with st.spinner("Updating..."):
#                 try:
#                     res = requests.post(
#                         f"{BACKEND_URL}/auth/reset-password",
#                         json={
#                             "email": st.session_state.reset_email,
#                             "new_password": new_pass
#                         },
#                         timeout=5
#                     )

#                     if res.status_code == 200:
#                         st.success("Password updated")
#                         time.sleep(1)
#                         go_to("login")
#                     else:
#                         st.error("Reset failed")

#                 except:
#                     # fallback mock
#                     mock_reset_password()
#                     st.warning("Backend not connected (mock used)")
#                     time.sleep(1)
#                     go_to("login")


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
    Step 1: Email Input      → POST /auth/forgot-password  ✅
    Step 2: OTP Verification → POST /auth/verify-otp       ✅
    Step 3: New Password     → POST /auth/reset-password   ✅
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
# ✅ POST /auth/forgot-password
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
# ✅ POST /auth/verify-otp
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
# ✅ POST /auth/reset-password
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
