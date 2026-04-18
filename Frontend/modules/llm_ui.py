# import streamlit as st
# import time
# import uuid
# from datetime import datetime
# import requests

# # --- 1. ARCHITECTURAL DESIGN SYSTEM (CSS) ---
# def inject_ui_styles():
#     st.markdown(f"""
#         <style>
#         @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&display=swap');
#         @import url('https://fonts.googleapis.com/css2?family=Lexend+Deca:wght@300;400;600&display=swap');

#         .stApp {{ background-color: #0a0a0a; color: #f3f4f6; font-family: 'Inter', sans-serif; line-height: 1.6; }}
#         /* This hides the automatic 'Pages' navigation menu in the sidebar */
#         [data-testid="stSidebarNav"] {{
#             display: none !important;
#         }}
#         /* Typography & Visual Hierarchy */
#         .hero-title {{
#             text-align: center; font-family: 'Lexend Deca', sans-serif;
#             font-size: 4rem; font-weight: 600; letter-spacing: -4px; 
#             background: linear-gradient(to bottom, #ffffff 30%, #6b7280 100%);
#             -webkit-background-clip: text; -webkit-text-fill-color: transparent;
#             margin-bottom: 0px;
#         }}
#         .hero-subtitle {{
#             text-align: center; color: #9ca3af; font-size: 1.1rem; 
#             font-weight: 300; margin-bottom: 40px;
#         }}

#         /* Professional Card Styling for Main View */
#         .glass-card {{
#             background: rgba(255, 255, 255, 0.03);
#             border: 1px solid rgba(255, 255, 255, 0.05);
#             border-radius: 16px;
#             padding: 25px;
#             margin-top: 20px;
#         }}

#         [data-testid="stSidebar"] {{ background-color: #0d0d0d; border-right: 1px solid #1e1e1e; }}

#         /* Button Interaction Feedback */
#         div.stButton > button {{
#             background-color: rgba(255, 255, 255, 0.02) !important;
#             color: #9ca3af !important;
#             border: 1px solid #262626 !important;
#             border-radius: 10px; width: 100%; text-align: left;
#             transition: all 0.2s ease;
#         }}
#         div.stButton > button:hover {{
#             border-color: #3b82f6 !important;
#             color: #3b82f6 !important;
#             background-color: rgba(59, 130, 246, 0.08) !important;
#             transform: translateY(-1px);
#         }}

#         div[data-testid="stRadio"] > label {{
#             color: #4b5563 !important; font-size: 0.7rem !important;
#             font-weight: 700 !important; text-transform: uppercase;
#         }}

#         .user-bubble {{
#             background: linear-gradient(145deg, #1a1a1a 0%, #0f0f0f 100%);
#             border: 1px solid #2e2e2e; 
#             padding: 12px 18px;
#             border-radius: 20px 20px 4px 20px; 
#             margin: 10px 0 10px auto;
#             max-width: 80%; width: fit-content; display: block; font-size: 0.95rem; color: #ffffff;
#         }}

#         [data-testid="stChatMessage"] {{
#             width: fit-content !important;
#             max-width: 85% !important;
#             border-radius: 12px;
#         }}
#         </style>
#     """, unsafe_allow_html=True)

# # --- 2. CORE ENGINE & STATE ---
# def init_store():
#     if "chats" not in st.session_state: st.session_state.chats = {}  
#     if "active_id" not in st.session_state: st.session_state.active_id = None
#     if "ai_mode" not in st.session_state: st.session_state.ai_mode = "EchoAI"
#     # Add inside init_store()
#     if "echo_speed" not in st.session_state:
#         st.session_state.echo_speed = "default"

# def create_thread():
#     cid = str(uuid.uuid4())
#     st.session_state.chats[cid] = {
#         "title": "New Chat",
#         "messages": [],
#         "mode": st.session_state.ai_mode,
#         "ts": datetime.now().strftime("%H:%M")
#     }
#     st.session_state.active_id = cid

# # --- 3. UI COMPONENTS ---
# def render_sidebar():
#     with st.sidebar:
#         st.markdown("<h2 style='letter-spacing:-1.5px; font-weight:600;'>Nexa<span style='color:#3b82f6;'>AI</span></h2>", unsafe_allow_html=True)
        
