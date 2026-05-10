# # modules/llm_ui.py

import streamlit as st
import time
import uuid
from datetime import datetime
import requests
import os
from PIL import Image
from utils.cookies import cookies
import re

BACKEND_URL = "http://localhost:8000"
def _h():
    """Auth headers shorthand."""
    return {"Authorization": f"Bearer {st.session_state.get('token', '')}"}

_FILLER = re.compile(
    r"^\s*("
    r"tell\s+me(\s+about)?|what\s+is|what\s+are|what's|"
    r"explain(\s+me)?|describe|define|"
    r"how\s+(do|does|to|can)|"
    r"can\s+you|could\s+you|please|"
    r"i\s+want\s+to\s+(know|learn)|"
    r"give\s+me|show\s+me|help\s+me(\s+with)?|"
    r"write\s+(me\s+)?a|create\s+(me\s+)?a"
    r")\s+",
    re.IGNORECASE,
)
 
def _smart_title(prompt: str) -> str:
    """
    'tell me about computer networks' → 'Computer Networks'
    'explain how HTTP works'          → 'How HTTP Works'
    'what is a REST API?'             → 'REST API'
    Max 5 words, title-cased, no punctuation.
    """
    text = _FILLER.sub("", prompt.strip())
    if not text:
        text = prompt.strip()
    # Strip punctuation (keep hyphens/apostrophes inside words)
    text = re.sub(r"[^\w\s\-']", "", text)
    words = text.split()
    if not words:
        return prompt[:32]
    # Title-case each word, cap at 5
    title = " ".join(w.capitalize() for w in words[:5])
    return title
 

def _save_chat(cid: str):
    """POST /history/save — upserts full chat after every AI reply."""
    chat = st.session_state.chats.get(cid)
    if not chat:
        return
    try:
        requests.post(
            f"{BACKEND_URL}/history/save",
            json={
                "client_id": cid,
                "title":     chat["title"],
                "mode":      chat["mode"],
                "messages":  chat["messages"],
            },
            headers=_h(), timeout=8,
        )
    except Exception:
        pass   # Local session still works if backend down
 
 
def _rename_api(cid: str, title: str):
    """PATCH /history/{cid}/title — persists renamed title to DB."""
    try:
        requests.patch(
            f"{BACKEND_URL}/history/{cid}/title",
            json={"title": title},
            headers=_h(), timeout=5,
        )
    except Exception:
        pass
 
 
def _delete_api(cid: str):
    """DELETE /history/{cid} — permanently removes chat + messages from DB."""
    try:
        requests.delete(
            f"{BACKEND_URL}/history/{cid}",
            headers=_h(), timeout=5,
        )
    except Exception:
        pass
 
 
def load_chats():
    """
    GET /history/ → rebuild chats dict from DB.
    Called once per session (chats_loaded flag prevents re-fetch).
    Issue 1: always uses fresh DB state — no stale session cache.
    """
    if st.session_state.get("chats_loaded"):
        return
    try:
        res = requests.get(f"{BACKEND_URL}/history/", headers=_h(), timeout=8)
        if res.status_code == 200:
            loaded: dict = {}
            for c in res.json():
                cid = c.get("client_id") or str(uuid.uuid4())
                loaded[cid] = {
                    "title":     c["title"],
                    "messages":  c["messages"],
                    "mode":      c["mode"],
                    "ts":        c.get("created_at", "")[:16].replace("T", " "),
                    # title_set: True means AI or user already set a real title
                    "title_set": bool(c["title"]) and c["title"] != "New Chat",
                }
            st.session_state.chats = loaded
    except Exception:
        pass   # Keep empty dict — user can still create chats
    finally:
        st.session_state.chats_loaded = True   # Don't retry even on error
 
# def _send_cancel():
#     """
#     POST /chat/cancel → backend sets threading.Event → Ollama stream closes.
#     Then resets local generating state.
#     """
#     rid = st.session_state.get("active_request_id")
#     if rid:
#         try:
#             requests.post(
#                 f"{BACKEND_URL}/chat/cancel",
#                 json={"request_id": rid},
#                 headers=_h(), timeout=3,
#             )
#         except Exception:
#             pass   # Even if cancel request fails, local state is reset
#     st.session_state.active_request_id = None
#     st.session_state.is_generating     = False


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
        /*.chat-scroll-area {{
            max-height: calc(100vh - 520px);
            overflow-y: auto;
            overflow-x: hidden;
            padding: 4px 2px;
            border: none !important;
        }}*/

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

        
        
