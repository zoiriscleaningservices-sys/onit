import json
import time
import random
import uuid
import re
import urllib.request
import os

# Your xAI API key (get from https://x.ai/api)
XAI_API_KEY = os.getenv('XAI_API_KEY')  # Set this environment variable 

# Supabase details from the HTML
SUPABASE_URL = 'https://dwxbzltxsdeshmmtcycv.supabase.co'
SUPABASE_ANON_KEY = 'sb_publishable_4PWdqRYFR0E-tp-OjdTP3Q_S_5qvRbp'

# List of free stock image URLs from Unsplash (related to cleaning services)
IMAGE_URLS = [
    'https://images.unsplash.com/premium_photo-1663047397245-2ddad26c5dd7?fm=jpg&q=60&w=3000&ixlib=rb-4.1.0',
    'https://images.unsplash.com/photo-1686178827149-6d55c72d81df?fm=jpg&q=60&w=3000&ixlib=rb-4.1.0',
    'https://images.unsplash.com/photo-1740657254989-42fe9c3b8cce?fm=jpg&q=60&w=3000&ixlib=rb-4.1.0',
    'https://images.unsplash.com/photo-1585421514284-efb74c2b69ba?fm=jpg&q=60&w=3000&ixlib=rb-4.1.0',
    'https://images.unsplash.com/photo-1603712725038-e9334ae8f39f?fm=jpg&q=60&w=3000&ixlib=rb-4.1.0',
    'https://images.unsplash.com/photo-1482449609509-eae2a7ea42b7?fm=jpg&q=60&w=3000&ixlib=rb-4.1.0',
    'https://images.unsplash.com/photo-1581578731548-c64695cc6952?fm=jpg&q=60&w=3000&ixlib=rb-4.1.0',
    'https://images.unsplash.com/photo-1437326300822-01d8f13c024f?fm=jpg&q=60&w=3000&ixlib=rb-4.1.0',
    'https://images.unsplash.com/photo-1642505172378-a6f5e5b15580?fm=jpg&q=60&w=3000&ixlib=rb-4.1.0',
    'https://images.unsplash.com/photo-1563453392212-326f5e854473?fm=jpg&q=60&w=3000&ixlib=rb-4.1.0'
]

def generate_blog_post():
    prompt = """
    Generate a unique blog post title and content about a random topic related to cleaning services for Zoiris Cleaning Services in Mobile, AL. 
    Optimize for SEO by including keywords like 'cleaning services Mobile AL', 'house cleaning Mobile Alabama', 'professional cleaners in Mobile', 'commercial cleaning Mobile AL', etc., naturally throughout the post.
    Include the phone number (251) 930-8621 and email zoiriscleaningservices@gmail.com in the content as a call to action at the end.
    Use markdown syntax like **bold** or __underline__ for keywords where appropriate.
    The content should be 400-600 words, engaging, informative, and focused on Mobile, AL aspects (e.g., local weather, landmarks, community).
    Format the output exactly as:
    Title: [Your Title Here]
    
    Content: [Your Full Content Here]
    """
    
    request_data = {
        "model": "grok-4",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7,
        "max_tokens": 1024
    }
    
    req = urllib.request.Request(
        "https://api.x.ai/v1/chat/completions",
        data=json.dumps(request_data).encode('utf-8'),
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {XAI_API_KEY}"
        },
        method="POST"
    )
    
    with urllib.request.urlopen(req) as response:
        result = json.loads(response.read().decode('utf-8'))
        generated_text = result['choices'][0]['message']['content']
    
    # Parse title and content
    lines = generated_text.split('\n')
    title = lines[0].replace('Title: ', '').strip()
    content = '\n'.join(lines[2:]).strip()  # Skip the 'Content:' line
    
    return title, content

def post_to_supabase(title, content):
    # Generate slug
    slug = re.sub(r'[^a-z0-9-]', '', title.lower().replace(' ', '-'))[:80]
    
    # Select random featured image
    profile_url = random.choice(IMAGE_URLS)
    
    # Select 0-3 random gallery images
    num_gallery = random.randint(0, 3)
    photos_urls = random.sample(IMAGE_URLS, num_gallery) if num_gallery > 0 else None
    
    post_data = {
        "id": str(uuid.uuid4()),
        "created_at": time.strftime("%Y-%m-%dT%H:%M:%S.%fZ", time.gmtime()),
        "name": title,
        "description": content,
        "profile": profile_url,
        "photos": photos_urls,
        "slug": slug
    }
    
    req = urllib.request.Request(
        f"{SUPABASE_URL}/rest/v1/services",
        data=json.dumps(post_data).encode('utf-8'),
        headers={
            "apikey": SUPABASE_ANON_KEY,
            "Authorization": f"Bearer {SUPABASE_ANON_KEY}",
            "Content-Type": "application/json",
            "Prefer": "return=minimal"
        },
        method="POST"
    )
    
    with urllib.request.urlopen(req) as response:
        if response.status == 201:
            print(f"Successfully posted: {title}")
        else:
            print(f"Error posting: {response.status}")

if __name__ == "__main__":
    if not XAI_API_KEY:
        print("Please set the XAI_API_KEY environment variable.")
    else:
        while True:
            try:
                title, content = generate_blog_post()
                post_to_supabase(title, content)
                print("Waiting 5 minutes for next post...")
                time.sleep(300)  # 5 minutes
            except Exception as e:
                print(f"Error: {e}")
                time.sleep(60)  # Retry after 1 minute if error