#         st.markdown('<div style="margin-top:20px;"></div>', unsafe_allow_html=True)
#         mode = st.radio(
#             "Select Intelligence Engine",
#             ["EchoAI", "AtlasAI"],
#             help="EchoAI: General topics | AtlasAI: Personalized learning partner"
#         )
#         # In render_sidebar() — only show when EchoAI is active
#         if st.session_state.ai_mode == "EchoAI":
#             speed = st.radio(
#                 "Response Speed",
#                 ["Default", "Fast"],
#                 index=0 if st.session_state.echo_speed == "default" else 1
#             )
#             st.session_state.echo_speed = "fast" if speed == "Fast" else "default"
#         if mode != st.session_state.ai_mode:
#             st.session_state.ai_mode = mode
#             create_thread()   # ✅ new chat
#             st.rerun()
        
#         st.markdown("---")
#         if st.button("＋ New Chat", use_container_width=True):
#             create_thread()
#             st.rerun()

#         st.markdown('<div style="color:#4b5563; font-size:0.7rem; font-weight:700; text-transform:uppercase; margin:20px 0 10px 5px;">History</div>', unsafe_allow_html=True)
        
#         find_chat = st.text_input("Find Chat", placeholder="Search Chat...", label_visibility="collapsed")
        
#         chat_list = list(reversed(list(st.session_state.chats.items())))
#         filtered_chats = [item for item in chat_list if find_chat.lower() in item[1]['title'].lower()]

#         if not filtered_chats:
#             st.caption("No chat found.")
#         else:
#             for cid, data in filtered_chats:
#                 is_active = cid == st.session_state.active_id
#                 cols = st.columns([0.85, 0.15])
#                 with cols[0]:
#                     label = f"📖 {data['title'][:18]}" if data.get('mode') == "AtlasAI" else f"{data['title'][:18]}"
#                     if st.button(label, key=f"n_{cid}", type="primary" if is_active else "secondary"):
#                         st.session_state.active_id = cid
#                         st.rerun()
#                 with cols[1]:
#                     if st.button("×", key=f"d_{cid}"):
#                         del st.session_state.chats[cid]
#                         if st.session_state.active_id == cid: st.session_state.active_id = None
#                         st.rerun()

#         st.markdown("<div style='margin-top: 30px;'></div>", unsafe_allow_html=True)
#         st.markdown("---")
        
#         st.markdown("""
#             <div style='display: flex; align-items: center; gap: 10px; padding: 5px;'>
#                 <div style='background: #3b82f6; width: 32px; height: 32px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: bold;'>A</div>
#                 <div style='overflow: hidden;'>
#                     <p style='margin:0; font-size:0.85rem; font-weight:600;'>Alex Architect</p>
#                     <p style='margin:0; font-size:0.7rem; color:#6b7280;'>Pro Plan</p>
#                 </div>
#             </div>
#             <div style='margin-top: 10px;'></div>
#         """, unsafe_allow_html=True)

#         if st.button("👤 View Profile", use_container_width=True):
#             st.session_state.page = "profile"  # Tell app.py to switch to the profile view
#             st.rerun()                        # Refresh to trigger the change
            
#         if st.button("🚪 Logout", use_container_width=True):
#             st.session_state.clear()
#             st.session_state.page = "login"   # Reset to login page
#             st.rerun()

# def render_message(role, text):
#     if role == "user":
#         st.markdown(f'<div class="user-bubble">{text}</div><div style="clear:both"></div>', unsafe_allow_html=True)
#     else:
#         icon = "🎓" if st.session_state.ai_mode == "AtlasAI" else "🧠"
#         with st.chat_message("assistant", avatar=icon):
#             st.markdown(text)

# def render_hero_screen():
#     st.markdown("<br><br><br>", unsafe_allow_html=True)
#     _, mid, _ = st.columns([0.15, 0.7, 0.15])
#     with mid:
#         # Hierarchy: Large Title -> Subtle Subtitle
#         st.markdown(f'<h1 class="hero-title">{st.session_state.ai_mode}</h1>', unsafe_allow_html=True)
#         desc = "Your personalized learning partner for exam prep and research." if st.session_state.ai_mode == "AtlasAI" else "The industrial standard for deep logic and professional intelligence."
#         st.markdown(f'<p class="hero-subtitle">{desc}</p>', unsafe_allow_html=True)
        
