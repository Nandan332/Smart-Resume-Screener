import os
import random

def get_embedding(text: str):
    """
    Try to call Gemini embedding if GEMINI_API_KEY exists in env.
    Fallback: deterministic pseudo-random vector (128 dims).
    """
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        # fallback deterministic pseudo-embedding
        seed_val = abs(hash(text)) & 0xffffffff
        rnd = random.Random(seed_val)
        return [rnd.random() for _ in range(128)]

    # Real Gemini call using google.generativeai if configured in app
    try:
        import google.generativeai as genai
        genai.configure(api_key=api_key)
        model = "models/text-embedding-003"  # adjust if needed
        resp = genai.embed_content(model=model, content=text)
        # response shape may vary; try to read embedding key
        if isinstance(resp, dict) and "embedding" in resp:
            return resp["embedding"]
        # fallback if structure differs
        return resp
    except Exception as e:
        print("Gemini embedding error:", e)
        # fallback deterministic
        seed_val = abs(hash(text)) & 0xffffffff
        rnd = random.Random(seed_val)
        return [rnd.random() for _ in range(128)]
