import json
import time
import random
import uuid
import re
import requests
import os
from datetime import datetime

# === CONFIGURATION ===
GROQ_API_KEY = os.getenv('GROQ_API_KEY')  # Get free key at https://console.groq.com/keys

SUPABASE_URL = 'https://dwxbzltxsdeshmmtcycv.supabase.co'
SUPABASE_ANON_KEY = 'sb_publishable_4PWdqRYFR0E-tp-OjdTP3Q_S_5qvRbp'

IMAGE_URLS = [ ... ]  # Keep your same list

def generate_blog_post():
    prompt = """[Your full prompt here - same as before]"""

    response = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": "llama-3.1-70b-versatile",  # Fast & high-quality, free tier eligible
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.8,
            "max_tokens": 1500
        }
    )

    if response.status_code != 200:
        raise Exception(f"Groq error: {response.text}")

    text = response.json()['choices'][0]['message']['content']

    # Same parsing as before
    # ...

    return title, content

# Keep post_to_supabase the same (using requests)

if __name__ == "__main__":
    if not GROQ_API_KEY:
        print("ERROR: GROQ_API_KEY missing")
        exit(1)

    # Rest same
