import os
import re

TEMPLATE_DIR = 'foley'
TEMPLATE_FILE = 'index.html'

cities = [
    {"name": "Pensacola Beach", "slug": "pensacola-beach", "county": "Escambia County", "zip": "32561", "zips": ["32561"], "lat": "30.3323", "long": "-87.1408"},
    {"name": "Gulf Breeze", "slug": "gulf-breeze", "county": "Santa Rosa County", "zip": "32561", "zips": ["32561", "32562"], "lat": "30.3582", "long": "-87.1724"},
    {"name": "Destin", "slug": "destin", "county": "Okaloosa County", "zip": "32541", "zips": ["32541", "32540"], "lat": "30.3935", "long": "-86.4753"},
    {"name": "Santa Rosa Beach", "slug": "santa-rosa-beach", "county": "Walton County", "zip": "32459", "zips": ["32459"], "lat": "30.4011", "long": "-86.2238"},
    {"name": "Seaside", "slug": "seaside", "county": "Walton County", "zip": "32459", "zips": ["32459"], "lat": "30.3204", "long": "-86.1365"},
    {"name": "Rosemary Beach", "slug": "rosemary-beach", "county": "Walton County", "zip": "32461", "zips": ["32461"], "lat": "30.2785", "long": "-85.9658"},
    {"name": "Alys Beach", "slug": "alys-beach", "county": "Walton County", "zip": "32461", "zips": ["32461"], "lat": "30.2858", "long": "-85.9814"}
]

# All existing and new services to link inside the new location hubs
all_services = [
    {"slug": "commercial-cleaning", "name": "Commercial Cleaning"},
    {"slug": "deep-cleaning", "name": "Deep Cleaning"},
    {"slug": "house-cleaning", "name": "House Cleaning"},
    {"slug": "move-in-cleaning", "name": "Move-In Cleaning"},
    {"slug": "move-out-cleaning", "name": "Move-Out Cleaning"},
    {"slug": "vacation-rental-cleaning", "name": "Vacation Rental Cleaning"},
    {"slug": "airbnb-cleaning", "name": "Airbnb Cleaning"},
    {"slug": "post-construction-cleanup", "name": "Post-Construction Cleanup"},
    {"slug": "carpet-cleaning", "name": "Carpet Cleaning"},
    {"slug": "pressure-washing", "name": "Pressure Washing"},
    {"slug": "Detailing-Mobile-AL", "name": "Detailing"},
    {"slug": "laundry-services", "name": "Laundry Services"},
    {"slug": "window-cleaning", "name": "Window Cleaning"},
    {"slug": "luxury-estate-cleaning", "name": "Luxury Estate Cleaning"},
    {"slug": "luxury-estate-management", "name": "Luxury Estate Management"},
    {"slug": "home-watch-services", "name": "Home Watch Services"},
    {"slug": "property-management-janitorial", "name": "Property Management Janitorial"},
    {"slug": "property-maintenance", "name": "Property Maintenance"},
    {"slug": "airbnb-vacation-rental-management", "name": "Airbnb & Vacation Rental Management"},
    {"slug": "gutter-cleaning", "name": "Gutter Cleaning"},
    {"slug": "office-janitorial-services", "name": "Office Janitorial Services"},
    {"slug": "janitorial-cleaning-services", "name": "Janitorial Cleaning Services"},
    {"slug": "medical-dental-facility-cleaning", "name": "Medical & Dental Facility Cleaning"},
    {"slug": "industrial-warehouse-cleaning", "name": "Industrial & Warehouse Cleaning"},
    {"slug": "floor-stripping-waxing", "name": "Floor Stripping & Waxing"},
    {"slug": "gym-fitness-center-cleaning", "name": "Gym & Fitness Center Cleaning"},
    {"slug": "school-daycare-cleaning", "name": "School & Daycare Cleaning"},
    {"slug": "church-worship-center-cleaning", "name": "Church & Worship Center Cleaning"},
    {"slug": "solar-panel-cleaning", "name": "Solar Panel Cleaning"}
]

