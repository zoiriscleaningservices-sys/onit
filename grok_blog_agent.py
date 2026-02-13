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

# 100+ royalty-free cleaning images (expanded list from Pexels and Unsplash - all free for commercial use, no attribution required)
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
    "https://images.pexels.com/photos/4107135/pexels-photo-4107135.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2",
    "https://images.pexels.com/photos/4239028/pexels-photo-4239028.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2",
    "https://images.pexels.com/photos/6197113/pexels-photo-6197113.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2",
    "https://images.pexels.com/photos/5998125/pexels-photo-5998125.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2",
    "https://images.pexels.com/photos/4239031/pexels-photo-4239031.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2",
    "https://images.pexels.com/photos/4107140/pexels-photo-4107140.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2",
    "https://images.pexels.com/photos/6201987/pexels-photo-6201987.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2",
    "https://images.pexels.com/photos/4239143/pexels-photo-4239143.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2",
    "https://images.pexels.com/photos/9462338/pexels-photo-9462338.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2",
    "https://images.pexels.com/photos/4107126/pexels-photo-4107126.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2",
    # Additional Pexels cleaning-related images
    "https://images.pexels.com/photos/4239033/pexels-photo-4239033.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2",
    "https://images.pexels.com/photos/4107131/pexels-photo-4107131.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2",
    "https://images.pexels.com/photos/6195972/pexels-photo-6195972.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2",
    "https://images.pexels.com/photos/6201990/pexels-photo-6201990.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2",
    "https://images.pexels.com/photos/4239025/pexels-photo-4239025.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2",
    "https://images.pexels.com/photos/9462343/pexels-photo-9462343.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2",
    "https://images.pexels.com/photos/4107138/pexels-photo-4107138.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2",
    "https://images.pexels.com/photos/6197118/pexels-photo-6197118.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2",
    "https://images.pexels.com/photos/5998130/pexels-photo-5998130.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2",
    "https://images.pexels.com/photos/4239140/pexels-photo-4239140.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2",
    # Unsplash cleaning images (high-quality, royalty-free)
    "https://images.unsplash.com/photo-1581578731548-565e3b3fd02b?auto=format&fit=crop&w=1260&q=80",
    "https://images.unsplash.com/photo-1558618666-7b3cb8a3b9c6?auto=format&fit=crop&w=1260&q=80",
    "https://images.unsplash.com/photo-1584622650111-993a4261c1f5?auto=format&fit=crop&w=1260&q=80",
    "https://images.unsplash.com/photo-1519681393784-d120267933ba?auto=format&fit=crop&w=1260&q=80",
    "https://images.unsplash.com/photo-1600585154340-be6161a56a0c?auto=format&fit=crop&w=1260&q=80",
    "https://images.unsplash.com/photo-1581579438748-1e6bb24fd3c3?auto=format&fit=crop&w=1260&q=80",
    "https://images.unsplash.com/photo-1618004907033-1d2f8e8e6e0f?auto=format&fit=crop&w=1260&q=80",
    "https://images.unsplash.com/photo-1556912110-9d3b2d8e3f04?auto=format&fit=crop&w=1260&q=80",
    "https://images.unsplash.com/photo-1583258292688-1231a9f71da9?auto=format&fit=crop&w=1260&q=80",
    "https://images.unsplash.com/photo-1600568444334-1a3e2fd58a8d?auto=format&fit=crop&w=1260&q=80",
    "https://images.unsplash.com/photo-1591729896579-4e054b100c24?auto=format&fit=crop&w=1260&q=80",
    "https://images.unsplash.com/photo-1616594039961-9b858c2e8513?auto=format&fit=crop&w=1260&q=80",
    "https://images.unsplash.com/photo-1581578303128-3fc40e9a93c6?auto=format&fit=crop&w=1260&q=80",
    "https://images.unsplash.com/photo-1527515637462-cff94ebc1b04?auto=format&fit=crop&w=1260&q=80",
    "https://images.unsplash.com/photo-1609017048893-9b1e3c6ea3a3?auto=format&fit=crop&w=1260&q=80",
    # Continue adding more from Pexels/Unsplash searches
    "https://images.pexels.com/photos/4239029/pexels-photo-4239029.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2",
    "https://images.pexels.com/photos/4107127/pexels-photo-4107127.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2",
    "https://images.pexels.com/photos/6195960/pexels-photo-6195960.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2",
    "https://images.pexels.com/photos/6201985/pexels-photo-6201985.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2",
    "https://images.pexels.com/photos/9462340/pexels-photo-9462340.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2",
]

def generate_post_with_grok():
    response = client.chat.completions.create(
        model="grok-4",  # Best quality model
        messages=[
            {"role": "system", "content": "You are a top SEO blogger for Zoiris Cleaning Services in Mobile, AL. Write ONE completely unique, long (1000-1500 words), helpful blog post on a varied topic like home maintenance, lifestyle tips, or local Mobile AL insights, but always tie it back to promoting Zoiris Cleaning Services as the top-rated, affordable provider. Title: catchy + keyword-rich but SHORT (50-60 characters max). Use keywords naturally (no stuffing): cleaning services Mobile AL, house cleaning Mobile Alabama, professional cleaners Mobile AL, deep cleaning Mobile AL, move in move out cleaning Mobile AL, commercial cleaning Mobile AL, eco-friendly cleaning Mobile Alabama, top rated cleaning Mobile AL, affordable cleaning services Mobile AL, cheap cleaning Mobile AL, office cleaning Mobile AL. Focus on local ranking for Mobile AL by including sections with local tips (humidity, mold, hurricanes, salt air, pollen). Make it compliant with Google policies: helpful, original content without spam. Benefits of services, and end with CTA: Call **(251) 930-8621** or email zoiriscleaningservices@gmail.com. Use **bold** for key phrases. Output ONLY JSON: {\"title\": \"string\", \"content\": \"string with \\n for new lines\"}"},
            {"role": "user", "content": "Generate a fresh, unique post on a new topic for Zoiris Cleaning Services in Mobile AL."}
        ],
        response_format={"type": "json_object"},
        temperature=1.0
    )
    data = json.loads(response.choices[0].message.content)
    return data["title"], data["content"]

def main():
    try:
        title, content = generate_post_with_grok()

        # Safe slug generation (pure Python regex) - limited to 80 chars for safety
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
            print(f"Character count: {len(title)} (ideal 50-60 for full Google display)")
            print(f"URL: https://www.zoiriscleaningservices.com/blog/blog/{slug}")
        else:
            print("Insert failed:", result)

    except Exception as e:
        print("ERROR:", str(e))
        raise

if __name__ == "__main__":
    main()
