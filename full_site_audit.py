import os
from pathlib import Path
import re

def full_site_indexing_audit():
    print("=" * 70)
    print("FULL SITE INDEXING READINESS AUDIT (855 PAGES)")
    print("=" * 70)
    
    base_url = "https://www.zoiriscleaningservices.com"
    base_dir = Path('.')
    excluded_dirs = {'.git', '.github', 'upload', 'favicon', 'tmp', '.gemini'}
    
    html_files = list(base_dir.glob('**/index.html'))
    valid_files = [f for f in html_files if not any(ex in str(f) for ex in excluded_dirs)]
    
    print(f"Auditing {len(valid_files)} pages...")
    
    issues = {
        "missing_canonical": [],
        "mismatched_canonical": [],
        "noindex_found": [],
        "missing_title": [],
        "missing_description": []
    }
    
    for f in valid_files:
        rel_path = str(f.parent).replace('\\', '/').strip('./').strip('/')
        if rel_path == '':
            expected_url = f"{base_url}/"
        else:
            expected_url = f"{base_url}/{rel_path}/"
            
        content = f.read_text(encoding='utf-8', errors='ignore')
        
        # Canonical Check
        canonical_match = re.search(r'<link [^>]*rel="canonical"[^>]*>', content) or \
                         re.search(r'<link [^>]*href="[^"]+"[^>]*rel="canonical"[^>]*>', content)
        
        if not canonical_match:
            issues["missing_canonical"].append(str(f))
        else:
            href_match = re.search(r'href="([^"]+)"', canonical_match.group(0))
            if href_match:
                found_url = href_match.group(1)
                # Normalize both for comparison (trailing slash)
                if found_url.rstrip('/') != expected_url.rstrip('/'):
                    issues["mismatched_canonical"].append(f"{f}: Found {found_url}, Expected {expected_url}")
            else:
                issues["missing_canonical"].append(str(f) + " (tag exists but no href)")
        
        # Robots Check
        robots_match = re.search(r'<meta name="robots" content="([^"]+)"', content)
        if robots_match and "noindex" in robots_match.group(1).lower():
            issues["noindex_found"].append(str(f))
            
        # Basic SEO Check
        if "<title>" not in content:
            issues["missing_title"].append(str(f))
        if 'name="description"' not in content.lower():
            issues["missing_description"].append(str(f))

    print("\n[RESULTS]")
    print(f"  Missing Canonical: {len(issues['missing_canonical'])}")
    print(f"  Mismatched Canonical: {len(issues['mismatched_canonical'])}")
    print(f"  Noindex Found: {len(issues['noindex_found'])}")
    print(f"  Missing Title: {len(issues['missing_title'])}")
    print(f"  Missing Description: {len(issues['missing_description'])}")
    
    if any(len(v) > 0 for v in issues.values()):
        print("\n[DETAIL OF ISSUES]")
        for category, list_of_issues in issues.items():
            if list_of_issues:
                print(f"\n--- {category.upper()} ---")
                for issue in list_of_issues[:10]: # Show first 10
                    print(f"  {issue}")
                if len(list_of_issues) > 10:
                    print(f"  ... and {len(list_of_issues) - 10} more.")
    else:
        print("\n[SUCCESS] All 855 pages are perfectly optimized for indexing!")

if __name__ == '__main__':
    full_site_indexing_audit()
