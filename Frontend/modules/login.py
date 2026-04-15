# modules/login.py

import streamlit as st
import requests
from email_reset_pass import render_forgot_password_flow

# --- 1. CONFIGURATION & STATE ---
def init_auth_state():
    if "reset_tokens" not in st.session_state:
        st.session_state.reset_tokens = {}
    if "page" not in st.session_state:
        st.session_state.page = "login"
    if "token" not in st.session_state:
        st.session_state.token = None
    if "user" not in st.session_state:
        st.session_state.user = {}
    if "profile_data" not in st.session_state:
        st.session_state.profile_data = {
            "name": "",
            "email": ""
        }

def go_to(page_name):
    st.session_state.page = page_name
    st.rerun()

# --- 2. UI STYLES --- (unchanged)
def inject_auth_styles():
    st.markdown("""
        <style>
         #MainMenu, footer, header {visibility: hidden;}
        .login-card {
            background-color: #ffffff;
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            width: 100%; 
            margin: auto;
        }
        .stButton>button[kind="primary"],
        div[data-testid^="stButton"] button[kind="primary"] {
            width: 200px;
            border-radius: 8px;
            height: 3em;
            background-color: #3b82f6 !important;
            color: white !important;
            border: 2px solid #3b82f6 !important;
        }
        .stButton>button[kind="primary"]:hover,
        div[data-testid^="stButton"] button[kind="primary"]:hover {
            color: #0056b3 !important;
            background-color: white !important;
            border: 2px solid #3b82f6 !important;
        }
        div[data-testid="stBaseButton-tertiary"] button,
        div[data-testid="stBaseButton-tertiary"] button span,
        div[data-testid="stBaseButton-tertiary"] button p,
        div[data-testid^="stButton"] button[kind="tertiary"],
        div[data-testid^="stButton"] button[kind="tertiary"] span,
        div[data-testid^="stButton"] button[kind="tertiary"] p {
            color: #3b82f6 !important;
            background-color: transparent !important;
            border: none !important;
            box-shadow: none !important;
            padding: 0 !important;
        }
        div[data-testid="stBaseButton-tertiary"] button:hover,
        div[data-testid="stBaseButton-tertiary"] button:hover span,
        div[data-testid="stBaseButton-tertiary"] button:hover p,
        div[data-testid="stBaseButton-tertiary"] button:focus,
        div[data-testid="stBaseButton-tertiary"] button:focus span,
        div[data-testid="stBaseButton-tertiary"] button:focus p,
        div[data-testid^="stButton"] button[kind="tertiary"]:hover,
        div[data-testid^="stButton"] button[kind="tertiary"]:focus {
            color: #0056b3 !important;
            background-color: transparent !important;
            border: none !important;
            box-shadow: none !important;
        }
        div[data-testid^="stButton"] button:focus,
        div[data-testid="stBaseButton-tertiary"] button:focus {
            outline: none !important;
            box-shadow: none !important;
        }
        .forgot-password-container {
            display: flex;
            justify-content: flex-end;
            padding-top: 1px;
            margin-bottom: -9px !important;
            margin-right: 50px !important;
            color: #3b82f6 !important;
        }
        .inline-row {
            display: flex;
            flex-direction: row;
            align-items: center;
            gap: 5px;
            margin-top: -1px;
        }
        .inline-row div[data-testid="stButton"] {
            width: auto !important;
            display: inline-block !important;
        }
        .inline-row div[data-testid="stButton"] p {
            margin: 0 !important;
            line-height: 1 !important;
        }
        body {
            background: radial-gradient(circle at top, #0a0f1f, #000000);
        }
        section[data-testid="stMain"] > div {
            background: radial-gradient(circle, rgba(29, 18, 227,0.09) 0%, transparent 70%);
        }
        .block-container {
            padding-top: 1rem !important;
            padding-bottom: 0rem !important;
        }
        html, body, [data-testid="stAppViewContainer"] {
            height: 100vh;
            overflow: hidden;
        }
        section[data-testid="stMain"] > div {
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
        }
        </style>
    """, unsafe_allow_html=True)

