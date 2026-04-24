import streamlit as st
def render_terms():
    st.set_page_config(page_title="Terms & Conditions", layout="wide")

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

    .title {
        text-align: center;
        font-size: 42px;
        font-weight: 700;
        color: #60a5fa;
    }

    .text {
        color: #cbd5e1;
        font-size: 14px;
        line-height: 1.8;
    }

    .section {
        margin-top: 20px;
        padding: 20px;
        background: rgba(255,255,255,0.05);
        border-radius: 12px;
        border: 1px solid rgba(255,255,255,0.08);
        backdrop-filter: blur(10px);
    }

    h4 {
        color: #93c5fd;
    }

    </style>
    """, unsafe_allow_html=True)

    # ================= HEADER =================
    st.markdown("<div class='title'>Terms & Conditions</div>", unsafe_allow_html=True)

    st.markdown("---")

    # ================= CONTENT =================

    st.markdown("""
    <div class="section">
    <h4>1. Service Usage</h4>
    <div class="text">
    AI Teaching Assistant is provided as an educational AI-powered learning system. By using this platform, users agree to use the service only for personal learning and educational purposes. Any misuse, reverse engineering, or unauthorized access attempts are strictly prohibited.
    </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="section">
    <h4>2. AI Limitations</h4>
    <div class="text">
    The system generates responses based on retrieval-augmented generation (RAG) and semantic similarity from uploaded lecture content. While efforts are made to ensure accuracy, the system may occasionally produce incomplete or approximate explanations. Users should not treat outputs as absolute factual authority.
    </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="section">
    <h4>3. Data Responsibility</h4>
    <div class="text">
    Users are responsible for the content they upload into the system. The platform processes uploaded lecture data only for generating responses and does not guarantee external validation of content accuracy.
    </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="section">
    <h4>4. Fair Usage Policy</h4>
    <div class="text">
    To ensure system stability and equal access, usage limits are applied based on subscription plans. Excessive or automated querying that affects system performance may result in temporary restrictions.
    </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="section">
    <h4>5. System Availability</h4>
    <div class="text">
    The platform aims to maintain high availability but does not guarantee uninterrupted access. Maintenance, updates, or system overload may temporarily affect service performance.
    </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="section">
    <h4>6. Modifications</h4>
    <div class="text">
    The terms of service may be updated periodically to reflect system improvements, policy changes, or feature enhancements. Continued use of the system implies acceptance of updated terms.
    </div>
    </div>
    """, unsafe_allow_html=True)