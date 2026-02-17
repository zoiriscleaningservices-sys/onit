import os
import re
from pathlib import Path

def fix_mismatched_canonicals():
    print("Fixing mismatched canonical tags...")
    
    base_url = "https://www.zoiriscleaningservices.com"
    base_dir = Path('.')
    
    # Define the specific fixes needed based on audit results
    corrections = {
        "blog/index.html": "/blog/",
        "Gallery/index.html": "/Gallery/",
        "services/airbnb-cleaning/index.html": "/services/airbnb-cleaning/",
        "services/carpet-cleaning/index.html": "/services/carpet-cleaning/",
        "services/commercial-cleaning/index.html": "/services/commercial-cleaning/",
        "services/deep-cleaning/index.html": "/services/deep-cleaning/",
        "services/Detailing-Mobile-AL/index.html": "/services/Detailing-Mobile-AL/",
        "services/house-cleaning/index.html": "/services/house-cleaning/",
        "services/laundry-services/index.html": "/services/laundry-services/",
        "services/move-in-cleaning/index.html": "/services/move-in-cleaning/",
        "services/move-out-cleaning/index.html": "/services/move-out-cleaning/",
        "services/post-construction-cleanup/index.html": "/services/post-construction-cleanup/",
        "services/pressure-washing/index.html": "/services/pressure-washing/",
        "services/vacation-rental-cleaning/index.html": "/services/vacation-rental-cleaning/",
        "services/window-cleaning/index.html": "/services/window-cleaning/",
        "apple-touch-icon.png": None, # Ignore non-html
        "apply/index.html": "/apply/"
    }
    
    fixed_count = 0
    
    for rel_path, correct_suffix in corrections.items():
        if correct_suffix is None: continue
        
        file_path = base_dir / rel_path
        if not file_path.exists():
            print(f"  [SKIPPED] {rel_path} not found.")
            continue
            
        content = file_path.read_text(encoding='utf-8', errors='ignore')
        
        # Regex to find the canonical link tag and its href
        # This handles both href before rel and rel before href
        pattern = r'(<link [^>]*rel="canonical"[^>]*href=")([^"]+)("[^>]*>)|(<link [^>]*href=")([^"]+)("[^>]*rel="canonical"[^>]*>)'
        
        correct_url = f"{base_url}{correct_suffix}"
        
        def replace_func(match):
            if match.group(1): # Pattern with rel before href
                return f'{match.group(1)}{correct_url}{match.group(3)}'
            else: # Pattern with href before rel
                return f'{match.group(4)}{correct_url}{match.group(6)}'
        
        new_content = re.sub(pattern, replace_func, content)
        
        if new_content != content:
            file_path.write_text(new_content, encoding='utf-8')
            print(f"  [FIXED] {rel_path} -> {correct_url}")
            fixed_count += 1
        else:
            # Check if it was already correct or if regex failed
            if f'href="{correct_url}"' in content or f"href='{correct_url}'" in content:
                print(f"  [OK] {rel_path} already correct.")
            else:
                print(f"  [FAILED] Could not find canonical tag in {rel_path}")

    print(f"\nDone. Fixed {fixed_count} canonical tags.")

if __name__ == '__main__':
    fix_mismatched_canonicals()
