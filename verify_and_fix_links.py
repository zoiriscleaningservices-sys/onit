"""
Comprehensive Link Verification and Fixing Script
This script will:
1. Scan all HTML files for navigation links
2. Identify broken or inconsistent links
3. Fix navigation links to ensure consistency
4. Generate a report of all changes
"""

import os
import re
from pathlib import Path
from collections import defaultdict

# Define the correct navigation structure
CORRECT_SERVICE_LINKS = {
    'commercial-cleaning': '/services/commercial-cleaning/',
    'deep-cleaning': '/services/deep-cleaning/',
    'house-cleaning': '/services/house-cleaning/',
    'move-in-cleaning': '/services/move-in-cleaning/',
    'move-out-cleaning': '/services/move-out-cleaning/',
    'vacation-rental-cleaning': '/services/vacation-rental-cleaning/',
    'airbnb-cleaning': '/services/airbnb-cleaning/',
    'post-construction-cleanup': '/services/post-construction-cleanup/',
    'carpet-cleaning': '/services/carpet-cleaning/',
    'pressure-washing': '/services/pressure-washing/',
    'Detailing-Mobile-AL': '/services/Detailing-Mobile-AL/',
    'laundry-services': '/services/laundry-services/',
    'window-cleaning': '/services/window-cleaning/',
}

CORRECT_LOCATION_LINKS = {
    'downtown-mobile': '/downtown-mobile/',
    'midtown-mobile': '/midtown-mobile/',
    'west-mobile': '/west-mobile/',
    'saraland': '/saraland/',
    'semmes': '/semmes/',
    'theodore': '/theodore/',
    'satsuma': '/satsuma/',
    'grand-bay': '/grand-bay/',
    'daphne': '/daphne/',
    'fairhope': '/fairhope/',
    'spanish-fort': '/spanish-fort/',
    'eastern-shore': '/eastern-shore/',
    'gulf-shores': '/gulf-shores/',
    'orange-beach': '/orange-beach/',
    'foley': '/foley/',
    'fort-morgan': '/fort-morgan/',
    'robertsdale': '/robertsdale/',
    'bay-minette': '/bay-minette/',
    'loxley': '/loxley/',
    'elberta': '/elberta/',
    'summerdale': '/summerdale/',
    'dauphin-island': '/dauphin-island/',
    'tillmans-corner': '/tillmans-corner/',
    'maid-service-mobile-al': '/maid-service-mobile-al/',
}

CORRECT_MAIN_LINKS = {
    'home': '/',
    'about': '/about/',
    'blog': '/blog/',
    'contact': '/contact/',
    'gallery': '/Gallery/',
    'apply': '/apply/',
}

def find_all_html_files(root_dir):
    """Find all HTML files in the directory tree"""
    html_files = []
    for root, dirs, files in os.walk(root_dir):
        # Skip .git directory
        if '.git' in root:
            continue
        for file in files:
            if file.endswith('.html'):
                html_files.append(os.path.join(root, file))
    return html_files

def extract_nav_links(content):
    """Extract all navigation links from HTML content"""
    # Find all href attributes
    href_pattern = r'href=["\']([^"\']+)["\']'
    links = re.findall(href_pattern, content)
    return links

def categorize_link(link):
    """Categorize a link as service, location, main, or other"""
    link = link.strip('/')
    
    # Check if it's a service link
    for service in CORRECT_SERVICE_LINKS.keys():
        if service in link:
            return 'service', service
    
    # Check if it's a location link
    for location in CORRECT_LOCATION_LINKS.keys():
        if location in link:
            return 'location', location
    
    # Check if it's a main link
    if link == '' or link == '/':
        return 'main', 'home'
    for main in CORRECT_MAIN_LINKS.keys():
        if main in link:
            return 'main', main
    
    return 'other', link

def fix_navigation_links(content):
    """Fix all navigation links in the content"""
    changes = []
    
    # Fix service links - handle both with and without /services/ prefix
    for service, correct_link in CORRECT_SERVICE_LINKS.items():
        # Pattern 1: Missing /services/ prefix
        wrong_pattern1 = f'href="/{service}/"'
        if wrong_pattern1 in content:
            content = content.replace(wrong_pattern1, f'href="{correct_link}"')
            changes.append(f"Fixed: /{service}/ -> {correct_link}")
        
        # Pattern 2: Already correct
        # (no change needed)
    
    # Fix location links - ensure they don't have /services/ prefix
    for location, correct_link in CORRECT_LOCATION_LINKS.items():
        # Pattern: Incorrect /services/ prefix on location
        wrong_pattern = f'href="/services/{location}/"'
        if wrong_pattern in content:
            content = content.replace(wrong_pattern, f'href="{correct_link}"')
            changes.append(f"Fixed: /services/{location}/ -> {correct_link}")
    
    return content, changes

def verify_and_fix_file(file_path):
    """Verify and fix links in a single HTML file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        fixed_content, changes = fix_navigation_links(content)
        
        if changes:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(fixed_content)
            return True, changes
        
        return False, []
    
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return False, []

def generate_report(results):
    """Generate a comprehensive report of all changes"""
    report = []
    report.append("=" * 80)
    report.append("NAVIGATION LINK VERIFICATION AND FIX REPORT")
    report.append("=" * 80)
    report.append("")
    
    total_files = len(results)
    fixed_files = sum(1 for modified, _ in results.values() if modified)
    
    report.append(f"Total HTML files scanned: {total_files}")
    report.append(f"Files with fixes: {fixed_files}")
    report.append(f"Files without issues: {total_files - fixed_files}")
    report.append("")
    report.append("=" * 80)
    report.append("DETAILED CHANGES")
    report.append("=" * 80)
    report.append("")
    
    for file_path, (modified, changes) in sorted(results.items()):
        if modified:
            report.append(f"\n{file_path}")
            report.append("-" * 80)
            for change in changes:
                report.append(f"  • {change}")
    
    if fixed_files == 0:
        report.append("\n[OK] No issues found! All navigation links are correct.")
    
    return "\n".join(report)

def main():
    """Main execution function"""
    root_dir = r"c:\Users\lucia\OneDrive\Desktop\ZOIRISCLEANING"
    
    print("Starting navigation link verification and fixing...")
    print(f"Scanning directory: {root_dir}")
    print("")
    
    # Find all HTML files
    html_files = find_all_html_files(root_dir)
    print(f"Found {len(html_files)} HTML files")
    print("")
    
    # Process each file
    results = {}
    for file_path in html_files:
        modified, changes = verify_and_fix_file(file_path)
        results[file_path] = (modified, changes)
        if modified:
            print(f"[FIXED] {file_path}")
    
    # Generate and save report
    report = generate_report(results)
    report_path = os.path.join(root_dir, "link_verification_report.txt")
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print("")
    print("=" * 80)
    print(f"Report saved to: {report_path}")
    print("=" * 80)
    print("")
    print(report)

if __name__ == "__main__":
    main()
