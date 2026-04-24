# modules/llm_ui.py

import streamlit as st
import time
import uuid
from datetime import datetime
import requests
import os
from PIL import Image

# --- 1. ARCHITECTURAL DESIGN SYSTEM (CSS) ---
def inject_ui_styles():
    st.markdown(f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&display=swap');
        @import url('https://fonts.googleapis.com/css2?family=Lexend+Deca:wght@300;400;600&display=swap');

        .stApp {{ background-color: #0a0a0a; color: #f3f4f6; font-family: 'Inter', sans-serif; line-height: 1.2; }}
        [data-testid="stSidebarNav"] {{ display: none !important; }}

        .hero-title {{
            text-align: center; font-family: 'Lexend Deca', sans-serif;
            font-size: 4rem; font-weight: 600; letter-spacing: -4px; 
            background: linear-gradient(to bottom, #ffffff 30%, #101db5 100%);
            -webkit-background-clip: text; -webkit-text-fill-color: transparent;
            letter-spacing: 0px;
            margin-bottom: 0px;
            
        }}
        .hero-subtitle {{
            text-align: center; color: #9ca3af; font-size: 1.1rem; 
            font-weight: 300; margin-bottom: 40px;
            margin-bottom: 25px;
        }}
        .glass-card {{
            background: rgba(255, 255, 255, 0.03);
            border: 1px solid rgba(255, 255, 255, 0.05);
            border-radius: 16px;
            padding: 25px;
            margin-top: 20px;
        }}
        [data-testid="stSidebar"] {{ background-color: #0d0d0d; border-right: 1px solid #1e1e1e; }}

        div.stButton > button {{
            background-color: rgba(255, 255, 255, 0.02) !important;
            color: #9ca3af !important;
            border: 1px solid #262626 !important;
            border-radius: 10px; width: 100%; text-align: left;
            transition: all 0.2s ease;
        }}
        div.stButton > button:hover {{
            border-color: #3b82f6 !important;
            color: #3b82f6 !important;
            background-color: rgba(59, 130, 246, 0.08) !important;
            transform: translateY(-1px);
        }}
        div[data-testid="stRadio"] > label {{
            color: #4b5563 !important; font-size: 0.7rem !important;
            font-weight: 700 !important; text-transform: uppercase;
        }}
        .user-bubble {{
            background: linear-gradient(145deg, #1a1a1a 0%, #0f0f0f 100%);
            border: 1px solid #2e2e2e; 
            padding: 12px 18px;
            border-radius: 20px 20px 4px 20px; 
            margin: 10px 0 10px auto;
            max-width: 80%; width: fit-content; display: block; font-size: 0.95rem; color: #ffffff;
        }}
        [data-testid="stChatMessage"] {{
            width: fit-content !important;
            max-width: 85% !important;
            border-radius: 12px;
        }}

        /* ---- Delete Dialog Styling ---- */
        div[data-testid="stDialog"] {{
            display: flex;
            align-items: center;
            justify-content: center;
        }}
        div[data-testid="stDialog"] button[kind="primary"] {{
            background-color: #ef4444 !important;
            border-color: #ef4444 !important;
            color: white !important;
        }}
        div[data-testid="stDialog"] button[kind="primary"]:hover {{
            background-color: #dc2626 !important;
            border-color: #dc2626 !important;
        }}
        div[data-testid="stDialog"] button[kind="secondary"] {{
            background-color: transparent !important;
            color: #9ca3af !important;
            border-color: #262626 !important;
        }}

        /* ---- ••• Popover Menu Styling ---- */
        div[data-testid="stPopover"] > div > button {{
            background-color: transparent !important;
            border: none !important;
            color: #6b7280 !important;
            font-size: 0.85rem !important;
            font-weight: 700 !important;
            letter-spacing: 2px !important;
            padding: 2px 4px !important;
            width: auto !important;
            min-width: unset !important;
        }}
        div[data-testid="stPopover"] > div > button:hover {{
            color: #3b82f6 !important;
            background-color: transparent !important;
            border: none !important;
        }}
        div[data-testid="stPopoverBody"] button {{
            width: 100% !important;
            text-align: left !important;
            background-color: transparent !important;
            color: #d1d5db !important;
            border: none !important;
            font-size: 0.85rem !important;
            padding: 6px 10px !important;
        }}
        div[data-testid="stPopoverBody"] button:hover {{
            color: #3b82f6 !important;
            background-color: rgba(59,130,246,0.08) !important;
            border-radius: 6px !important;
        }}
        .chat-scroll-area {{
            max-height: calc(100vh - 520px);
            overflow-y: auto;
            overflow-x: hidden;
            padding: 4px 2px;
        }}

        /* scrollbar */
        .chat-scroll-area::-webkit-scrollbar {{
            width: 3px;
        }}
        .chat-scroll-area::-webkit-scrollbar-thumb {{
            background: #2e2e2e;
            border-radius: 10px;
        }}

        /* Sticky bottom section */
        .sidebar-bottom-section {{
            position: sticky;
            bottom: 0;
            background-color: #0d0d0d;
            padding-top: 8px;
            z-index: 999;
            border-top: 1px solid #1e1e1e;
        }}
        /* ---- Popover Menu Precision Styling ---- */

/* 1. Force the container to match the sidebar background exactly */
div[data-testid="stPopoverBody"] {{
    background-color: #0d0d0d !important; /* Matches your sidebar */
    border: 2px solid #1e1e1e !important; /* Subtle border for definition */
    box-shadow: 0px 4px 15px rgba(0, 0, 0, 0.5) !important;
    padding: 4px !important;
    min-width: 150px !important;
}}

/* 2. Strip any background from the inner Streamlit wrapper */
div[data-testid="stPopoverBody"] > div {{
    background-color: transparent !important;
}}

/* 3. Style the buttons to be clean and flat */
div[data-testid="stPopoverBody"] button {{
    background-color: transparent !important;
    border: none !important;
    box-shadow: none !important;
    color: #d1d5db !important;
    width: 100% !important;
    text-align: left !important;
    padding: 8px 12px !important;
    font-size: 0.85rem !important;
}}

/* 4. Subtle hover tint instead of solid gray */
div[data-testid="stPopoverBody"] button:hover {{
    background-color: rgba(59, 130, 246, 0.1) !important;
    color: #3b82f6 !important;
    border-radius: 1px !important;
}}
                        </style>
    """, unsafe_allow_html=True)

# --- 2. CORE ENGINE & STATE ---
def init_store():
    if "chats" not in st.session_state: st.session_state.chats = {}
    if "active_id" not in st.session_state: st.session_state.active_id = None
    if "ai_mode" not in st.session_state: st.session_state.ai_mode = "AtlasAI"
    if "echo_speed" not in st.session_state: st.session_state.echo_speed = "default"
    if "rename_cid" not in st.session_state: st.session_state.rename_cid = None

def create_thread():
    cid = str(uuid.uuid4())
    st.session_state.chats[cid] = {
        "title": "New Chat",
        "messages": [],
        "mode": st.session_state.ai_mode,
        "ts": datetime.now().strftime("%H:%M")
    }
    st.session_state.active_id = cid

# -------------------- DELETE DIALOG --------------------
@st.dialog("Delete Chat?")
def delete_chat_dialog(cid):
    title = st.session_state.chats[cid]["title"]
    st.write(f'Are you sure you want to delete **"{title}"**?')
    st.warning("This action cannot be undone.")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Delete", type="primary", use_container_width=True):
            del st.session_state.chats[cid]
            if st.session_state.active_id == cid:
                st.session_state.active_id = None
            st.rerun()
    with col2:
        if st.button("Cancel", type="secondary", use_container_width=True):
            st.rerun()

# -------------------- RENAME DIALOG --------------------
@st.dialog("Rename Chat")
def rename_chat_dialog(cid):
    current_title = st.session_state.chats[cid]["title"]
    new_title = st.text_input("New name", value=current_title, max_chars=40)
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Save", type="primary", use_container_width=True):
            if new_title.strip():
                st.session_state.chats[cid]["title"] = new_title.strip()
            st.rerun()
    with col2:
        if st.button("Cancel", type="secondary", use_container_width=True):
            st.rerun()

# --- 3. UI COMPONENTS ---
def render_sidebar():
    with st.sidebar:

        # -------- LOGO --------
        st.markdown("<h2 style='letter-spacing:-1.5px; font-weight:600;'>Nexa<span style='color:#3b82f6;'>AI</span></h2>", unsafe_allow_html=True)
        st.markdown('<div style="margin-top:20px;"></div>', unsafe_allow_html=True)

        # -------- AI MODE --------
        mode = st.radio(
            "Choose Assistant",
            ["AtlasAI", "EchoAI"],
            help="AtlasAI: Video-based learning | EchoAI: Quick answers"
        )

        if st.session_state.ai_mode == "EchoAI":
            speed = st.radio(
                "Response Speed",
                ["Default", "Fast", "Smart"],
                index={"default": 0, "fast": 1, "smart": 2}.get(st.session_state.echo_speed, 0),
                help="Default: llama3 | Fast: phi3-mini | Smart: qwen2.5:7b"
            )
            st.session_state.echo_speed = {"Default": "default", "Fast": "fast", "Smart": "smart"}[speed]

        if mode != st.session_state.ai_mode:
            st.session_state.ai_mode = mode
            st.session_state.active_id = None
            st.rerun()

        # -------- NEW CHAT --------
        st.markdown("---")
        if st.button("＋ New Chat", use_container_width=True):
            create_thread()
            st.rerun()

        # -------- HISTORY LABEL --------
        st.markdown(
            '<div style="color:#4b5563; font-size:0.7rem; font-weight:700; text-transform:uppercase; margin:12px 0 6px 5px;">History</div>',
            unsafe_allow_html=True
        )

        # -------- SEARCH --------
        find_chat = st.text_input("Find Chat", placeholder="Search Chat...", label_visibility="collapsed")

        chat_list = list(reversed(list(st.session_state.chats.items())))
        filtered_chats = [item for item in chat_list if find_chat.lower() in item[1]['title'].lower()]

        # -------- SCROLLABLE AREA — open div --------
        st.markdown('<div class="chat-scroll-area">', unsafe_allow_html=True)

        if not filtered_chats:
            st.caption("No chat found.")
        else:
            for cid, data in filtered_chats:
                is_active = cid == st.session_state.active_id
                cols = st.columns([0.78, 0.22])
                with cols[0]:
                    label = f"{data['title'][:16]}"
                    if st.button(label, key=f"n_{cid}", type="primary" if is_active else "secondary"):
                        st.session_state.active_id = cid
                        st.rerun()
                with cols[1]:
                    with st.popover("•••"):
                        if st.button("Rename", key=f"ren_{cid}", use_container_width=True):
                            rename_chat_dialog(cid)
                        if st.button("Delete", key=f"del_{cid}", use_container_width=True):
                            delete_chat_dialog(cid)

        # -------- SCROLLABLE AREA — close div --------
        st.markdown('</div>', unsafe_allow_html=True)

        # -------- STICKY BOTTOM --------
        st.markdown('<div class="sidebar-bottom-section">', unsafe_allow_html=True)

        user_name = st.session_state.get("profile_data", {}).get("name", "User")
        user_initial = user_name[0].upper() if user_name else "U"

        st.markdown(f"""
            <div style='display:flex; align-items:center; gap:10px; padding:6px 5px;'>
                <div style='background:#3b82f6; width:32px; height:32px; border-radius:50%;
                     display:flex; align-items:center; justify-content:center;
                     font-weight:bold; flex-shrink:0;'>{user_initial}</div>
                <div>
                    <p style='margin:0; font-size:0.85rem; font-weight:600;'>{user_name}</p>
                </div>
            </div>
        """, unsafe_allow_html=True)

        if st.button("View Profile", use_container_width=True):
            st.session_state.page = "profile"
            st.rerun()

        if st.button("Logout", use_container_width=True):
            st.session_state.clear()
            st.session_state.page = "login"
            st.rerun()

        st.markdown('</div>', unsafe_allow_html=True)

def render_message(role, text):
    if role == "user":
        st.markdown(f'<div class="user-bubble">{text}</div><div style="clear:both"></div>', unsafe_allow_html=True)
    else:
        # ✅ Use logo image as avatar for both AI modes
        logo_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "logo.png")
        try:
            from PIL import Image
            logo = Image.open(logo_path)
            with st.chat_message("assistant", avatar=logo):
                st.markdown(text)  # ✅ proper markdown rendering
        except Exception:
            with st.chat_message("assistant"):
                st.markdown(text)

def render_hero_screen():
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    _, mid, _ = st.columns([0.15, 0.7, 0.15])
    with mid:
        st.markdown(f'<h1 class="hero-title">{st.session_state.ai_mode}</h1>', unsafe_allow_html=True)
        desc = "Learn directly from your course videos with clear explanations and exact timestamps." if st.session_state.ai_mode == "AtlasAI" else "Need a quick answer? Get clear explanations instantly without watching the full lecture."
        st.markdown(f'<p class="hero-subtitle">{desc}</p>', unsafe_allow_html=True)

        if st.button(f"Start New {st.session_state.ai_mode} Session", use_container_width=True, type="primary"):
            create_thread()
            st.rerun()

        c1, c2 = st.columns(2)
        prompts = [
            ["Summaries Css Box Model", " Write a simple html skeleton for a webpage"],
            ["Where is margin taught?", "Where is SEO taught in this course?"]
        ]

        idx = 0 if st.session_state.ai_mode == "EchoAI" else 1
        with c1:
            if st.button(prompts[idx][0]):
                create_thread()
                st.session_state.chats[st.session_state.active_id]["messages"].append({"role": "user", "content": prompts[idx][0]})
                st.rerun()
        with c2:
            if st.button(prompts[idx][1]):
                create_thread()
                st.session_state.chats[st.session_state.active_id]["messages"].append({"role": "user", "content": prompts[idx][1]})
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

        with st.expander("See a preview of the response style"):

            if st.session_state.ai_mode == "EchoAI":
               st.markdown("""
                **User:** *What is the CSS Box Model?*  

                **EchoAI:** The CSS Box Model defines how elements are structured and spaced in a webpage.  
                It consists of content, padding, border, and margin, which together control layout and spacing.
                    """)

            else:  # AtlasAI
                st.markdown("""
        **User:** *Where is margin taught?*  

        **AtlasAI:** Margin is part of the CSS Box Model and controls the space outside an element.
        
        **Video:** x (CSS Box Model)  
        **Timestamp:** 12:40
                """)

def render_chat_interface():
    st.markdown(f"""
        <div style='display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #1e1e1e; padding-bottom: 10px; margin-bottom: 20px;'>
            <h3 style='margin:0;'>{st.session_state.ai_mode}</h3>
            <span style='background: #111; color: #3b82f6; font-size: 0.75rem; padding: 4px 12px; border-radius: 20px; border: 1px solid #3b82f6;'>Online</span>
        </div>
    """, unsafe_allow_html=True)

    chat = st.session_state.chats[st.session_state.active_id]

    if not chat['messages']:
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.info(f"**Welcome to your new {st.session_state.ai_mode} session.** Type your first message below or choose a starter.")

    for msg in chat['messages']:
        render_message(msg['role'], msg['content'])

    if prompt := st.chat_input(f"Message {st.session_state.ai_mode}..."):
        chat['messages'].append({"role": "user", "content": prompt})

        # ✅ AI-generated title — short, meaningful, based on user query
        if chat['title'] == "New Chat":
            try:
                token = st.session_state.get("token")
                headers = {"Authorization": f"Bearer {token}"}
                title_res = requests.post(
                    "http://localhost:8000/chat/",
                    json={
                        "messages": [
                            {
                                "role": "user",
                                "content": f"Generate a short chat title (max 5 words, no quotes, no punctuation) for this message: {prompt}"
                            }
                        ],
                        "speed": "fast"
                    },
                    headers=headers,
                    timeout=5
                )
                if title_res.status_code == 200:
                    ai_title = title_res.json().get("response", "").strip()
                    # Clean up — remove quotes, newlines, limit length
                    ai_title = ai_title.replace('"', '').replace("'", '').replace('\n', ' ').strip()
                    chat['title'] = ai_title[:35] if ai_title else prompt[:25] + "..."
                else:
                    chat['title'] = prompt[:25] + "..."
            except Exception:
                chat['title'] = prompt[:25] + "..."

        st.rerun()

    if chat['messages'] and chat['messages'][-1]['role'] == "user":
        # ✅ Load logo for avatar
        logo_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "logo.png")
        try:
            from PIL import Image
            logo = Image.open(logo_path)
            avatar = logo
        except Exception:
            avatar = None

        with st.chat_message("assistant", avatar=avatar):
            ph = st.empty()
            ph.markdown("Thinking...")

            try:
                token = st.session_state.get("token")
                headers = {"Authorization": f"Bearer {token}"}

                if st.session_state.ai_mode == "AtlasAI":
                    api_res = requests.post(
                        "http://localhost:8000/rag/",
                        json={"query": chat['messages'][-1]['content']},
                        headers=headers,
                        timeout=60
                    )
                else:
                    api_res = requests.post(
                        "http://localhost:8000/chat/",
                        json={
                            "messages": chat['messages'],
                            "speed": st.session_state.echo_speed
                        },
                        headers=headers,
                        timeout=180
                    )

                if api_res.status_code == 200:
                    full = api_res.json().get("response", "No response")
                else:
                    full = f"Error: {api_res.json().get('detail', 'Something went wrong')}"

            except requests.exceptions.Timeout:
                full = "Request timed out. Please try again."
            except Exception as e:
                full = f"Error: {str(e)}"

            # ✅ Streaming effect word by word
            display = ""
            for chunk in full.split():
                display += chunk + " "
                time.sleep(0.02)
                # Show plain text while streaming
                ph.markdown(display + "▌")

            # ✅ Final render with proper markdown (code blocks, bold, etc.)
            ph.markdown(full)
            chat['messages'].append({"role": "assistant", "content": full})

# --- 4. THE MASTER WRAPPER FUNCTION ---
def render_nexus_app():
    inject_ui_styles()
    init_store()
    render_sidebar()

    if not st.session_state.active_id:
        render_hero_screen()
    else:
        render_chat_interface()

# --- 5. ENTRY POINT ---
def main():
    base_dir = os.path.dirname(os.path.dirname(__file__))
    logo_path = os.path.join(base_dir, "assets", "logo.png")

    try:
        # 2. Load the image file
        logo_img = Image.open(logo_path)
        
        # 3. Apply the logo to the page configuration
        st.set_page_config(
            page_title="Nexa AI", 
            page_icon=logo_img,  # ✅ This adds the logo to your browser tab
            layout="wide"
        )
    except Exception:
        # Fallback if image path is incorrect
        st.set_page_config(page_title="Nexa AI", layout="wide")

    render_nexus_app()

if __name__ == "__main__":
    main()