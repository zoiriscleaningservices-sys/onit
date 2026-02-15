import os
import shutil
import re

# Template Config
TEMPLATE_DIR = 'foley'
TEMPLATE_FILE = 'index.html'

# Full Cities List (45 Cities)
cities = [
    {
        "name": "Birmingham",
        "slug": "birmingham",
        "county": "Jefferson County",
        "zip": "35203",
        "zips": ["35203", "35204", "35205", "35206", "35209", "35211", "35212", "35222", "35233", "35234"],
        "lat": "33.5186",
        "long": "-86.8104"
    },
    {
        "name": "Montgomery",
        "slug": "montgomery",
        "county": "Montgomery County",
        "zip": "36104",
        "zips": ["36104", "36105", "36106", "36107", "36108", "36109", "36110", "36111", "36116", "36117"],
        "lat": "32.3668",
        "long": "-86.3000"
    },
    {
        "name": "Huntsville",
        "slug": "huntsville",
        "county": "Madison County",
        "zip": "35801",
        "zips": ["35801", "35802", "35803", "35805", "35806", "35810", "35811", "35816", "35824"],
        "lat": "34.7304",
        "long": "-86.5861"
    },
    {
        "name": "Tuscaloosa",
        "slug": "tuscaloosa",
        "county": "Tuscaloosa County",
        "zip": "35401",
        "zips": ["35401", "35404", "35405", "35406", "35453", "35456", "35473", "35475", "35476", "35487"],
        "lat": "33.2098",
        "long": "-87.5692"
    },
    {
        "name": "Hoover",
        "slug": "hoover",
        "county": "Jefferson County",
        "zip": "35216",
        "zips": ["35216", "35226", "35244", "35236", "35022", "35124"],
        "lat": "33.4054",
        "long": "-86.8114"
    },
    {
        "name": "Dothan",
        "slug": "dothan",
        "county": "Houston County",
        "zip": "36301",
        "zips": ["36301", "36303", "36305", "36321", "36350"],
        "lat": "31.2232",
        "long": "-85.3905"
    },
    {
        "name": "Auburn",
        "slug": "auburn",
        "county": "Lee County",
        "zip": "36830",
        "zips": ["36830", "36832", "36849", "36801", "36879"],
        "lat": "32.6099",
        "long": "-85.4808"
    },
    {
        "name": "Decatur",
        "slug": "decatur",
        "county": "Morgan County",
        "zip": "35601",
        "zips": ["35601", "35603", "35699", "35640", "35670"],
        "lat": "34.6059",
        "long": "-86.9833"
    },
    {
        "name": "Madison",
        "slug": "madison",
        "county": "Madison County",
        "zip": "35758",
        "zips": ["35758", "35756", "35757", "35896"],
        "lat": "34.6993",
        "long": "-86.7483"
    },
    {
        "name": "Florence",
        "slug": "florence",
        "county": "Lauderdale County",
        "zip": "35630",
        "zips": ["35630", "35633", "35634", "35617", "35645"],
        "lat": "34.7998",
        "long": "-87.6773"
    },
    # Phase 2 Cities (Tier 2)
    {
        "name": "Phenix City",
        "slug": "phenix-city",
        "county": "Russell County",
        "zip": "36867",
        "zips": ["36867", "36868", "36869"],
        "lat": "32.4709",
        "long": "-85.0007"
    },
    {
        "name": "Prattville",
        "slug": "prattville",
        "county": "Autauga County",
        "zip": "36067",
        "zips": ["36066", "36067", "36068"],
        "lat": "32.4640",
        "long": "-86.4597"
    },
    {
        "name": "Gadsden",
        "slug": "gadsden",
        "county": "Etowah County",
        "zip": "35901",
        "zips": ["35901", "35903", "35904", "35905"],
        "lat": "34.0143",
        "long": "-86.0066"
    },
    {
        "name": "Vestavia Hills",
        "slug": "vestavia-hills",
        "county": "Jefferson County",
        "zip": "35216",
        "zips": ["35216", "35226", "35242", "35243"],
        "lat": "33.4487",
        "long": "-86.7878"
    },
    {
        "name": "Alabaster",
        "slug": "alabaster",
        "county": "Shelby County",
        "zip": "35007",
        "zips": ["35007", "35114"],
        "lat": "33.2442",
        "long": "-86.8163"
    },
    {
        "name": "Opelika",
        "slug": "opelika",
        "county": "Lee County",
        "zip": "36801",
        "zips": ["36801", "36804"],
        "lat": "32.6454",
        "long": "-85.3782"
    },
    {
        "name": "Enterprise",
        "slug": "enterprise",
        "county": "Coffee County",
        "zip": "36330",
        "zips": ["36330", "36331"],
        "lat": "31.3151",
        "long": "-85.8552"
    },
    {
        "name": "Bessemer",
        "slug": "bessemer",
        "county": "Jefferson County",
        "zip": "35020",
        "zips": ["35020", "35022", "35023"],
        "lat": "33.4018",
        "long": "-86.9544"
    },
    {
        "name": "Homewood",
        "slug": "homewood",
        "county": "Jefferson County",
        "zip": "35209",
        "zips": ["35209", "35259"],
        "lat": "33.4717",
        "long": "-86.8008"
    },
    {
        "name": "Athens",
        "slug": "athens",
        "county": "Limestone County",
        "zip": "35611",
        "zips": ["35611", "35613", "35614"],
        "lat": "34.8028",
        "long": "-86.9716"
    },
    {
        "name": "Northport",
        "slug": "northport",
        "county": "Tuscaloosa County",
        "zip": "35473",
        "zips": ["35473", "35475", "35476"],
        "lat": "33.2290",
        "long": "-87.5772"
    },
    {
        "name": "Anniston",
        "slug": "anniston",
        "county": "Calhoun County",
        "zip": "36201",
        "zips": ["36201", "36206", "36207"],
        "lat": "33.6598",
        "long": "-85.8316"
    },
    {
        "name": "Oxford",
        "slug": "oxford",
        "county": "Calhoun County",
        "zip": "36203",
        "zips": ["36203"],
        "lat": "33.6146",
        "long": "-85.8350"
    },
    {
        "name": "Albertville",
        "slug": "albertville",
        "county": "Marshall County",
        "zip": "35950",
        "zips": ["35950", "35951"],
        "lat": "34.2676",
        "long": "-86.2089"
    },
    {
        "name": "Selma",
        "slug": "selma",
        "county": "Dallas County",
        "zip": "36701",
        "zips": ["36701", "36703"],
        "lat": "32.4073",
        "long": "-87.0211"
    },
    # Phase 3 Cities (Tier 3)
    {
        "name": "Foley",
        "slug": "foley",
        "county": "Baldwin County",
        "zip": "36535",
        "zips": ["36535", "36536"],
        "lat": "30.4066",
        "long": "-87.6836"
    },
    {
        "name": "Mountain Brook",
        "slug": "mountain-brook",
        "county": "Jefferson County",
        "zip": "35213",
        "zips": ["35213", "35223"],
        "lat": "33.4859",
        "long": "-86.7461"
    },
    {
        "name": "Cullman",
        "slug": "cullman",
        "county": "Cullman County",
        "zip": "35055",
        "zips": ["35055", "35056", "35057", "35058"],
        "lat": "34.1748",
        "long": "-86.8436"
    },
    {
        "name": "Troy",
        "slug": "troy",
        "county": "Pike County",
        "zip": "36081",
        "zips": ["36081", "36079"],
        "lat": "31.8088",
        "long": "-85.9697"
    },
    {
        "name": "Helena",
        "slug": "helena",
        "county": "Shelby County",
        "zip": "35080",
        "zips": ["35080", "35022"],
        "lat": "33.2965",
        "long": "-86.8417"
    },
    {
        "name": "Calera",
        "slug": "calera",
        "county": "Shelby County",
        "zip": "35040",
        "zips": ["35040"],
        "lat": "33.1021",
        "long": "-86.7533"
    },
    {
        "name": "Muscle Shoals",
        "slug": "muscle-shoals",
        "county": "Colbert County",
        "zip": "35661",
        "zips": ["35661", "35662"],
        "lat": "34.7448",
        "long": "-87.6675"
    },
    {
        "name": "Saraland",
        "slug": "saraland",
        "county": "Mobile County",
        "zip": "36571",
        "zips": ["36571"],
        "lat": "30.8207",
        "long": "-88.0706"
    },
    {
        "name": "Gardendale",
        "slug": "gardendale",
        "county": "Jefferson County",
        "zip": "35071",
        "zips": ["35071"],
        "lat": "33.6457",
        "long": "-86.8117"
    },
    {
        "name": "Chelsea",
        "slug": "chelsea",
        "county": "Shelby County",
        "zip": "35043",
        "zips": ["35043"],
        "lat": "33.3421",
        "long": "-86.6297"
    },
    {
        "name": "Hueytown",
        "slug": "hueytown",
        "county": "Jefferson County",
        "zip": "35023",
        "zips": ["35023"],
        "lat": "33.4392",
        "long": "-86.9972"
    },
    {
        "name": "Millbrook",
        "slug": "millbrook",
        "county": "Elmore County",
        "zip": "36054",
        "zips": ["36054"],
        "lat": "32.4787",
        "long": "-86.3683"
    },
    {
        "name": "Tillmans Corner",
        "slug": "tillmans-corner",
        "county": "Mobile County",
        "zip": "36619",
        "zips": ["36619"],
        "lat": "30.5891",
        "long": "-88.1764"
    },
    {
        "name": "Hartselle",
        "slug": "hartselle",
        "county": "Morgan County",
        "zip": "35640",
        "zips": ["35640"],
        "lat": "34.4443",
        "long": "-86.9333"
    },
    {
        "name": "Fort Payne",
        "slug": "fort-payne",
        "county": "DeKalb County",
        "zip": "35967",
        "zips": ["35967", "35968"],
        "lat": "34.4440",
        "long": "-85.7197"
    }
]

