import os
import shutil
import re

# Template source
TEMPLATE_DIR = 'house-cleaning'
TEMPLATE_FILE = 'index.html'

services = [
    {
        "slug": "laundry-services",
        "title": "Laundry & Clothing Care Services",
        "h1": "Professional Laundry, Folding & Delivery Services",
        "desc": "Let ZOIRIS handle your laundry! We offer washing, folding, and clothing delivery services to save you time.",
        "content_intro": "Tired of piling laundry? Our **Laundry Services** take the hassle out of your week. We provide expert **washing, drying, and folding** services with optional pickup and delivery.",
        "bullets": [
             "Wash & Fold Service",
             "Clothing Delivery & Pickup",
             "Ironing & steaming",
             "Linens & Bedding",
             "Closet Organization"
        ]
    },
    {
        "slug": "window-cleaning",
        "title": "Professional Window Cleaning Services",
        "h1": "Crystal Clear Window Cleaning Services",
        "desc": "Streak-free window cleaning for homes and businesses. We clean interior and exterior windows, screens, and tracks.",
        "content_intro": "Brighten your space with our **Professional Window Cleaning**. We remove dirt, grime, and streaks from your windows, ensuring a crystal-clear view.",
        "bullets": [
             "Interior & Exterior Cleaning",
             "Screen Cleaning",
             "Track & Sill Detailed Cleaning",
             "Skylights & Glass Doors",
             "Post-Construction Window Scraping"
        ]
    }
]

def create_page(svc):
    target_dir = svc['slug']
    target_file = os.path.join(target_dir, 'index.html')
    
    # Create directory
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
        print(f"Created directory: {target_dir}")

    # Read template
    if not os.path.exists(os.path.join(TEMPLATE_DIR, TEMPLATE_FILE)):
        print(f"Template not found: {TEMPLATE_DIR}/{TEMPLATE_FILE}")
        return

    with open(os.path.join(TEMPLATE_DIR, TEMPLATE_FILE), 'r', encoding='utf-8') as f:
        content = f.read()

    # Replacements
    # Title
    content = re.sub(r'<title>.*?</title>', f'<title>{svc["title"]} | Zoiris Cleaning</title>', content)
    
    # H1 (Hero) - Assuming generic hero class or H1 tag
    # House cleaning might have "House Cleaning Services" hardcoded
    content = content.replace('House Cleaning', svc['title']) # Simple replace might be risky but effective for "House Cleaning"
    
    # Description
    content = re.sub(r'<meta name="description" content=".*?" />', f'<meta name="description" content="{svc["desc"]}" />', content)

    # Content Injection
    # We'll look for the first paragraph of content or specific section
    # This is a bit rough without a robust parser, but replacing the main intro text usually works if unique.
    # House cleaning likely has "Experience the joy of a spotless home..."
    
    # Let's try to replace the H2 and Intro paragraph in the "Services" section
    # <h2 ...> ... </h2>
    
    # Ideally, we write a specific block.
    # For now, simplistic string replacement for "House Cleaning" to "Laundry Services" gets us 80% there.
    # Then we append specific bullet points.
    
    # Refined replace:
    content = content.replace('House Cleaning', svc['title'].split(' Services')[0]) 
    content = content.replace('Cleaning Services for Homes', svc['title'])

    # Write file
    with open(target_file, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Generated: {target_file}")

# Execution
for svc in services:
    create_page(svc)
