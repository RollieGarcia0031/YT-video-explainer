# YT Video Explainer Monorepo

This repository is organized as a monorepo for:

- **Frontend:** Next.js app in `./frontend` (deploy to Vercel)
- **Backend:** FastAPI + local Hugging Face model in `./backend` (deploy to Hugging Face Spaces with Docker SDK)

## Project Structure

```text
.
├── backend/            # FastAPI app, transcript parsing, local LLM inference
├── frontend/           # Next.js app
├── docker-compose.yml  # Local development for frontend + backend
└── Dockerfile          # Hugging Face Spaces backend image (port 7860)
```

## Backend (Hugging Face Spaces / Docker)

- Root `Dockerfile` installs Python and backend dependencies.
- FastAPI serves on **port 7860**.
- Models are downloaded with `huggingface_hub` into `/models`.
- CORS allows:
  - `http://localhost:3000`
  - `https://your-app.vercel.app` (or set `VERCEL_APP_ORIGIN`)

## Frontend (Vercel)

All API calls use `process.env.NEXT_PUBLIC_API_URL`.

- Local dev: set in `frontend/.env.local`
  - `NEXT_PUBLIC_API_URL=http://localhost:7860`
- Production (Vercel): set environment variable to:
  - `https://[user]-[space].hf.space`

## Local Development

### Option A: Run with Docker Compose (recommended)

#### 1) Prerequisites

- Docker + Docker Compose installed and running.

#### 2) Start both services

```bash
docker compose up --build
```

This starts:

- Frontend at `http://localhost:3000`
- Backend at `http://localhost:7860`
- Persistent model cache mounted at `./models:/models`

> First backend startup can take longer because the selected Hugging Face model is downloaded into `./models`.

#### 3) Use the app

1. Open `http://localhost:3000`
2. Paste a YouTube URL
3. Click **Analyze**

#### 4) Stop services

```bash
docker compose down
```

### Option B: Run services manually (without Docker)

#### Backend

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r backend/requirements.txt
export HF_MODEL_ID=google/flan-t5-small
export MODELS_DIR=./models
export VERCEL_APP_ORIGIN=https://your-app.vercel.app
uvicorn backend.main:app --host 0.0.0.0 --port 7860
```

#### Frontend (new terminal)

```bash
cd frontend
npm install
cat > .env.local <<'ENV'
NEXT_PUBLIC_API_URL=http://localhost:7860
ENV
npm run dev
```

Then open `http://localhost:3000`.