import os
import requests

OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")
MODEL = os.getenv("MODEL", "phi3")


def generate_explanation(transcript):

    prompt = f"""
You are an AI tutor.

Explain the following YouTube transcript clearly.

Transcript:
{transcript}

Provide:

1. Simple summary
2. Key concepts
3. Beginner-friendly explanation
4. Additional learning resources
"""

    response = requests.post(
        f"{OLLAMA_URL}/api/chat",
        json={
            "model": MODEL,
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "stream": False
        }
    )

    data = response.json()

    return data["message"]["content"]

