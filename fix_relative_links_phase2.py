"""
Enhanced Link Verification and Fixing Script - Phase 2
This script will fix relative service links in location pages
"""

import os
import re

def fix_relative_service_links(content):
    """Fix relative service links to absolute links with /services/ prefix"""
    changes = []
    
    # Pattern for relative service links (without leading slash)
    patterns = {
        'commercial-cleaning/': '/services/commercial-cleaning/',
        'deep-cleaning/': '/services/deep-cleaning/',
        'house-cleaning/': '/services/house-cleaning/',
        'move-in-out/': '/services/move-in-cleaning/',  # Note: this is a special case
        'vacation-rental-cleaning/': '/services/vacation-rental-cleaning/',
        'airbnb-cleaning/': '/services/airbnb-cleaning/',
        'post-construction-cleanup/': '/services/post-construction-cleanup/',
        'carpet-cleaning/': '/services/carpet-cleaning/',
        'pressure-washing/': '/services/pressure-washing/',
        'detailing/': '/services/Detailing-Mobile-AL/',  # Note: special case for detailing
        'laundry-services/': '/services/laundry-services/',
        'window-cleaning/': '/services/window-cleaning/',
    }
    
    for old_link, new_link in patterns.items():
        # Match href="relative-link" (without leading slash)
        pattern = f'href="{old_link}"'
        if pattern in content:
            content = content.replace(pattern, f'href="{new_link}"')
            changes.append(f"Fixed: {old_link} -> {new_link}")
    
    return content, changes

def process_file(file_path):
    """Process a single HTML file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        fixed_content, changes = fix_relative_service_links(content)
        
        if changes:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(fixed_content)
            return True, changes
        
        return False, []
    
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return False, []

def find_all_html_files(root_dir):
    """Find all HTML files"""
    html_files = []
    for root, dirs, files in os.walk(root_dir):
        if '.git' in root:
            continue
        for file in files:
            if file.endswith('.html'):
                html_files.append(os.path.join(root, file))
    return html_files

def main():
    root_dir = r"c:\Users\lucia\OneDrive\Desktop\ZOIRISCLEANING"
    
    print("Phase 2: Fixing relative service links in location pages...")
    print("")
    
    html_files = find_all_html_files(root_dir)
    print(f"Found {len(html_files)} HTML files")
    print("")
    
    fixed_count = 0
    total_changes = 0
    
    for file_path in html_files:
        modified, changes = process_file(file_path)
        if modified:
            fixed_count += 1
            total_changes += len(changes)
            print(f"[FIXED] {file_path}")
    
    print("")
    print("=" * 80)
    print(f"Phase 2 Complete!")
    print(f"Files fixed: {fixed_count}")
    print(f"Total changes: {total_changes}")
    print("=" * 80)

if __name__ == "__main__":
    main()
