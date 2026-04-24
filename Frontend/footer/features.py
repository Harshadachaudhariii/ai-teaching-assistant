import streamlit as st
def render_features():
    st.set_page_config(page_title="Features", layout="wide")

    st.markdown(
    """
    <style>

    /* ================= YOUR RADIAL BACKGROUND (UNCHANGED) ================= */

    .stApp {
        position: relative;
        overflow: hidden;
    }

    /* Center glow */
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

    /* Floating blob */
    .stApp::after {
        content: "";
        position: fixed;
        top: -100px;
        left: -100px;
        width: 400px;
        height: 400px;
        background: radial-gradient(circle,
            rgba(168,85,247,0.25),
            transparent 70%
        );
        filter: blur(120px);
        z-index: 0;
        pointer-events: none;
    }

    /* Bottom blob */
    .floating-blob {
        position: fixed;
        bottom: -120px;
        right: -120px;
        width: 500px;
        height: 500px;
        background: radial-gradient(circle,
            rgba(16,185,129,0.18),
            transparent 70%
        );
        filter: blur(140px);
        z-index: 0;
        pointer-events: none;
    }

    /* ================= FIX: CONTENT MUST BE ABOVE BACKGROUND ================= */

    /* SAFE CONTENT LAYER FIX */
    [data-testid="stAppViewContainer"] {
        position: relative;
        z-index: 10;
    }

    [data-testid="stHeader"] {
        z-index: 10;
    }

    .main {
        position: relative;
        z-index: 10;
    }

    .block-container {
        position: relative;
        z-index: 10;
    }


    /* ================= UI STYLES ================= */

    .main-title {
        text-align: center;
        font-size: 42px;
        font-weight: 700;
        color: #60a5fa;
    }

    .sub-title {
        text-align: center;
        font-size: 18px;
        color: #cbd5e1;
        margin-bottom: 30px;
    }
    .last_box:hover {
        background: rgba(255, 255, 255, 0.08);
        border: 1px solid #3b82f6;
        box-shadow: 0 0 20px rgba(59, 130, 246, 0.35);
        transform: translateY(-3px);
        }
    .feature-box {
        background: rgba(255, 255, 255, 0.05);
        padding: 20px;
        border-radius: 12px;
        border: 1px solid rgba(255, 255, 255, 0.10);
        backdrop-filter: blur(10px);
        transition: all 0.25s ease-in-out;
    }

    /* 🔥 HOVER EFFECT */
    .feature-box:hover {
        background: rgba(255, 255, 255, 0.08);
        border: 1px solid #3b82f6;
        box-shadow: 0 0 20px rgba(59, 130, 246, 0.35);
        transform: translateY(-4px);
    }

    .feature-title {
        font-size: 20px;
        font-weight: 600;
        color: #93c5fd;
    }

    .feature-text {
        font-size: 15px;
        color: #e2e8f0;
        line-height: 1.5;
    }
    header {
        visibility: hidden;
        height: 0px;
    }

    [data-testid="stToolbar"] {
        display: none !important;
    }

    [data-testid="stDecoration"] {
        display: none !important;
    }
    </style>

    <div class="floating-blob"></div>
    """,
    unsafe_allow_html=True
    )

    # ---------------- HEADER ----------------
    st.markdown("<div class='main-title'>AI Teaching Assistant</div>", unsafe_allow_html=True)

    st.markdown(
        "<div class='sub-title'>Your personal AI tutor that learns from your lectures and answers instantly</div>",
        unsafe_allow_html=True
    )

    st.markdown("---")

    # ---------------- FEATURE SECTION ----------------
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <div class="feature-box">
            <div class="feature-title">Ask Anything from Lectures</div>
            <div class="feature-text">
            Stop rewatching long videos. Just ask questions like:
            <br><br>
            • Explain recursion<br>
            • What is binary search?<br>
            • Stack vs Queue<br><br>
            Get direct answers from your lecture content.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="feature-box">
            <div class="feature-title">Smart AI Model Routing</div>
            <div class="feature-text">
            System automatically selects best model:
            <br><br>
            phi3-mini → Fast answers<br>
            llama3 → Deep explanations<br><br>
            No manual selection needed.
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    col3, col4 = st.columns(2)

    with col3:
        st.markdown("""
        <div class="feature-box">
            <div class="feature-title">RAG-Based Learning System</div>
            <div class="feature-text">
            Works only on YOUR data:
            <br><br>
            • Lecture transcripts<br>
            • Course notes<br>
            • Timestamp-based knowledge<br><br>
            No random internet answers.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown("""
        <div class="feature-box">
            <div class="feature-title">High-Speed Engine</div>
            <div class="feature-text">
            Optimized for performance:
            <br><br>
            • Vector search indexing<br>
            • Response caching<br>
            • Fast retrieval pipeline<br><br>
            Answers in seconds.
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # ---------------- BOTTOM SECTION ----------------
    st.markdown("""
    <div style="
        text-align:center;
        padding:20px;
        background: rgba(255,255,255,0.05);
        border-radius:10px;
        border:1px solid rgba(255,255,255,0.1);
        transition: all 0.25s ease-in-out;
    ", class="last_box">
    Built to act like your personal AI tutor — always available, always ready.
    </div>
    """, unsafe_allow_html=True)