run:
	uvicorn backend.app.main:app --reload --port 8000

backend:
	uvicorn backend.app.main:app --reload --port 8000

frontend:
	streamlit run Frontend/app.py

install:
	python -m pip install -r requirements.txt

install-dev:
	python -m pip install -r requirements-dev.txt || true

docker-up:
	docker compose up --build

test:
	pytest -q

.PHONY: run backend frontend install install-dev docker-up test
