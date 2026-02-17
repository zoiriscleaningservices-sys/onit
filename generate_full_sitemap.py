"""
Regenerate Sitemap.xml to ensure 100% coverage
"""

import os
from pathlib import Path
from datetime import datetime

base_url = "https://www.zoiriscleaningservices.com"
base_dir = Path('.')
today = datetime.now().strftime('%Y-%m-%d')

# Excluded patterns
excluded_dirs = {'.git', '.github', 'upload', 'favicon', 'tmp', '.gemini'}

def generate_sitemap():
    print("Generating complete sitemap.xml...")
    
    html_files = list(base_dir.glob('**/index.html'))
    
    urls = []
    for f in html_files:
        # Skip excluded directories
        if any(ex in str(f) for ex in excluded_dirs):
            continue
            
        rel_path = str(f.parent).replace('\\', '/').strip('./').strip('/')
        if rel_path == '':
            url = f"{base_url}/"
            priority = "1.0"
            changefreq = "weekly"
        else:
            url = f"{base_url}/{rel_path}/"
            # Prioritize services and main locations
            if rel_path.startswith('services/'):
                priority = "0.95"
                changefreq = "weekly"
            elif '/' not in rel_path: # Main location
                priority = "0.9"
                changefreq = "weekly"
            else: # Location-service or deeper
                priority = "0.8"
                changefreq = "monthly"
        
        urls.append({
            'loc': url,
            'lastmod': today,
            'changefreq': changefreq,
            'priority': priority
        })

    # Sort URLs for consistency
    urls.sort(key=lambda x: x['loc'])

    # Build XML
    xml = ['<?xml version="1.0" encoding="UTF-8"?>',
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">']
    
    for u in urls:
        xml.append('  <url>')
        xml.append(f"    <loc>{u['loc']}</loc>")
        xml.append(f"    <lastmod>{u['lastmod']}</lastmod>")
        xml.append(f"    <changefreq>{u['changefreq']}</changefreq>")
        xml.append(f"    <priority>{u['priority']}</priority>")
        xml.append('  </url>')
    
    xml.append('</urlset>')

    with open('sitemap.xml', 'w', encoding='utf-8') as f:
        f.write('\n'.join(xml))
    
    print(f"Sitemap generated with {len(urls)} URLs.")

if __name__ == '__main__':
    generate_sitemap()
