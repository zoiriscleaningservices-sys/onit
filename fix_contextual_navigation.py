"""
Fix Contextual Navigation Links - Version 2

This improved script handles both absolute and relative navigation links
and ensures proper context-aware navigation across all pages.
"""

import os
import re
from pathlib import Path

# Define all locations and services
LOCATIONS = [
    'alabaster', 'albertville', 'anniston', 'athens', 'auburn', 'bay-minette',
    'bessemer', 'birmingham', 'calera', 'chelsea', 'cullman', 'daphne',
    'dauphin-island', 'decatur', 'dothan', 'downtown-mobile', 'eastern-shore',
    'elberta', 'enterprise', 'fairhope', 'florence', 'foley', 'fort-morgan',
    'fort-payne', 'gadsden', 'gardendale', 'grand-bay', 'gulf-shores',
    'hartselle', 'helena', 'homewood', 'hoover', 'hueytown', 'huntsville',
    'loxley', 'madison', 'maid-service-mobile-al', 'midtown-mobile',
    'millbrook', 'montgomery', 'mountain-brook', 'muscle-shoals', 'northport',
    'opelika', 'orange-beach', 'oxford', 'phenix-city', 'prattville',
    'robertsdale', 'saraland', 'satsuma', 'selma', 'semmes', 'spanish-fort',
    'summerdale', 'theodore', 'tillmans-corner', 'troy', 'tuscaloosa',
    'vestavia-hills', 'west-mobile'
]

SERVICES = [
    'commercial-cleaning', 'deep-cleaning', 'house-cleaning', 'move-in-cleaning',
    'move-out-cleaning', 'vacation-rental-cleaning', 'airbnb-cleaning',
    'post-construction-cleanup', 'carpet-cleaning', 'pressure-washing',
    'Detailing-Mobile-AL', 'laundry-services', 'window-cleaning', 'detailing',
    'move-in-out'
]

def get_navigation_script(page_type, current_location=None, current_service=None):
    """Generate JavaScript for contextual navigation based on page type"""
    
    script = """
<script>
// Contextual Navigation Fix v2
(function() {
    'use strict';
    
    const currentLocation = '""" + (current_location or '') + """';
    const currentService = '""" + (current_service or '') + """';
    
    // List of all services for matching
    const services = ['commercial-cleaning', 'deep-cleaning', 'house-cleaning', 'move-in-cleaning',
                     'move-out-cleaning', 'vacation-rental-cleaning', 'airbnb-cleaning',
                     'post-construction-cleanup', 'carpet-cleaning', 'pressure-washing',
                     'Detailing-Mobile-AL', 'laundry-services', 'window-cleaning', 'detailing', 'move-in-out'];
    
    const locations = ['alabaster', 'albertville', 'anniston', 'athens', 'auburn', 'bay-minette',
                      'bessemer', 'birmingham', 'calera', 'chelsea', 'cullman', 'daphne',
                      'dauphin-island', 'decatur', 'dothan', 'downtown-mobile', 'eastern-shore',
                      'elberta', 'enterprise', 'fairhope', 'florence', 'foley', 'fort-morgan',
                      'fort-payne', 'gadsden', 'gardendale', 'grand-bay', 'gulf-shores',
                      'hartselle', 'helena', 'homewood', 'hoover', 'hueytown', 'huntsville',
                      'loxley', 'madison', 'maid-service-mobile-al', 'midtown-mobile',
                      'millbrook', 'montgomery', 'mountain-brook', 'muscle-shoals', 'northport',
                      'opelika', 'orange-beach', 'oxford', 'phenix-city', 'prattville',
                      'robertsdale', 'saraland', 'satsuma', 'selma', 'semmes', 'spanish-fort',
                      'summerdale', 'theodore', 'tillmans-corner', 'troy', 'tuscaloosa',
                      'vestavia-hills', 'west-mobile'];
    
    function extractService(href) {
        // Try to extract service from various href patterns
        // Pattern 1: /services/service-name/
        let match = href.match(/\\/services\\/([^\\/]+)\\//);
        if (match) return match[1];
        
        // Pattern 2: ../service-name/ (relative)
        match = href.match(/\\.\\.\\/([\w-]+)\\//);
        if (match && services.includes(match[1])) return match[1];
        
        // Pattern 3: /location/service-name/
        const parts = href.split('/').filter(p => p);
        if (parts.length === 2 && locations.includes(parts[0]) && services.includes(parts[1])) {
            return parts[1];
        }
        
        return null;
    }
    
    function extractLocation(href) {
        // Try to extract location from various href patterns
        const parts = href.split('/').filter(p => p);
        
        // Pattern 1: /location/
        if (parts.length === 1 && locations.includes(parts[0])) {
            return parts[0];
        }
        
        // Pattern 2: /location/service/
        if (parts.length === 2 && locations.includes(parts[0])) {
            return parts[0];
        }
        
        return null;
    }
    
    function updateNavigationLinks() {
        // Update all navigation links
        const navLinks = document.querySelectorAll('nav a[href]');
        
        navLinks.forEach(link => {
            const href = link.getAttribute('href');
            
            // Skip external links, anchors, and static pages
            if (!href || href.startsWith('http') || href.startsWith('#') || 
                href.includes('/about/') || href.includes('/blog/') || 
                href.includes('/contact/') || href.includes('/Gallery/') ||
                href.includes('/apply/') || href === '/') {
                return;
            }
            
            const service = extractService(href);
            const location = extractLocation(href);
            
            // If we're on a location page and this is a service link
            if (currentLocation && service && !location) {
                link.setAttribute('href', `/${currentLocation}/${service}/`);
            }
            
            // If we're on a service page (under /services/) and this is a location link
            if (currentService && !currentLocation && location && !service) {
                link.setAttribute('href', `/${location}/${currentService}/`);
            }
            
            // If we're on a location-service page
            if (currentLocation && currentService) {
                if (service && !location) {
                    // Service link - keep current location
                    link.setAttribute('href', `/${currentLocation}/${service}/`);
                } else if (location && !service) {
                    // Location link - keep current service
                    link.setAttribute('href', `/${location}/${currentService}/`);
                }
            }
        });
    }
    
    // Run on page load
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', updateNavigationLinks);
    } else {
        updateNavigationLinks();
    }
})();
</script>
"""
    return script

