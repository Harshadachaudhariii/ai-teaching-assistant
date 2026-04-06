import streamlit as st

# 1. Page Configuration
st.set_page_config(layout="wide", page_title="SaaS User Dashboard")

# 2. Advanced CSS Injection
st.markdown("""
    <style>
    /* Hide Default Streamlit Elements */
    #MainMenu, footer, header {visibility: hidden;}

    /* 1. Circular Profile Logo Trigger */
    div[data-testid="stPopover"] > button {
        border-radius: 50% !important;
        width: 50px !important;
        height: 50px !important;
        padding: 0px !important;
        border: 1px solid #EEEEEE !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
    }
    
    /* Remove the default Chevron Arrow from Popover */
    div[data-testid="stPopover"] svg {
        display: none !important;
    }

    /* 2. Slim Rectangular Dropdown Menu */
    div[data-testid="stPopoverContent"] {
        width: 180px !important;
        padding: 8px !important;
        border-radius: 10px !important;
    }

    /* 3. Base Button Style - NO BORDER, NO BACKGROUND (Initial View) */
    div[data-testid="stPopoverContent"] button {
        background-color: transparent !important;
        border: 1px solid transparent !important; /* Invisible to prevent jumping */
        color: #31333F !important;
        text-align: left !important;
        width: 100% !important;
        transition: all 0.2s ease-in-out !important;
        padding: 8px 12px !important;
    }

    /* 4. HOVER STATE: Profile & Settings (Light Blue + Border) */
    div[data-testid="stPopoverContent"] button:not(:last-child):hover {
        background-color: #F0F2FF !important;
        border: 1px solid #1A73E8 !important;
        color: #1A73E8 !important;
    }

    /* 5. HOVER STATE: Logout (Red BG + Red Border) */
    div[data-testid="stPopoverContent"] button:last-child:hover {
        background-color: #FF4B4B !important;
        border: 1px solid #B91C1C !important;
        color: white !important;
    }

    /* Sidebar Styling */
    .sidebar-header {
        font-size: 24px;
        font-weight: bold;
        margin-bottom: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. State Management
if 'main_page' not in st.session_state:
    st.session_state.main_page = 'Home'
if 'sub_tab' not in st.session_state:
    st.session_state.sub_tab = 'User Details'

# 4. Header with Circular Logo
col_title, col_profile = st.columns([0.9, 0.1])

with col_title:
    if st.session_state.main_page == 'Home':
        st.title("Main Dashboard")

with col_profile:
    # Popover containing the refined hover buttons
    with st.popover("👤"):
        if st.button("Profile", use_container_width=True):
            st.session_state.main_page = 'Profile'
            st.rerun()
        if st.button("Settings", use_container_width=True):
            st.session_state.main_page = 'Settings'
            st.rerun()
        if st.button("Log Out", use_container_width=True):
            st.toast("Logged out successfully!")

st.divider()

# 5. Main Layout Logic
if st.session_state.main_page == 'Home':
    st.info("Welcome! Please open the Profile menu to view details.")
    st.stop()

# Layout with Sidebar (Col1) and Content Area (Col2)
col1, col2 = st.columns([0.25, 0.75], gap="large")

with col1:
    if st.session_state.main_page == 'Profile':
        st.markdown('<p class="sidebar-header">John Doe</p>', unsafe_allow_html=True)
        st.selectbox("Course Selection", ["Sigma Web Development", "Data Science", "Cyber Security"], label_visibility="collapsed")
        st.write("") # Spacer
        if st.button("Username", use_container_width=True):
            st.session_state.sub_tab = 'Username'
        if st.button("User Details", use_container_width=True):
            st.session_state.sub_tab = 'User Details'
            
    elif st.session_state.main_page == 'Settings':
        st.markdown('<p class="sidebar-header">Settings Details</p>', unsafe_allow_html=True)
        if st.button("Website Custom Design", use_container_width=True):
            st.session_state.sub_tab = 'Design'

with col2:
    # DYNAMIC CONTENT AREA
    if st.session_state.main_page == 'Profile':
        if st.session_state.sub_tab == 'Username':
            st.subheader("Login Credentials")
            st.text_input("Username", placeholder="Enter username")
            st.text_input("Password", type="password")
            st.text_input("Confirm Password", type="password")
        
        elif st.session_state.sub_tab == 'User Details':
            st.subheader("User Details")
            st.text_input("Full Name", value="John Doe")
            st.text_input("Email ID", placeholder="example@mail.com")
            st.date_input("Date of Birth (DOB)")
            st.text_area("Bio", placeholder="Tell us about yourself...")

    elif st.session_state.main_page == 'Settings':
        st.subheader("Website Custom Design")
        st.color_picker("Primary Theme Color", "#1A73E8")
        st.select_slider("Font Size", options=["Small", "Default", "Large"])

    # 6. Action Row (Columns 2)
    st.write("---")
    b_col1, b_col2, b_col3 = st.columns([0.15, 0.15, 0.15])
    with b_col1:
        if st.button("← Back"):
            st.session_state.main_page = 'Home'
            st.rerun()
    with b_col2:
        if st.button("Edit"):
            st.info("Edit mode enabled!")
    with b_col3:
        if st.button("Save Changes", type="primary"):
            st.success("Changes Saved!")