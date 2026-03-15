import os
from functools import lru_cache

from huggingface_hub import snapshot_download
from transformers import pipeline

MODEL_ID = os.getenv("HF_MODEL_ID", "google/flan-t5-small")
MODELS_DIR = os.getenv("MODELS_DIR", "/models")


@lru_cache(maxsize=1)
def _get_generator():
    local_model_path = os.path.join(MODELS_DIR, MODEL_ID.replace("/", "--"))

    snapshot_download(
        repo_id=MODEL_ID,
        local_dir=local_model_path,
        local_dir_use_symlinks=False,
    )

    return pipeline(
        task="text-generation",
        model=local_model_path,
        tokenizer=local_model_path,
    )


def generate_explanation(transcript: str) -> str:
    generator = _get_generator()

    prompt = f"""
You are an AI tutor.

Explain the following YouTube transcript clearly.

Transcript:
{transcript[:5000]}

Provide:
1. Simple summary
2. Key concepts
3. Beginner-friendly explanation
4. Additional learning resources
"""

    result = generator(prompt, max_new_tokens=300, do_sample=False)
    return result[0]["generated_text"]
