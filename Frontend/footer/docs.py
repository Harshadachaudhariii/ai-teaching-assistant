import streamlit as st
def render_docs():
    st.set_page_config(page_title="Docs", layout="wide")

    # ================= RADIAL BACKGROUND =================
    st.markdown("""
    <style>

    .stApp {
        position: relative;
        overflow: hidden;
    }

    .stApp::before {
        content: "";
        position: fixed;
        top: 50%;
        left: 50%;
        width: 900px;
        height: 900px;
        transform: translate(-50%, -50%);
        background: radial-gradient(circle,
            rgba(59,130,246,0.20) 0%,
            rgba(59,130,246,0.10) 25%,
            transparent 70%
        );
        filter: blur(90px);
        z-index: 0;
        pointer-events: none;
    }

    [data-testid="stAppViewContainer"],
    .main,
    .block-container {
        position: relative;
        z-index: 10;
    }

    /* text styling */
    .title {
        font-size: 38px;
        font-weight: 700;
        color: #60a5fa;
    }

    .subtitle {
        font-size: 14px;
        color: #94a3b8;
        margin-bottom: 20px;
    }

    .content {
        color: #cbd5e1;
        font-size: 14px;
        line-height: 1.8;
    }

    </style>
    """, unsafe_allow_html=True)

    # ================= HEADER =================
    st.markdown("<div class='title'>Documentation</div>", unsafe_allow_html=True)
    st.markdown("<div class='subtitle'>System design and architecture overview</div>", unsafe_allow_html=True)

    # ================= SIDEBAR NAV =================
    menu = st.sidebar.radio(
        "📘 Docs Sections",
        [
            "Overview",
            "Data Processing",
            "Query Flow",
            "AI Response System",
            "Design Decisions"
        ]
    )

    # ================= SECTION 1 =================
    if menu == "Overview":
        st.markdown("""
        <div class='content'>
        AI Teaching Assistant is a lecture-aware retrieval system that enables users to ask questions from their course content and receive answers with exact video references and timestamps.<br><br>

        The system is designed to eliminate manual searching in long lectures by enabling semantic understanding of educational content.
        </div>
        """, unsafe_allow_html=True)

    # ================= SECTION 2 =================
    elif menu == "Data Processing":
        st.markdown("""
        <div class='content'>
        • Lecture content is split into meaningful semantic segments<br>
        • Each segment is converted into embeddings using Sentence Transformers<br>
        • Embeddings capture meaning instead of keywords<br>
        • Stored in memory-based structure for fast retrieval<br><br>

        This ensures efficient semantic understanding of lecture content.
        </div>
        """, unsafe_allow_html=True)

    # ================= SECTION 3 =================
    elif menu == "Query Flow":
        st.markdown("""
        <div class='content'>
        • User enters a natural language question<br>
        • Query is converted into embedding<br>
        • Cosine similarity is computed against stored embeddings<br>
        • Top matching lecture segments are retrieved<br>
        • Video number + timestamp is extracted for navigation<br><br>

        This enables direct mapping from question → exact lecture moment.
        </div>
        """, unsafe_allow_html=True)

    # ================= SECTION 4 =================
    elif menu == "AI Response System":
        st.markdown("""
        <div class='content'>
        • Retrieved context is sent to LLM<br>
        • phi3-mini → fast responses<br>
        • llama3 → deep reasoning answers<br>
        • Model router selects best model automatically<br>
        • Output = Explanation + Timestamp + Video reference<br><br>

        Ensures accurate and context-grounded responses.
        </div>
        """, unsafe_allow_html=True)

    # ================= SECTION 5 =================
    elif menu == "Design Decisions":
        st.markdown("""
        <div class='content'>
        • No external vector database used<br>
        • Cosine similarity for semantic search<br>
        • Timestamp-based retrieval system<br>
        • Lightweight architecture for speed<br>
        • Lecture-grounded responses only (no hallucination)<br><br>

        Focus is on simplicity, accuracy, and performance.
        </div>
        """, unsafe_allow_html=True)