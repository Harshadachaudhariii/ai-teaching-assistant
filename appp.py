import streamlit as st
import random
import time
params = st.query_params

# Handle open chat
for key in params:
    if key.startswith("open_"):
        chat = key.replace("open_", "")
        if chat in st.session_state.chats:
            st.session_state.current_chat = chat
            st.session_state.pending_prompt = None

# Handle menu click (dots)
for key in params:
    if key.startswith("menu_"):
        chat = key.replace("menu_", "")
        st.session_state["confirm_delete"] = chat

# Clear params after handling
st.query_params.clear()

st.markdown("""
<style>

/* Remove button styling */
.stButton button {
    background: none !important;
    border: none !important;
    outline: none !important;
    box-shadow: none !important;
    text-align: left;
    padding: 6px;
    width: 100%;
}

/* Chat row */
.chat-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 6px;
    border-radius: 8px;
}

/* Hover background */
.chat-row:hover {
    background-color: #2a2a2a;
}

/* Hide menu by default */
.menu-btn {
    visibility: hidden;
    display: flex;
    align-items: center;
}

/* Show horizontal dots on hover */
.chat-row:hover .menu-btn {
    visibility: visible;
}

/* Style dots button */
.menu-btn button {
    width: auto !important;
    font-size: 18px;
    padding: 2px 6px;
    border: none !important;
    outline: none !important;
    box-shadow: none !important;
    background: transparent !important;
}

/* Popup overlay */
.overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0,0,0,0.6);
    z-index: 999;
}

/* Popup box */
.modal {
    position: fixed;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    background: #1e1e1e;
    padding: 20px;
    border-radius: 10px;
    width: 320px;
    text-align: center;
    z-index: 1000;
}

/* Popup buttons */
.modal-buttons {
    display: flex;
    justify-content: space-between;
    margin-top: 15px;
}

/* Cancel button */
button:has(span:contains("Cancel")) {
    background-color: black !important;
    color: white !important;
}

/* Delete button */
button:has(span:contains("Delete")) {
    background-color: red !important;
    color: white !important;
}

</style>
""", unsafe_allow_html=True)



# Random welcome messages (single line only)
WELCOME_MESSAGES = [
    "What’s on your mind today?",
    "Let’s start learning!",
    "Start with any question you have!",
]
# Title generator
def generate_chat_title(text):
    if len(text.strip()) < 5:
        return "New Chat"
    words = text.strip().split()
    return " ".join(words[:4]).capitalize()  # limit length

# Initialize session
if "chats" not in st.session_state:
    msg = random.choice(WELCOME_MESSAGES)
    st.session_state.chats = {
        "Chat 1": {
            "messages": [],
            "welcome": msg,
            "title": "New Chat"
        }
    }

if "current_chat" not in st.session_state:
    st.session_state.current_chat = "Chat 1"

if "pending_prompt" not in st.session_state:
    st.session_state.pending_prompt = None


# Sidebar
with st.sidebar:
    st.title("AI Assistant")

    if st.button("New Chat"):
        chat_name = f"Chat {len(st.session_state.chats) + 1}"
        msg = random.choice(WELCOME_MESSAGES)

        st.session_state.chats[chat_name] = {
            "messages": [],
            "welcome": msg,
            "title": "New Chat"
        }

        st.session_state.current_chat = chat_name
        st.session_state.pending_prompt = None
        st.rerun()

    st.subheader("Chats")

    for chat in list(st.session_state.chats.keys()):
        chat_title = st.session_state.chats[chat]["title"]

        # Chat row
        st.markdown("<div class='chat-row'>", unsafe_allow_html=True)

        col1, col2 = st.columns([5,1])

        # Title click (WORKING)
        with col1:
            if st.button(chat_title, key=f"open_{chat}"):
                st.session_state.current_chat = chat
                st.session_state.pending_prompt = None
                st.rerun()

        # Dots click (WORKING)
        with col2:
            st.markdown("<div class='menu-btn'>", unsafe_allow_html=True)
            if st.button("⋯", key=f"menu_{chat}"):
                st.session_state["confirm_delete"] = chat
            st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)


        # if st.session_state.get(f"menu_open_{chat}", False):
        #     st.markdown("<div class='delete-btn'>", unsafe_allow_html=True)

        #     if st.button("🗑 Delete", key=f"del_{chat}", help="Delete this chat"):
        #         del st.session_state.chats[chat]

        #         if st.session_state.chats:
        #             st.session_state.current_chat = list(st.session_state.chats.keys())[0]
        #         else:
        #             msg = random.choice(WELCOME_MESSAGES)
        #             st.session_state.chats["Chat 1"] = {
        #                 "messages": [],
        #                 "welcome": msg,
        #                 "title": "New Chat"
        #             }
        #             st.session_state.current_chat = "Chat 1"

        #         st.session_state.pending_prompt = None
        #         st.rerun()

        #     st.markdown("</div>", unsafe_allow_html=True)
    # ---------------- DELETE POPUP ----------------
    if "confirm_delete" in st.session_state:
        chat = st.session_state["confirm_delete"]
        title = st.session_state.chats[chat]["title"]

        st.markdown(f"""
        <div class="overlay"></div>
        <div class="modal">
            <h4>Delete Chat?</h4>
            <p>This will delete "{title}".</p>
        </div>
        """, unsafe_allow_html=True)

        col1, col2, col3 = st.columns([1,2,1])

        with col2:
            c1, c2 = st.columns(2)

            with c1:
                if st.button("Cancel"):
                    del st.session_state["confirm_delete"]
                    st.rerun()

            with c2:
                if st.button("Delete"):
                    del st.session_state.chats[chat]

                    new_chat = f"Chat {len(st.session_state.chats)+1}"
                    msg = random.choice(WELCOME_MESSAGES)

                    st.session_state.chats[new_chat] = {
                        "messages": [],
                        "welcome": msg,
                        "title": "New Chat"
                    }

                    st.session_state.current_chat = new_chat
                    st.session_state.pending_prompt = None

                    del st.session_state["confirm_delete"]
                    st.rerun()


#  Main chat
current = st.session_state.chats[st.session_state.current_chat]
messages = current["messages"]
welcome_msg = current["welcome"]

# Empty state (single line)
if len(messages) == 0:
    st.markdown(f"""
    <div style='text-align: center; margin-top: 120px;'>
        <h2>{welcome_msg}</h2>
    </div>
    """, unsafe_allow_html=True)

# Show messages
for msg in messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Input
prompt = st.chat_input("Ask your question...")

if prompt:
    st.session_state.pending_prompt = prompt

# Dummy response
def response_generator():
    response = random.choice([
        "Hello there! How can I assist you today?",
        "Hi, human! Is there anything I can help you with?",
        "Do you need help?",
    ])
    for word in response.split():
        yield word + " "
        time.sleep(0.03)


# Controlled response
if st.session_state.pending_prompt:

    prompt = st.session_state.pending_prompt
    current_chat = st.session_state.current_chat
    chat_data = st.session_state.chats[current_chat]

    with st.chat_message("user"):
        st.markdown(prompt)

    messages.append({"role": "user", "content": prompt})
    if len(messages) == 1:
        chat_data["title"] = generate_chat_title(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            time.sleep(0.5)  # simulate thinking delay
        response = st.write_stream(response_generator())

    messages.append({"role": "assistant", "content": response})

    st.session_state.pending_prompt = None