#         # Primary Action
#         if st.button(f"Start New {st.session_state.ai_mode} Session", use_container_width=True, type="primary"):
#             create_thread()
#             st.rerun()

#         # 1. & 2. GUIDED INTERACTION (Fill empty space)
#         st.markdown('<div class="glass-card">', unsafe_allow_html=True)
#         st.markdown("<p style='font-size:0.8rem; color:#6b7280; font-weight:600; text-transform:uppercase; margin-bottom:15px;'>Suggested Prompts</p>", unsafe_allow_html=True)
        
#         c1, c2 = st.columns(2)
#         prompts = [
#             ["Explain Quantum Computing", "Summarize this chapter"],
#             ["Debug my Python logic", "Generate a mock quiz"]
#         ]
        
#         idx = 0 if st.session_state.ai_mode == "EchoAI" else 1
#         with c1:
#             if st.button(prompts[idx][0]):
#                 create_thread()
#                 st.session_state.chats[st.session_state.active_id]["messages"].append({"role": "user", "content": prompts[idx][0]})
#                 st.rerun()
#         with c2:
#             if st.button(prompts[idx][1]):
#                 create_thread()
#                 st.session_state.chats[st.session_state.active_id]["messages"].append({"role": "user", "content": prompts[idx][1]})
#                 st.rerun()
#         st.markdown('</div>', unsafe_allow_html=True)

#         # 2. Preview interaction block
#         with st.expander("See a preview of the response style"):
#             st.markdown("""
#             **User:** *How do I optimize a SQL query?* **EchoAI:** To optimize a SQL query, start by analyzing the Execution Plan. 
#             Ensure your columns are indexed, avoid `SELECT *`, and use `JOIN` instead of subqueries where possible.
#             """)

# def render_chat_interface():
#     # 3. Improved Header Section
#     st.markdown(f"""
#         <div style='display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #1e1e1e; padding-bottom: 10px; margin-bottom: 20px;'>
#             <h3 style='margin:0;'>{st.session_state.ai_mode}</h3>
#             <span style='background: #111; color: #3b82f6; font-size: 0.75rem; padding: 4px 12px; border-radius: 20px; border: 1px solid #3b82f6;'>Online</span>
#         </div>
#     """, unsafe_allow_html=True)
    
#     chat = st.session_state.chats[st.session_state.active_id]
    
#     # 3. Chat Empty State
#     if not chat['messages']:
#         st.markdown("<br><br>", unsafe_allow_html=True)
#         st.info(f"**Welcome to your new {st.session_state.ai_mode} session.** Type your first message below or choose a starter.")
#         if st.button("✨ What are we working on today?"):
#              chat['messages'].append({"role": "user", "content": "What can you help me with in this mode?"})
#              st.rerun()

#     for msg in chat['messages']:
#         render_message(msg['role'], msg['content'])

#     if prompt := st.chat_input(f"Message {st.session_state.ai_mode}..."):
#         chat['messages'].append({"role": "user", "content": prompt})
#         if chat['title'] == "New Chat": chat['title'] = prompt[:25] + "..."
#         st.rerun()

#     if chat['messages'] and chat['messages'][-1]['role'] == "user":
#         with st.chat_message("assistant", avatar="🎓" if st.session_state.ai_mode == "AtlasAI" else "✨"):
#             ph = st.empty()
#             ph.markdown("⏳ Thinking...")

#             try:
#                 token = st.session_state.get("token")
#                 headers = {"Authorization": f"Bearer {token}"}

#                 if st.session_state.ai_mode == "AtlasAI":
#                     # ← RAG call
#                     api_res = requests.post(
#                         "http://localhost:8000/rag/",
#                         json={"query": chat['messages'][-1]['content']},
#                         headers=headers,
#                         timeout=60
#                     )
#                 else:
#                     # ← EchoAI call
#                     api_res = requests.post(
#                         "http://localhost:8000/chat/",
#                         json={
#                             "messages": chat['messages'],
#                             "speed": st.session_state.echo_speed
#                         },
#                         headers=headers,
#                         timeout=60
#                     )