def create_thread():
    cid = str(uuid.uuid4())
    st.session_state.chats[cid] = {
        "title":     "New Chat",
        "messages":  [],
        "mode":      st.session_state.ai_mode,
        "ts":        datetime.now().strftime("%H:%M"),
        "title_set": False,
    }
    st.session_state.active_id = cid

@st.dialog("Rename Chat")
def dlg_rename(cid: str):
    current = st.session_state.chats.get(cid, {}).get("title", "")
    new_t   = st.text_input("New title", value=current, max_chars=50)
    c1, c2  = st.columns(2)
    with c1:
        if st.button("Save", type="primary", use_container_width=True):
            t = new_t.strip()
            if t and t != current:
                # Issue 1: PATCH to DB first, then update local state
                _rename_api(cid, t)
                st.session_state.chats[cid]["title"]     = t
                st.session_state.chats[cid]["title_set"] = True
            st.rerun()
    with c2:
        if st.button("Cancel", use_container_width=True):
            st.rerun()
 
 
@st.dialog("Delete Chat?")
def dlg_delete(cid: str):
    title = st.session_state.chats.get(cid, {}).get("title", "this chat")
    st.markdown(f"Permanently delete **\"{title}\"**?")
    st.caption("This cannot be undone.")
    c1, c2 = st.columns(2)
    with c1:
        if st.button("Delete", type="primary", use_container_width=True):
            # Issue 1: DELETE from DB first
            _delete_api(cid)
            # Remove from local state — will NOT reappear after re-login
            st.session_state.chats.pop(cid, None)
            if st.session_state.active_id == cid:
                st.session_state.active_id = None
            st.rerun()
    with c2:
        if st.button("Cancel", use_container_width=True):
            st.rerun()
            


def render_message(role, text):
    if role == "user":
        st.markdown(f'<div class="user-bubble">{text}</div><div style="clear:both"></div>', unsafe_allow_html=True)
    else:
        #  Use logo image as avatar for both AI modes
        logo_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "logo.png")
        try:
            logo = Image.open(logo_path)
            with st.chat_message("assistant", avatar=logo):
                st.markdown(text)  #  proper markdown rendering
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


# ── REPLACE: guest_popup ────────────────────────────────────────
@st.dialog("Please Login")
def guest_popup():
    st.markdown("Please login to continue")
    c1, c2 = st.columns(2)
    with c1:
        if st.button("Continue with Login", use_container_width=True, type="primary"):
            st.session_state.page = "login"
            st.rerun()
    with c2:
        if st.button("Stay without Login", use_container_width=True):
            # Close popup only — chat remains blocked (no token = no chat)
            st.rerun()


# ── REPLACE: init_store ─────────────────────────────────────────
def init_store():
    _defaults = {
        "chats":             {},
        "active_id":         None,
        "ai_mode":           "AtlasAI",
        "echo_speed":        "default",
        "chats_loaded":      False,
        "is_generating":     False,
        "active_request_id": None,
        # show_guest_popup removed — popup triggered on action, not on load
    }
    for k, v in _defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

    # Load chat history from DB once per session (only when logged in)
    if st.session_state.get("token") and not st.session_state.chats_loaded:
        load_chats()


