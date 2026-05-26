# NexaAI: AI Teaching Assistant

![Python](https://img.shields.io/badge/Python-3.11-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-green)
![Streamlit](https://img.shields.io/badge/Streamlit-Frontend-red)
![Docker](https://img.shields.io/badge/Docker-Containerized-blue)
![License](https://img.shields.io/badge/License-MIT-yellow)

---

## Problem Statement

Traditional educational videos are linear and difficult to search efficiently. Students often spend a large amount of time skipping through lengthy lecture recordings just to find a single explanation, code snippet, or mathematical concept.

Additionally, relying on expensive third-party AI services introduces major concerns regarding:

- Privacy of student data
- Exposure of premium course materials
- High and unpredictable API costs

---

## Solution Proposed

NexaAI is a privacy-focused offline AI Teaching Assistant designed for intelligent lecture interaction.

The system processes lecture transcript JSON files, converts them into embeddings, and enables Retrieval-Augmented Generation (RAG) based question answering.

NexaAI introduces a dual-assistant architecture:

### AtlasAI
- Strict syllabus-based assistant
- Answers only from course material
- Provides exact timestamps and lecture references

### EchoAI
- General-purpose AI companion
- Handles programming, logic, debugging, and general questions

---

## Features

- Retrieval-Augmented Generation (RAG)
- Timestamp-based lecture search
- Offline-first architecture
- FastAPI backend API
- Streamlit interactive frontend
- Docker container support
- CI/CD using GitHub Actions
- Local vector embedding pipeline
- JSON transcript ingestion

---

## Tech Stack Used

| Category | Technologies |
|---|---|
| Language | Python |
| Backend | FastAPI |
| Frontend | Streamlit |
| Database | SQLite |
| ORM | SQLAlchemy |
| ML / Embeddings | Scikit-Learn |
| Containerization | Docker |
| CI/CD | GitHub Actions |

---

## Infrastructure Required

- Docker
- Docker Compose
- GitHub Actions
- Python 3.10+

---

# Project Structure

```text
backend/                FastAPI backend
Frontend/               Streamlit frontend
LLM/                    Embedding & preprocessing pipeline
docker/                 Docker configurations
docs/                   Project architecture images
.github/workflows/      CI pipeline