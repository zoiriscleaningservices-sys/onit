import json
import time
import random
import uuid
import re
import requests
import os
from datetime import datetime

# === CONFIGURATION ===
GROQ_API_KEY = os.getenv('GROQ_API_KEY')  # Free key from https://console.groq.com/keys

SUPABASE_URL = 'https://dwxbzltxsdeshmmtcycv.supabase.co'
SUPABASE_ANON_KEY = 'sb_publishable_4PWdqRYFR0E-tp-OjdTP3Q_S_5qvRbp'

IMAGE_URLS = [
    "https://images.unsplash.com/photo-1585421514284-efb74c2b69ba?ixlib=rb-4.0.3&auto=format&fit=crop&w=1400&q=80",
    "https://images.unsplash.com/photo-1603712725038-e9334ae8f39f?ixlib=rb-4.0.3&auto=format&fit=crop&w=1400&q=80",
    "https://images.unsplash.com/photo-1581578731548-c64695cc6952?ixlib=rb-4.0.3&auto=format&fit=crop&w=1400&q=80",
    "https://images.unsplash.com/photo-1558618664-f4d05c2e5750?ixlib=rb-4.0.3&auto=format&fit=crop&w=1400&q=80",
    "https://images.unsplash.com/photo-1584622650111-993a426fbf0a?ixlib=rb-4.0.3&auto=format&fit=crop&w=1400&q=80",
    "https://images.unsplash.com/photo-1616588330908-3508269d1999?ixlib=rb-4.0.3&auto=format&fit=crop&w=1400&q=80",
    "https://images.unsplash.com/photo-1556912173-3bb406ef7e77?ixlib=rb-4.0.3&auto=format&fit=crop&w=1400&q=80",
    "https://images.unsplash.com/photo-1600585154340-be6161a56a0c?ixlib=rb-4.0.3&auto=format&fit=crop&w=1400&q=80",
    "https://images.unsplash.com/photo-1519643381402-145847b87c9a?ixlib=rb-4.0.3&auto=format&fit=crop&w=1400&q=80",
    "https://images.unsplash.com/photo-1583254764196-8db317f9b9c1?ixlib=rb-4.0.3&auto=format&fit=crop&w=1400&q=80",
    "https://images.pexels.com/photos/4239013/pexels-photo-4239013.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2",
    "https://images.pexels.com/photos/5591766/pexels-photo-5591766.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2",
    "https://images.pexels.com/photos/6194981/pexels-photo-6194981.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2",
    "https://images.pexels.com/photos/4099296/pexels-photo-4099296.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2",
    "https://images.pexels.com/photos/5591794/pexels-photo-5591794.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2"
]

def generate_blog_post():
    prompt = """
You are an expert SEO blog writer for Zoiris Cleaning Services, a professional cleaning company in Mobile, Alabama.

Create a unique, engaging, and informative blog post (450-650 words) on a cleaning-related topic relevant to Mobile, AL residents.

Incorporate these SEO keywords naturally multiple times:
- cleaning services Mobile AL
- house cleaning Mobile Alabama
- professional cleaners Mobile
- deep cleaning Mobile AL
- residential cleaning Mobile AL
- commercial cleaning Mobile Alabama

Tie in local elements: Mobile's humid climate, pollen, beaches, Mardi Gras cleanup, port dust, etc.

Use **bold** for key phrases and __underline__ for emphasis where it fits.

End with a strong call-to-action:
"Ready for a spotless home or office? Contact Zoiris Cleaning Services today at (251) 930-8621 or email zoiriscleaningservices@gmail.com for a free quote!"

Output strictly in this format:

Title: [SEO-Optimized Title Here]

Content: [Full blog post here with markdown formatting]
"""

    response = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": "llama-3.1-70b-versatile",  # Excellent quality, free tier eligible
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.85,
            "max_tokens": 1800
        }
    )

    if response.status_code != 200:
        raise Exception(f"Groq API error {response.status_code}: {response.text}")

    text = response.json()['choices'][0]['message']['content']

    # Robust parsing
    if "Title:" in text and "Content:" in text:
        title = text.split("Title:")[1].split("Content:")[0].strip()
        content = text.split("Content:")[1].strip()
    else:
        lines = text.splitlines()
        title = lines[0].replace("Title:", "").strip() if lines else "Professional Cleaning Tips for Mobile AL"
        content = "\n".join(lines[2:]).strip()

    return title, content

def post_to_supabase(title, content):
    slug = re.sub(r'[^a-z0-9-]+', '-', title.lower()).strip('-')[:80]

    profile_url = random.choice(IMAGE_URLS)
    gallery_urls = random.sample([url for url in IMAGE_URLS if url != profile_url], random.randint(1, 5))

    post_data = {
        "id": str(uuid.uuid4()),
        "created_at": datetime.utcnow().isoformat() + "Z",
        "name": title,
        "description": content,
        "profile": profile_url,
        "photos": gallery_urls,
        "slug": slug
    }

    response = requests.post(
        f"{SUPABASE_URL}/rest/v1/services",
        headers={
            "apikey": SUPABASE_ANON_KEY,
            "Authorization": f"Bearer {SUPABASE_ANON_KEY}",
            "Content-Type": "application/json",
            "Prefer": "return=minimal"
        },
        json=post_data
    )

    if response.status_code == 201:
        print(f"SUCCESS: Published '{title}'")
        print(f"Live URL: https://www.zoiriscleaningservices.com/blog/{slug}")
    else:
        print(f"Failed: {response.status_code} - {response.text}")

if __name__ == "__main__":
    if not GROQ_API_KEY:
        print("ERROR: GROQ_API_KEY missing")
        exit(1)

    print(f"[{datetime.now()}] Zoiris Cleaning AI Blog Agent (Groq Free) - Starting...")
    try:
        title, content = generate_blog_post()
        post_to_supabase(title, content)
    except Exception as e:
        print(f"AGENT FAILED: {str(e)}")
