"""
Remove Invalid URLs from Sitemap
This script removes URLs that don't have corresponding files
"""

import os
import re

def remove_invalid_urls():
    """Remove invalid URLs from sitemap.xml"""
    
    sitemap_path = r"c:\Users\lucia\OneDrive\Desktop\ZOIRISCLEANING\sitemap.xml"
    root_dir = r"c:\Users\lucia\OneDrive\Desktop\ZOIRISCLEANING"
    
    with open(sitemap_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # URLs to remove (found by validation)
    invalid_urls = [
        'https://www.zoiriscleaningservices.com/cleaning-services-midland-tx/',
        'https://www.zoiriscleaningservices.com/cleaning-services-bradenton-fl/',
        'https://www.zoiriscleaningservices.com/blog/beat-pollen-spring-cleaning-tips-for-mobile-al',
        'https://www.zoiriscleaningservices.com/blog/premier-cleaning-services-mobile-al-by-zoiris',
        'https://www.zoiriscleaningservices.com/blog/professional-cleaning-services-in-mobile-al-zoiris-cleaning-services',
        'https://www.zoiriscleaningservices.com/blog/commercial-cleaning-services-for-businesses-in-mobile-al',
        'https://www.zoiriscleaningservices.com/blog/top-residential-cleaning-services-in-mobile-al'
    ]
    
    removed_count = 0
    
    for url in invalid_urls:
        # Find and remove the entire <url> block for this URL
        # Pattern: <url>...</url> containing this specific URL
        pattern = r'<url>\s*<loc>' + re.escape(url) + r'</loc>.*?</url>\s*'
        
        if re.search(pattern, content, re.DOTALL):
            content = re.sub(pattern, '', content, flags=re.DOTALL)
            removed_count += 1
            print(f"Removed: {url}")
    
    # Write back to file
    with open(sitemap_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("")
    print("=" * 80)
    print(f"Removed {removed_count} invalid URLs from sitemap")
    print("=" * 80)
    
    return removed_count

if __name__ == "__main__":
    print("Cleaning up sitemap...")
    print("")
    remove_invalid_urls()
    print("")
    print("[OK] Sitemap cleanup complete!")
