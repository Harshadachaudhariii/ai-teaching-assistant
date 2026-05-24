## AI Teaching Assistant — README

**Project**: RAG-based AI Teaching Assistant — a backend API (FastAPI) and a Streamlit frontend that can ingest transcript JSONs, build embeddings, and answer questions using a retrieval-augmented generation (RAG) workflow.

**Quick links**
- Backend entry: `backend/app/main.py`
- Frontend entry: `Frontend/app.py`
- Embeddings pipeline: `LLM/preprocess_json.py`
- Env template: `.env.example`

**Requirements**
- Python 3.10+ (3.11 recommended)
- Docker & Docker Compose (optional, for containerized runs)

**Setup (local, virtualenv)**
1. Create and activate a virtual environment:
```bash
python -m venv .venv
# Windows PowerShell
.\.venv\Scripts\Activate.ps1
# macOS / Linux
source .venv/bin/activate
```
2. Install runtime dependencies:
```bash
python -m pip install -r requirements.txt
```
3. Copy environment file and fill secrets:
```bash
cp .env
# then edit .env
```

**Run locally**
- Start the backend API (development):
```bash
uvicorn backend.app.main:app --reload --port 8000
```
- Start the frontend UI (Streamlit):
```bash
streamlit run Frontend/app.py
```
- Shortcuts via `Makefile`:
```bash
make backend      # runs backend
make frontend     # runs frontend
make test         # runs pytest
make docker-up    # docker compose up --build
```

**Docker (containerized)**
- Build and start services with Docker Compose (includes placeholder Ollama service):
```bash
docker compose up --build
```

**Testing & CI**
- Unit / smoke tests live under `backend/tests/`. Run locally with:
```bash
pytest -q
```
- GitHub Actions workflow is configured at `.github/workflows/ci.yml` and runs tests on push/PR to `main`.

**How to prepare your data (RAG pipeline)**
1. Collect or export transcripts for your videos as JSON files and place them in the `jsons/` folder.
2. Run the preprocessing script to convert transcripts to embeddings: `LLM/preprocess_json.py`. This script produces `embeddings.joblib` which the app can load.
3. The backend RAG service (`backend/services/rag_service.py`) reads the vector store and answers queries by combining retrieved context and an LLM prompt.

**Preparing transcripts (video → audio → JSON)**
If you have raw video files, follow these steps to extract audio and create JSON transcripts that the pipeline can consume.

1. Install prerequisites

 - Install `ffmpeg` (system package). On macOS: `brew install ffmpeg`. On Ubuntu: `sudo apt install ffmpeg`.
 - Install a local Whisper implementation (optional):
```bash
python -m pip install -U openai-whisper
```

2. Extract audio from a video (example using `ffmpeg`) — convert to 16 kHz mono WAV:
```bash
ffmpeg -i input.mp4 -ar 16000 -ac 1 -vn input.wav
```

3. Transcribe audio to JSON using Whisper (Python snippet)

Create a small Python script `transcribe_to_json.py`:
```python
import whisper, json
model = whisper.load_model('small')
result = model.transcribe('input.wav')
with open('jsons/input.json', 'w', encoding='utf-8') as f:
		json.dump(result, f, ensure_ascii=False, indent=2)
```

Run it:
```bash
python transcribe_to_json.py
```

The generated JSON will include `text`, `segments` (with timestamps), `language`, and `duration`. Move or save those JSON files into the repository `jsons/` folder so the embedding/preprocessing script can read them.

4. Batch processing (folder of videos)

 - Convert all videos in a folder to WAVs using a loop (bash):
```bash
mkdir -p audio
for f in videos/*.{mp4,mkv,mov,avi,webm}; do
	[ -f "$f" ] || continue
	name=$(basename "$f")
	ffmpeg -y -i "$f" -ar 16000 -ac 1 -vn "audio/${name%.*}.wav"
done
```

 - Then transcribe each WAV to JSON with a small Python loop (use the `whisper` model as above).

5. Alternatives

- Use the OpenAI Audio Transcriptions API (if you prefer cloud transcription) and save the response as JSON. This requires an API key and network access.
- Use lighter or faster models (`tiny`, `base`) for speed; `small`/`medium` balance quality and cost.

6. Tips

- Keep `jsons/` organized by original filename so downstream preprocessing can match audio/text to source video.
- For long videos, consider chunking audio before transcribing to avoid memory/time limits.
- Verify transcript quality and clean punctuation or speaker labels before embedding.


**Project structure (top-level)**
- `backend/` — FastAPI app, routers, services, models, DB
- `Frontend/` — Streamlit UI and helper modules
- `LLM/` — preprocessing and embedding scripts
- `jsons/` — transcript JSON files (input)
- `docker/` — Dockerfiles for backend/frontend
- `.github/workflows/ci.yml` — CI workflow





