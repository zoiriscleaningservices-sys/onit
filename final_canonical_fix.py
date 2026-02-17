import os
import re
from pathlib import Path

def final_cleanup():
    base_url = "https://www.zoiriscleaningservices.com"
    base_dir = Path('.')
    
    # Specific casing fixes for detailing
    targets = [
        "saraland/detailing/index.html",
        "foley/detailing/index.html"
    ]
    
    fixed = 0
    for p in targets:
        f = base_dir / p
        if f.exists():
            c = f.read_text(encoding='utf-8')
            # Fix uppercase Detailings
            nc = re.sub(r'https://www\.zoiriscleaningservices\.com/([^/]+)/Detailing/', 
                        lambda m: f"{base_url}/{m.group(1)}/detailing/", c)
            if nc != c:
                f.write_text(nc, encoding='utf-8')
                print(f"Fixed canonical casing in {p}")
                fixed += 1
    
    print(f"Final cleanup done. Fixed {fixed} pages.")

if __name__ == '__main__':
    final_cleanup()