def render_sidebar():
    # ── Extra CSS for ChatGPT-style chat rows (no border, hover only) ──
    # Injected here so it stays with the sidebar logic, not in inject_ui_styles
    st.markdown("""
        <style>

/* ─────────────────────────────────────────────
   CHAT ROW BUTTON
   ───────────────────────────────────────────── */
[data-testid="stSidebar"] div.stButton > button {

    /* remove default styles */
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;

    /* left alignment */
    /* FORCE REAL LEFT ALIGN */
    display: flex !important;
    justify-content: flex-start !important;
    align-items: center !important;

    text-align: left !important;
    width: 100% !important;

    padding-left: 12px !important;

    flex-direction: row !important;

    /* compact spacing */
    padding: 4px 8px !important;
    margin: 0 !important;
    min-height: 34px !important;

    /* text */
    color: #d1d5db !important;
    font-size: 0.84rem !important;
    font-weight: 400 !important;

    /* shape */
    border-radius: 7px !important;

    /* remove animation */
    transform: none !important;
    transition: background-color 0.12s ease !important;

    /* flush left */
    width: 100% !important;
    
}
    [data-testid="stSidebar"] div.stButton > button p {
    text-align: left !important;
    width: 100% !important;
    margin: 0 !important;
}

[data-testid="stSidebar"] div.stButton > button div {
    justify-content: flex-start !important;
}

/* ─────────────────────────────────────────────
   HOVER EFFECT
   ───────────────────────────────────────────── */
[data-testid="stSidebar"] div.stButton > button:hover {

    background-color: rgba(255,255,255,0.08) !important;

    border: none !important;
    box-shadow: none !important;
    color: #ffffff !important;
    transform: none !important;
}


/* ─────────────────────────────────────────────
   ACTIVE CHAT
   ───────────────────────────────────────────── */
.active-chat-btn button {

    background-color: rgba(255,255,255,0.10) !important;
    color: #ffffff !important;
    font-weight: 500 !important;
}


/* ─────────────────────────────────────────────
   REMOVE EXTRA GAP BETWEEN CHAT ROWS
   ───────────────────────────────────────────── */
[data-testid="stSidebar"] .element-container {

    margin-bottom: 0px !important;
padding-bottom: 0px !important;
}

/* ─────────────────────────────────────────────
   CHAT LIST AREA
   ───────────────────────────────────────────── */
.chat-scroll-area {

    padding-left: 0 !important;
    margin-left: 0 !important;
}


/* ─────────────────────────────────────────────
   REMOVE EXTRA COLUMN SPACING
   ───────────────────────────────────────────── */
[data-testid="column"] {
    padding-top: 0 !important;
    padding-bottom: 0 !important;
}

/* ─────────────────────────────────────────────
   THREE DOTS BUTTON
   ───────────────────────────────────────────── */
[data-testid="stSidebar"] div[data-testid="stPopover"] > div > button {

    background: transparent !important;
    border: none !important;
    box-shadow: none !important;

    color: #6b7280 !important;

    padding: 2px 4px !important;
    margin: 0 !important;

    min-height: 30px !important;
    width: auto !important;
    min-width: unset !important;

    font-size: 1rem !important;
    line-height: 1 !important;

    writing-mode: horizontal-tb !important;

    transition: background-color 0.12s ease !important;
}


/* ─────────────────────────────────────────────
   THREE DOTS HOVER
   ───────────────────────────────────────────── */
[data-testid="stSidebar"] div[data-testid="stPopover"] > div > button:hover {

    background-color: rgba(255,255,255,0.08) !important;
    color: #ffffff !important;

    border: none !important;
    box-shadow: none !important;
}


/* ─────────────────────────────────────────────
   REMOVE DEFAULT STREAMLIT BUTTON SPACING
   ───────────────────────────────────────────── */
[data-testid="stSidebar"] .stButton {

    margin: 0 !important;
    padding: 0 !important;
}

/* CHAT BUTTON TIGHT */
[data-testid="stSidebar"] .stButton {
    margin: 0 !important;
    padding: 0 !important;
    line-height: 1 !important;
}

/* BUTTON HEIGHT */
[data-testid="stSidebar"] div.stButton > button {
    min-height: 35px !important;
    height: 35px !important;
    margin: 0 !important;
}
    /* ─────────────────────────────────────────────
   EXPANDER CLEANUP
   ───────────────────────────────────────────── */

[data-testid="stExpander"],
details {
    border: none !important;
    box-shadow: none !important;
}

/* remove arrow */
summary {
    list-style: none !important;
    display: flex !important;
    padding: 0 !important;
}

summary svg {
    display: none !important;
}

/* remove spacing inside expander */
[data-testid="stExpanderDetails"] [data-testid="stVerticalBlock"] {
    gap: 0px !important;
}

/* make each chat row tight */
[data-testid="stHorizontalBlock"] {
    gap: 0px !important;
    align-items: left !important;
    margin-bottom: 2px !important;
}

/* remove button extra spacing */
[data-testid="stExpander"] .stButton {
    margin: 0 !important;
    padding: 0 !important;
}

/* compact button height */
[data-testid="stExpander"] div.stButton > button {
    min-height: 34px !important;
    height: 34px !important;
    padding-top: 0 !important;
    padding-bottom: 0 !important;
}
/* REMOVE EXPANDER BOTTOM LINE */
[data-testid="stExpander"] {
    border: none !important;
    box-shadow: none !important;
    background: transparent !important;
}

[data-testid="stExpander"] details {
    border: none !important;
}

[data-testid="stExpander"] summary {
    border: none !important;
}

[data-testid="stExpanderDetails"] {
    border: none !important;
}
</style>
    """, unsafe_allow_html=True)
 
    with st.sidebar:
 
        # -------- LOGO --------
        st.markdown("<h2 style='letter-spacing:-1.5px; font-weight:600;'>NexaAI</h2>",
                    unsafe_allow_html=True)
        st.markdown('<div style="margin-top:20px;"></div>', unsafe_allow_html=True)
 
        # -------- AI MODE --------
        mode = st.radio(
            "Choose Assistant",
            ["AtlasAI", "EchoAI"],
            horizontal=True,
            help="AtlasAI: Video-based learning | EchoAI: Quick answers"
        )
        if mode != st.session_state.ai_mode:
            st.session_state.ai_mode   = mode
            st.session_state.active_id = None
            st.rerun()
 
        if st.session_state.ai_mode == "EchoAI":
            speed = st.radio(
                "Response Speed",
                ["Default", "Fast", "Smart"],
                index={"default": 0, "fast": 1, "smart": 2}.get(
                    st.session_state.echo_speed, 0),
                horizontal=True,
            )
            st.session_state.echo_speed = {
                "Default": "default", "Fast": "fast", "Smart": "smart"
            }[speed]
 
        # -------- NEW CHAT --------
        st.markdown("---")
        if st.button("＋ New Chat", use_container_width=True):
            if not st.session_state.get("token"):
                guest_popup()   # blocked — popup only
            else:
                create_thread()
                st.rerun()
 
 
        # -------- SEARCH --------
        find_chat = st.text_input(
            "Find Chat", placeholder="Search Chat...", label_visibility="collapsed"
        )
        # -------- HISTORY LABEL --------
        st.markdown(
    f'<div style="color:#4b5563; font-size:0.7rem; font-weight:700;'
    f' text-transform:uppercase; margin:12px 0 6px 5px;">'
    f'{st.session_state.ai_mode} Chats</div>',
    unsafe_allow_html=True
)
        chat_list = list(reversed(list(st.session_state.chats.items())))

        filtered = [
            (cid, d)
            for cid, d in chat_list
            if (
                find_chat.lower() in d["title"].lower()
                and d.get("mode") == st.session_state.ai_mode
            )
        ]

 
        # -------- SCROLLABLE AREA --------
        st.markdown('<div class="chat-scroll-area">', unsafe_allow_html=True)

        # -------- CURRENT MODE CHATS --------
        with st.expander(f"{st.session_state.ai_mode} Chats", expanded=True):

            if not filtered:
                st.caption(f"No {st.session_state.ai_mode} chats")

            for cid, data in filtered:

                is_active = cid == st.session_state.active_id

                if is_active:
                    st.markdown('<div class="active-chat-btn">', unsafe_allow_html=True)

                cols = st.columns([0.82, 0.18], gap="small")

                with cols[0]:
                    if st.button(
                        data["title"][:22],
                        key=f"chat_{cid}",
                        use_container_width=True,
                    ):
                        st.session_state.active_id = cid
                        st.rerun()

                with cols[1]:
                    with st.popover("⋯"):

                        if st.button(
                            "Rename",
                            key=f"ren_{cid}",
                            use_container_width=True
                        ):
                            dlg_rename(cid)

                        if st.button(
                            "Delete",
                            key=f"del_{cid}",
                            use_container_width=True
                        ):
                            dlg_delete(cid)

                if is_active:
                    st.markdown("</div>", unsafe_allow_html=True)
 
        # -------- BOTTOM SECTION --------
        st.markdown('<div class="sidebar-bottom-section">', unsafe_allow_html=True)
 
        if st.session_state.get("token"):
            user_name = st.session_state.get("profile_data", {}).get("name", "")
            if user_name:
                initial = user_name[0].upper()
                st.markdown(f"""
                    <div style='display:flex; align-items:center; gap:10px; padding:6px 5px;'>
                        <div style='background:#3b82f6; width:30px; height:30px; border-radius:50%;
                             display:flex; align-items:center; justify-content:center;
                             font-weight:bold; font-size:0.8rem; flex-shrink:0;'>{initial}</div>
                        <p style='margin:0; font-size:0.83rem; font-weight:600;
                                  color:#e5e7eb; white-space:nowrap; overflow:hidden;
                                  text-overflow:ellipsis;'>{user_name}</p>
                    </div>
                """, unsafe_allow_html=True)
 
            if st.button("Logout", use_container_width=True):

                # Remove saved cookie token
                cookies["token"] = ""
                cookies.save()

                # Clear session
                for k in list(st.session_state.keys()):
                    del st.session_state[k]

                st.session_state.page = "login"
                st.rerun()
        else:
            # Not logged in — show login button in sidebar
            if st.button("Login / Sign up", type="primary",
                         use_container_width=True):
                st.session_state.page = "login"
                st.rerun()
 
        st.markdown("</div>", unsafe_allow_html=True)

