import streamlit as st
def render_about():
    st.set_page_config(page_title="About", layout="wide")

    st.markdown("""
    <style>

    /* ================= RADIAL BACKGROUND ================= */

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

    .stApp::after {
        content: "";
        position: fixed;
        top: -120px;
        left: -120px;
        width: 450px;
        height: 450px;
        background: radial-gradient(circle,
            rgba(168,85,247,0.25),
            transparent 70%
        );
        filter: blur(120px);
        z-index: 0;
        pointer-events: none;
    }

    .floating-blob {
        position: fixed;
        bottom: -140px;
        right: -140px;
        width: 520px;
        height: 520px;
        background: radial-gradient(circle,
            rgba(16,185,129,0.18),
            transparent 70%
        );
        filter: blur(140px);
        z-index: 0;
        pointer-events: none;
    }

    /* ================= CONTENT LAYER ================= */

    [data-testid="stAppViewContainer"],
    .main,
    .block-container {
        position: relative;
        z-index: 10;
    }

    /* ================= UI ================= */

    .title {
        text-align: center;
        font-size: 44px;
        font-weight: 700;
        color: #60a5fa;
    }

    .subtitle {
        text-align: center;
        font-size: 16px;
        color: #94a3b8;
        margin-bottom: 30px;
    }

    .card {
        background: rgba(255,255,255,0.05);
        border: 1px solid rgba(255,255,255,0.10);
        backdrop-filter: blur(12px);
        border-radius: 14px;
        padding: 22px;
        transition: 0.25s ease;
    }

    .card:hover {
        transform: translateY(-5px);
        border: 1px solid #3b82f6;
        box-shadow: 0 0 25px rgba(59,130,246,0.35);
    }

    .section-title {
        font-size: 20px;
        font-weight: 600;
        color: #93c5fd;
        margin-bottom: 8px;
    }

    .text {
        font-size: 18px;
        color: #cbd5e1;
        line-height: 1.7;
    }

    .footer {
        margin-top: 50px;
        text-align: center;
        font-size: 13px;
        color: #94a3b8;
        border-top: 1px solid rgba(255,255,255,0.08);
        padding: 20px;
    }

    </style>

    <div class="floating-blob"></div>
    """, unsafe_allow_html=True)

    # ================= HEADER =================
    st.markdown("<div class='title'>About AI Teaching Assistant</div>", unsafe_allow_html=True)
    st.markdown("<div class='subtitle'>A modern AI system that transforms lectures into interactive knowledge</div>", unsafe_allow_html=True)

    st.markdown("---")

    # ================= PROBLEM STATEMENT =================
    st.markdown("""
    <div class="card">
    <div class="section-title">Problem We Solve</div>
    <div class="text">
    Traditional learning systems are slow, fragmented, and heavily dependent on passive consumption, which makes it extremely difficult for students to build deep conceptual understanding in an efficient and structured way.<br><br>
    • Students are forced to repeatedly rewatch long lecture videos just to find small pieces of information, which wastes a significant amount of time and reduces overall learning efficiency.<br>
    • Educational content is usually scattered across multiple sources such as video lectures, handwritten notes, PDFs, and external references, making it difficult to maintain a unified understanding of a topic.<br>
    • Searching for specific concepts within hours of lecture material is highly time-consuming, especially when there is no structured indexing or intelligent retrieval system available.<br>
    • There is no real-time question-answering system that can understand lecture content and provide instant, context-aware explanations based on the actual learning material.<br>
    • Students often struggle with revision because they must manually revisit entire topics instead of quickly accessing precise, relevant explanations of concepts they are unsure about.<br>
    • Most learning platforms do not adapt to the user’s own uploaded content, meaning students cannot interact directly with their personal study material in an intelligent way.<br><br>
    This creates a major gap between passive content consumption and active understanding, leading to slower learning progress, reduced retention, and inefficient revision cycles.
    </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ================= SOLUTION =================
    st.markdown("""
    <div class="card">
    <div class="section-title">Our Solution</div>
    <div class="text">
    AI Teaching Assistant converts your course lectures into a structured, searchable intelligence system that allows users to ask questions and directly navigate to the exact part of the video where the concept is explained.<br><br>
    • The system automatically processes lecture content and extracts meaningful segments along with their associated video references and timestamps without requiring the user to manually structure data.<br>
    • All lecture data is internally converted into semantically meaningful chunks while preserving metadata such as video number and timestamp boundaries for accurate retrieval.<br>
    • When a user asks a question related to the course, the query is semantically matched against stored lecture embeddings using a RAG-based retrieval system.<br>
    • The system identifies the most relevant lecture segment and returns the exact video number along with the precise timestamp where the concept is explained.<br>
    • Along with the retrieved timestamp, a concise explanation is generated using an LLM (phi3-mini for fast responses or llama3 for deeper reasoning).<br>
    • A smart routing layer automatically selects the most suitable model based on query complexity to balance speed and response quality.<br>
    • The final response is delivered as a structured learning output: video reference + timestamp + short explanation, allowing users to jump directly to the exact learning moment instead of searching manually.<br>

    This transforms passive lecture watching into an intelligent, time-aware learning experience powered by semantic search and contextual AI understanding.
    </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ================= HOW IT WORKS =================
    st.markdown("""
    <div class="card">
    <div class="section-title">How It Works</div>
    <div class="text">
    The system processes learning content through a lightweight yet effective semantic retrieval pipeline designed specifically for lecture-based question answering.<br><br>
    • Lecture content is automatically processed and divided into meaningful text segments while preserving context and lecture structure.<br>
    • Each segment is converted into vector embeddings that represent its semantic meaning rather than relying on keyword matching.<br>
    • When a user asks a question, the query is also converted into an embedding using the same embedding model for consistency in representation.<br>
    • The system computes similarity between the user query and all stored lecture embeddings using cosine similarity to identify the most relevant content.<br>
    • The top matching segments are selected along with their associated metadata such as video number and timestamp range.<br>
    • A context assembly layer prepares the retrieved segments and forwards them to a large language model (lama3 for deeper reasoning).<br>
    • A smart routing mechanism selects the appropriate model based on query complexity to optimize response quality and latency.<br>
    • The final output combines a concise explanation with exact video reference and timestamp, enabling direct navigation to the relevant part of the lecture.<br><br>
    This approach ensures accurate, context-aware answers without requiring a heavy vector database system, while still maintaining strong semantic retrieval performance.
    </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ================= TECH STACK =================
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <div class="card">
        <div class="section-title">Core Stack</div>
        <div class="text">
        • Streamlit (UI layer)<br>
        • Python (Backend logic)<br>
        • Ollama (Local LLM runtime)<br>
        • Sentence Transformers (Embeddings)<br>
        • Cosine Similarity (Semantic search)
        </div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="card">
        <div class="section-title">AI System</div>
        <div class="text">
        • Semantic Retrieval Pipeline<br>
        • RAG-based response generation<br>
        • Model Router (phi3 / llama3)<br>
        • Context-aware prompting<br>
        • Timestamp-aware lecture mapping
        </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ================= VISION =================
    st.markdown("""
    <div class="card">
    <div class="section-title">Vision</div>
    <div class="text">
    Our goal is to build an intelligent learning assistant that:
    <br><br>
    • Eliminates passive video learning<br>
    • Converts content into interactive knowledge<br>
    • Reduces revision time drastically<br>
    • Personalizes learning experience for every student<br><br>

    This is not just a chatbot — it is a learning system.
    </div>
    </div>
    """, unsafe_allow_html=True)

    # ================= FOOTER =================
    st.markdown("""
    <div class="footer">
    AI Teaching Assistant © 2026 • Built as RAG-based Learning System • Designed for scalable AI education
    </div>
    """, unsafe_allow_html=True)