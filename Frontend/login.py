import streamlit as st

# 1. Navigation Logic
if "page" not in st.session_state:
    st.session_state.page = "login"
if "users" not in st.session_state:
    st.session_state.users = {}
def go_to(page_name):
    st.session_state.page = page_name
    st.rerun()

# 2. Updated CSS to target "tertiary" buttons
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
    
    /* Main Login Button (Primary) */
    .stButton>button[kind="primary"] {
        width: 200px;
        border-radius: 8px;
        height: 3em;
        background-color: #FF4B4B !important;
        color: white !important;
        border: 2px solid #FF4B4B !important;
    }
    /* Hover effect for Main Buttons: White background, Red text */
    .stButton>button[kind="primary"]:hover {
        background-color: white !important;
        color: #FF4B4B !important;
        border: 2px solid #FF4B4B !important;
    }

    /* "Link" Style Buttons (Targeting Tertiary) */
    div[data-testid="stBaseButton-tertiary"] button {
        color: #007BFF !important;
        background-color: transparent !important;
        border: none !important;
        box-shadow: none !important;
        padding: 0 !important;
    }
    
    div[data-testid="stBaseButton-tertiary"] button p {
        color: #007BFF !important;
    }
    /* Remove hover background but keep the text color blue */
    div[data-testid="stBaseButton-tertiary"]:hover span,
    div[data-testid="stBaseButton-tertiary"] button:active span,
    div[data-testid="stBaseButton-tertiary"] button:focus span{
        color: #0056b3 !important;
        background-color: transparent !important;
        border: none !important;
    }
    /* Ensure no background appears on hover */
    div[data-testid="stBaseButton-tertiary"] button:hover {
        background-color: transparent !important;
        border: none !important;
    }
    /* Target the internal span/text on hover to override Streamlit red */
    div[data-testid="stBaseButton-tertiary"] button:hover:enabled p {
        color: #0056b3 !important;
    }

    .forgot-password-container {
        display: flex;
        justify-content: flex-end;
        padding-top: 1px;
        margin-bottom: -9px !important;
        margin-right: 50px !important;
    }
    * ... keep your existing primary and tertiary button CSS ... */

    /* The container for the "New here?" row */
    .inline-row {
        display: flex;
        flex-direction: row;
        align-items: center; /* Vertical alignment */
        gap: 5px;            /* Space between text and button */
        margin-top: 15px;
    }

    /* Force the Streamlit button container to not take up 100% width */
    .inline-row div[data-testid="stButton"] {
        width: auto !important;
        display: inline-block !important;
    }

    /* Remove the default paragraph margin inside the button text */
    .inline-row div[data-testid="stButton"] p {
        margin: 0 !important;
        line-height: 1 !important;
    }
    /* Subtle AI glow background */
    body {
        background: radial-gradient(circle at top, #0a0f1f, #000000);
    }

    /* Light glow effect */
    section[data-testid="stMain"] > div {
        background: radial-gradient(circle, rgba(255,75,75,0.09) 0%, transparent 70%);
    }
    /* Remove default spacing causing scroll */
    .block-container {
        padding-top: 1rem !important;
        padding-bottom: 0rem !important;
    }

    /* Force full viewport height */
    html, body, [data-testid="stAppViewContainer"] {
        height: 100vh;
        overflow: hidden;
    }

    /* Center content vertically */
    section[data-testid="stMain"] > div {
        display: flex;
        justify-content: center;
        align-items: center;
        height: 100vh;
    }
    </style>
""", unsafe_allow_html=True)

# 3. Layout (1:4:1)
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
            
            # Login and Forgot Password in the SAME ROW
            btn_col1, btn_col2 = st.columns([1, 1])
            with btn_col1:
                if st.button("Log In", type="primary"):
                    if email in st.session_state.users:
                        if st.session_state.users[email]["password"] == password:
                            st.success("Login successful!")
                        else:
                            st.error("Wrong password.")
                    else:
                        st.error("User not found. Please register.")
            with btn_col2:
                st.markdown('<div class="forgot-password-container">', unsafe_allow_html=True)
                if st.button("Forgot Password?", type="tertiary", key="forgot_pass"):
                    go_to("reset")
                st.markdown('</div>', unsafe_allow_html=True)

        # "New here? Create account" in one row
        # Replace the old column logic with this:
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
                    st.session_state.users[email] = {
                        "name": full_name,
                        "password": password
                    }
                    st.success("Account created successfully!")
                

        # Better login link
        st.markdown('<div class="inline-row"><span>Already have an account?</span>', unsafe_allow_html=True)
        if st.button("Log in", type="tertiary", key="back_reg"):
            go_to("login")
        st.markdown('</div>', unsafe_allow_html=True)

    elif st.session_state.page == "reset":
        st.title("Password Reset")
        with st.container(border=True):
            st.text_input("Email")
            if st.button("Reset", type="primary"):
                st.info("Link sent!")
        if st.button("Back to Login", type="tertiary", key="back_reset"):
            go_to("login")