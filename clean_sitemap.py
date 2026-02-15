import re
import os

sitemap_path = 'sitemap.xml'
with open(sitemap_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Extract header and footer
header_match = re.search(r'^(.*?)<url>', content, re.DOTALL)
footer_match = re.search(r'</urlset>.*$', content, re.DOTALL)

if header_match and footer_match:
    header = header_match.group(1)
    footer = footer_match.group(0)
    
    # Extract all url blocks
    url_pattern = r'<url>.*?</url>'
    urls = re.findall(url_pattern, content, re.DOTALL)
    
    print(f"Total URL entries found: {len(urls)}")
    
    unique_urls = {}
    cleaned_blocks = []
    
    for block in urls:
        loc_match = re.search(r'<loc>(.*?)</loc>', block)
        if loc_match:
            loc = loc_match.group(1)
            if loc not in unique_urls:
                unique_urls[loc] = True
                cleaned_blocks.append(block)
    
    print(f"Unique URL entries: {len(cleaned_blocks)}")
    
    new_content = header + '\n'.join(cleaned_blocks) + '\n' + footer
    
    with open(sitemap_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
        
    print("Sitemap cleaned.")
else:
    print("Could not parse sitemap structure.")
