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

def generate_post_with_grok():
    response = client.chat.completions.create(
        model="grok-4",
        messages=[
            {"role": "system", "content": "You are a top SEO blogger for Zoiris Cleaning Services in Mobile, AL. Write ONE completely unique, long (1000-1500 words), helpful blog post about the full range of cleaning services offered by Zoiris Cleaning Services in Mobile, Alabama. Title: catchy + keyword-rich but SHORT (50-60 characters max). Primary keywords (use frequently & naturally): cleaning services Mobile AL, house cleaning Mobile Alabama, professional cleaners Mobile AL, deep cleaning Mobile AL, move in move out cleaning Mobile AL, commercial cleaning Mobile AL, eco-friendly cleaning Mobile Alabama. Incorporate as many service terms as possible naturally. Content: in-depth guide showcasing Zoiris as the top provider for ALL cleaning needs in Mobile AL. Include sections on residential, commercial, specialty cleans, local Mobile tips (humidity, mold, hurricanes, salt air, pollen), benefits, and end with strong CTA: Call **(251) 930-8621** or email zoiriscleaningservices@gmail.com. Use **bold** for key phrases. Output ONLY JSON: {\"title\": \"string\", \"content\": \"string with \\n for new lines\", \"image_prompt\": \"string\"}"},
            {"role": "user", "content": "Generate a fresh, unique comprehensive post covering the full range of cleaning services by Zoiris Cleaning Services in Mobile AL. Also include a detailed image_prompt for a professional featured image that perfectly matches this post."}
        ],
        response_format={"type": "json_object"},
        temperature=1.0
    )
    data = json.loads(response.choices[0].message.content)
    return data["title"], data["content"], data.get("image_prompt", "Professional cleaning team providing top-rated cleaning services in a bright, modern home in Mobile Alabama")

def generate_image(prompt: str):
    """Generate an image using Grok's image model and return base64 string"""
    try:
        response = client.images.generate(
            model="grok-2-image-1212",  # Current Grok image generation model
            prompt=prompt,
            n=1,
            response_format="b64_json"  # Returns base64 directly
        )
        return response.data[0].b64_json
    except Exception as e:
        print(f"Image generation failed: {e}")
        # Fallback: return a placeholder base64 (transparent 1x1 pixel)
        return "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII="

def main():
    try:
        title, content, image_prompt = generate_post_with_grok()

        print(f"Blog Title: {title}")
        print(f"Generating featured image with prompt: {image_prompt}")

        # Generate featured profile image
        full_prompt = image_prompt + ", professional photography style, high resolution, bright and clean, realistic, detailed, inviting"
        profile_b64 = generate_image(full_prompt)

        # Generate 3-5 additional gallery images with variations
        photos_b64 = []
        num_photos = random.randint(3, 5)
        print(f"Generating {num_photos} additional images...")
        for i in range(num_photos):
            variation = f"{image_prompt}, variation {i+1}, different angle or room, professional cleaning scene in Mobile AL, bright natural light, eco-friendly products, happy team"
            b64 = generate_image(variation)
            photos_b64.append(b64)

        # Safe slug generation
        slug = re.sub(r'[^a-z0-9]+', '-', title.lower())
        slug = re.sub(r'-+', '-', slug)
        slug = slug.strip('-')[:80]

        post = {
            "id": str(uuid.uuid4()),
            "name": title,
            "description": content,
            "profile": profile_b64,      # base64 string for featured image
            "photos": photos_b64,        # list of base64 strings for gallery
            "slug": slug,
            "created_at": "now()"
        }

        result = supabase.table("services").insert(post).execute()
        if result.data:
            print(f"\nSUCCESS! Blog post published successfully!")
            print(f"Title: {title}")
            print(f"Character count: {len(title)} (ideal 50-60)")
            print(f"Featured + {len(photos_b64)} AI-generated images attached")
            print(f"URL: https://www.zoiriscleaningservices.com/blog/blog/{slug}")
        else:
            print("Insert failed:", result)

    except Exception as e:
        print("ERROR:", str(e))
        raise

if __name__ == "__main__":
    main()
