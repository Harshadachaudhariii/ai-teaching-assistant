# NexaAI: AI Teaching Assistant

![Python](https://img.shields.io/badge/Python-3.11-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-green)
![Streamlit](https://img.shields.io/badge/Streamlit-Frontend-red)
![Docker](https://img.shields.io/badge/Docker-Containerized-blue)

---

## Problem Statement

Traditional educational videos are stuck in a straight line and hard to search through. Students often waste hours skipping forward and backward through long lecture recordings just to find a single explanation, a quick snippet of code, or a specific math formula. At the same time, relying on expensive, third-party AI tools creates big risks around leaking private student data, exposing exclusive course materials, and facing unpredictable monthly bills.

---

## Solution Proposed

NexaAI is a privacy-focused offline AI Teaching Assistant designed for intelligent lecture interaction.The system processes lecture transcript JSON files, converts them into embeddings, and enables Retrieval-Augmented Generation (RAG) based question answering.
NexaAI introduces a dual-assistant architecture:

### AtlasAI
- Strict syllabus-based assistant
- Answers only from course material
- Provides exact timestamps and lecture references

### EchoAI
- General-purpose AI companion
- Handles programming, logic, debugging, and general questions

---

## Tech Stack Used
1. Python 
2. FastAPI 
3. SQLite 
4. SQLAlchemy 
5. Streamlit 
6. Scikit-Learn

---

## Infrastructure Required
- Docker
- GitHub Actions

---
# How to run

## step 1. Cloning the repository.

```bash
git clone https://github.com/Harshadachaudhariii/ai-teaching-assistant.git
```

## step 2. Create a virtual environment.
python -m venv .venv

# Windows PowerShell
.\.venv\Scripts\Activate.ps1

# macOS / Linux
source .venv/bin/activate
