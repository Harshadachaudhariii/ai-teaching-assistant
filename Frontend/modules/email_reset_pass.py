# import streamlit as st
# import uuid

# # -------------------- SESSION SETUP --------------------
# if "page" not in st.session_state:
#     st.session_state.page = "login"

# if "users" not in st.session_state:
#     st.session_state.users = {}

# if "reset_tokens" not in st.session_state:
#     st.session_state.reset_tokens = {}

# if "logged_in" not in st.session_state:
#     st.session_state.logged_in = False


# def go_to(page):
#     st.session_state.page = page
#     st.rerun()


# # -------------------- TOKEN HANDLING --------------------
# query_params = st.query_params

# if "token" in query_params:
#     st.session_state.page = "reset_password"
#     st.session_state.token = query_params["token"]


# # -------------------- BASIC UI --------------------
# st.set_page_config(layout="centered")

# st.markdown("""
# <style>
# #MainMenu, footer, header {visibility: hidden;}

# .stButton>button[kind="primary"] {
#     width: 200px;
#     border-radius: 8px;
#     height: 3em;
#     background-color: #FF4B4B !important;
#     color: white !important;
# }

# .stButton>button[kind="primary"]:hover {
#     background-color: white !important;
#     color: #FF4B4B !important;
#     border: 2px solid #FF4B4B !important;
# }
# </style>
# """, unsafe_allow_html=True)


# # -------------------- LAYOUT --------------------
# _, col, _ = st.columns([1, 3, 1])

# with col:

#     # ---------------- LOGIN ----------------
#     if st.session_state.page == "login":

#         st.title("Welcome Back")

#         email = st.text_input("Email")
#         password = st.text_input("Password", type="password")

#         if st.button("Login", type="primary"):
#             if email in st.session_state.users:
#                 if st.session_state.users[email]["password"] == password:
#                     st.success("Login successful!")
#                     st.session_state.logged_in = True
#                     st.session_state.current_user = email
#                 else:
#                     st.error("Wrong password")
#             else:
#                 st.error("User not found")

#         if st.button("Forgot Password?"):
#             go_to("reset")

#         if st.button("Create Account"):
#             go_to("register")

#     # ---------------- REGISTER ----------------
#     elif st.session_state.page == "register":

#         st.title("Create Account")

#         name = st.text_input("Full Name")
#         email = st.text_input("Email")
#         password = st.text_input("Password", type="password")
#         confirm = st.text_input("Confirm Password", type="password")

#         if st.button("Sign Up", type="primary"):
#             if not name or not email or not password or not confirm:
#                 st.warning("Fill all fields")
#             elif email in st.session_state.users:
#                 st.error("User already exists")
#             elif password != confirm:
#                 st.error("Passwords do not match")
#             else:
#                 st.session_state.users[email] = {
#                     "name": name,
#                     "password": password
#                 }
#                 st.success("Account created!")
#                 go_to("login")

#         if st.button("Back to Login"):
#             go_to("login")

#     # ---------------- FORGOT PASSWORD ----------------
#     elif st.session_state.page == "reset":

#         st.title("Forgot Password")

#         email = st.text_input("Enter your email")

#         if st.button("Generate Reset Link", type="primary"):
#             if email in st.session_state.users:
#                 token = str(uuid.uuid4())
#                 st.session_state.reset_tokens[token] = email

#                 link = f"http://localhost:8501/?token={token}"

#                 st.info("Copy this link:")
#                 st.code(link)
#             else:
#                 st.error("Email not found")

#         if st.button("Back"):
#             go_to("login")

#     # ---------------- RESET PASSWORD ----------------
#     elif st.session_state.page == "reset_password":

#         st.title("Set New Password")

#         new_password = st.text_input("New Password", type="password")

#         if st.button("Update Password"):
#             token = st.session_state.get("token")

#             if token in st.session_state.reset_tokens:
#                 email = st.session_state.reset_tokens[token]

#                 st.session_state.users[email]["password"] = new_password

#                 # remove token after use
#                 del st.session_state.reset_tokens[token]

#                 # clear URL
#                 st.query_params.clear()

#                 st.success("Password updated!")
#                 go_to("login")
#             else:
#                 st.error("Invalid or expired link")

import streamlit as st
import time
import re

def go_to(page):
    st.session_state.page = page
    st.rerun()

def validate_email(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)

def render_auth_system():
    # ... (Keep your init_auth_state and styles) ...
    
    # Initialize Specific Reset States
    if "reset_step" not in st.session_state:
        st.session_state.reset_step = "email" # email -> otp -> new_password
    if "otp_timer" not in st.session_state:
        st.session_state.otp_timer = 0

    _, col, _ = st.columns([1, 4, 1])

    with col:
        if st.session_state.page == "reset":
            render_forgot_password_flow()

def render_forgot_password_flow():
    """Main Orchestrator for the Forgot Password Flow"""
    if "reset_step" not in st.session_state:
        st.session_state.reset_step = "email"
    # STEP 1: EMAIL INPUT
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
                        time.sleep(1.5) # Simulate API: POST /auth/forgot-password
                        st.session_state.reset_email = email
                        st.session_state.reset_step = "otp"
                        st.session_state.otp_timer = time.time() + 30
                        st.rerun()
        
        if st.button("Back to Login", type="tertiary"):
            go_to("login")

    # STEP 2: OTP VERIFICATION
    elif st.session_state.reset_step == "otp":
        st.title("Verify OTP")
        st.caption(f"We've sent a code to **{st.session_state.reset_email}**")
        
        with st.container(border=True):
            # 6-digit OTP Input
            otp_code = st.text_input("6-Digit Code", placeholder="000000", help="Enter the 6-digit code sent to your email")
            
            if st.button("Verify OTP", type="primary", use_container_width=True):
                if len(otp_code) != 6:
                    st.error("Please enter a valid 6-digit code")
                elif otp_code != "123456": # Mock Validation
                    st.error("Incorrect OTP")
                else:
                    with st.spinner("Verifying..."):
                        time.sleep(1) # Simulate API: POST /auth/verify-otp
                        st.session_state.reset_step = "new_password"
                        st.rerun()

            # Resend Timer Logic
            current_time = time.time()
            if current_time < st.session_state.otp_timer:
                remaining = int(st.session_state.otp_timer - current_time)
                st.button(f"Resend OTP in {remaining}s", disabled=True, use_container_width=True)
                time.sleep(1)
                st.rerun()
            else:
                if st.button("Resend OTP", use_container_width=True):
                    st.session_state.otp_timer = time.time() + 30
                    st.toast("New OTP sent!")
                    st.rerun()

    # STEP 3: RESET PASSWORD
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
                st.markdown(f"Strength: <span style='color:{color}'>{strength}</span>", unsafe_allow_html=True)

            if st.button("Update Password", type="primary", use_container_width=True):
                if len(new_pass) < 8:
                    st.error("Password must be at least 8 characters")
                elif new_pass != conf_pass:
                    st.error("Passwords do not match")
                else:
                    with st.spinner("Updating password..."):
                        time.sleep(1.5) # Simulate API: POST /auth/reset-password
                        # Update actual user DB
                        email = st.session_state.reset_email
                        if email in st.session_state.users:
                            st.session_state.users[email]['password'] = new_pass
                        
                        st.success("Password updated successfully!")
                        time.sleep(1)
                        # Reset the flow and go home
                        st.session_state.reset_step = "email"
                        go_to("login")