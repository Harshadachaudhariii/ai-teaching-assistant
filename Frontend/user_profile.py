import streamlit as st
import datetime
import re
import pyotp
import qrcode
from PIL import Image
import io
import random

st.set_page_config(layout="wide", page_title="Streamlit SaaS UI", initial_sidebar_state="expanded")

# =========================
# PROFESSIONAL CSS (Updated)
# =========================
st.markdown("""
<style>
#MainMenu, footer {visibility: hidden;}

html, body {
    background-color: #0a0a0a !important;
}

/* Sidebar Styling */
[data-testid="stSidebar"] {
    background-color: #0e0e0e !important;
    border-right: 1px solid #1e293b;
}

/* UNIVERSAL BUTTON THEME: Transparent, Blue Hover */
div.stButton > button {
    width: 100%;
    text-align: left;
    background-color: transparent !important;
    color: #ded1d1 !important;
    border: 1px solid transparent !important; /* Normal state transparent border */
    box-shadow: none !important;
    border-radius: 8px;
    font-size: 14px;
    transition: all 0.3s ease;
    padding: 10px 10px;
}

/* Professional Hover Effect */
div.stButton > button:hover {
    color: #2563eb !important;
    border: 1px solid #2563eb !important;
    background-color: transparent !important;
}

/* Popover Position & Style */
.stPopover {
    float: right;
    margin-top: -30px;
    margin-left: 1040px;
}
.stPopover > div:first-child > button {
    border-radius: 50% !important;
    width: 40px !important;
    height: 40px !important;
    background-color: #111111 !important;
    border: 1px solid #222 !important;
}

/* Sidebar Titles */
.sidebar-title {
    font-size: 11px;
    letter-spacing: 1px;
    color: #555;
    margin-top: 15px;
    margin-bottom: 5px;
    padding-left: 10px;
    font-weight: bold;
}

.separator {
    border-bottom: 1px solid #222;
    margin: 20px 0;
}

.logout-container {
    position: absolute;
    bottom: 20px;
    width: 100%;
}
</style>
""", unsafe_allow_html=True)

# =========================
# SESSION STATE (Your Logic)
# =========================
if "view" not in st.session_state:
    st.session_state.view = "Profile"
    
if "edit_mode" not in st.session_state:
    st.session_state.edit_mode = False
    
if "profile_data" not in st.session_state:
    st.session_state.profile_data = {
        "name": "Alex Johnson",
        "email": "alex@example.com",
        "qualification": "Bachelor of Design",
        "mobile": "+1 987 654 321",
        "dob": datetime.date(2000, 1, 1),
        "country": "India",
        "username": "alex_designer",
        "gender": "Male",
        "goal": "Get UI/UX Job",
        "level": "Intermediate",
        "interest": ["UI/UX"],
    }

# =========================
# FUNCTIONS (Your Logic)
# =========================
def logout():
    st.session_state.clear()
    st.success("Logged out successfully")
    st.rerun()
    
def get_password_status(password):
    return {
        "8+ characters": len(password) >= 8,
        "A number": bool(re.search(r"\d", password)),
        "A special character": bool(re.search(r"[@$!%*?&]", password)),
        "Uppercase letter": bool(re.search(r"[A-Z]", password)),
    }

# =========================
# TOP RIGHT PROFILE MENU
# =========================
with st.popover("👤"):
    st.markdown(f"**{st.session_state.profile_data['name']}**")
    if st.button("View Profile", use_container_width=True):
        st.session_state.view = "Profile"
        st.rerun()
    if st.button("Logout", type="secondary", use_container_width=True):
        logout()

