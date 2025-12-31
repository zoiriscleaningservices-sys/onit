import json
import random
import uuid
import re
import requests
import os
from datetime import datetime

GROQ_API_KEY = os.getenv('GROQ_API_KEY')

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
You are an expert SEO blog writer for Zoiris Cleaning Services in Mobile, Alabama.

Write a unique 500-700 word blog post about cleaning tips or services.

Include these keywords naturally: cleaning services Mobile AL, house cleaning Mobile Alabama, professional cleaners Mobile, deep cleaning Mobile AL, residential cleaning Mobile AL, commercial cleaning Mobile Alabama.

Mention local things like humidity, pollen, beaches, Mardi Gras.

Use **bold** and __underline__ for keywords.

End with: "Contact Zoiris Cleaning Services at (251) 930-8621 or zoiriscleaningservices@gmail.com for a free quote!"

Output exactly:

Title: [Title]

Content: [Full post]
"""

    response = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers={"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"},
        json={
            "model": "llama-3.1-70b-versatile",
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.8,
            "max_tokens": 1800
        }
    )

    if response.status_code != 200:
        raise Exception(f"Error: {response.text}")

    text = response.json()['choices'][0]['message']['content']

    title = text.split("Title:")[1].split("Content:")[0].strip() if "Title:" in text else "Best Cleaning Services in Mobile AL"
    content = text.split("Content:")[1].strip() if "Content:" in text else text

    return title, content

def post_to_supabase(title, content):
    slug = re.sub(r'[^a-z0-9-]+', '-', title.lower()).strip('-')[:80]
    profile_url = random.choice(IMAGE_URLS)
    gallery_urls = random.sample([u for u in IMAGE_URLS if u != profile_url], random.randint(2, 5))

    data = {
        "id": str(uuid.uuid4()),
        "created_at": datetime.utcnow().isoformat() + "Z",
        "name": title,
        "description": content,
        "profile": profile_url,
        "photos": gallery_urls,
        "slug": slug
    }

    r = requests.post(
        f"{SUPABASE_URL}/rest/v1/services",
        headers={
            "apikey": SUPABASE_ANON_KEY,
            "Authorization": f"Bearer {SUPABASE_ANON_KEY}",
            "Content-Type": "application/json",
            "Prefer": "return=minimal"
        },
        json=data
    )

    if r.status_code == 201:
        print(f"SUCCESS! New post: {title}")
        print(f"View: https://www.zoiriscleaningservices.com/blog/{slug}")
    else:
        print(f"Failed: {r.status_code} {r.text}")

if __name__ == "__main__":
    if not GROQ_API_KEY:
        print("No GROQ_API_KEY")
        exit(1)

    try:
        title, content = generate_blog_post()
        post_to_supabase(title, content)
    except Exception as e:
        print(f"Error: {e}")