def generate_pages():
    if not os.path.exists(os.path.join(TEMPLATE_DIR, TEMPLATE_FILE)):
        print(f"Error: Template file not found at {TEMPLATE_DIR}/{TEMPLATE_FILE}")
        return

    with open(os.path.join(TEMPLATE_DIR, TEMPLATE_FILE), 'r', encoding='utf-8') as f:
        template_content = f.read()

    new_sitemap_entries = []

    for city in cities:
        print(f"Generating Hub Page for {city['name']}...")
        if not os.path.exists(city['slug']):
            os.makedirs(city['slug'])

        content = template_content
        
        # Replace template placeholders
        content = content.replace('Foley', city['name'])
        content = content.replace('36535', city['zip'])
        content = content.replace('Baldwin County', city['county'])
        content = content.replace('30.4066', city['lat'])
        content = content.replace('-87.6836', city['long'])
        
        # URL / Canonical
        content = content.replace('/foley/', f'/{city["slug"]}/')
        
        # Zips Array
        zip_pattern = r'const serviceZips = \[[^\]]*\];'
        new_zips_js = 'const serviceZips = [\n      ' + ', '.join([f'"{z}"' for z in city['zips']]) + '\n    ];'
        content = re.sub(zip_pattern, new_zips_js, content)

        # Cleanup Hidden Text
        content = re.sub(r'<div style="display:none;">.*?</div>', '', content, flags=re.DOTALL)

        # Generate mega grid of services for this city
        links_html = f'<div class="grid grid-cols-1 md:grid-cols-3 gap-4 mt-4 text-center">'
        for s in all_services:
            s_target_slug = s['slug'].replace('-Mobile-AL', '').replace('-mobile-al', '')
            link_url = f"/{city['slug']}/{s_target_slug}/"
            links_html += f'<a href="{link_url}" class="block p-4 bg-gray-50 hover:bg-blue-100 rounded-lg transition border border-gray-200 text-blue-900 font-semibold">{s["name"]} in {city["name"]}</a>'
        links_html += '</div>'
        
        services_section = f'''
        <section class="py-16 bg-white shrink-0">
          <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <h2 class="text-3xl font-bold text-center text-gray-900 mb-8">Professional Cleaning Services in {city['name']}</h2>
            <p class="text-center text-lg text-gray-600 mb-10 max-w-3xl mx-auto">
              We offer a complete range of luxury residential and commercial cleaning solutions tailored to {city['name']} properties. 
            </p>
            {links_html}
          </div>
        </section>
        '''
        
        # Inject the services matrix before Footer
        # the template likely has <footer... let's replace
        if '<footer' in content:
            content = content.replace('<footer', f'{services_section}\n<footer')
        else:
            print("Warning: no <footer found, appending to body.")
            content = content.replace('</body>', f'{services_section}\n</body>')

        target_file = os.path.join(city['slug'], 'index.html')
        with open(target_file, 'w', encoding='utf-8') as f:
            f.write(content)
            
        # Add to sitemap entries string
        new_sitemap_entries.append(f'  <url>\n    <loc>https://www.zoiriscleaningservices.com/{city["slug"]}/</loc>\n    <lastmod>2026-02-21</lastmod>\n    <changefreq>weekly</changefreq>\n    <priority>0.9</priority>\n  </url>')

    # Update Sitemap safely
    sitemap_path = 'sitemap.xml'
    if os.path.exists(sitemap_path):
        with open(sitemap_path, 'r', encoding='utf-8') as f:
            sitemap_content = f.read()
        
        final_entries_to_add = []
        for entry in new_sitemap_entries:
            match = re.search(r'<loc>(.*?)</loc>', entry)
            if match:
                url = match.group(1)
                if url not in sitemap_content:
                    final_entries_to_add.append(entry)
        
        if final_entries_to_add:
            if '</urlset>' in sitemap_content:
                new_content = sitemap_content.replace('</urlset>', '\n'.join(final_entries_to_add) + '\n</urlset>')
                with open(sitemap_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                print(f"Added {len(final_entries_to_add)} new high-end hub pages to sitemap.xml.")

if __name__ == "__main__":
    generate_pages()
