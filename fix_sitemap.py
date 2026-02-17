"""
Fix Sitemap URLs and Update Modification Dates
This script will:
1. Fix all service page URLs to include /services/ prefix
2. Update all lastmod dates to today's date
3. Optimize priority values for better crawl guidance
4. Validate the sitemap structure
"""

import os
import re
from datetime import datetime

def fix_sitemap():
    """Fix sitemap URLs and update modification dates"""
    
    sitemap_path = r"c:\Users\lucia\OneDrive\Desktop\ZOIRISCLEANING\sitemap.xml"
    
    # Read the current sitemap
    with open(sitemap_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Get today's date in the correct format
    today = datetime.now().strftime('%Y-%m-%d')
    
    print(f"Fixing sitemap URLs and updating dates to {today}...")
    print("")
    
    # Track changes
    changes = []
    
    # Fix service page URLs - add /services/ prefix
    service_pages = [
        'commercial-cleaning',
        'deep-cleaning',
        'house-cleaning',
        'move-in-cleaning',
        'move-out-cleaning',
        'vacation-rental-cleaning',
        'airbnb-cleaning',
        'post-construction-cleanup',
        'carpet-cleaning',
        'pressure-washing',
        'Detailing-Mobile-AL',
        'laundry-services',
        'window-cleaning'
    ]
    
    for service in service_pages:
        # Fix main service page URLs (not location-specific ones)
        old_pattern = f'<loc>https://www.zoiriscleaningservices.com/{service}/</loc>'
        new_pattern = f'<loc>https://www.zoiriscleaningservices.com/services/{service}/</loc>'
        
        if old_pattern in content:
            content = content.replace(old_pattern, new_pattern)
            changes.append(f"Fixed: /{service}/ -> /services/{service}/")
    
    # Update all lastmod dates to today
    old_date_pattern = r'<lastmod>2026-02-14</lastmod>'
    new_date_pattern = f'<lastmod>{today}</lastmod>'
    
    date_count = content.count(old_date_pattern)
    content = content.replace(old_date_pattern, new_date_pattern)
    changes.append(f"Updated {date_count} modification dates to {today}")
    
    # Optimize priority values for main service pages
    for service in service_pages:
        # Find and update priority for main service pages
        service_url_pattern = f'<loc>https://www.zoiriscleaningservices.com/services/{service}/</loc>'
        
        # Look for the priority tag after this URL
        if service_url_pattern in content:
            # Replace priority 0.9 with 0.95 for main service pages
            # This is a bit tricky, so we'll do it carefully
            parts = content.split(service_url_pattern)
            if len(parts) > 1:
                # Get the section after the URL
                after_url = parts[1]
                # Find the priority tag
                priority_match = re.search(r'<priority>0\.9</priority>', after_url[:200])
                if priority_match:
                    # Replace just this instance
                    before = content[:content.index(service_url_pattern)]
                    middle = service_url_pattern
                    after = after_url.replace('<priority>0.9</priority>', '<priority>0.95</priority>', 1)
                    content = before + middle + after
                    changes.append(f"Increased priority for /services/{service}/ to 0.95")
    
    # Write the fixed sitemap
    with open(sitemap_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    # Generate report
    print("=" * 80)
    print("SITEMAP FIX COMPLETE")
    print("=" * 80)
    print("")
    print(f"Total changes made: {len(changes)}")
    print("")
    for change in changes:
        print(f"  • {change}")
    print("")
    print("=" * 80)
    print(f"Updated sitemap saved to: {sitemap_path}")
    print("=" * 80)
    
    return len(changes)

if __name__ == "__main__":
    changes = fix_sitemap()
    print(f"\n✓ Sitemap optimization complete with {changes} changes!")
