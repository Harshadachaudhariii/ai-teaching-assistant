import streamlit as st
import uuid

# -------------------- SESSION SETUP --------------------
if "page" not in st.session_state:
    st.session_state.page = "login"

if "users" not in st.session_state:
    st.session_state.users = {}

if "reset_tokens" not in st.session_state:
    st.session_state.reset_tokens = {}

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False


def go_to(page):
    st.session_state.page = page
    st.rerun()


# -------------------- TOKEN HANDLING --------------------
query_params = st.query_params

if "token" in query_params:
    st.session_state.page = "reset_password"
    st.session_state.token = query_params["token"]


# -------------------- BASIC UI --------------------
st.set_page_config(layout="centered")

st.markdown("""
<style>
#MainMenu, footer, header {visibility: hidden;}

.stButton>button[kind="primary"] {
    width: 200px;
    border-radius: 8px;
    height: 3em;
    background-color: #FF4B4B !important;
    color: white !important;
}

.stButton>button[kind="primary"]:hover {
    background-color: white !important;
    color: #FF4B4B !important;
    border: 2px solid #FF4B4B !important;
}
</style>
""", unsafe_allow_html=True)


# -------------------- LAYOUT --------------------
_, col, _ = st.columns([1, 3, 1])

with col:

    # ---------------- LOGIN ----------------
    if st.session_state.page == "login":

        st.title("Welcome Back")

        email = st.text_input("Email")
        password = st.text_input("Password", type="password")

        if st.button("Login", type="primary"):
            if email in st.session_state.users:
                if st.session_state.users[email]["password"] == password:
                    st.success("Login successful!")
                    st.session_state.logged_in = True
                    st.session_state.current_user = email
                else:
                    st.error("Wrong password")
            else:
                st.error("User not found")

        if st.button("Forgot Password?"):
            go_to("reset")

        if st.button("Create Account"):
            go_to("register")

    # ---------------- REGISTER ----------------
    elif st.session_state.page == "register":

        st.title("Create Account")

        name = st.text_input("Full Name")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        confirm = st.text_input("Confirm Password", type="password")

        if st.button("Sign Up", type="primary"):
            if not name or not email or not password or not confirm:
                st.warning("Fill all fields")
            elif email in st.session_state.users:
                st.error("User already exists")
            elif password != confirm:
                st.error("Passwords do not match")
            else:
                st.session_state.users[email] = {
                    "name": name,
                    "password": password
                }
                st.success("Account created!")
                go_to("login")

        if st.button("Back to Login"):
            go_to("login")

    # ---------------- FORGOT PASSWORD ----------------
    elif st.session_state.page == "reset":

        st.title("Forgot Password")

        email = st.text_input("Enter your email")

        if st.button("Generate Reset Link", type="primary"):
            if email in st.session_state.users:
                token = str(uuid.uuid4())
                st.session_state.reset_tokens[token] = email

                link = f"http://localhost:8501/?token={token}"

                st.info("Copy this link:")
                st.code(link)
            else:
                st.error("Email not found")

        if st.button("Back"):
            go_to("login")

    # ---------------- RESET PASSWORD ----------------
    elif st.session_state.page == "reset_password":

        st.title("Set New Password")

        new_password = st.text_input("New Password", type="password")

        if st.button("Update Password"):
            token = st.session_state.get("token")

            if token in st.session_state.reset_tokens:
                email = st.session_state.reset_tokens[token]

                st.session_state.users[email]["password"] = new_password

                # remove token after use
                del st.session_state.reset_tokens[token]

                # clear URL
                st.query_params.clear()

                st.success("Password updated!")
                go_to("login")
            else:
                st.error("Invalid or expired link")