# Services Data
services = [
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
    {"slug": "Detailing-Mobile-AL", "name": "Detailing"}, # Note casing
    {"slug": "laundry-services", "name": "Laundry Services"},
    {"slug": "window-cleaning", "name": "Window Cleaning"}
]

def generate_pages():
    # Read Template
    if not os.path.exists(os.path.join(TEMPLATE_DIR, TEMPLATE_FILE)):
        print(f"Error: Template file not found at {TEMPLATE_DIR}/{TEMPLATE_FILE}")
        return

    with open(os.path.join(TEMPLATE_DIR, TEMPLATE_FILE), 'r', encoding='utf-8') as f:
        template_content = f.read()

    new_sitemap_entries = []

    for city in cities:
        print(f"Generating Hub Page for {city['name']}...")
        
        # Create Directory
        if not os.path.exists(city['slug']):
            os.makedirs(city['slug'])

        # Prepare Content
        content = template_content
        
        # Replacements
        # Basic City/State/Zip
        content = content.replace('Foley', city['name'])
        content = content.replace('36535', city['zip'])
        content = content.replace('Baldwin County', city['county']) # County Replacement
        
        # Schema Geo
        content = content.replace('30.4066', city['lat'])
        content = content.replace('-87.6836', city['long'])
        
        # URL / Canonical
        # Note: If template has /foley/ in canonical, we replace with /city['slug']/
        content = content.replace('/foley/', f'/{city["slug"]}/')
        
        # Service Area Zips (JS Array)
        zip_pattern = r'const serviceZips = \[[^\]]*\];'
        new_zips_js = 'const serviceZips = [\n      ' + ', '.join([f'"{z}"' for z in city['zips']]) + '\n    ];'
        content = re.sub(zip_pattern, new_zips_js, content)

        # 6. SAFETY CLEANUP (Remove Hidden Text)
        content = re.sub(r'<div style="display:none;">.*?</div>', '', content, flags=re.DOTALL)

        # 7. INJECT SERVICES MATRIX
        # We need to inject a section with links to all services in this city
        
        links_html = f'<div class="grid grid-cols-1 md:grid-cols-3 gap-4 mt-4 text-center">'
        for s in services:
            s_target_slug = s['slug'].replace('-Mobile-AL', '').replace('-mobile-al', '')
            link_url = f"/{city['slug']}/{s_target_slug}/"
            links_html += f'<a href="{link_url}" class="block p-4 bg-gray-50 hover:bg-blue-100 rounded-lg transition border border-gray-200 text-blue-900 font-semibold">{s["name"]} in {city["name"]}</a>'
        links_html += '</div>'
        
        services_section = f'''
        <section class="py-16 bg-white">
          <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <h2 class="text-3xl font-bold text-center text-gray-900 mb-8">Professional Cleaning Services in {city['name']}</h2>
            <p class="text-center text-lg text-gray-600 mb-10 max-w-3xl mx-auto">
              We offer a complete range of residential and commercial cleaning solutions tailored to {city['name']} residents. 
              Click below to explore our specialized services.
            </p>
            {links_html}
          </div>
        </section>
        '''
        
        # Inject before Footer (assuming Footer starts near end or looks for specific tag)
        # We'll look for <footer and inject before it
        # if '<footer' in content:
        #     content = content.replace('<footer', f'{services_section}\n<footer')
        # else:
        #      # Fallback: append to body
        #     content = content.replace('</body>', f'{services_section}\n</body>')


        # Write File
        target_file = os.path.join(city['slug'], 'index.html')
        with open(target_file, 'w', encoding='utf-8') as f:
            f.write(content)
            
        # Sitemap Entry
        new_sitemap_entries.append(f'  <url>\n    <loc>https://www.zoiriscleaningservices.com/{city["slug"]}/</loc>\n    <lastmod>2026-02-14</lastmod>\n    <changefreq>weekly</changefreq>\n    <priority>0.9</priority>\n  </url>')

    # Update Sitemap
    sitemap_path = 'sitemap.xml'
    if os.path.exists(sitemap_path):
        with open(sitemap_path, 'r', encoding='utf-8') as f:
            sitemap_content = f.read()
        
        # Check if we need to add new entries or if they already exist
        # Simple check: if the URL is not in sitemap, add it.
        # But we generated a list of all 45 cities.
        # Let's just append ANY that are missing.
        
        final_entries_to_add = []
        for entry in new_sitemap_entries:
            # Extract URL to check
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
                print(f"Added {len(final_entries_to_add)} new hub pages to sitemap.xml.")
            else:
                 print("Error: Could not find </urlset> in sitemap.xml")
        else:
            print("Sitemap already contains all hub pages.")

    else:
        print("Error: sitemap.xml not found")

if __name__ == "__main__":
    generate_pages()