def inject_navigation_script(file_path, page_type, current_location=None, current_service=None):
    """Inject or update navigation script in HTML file"""
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Remove any existing contextual navigation script
    content = re.sub(
        r'<script>\s*//\s*Contextual Navigation Fix.*?</script>',
        '',
        content,
        flags=re.DOTALL
    )
    
    # Create new script
    nav_script = get_navigation_script(page_type, current_location, current_service)
    
    # Insert before closing </body> tag
    if '</body>' in content:
        content = content.replace('</body>', nav_script + '\n</body>')
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

def main():
    base_dir = Path(r'C:\Users\lucia\OneDrive\Desktop\ZOIRISCLEANING')
    
    print("Starting contextual navigation fix v2...")
    print("=" * 60)
    
    processed_count = 0
    
    # Process root index.html
    root_index = base_dir / 'index.html'
    if root_index.exists():
        print("Processing root index.html")
        inject_navigation_script(root_index, 'static')
        processed_count += 1
    
    # Process static pages
    for static_page in ['about', 'blog', 'contact', 'Gallery', 'apply']:
        static_index = base_dir / static_page / 'index.html'
        if static_index.exists():
            print(f"Processing static page: {static_page}")
            inject_navigation_script(static_index, 'static')
            processed_count += 1
    
    # Process location pages
    for location in LOCATIONS:
        location_index = base_dir / location / 'index.html'
        if location_index.exists():
            print(f"Processing location: {location}")
            inject_navigation_script(location_index, 'location', current_location=location)
            processed_count += 1
        
        # Process location-service pages
        for service in SERVICES:
            service_index = base_dir / location / service / 'index.html'
            if service_index.exists():
                inject_navigation_script(service_index, 'location-service', 
                                        current_location=location, 
                                        current_service=service)
                processed_count += 1
    
    # Process service pages under /services/
    for service in SERVICES:
        service_index = base_dir / 'services' / service / 'index.html'
        if service_index.exists():
            print(f"Processing service: {service}")
            inject_navigation_script(service_index, 'service', current_service=service)
            processed_count += 1
    
    print("=" * 60)
    print(f"Navigation fix complete! Processed {processed_count} pages.")
    print("\nNavigation is now context-aware:")
    print("  - Location pages -> Service links go to location-specific services")
    print("  - Service pages -> Location links go to service-specific locations")
    print("  - Location-service pages -> Both dropdowns maintain context")
    print("  - Static pages -> Standard navigation")

if __name__ == '__main__':
    main()
