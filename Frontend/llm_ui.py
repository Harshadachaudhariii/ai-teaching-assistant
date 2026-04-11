import streamlit as st
import time
import uuid
from datetime import datetime

# --- 1. ARCHITECTURAL DESIGN SYSTEM (CSS) ---
def inject_ui_styles():
    st.markdown(f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&display=swap');
        @import url('https://fonts.googleapis.com/css2?family=Lexend+Deca:wght@300;400;600&display=swap');

        .stApp {{ background-color: #0a0a0a; color: #f3f4f6; font-family: 'Inter', sans-serif; }}
        
        .hero-title {{
            text-align: center; font-family: 'Lexend Deca', sans-serif;
            font-size: 4rem; font-weight: 600; letter-spacing: -4px; 
            background: linear-gradient(to bottom, #ffffff 30%, #6b7280 100%);
            -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        }}
        .hero-subtitle {{
            text-align: center; color: #9ca3af; font-size: 1.1rem; 
            font-weight: 300; margin-bottom: 40px;
        }}

        [data-testid="stSidebar"] {{ background-color: #0d0d0d; border-right: 1px solid #1e1e1e; }}

        div.stButton > button {{
            background-color: rgba(255, 255, 255, 0.02) !important;
            color: #9ca3af !important;
            border: 1px solid #262626 !important;
            border-radius: 10px; width: 100%; text-align: left;
        }}
        div.stButton > button:hover {{
            border-color: #3b82f6 !important;
            color: #3b82f6 !important;
            background-color: rgba(59, 130, 246, 0.08) !important;
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
            max-width: 80%; 
            width: fit-content; 
            display: block;    
            font-size: 0.95rem; 
            color: #ffffff;
        }}

        [data-testid="stChatMessage"] {{
            width: fit-content !important;
            max-width: 85% !important;
        }}
        </style>
    """, unsafe_allow_html=True)

# --- 2. CORE ENGINE & STATE ---
def init_store():
    if "chats" not in st.session_state: st.session_state.chats = {}  
    if "active_id" not in st.session_state: st.session_state.active_id = None
    if "ai_mode" not in st.session_state: st.session_state.ai_mode = "LearnAI"

def create_thread():
    cid = str(uuid.uuid4())
    st.session_state.chats[cid] = {
        "title": "New Chat",
        "messages": [],
        "mode": st.session_state.ai_mode,
        "ts": datetime.now().strftime("%H:%M")
    }
    st.session_state.active_id = cid

# --- 3. UI COMPONENTS ---
def render_sidebar():
    with st.sidebar:
        st.markdown("<h2 style='letter-spacing:-1.5px; font-weight:600;'>Nexus <span style='color:#3b82f6;'>AI</span></h2>", unsafe_allow_html=True)
        
        st.markdown('<div style="margin-top:20px;"></div>', unsafe_allow_html=True)
        mode = st.radio(
            "Select Intelligence Engine",
            ["LearnAI", "Study Buddy"],
            help="LearnAI: General topics | Study Buddy: Personalized learning partner"
        )
        st.session_state.ai_mode = mode
        
        st.markdown("---")
        if st.button("＋ New Chat", use_container_width=True):
            create_thread()
            st.rerun()

        st.markdown('<div style="color:#4b5563; font-size:0.7rem; font-weight:700; text-transform:uppercase; margin:20px 0 10px 5px;">History</div>', unsafe_allow_html=True)
        
        find_chat = st.text_input("Find Chat", placeholder="Search Chat...", label_visibility="collapsed")
        
        chat_list = list(reversed(list(st.session_state.chats.items())))
        filtered_chats = [item for item in chat_list if find_chat.lower() in item[1]['title'].lower()]

        if not filtered_chats:
            st.caption("No chat found.")
        else:
            for cid, data in filtered_chats:
                is_active = cid == st.session_state.active_id
                cols = st.columns([0.85, 0.15])
                with cols[0]:
                    label = f"📖 {data['title'][:18]}" if data.get('mode') == "Study Buddy" else f"🧠 {data['title'][:18]}"
                    if st.button(label, key=f"n_{cid}", type="primary" if is_active else "secondary"):
                        st.session_state.active_id = cid
                        st.rerun()
                with cols[1]:
                    if st.button("×", key=f"d_{cid}"):
                        del st.session_state.chats[cid]
                        if st.session_state.active_id == cid: st.session_state.active_id = None
                        st.rerun()

        st.markdown("<div style='margin-top: 30px;'></div>", unsafe_allow_html=True)
        st.markdown("---")
        
        st.markdown("""
            <div style='display: flex; align-items: center; gap: 10px; padding: 5px;'>
                <div style='background: #3b82f6; width: 32px; height: 32px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: bold;'>A</div>
                <div style='overflow: hidden;'>
                    <p style='margin:0; font-size:0.85rem; font-weight:600;'>Alex Architect</p>
                    <p style='margin:0; font-size:0.7rem; color:#6b7280;'>Pro Plan</p>
                </div>
            </div>
            <div style='margin-top: 10px;'></div>
        """, unsafe_allow_html=True)

        if st.button("👤 View Profile", use_container_width=True):
            st.toast("Opening profile settings...", icon="⚙️")
            
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.clear()
            st.rerun()

def render_message(role, text):
    if role == "user":
        st.markdown(f'<div class="user-bubble">{text}</div><div style="clear:both"></div>', unsafe_allow_html=True)
    else:
        icon = "🎓" if st.session_state.ai_mode == "Study Buddy" else "🧠"
        with st.chat_message("assistant", avatar=icon):
            st.markdown(text)

def render_hero_screen():
    st.markdown("<br><br><br><br>", unsafe_allow_html=True)
    _, mid, _ = st.columns([0.2, 0.6, 0.2])
    with mid:
        st.markdown(f'<h1 class="hero-title">{st.session_state.ai_mode}</h1>', unsafe_allow_html=True)
        desc = "Your study buddy for exam prep and deep learning." if st.session_state.ai_mode == "Study Buddy" else "The architectural standard for professional intelligence."
        st.markdown(f'<p class="hero-subtitle">{desc}</p>', unsafe_allow_html=True)
        
        if st.button(f"＋ Start with New {st.session_state.ai_mode} Chat", use_container_width=True):
            create_thread()
            st.rerun()

def render_chat_interface():
    # Header
    st.markdown(f"### {st.session_state.ai_mode} <small style='color:#6b7280; font-size:0.8rem;'>Active Session</small>", unsafe_allow_html=True)
    
    chat = st.session_state.chats[st.session_state.active_id]
    for msg in chat['messages']:
        render_message(msg['role'], msg['content'])

    if prompt := st.chat_input(f"Message {st.session_state.ai_mode}..."):
        chat['messages'].append({"role": "user", "content": prompt})
        if chat['title'] == "New Chat": chat['title'] = prompt[:25] + "..."
        st.rerun()

    if chat['messages'] and chat['messages'][-1]['role'] == "user":
        with st.chat_message("assistant", avatar="🎓" if st.session_state.ai_mode == "Study Buddy" else "✨"):
            ph = st.empty()
            if st.session_state.ai_mode == "Study Buddy":
                res = "I've reviewed your topic. Let's break this down into digestible concepts for your study session. Where should we start?"
            else:
                res = "Optimizing response for high-performance intelligence. The parameters are set for professional depth. How shall we proceed?"
            
            full = ""
            for chunk in res.split():
                full += chunk + " "
                time.sleep(0.03)
                ph.markdown(full + " <span style='color:#3b82f6;'>▌</span>", unsafe_allow_html=True)
            ph.markdown(full)
            chat['messages'].append({"role": "assistant", "content": full})

# --- 4. THE MASTER WRAPPER FUNCTION ---
def render_nexus_app():
    """
    Master function that calls all sub-functions to build the UI.
    This makes the backend ready by separating UI logic from data flow.
    """
    inject_ui_styles()
    init_store()
    render_sidebar()

    if not st.session_state.active_id:
        render_hero_screen()
    else:
        render_chat_interface()

# --- 5. ENTRY POINT ---
def main():
    st.set_page_config(page_title="Nexus AI", layout="wide")
    render_nexus_app()

if __name__ == "__main__":
    main()