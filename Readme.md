# NexaAI: AI Teaching Assistant

![Python](https://img.shields.io/badge/Python-3.11-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-green)
![Streamlit](https://img.shields.io/badge/Streamlit-Frontend-red)
![Docker](https://img.shields.io/badge/Docker-Containerized-blue)


## Problem Statement

Traditional educational videos are stuck in a straight line and hard to search through. Students often waste hours skipping forward and backward through long lecture recordings just to find a single explanation, a quick snippet of code, or a specific math formula. At the same time, relying on expensive, third-party AI tools creates big risks around leaking private student data, exposing exclusive course materials, and facing unpredictable monthly bills.


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


## Tech Stack Used
1. Python 
2. FastAPI 
3. SQLite 
4. SQLAlchemy 
5. Streamlit 
6. Scikit-Learn


## Infrastructure Required
- Docker
- GitHub Actions


# How to run

## Step 1. Cloning the repository.

```bash
git clone https://github.com/Harshadachaudhariii/ai-teaching-assistant.git
```

## Step 2. Create a virtual environment.
```bash
python -m venv .venv

# Windows PowerShell
.\.venv\Scripts\Activate.ps1

# macOS / Linux
source .venv/bin/activate
```

## Step 3. Install the requirements
```bash
python -m pip install -r requirements.txt
```

## Step 4. Configure Environment Variables
Create a .env file in your root workspace. Use the following baseline parameters:
```bash
SECRET_KEY=your_super_secret_jwt_signing_key
OLLAMA_BASE_URL=http://localhost:11434
DATABASE_URL=sqlite:///./db/nexa_ai.db

Email SMTP Setup (For Password Reset OTP Validation)

EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USERNAME=your_email@gmail.com
EMAIL_PASSWORD=your_app_password
EMAIL_FROM=your_email@gmail.com
```

## Step 5. Start the Application Stack
You can launch both server ecosystems simultaneously using the project Makefile hooks:
```bash
make backend      # Bootstraps FastAPI Backend on port 8000 via Uvicorn
make frontend     # Instantiates Streamlit Frontend on port 8501
```

Alternatively, step manually into individual workspace packages to initiate runtimes natively:
```bash
# Manual Backend Initialization
cd backend
uvicorn app.main:app --reload --port 8000
```
```bash
# Manual Frontend Initialization
cd Frontend
streamlit run app.py
```

## Run Locally
1. Check if the Dockerfile is available in the project directory
2. Build the Docker image
From the project root directory:
```bash
docker compose up -d --build
```

Access application:
```bash
1. Frontend (Streamlit)
http://localhost:8501

2. Backend API (FastAPI)
http://localhost:8000
```

## Project Architecture
![Project Architecture](docs/Architecture%20of%20NexaAI%20Teaching%20Assistant.png)

## Conclusion
NexaAI provides a safe, fast, and completely free way to build modern digital classrooms. By running smart AI models directly on local computers, schools and colleges can give students an interactive tool to instantly search through lectures. They can do all of this without risking private student data, exposing exclusive course materials, or leaking valuable academic research records.