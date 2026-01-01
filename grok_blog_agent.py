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

# Large pool of high-quality, royalty-free cleaning images (Pexels + Unsplash)
IMAGE_POOL = [
# Original strong Pexels/Unsplash cleaning shots
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
    # ... (all your previous ones remain)

    # New fresh professional cleaning images
    "https://lisasnatural.com/wp-content/uploads/2017/12/move-out-cleaning-services.jpg",
    "https://freshspacecleaning.com/wp-content/uploads/2023/02/benefits-move-inmove-out-cleaning-service-1-1024x576.png",
    "https://www.premierjanitors.com/wp-content/uploads/2025/02/Commercial-Cleaning-Services-Mobile-Baldwin-County-AL.jpg",
    "https://momentumbsla.com/wp-content/uploads/2022/03/post-construction-cleaning-01-res.jpg",
    "https://steamcommander.com/wp-content/uploads/2024/08/Steam-Commnader-Steam-Cleaning.jpg",
    "https://lakesidefacilityservices.com/wp-content/uploads/2023/04/window-1-1024x535.jpg",
    "https://www.calltaylorspowerwashing.com/fbm-data/images/services/soft-washing.jpg",
    "https://media-cldnry.s-nbcnews.com/image/upload/t_fit-560w,f_auto,q_auto:best/rockcms/2024-04/240415-eco-friendly-cleaning-bd-social-4a72ba.jpg",
    "https://media.cnn.com/api/v1/images/stellar/prod/200918150934-03-hurricane-sally-0917.jpg?q=w_3000,h_1868,x_0,y_0,c_fill",
    "https://www.al.com/resizer/v2/HOPW5OUCRJDZXI2OI44KUKPV5U.jpg?auth=161fc3c61cb5b139fbcd45810d9e1dd3550b077608d8d904cb9061ec268f06bb&width=1280&smart=true&quality=90",

    # Add dozens more high-res ones here (all direct, visible URLs)
    "https://www.leticiascleaning.com/wp-content/uploads/2022/02/move-in-move-out-cleaning-V2.png",
    "https://www.portland-cleaning.com/wp-content/uploads/2022/11/Move-Out-Cleaning-Company-Portland-OR.jpg",
    "https://thefacilitiesgroup.com/wp-content/uploads/2023/10/Post-Construction-Clean-up-SS-scaled.jpg",
    "https://imperialcleaning.com/wp-content/uploads/2019/03/Post-Construction-Cleaning-Services.jpg",
    "https://www.advancedcarpetcleaningbcs.com/wp-content/uploads/2024/07/professional-carpet-steam-cleaning-5-640x480.png",
    "https://evergreencleans.com/wp-content/uploads/2021/03/Window-Cleaning-Post-Falls.png",
    "https://skbuildingservices.com/wp-content/uploads/2023/02/Exterior-window-cleaning-tools-scaled-1.jpeg",
    "https://campcpw.com/wp-content/uploads/2023/02/pressure-washing-in-mobile-alabama-1.jpeg",
    "https://formulacorp.com/wp-content/uploads/2014/07/Private-label-all-natural-cleaning-products-1-800x549.png",
    "https://www.reviewed.com/home-outdoors/features/9-benefits-of-switching-to-natural-or-green-cleaners",
    # Continue adding all the strong ones from searches...
]

def generate_post_with_grok():
    response = client.chat.completions.create(
        model="grok-4",
        messages=[
            {"role": "system", "content": "You are an expert local blogger writing helpful, high-value content for Zoiris Cleaning Services in Mobile, AL. Write ONE completely unique, long (1000-1500 words), genuinely useful blog post on a specific cleaning topic relevant to Mobile residents and businesses. Title: catchy, helpful, and keyword-rich but natural and SHORT (under 60 characters). Primary focus keywords (use naturally, 8-12 times total across the post): cleaning services Mobile AL, house cleaning Mobile Alabama, professional cleaners Mobile AL, deep cleaning Mobile AL, move in move out cleaning Mobile AL, commercial cleaning Mobile AL, eco-friendly cleaning Mobile Alabama. Do NOT stuff keywords or list services unnaturally. Instead, provide real value with sections, practical tips, local Mobile-specific advice (humidity, mold prevention, hurricane recovery, salt air, pollen), benefits of professional help, and real-world examples. Mention Zoiris Cleaning Services naturally as the trusted local expert. End with a soft, helpful CTA: Call **(251) 930-8621** or email zoiriscleaningservices@gmail.com for a free quote. Use **bold** sparingly for key phrases only. Output ONLY JSON: {\"title\": \"string\", \"content\": \"string with \\n for new lines\"}"},
            {"role": "user", "content": "Generate a fresh, unique, helpful blog post on a new cleaning-related topic tailored for Mobile, AL homes and businesses."}
        ],
        response_format={"type": "json_object"},
        temperature=1.0
    )
    data = json.loads(response.choices[0].message.content)
    return data["title"], data["content"]

def main():
    try:
        title, content = generate_post_with_grok()

        # Safe, clean slug
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
            print(f"Characters in title: {len(title)} (Google-friendly)")
            print(f"URL: https://www.zoiriscleaningservices.com/blog/blog/{slug}")
        else:
            print("Insert failed:", result)

    except Exception as e:
        print("ERROR:", str(e))
        raise

if __name__ == "__main__":
    main()
