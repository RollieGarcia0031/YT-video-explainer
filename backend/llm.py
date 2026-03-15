import os
from functools import lru_cache

from huggingface_hub import snapshot_download
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
import torch

MODEL_ID = os.getenv("HF_MODEL_ID", "google/flan-t5-base")
MODELS_DIR = os.getenv("MODELS_DIR", "/models")


@lru_cache(maxsize=1)
def _get_generator():
    local_model_path = os.path.join(MODELS_DIR, MODEL_ID.replace("/", "--"))

    snapshot_download(
        repo_id=MODEL_ID,
        local_dir=local_model_path,
    )

    model = AutoModelForSeq2SeqLM.from_pretrained(local_model_path)
    tokenizer = AutoTokenizer.from_pretrained(local_model_path)
    
    return {"model": model, "tokenizer": tokenizer}


def generate_explanation(transcript: str) -> str:
    generator = _get_generator()
    model = generator["model"]
    tokenizer = generator["tokenizer"]
    
    # More aggressive truncation to stay well under 512 limit
    # Reserve tokens for prompt + output
    max_input_tokens = 300  # Much smaller to be safe
    tokens = tokenizer.encode(transcript)
    
    if len(tokens) > max_input_tokens:
        truncated = tokenizer.decode(tokens[:max_input_tokens])
    else:
        truncated = transcript

    prompt = f"""Explain this YouTube transcript:

{truncated}

Provide a clear explanation with:
1. Summary
2. Key concepts
3. Beginner-friendly breakdown"""

    # Encode input with strict truncation
    input_ids = tokenizer.encode(
        prompt, 
        return_tensors="pt", 
        max_length=512, 
        truncation=True
    )
    
    # Generate with better parameters for longer output
    output_ids = model.generate(
        input_ids,
        max_new_tokens=500,
        min_new_tokens=100,
        do_sample=True,
        top_p=0.95,
        temperature=0.7,
        no_repeat_ngram_size=2,
    )
    
    # Decode output
    explanation = tokenizer.decode(output_ids[0], skip_special_tokens=True)
    
    return explanation
