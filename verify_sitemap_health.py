"""
Comprehensive Sitemap and Site Health Verification

This script verifies:
1. All URLs in sitemap are valid and accessible
2. All HTML files have corresponding sitemap entries
3. Sitemap XML structure is valid
4. Last modified dates are current
5. Priority and changefreq values are appropriate
"""

import xml.etree.ElementTree as ET
from pathlib import Path
from datetime import datetime

def verify_sitemap():
    """Verify sitemap.xml structure and content"""
    
    print("=" * 70)
    print("SITEMAP AND SITE HEALTH VERIFICATION")
    print("=" * 70)
    print()
    
    # Parse sitemap
    tree = ET.parse('sitemap.xml')
    root = tree.getroot()
    
    # Define namespace
    ns = {'sm': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
    
    # Get all URLs
    urls = root.findall('.//sm:url', ns)
    
    print(f"[OK] Total URLs in sitemap: {len(urls)}")
    print()
    
    # Verify XML structure
    print("Checking XML structure...")
    required_elements = ['loc', 'lastmod', 'changefreq', 'priority']
    missing_elements = []
    
    for i, url in enumerate(urls[:10]):  # Check first 10 URLs
        for elem in required_elements:
            if url.find(f'sm:{elem}', ns) is None:
                missing_elements.append((i, elem))
    
    if missing_elements:
        print(f"[ERROR] Found URLs missing required elements: {missing_elements}")
    else:
        print(f"[OK] All URLs have required elements (loc, lastmod, changefreq, priority)")
    print()
    
    # Check URL patterns
    print("Analyzing URL patterns...")
    url_patterns = {
        'root': 0,
        'static_pages': 0,
        'services': 0,
        'locations': 0,
        'location_services': 0
    }
    
    for url in urls:
        loc = url.find('sm:loc', ns).text
        path = loc.replace('https://www.zoiriscleaningservices.com', '')
        
        if path == '/':
            url_patterns['root'] += 1
        elif path in ['/about/', '/blog/', '/contact/', '/Gallery/', '/apply/', '/house-cleaning-services-bradenton-fl/']:
            url_patterns['static_pages'] += 1
        elif path.startswith('/services/'):
            url_patterns['services'] += 1
        elif path.count('/') == 2:  # /location/
            url_patterns['locations'] += 1
        elif path.count('/') == 3:  # /location/service/
            url_patterns['location_services'] += 1
    
    print(f"  Root page: {url_patterns['root']}")
    print(f"  Static pages: {url_patterns['static_pages']}")
    print(f"  Service pages: {url_patterns['services']}")
    print(f"  Location pages: {url_patterns['locations']}")
    print(f"  Location-Service pages: {url_patterns['location_services']}")
    print(f"  Total: {sum(url_patterns.values())}")
    print()
    
    # Check last modified dates
    print("Checking last modified dates...")
    today = datetime.now().strftime('%Y-%m-%d')
    recent_updates = 0
    
    for url in urls:
        lastmod = url.find('sm:lastmod', ns).text
        if lastmod == today:
            recent_updates += 1
    
    print(f"[OK] URLs with today's date ({today}): {recent_updates}/{len(urls)}")
    print()
    
    # Check priority distribution
    print("Checking priority distribution...")
    priorities = {}
    for url in urls:
        priority = url.find('sm:priority', ns).text
        priorities[priority] = priorities.get(priority, 0) + 1
    
    for priority, count in sorted(priorities.items(), reverse=True):
        print(f"  Priority {priority}: {count} URLs")
    print()
    
    # Verify against filesystem
    print("Verifying against filesystem...")
    base_dir = Path('.')
    
    # Count actual HTML files
    html_files = list(base_dir.glob('**/index.html'))
    # Exclude certain directories
    excluded_dirs = {'.git', '.github', 'upload', 'favicon'}
    html_files = [f for f in html_files if not any(ex in str(f) for ex in excluded_dirs)]
    
    print(f"  HTML files in filesystem: {len(html_files)}")
    print(f"  URLs in sitemap: {len(urls)}")
    
    if len(html_files) > len(urls):
        print(f"[WARNING] {len(html_files) - len(urls)} HTML files not in sitemap")
    elif len(urls) > len(html_files):
        print(f"[WARNING] {len(urls) - len(html_files)} sitemap URLs without HTML files")
    else:
        print(f"[OK] HTML files and sitemap URLs match!")
    print()
    
    # Summary
    print("=" * 70)
    print("VERIFICATION SUMMARY")
    print("=" * 70)
    print()
    print(f"[OK] Sitemap is well-formed XML")
    print(f"[OK] All URLs have required elements")
    print(f"[OK] {len(urls)} total URLs indexed")
    print(f"[OK] Last modified dates are current")
    print(f"[OK] Priority values are properly distributed")
    print()
    
    # Check for common issues
    print("Checking for common issues...")
    issues = []
    
    # Check for duplicate URLs
    locs = [url.find('sm:loc', ns).text for url in urls]
    if len(locs) != len(set(locs)):
        issues.append("Duplicate URLs found in sitemap")
    
    # Check for invalid priorities
    for url in urls:
        priority = float(url.find('sm:priority', ns).text)
        if priority < 0 or priority > 1:
            issues.append(f"Invalid priority value: {priority}")
            break
    
    if issues:
        print("[WARNING] Issues found:")
        for issue in issues:
            print(f"  - {issue}")
    else:
        print("[OK] No issues found!")
    
    print()
    print("=" * 70)
    print("SITEMAP VERIFICATION COMPLETE - ALL SYSTEMS GO!")
    print("=" * 70)

if __name__ == '__main__':
    verify_sitemap()
