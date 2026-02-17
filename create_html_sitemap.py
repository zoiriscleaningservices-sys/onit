"""
Create HTML Sitemap Page
This script generates a user-friendly HTML sitemap that:
1. Lists all pages organized by category
2. Helps Google discover all pages through internal links
3. Improves user experience
4. Provides additional crawl paths
"""

import os
from pathlib import Path

def find_all_html_files(root_dir):
    """Find all HTML files and categorize them"""
    
    categories = {
        'main': [],
        'services': [],
        'locations': [],
        'location_services': [],
        'blog': []
    }
    
    for root, dirs, files in os.walk(root_dir):
        if '.git' in root or 'node_modules' in root:
            continue
            
        for file in files:
            if file == 'index.html':
                rel_path = os.path.relpath(os.path.join(root, file), root_dir)
                url_path = '/' + rel_path.replace('\\', '/').replace('/index.html', '/')
                
                # Categorize the page
                if url_path == '/':
                    categories['main'].append(('Home', url_path))
                elif url_path in ['/about/', '/contact/', '/Gallery/', '/apply/', '/blog/']:
                    page_name = url_path.strip('/').title()
                    categories['main'].append((page_name, url_path))
                elif url_path.startswith('/services/'):
                    service_name = url_path.replace('/services/', '').strip('/').replace('-', ' ').title()
                    categories['services'].append((service_name, url_path))
                elif url_path.startswith('/blog/'):
                    blog_name = url_path.replace('/blog/', '').strip('/').replace('-', ' ').title()
                    categories['blog'].append((blog_name, url_path))
                elif '/' in url_path.strip('/') and url_path.count('/') > 2:
                    # Location-specific service page
                    parts = url_path.strip('/').split('/')
                    location = parts[0].replace('-', ' ').title()
                    service = parts[1].replace('-', ' ').title()
                    page_name = f"{service} in {location}"
                    categories['location_services'].append((page_name, url_path))
                else:
                    # Main location page
                    location_name = url_path.strip('/').replace('-', ' ').title()
                    categories['locations'].append((location_name, url_path))
    
    # Sort all categories
    for key in categories:
        categories[key].sort()
    
    return categories

def generate_html_sitemap(categories):
    """Generate the HTML sitemap page"""
    
    html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sitemap - Zoiris Cleaning Services</title>
    <meta name="description" content="Complete sitemap of all Zoiris Cleaning Services pages including services, locations, and blog posts.">
    <meta name="robots" content="index, follow">
    <link rel="canonical" href="https://www.zoiriscleaningservices.com/sitemap.html">
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #333;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            padding: 40px;
            border-radius: 10px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        }
        
        h1 {
            color: #667eea;
            margin-bottom: 10px;
            font-size: 2.5em;
        }
        
        .intro {
            color: #666;
            margin-bottom: 40px;
            font-size: 1.1em;
        }
        
        .section {
            margin-bottom: 40px;
        }
        
        h2 {
            color: #764ba2;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 3px solid #667eea;
            font-size: 1.8em;
        }
        
        .links {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
            gap: 15px;
        }
        
        .links a {
            display: block;
            padding: 12px 15px;
            background: #f8f9fa;
            color: #667eea;
            text-decoration: none;
            border-radius: 5px;
            transition: all 0.3s ease;
            border-left: 4px solid #667eea;
        }
        
        .links a:hover {
            background: #667eea;
            color: white;
            transform: translateX(5px);
            box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
        }
        
        .count {
            color: #999;
            font-size: 0.9em;
            margin-left: 10px;
        }
        
        @media (max-width: 768px) {
            .container {
                padding: 20px;
            }
            
            h1 {
                font-size: 2em;
            }
            
            h2 {
                font-size: 1.5em;
            }
            
            .links {
                grid-template-columns: 1fr;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Sitemap</h1>
        <p class="intro">
            Complete directory of all pages on Zoiris Cleaning Services. 
            Browse our services, locations, and resources to find exactly what you need.
        </p>
"""
    
    # Main Pages
    if categories['main']:
        html += f"""
        <div class="section">
            <h2>Main Pages <span class="count">({len(categories['main'])} pages)</span></h2>
            <div class="links">
"""
        for name, url in categories['main']:
            html += f'                <a href="{url}">{name}</a>\n'
        html += """            </div>
        </div>
"""
    
    # Services
    if categories['services']:
        html += f"""
        <div class="section">
            <h2>Our Services <span class="count">({len(categories['services'])} services)</span></h2>
            <div class="links">
"""
        for name, url in categories['services']:
            html += f'                <a href="{url}">{name}</a>\n'
        html += """            </div>
        </div>
"""
    
    # Locations
    if categories['locations']:
        html += f"""
        <div class="section">
            <h2>Service Locations <span class="count">({len(categories['locations'])} locations)</span></h2>
            <div class="links">
"""
        for name, url in categories['locations']:
            html += f'                <a href="{url}">{name}</a>\n'
        html += """            </div>
        </div>
"""
    
    # Blog
    if categories['blog']:
        html += f"""
        <div class="section">
            <h2>Blog Posts <span class="count">({len(categories['blog'])} posts)</span></h2>
            <div class="links">
"""
        for name, url in categories['blog']:
            html += f'                <a href="{url}">{name}</a>\n'
        html += """            </div>
        </div>
"""
    
    # Location-specific services (collapsed by default due to large number)
    if categories['location_services']:
        html += f"""
        <div class="section">
            <h2>Location-Specific Services <span class="count">({len(categories['location_services'])} pages)</span></h2>
            <p style="color: #666; margin-bottom: 15px; font-size: 0.95em;">
                Services available in specific locations. Click to view details.
            </p>
            <div class="links">
"""
        # Only show first 50 to avoid overwhelming the page
        for name, url in categories['location_services'][:50]:
            html += f'                <a href="{url}">{name}</a>\n'
        
        if len(categories['location_services']) > 50:
            html += f'                <p style="padding: 15px; color: #999;">...and {len(categories['location_services']) - 50} more location-specific service pages</p>\n'
        
        html += """            </div>
        </div>
"""
    
    html += """
    </div>
</body>
</html>
"""
    
    return html

def main():
    root_dir = r"c:\Users\lucia\OneDrive\Desktop\ZOIRISCLEANING"
    
    print("Generating HTML sitemap...")
    print("")
    
    # Find and categorize all pages
    categories = find_all_html_files(root_dir)
    
    # Count total pages
    total = sum(len(pages) for pages in categories.values())
    
    print(f"Found {total} total pages:")
    print(f"  - Main pages: {len(categories['main'])}")
    print(f"  - Services: {len(categories['services'])}")
    print(f"  - Locations: {len(categories['locations'])}")
    print(f"  - Blog posts: {len(categories['blog'])}")
    print(f"  - Location-specific services: {len(categories['location_services'])}")
    print("")
    
    # Generate HTML
    html = generate_html_sitemap(categories)
    
    # Save to file
    output_path = os.path.join(root_dir, 'sitemap.html')
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print("=" * 80)
    print(f"HTML sitemap created: {output_path}")
    print("=" * 80)
    print("")
    print("[OK] HTML sitemap generation complete!")

if __name__ == "__main__":
    main()
