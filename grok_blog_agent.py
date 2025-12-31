import os
import uuid
import random
import re  # <-- Added for proper regex
import json
from supabase import create_client, Client
from openai import OpenAI

SUPABASE_URL = "https://dwxbzltxsdeshmmtcycv.supabase.co"
SUPABASE_ANON_KEY = "sb_publishable_4PWdqRYFR0E-tp-OjdTP3Q_S_5qvRbp"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)

XAI_API_KEY = os.environ["XAI_API_KEY"]
client = OpenAI(api_key=XAI_API_KEY, base_url="https://api.x.ai/v1")

# 100+ royalty-free cleaning images (expand this list as needed)
IMAGE_POOL = [
    "https://images.pexels.com/photos/6195951/pexels-photo-6195951.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2",
    "https://images.pexels.com/photos/6195274/pexels-photo-6195274.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2",
    "https://images.pexels.com/photos/6196684/pexels-photo-6196684.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2",
    "https://images.pexels.com/photos/6195104/pexels-photo-6195104.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2",
    "https://images.pexels.com/photos/6195287/pexels-photo-6195287.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2",
    "https://images.pexels.com/photos/6196229/pexels-photo-6196229.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2",
    "https://images.pexels.com/photos/4239031/pexels-photo-4239031.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2",
    "https://images.pexels.com/photos/9462341/pexels-photo-9462341.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2",
    "https://images.pexels.com/photos/4107129/pexels-photo-4107129.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2",
    "https://images.pexels.com/photos/4253621/pexels-photo-4253621.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2",
    # Add more Pexels/Unsplash URLs here — all free for commercial use
    "https://images.unsplash.com/photo-1581578731548-565e3b3fd02b?auto=format&fit=crop&w=1260&q=80",
    "https://images.unsplash.com/photo-1558618666-7b3cb8a3b9c6?auto=format&fit=crop&w=1260&q=80",
    # ... continue adding up to 100+
]

def generate_post_with_grok():
    response = client.chat.completions.create(
        model="grok-4",  # Best quality model
        messages=[
            {"role": "system", "content": "You are a top SEO blogger for Zoiris Cleaning Services in Mobile, AL. Write ONE completely unique, long (1000-1500 words), helpful blog post. Title: catchy + keyword-rich. Content: in-depth guide on a cleaning topic. Use keywords naturally: cleaning services Mobile AL, house cleaning Mobile Alabama, professional cleaners Mobile AL, deep cleaning Mobile AL, move in move out cleaning Mobile AL, commercial cleaning Mobile AL, eco-friendly cleaning Mobile Alabama. Include sections, local tips (humidity, mold, hurricanes), benefits, and end with CTA: Call **(251) 930-8621** or email zoiriscleaningservices@gmail.com. Use **bold** for key phrases. Output ONLY JSON: {\"title\": \"string\", \"content\": \"string with \\n for new lines\"}"},
            {"role": "user", "content": "Generate a fresh, unique post on a new cleaning topic for Mobile AL."}
        ],
        response_format={"type": "json_object"},
        temperature=1.0
    )
    data = json.loads(response.choices[0].message.content)
    return data["title"], data["content"]

def main():
    try:
        title, content = generate_post_with_grok()

        # Fixed slug generation (pure Python regex)
        slug = re.sub(r'[^a-z0-9]+', '-', title.lower())
        slug = re.sub(r'-+', '-', slug)
        slug = slug.strip('-')[:80]

        profile = random.choice(IMAGE_POOL)
        photos = random.sample(IMAGE_POOL, k=random.randint(3, 5))

        post = {
            "id": str(uuid.uuid4()),
            "name": title,
            "description": content,
            "profile": profile,
            "photos": photos,
            "slug": slug,
            "created_at": "now()"
        }

        result = supabase.table("services").insert(post).execute()
        if result.data:
            print(f"SUCCESS! Published: {title}")
            print(f"URL: https://www.zoiriscleaningservices.com/blog/blog/{slug}")
        else:
            print("Insert failed:", result)

    except Exception as e:
        print("ERROR:", str(e))
        raise

if __name__ == "__main__":
    main()