# ── REPLACE: render_chat_interface ──────────────────────────────
def render_chat_interface():
    chat = st.session_state.chats[st.session_state.active_id]
    cid  = st.session_state.active_id
    st.caption("NexaAI can make mistakes. Check important info.")
    for msg in chat["messages"]:
        render_message(msg["role"], msg["content"])

    # ── Chat input — blocked for guests ──
    prompt = st.chat_input(f"Message {st.session_state.ai_mode}...")

    if prompt:
        if not st.session_state.get("token"):
            guest_popup()     # show dialog; chat remains blocked after dismiss
            st.stop()

        chat["messages"].append({"role": "user", "content": prompt})

        # ── Issue 4: local smart title — no API call ──
        if not chat.get("title_set"):
            chat["title"]     = _smart_title(prompt)
            chat["title_set"] = True

        st.rerun()
        
    # ── Generate AI response ──
    if chat["messages"] and chat["messages"][-1]["role"] == "user":
        logo_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)), "assets", "logo.png"
        )
        try:
            avatar = Image.open(logo_path)
        except Exception:
            avatar = None

        with st.chat_message("assistant", avatar=avatar):
            ph = st.empty()
            ph.markdown("Thinking...")

            full = ""   # ALWAYS initialize

            try:
                token = st.session_state.get("token")
                headers = {"Authorization": f"Bearer {token}"}

                # ─────────────────────────────
                # AtlasAI (NON-STREAM)
                # ─────────────────────────────
                if st.session_state.ai_mode == "AtlasAI":
                    api_res = requests.post(
                        f"{BACKEND_URL}/rag/",
                        json={"query": chat["messages"][-1]["content"]},
                        headers=headers,
                        timeout=60,
                    )

                    if api_res.status_code == 200:
                        full = api_res.json().get("response", "")
                    else:
                        full = f"Error: {api_res.text}"

                # ─────────────────────────────
                # EchoAI (STREAM)
                # ─────────────────────────────
                else:
                    if st.session_state.echo_speed not in ["default", "fast", "smart"]:
                        st.session_state.echo_speed = "default"
                    stream_res = requests.post(
                        f"{BACKEND_URL}/chat/stream",
                        json={
                            "messages": chat["messages"],
                            "speed": st.session_state.echo_speed,
                            "request_id": str(uuid.uuid4())
                        },
                        headers=headers,
                        stream=True,
                        timeout=300,
                    )

                    try:
                        for line in stream_res.iter_lines():
                            if not line:
                                continue

                            decoded = line.decode("utf-8")

                            if decoded.startswith("data: "):
                                token = decoded.replace("data: ", "")

                                if token == "[DONE]":
                                    break

                                if token.startswith("__rid__"):
                                    continue

                                full += token
                                ph.markdown(full + "▌")

                    finally:
                        stream_res.close()   # IMPORTANT CLEANUP

            except requests.exceptions.Timeout:
                full = "Request timed out. Please try again."
            except Exception as e:
                full = f"Error: {str(e)}"

            # final render
            ph.markdown(full)

            chat["messages"].append({
                "role": "assistant",
                "content": full
            })

            _save_chat(cid)



# ── REPLACE: render_nexus_app ───────────────────────────────────
def render_nexus_app():
    inject_ui_styles()
    init_store()
    render_sidebar()

    # No token → show hero/chat UI but chat is gated by guest_popup
    # (sidebar + hero visible to everyone, input blocked without login)
    if not st.session_state.active_id:
        render_hero_screen()
    else:
        render_chat_interface()
        