# --- 3. MASTER WRAPPER FUNCTION ---
def render_auth_system():
    init_auth_state()
    inject_auth_styles()

    _, col, _ = st.columns([1, 4, 1])

    with col:
        if st.session_state.page == "login":
            st.markdown("""
            <div style="text-align: center; margin-bottom: 10px;">
                <h3 style="margin-bottom: 5px;">AI Learning Assistant</h3>
                <p style="color: gray; font-size: 14px;">
                    Ask questions. Get instant answers. Learn smarter.
                </p>
            </div>
            """, unsafe_allow_html=True)
            st.title("Welcome Back")
            st.caption("Continue your learning journey with AI assistance.")

            with st.container(border=True):
                email = st.text_input("Email Address", placeholder="name@company.com")
                password = st.text_input("Password", type="password", placeholder="••••••••")

                btn_col1, btn_col2 = st.columns([1, 1])
                with btn_col1:
                    if st.button("Log In", type="primary"):
                        if not email or not password:
                            st.warning("Please enter email and password.")
                        else:
                            try:
                                # ✅ Step 1: Login
                                res = requests.post(
                                    "http://localhost:8000/auth/login",
                                    json={"email": email, "password": password},
                                    timeout=5
                                )

                                if res.status_code == 200:
                                    data = res.json()
                                    token = data.get("access_token")

                                    if not token:
                                        st.error("Login failed: No token received")
                                    else:
                                        # ✅ Step 2: Save token
                                        st.session_state.token = token

                                        # ✅ Step 3: Fetch user info
                                        me_res = requests.get(
                                            "http://localhost:8000/auth/me",
                                            headers={"Authorization": f"Bearer {token}"},
                                            timeout=5
                                        )

                                        if me_res.status_code == 200:
                                            user_data = me_res.json()
                                            st.session_state.user = user_data
                                            st.session_state.profile_data["name"] = user_data.get("name", "")
                                            st.session_state.profile_data["email"] = user_data.get("email", "")

                                        st.success("Login successful!")
                                        go_to("llm_ui")
                                else:
                                    try:
                                        err = res.json().get("detail", "Login failed")
                                    except:
                                        err = "Login failed (server error)"
                                    st.error(err)

                            except requests.exceptions.Timeout:
                                st.error("Server timeout. Try again.")
                            except Exception as e:
                                st.error(f"Backend error: {e}")

                with btn_col2:
                    st.markdown('<div class="forgot-password-container">', unsafe_allow_html=True)
                    if st.button("Forgot Password?", type="tertiary", key="forgot_pass"):
                        go_to("reset")
                    st.markdown('</div>', unsafe_allow_html=True)

            st.markdown('<div class="inline-row"><span>New here?</span>', unsafe_allow_html=True)
            if st.button("Create an account", type="tertiary", key="create_link"):
                go_to("register")
            st.markdown('</div>', unsafe_allow_html=True)

        elif st.session_state.page == "register":
            st.title("Create Your AI Account")
            st.caption("Start your journey with AI-powered learning.")

            with st.container(border=True):
                full_name = st.text_input("Full Name")
                email = st.text_input("Email Address")
                password = st.text_input("Password", type="password")
                confirm_password = st.text_input("Confirm Password", type="password")

                if st.button("Create Account", type="primary"):
                    if not full_name or not email or not password or not confirm_password:
                        st.warning("Please fill all fields.")
                    elif password != confirm_password:
                        st.error("Passwords do not match.")
                    else:
                        try:
                            # ✅ Register API call
                            res = requests.post(
                                "http://localhost:8000/auth/register",
                                json={
                                    "name": full_name,
                                    "email": email,
                                    "password": password
                                },
                                timeout=5
                            )

                            if res.status_code == 200:
                                st.success("Account created successfully!")
                                st.info("Please log in with your credentials.")
                                go_to("login")
                            else:
                                st.error(res.json().get("detail", "Registration failed"))

                        except requests.exceptions.Timeout:
                            st.error("Server timeout. Try again.")
                        except Exception as e:
                            st.error(f"Backend error: {e}")

            st.markdown('<div class="inline-row"><span>Already have an account?</span>', unsafe_allow_html=True)
            if st.button("Log in", type="tertiary", key="back_reg"):
                go_to("login")
            st.markdown('</div>', unsafe_allow_html=True)

        elif st.session_state.page == "reset":
            render_forgot_password_flow()

# --- 4. EXECUTION ---
if __name__ == "__main__":
    render_auth_system()