#                 if api_res.status_code == 200:
#                     full = api_res.json().get("response", "No response")
#                 else:
#                     full = f"Error: {api_res.json().get('detail', 'Something went wrong')}"

#             except requests.exceptions.Timeout:
#                 full = "Request timed out. Please try again."
#             except Exception as e:
#                 full = f"Error: {str(e)}"

#             # Streaming effect
#             display = ""
#             for chunk in full.split():
#                 display += chunk + " "
#                 time.sleep(0.03)
#                 ph.markdown(display + " <span style='color:#3b82f6;'>▌</span>", unsafe_allow_html=True)
#             ph.markdown(display)
#             chat['messages'].append({"role": "assistant", "content": display})

# # --- 4. THE MASTER WRAPPER FUNCTION ---
# def render_nexus_app():
#     inject_ui_styles()
#     init_store()
#     render_sidebar()

#     if not st.session_state.active_id:
#         render_hero_screen()
#     else:
#         render_chat_interface()

# # --- 5. ENTRY POINT ---
# def main():
#     st.set_page_config(page_title="Nexus AI", layout="wide")
#     render_nexus_app()

# if __name__ == "__main__":
#     main()

# modules/llm_ui.py

import streamlit as st
import time
import uuid
from datetime import datetime
import requests

# --- 1. ARCHITECTURAL DESIGN SYSTEM (CSS) ---
def inject_ui_styles():
    st.markdown(f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&display=swap');
        @import url('https://fonts.googleapis.com/css2?family=Lexend+Deca:wght@300;400;600&display=swap');

        .stApp {{ background-color: #0a0a0a; color: #f3f4f6; font-family: 'Inter', sans-serif; line-height: 1.6; }}
        [data-testid="stSidebarNav"] {{ display: none !important; }}

        .hero-title {{
            text-align: center; font-family: 'Lexend Deca', sans-serif;
            font-size: 4rem; font-weight: 600; letter-spacing: -4px; 
            background: linear-gradient(to bottom, #ffffff 30%, #6b7280 100%);
            -webkit-background-clip: text; -webkit-text-fill-color: transparent;
            margin-bottom: 0px;
        }}
        .hero-subtitle {{
            text-align: center; color: #9ca3af; font-size: 1.1rem; 
            font-weight: 300; margin-bottom: 40px;
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
        </style>
    """, unsafe_allow_html=True)

# --- 2. CORE ENGINE & STATE ---
def init_store():
    if "chats" not in st.session_state: st.session_state.chats = {}
    if "active_id" not in st.session_state: st.session_state.active_id = None
    if "ai_mode" not in st.session_state: st.session_state.ai_mode = "EchoAI"
    if "echo_speed" not in st.session_state: st.session_state.echo_speed = "default"

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
        st.markdown("<h2 style='letter-spacing:-1.5px; font-weight:600;'>Nexa<span style='color:#3b82f6;'>AI</span></h2>", unsafe_allow_html=True)

        st.markdown('<div style="margin-top:20px;"></div>', unsafe_allow_html=True)
        mode = st.radio(
            "Choose Assistant",
            ["EchoAI", "AtlasAI"],
            help="EchoAI: General topics | AtlasAI: Personalized learning partner"
        )

        if st.session_state.ai_mode == "EchoAI":
            speed = st.radio(
                "Response Speed",
                ["Default", "Fast"],
                index=0 if st.session_state.echo_speed == "default" else 1
            )
            st.session_state.echo_speed = "fast" if speed == "Fast" else "default"

        if mode != st.session_state.ai_mode:
            st.session_state.ai_mode = mode
            create_thread()
            st.rerun()

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
                    label = f"📖 {data['title'][:18]}" if data.get('mode') == "AtlasAI" else f"{data['title'][:18]}"
                    if st.button(label, key=f"n_{cid}", type="primary" if is_active else "secondary"):
                        st.session_state.active_id = cid
                        st.rerun()
                with cols[1]:
                    if st.button("×", key=f"d_{cid}"):
                        del st.session_state.chats[cid]
                        if st.session_state.active_id == cid:
                            st.session_state.active_id = None
                        st.rerun()

        st.markdown("<div style='margin-top: 30px;'></div>", unsafe_allow_html=True)
        st.markdown("---")

        # ✅ Fix — dynamic username from session state
        user_name = st.session_state.get("profile_data", {}).get("name", "User")
        user_initial = user_name[0].upper() if user_name else "U"

        st.markdown(f"""
            <div style='display: flex; align-items: center; gap: 10px; padding: 5px;'>
                <div style='background: #3b82f6; width: 32px; height: 32px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: bold;'>{user_initial}</div>
                <div style='overflow: hidden;'>
                    <p style='margin:0; font-size:0.85rem; font-weight:600;'>{user_name}</p>
                </div>
            </div>
            <div style='margin-top: 10px;'></div>
        """, unsafe_allow_html=True)

        if st.button("👤 View Profile", use_container_width=True):
            st.session_state.page = "profile"
            st.rerun()

        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.clear()
            st.session_state.page = "login"
            st.rerun()

def render_message(role, text):
    if role == "user":
        st.markdown(f'<div class="user-bubble">{text}</div><div style="clear:both"></div>', unsafe_allow_html=True)
    else:
        icon = "🎓" if st.session_state.ai_mode == "AtlasAI" else "🧠"
        with st.chat_message("assistant", avatar=icon):
            st.markdown(text)

def render_hero_screen():
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    _, mid, _ = st.columns([0.15, 0.7, 0.15])
    with mid:
        st.markdown(f'<h1 class="hero-title">{st.session_state.ai_mode}</h1>', unsafe_allow_html=True)
        desc = "Your personalized learning partner for exam prep and research." if st.session_state.ai_mode == "AtlasAI" else "The industrial standard for deep logic and professional intelligence."
        st.markdown(f'<p class="hero-subtitle">{desc}</p>', unsafe_allow_html=True)

        if st.button(f"Start New {st.session_state.ai_mode} Session", use_container_width=True, type="primary"):
            create_thread()
            st.rerun()

        # st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        # st.markdown("<p style='font-size:0.8rem; color:#6b7280; font-weight:600; text-transform:uppercase; margin-bottom:15px;'>Suggested Prompts</p>", unsafe_allow_html=True)

        c1, c2 = st.columns(2)
        prompts = [
            ["Fix my Python error", " Write a SQL query"],
            ["Debug my Python logic", "Generate a mock quiz"]
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
            st.markdown("""
            **User:** *How do I optimize a SQL query?* **EchoAI:** To optimize a SQL query, start by analyzing the Execution Plan. 
            Ensure your columns are indexed, avoid `SELECT *`, and use `JOIN` instead of subqueries where possible.
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
        if st.button("✨ What are we working on today?"):
            chat['messages'].append({"role": "user", "content": "What can you help me with in this mode?"})
            st.rerun()

    for msg in chat['messages']:
        render_message(msg['role'], msg['content'])

    if prompt := st.chat_input(f"Message {st.session_state.ai_mode}..."):
        chat['messages'].append({"role": "user", "content": prompt})
        if chat['title'] == "New Chat":
            chat['title'] = prompt[:25] + "..."
        st.rerun()

    if chat['messages'] and chat['messages'][-1]['role'] == "user":
        with st.chat_message("assistant", avatar="🎓" if st.session_state.ai_mode == "AtlasAI" else "✨"):
            ph = st.empty()
            ph.markdown("⏳ Thinking...")

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
                        timeout=60
                    )

                if api_res.status_code == 200:
                    full = api_res.json().get("response", "No response")
                else:
                    full = f"Error: {api_res.json().get('detail', 'Something went wrong')}"

            except requests.exceptions.Timeout:
                full = "Request timed out. Please try again."
            except Exception as e:
                full = f"Error: {str(e)}"

            # Streaming effect
            display = ""
            for chunk in full.split():
                display += chunk + " "
                time.sleep(0.03)
                ph.markdown(display + " <span style='color:#3b82f6;'>▌</span>", unsafe_allow_html=True)
            ph.markdown(display)
            chat['messages'].append({"role": "assistant", "content": display})

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
    st.set_page_config(page_title="Nexus AI", layout="wide")
    render_nexus_app()

if __name__ == "__main__":
    main()