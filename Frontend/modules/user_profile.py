import streamlit as st
from datetime import datetime, date
import re
import qrcode
import io
import random
import json
import requests
from datetime import datetime, date
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
import os
from PIL import Image
# =========================
# PROFESSIONAL CSS (Updated)
# =========================
def inject_profile_styles():
    st.markdown("""
    <style>
    #MainMenu, footer {visibility: hidden;}

    html, body {
        background-color: #0a0a0a !important;
        overflow-x: hidden !important;
    }
    .stApp {
    overflow-x: hidden !important;
}
    .block-container {
    max-width: 100vw;
    overflow-x: hidden !important;
}
    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: #0e0e0e !important;
        border-right: 1px solid #1e293b;
        display: flex !important; /* Force sidebar to show when in profile */
    }

    /* UNIVERSAL BUTTON THEME: Transparent, Blue Hover */
div.stButton > button {
    width: fit-content; /* Changed from 100% to fit-content */
    text-align: left;
    background-color: transparent !important;
    color: #ded1d1 !important;
    border: 1px solid transparent !important; 
    box-shadow: none !important;
    border-radius: 8px;
    font-size: 14px;
    transition: all 0.3s ease;
    padding: 8px 12px; /* Added more horizontal padding for better look */
    margin-top: 1px;
    margin-left: 1px; /* Aligns it with the sidebar text/icons */
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


def generate_pdf(data):
    import io
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
    from reportlab.lib.styles import getSampleStyleSheet

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer)
    styles = getSampleStyleSheet()

    content = []

    # -------- SAFE EXTRACTION --------
    user_info = data.get("user_info", {})
    security = data.get("security_settings", {})
    projects = data.get("projects", [])

    # -------- TITLE --------
    content.append(Paragraph("User Data Export", styles["Title"]))
    content.append(Spacer(1, 10))

    # -------- USER INFO --------
    content.append(Paragraph(f"Name: {user_info.get('name', 'N/A')}", styles["Normal"]))

    # 🔴 FIX: degree → qualification
    content.append(Paragraph(f"Qualification: {user_info.get('qualification', 'N/A')}", styles["Normal"]))

    content.append(Paragraph(f"Batch: {user_info.get('batch', 'N/A')}", styles["Normal"]))
    content.append(Spacer(1, 10))

    # -------- SECURITY --------
    content.append(Paragraph("Security Settings", styles["Heading2"]))
    content.append(Paragraph(
        f"2FA Enabled: {security.get('two_factor_enabled', 'N/A')}",
        styles["Normal"]
    ))
    content.append(Paragraph(
        f"Visibility: {security.get('profile_visibility', 'N/A')}",
        styles["Normal"]
    ))
    content.append(Spacer(1, 10))

    # -------- PROJECTS --------
    content.append(Paragraph("Projects", styles["Heading2"]))

    if projects:
        for proj in projects:
            content.append(Paragraph(f"- {proj}", styles["Normal"]))
    else:
        content.append(Paragraph("No projects available", styles["Normal"]))

    # -------- BUILD --------
    doc.build(content)
    buffer.seek(0)

    return buffer
def apply_theme():
    theme = st.session_state.get("app_theme", "Dark")

    theme_styles = {
        "Dark": """
            .stApp { background-color: #0a0a0a !important; color: #f3f4f6 !important; }
            [data-testid="stSidebar"] { background-color: #0e0e0e !important; }
            .block-container { background-color: #0a0a0a !important; }
        """,

        "Light": """
            .stApp { background-color: #f5f5f0 !important; color: #1a1a1a !important; }
            [data-testid="stSidebar"] { background-color: #ebebeb !important; }
            .block-container { background-color: #f5f5f0 !important; }

            p, h1, h2, h3, h4, label, span {
                color: #1a1a1a !important;
            }
        """,

        "Midnight Blue": """
            .stApp { background-color: #0d1117 !important; color: #c9d1d9 !important; }
            [data-testid="stSidebar"] { background-color: #161b22 !important; }
            .block-container { background-color: #0d1117 !important; }
        """
    }

    st.markdown(
        f"<style>{theme_styles[theme]}</style>",
        unsafe_allow_html=True
    )
def apply_font():
    font = st.session_state.get("app_font", "Inter")
    size = st.session_state.get("app_font_size", 15)

    google_fonts = ["Inter", "Roboto", "Poppins"]

    font_import = ""
    if font in google_fonts:
        font_import = f"""
        @import url('https://fonts.googleapis.com/css2?family={font.replace(" ", "+")}:wght@300;400;500;600&display=swap');
        """

    st.markdown(f"""
        <style>
        {font_import}

        .stApp, .stApp p, .stApp div, .stApp span, .stApp label {{
            font-family: '{font}', sans-serif !important;
            font-size: {size}px !important;
        }}
        </style>
    """, unsafe_allow_html=True)
# =========================
# SESSION STATE (Dynamic Ready)
# =========================

def load_default_profile():
    """Fallback profile (used only if no real data is loaded)"""
    return {
        "name": "User",
        "email": "",
        "qualification": "",
        "mobile": "",
        "dob": date(2000, 1, 1),
        "country": "India",
        "username": "",
        "gender": "Other",
        "github_url": "",
        "linkedin_url": "",
        "goal": "",
        "level": "Beginner",
        "interest": [],
    }


# Initialize profile data safely
if "profile_data" not in st.session_state:
    st.session_state.profile_data = load_default_profile()

# =========================
# FUNCTIONS (Your Logic)
# =========================
def logout():
    # ✅ Fix — redirect to login after logout
    st.session_state.clear()
    st.session_state.page = "login"
    st.rerun()
    
def get_password_status(password):
    return {
        "8+ characters": len(password) >= 8,
        "A number": bool(re.search(r"\d", password)),
        "A special character": bool(re.search(r"[@$!%*?&]", password)),
        "Uppercase letter": bool(re.search(r"[A-Z]", password)),
    }



# =========================
# SIDEBAR (Your Logic)
# =========================
def render_sidebar():
    with st.sidebar:
        data = st.session_state.profile_data
        # Locate line 1453 in your sidebar code
        name = data.get("name", "")

        # Use the first letter if name exists, otherwise use a default like "U"
        if name and len(name) > 0:
            initial = name[0].upper()
        else:
            initial = "U"

        st.markdown(f"""
        <div style="display:flex; align-items:center; gap:10px; padding-left:10px;">
            <div style="width:40px;height:40px;border-radius:50%;background:#2563eb;color:white;display:flex;align-items:center;justify-content:center;font-weight:bold;">{initial}</div>
            <div>
                <b style="color:white;">{data['name']}</b><br>
                <span style='font-size:12px;color:gray;'>{data.get('goal','User')}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<div class="separator"></div>', unsafe_allow_html=True)
        if st.button("Back to Chat", use_container_width=False):
            st.session_state.page = "llm_ui" # Change state back to chat
            st.rerun()
        st.markdown('<div class="sidebar-title">ACCOUNT</div>', unsafe_allow_html=True)

        if st.button("Profile"): st.session_state.view = "Profile"
        if st.button("Settings"): st.session_state.view = "Settings"
        if st.button("Security"): st.session_state.view = "Security"
        if st.button("Connected Accounts"): st.session_state.view = "Connections"
        if st.button("Privacy"): st.session_state.view = "Privacy"

        st.markdown('<div class="sidebar-title">INSIGHTS</div>', unsafe_allow_html=True)
        if st.button("Profile Insights"): st.session_state.view = "Insights"
        if st.button("AI Insights"): st.session_state.view = "AI"
        if st.button("Activity Log"): st.session_state.view = "Activity"

        st.markdown('<div class="sidebar-title">OTHER</div>', unsafe_allow_html=True)
        if st.button("Billing"): st.session_state.view = "Billing"
        if st.button("About"): st.session_state.view = "About"

        st.markdown('<div class="logout-container">', unsafe_allow_html=True)
        if st.button("Logout"): logout()
        st.markdown('</div>', unsafe_allow_html=True)

# =========================
# PAGES (Your Logic)
# =========================
def render_profile():
    st.title("User Profile")
    st.caption("Manage your personal information and learning preferences to get better AI recommendations.")

    data     = st.session_state.profile_data
    disabled = not st.session_state.edit_mode

    # ✅ Initialize temp edit state ONCE when Edit is clicked
    if st.session_state.edit_mode and "edit_temp" not in st.session_state:
        st.session_state.edit_temp = data.copy()

    # ✅ Use temp state while editing, real data when viewing
    d = st.session_state.edit_temp if st.session_state.edit_mode else data

    c1, c2 = st.columns(2)
    with c1:
        name          = st.text_input("Name",          d["name"],                      disabled=disabled)
        username      = st.text_input("Username",       d["username"],                  disabled=disabled)
        qualification = st.text_input("Qualification",  d.get("qualification", ""),     disabled=disabled)
        dob           = st.date_input("Date of Birth",  value=d["dob"],                 disabled=disabled)
        gender        = st.radio("Gender", ["Male", "Female", "Other"],
                                 index=["Male","Female","Other"].index(d.get("gender","Other")),
                                 disabled=disabled)

    with c2:
        email        = st.text_input("Email ID",    d["email"],    placeholder="your@gmail.com", disabled=disabled)
        mobile       = st.text_input("Mobile",      d["mobile"],                                  disabled=disabled)
        github_url   = st.text_input("GitHub URL",  d.get("github_url",""),   placeholder="https://github.com/your-profile",   disabled=disabled)
        linkedin_url = st.text_input("LinkedIn URL",d.get("linkedin_url",""),placeholder="https://linkedin.com/in/your-profile",disabled=disabled)

        country_options = ["Select Country", "USA", "India", "UK"]
        try:
            c_idx = country_options.index(d.get("country", "Select Country"))
        except ValueError:
            c_idx = 0
        country = st.selectbox("Country", country_options, index=c_idx, disabled=disabled)

    st.markdown("### Learning Profile")
    st.caption("Customize your learning goals and interests to receive personalized guidance.")
    col3, col4 = st.columns(2)
    with col3:
        goal = st.text_input("Learning Goal", d["goal"], disabled=disabled)
        level_options = ["Select your skill level", "Beginner", "Intermediate", "Advanced"]
        try:
            l_idx = level_options.index(d.get("level", "Select your skill level"))
        except ValueError:
            l_idx = 0
        level = st.selectbox("Skill Level", options=level_options, index=l_idx, disabled=disabled)

    with col4:
        interest = st.multiselect(
            "Interested Domains",
            ["UI/UX Design","Artificial Intelligence (AI)","Web Development","Data Science",
             "Cybersecurity","Cloud Computing","Mobile App Development","Machine Learning (ML)",
             "DevOps","Game Development","Blockchain","Internet of Things (IoT)",
             "Digital Marketing","Product Management","Data Analytics","Other"],
            default=d["interest"],
            disabled=disabled
        )

    st.markdown('<div class="separator"></div>', unsafe_allow_html=True)
    col_space, col_reset, col_cancel, col_save = st.columns([12, 1.3, 1.3, 1.3])

    if not st.session_state.edit_mode:
        with col_save:
            if st.button("Edit", use_container_width=True):
                st.session_state.edit_mode = True
                # ✅ Save original data for reset
                st.session_state.default_profile_data = data.copy()
                st.session_state.edit_temp = data.copy()
                st.rerun()
    else:
        with col_reset:
            if st.button("Reset", use_container_width=True):
                # ✅ Restore original data — true reset
                st.session_state.edit_temp = st.session_state.default_profile_data.copy()
                st.rerun()

        with col_cancel:
            if st.button("Cancel", use_container_width=True):
                # ✅ Discard all changes — nothing saved
                del st.session_state.edit_temp
                st.session_state.edit_mode = False
                st.rerun()

        with col_save:
            if st.button("Save", type="primary", use_container_width=True):
                # ✅ Save temp → real profile_data
                updated = {
                    "name": name, "email": email, "qualification": qualification,
                    "mobile": mobile, "dob": dob, "country": country,
                    "username": username, "gender": gender, "goal": goal,
                    "level": level, "interest": interest,
                    "github_url": github_url, "linkedin_url": linkedin_url,
                }
                st.session_state.profile_data.update(updated)
                del st.session_state.edit_temp
                st.session_state.edit_mode = False
                add_activity("👤", "Profile Updated", "User updated profile details")
                st.success("Profile saved!")
                st.rerun()
    
# SETTINGS
def render_settings():
    st.title("Settings")
    st.caption("Control your application preferences, notifications, and experience.")
    tab1, tab2, tab3, tab4 = st.tabs(
        ["Appearance", "Notifications", "General", "Help"]
    )
    with tab1:
        st.caption("Adjust how the platform looks and feels for your comfort.")

        # -------- THEME --------
        st.subheader("Theme")

        themes = ["Dark", "Light", "Midnight Blue"]

        if "app_theme" not in st.session_state:
            st.session_state.app_theme = "Dark"

        current_theme = (
            st.session_state.app_theme
            if st.session_state.app_theme in themes else "Dark"
        )

        theme = st.radio(
            "Select Theme",
            themes,
            index=themes.index(current_theme),
            horizontal=True
        )

        if theme != st.session_state.app_theme:
            st.session_state.app_theme = theme
            st.rerun()

        st.divider()

        # -------- FONT --------
        st.subheader("Font")

        fonts = ["Inter", "Roboto", "Poppins", "Arial", "Georgia"]

        if "app_font" not in st.session_state:
            st.session_state.app_font = "Inter"

        if "app_font_size" not in st.session_state:
            st.session_state.app_font_size = 15

        current_font = (
            st.session_state.app_font
            if st.session_state.app_font in fonts else "Inter"
        )

        font = st.selectbox(
            "Font Family",
            fonts,
            index=fonts.index(current_font)
        )

        font_size = st.slider(
            "Font Size",
            12, 22,
            st.session_state.app_font_size
        )

        # Apply instantly (no button needed)
        st.session_state.app_font = font
        st.session_state.app_font_size = font_size

        st.divider()

        # -------- CHAT DISPLAY --------
        st.subheader("Chat Display")

        if "show_timestamps" not in st.session_state:
            st.session_state.show_timestamps = True

        if "compact_mode" not in st.session_state:
            st.session_state.compact_mode = False

        st.toggle("Show message timestamps", key="show_timestamps")
        st.toggle("Compact chat mode", key="compact_mode")
            
        with tab2:
            st.caption("Choose what updates and alerts you want to receive via email.")

            # -------- SAFE SESSION INITIALIZATION --------
            if "profile_data" not in st.session_state:
                st.session_state.profile_data = {"email": "", "name": "User"}

            defaults = {
                "notif_email": True,
                "notif_course": True,
                "notif_ai": False,
                "notif_security": True,
                "notif_weekly": False,
            }

            for key, val in defaults.items():
                if key not in st.session_state:
                    st.session_state[key] = val

            # -------- EMAIL INFO --------
            st.subheader("Email Notifications")

            user_email = st.session_state.profile_data.get("email", "")
            disabled = not bool(user_email)

            if user_email:
                st.info(f"Notifications will be sent to: **{user_email}**")
            else:
                st.warning("No email found. Update your profile first.")

            # -------- TOGGLES --------
            col1, col2 = st.columns(2)

            with col1:
                st.toggle("General Email Notifications", key="notif_email", disabled=disabled)
                st.toggle("Course Updates", key="notif_course", disabled=disabled)
                st.toggle("Security Alerts", key="notif_security", disabled=disabled)

            with col2:
                st.toggle("AI Recommendations", key="notif_ai", disabled=disabled)
                st.toggle("Weekly Progress Summary", key="notif_weekly", disabled=disabled)

            st.divider()

            # -------- TEST EMAIL --------
            st.subheader("Test Notification")

            if st.button("Send Test Email", type="primary"):
                if not user_email:
                    st.error("Please add your email in Profile first.")
                elif not st.session_state.notif_email:
                    st.warning("Enable Email Notifications first.")
                else:
                    try:
                        import smtplib
                        from email.mime.text import MIMEText
                        from email.mime.multipart import MIMEMultipart

                        # ⚠️ Replace these with your real credentials
                        EMAIL_HOST = "smtp.gmail.com"
                        EMAIL_PORT = 587
                        EMAIL_USERNAME = "your_email@gmail.com"
                        EMAIL_PASSWORD = "your_app_password"
                        EMAIL_FROM = EMAIL_USERNAME

                        msg = MIMEMultipart("alternative")
                        msg["Subject"] = "NexaAI — Test Notification"
                        msg["From"] = EMAIL_FROM
                        msg["To"] = user_email

                        html = f"""
                        <html>
                        <body style="font-family:Arial;background:#0a0a0a;color:#f3f4f6;padding:30px;">
                            <div style="max-width:480px;margin:auto;background:#111;border:1px solid #222;border-radius:16px;padding:30px;">
                                <h2 style="color:#3b82f6;">NexaAI</h2>
                                <p>Hi <b>{st.session_state.profile_data.get("name","User")}</b>, your notifications are working!</p>
                                <p style="color:#666;font-size:12px;">© 2026 NexaAI Team</p>
                            </div>
                        </body>
                        </html>
                        """

                        msg.attach(MIMEText(html, "html"))

                        with smtplib.SMTP(EMAIL_HOST, EMAIL_PORT) as server:
                            server.ehlo()
                            server.starttls()
                            server.login(EMAIL_USERNAME, EMAIL_PASSWORD)
                            server.sendmail(EMAIL_FROM, user_email, msg.as_string())

                        st.success(f"Test email sent to **{user_email}**")

                        # -------- ACTIVITY LOG --------
                        if "activity_logs" in st.session_state:
                            add_activity("📧", "Test Email Sent", f"Sent to {user_email}")

                    except Exception as e:
                        st.error(f"Email failed: {str(e)}")
    with tab3:
        
        st.caption("Configure your general app preferences.")
 
        # ---- TIMEZONE — dynamic from profile ----
        st.subheader("Timezone")
        country = st.session_state.profile_data.get("country", "India")
        country_tz = {"India": "IST (UTC+5:30)", "USA": "EST (UTC-5)", "UK": "GMT (UTC+0)"}
        detected_tz = country_tz.get(country, "IST (UTC+5:30)")
        st.info(f"Detected from profile country **{country}**: **{detected_tz}**")
 
        if "app_timezone" not in st.session_state:
            st.session_state.app_timezone = detected_tz
        tz = st.selectbox("Select Timezone", ["IST (UTC+5:30)", "EST (UTC-5)", "PST (UTC-8)", "GMT (UTC+0)", "UTC"])
        st.session_state.app_timezone = tz
 
        st.divider()
 
        # ---- AI BEHAVIOUR ----
        st.subheader("AI Behaviour")
        if "auto_title" not in st.session_state:
            st.session_state.auto_title = True
        if "save_history" not in st.session_state:
            st.session_state.save_history = True
        st.session_state.auto_title   = st.toggle("Auto-generate chat titles using AI", value=st.session_state.auto_title)
        st.session_state.save_history = st.toggle("Save chat history across sessions",  value=st.session_state.save_history)
    with tab4:
        st.caption("Need assistance? Find answers or contact support.")
        # --- HELP VIEW ---
    # REMOVED the 'if st.session_state.view' check so it always shows when tab4 is active
        st.title("Support Center")
        st.write("Get help with your account or report technical issues.")
        st.divider()

    # --- FAQ SECTION ---
        st.subheader("Frequently Asked Questions")
        
        with st.expander("How do I export my data?"):
            st.markdown("<p style='color: #FFFFFF; font-size: 16px;'>Go to the <b>Privacy</b> tab and click <b>Download My Data</b>. Your profile and security data will be exported.</p>", unsafe_allow_html=True)

        with st.expander("How is my AI Readiness score calculated?"):
            st.markdown("<p style='color: #FFFFFF; font-size: 16px;'>It is based on your completed topics vs industry-standard skill benchmarks for your selected skill level.</p>", unsafe_allow_html=True)

        with st.expander("What is EchoAI?"):
            st.markdown("<p style='color: #FFFFFF; font-size: 16px;'>EchoAI is a general-purpose AI. It uses Llama3 (default), Phi3-mini (fast), or Llama3 with more tokens (smart mode).</p>", unsafe_allow_html=True)

        with st.expander("What is AtlasAI?"):
            st.markdown("<p style='color: #FFFFFF; font-size: 16px;'>AtlasAI is RAG-based — it only answers from your course videos giving exact video number and timestamp.</p>", unsafe_allow_html=True)

        with st.expander("How does OTP password reset work?"):
            st.markdown("<p style='color: #FFFFFF; font-size: 16px;'>Enter email → receive 6-digit OTP → verify within 1 minute → set new password.</p>", unsafe_allow_html=True)

        with st.expander("Why does AtlasAI say Not found in course content?"):
            st.markdown("<p style='color: #FFFFFF; font-size: 16px;'>The topic is not in the course videos. Try rephrasing or asking about a specific concept from the course.</p>", unsafe_allow_html=True)

        with st.expander("How do I delete my account?"):
            st.markdown("<p style='color: #FFFFFF; font-size: 16px;'>Go to <b>Privacy</b> → <b>Danger Zone</b> → <b>Delete Account</b>. This is permanent and cannot be undone.</p>", unsafe_allow_html=True)

        with st.expander("Is my data private?"):
            st.markdown("<p style='color: #FFFFFF; font-size: 16px;'>Yes. All AI models run locally via Ollama. No data is sent to external services like OpenAI.</p>", unsafe_allow_html=True)

        with st.expander("What does Smart speed mode do in EchoAI?"):
            st.markdown("<p style='color: #FFFFFF; font-size: 16px;'>Smart mode uses 2000 tokens vs 600 default — giving longer, more detailed responses for complex topics.</p>", unsafe_allow_html=True)

        with st.expander("How do I change my profile information?"):
            st.markdown("<p style='color: #FFFFFF; font-size: 16px;'>Go to <b>Profile</b> tab → click <b>Edit</b> → update your info → click <b>Save</b>.</p>", unsafe_allow_html=True)

        st.divider()

        # --- CONTACT FORM ---
        
        # Using columns to keep the form neat
        contact_col, info_col = st.columns([2, 1])

        st.subheader("Report an Issue")
        contact_col, info_col = st.columns([2, 1])

        with contact_col:
            issue_type = st.selectbox(
                "Issue Category",
                ["Bug Report", "Feature Request", "Account Access", "AI Response Quality", "Other"],
                key="help_issue_type"
            )
            message = st.text_area("Describe your issue", placeholder="Please provide details...", key="help_message")
            b1, b2 = st.columns([2, 1])
            with b2:
                if st.button("Submit Report", type="primary", use_container_width=True):
                    if message:
                        st.success("Report submitted!")
                        st.toast("Ticket created!")
                        add_activity("🐛", "Issue Reported", f"{issue_type}: {message[:40]}")
                    else:
                        st.error("Please describe the issue first.")

        with info_col:
            st.info("**Technical Support**")
            st.caption("Response time: < 24 hours")
            st.write("---")
            st.write("**Location**")
            user_country = st.session_state.profile_data.get("country", "India")
            st.caption(user_country)
    

# --- SECURITY VIEW ---
def render_security():
    st.title("Security & Sessions")
    st.caption("Protect your account by managing password, authentication, and active sessions.")
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
    btn_spacer, btn_col1, btn_col2 = st.columns([6, 2, 2])
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
                # Replace with your actual get_password_status check
            if st.button("Save", key="save_pw_btn", type="primary", use_container_width=True):
                add_activity("🔐", "Password Changed", "User updated account password")
                status = get_password_status(new_pw)
                if new_pw == confirm_pw and all(status.values()):
                    st.session_state.edit_mode = False
                    st.success("Password Updated!")
                    st.rerun()
                else:
                    st.session_state.pw_error = True

            # Show error below (FULL WIDTH)
            if st.session_state.get("pw_error"):
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
                            add_activity("🛡️", "2FA Enabled", "Two-factor authentication enabled")
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
                add_activity("⚠️", "2FA Disabled", "Two-factor authentication disabled")
                st.session_state.two_fa_enabled = False
                st.rerun()

    st.divider()

    # --- SECTION 3: ACTIVE SESSIONS ---
    st.subheader("Active Sessions")
    
    #  Dynamic — store sessions in session_state
    if "active_sessions" not in st.session_state:
        import platform
        import socket
        
        # Get system details
        os_name = platform.system()
        hostname = socket.gethostname()
        
        # Detect Browser from Headers
        user_agent = st.context.headers.get("User-Agent", "")
        
        if "Firefox" in user_agent:
            browser_name = "Firefox Browser"
        elif "Edg" in user_agent:
            browser_name = "Edge Browser"
        elif "Chrome" in user_agent:
            browser_name = "Chrome Browser"
        elif "Safari" in user_agent:
            browser_name = "Safari Browser"
        else:
            browser_name = "Web Browser"

        st.session_state.active_sessions = [
            {
                "id": "current",
                "device": f"{os_name} — {hostname}",
                "location": st.session_state.profile_data.get("country", "India"),
                "status": "Active now",
                "browser": browser_name,
                "current": True
            }
        ]
    for session in st.session_state.active_sessions:
        with st.container():
            sc1, sc2 = st.columns([3, 1])
            with sc1:
                st.markdown(f"**{session['device']} — {session['location']}**")
                color = "#4CAF50" if session["current"] else "#FFFFFF"
                opacity = "1" if session["current"] else "0.7"
                st.markdown(
                    f"<p style='color:{color}; font-size:14px; margin-top:-10px; opacity:{opacity};'>"
                    f"{session['status']} • {session['browser']}</p>",
                    unsafe_allow_html=True
                )
            with sc2:
                if session["current"]:
                    st.button("Current", disabled=True, key=f"sess_{session['id']}", use_container_width=True)
                else:
                    if st.button("Revoke", key=f"rev_{session['id']}", use_container_width=True):
                        st.session_state.active_sessions = [
                            s for s in st.session_state.active_sessions
                            if s["id"] != session["id"]
                        ]
                        add_activity("🔒", "Session Revoked", f"Revoked session: {session['device']}")
                        st.toast(f"Session revoked: {session['device']}")
                        st.rerun()

    st.divider()
    st.caption("🛡️ Security Tip: If you see a device you don't recognize, revoke it and change your password immediately.")

# CONNECTIONS
# CONNECTIONS
def render_connections(): 
    st.title("Connected Accounts") 
    st.caption("Manage your linked social and professional accounts for better integration.") 
    st.divider()

    profile = st.session_state.profile_data

    def account_row(name, icon, url_key, placeholder_url, open_url):
        conn_data    = st.session_state.connections[name]
        is_connected = conn_data["connected"]
        # ✅ Uses real URL from profile_data
        linked_url   = profile.get(url_key, "")

        col1, col2, col3 = st.columns([0.5, 3, 1.5])
        with col1:
            st.markdown(f"### {icon}")
        with col2:
            st.markdown(f"**{name}**")
            if is_connected and linked_url:
                st.caption(f"Linked: {linked_url}")
                st.markdown(
                    f"<a href='{linked_url}' target='_blank' style='color:#3b82f6; font-size:12px;'>Open {name} ↗</a>",
                    unsafe_allow_html=True
                )
            elif is_connected and not linked_url:
                st.caption("Connected (no URL saved in profile)")
            else:
                st.caption("Not connected")
                if not linked_url:
                    st.markdown(
                        f"<span style='color:#f59e0b; font-size:12px;'>⚠️ Add {name} URL in Profile tab first</span>",
                        unsafe_allow_html=True
                    )

        with col3:
            if is_connected:
                if st.button("Disconnect", key=f"btn_dis_{name}", use_container_width=True):
                    st.session_state.connections[name]["connected"] = False
                    st.session_state.connections[name]["email"]     = None
                    add_activity("❌", f"{name} Disconnected", f"{name} account removed")
                    st.success(f"{name} disconnected.")
                    st.rerun()
            else:
                if not linked_url:
                    st.button("Connect", key=f"btn_con_{name}", use_container_width=True, disabled=True)
                    st.caption("Add URL in Profile first")
                else:
                    if st.button("Connect", key=f"btn_con_{name}", type="primary", use_container_width=True):
                        st.session_state.connections[name]["connected"] = True
                        st.session_state.connections[name]["email"]     = linked_url
                        add_activity("🔗", f"{name} Connected", f"{name} linked: {linked_url}")
                        st.success(f"{name} connected!")
                        st.rerun()
        st.divider()

    account_row("Google",   "🌐", "email",       "your@gmail.com",                  "https://myaccount.google.com")
    account_row("GitHub",   "💻", "github_url",  "https://github.com/username",     "https://github.com")
    account_row("LinkedIn", "👔", "linkedin_url","https://linkedin.com/in/username","https://linkedin.com")

    st.info("💡 Tip: Add your GitHub and LinkedIn URLs in the **Profile** tab to enable connection.")

# PRIVACY
# --- PRIVACY VIEW ---
def render_privacy():
    st.title("Privacy & Data Control")
    st.caption("Control how your data is used and manage your privacy settings.")
    st.divider()

    # ---- INIT PRIVACY STATE ----
    if "privacy_public"       not in st.session_state: st.session_state.privacy_public       = True
    if "privacy_seo"          not in st.session_state: st.session_state.privacy_seo           = False
    if "privacy_ai_personal"  not in st.session_state: st.session_state.privacy_ai_personal  = True

    # --- SECTION 1: VISIBILITY ---
    st.subheader("Profile Visibility")

    with st.container():
        v1, v2 = st.columns([3, 1])
        with v1:
            st.markdown("**Public Profile**")
            st.caption("Allow others to see your projects, skills, and learning progress.")
        with v2:
            new_public = st.toggle(
                "Public",
                value=st.session_state.privacy_public,
                key="visibility_toggle",
                label_visibility="collapsed"
            )
        if new_public != st.session_state.privacy_public:
            st.session_state.privacy_public = new_public
            status = "Public" if new_public else "Private"
            # ✅ Would call backend: PATCH /user/privacy {"public": new_public}
            add_activity("🛡️", "Profile Visibility Changed", f"Profile set to {status}")
            st.toast(f"Profile set to **{status}**")
            st.rerun()

    # Show current status
    if st.session_state.privacy_public:
        st.success("Your profile is **Public** — visible to others.")
    else:
        st.warning("Your profile is **Private** — only you can see it.")

    with st.container():
        s1, s2 = st.columns([3, 1])
        with s1:
            st.markdown("**Search Engine Indexing**")
            st.caption("Allow Google to index your profile.")
        with s2:
            new_seo = st.toggle("SEO", value=st.session_state.privacy_seo, key="seo_toggle", label_visibility="collapsed")
        if new_seo != st.session_state.privacy_seo:
            st.session_state.privacy_seo = new_seo
            add_activity("🔍", "SEO Setting Changed", f"Search indexing: {'on' if new_seo else 'off'}")

    st.divider()

    # --- SECTION 2: DATA & AI ---
    st.subheader("Data & Personalization")
    with st.container():
        a1, a2 = st.columns([3, 1])
        with a1:
            st.markdown("**AI Personalization**")
            st.caption("Allow the system to use your activity to improve AI recommendations.")
        with a2:
            new_ai = st.toggle("Enabled", value=st.session_state.privacy_ai_personal, key="ai_toggle", label_visibility="collapsed")
        if new_ai != st.session_state.privacy_ai_personal:
            st.session_state.privacy_ai_personal = new_ai

    st.divider()

    # --- SECTION 3: EXPORT ---
    st.subheader("Your Personal Data")
    with st.container():
        d1, d2 = st.columns([3, 1])
        with d1:
            st.markdown("**Export Account Data**")
            st.caption("Download a copy of your account data anytime.")
        with d2:
            try:
                # ✅ Dynamic — real profile data
                profile = st.session_state.profile_data
                export_payload = {
                    "user_info": {
                        "name":          profile.get("name", "User"),
                        "email":         profile.get("email", ""),
                        "qualification": profile.get("qualification", ""),
                        "country":       profile.get("country", "India"),
                        "username":      profile.get("username", ""),
                        "gender":        profile.get("gender", ""),
                        "goal":          profile.get("goal", ""),
                        "level":         profile.get("level", "Beginner"),
                        "interests":     ", ".join(profile.get("interest", [])),
                    },
                    "security_settings": {
                        "two_factor_enabled": st.session_state.get("two_fa_enabled", False),
                        "profile_visibility": "Public" if st.session_state.privacy_public else "Private"
                    },
                    "projects": ["NexaAI — AI Teaching Assistant"]
                }
                pdf_file = generate_pdf(export_payload)
                clicked = st.download_button(
                    label="Download PDF",
                    data=pdf_file,
                    file_name=f"{profile.get('name','user')}_data.pdf",
                    mime="application/pdf",
                    use_container_width=True
                )
                if clicked:
                    add_activity("📄", "Data Exported", "User downloaded profile PDF")
            except Exception as e:
                st.error(f"Export Error: {str(e)}")

    st.divider()

    # --- SECTION 4: DANGER ZONE ---
    st.subheader("Danger Zone")
    with st.container():
        del1, del2 = st.columns([3, 1])
        with del1:
            st.markdown("**Delete Account**")
            st.caption("Permanently remove your account and all associated data. This cannot be undone.")
        with del2:
            if st.button("Delete", type="primary", use_container_width=True):
                st.session_state.show_delete_warning = True

    if st.session_state.get("show_delete_warning"):
        st.warning("⚠️ Are you sure? This will permanently erase all your data.")
        c1, c2, _ = st.columns([1, 1, 2])
        with c1:
            if st.button("Confirm Delete", type="primary", key="final_del", use_container_width=True):
                add_activity("🗑️", "Account Deleted", "User permanently deleted account")
                # ✅ Would call: DELETE /user/{id} on backend
                st.success("Account deleted.")
                import time; time.sleep(1)
                st.session_state.clear()
                st.session_state.page = "login"
                st.rerun()
        with c2:
            if st.button("Cancel", key="cancel_del", use_container_width=True):
                st.session_state.show_delete_warning = False
                st.rerun()

# PROFILE INSIGHTS
# --- PROFILE INSIGHTS VIEW ---
def render_insights():
    st.title("Profile Insights")
    st.caption("Track your learning progress and understand your skill development.")
    st.divider()

    # =========================
    # DYNAMIC DATA SOURCE
    # =========================
    if "insights_data" not in st.session_state:
        st.session_state.insights_data = None

    def load_default_insights():
        return {
            "metrics": {"completed": 0, "in_progress": 0, "readiness": "0%"},
            "suggestions": []
        }

    insights_data = st.session_state.insights_data or load_default_insights()
    metrics = insights_data.get("metrics", {})
    suggestions = insights_data.get("suggestions", [])

    # =========================
    # SECTION 1: METRICS
    # =========================
    m1, m2, m3 = st.columns(3)
    with m1:
        st.metric("Topics Completed", metrics.get("completed", 0))
    with m2:
        st.metric("In Progress", metrics.get("in_progress", 0))
    with m3:
        st.metric("Skill Readiness", metrics.get("readiness", "0%"))

    st.divider()

    # =========================
    # SECTION 2: PROGRESS BAR
    # =========================
    st.subheader("Overall Learning Progress")

    completed = int(metrics.get("completed", 0))
    in_progress = int(metrics.get("in_progress", 0))
    total = completed + in_progress
    progress_val = int((completed / total) * 100) if total > 0 else 0

    col_p1, col_p2 = st.columns([4, 1])
    with col_p1:
        st.progress(progress_val / 100)
    with col_p2:
        st.write(f"**{progress_val}%**")

    st.divider()

    # =========================
    # SECTION 3: SUGGESTIONS
    # =========================
    st.subheader("Personalized Recommendations")
    st.caption("Based on your profile, EchoAI generates personalized insights for your learning journey.")

    def insight_card(title, text, type="info"):
        if type == "info":
            st.info(f"**{title}**")
        elif type == "success":
            st.success(f"**{title}**")
        elif type == "warning":
            st.warning(f"**{title}**")
        st.markdown(f"""
            <p style='color: #FFFFFF; font-size: 16px; margin-top: -10px; margin-bottom: 20px;'>
                {text}
            </p>
        """, unsafe_allow_html=True)

    if suggestions:
        cols = st.columns(2)
        for i, item in enumerate(suggestions):
            with cols[i % 2]:
                insight_card(
                    item.get("title", ""),
                    item.get("text", ""),
                    item.get("type", "info")
                )
    else:
        st.info("No insights yet. Click **Refresh Analysis** to generate insights using EchoAI.")

    # =========================
    # SECTION 4: ACTION — EchoAI powered
    # =========================
    st.divider()
    _, q_col = st.columns([3, 1])
    with q_col:
        if st.button("Refresh Analysis", use_container_width=True):
            st.toast("EchoAI is analyzing your profile...")

            # ✅ Build prompt from user profile
            profile = st.session_state.profile_data
            name    = profile.get("name", "User")
            goal    = profile.get("goal", "Not specified")
            level   = profile.get("level", "Beginner")
            interest = ", ".join(profile.get("interest", [])) or "Not specified"
            qualification = profile.get("qualification", "Not specified")
            country = profile.get("country", "India")

            prompt = f"""
You are an expert AI learning coach analyzing a student profile to generate profile insights.

Student Profile:
- Name: {name}
- Qualification: {qualification}
- Country: {country}
- Learning Goal: {goal}
- Skill Level: {level}
- Interests: {interest}

Based on this profile, generate:
1. Metrics estimation (topics completed, in progress, readiness percentage) based on skill level
2. 4 personalized learning recommendations

Return ONLY a JSON object in this exact format (no extra text, no markdown):
{{
  "metrics": {{
    "completed": <number based on level: Beginner=5, Intermediate=15, Advanced=30>,
    "in_progress": <number: Beginner=3, Intermediate=7, Advanced=10>,
    "readiness": "<percentage: Beginner=40%, Intermediate=70%, Advanced=90%>"
  }},
  "suggestions": [
    {{"title": "Short Title", "text": "Detailed actionable advice.", "type": "info"}},
    {{"title": "Short Title", "text": "Detailed actionable advice.", "type": "success"}},
    {{"title": "Short Title", "text": "Detailed actionable advice.", "type": "warning"}},
    {{"title": "Short Title", "text": "Detailed actionable advice.", "type": "info"}}
  ]
}}
"""
            try:
                token = st.session_state.get("token")
                headers = {"Authorization": f"Bearer {token}"}

                # ✅ Call EchoAI backend
                res = requests.post(
                    "http://localhost:8000/chat/",
                    json={
                        "messages": [{"role": "user", "content": prompt}],
                        "speed": "default"
                    },
                    headers=headers,
                    timeout=60
                )

                if res.status_code == 200:
                    raw = res.json().get("response", "")
                    # ✅ Clean JSON from response
                    raw = raw.strip()
                    if "```" in raw:
                        raw = raw.split("```")[1]
                        if raw.startswith("json"):
                            raw = raw[4:]
                    parsed = json.loads(raw.strip())
                    st.session_state.insights_data = parsed
                    add_activity("📊", "Profile Insights Refreshed", "EchoAI generated new profile insights")
                    st.success("Insights updated by EchoAI!")
                else:
                    st.error("Failed to get insights. Try again.")

            except Exception as e:
                st.error(f"EchoAI Error: {str(e)}")

            st.rerun()

# --- AI INSIGHTS VIEW ---
def render_ai():
    st.title("AI Insights & Recommendations")
    st.caption("Smart recommendations generated based on your profile and skill level.")
    st.divider()

    # ✅ Dynamic user data (NOT static anymore)
    profile = st.session_state.profile_data
    goal = profile.get("goal", "Technical Role")
    level = profile.get("level", "Intermediate")

    # ✅ Dynamic suggestion logic (TEXT SAME STYLE, but selected smartly)
    if level == "Beginner":
        suggestions = [
            {"title": "Focus: Fundamentals", "text": "Build strong basics in Python, logic building, and problem-solving.", "type": "info"},
            {"title": "Focus: Guided Learning", "text": "Follow structured courses instead of random tutorials.", "type": "success"},
            {"title": "Action: Practice", "text": "Solve basic problems daily to build confidence.", "type": "warning"},
            {"title": "Core Strategy", "text": "Consistency is more important than complexity at this stage.", "type": "info"}
        ]

    elif level == "Intermediate":
        suggestions = [
            {"title": "Focus: Portfolio Projects", "text": "Move beyond basic scripts. Build end-to-end applications that solve specific industry problems.", "type": "info"},
            {"title": "Focus: Real-world Thinking", "text": "Start understanding system design and real use-cases.", "type": "success"},
            {"title": "Action: Practical Tasks", "text": "Work on debugging and data cleaning tasks.", "type": "warning"},
            {"title": "Core Strategy", "text": "Shift from theory to practical execution.", "type": "info"}
        ]

    else:  # Advanced
        suggestions = [
            {"title": "Focus: Specialization", "text": "Choose a niche like AI, Backend, or Data Engineering.", "type": "info"},
            {"title": "Focus: Scaling Systems", "text": "Work on scalable architectures and optimization.", "type": "success"},
            {"title": "Action: Open Source", "text": "Contribute to real-world projects.", "type": "warning"},
            {"title": "Core Strategy", "text": "Build authority in one domain instead of being generic.", "type": "info"}
        ]

    # --- STATUS ---
    c1, c2 = st.columns(2)
    with c1:
        st.info(f"**Current Goal:** {goal}")
    with c2:
        st.success(f"**Skill Level:** {level}")

    st.divider()

    # --- CARDS ---
    st.subheader("Smart Recommendations")

    def ai_card(title, text, type="info"):
        if type == "info": st.info(f"**{title}**")
        elif type == "success": st.success(f"**{title}**")
        elif type == "warning": st.warning(f"**{title}**")

        st.markdown(f"""
            <p style='color: #FFFFFF; font-size: 16px; margin-top: -10px; margin-bottom: 20px;'>
                {text}
            </p>
        """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        ai_card(**suggestions[0])
        ai_card(**suggestions[2])
    with col2:
        ai_card(**suggestions[1])
        ai_card(**suggestions[3])

    st.divider()

    _, btn_col = st.columns([3, 1])
    with btn_col:
        if st.button("Generate New Insights", use_container_width=True):
            st.toast("AI is analyzing your profile...")
            st.rerun()

# active log
# --- ACTIVITY LOG VIEW ---
def render_activity():
    st.title("Activity Log")
    st.caption("A record of your recent actions and account activity.")
    st.divider()

    # ✅ 1. Initialize dynamic activity store
    if "activity_logs" not in st.session_state:
        st.session_state.activity_logs = []

    logs = st.session_state.activity_logs

    # ✅ 2. Empty state
    if len(logs) == 0:
        st.info("No activity yet. Your actions will appear here.")
        return

    # ✅ 3. Timeline Renderer
    for i, log in enumerate(reversed(logs)):  # latest first
        with st.container():
            col_icon, col_info, col_time = st.columns([0.5, 3, 1.5])

            with col_icon:
                st.markdown(f"### {log['icon']}")

            with col_info:
                st.markdown(f"**{log['event']}**")
                st.markdown(
                    f"<p style='color: #FFFFFF; font-size: 15px; opacity: 0.9; margin-top: -10px;'>{log['detail']}</p>",
                    unsafe_allow_html=True
                )

            with col_time:
                st.markdown(
                    f"<p style='text-align: right; color: #AAAAAA; font-style: italic; font-size: 13px;'>{log['time']}</p>",
                    unsafe_allow_html=True
                )

        if i < len(logs) - 1:
            st.divider()

    # ✅ 4. Footer actions
    st.divider()
    col1, col2 = st.columns([2, 1])

    with col2:
        if st.button("Refresh Logs", use_container_width=True):
            st.toast("Fetching latest logs...")
            st.rerun()

    with col1:
        if st.button("Clear Logs", use_container_width=True):
            st.session_state.activity_logs = []
            st.toast("Logs cleared")
            st.rerun()

from datetime import datetime
import pytz

def add_activity(icon, event, detail):
    if "activity_logs" not in st.session_state:
        st.session_state.activity_logs = []

    tz = st.session_state.get("app_timezone", "IST (UTC+5:30)")

    tz_map = {
        "IST (UTC+5:30)": "Asia/Kolkata",
        "EST (UTC-5)": "US/Eastern",
        "PST (UTC-8)": "US/Pacific",
        "GMT (UTC+0)": "UTC",
        "UTC": "UTC"
    }

    zone = pytz.timezone(tz_map.get(tz, "Asia/Kolkata"))
    current_time = datetime.now(zone).strftime("%d %b, %I:%M %p")

    st.session_state.activity_logs.append({
        "icon": icon,
        "event": event,
        "detail": detail,
        "time": current_time
    })
# --- BILLING / EXPLORE PLANS VIEW ---
def render_billing():
    from billing import render_billing as _billing
    _billing()

def render_plus_payment():
    from billing import render_plus_payment as _plus
    _plus()

def render_pro_payment():
    from billing import render_pro_payment as _pro
    _pro()
# --- ABOUT VIEW ---
def render_about():
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
                    <span class="tech-badge">v1.0.2-stable</span>
                </div>
            </div>
        """, unsafe_allow_html=True)

    # 3. Content Columns
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Project Mission")
        st.markdown(f"""
            <p style='color: #FFFFFF; font-size: 16px; opacity: 0.9;'>
                To bridge the gap between academic theory and industry readiness. 
                This assistant analyzes learning patterns to suggest real-world 
                SRE and AI workflows.
            </p>
        """, unsafe_allow_html=True)

    with col2:
        st.subheader("Security & Privacy")
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
        st.markdown("<p style='text-align: center; color: #8B949E;'>Developed by NexaAI Teams<br>© 2026 AI Learning Hub</p>", unsafe_allow_html=True)
        
        # Social/Github Link (Optional)
        st.button("View Source on GitHub", use_container_width=True)

    # --- QUICK ACTION ---
    if st.button("Check for Updates", use_container_width=True):
        st.toast("You are using the latest version!")
def init_profile_state():
    if "profile_data" not in st.session_state:
        st.session_state.profile_data = load_default_profile()
        
    if "connections" not in st.session_state:
        st.session_state.connections = {
            "Google": {"connected": False, "email": ""},
            "GitHub": {"connected": False, "email": ""},
            "LinkedIn": {"connected": False, "email": ""}
        }
    if "edit_mode" not in st.session_state: 
        st.session_state.edit_mode = False
    if "view" not in st.session_state:
        st.session_state.view = "Profile"

        
def render_app():
    # Top UI (always visible)
    inject_profile_styles()
    init_profile_state()
   # your popover
    render_sidebar()  # your sidebar

    # Page routing
    ROUTES = {
        "Profile": render_profile,
        "Settings": render_settings,
        "Security": render_security,
        "Connections": render_connections,
        "Privacy": render_privacy,
        "Insights": render_insights,
        "AI": render_ai,
        "Activity": render_activity,
        "Billing": render_billing,
        "About": render_about,
        "Plus_Payment": render_plus_payment,
        "Pro_Payment": render_pro_payment,
    }

    ROUTES.get(st.session_state.view, render_profile)()
def main():
    base_dir = os.path.dirname(os.path.dirname(__file__))
    logo_path = os.path.join(base_dir, "assets", "logo.png")

    try:
        # 2. Load the image file
        logo_img = Image.open(logo_path)
        
        # 3. Apply the logo to the page configuration
        st.set_page_config(
            page_title="Nexa AI- User Profile", 
            page_icon=logo_img,  # ✅ This adds the logo to your browser tab
            layout="wide"
        )
    except Exception:
        # Fallback if image path is incorrect
        st.set_page_config(page_title="Nexa AI- User Profile", layout="wide")

    render_app()    
if __name__ == "__main__":    
    main()