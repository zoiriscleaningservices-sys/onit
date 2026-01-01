import os
import uuid
import random
import re  # <-- Added for proper regex
import json
import base64
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
            {"role": "system", "content": "You are a top SEO blogger for Zoiris Cleaning Services in Mobile, AL. Write ONE completely unique, long (1000-1500 words), helpful blog post about the full range of cleaning services offered by Zoiris Cleaning Services in Mobile, Alabama. Title: catchy + keyword-rich but SHORT (50-60 characters max). Primary keywords (use frequently & naturally): cleaning services Mobile AL, house cleaning Mobile Alabama, professional cleaners Mobile AL, deep cleaning Mobile AL, move in move out cleaning Mobile AL, commercial cleaning Mobile AL, eco-friendly cleaning Mobile Alabama. Incorporate as many of these service terms as possible naturally throughout the post: Deep clean, General housekeeping, Moving-related cleaning, Office & workplace cleaning, Standard cleaning, Recurring Services, Interior & exterior window cleaning, Bath And Kitchen, Business Cleaning, COVID-19 Clean, Carpet Vacuum, Ceiling Fans, Changing Sheets, Cleaning Equipment, Cleaning Your Home, Contract Cleaning, Contract Cleaning Services, Damp Mop, Deep Clean, Detailed Cleaning, Dining Room, Full Cleaning Service, Furniture Polish, Glass Cleaner, Granite Cleaner, Hardwood Floors, Hire A Cleaning Service, Home Or Business Cleaning, Initial Cleaning, Job Cleaning, Light Fixtures, Living Rooms, Maid Service, Monthly Cleaning Services, Move-Out, Office Cleaning Services, One Time Cleanings, Oven Clean, Personalized Service, Quarterly Cleaning Services, Refrigerator Clean, Regular Cleaning, Residential Clean, Rugs Vacuum, Specialty Cleaning, Take Trash, Trash Out, Vacuum Cleaner, Washing Dishes, Weekly Cleaning Services, Window Coverings, Wiping Down, Wood Floor Cleaner, Advanced Cleaning, Apartment Cleaning, Bathroom Cleaning, Best Maid Service, Blinds Dusted, Cabinet Cleaning And Organizing, Clean Window Sills, Cleaner Homes, Cleaning For Seniors, Cleaning Job, Cleaning Maid Services, Cleaning Process, Comprehensive Cleaning, Consistent Cleaning, Customized Clean, detailed cleaning, Dining Room Cleaning, Disinfection Housekeeping, Enhanced Disinfection, Everyday Housekeeping, Exceptional Clean, Free Cleaning, Green Cleaning, Gutter Cleaning, Holiday Cleaning, Home Organization, house cleaning, Household Disinfecting, Housekeeping Kitchen, Kitchen And Laundry Room, Laundry Room Cleaning, Living Room Cleaning, Mobile Home Cleaning, Move In/ Out Cleaning, Organizational Services, Our Home Cleaning Services, Oven Cleaning, Personalized Cleaning, Premium Home Cleaning Services, Pressure Washing, Refrigerator Cleaning, rental property cleaning, Room Cleaning Kitchen, Routine Cleanings, Seasonal Cleaning, Sparkling Clean, Specialized Cleaning, Specialty House Cleaning Services, Vacation Rental Cleaning, Wall Washing, Window Blind Cleaning, Wood Floors, Mattress cleaning, Upholstery cleaning, Fitness center & gym cleaning, Laboratory cleaning, Medical institution cleaning, Move-out cleaning, Movie theater cleaning, Multi-tenant cleaning, Office cleaning, Post-construction cleaning, Post-event cleaning, School & campus cleaning, Stadium cleaning, Gutter cleaning, Glass & mirror cleaning, Power/pressure washing, Rooftop/skylight cleaning, Window washing, Area rug cleaning, Carpet steam cleaning, Drapes & curtain cleaning, General carpet cleaning, Leather cleaning, Pet stain & odor removal. Content: in-depth guide showcasing Zoiris as the top provider for ALL these services in Mobile AL. Include sections on residential, commercial, specialty cleans, local Mobile tips (humidity, mold, hurricanes, salt air, pollen), benefits, and end with strong CTA: Call **(251) 930-8621** or email zoiriscleaningservices@gmail.com. Use **bold** for key phrases. Output ONLY JSON: {\"title\": \"string\", \"content\": \"string with \\n for new lines\", \"image_prompt\": \"string\"}"},
            {"role": "user", "content": "Generate a fresh, unique comprehensive post covering the full range of cleaning services by Zoiris Cleaning Services in Mobile AL. Also provide a detailed image_prompt for a professional, high-quality featured image that perfectly matches this blog post topic."}
        ],
        response_format={"type": "json_object"},
        temperature=1.0
    )
    data = json.loads(response.choices[0].message.content)
    return data["title"], data["content"], data.get("image_prompt", "Professional cleaning service in a bright modern home in Mobile Alabama")

def generate_image(prompt: str):
    """Generate an image using Grok's image generation model and return base64"""
    response = client.images.generate(
        model="grok-2-image-1212",  # Current Grok image generation model
        prompt=prompt,
        n=1,
        size="1024x1024",
        response_format="b64_json"
    )
    return response.data[0].b64_json

def main():
    try:
        title, content, image_prompt = generate_post_with_grok()

        print(f"Generating featured image with prompt: {image_prompt}")
        profile_b64 = generate_image(image_prompt + ", professional photography, high resolution, clean and bright")

        # Generate 3-5 additional images with variations
        photos_b64 = []
        for i in range(random.randint(3, 5)):
            variation_prompt = image_prompt + f", different angle {i+1}, professional cleaning scene in Mobile AL home or office"
            b64 = generate_image(variation_prompt)
            photos_b64.append(b64)

        # Safe slug generation
        slug = re.sub(r'[^a-z0-9]+', '-', title.lower())
        slug = re.sub(r'-+', '-', slug)
        slug = slug.strip('-')[:80]

        post = {
            "id": str(uuid.uuid4()),
            "name": title,
            "description": content,
            "profile": profile_b64,          # base64 string
            "photos": photos_b64,            # list of base64 strings
            "slug": slug,
            "created_at": "now()"
        }

        result = supabase.table("services").insert(post).execute()
        if result.data:
            print(f"SUCCESS! Published: {title}")
            print(f"Character count: {len(title)} (ideal 50-60 for full Google display)")
            print(f"Featured image generated and attached (base64)")
            print(f"{len(photos_b64)} additional AI-generated images attached")
            print(f"URL: https://www.zoiriscleaningservices.com/blog/blog/{slug}")
        else:
            print("Insert failed:", result)

    except Exception as e:
        print("ERROR:", str(e))
        raise

if __name__ == "__main__":
    main()
