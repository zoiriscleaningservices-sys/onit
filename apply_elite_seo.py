import os
import re
import glob

ROOT_DIR = r"c:\Users\lucia\OneDrive\Desktop\ZOIRISCLEANING"

# Let's map cities and services to readable formats based on their slugs
def format_name(slug):
    # Capitalize words, remove hyphens
    words = slug.split('-')
    return ' '.join(w.capitalize() for w in words)

def get_page_info(filepath):
    """Determine location and service from the filepath."""
    rel_path = os.path.relpath(filepath, ROOT_DIR)
    parts = rel_path.split(os.sep)
    
    if len(parts) == 1 and parts[0] == 'index.html':
        return {"type": "home", "location": "Mobile, AL", "service": "Cleaning"}
        
    if len(parts) == 2 and parts[1] == 'index.html':
        loc_slug = parts[0]
        return {"type": "location_hub", "location": format_name(loc_slug), "service": "Cleaning"}
        
    if len(parts) == 3 and parts[2] == 'index.html':
        loc_slug = parts[0]
        srv_slug = parts[1]
        
        # Handle the special Detailing-Mobile-AL case
        if srv_slug.lower() == 'detailing-mobile-al':
            srv_slug = 'Detailing'
            
        return {"type": "service", "location": format_name(loc_slug), "service": format_name(srv_slug)}
        
    return None

def generate_seo_content(info):
    loc = info["location"]
    srv = info["service"]
    
    if info["type"] == "home":
        title = f"#1 Cleaning Service in Mobile, AL | Top-Rated Maid Services | Zoiris"
        desc = f"Looking for the best cleaning service in Mobile, AL? Zoiris Cleaning Services offers top-notch, highly-rated house cleaning and commercial cleaning. Call (251) 930-8621 for a free quote!"
        h1 = f"Top-Rated Cleaning Service in Mobile, AL"
    elif info["type"] == "location_hub":
        title = f"#1 {loc} Cleaning Service | Top-Rated Cleaners | Zoiris"
        desc = f"Need a trusted cleaning service in {loc}? Zoiris Cleaning offers the highest-rated residential and commercial cleaning in {loc}. Fast, affordable, and spotless. Call (251) 930-8621 today!"
        h1 = f"Expert Cleaning Services in {loc}"
    else: # service
        # If the service already has "cleaning" in it, don't duplicate
        srv_name = srv if "Cleaning" in srv else f"{srv} Cleaning"
        title = f"Best {srv_name} in {loc} | 5-Star Rated | Zoiris Cleaning"
        desc = f"Looking for professional {srv_name.lower()} in {loc}? We are the #1 rated local experts. Affordable, reliable, and guaranteed spotless. Call (251) 930-8621 for a free estimate!"
        h1 = f"Professional {srv_name} in {loc}"
        
    return title, desc, h1

def process_file(filepath):
    info = get_page_info(filepath)
    if not info:
        return False
        
    title, desc, h1 = generate_seo_content(info)
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"Error reading {filepath}: {e}")
        return False

    original_content = content
    
    # 1. Update Title
    # <title>...</title>
    title_pattern = re.compile(r'<title>.*?</title>', re.IGNORECASE | re.DOTALL)
    if title_pattern.search(content):
        content = title_pattern.sub(f'<title>{title}</title>', content)
    else:
        # Inject title before </head> if missing
        content = content.replace('</head>', f'  <title>{title}</title>\n</head>')

    # 2. Update Description
    # We want to match existing meta description or add a new one
    desc_pattern = re.compile(r'<meta[^>]*name=["\']description["\'][^>]*>', re.IGNORECASE)
    new_desc_tag = f'<meta name="description" content="{desc}">'
    if desc_pattern.search(content):
        content = desc_pattern.sub(new_desc_tag, content)
    else:
        # Inject description before </head>
        content = content.replace('</head>', f'  {new_desc_tag}\n</head>')

    # 3. Update H1
    # Find the H1 tag and replace its contents.
    # From index.html we saw: <h1 class="text-4xl md:text-5xl font-extrabold drop-shadow"></h1>
    # We will match <h1 ...>...</h1> and ensure it contains our h1 string.
    h1_pattern = re.compile(r'(<h1[^>]*>)(.*?)(</h1>)', re.IGNORECASE | re.DOTALL)
    
    def repl_h1(match):
        return f"{match.group(1)}{h1}{match.group(3)}"
        
    if h1_pattern.search(content):
        content = h1_pattern.sub(repl_h1, content)
        
    # Ensure changes occurred, then write back
    if content != original_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

def main():
    print("Starting Elite SEO Overhaul...")
    # exclude some dirs
    exclude = ['.git', '.github', 'tmp', '.gemini', 'upload', 'favicon', 'Gallery', 'about', 'contact', 'blog', 'apply']
    count = 0
    updated = 0
    
    for root, dirs, files in os.walk(ROOT_DIR):
        # Exclude directories inline
        dirs[:] = [d for d in dirs if d not in exclude]
        
        for file in files:
            if file.lower() == 'index.html':
                filepath = os.path.join(root, file)
                count += 1
                if process_file(filepath):
                    updated += 1
                    
    print(f"Processed {count} files. Updated {updated} files.")
    
if __name__ == "__main__":
    main()
