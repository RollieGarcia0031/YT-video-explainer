from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from youtube_utils import get_transcript
from llm import generate_explanation

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
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

    return {
        "explanation": explanation
    }

