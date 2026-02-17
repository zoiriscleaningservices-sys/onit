"""
Generate Priority Pages List for Manual Google Search Console Indexing
This creates a prioritized list of the top 100 pages to manually request indexing
"""

def generate_priority_list():
    """Generate prioritized list of pages for manual indexing"""
    
    priority_pages = []
    
    # Priority 1: Homepage (CRITICAL)
    priority_pages.append({
        'priority': 1,
        'url': 'https://www.zoiriscleaningservices.com/',
        'reason': 'Homepage - Most important page'
    })
    
    # Priority 2: Main Service Pages (13 pages)
    services = [
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
    
    for service in services:
        priority_pages.append({
            'priority': 2,
            'url': f'https://www.zoiriscleaningservices.com/services/{service}/',
            'reason': f'Main service page - {service.replace("-", " ").title()}'
        })
    
    # Priority 3: Major Location Pages (Top 20 cities)
    major_locations = [
        ('maid-service-mobile-al', 'Mobile (Main)'),
        ('downtown-mobile', 'Downtown Mobile'),
        ('midtown-mobile', 'Midtown Mobile'),
        ('west-mobile', 'West Mobile'),
        ('birmingham', 'Birmingham'),
        ('huntsville', 'Huntsville'),
        ('montgomery', 'Montgomery'),
        ('tuscaloosa', 'Tuscaloosa'),
        ('hoover', 'Hoover'),
        ('dothan', 'Dothan'),
        ('daphne', 'Daphne'),
        ('fairhope', 'Fairhope'),
        ('spanish-fort', 'Spanish Fort'),
        ('gulf-shores', 'Gulf Shores'),
        ('orange-beach', 'Orange Beach'),
        ('foley', 'Foley'),
        ('saraland', 'Saraland'),
        ('theodore', 'Theodore'),
        ('semmes', 'Semmes'),
        ('bay-minette', 'Bay Minette')
    ]
    
    for location_slug, location_name in major_locations:
        priority_pages.append({
            'priority': 3,
            'url': f'https://www.zoiriscleaningservices.com/{location_slug}/',
            'reason': f'Major location page - {location_name}'
        })
    
    # Priority 4: Main Pages
    main_pages = [
        ('about', 'About Us'),
        ('contact', 'Contact'),
        ('blog', 'Blog'),
        ('Gallery', 'Gallery'),
        ('apply', 'Careers/Apply')
    ]
    
    for page_slug, page_name in main_pages:
        priority_pages.append({
            'priority': 4,
            'url': f'https://www.zoiriscleaningservices.com/{page_slug}/',
            'reason': f'Main page - {page_name}'
        })
    
    # Priority 5: High-value location-service combinations (Top 30)
    # Focus on major cities + popular services
    high_value_combos = []
    popular_services = ['airbnb-cleaning', 'deep-cleaning', 'house-cleaning', 'commercial-cleaning', 'move-in-out']
    top_cities = ['maid-service-mobile-al', 'daphne', 'fairhope', 'gulf-shores', 'birmingham', 'huntsville']
    
    for city in top_cities:
        for service in popular_services:
            high_value_combos.append({
                'priority': 5,
                'url': f'https://www.zoiriscleaningservices.com/{city}/{service}/',
                'reason': f'High-value combo - {service.replace("-", " ").title()} in {city.replace("-", " ").title()}'
            })
    
    priority_pages.extend(high_value_combos[:30])  # Limit to 30
    
    return priority_pages

def save_priority_list(pages):
    """Save the priority list to a file"""
    
    output_path = r"c:\Users\lucia\OneDrive\Desktop\ZOIRISCLEANING\priority_pages_for_indexing.txt"
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("=" * 80 + "\n")
        f.write("PRIORITY PAGES FOR GOOGLE SEARCH CONSOLE INDEXING\n")
        f.write("=" * 80 + "\n\n")
        f.write("Instructions:\n")
        f.write("1. Go to Google Search Console\n")
        f.write("2. Use the URL Inspection tool\n")
        f.write("3. Paste each URL below and click 'Request Indexing'\n")
        f.write("4. Start with Priority 1 and work your way down\n")
        f.write("5. Google limits requests, so spread them over several days if needed\n\n")
        f.write("=" * 80 + "\n\n")
        
        current_priority = 0
        for page in pages:
            if page['priority'] != current_priority:
                current_priority = page['priority']
                f.write(f"\n{'=' * 80}\n")
                f.write(f"PRIORITY {current_priority}\n")
                f.write(f"{'=' * 80}\n\n")
            
            f.write(f"{page['url']}\n")
            f.write(f"  Reason: {page['reason']}\n\n")
        
        f.write("\n" + "=" * 80 + "\n")
        f.write(f"Total pages in this list: {len(pages)}\n")
        f.write("=" * 80 + "\n")
    
    return output_path

def main():
    print("Generating priority pages list for Google Search Console...")
    print("")
    
    pages = generate_priority_list()
    output_path = save_priority_list(pages)
    
    print(f"Generated {len(pages)} priority pages")
    print("")
    print("Breakdown by priority:")
    priority_counts = {}
    for page in pages:
        priority_counts[page['priority']] = priority_counts.get(page['priority'], 0) + 1
    
    for priority in sorted(priority_counts.keys()):
        print(f"  Priority {priority}: {priority_counts[priority]} pages")
    
    print("")
    print("=" * 80)
    print(f"Priority list saved to: {output_path}")
    print("=" * 80)
    print("")
    print("[OK] Priority pages list generation complete!")

if __name__ == "__main__":
    main()
