FROM node:20-bullseye

RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    curl

RUN curl -fsSL https://ollama.com/install.sh | sh

WORKDIR /app

COPY backend ./backend
COPY frontend ./frontend

RUN pip install -r backend/requirements.txt

WORKDIR /app/frontend
RUN npm install
RUN npm run build

WORKDIR /app

EXPOSE 3000
EXPOSE 8000
EXPOSE 11434

CMD ollama serve & \
    uvicorn backend.main:app --host 0.0.0.0 --port 8000 & \
    cd frontend && npm start
