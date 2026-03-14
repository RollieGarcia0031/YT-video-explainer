import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from backend.llm import generate_explanation
from backend.youtube_utils import get_transcript

app = FastAPI()

allowed_origins = [
    "http://localhost:3000",
    os.getenv("VERCEL_APP_ORIGIN", "https://your-app.vercel.app"),
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class VideoRequest(BaseModel):
    url: str


@app.get("/")
def health():
    return {"status": "ok"}


@app.post("/analyze")
async def analyze_video(data: VideoRequest):
    transcript = get_transcript(data.url)
    explanation = generate_explanation(transcript)

    return {"explanation": explanation}
