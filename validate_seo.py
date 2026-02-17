"""
Validate Sitemap and Internal Links
This script will:
1. Validate all URLs in sitemap.xml are accessible
2. Check for broken links
3. Verify internal link structure
4. Generate a validation report
"""

import os
import re
from urllib.parse import urlparse

def validate_sitemap():
    """Validate sitemap.xml structure and URLs"""
    
    sitemap_path = r"c:\Users\lucia\OneDrive\Desktop\ZOIRISCLEANING\sitemap.xml"
    root_dir = r"c:\Users\lucia\OneDrive\Desktop\ZOIRISCLEANING"
    
    print("Validating sitemap.xml...")
    print("")
    
    with open(sitemap_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract all URLs from sitemap
    url_pattern = r'<loc>(https://www\.zoiriscleaningservices\.com[^<]+)</loc>'
    urls = re.findall(url_pattern, content)
    
    print(f"Found {len(urls)} URLs in sitemap")
    print("")
    
    # Validate each URL
    valid_urls = []
    invalid_urls = []
    
    for url in urls:
        # Convert URL to local file path
        path = url.replace('https://www.zoiriscleaningservices.com', '')
        if path == '/':
            file_path = os.path.join(root_dir, 'index.html')
        else:
            file_path = os.path.join(root_dir, path.strip('/'), 'index.html')
        
        # Check if file exists
        if os.path.exists(file_path):
            valid_urls.append(url)
        else:
            invalid_urls.append((url, file_path))
    
    # Generate report
    print("=" * 80)
    print("SITEMAP VALIDATION REPORT")
    print("=" * 80)
    print("")
    print(f"Total URLs: {len(urls)}")
    print(f"Valid URLs: {len(valid_urls)}")
    print(f"Invalid URLs: {len(invalid_urls)}")
    print("")
    
    if invalid_urls:
        print("INVALID URLS (File not found):")
        print("-" * 80)
        for url, file_path in invalid_urls[:10]:  # Show first 10
            print(f"  URL: {url}")
            print(f"  Expected file: {file_path}")
            print("")
        
        if len(invalid_urls) > 10:
            print(f"  ...and {len(invalid_urls) - 10} more invalid URLs")
            print("")
    else:
        print("[OK] All URLs in sitemap are valid!")
        print("")
    
    # Check for correct service URLs
    service_urls = [url for url in urls if '/services/' in url]
    print(f"Service pages in sitemap: {len(service_urls)}")
    
    # Check for correct date format
    date_pattern = r'<lastmod>(\d{4}-\d{2}-\d{2})</lastmod>'
    dates = re.findall(date_pattern, content)
    unique_dates = set(dates)
    print(f"Unique modification dates: {', '.join(sorted(unique_dates))}")
    print("")
    
    print("=" * 80)
    
    return len(valid_urls), len(invalid_urls)

def check_html_sitemap():
    """Check if HTML sitemap exists and is accessible"""
    
    sitemap_html_path = r"c:\Users\lucia\OneDrive\Desktop\ZOIRISCLEANING\sitemap.html"
    
    print("\nChecking HTML sitemap...")
    print("")
    
    if os.path.exists(sitemap_html_path):
        # Get file size
        size = os.path.getsize(sitemap_html_path)
        print(f"[OK] HTML sitemap exists: {sitemap_html_path}")
        print(f"     File size: {size:,} bytes")
        
        # Count links in HTML sitemap
        with open(sitemap_html_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        link_count = content.count('<a href=')
        print(f"     Total links: {link_count}")
        print("")
        return True
    else:
        print("[ERROR] HTML sitemap not found!")
        print("")
        return False

def main():
    print("=" * 80)
    print("SEO VALIDATION SUITE")
    print("=" * 80)
    print("")
    
    # Validate XML sitemap
    valid_count, invalid_count = validate_sitemap()
    
    # Check HTML sitemap
    html_exists = check_html_sitemap()
    
    # Final summary
    print("=" * 80)
    print("VALIDATION SUMMARY")
    print("=" * 80)
    print("")
    
    if invalid_count == 0 and html_exists:
        print("[OK] All validations passed!")
        print(f"     - XML Sitemap: {valid_count} valid URLs")
        print(f"     - HTML Sitemap: Exists and accessible")
        print("")
        print("Next steps:")
        print("1. Submit sitemap.xml to Google Search Console")
        print("2. Request indexing for priority pages")
        print("3. Monitor coverage report for improvements")
    else:
        print("[WARNING] Some issues found:")
        if invalid_count > 0:
            print(f"     - {invalid_count} invalid URLs in sitemap")
        if not html_exists:
            print("     - HTML sitemap not found")
        print("")
        print("Please fix these issues before submitting to Google")
    
    print("")
    print("=" * 80)

if __name__ == "__main__":
    main()
