import xml.etree.ElementTree as ET
from pathlib import Path
import re

def check_indexing_readiness():
    print("=" * 70)
    print("GOOGLE SEARCH CONSOLE (GSC) INDEXING READINESS REPORT")
    print("=" * 70)
    
    # 1. Check Sitemap vs Filesystem
    tree = ET.parse('sitemap.xml')
    root = tree.getroot()
    ns = {'sm': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
    
    sitemap_locs = [url.find('sm:loc', ns).text for url in root.findall('.//sm:url', ns)]
    sitemap_paths = {loc.replace('https://www.zoiriscleaningservices.com', '').strip('/') for loc in sitemap_locs}
    
    base_dir = Path('.')
    html_files = list(base_dir.glob('**/index.html'))
    excluded_dirs = {'.git', '.github', 'upload', 'favicon', 'tmp', '.gemini'}
    
    valid_html_files = []
    for f in html_files:
        if not any(ex in str(f) for ex in excluded_dirs):
            valid_html_files.append(f)
            
    print(f"\n[SITEMAP COVERAGE]")
    print(f"Total valid HTML files found: {len(valid_html_files)}")
    print(f"Total entries in sitemap: {len(sitemap_locs)}")
    
    missing_from_sitemap = []
    for f in valid_html_files:
        rel_path = str(f.parent).replace('\\', '/').strip('./').strip('/')
        if rel_path == '.' or rel_path == '':
            rel_path = ''
        
        if rel_path not in sitemap_paths:
            missing_from_sitemap.append(rel_path)
            
    if missing_from_sitemap:
        print(f"\n[WARNING] Found {len(missing_from_sitemap)} pages missing from sitemap:")
        for m in sorted(missing_from_sitemap):
            print(f"  - /{m}/")
    else:
        print("\n[OK] All valid HTML files are present in the sitemap.")

    # 2. Meta Tag Check on Sample Pages
    print(f"\n[META TAG & CANONICAL CHECK]")
    samples = {
        "Homepage": "index.html",
        "About": "about/index.html",
        "Semmes Location": "semmes/index.html",
        "Deep Cleaning Service": "services/deep-cleaning/index.html",
        "Semmes Deep Cleaning": "semmes/deep-cleaning/index.html"
    }
    
    for name, path in samples.items():
        file_path = Path(path)
        if not file_path.exists():
            print(f"  {name}: File {path} not found.")
            continue
            
        content = file_path.read_text(encoding='utf-8', errors='ignore')
        
        # Check canonical
        canonical = re.search(r'<link rel="canonical" href="([^"]+)"', content)
        # Check robots
        robots = re.search(r'<meta name="robots" content="([^"]+)"', content)
        
        print(f"  {name} ({path}):")
        if canonical:
            print(f"    Canonical: {canonical.group(1)}")
        else:
            print(f"    [MISSING] Canonical tag")
            
        if robots:
            print(f"    Robots: {robots.group(1)}")
            if "noindex" in robots.group(1).lower():
                print(f"    [CRITICAL] Page is set to NOINDEX")
        else:
            print(f"    [MISSING] Meta robots tag (Defaults to index, follow)")
            
    # 3. Check Sitemap XML structure for loc encoding etc
    print(f"\n[SITEMAP VALIDITY]")
    invalid_urls = [loc for loc in sitemap_locs if not loc.startswith('https://')]
    if invalid_urls:
        print(f"  [ERROR] Found {len(invalid_urls)} invalid URLs in sitemap.")
    else:
        print(f"  [OK] All sitemap URLs use HTTPS and are absolute.")

check_indexing_readiness()