# =========================
# SIDEBAR (Your Logic)
# =========================
with st.sidebar:
    st.markdown("""
    <div style="display:flex; align-items:center; gap:10px; padding-left:10px;">
        <div style="width:40px;height:40px;border-radius:50%;background:#2563eb;color:white;display:flex;align-items:center;justify-content:center;font-weight:bold;">A</div>
        <div><b style="color:white;">Alex Johnson</b><br><span style='font-size:12px;color:gray;'>UI/UX Designer</span></div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="separator"></div>', unsafe_allow_html=True)
    if st.button("Back", use_container_width=True):
        st.session_state.view = "Landing"
        st.rerun()
    st.markdown('<div class="sidebar-title">ACCOUNT</div>', unsafe_allow_html=True)

    if st.button("👤 Profile"): st.session_state.view = "Profile"
    if st.button("⚙️ Settings"): st.session_state.view = "Settings"
    if st.button("🔐 Security"): st.session_state.view = "Security"
    if st.button("🔗 Connected Accounts"): st.session_state.view = "Connections"
    if st.button("🛡️ Privacy"): st.session_state.view = "Privacy"

    st.markdown('<div class="sidebar-title">INSIGHTS</div>', unsafe_allow_html=True)
    if st.button("📊 Profile Insights"): st.session_state.view = "Insights"
    if st.button("🤖 AI Insights"): st.session_state.view = "AI"
    if st.button("🕒 Activity Log"): st.session_state.view = "Activity"

    st.markdown('<div class="sidebar-title">OTHER</div>', unsafe_allow_html=True)
    if st.button("💳 Billing"): st.session_state.view = "Billing"
    if st.button("ℹ️ About"): st.session_state.view = "About"

    st.markdown('<div class="logout-container">', unsafe_allow_html=True)
    if st.button("🚪 Logout"): logout()
    st.markdown('</div>', unsafe_allow_html=True)

# =========================
# PAGES (Your Logic)
# =========================
if st.session_state.view == "Profile":
    st.title("User Profile")
    data = st.session_state.profile_data
    disabled = not st.session_state.edit_mode

    c1, c2 = st.columns(2)
    with c1:
        name = st.text_input("Name", data["name"], disabled=disabled)
        qualification = st.text_input("Qualification", data.get("qualification", ""), disabled=disabled)
        dob = st.date_input("Date of Birth", value=data["dob"], disabled=disabled)
        username = st.text_input("Username", data["username"], disabled=disabled)

    with c2:
        email = st.text_input("Email ID", data["email"], disabled=disabled)
        mobile = st.text_input("Mobile", data["mobile"], disabled=disabled)
        country = st.selectbox("Country", ["USA", "India", "UK"], disabled=disabled)
        gender = st.radio("Gender", ["Male", "Female", "Other"], disabled=disabled)

    st.markdown("### Learning Profile")
    col3, col4 = st.columns(2)
    with col3:
        goal = st.text_input("Learning Goal", data["goal"], disabled=disabled)
        level = st.selectbox("Skill Level", ["Beginner", "Intermediate", "Advanced"], 
                             index=["Beginner","Intermediate","Advanced"].index(data["level"]), disabled=disabled)
    with col4:
        interest = st.multiselect("Interested Domains", ["UI/UX", "AI", "Web Dev", "Data Science"], 
                                  default=data["interest"], disabled=disabled)

    st.markdown('<div class="separator"></div>', unsafe_allow_html=True)
    col1, col2, col3 = st.columns([13,1,1])
    with col2:
        if not st.session_state.edit_mode:
            if st.button("Edit"):
                st.session_state.edit_mode = True
                st.rerun()
    with col3:
        if st.session_state.edit_mode:
            if st.button("Save"):
                st.session_state.profile_data.update({
                    "name": name, "email": email, "qualification": qualification,
                    "mobile": mobile, "dob": dob, "country": country,
                    "username": username, "gender": gender, "goal": goal,
                    "level": level, "interest": interest,
                })
                st.session_state.edit_mode = False
                st.success("Saved")
                st.rerun()
    
# SETTINGS
elif st.session_state.view == "Settings":
    st.title("Settings")
    tab1, tab2, tab3, tab4 = st.tabs(
        ["Appearance", "Notifications", "General", "Help"]
    )
    with tab1:
        st.subheader("Theme")
        st.radio("Select Theme", ["Light", "Dark", "System"])

        st.subheader("Font")
        st.selectbox("Font Family", ["Arial", "Roboto", "Poppins"])
        st.slider("Font Size", 10, 24, 14)
        
    with tab2:
        st.toggle("Email Notifications")
        st.toggle("Course Updates")
        st.toggle("AI Recommendations")
    with tab3:
        st.subheader("General")
        st.selectbox("Language", ["English", "Hindi"])
        st.selectbox("Timezone", ["IST", "UTC"])
    with tab4:

        # --- HELP VIEW ---
    # REMOVED the 'if st.session_state.view' check so it always shows when tab4 is active
        st.title("Support Center")
        st.write("Get help with your account or report technical issues.")
        st.divider()

    # --- FAQ SECTION ---
        st.subheader("Frequently Asked Questions")
        
        with st.expander("How do I export my data?"):
            st.markdown("<p style='color: #FFFFFF; font-size: 16px;'>Go to the <b>Privacy</b> tab and click <b>Download My Data</b>.</p>", unsafe_allow_html=True)

        with st.expander("How is my AI Readiness score calculated?"):
            st.markdown("<p style='color: #FFFFFF; font-size: 16px;'>It is based on your completed topics vs. industry-standard skill benchmarks.</p>", unsafe_allow_html=True)

        st.divider()

        # --- CONTACT FORM ---
        st.subheader("Report an Issue")
        
        # Using columns to keep the form neat
        contact_col, info_col = st.columns([2, 1])
        
        with contact_col:
            issue_type = st.selectbox("Issue Category", ["Bug Report", "Feature Request", "Account Access"], key="help_issue_type")
            message = st.text_area("Describe your issue", placeholder="Please provide details...", key="help_message")
            
            # Making the button professional and right-aligned
            btn_col1, btn_col2 = st.columns([2, 1])
            with btn_col2:
                if st.button("Submit Report", type="primary", use_container_width=True):
                    if message:
                        st.success("Report submitted to the engineering team.")
                        st.toast("Ticket #4920 created.")
                    else:
                        st.error("Please describe the issue first.")

        with info_col:
            st.info("**Technical Support**")
            st.caption("Average response time: < 24 hours")
            st.write("---")
            st.write("📍 **Location**")
            st.caption("Bhusawal / Pune, India")
    

# --- SECURITY VIEW ---
elif st.session_state.view == "Security":
    st.title("Security & Sessions")
    st.write("Manage your password, authentication methods, and active devices.")
    st.divider()

    # 1. INITIALIZE SESSION STATES
    if "edit_mode" not in st.session_state:
        st.session_state.edit_mode = False
    if "two_fa_enabled" not in st.session_state:
        st.session_state.two_fa_enabled = False
    if "test_code" not in st.session_state:
        st.session_state.test_code = None

    # --- SECTION 1: CHANGE PASSWORD ---
    st.subheader("Authentication")
    is_editing = st.session_state.edit_mode

    st.info("**Password Policy:** 8+ characters including uppercase, numbers, and symbols.")

    # Password Inputs
    r1_col1, r1_col2 = st.columns(2)
    with r1_col1:
        current_pw = st.text_input("Current Password", type="password", disabled=not is_editing)
    with r1_col2:
        new_pw = st.text_input("New Password", type="password", disabled=not is_editing)
    
    r2_col1, r2_col2 = st.columns(2)
    with r2_col1:
        confirm_pw = st.text_input("Confirm New Password", type="password", disabled=not is_editing)
    
    # Password Buttons
    btn_spacer, btn_col1, btn_col2 = st.columns([8, 1, 1])
    if not is_editing:
        with btn_col2:
            if st.button("Edit", key="edit_pw_btn", use_container_width=True):
                st.session_state.edit_mode = True
                st.rerun()
    else:
        with btn_col1:
            if st.button("Cancel", key="cancel_pw_btn", use_container_width=True):
                st.session_state.edit_mode = False
                st.rerun()
        with btn_col2:
            if st.button("Save", key="save_pw_btn", type="primary", use_container_width=True):
                # Replace with your actual get_password_status check
                if new_pw == confirm_pw and len(new_pw) >= 8:
                    st.session_state.edit_mode = False
                    st.success("Password Updated!")
                    st.rerun()
                else:
                    st.error("Check requirements or password mismatch.")

    st.divider()

    # --- SECTION 2: ACCOUNT PROTECTION (2FA) ---
    st.subheader("Account Protection")
    
    if not st.session_state.two_fa_enabled:
        if st.session_state.test_code is None:
            c1, c2 = st.columns([3, 1])
            with c1:
                st.markdown("**Two-Factor Authentication (2FA)**")
                st.caption("Secure your account with a secondary 6-digit verification code.")
            with c2:
                if st.button("Enable", key="en_2fa", type="primary", use_container_width=True):
                    # import random (Ensure this is at the top of your file)
                    st.session_state.test_code = str(random.randint(100000, 999999))
                    st.rerun()
        else:
            # 2FA Setup Mode
            st.info("📱 Scan this QR code with your Authenticator App.")
            qr_col, input_col = st.columns([1, 2])
            
            with qr_col:
                # import qrcode, io (Ensure these are at the top)
                qr = qrcode.make(st.session_state.test_code)
                buf = io.BytesIO()
                qr.save(buf, format="PNG")
                st.image(buf, width=150)
            
            with input_col:
                st.write("### Verify Code")
                u_code = st.text_input("Enter 6-digit code", placeholder="000000")
                v1, v2 = st.columns(2)
                with v1:
                    if st.button("Verify", key="v_2fa", type="primary", use_container_width=True):
                        if u_code == st.session_state.test_code:
                            st.session_state.two_fa_enabled = True
                            st.session_state.test_code = None
                            st.success("2FA Enabled!")
                            st.rerun()
                with v2:
                    if st.button("Back", key="back_2fa", use_container_width=True):
                        st.session_state.test_code = None
                        st.rerun()
    else:
        # 2FA Active State
        c1, c2 = st.columns([3, 1])
        with c1:
            st.success("✅ **Two-Factor Authentication is Active**")
            st.caption("Your account is protected by an additional security layer.")
        with c2:
            if st.button("Disable", key="dis_2fa", use_container_width=True):
                st.session_state.two_fa_enabled = False
                st.rerun()

    st.divider()

    # --- SECTION 3: ACTIVE SESSIONS ---
    st.subheader("Active Sessions")
    
    # Session 1: Current
    with st.container():
        sc1, sc2 = st.columns([3, 1])
        with sc1:
            st.markdown("**Windows PC — Bhusawal, India**")
            st.markdown("<p style='color: #4CAF50; font-size: 14px; margin-top: -10px;'>Active now • Chrome Browser</p>", unsafe_allow_html=True)
        with sc2:
            st.button("Current", disabled=True, use_container_width=True)

    # Session 2: Other
    with st.container():
        so1, so2 = st.columns([3, 1])
        with so1:
            st.markdown("**Samsung Galaxy — Pune, India**")
            st.markdown("<p style='color: #FFFFFF; font-size: 14px; opacity: 0.7; margin-top: -10px;'>Last active: 45m ago</p>", unsafe_allow_html=True)
        with so2:
            if st.button("Revoke", key="rev_mob", use_container_width=True):
                st.toast("Mobile session terminated.")

    st.divider()
    st.caption("🛡️ Security Tip: If you see a device you don't recognize, revoke it and change your password immediately.")

# CONNECTIONS
elif st.session_state.view == "Connections":
    st.title("Connected Accounts")
    st.write("Manage your linked social and professional accounts.")
    
    st.divider()

    # --- HELPER FUNCTION FOR CLEAN ROWS ---
    def account_row(name, email, is_connected, icon="🔗"):
        col1, col2, col3 = st.columns([0.5, 3, 1.5])
        
        with col1:
            st.markdown(f"### {icon}")
            
        with col2:
            st.markdown(f"**{name}**")
            if is_connected:
                st.caption(f"Linked as: {email}")
            else:
                st.caption("Not connected")
                
        with col3:
            if is_connected:
                # Use a unique key for every button
                if st.button("Disconnect", key=f"btn_dis_{name}", use_container_width=True):
                    # Add logic to disconnect here
                    pass
            else:
                if st.button("Connect", key=f"btn_con_{name}", type="primary", use_container_width=True):
                    # Add logic to connect here
                    pass
        st.divider()

    # --- RENDER THE ACCOUNTS ---
    # In a real app, these values would come from your FastAPI backend
    account_row("Google", "harshada.c@gmail.com", is_connected=True, icon="🌐")
    account_row("GitHub", "harshada-codes", is_connected=True, icon="💻")
    account_row("LinkedIn", None, is_connected=False, icon="👔")

# PRIVACY
# --- PRIVACY VIEW ---
elif st.session_state.view == "Privacy":
    st.title("Privacy & Data Control")
    st.write("Manage your personal information, visibility, and data portability.")
    st.divider()

    # --- SECTION 1: VISIBILITY ---
    st.subheader("Profile Visibility")
    with st.container():
        v_col1, v_col2 = st.columns([3, 1])
        with v_col1:
            st.markdown("**Public Profile**")
            st.caption("Allow others to see your projects, skills, and batches.")
        with v_col2:
            st.toggle("Public", value=True, key="visibility_toggle", label_visibility="collapsed")
    
    with st.container():
        s_col1, s_col2 = st.columns([3, 1])
        with s_col1:
            st.markdown("**Search Engine Indexing**")
            st.caption("Allow Google to link to your profile and projects.")
        with s_col2:
            st.toggle("SEO", value=False, key="seo_toggle", label_visibility="collapsed")

    st.divider()

    # --- SECTION 2: DATA & AI ---
    st.subheader("Data & Personalization")
    with st.container():
        a1, a2 = st.columns([3, 1])
        with a1:
            st.markdown("**AI Personalization**")
            st.caption("Use your project data to improve AI-driven teaching suggestions.")
        with a2:
            st.toggle("Enabled", value=True, key="ai_toggle", label_visibility="collapsed")

    st.divider()

    # --- SECTION 3: YOUR PERSONAL DATA (FIXED BUTTON WIDTH) ---
    st.subheader("Your Personal Data")
    with st.container():
        d_col1, d_col2 = st.columns([3, 1]) # Same 3:1 ratio as toggles
        with d_col1:
            st.markdown("**Export Account Data**")
            st.caption("Download a JSON archive of your profile, security settings, and projects.")
        
        with d_col2:
            try:
                export_payload = {
                    "user_info": {
                        "name": "Harshada Chaudhari",
                        "degree": "B.Tech in Artificial Intelligence and Data Science",
                        "batch": "2026",
                        "college": "SSGBCOET, Bhusawal"
                    },
                    "security_settings": {
                        "two_factor_enabled": st.session_state.get("two_fa_enabled", False),
                        "profile_visibility": "Public" if st.session_state.get("visibility_toggle") else "Private"
                    },
                    "projects": ["ChatStream AI", "Movie Rec System", "Google Play EDA"]
                }
                json_data = json.dumps(export_payload, indent=4)

                # Button now stays inside the small column
                st.download_button(
                    label="📥 Download",
                    data=json_data,
                    file_name="harshada_data_export.json",
                    mime="application/json",
                    use_container_width=True
                )
            except Exception as e:
                st.error("Export Error")

    st.divider()

    # --- SECTION 4: DANGER ZONE (FIXED BUTTON WIDTH) ---
    st.subheader("Danger Zone")
    with st.container():
        del_col1, del_col2 = st.columns([3, 1])
        with del_col1:
            st.markdown("**Delete Account**")
            st.caption("Permanently remove your account and all associated data. This cannot be undone.")
        with del_col2:
            # Button stays small on the right
            if st.button("Delete", type="primary", use_container_width=True):
                st.session_state.show_delete_warning = True

    # Confirmation Logic (Only shows if button is clicked)
    if st.session_state.get("show_delete_warning"):
        st.warning("⚠️ Are you sure? This will erase your B.Tech project data.")
        # Sub-columns to keep confirmation buttons small too
        c_col1, c_col2, c_spacer = st.columns([1, 1, 2])
        with c_col1:
            if st.button("Confirm", type="primary", key="final_del", use_container_width=True):
                st.success("Account deleted.")
                st.rerun()
        with c_col2:
            if st.button("Cancel", key="cancel_del", use_container_width=True):
                st.session_state.show_delete_warning = False
                st.rerun()

# PROFILE INSIGHTS
# --- PROFILE INSIGHTS VIEW ---
elif st.session_state.view == "Insights":
    st.title("Profile Insights")
    st.write("AI-driven analysis of your learning progress and career readiness.")
    st.divider()

    # BACKEND PREP: This dictionary will eventually be replaced by your FastAPI response
    # insights_data = requests.get(f"{BACKEND_URL}/user/insights").json()
    insights_data = {
        "metrics": {
            "completed": "12",
            "in_progress": "5",
            "readiness": "85%"
        },
        "suggestions": [
            {"title": "Primary Focus", "text": "Apply your current theoretical knowledge to a new end-to-end technical project.", "type": "info"},
            {"title": "Learning Strength", "text": "Your recent activity shows high consistency. This pace is optimal for skill retention.", "type": "success"},
            {"title": "Next Milestone", "text": "Review your 'In Progress' list and aim to complete at least 2 topics by the weekend.", "type": "warning"},
            {"title": "Career Growth", "text": "Align your learning path with the specific requirements of your target internship roles.", "type": "info"}
        ]
    }

    # --- SECTION 1: KEY PERFORMANCE METRICS ---
    m1, m2, m3 = st.columns(3)
    with m1:
        st.metric(label="Topics Completed", value=insights_data["metrics"]["completed"], delta="↑ 2")
    with m2:
        st.metric(label="In Progress", value=insights_data["metrics"]["in_progress"], delta="-1", delta_color="inverse")
    with m3:
        st.metric(label="Skill Readiness", value=insights_data["metrics"]["readiness"], delta="5%")

    st.divider()

    # --- SECTION 2: LEARNING PROGRESS ---
    st.subheader("Overall Learning Progress")
    completed = int(insights_data["metrics"]["completed"])
    total = completed + int(insights_data["metrics"]["in_progress"])
    progress_val = int((completed / total) * 100)
    
    col_p1, col_p2 = st.columns([4, 1])
    with col_p1:
        st.progress(progress_val / 100)
    with col_p2:
        st.write(f"**{progress_val}%**")

    st.divider()

    # --- SECTION 3: AI-DRIVEN SUGGESTIONS (High Visibility) ---
    st.subheader("🎯 Personalized Recommendations")
    
    # Helper for high-visibility text
    def insight_card(title, text, type="info"):
        if type == "info": st.info(f"**{title}**")
        elif type == "success": st.success(f"**{title}**")
        elif type == "warning": st.warning(f"**{title}**")
        
        # High visibility CSS: White color, 16px font
        st.markdown(f"""
            <p style='color: #FFFFFF; font-size: 16px; font-weight: 400; margin-top: -10px; margin-bottom: 20px;'>
                {text}
            </p>
        """, unsafe_allow_html=True)

    # Displaying cards in a 2x2 grid
    row1_col1, row1_col2 = st.columns(2)
    with row1_col1:
        insight_card(insights_data["suggestions"][0]["title"], insights_data["suggestions"][0]["text"], "info")
    with row1_col2:
        insight_card(insights_data["suggestions"][1]["title"], insights_data["suggestions"][1]["text"], "success")

    row2_col1, row2_col2 = st.columns(2)
    with row2_col1:
        insight_card(insights_data["suggestions"][2]["title"], insights_data["suggestions"][2]["text"], "warning")
    with row2_col2:
        # Fixed 'Career Growth' card - no more Python help box!
        insight_card(insights_data["suggestions"][3]["title"], insights_data["suggestions"][3]["text"], "info")

    # --- SECTION 4: ACTIONS ---
    st.divider()
    _, q_col = st.columns([3, 1])
    with q_col:
        if st.button("Refresh Analysis", use_container_width=True):
            st.toast("Fetching latest backend insights...")
            st.rerun()

# --- AI INSIGHTS VIEW ---
elif st.session_state.view == "AI":
    st.title("AI Insights & Recommendations")
    st.write("Machine Learning-driven roadmap based on your current skill level.")
    st.divider()

    # DATA PREP: This dictionary will be your FastAPI JSON response later
    ai_data = {
        "goal": st.session_state.profile_data.get('goal', 'Technical Role'),
        "level": st.session_state.profile_data.get('level', 'Intermediate'),
        "suggestions": [
            {"title": "Focus: Portfolio Projects", "text": "Move beyond basic scripts. Build end-to-end applications that solve specific industry problems.", "type": "info"},
            {"title": "Focus: UX Case Studies", "text": "Document the 'Why' behind your technical decisions. Explain your architecture to non-technical stakeholders.", "type": "success"},
            {"title": "Action: Practical Tasks", "text": "Practice real-world system debugging and data cleaning tasks instead of just following tutorials.", "type": "warning"},
            {"title": "Core Strategy", "text": "Shift from theory to practical execution. Build a CI/CD pipeline for your existing Streamlit apps.", "type": "info"}
        ]
    }

    # --- SECTION 1: STATUS SUMMARY ---
    c1, c2 = st.columns(2)
    with c1:
        st.info(f"**Current Goal:** {ai_data['goal']}")
    with c2:
        st.success(f"**Skill Level:** {ai_data['level']}")

    st.divider()

    # --- SECTION 2: SMART RECOMMENDATIONS (High Visibility) ---
    st.subheader("🚀 Smart Recommendations")

    # Reuse the same high-visibility helper logic for consistency
    def ai_insight_card(title, text, type="info"):
        if type == "info": st.info(f"**{title}**")
        elif type == "success": st.success(f"**{title}**")
        elif type == "warning": st.warning(f"**{title}**")
        
        # High visibility CSS: White color, 16px font
        st.markdown(f"""
            <p style='color: #FFFFFF; font-size: 16px; font-weight: 400; margin-top: -10px; margin-bottom: 20px;'>
                {text}
            </p>
        """, unsafe_allow_html=True)

    # Grid Display
    row1_c1, row1_c2 = st.columns(2)
    with row1_c1:
        ai_insight_card(ai_data["suggestions"][0]["title"], ai_data["suggestions"][0]["text"], "info")
    with row1_c2:
        ai_insight_card(ai_data["suggestions"][1]["title"], ai_data["suggestions"][1]["text"], "success")

    row2_c1, row2_c2 = st.columns(2)
    with row2_c1:
        ai_insight_card(ai_data["suggestions"][2]["title"], ai_data["suggestions"][2]["text"], "warning")
    with row2_c2:
        ai_insight_card(ai_data["suggestions"][3]["title"], ai_data["suggestions"][3]["text"], "info")
        
    # --- SECTION 3: ACTIONS ---
    st.divider()
    _, ai_btn_col = st.columns([3, 1])
    with ai_btn_col:
        if st.button("Generate New Insights", use_container_width=True):
            st.toast("AI is analyzing your profile...")
            st.rerun()

# active log
# --- ACTIVITY LOG VIEW ---
elif st.session_state.view == "Activity":
    st.title("Activity Log")
    st.write("A secure history of your account actions and security events.")
    st.divider()

    # MOCK DATA: This list will eventually come from your FastAPI 'GET /user/activity'
    activity_data = [
        {"icon": "🔐", "event": "Logged In", "detail": "Session started from Chrome (Windows)", "time": "Today, 10:30 AM"},
        {"icon": "🔑", "event": "Password Changed", "detail": "Account security credentials updated", "time": "Yesterday, 04:15 PM"},
        {"icon": "📲", "event": "2FA Enabled", "detail": "Two-Factor Authentication activated", "time": "2 days ago, 09:00 AM"},
        {"icon": "👤", "event": "Profile Updated", "detail": "Changed B.Tech Batch to 2026", "time": "5 days ago, 11:20 AM"},
        {"icon": "🛡️", "event": "Session Revoked", "detail": "Mobile device (Samsung Galaxy) disconnected", "time": "1 week ago, 02:45 PM"}
    ]

    # --- TIMELINE RENDERER ---
    for i, log in enumerate(activity_data):
        with st.container():
            # [Icon, Event Details, Timestamp]
            col_icon, col_info, col_time = st.columns([0.5, 3, 1.5])
            
            with col_icon:
                st.markdown(f"### {log['icon']}")
            
            with col_info:
                st.markdown(f"**{log['event']}**")
                # Using your high-visibility 16px white text
                st.markdown(f"<p style='color: #FFFFFF; font-size: 15px; opacity: 0.9; margin-top: -10px;'>{log['detail']}</p>", unsafe_allow_html=True)
            
            with col_time:
                # Right-aligned timestamp in italics
                st.markdown(f"<p style='text-align: right; color: #AAAAAA; font-style: italic; font-size: 13px;'>{log['time']}</p>", unsafe_allow_html=True)

        # Add a divider between entries, but skip the last one for a cleaner look
        if i < len(activity_data) - 1:
            st.divider()

    # --- FOOTER ACTIONS ---
    st.divider()
    _, btn_col = st.columns([3, 1])
    with btn_col:
        # Standard SRE feature to clear the view (for frontend testing)
        if st.button("Refresh Logs", use_container_width=True):
            st.toast("Fetching latest audit logs...")
            st.rerun()

# --- BILLING / EXPLORE PLANS VIEW ---
elif st.session_state.view == "Billing":
    # 1. Inject Custom CSS for the 'Card' Look
    st.markdown("""
        <style>
        .plan-card {
            background-color: #0E1117;
            border: 1px solid #30363D;
            border-radius: 15px;
            padding: 30px;
            height: 550px;
            transition: transform 0.3s;
        }
        .plan-card:hover {
            border-color: #58A6FF;
            transform: translateY(-5px);
        }
        .price-text {
            font-size: 36px;
            font-weight: bold;
            margin-bottom: 0px;
        }
        .feature-list {
            font-size: 14px;
            color: #8B949E;
            margin-top: 20px;
            line-height: 1.8;
        }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("<h1 style='text-align: center; font-size: 50px;'>Explore plans</h1>", unsafe_allow_html=True)
    
    # Plan toggle (Visual only)
    st.markdown("<p style='text-align: center; color: #8B949E;'>Individual &nbsp;&nbsp; | &nbsp;&nbsp; Team</p>", unsafe_allow_html=True)
    st.write("##")

    # 2. Creating the 3-Column Grid
    col1, col2, col3 = st.columns(3)

    # --- FREE PLAN ---
    with col1:
        st.markdown(f"""
            <div class="plan-card">
                <h3>🌱</h3>
                <h2>Free</h2>
                <p style="color: #8B949E;">Basic access for students</p>
                <p class="price-text">₹0</p>
                <p style="color: #8B949E; font-size: 12px;">Free for everyone</p>
                <br>
                <div class="feature-list">
                    ✓ 5 Active Projects<br>
                    ✓ Basic AI Insights<br>
                    ✓ Community Support<br>
                    ✓ Public Profile
                </div>
            </div>
        """, unsafe_allow_html=True)
        if st.button("Current Plan", key="free_btn", use_container_width=True, disabled=True):
            pass

    # --- PRO PLAN ---
    with col2:
        st.markdown(f"""
            <div class="plan-card">
                <h3>🌿</h3>
                <h2>Pro</h2>
                <p style="color: #8B949E;">For career growth</p>
                <p class="price-text">₹499</p>
                <p style="color: #8B949E; font-size: 12px;">Per month billed annually</p>
                <br>
                <div class="feature-list">
                    ✓ Everything in Free, plus:<br>
                    ✓ Unlimited Projects<br>
                    ✓ Advanced SRE Metrics<br>
                    ✓ Priority AI Support<br>
                    ✓ Private Profile
                </div>
            </div>
        """, unsafe_allow_html=True)
        if st.button("Upgrade to Pro", key="pro_btn", type="primary", use_container_width=True):
            st.toast("Connecting to Secure Payment...")

    # --- MAX PLAN ---
    with col3:
        st.markdown(f"""
            <div class="plan-card">
                <h3>🌳</h3>
                <h2>Max</h2>
                <p style="color: #8B949E;">For power users</p>
                <p class="price-text">₹999</p>
                <p style="color: #8B949E; font-size: 12px;">Per month billed monthly</p>
                <br>
                <div class="feature-list">
                    ✓ Everything in Pro, plus:<br>
                    ✓ API Access<br>
                    ✓ Early Access Features<br>
                    ✓ Resume Review AI<br>
                    ✓ Custom Themes
                </div>
            </div>
        """, unsafe_allow_html=True)
        if st.button("Try Max", key="max_btn", use_container_width=True):
            st.toast("Checking Max availability...")

    st.write("##")
    st.divider()
    st.caption("Looking for enterprise solutions? Contact support.")

# --- ABOUT VIEW ---
elif st.session_state.view == "About":
    # 1. Custom CSS for a centered 'Hero' look
    st.markdown("""
        <style>
        .about-container {
            text-align: center;
            padding: 40px;
            background-color: #0E1117;
            border: 1px solid #30363D;
            border-radius: 20px;
            margin-bottom: 25px;
        }
        .tech-badge {
            display: inline-block;
            padding: 5px 12px;
            margin: 5px;
            background-color: #161B22;
            border: 1px solid #58A6FF;
            border-radius: 10px;
            color: #58A6FF;
            font-size: 13px;
            font-weight: 500;
        }
        </style>
    """, unsafe_allow_html=True)

    # 2. Hero Section
    with st.container():
        st.markdown("""
            <div class="about-container">
                <h1 style='font-size: 45px; margin-bottom: 0px;'>AI Learning Assistant</h1>
                <p style='color: #8B949E; font-size: 18px;'>Empowering 2026 Batch Students with Data-Driven Insights</p>
                <br>
                <div style='display: flex; justify-content: center; flex-wrap: wrap;'>
                    <span class="tech-badge">Python 3.10</span>
                    <span class="tech-badge">Streamlit</span>
                    <span class="tech-badge">FastAPI</span>
                    <span class="tech-badge">SRE Ready</span>
                    <span class="tech-badge">v1.0.2-stable</span>
                </div>
            </div>
        """, unsafe_allow_html=True)

    # 3. Content Columns
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("🎯 Project Mission")
        st.markdown(f"""
            <p style='color: #FFFFFF; font-size: 16px; opacity: 0.9;'>
                To bridge the gap between academic theory and industry readiness. 
                This assistant analyzes learning patterns to suggest real-world 
                SRE and AI workflows.
            </p>
        """, unsafe_allow_html=True)

    with col2:
        st.subheader("🛡️ Security & Privacy")
        st.markdown(f"""
            <p style='color: #FFFFFF; font-size: 16px; opacity: 0.9;'>
                Built with industry-standard security protocols, featuring 2FA, 
                Audit Logging, and transparent data management.
            </p>
        """, unsafe_allow_html=True)

    st.divider()

    # 4. Footer Branding
    f_col1, f_col2, f_col3 = st.columns([1, 2, 1])
    with f_col2:
        st.markdown("<p style='text-align: center; color: #8B949E;'>Developed by Harshada Chaudhari<br>© 2026 AI Learning Hub</p>", unsafe_allow_html=True)
        
        # Social/Github Link (Optional)
        st.button("View Source on GitHub", use_container_width=True)

    # --- QUICK ACTION ---
    if st.button("Check for Updates", use_container_width=True):
        st.toast("You are using the latest version!")