import os
import shutil
import re

# Target Cities Data (Same as create_locations.py)
# Target Cities Data (Same as create_locations.py)
cities = [
    {
        "name": "Birmingham",
        "slug": "birmingham",
        "county": "Jefferson County",
        "zip": "35203",
        "zips": ["35203", "35204", "35205", "35206", "35209", "35211", "35212", "35222", "35233", "35234"],
        "lat": "33.5186",
        "long": "-86.8104",
        "neighborhoods": ["Avondale", "Highland Park", "Forest Park", "Crestline", "Glen Iris", "Southside", "Five Points South", "Crestwood", "Redmont Park"]
    },
    {
        "name": "Montgomery",
        "slug": "montgomery",
        "county": "Montgomery County",
        "zip": "36104",
        "zips": ["36104", "36105", "36106", "36107", "36108", "36109", "36110", "36111", "36116", "36117"],
        "lat": "32.3668",
        "long": "-86.3000",
        "neighborhoods": ["Garden District", "Cloverdale", "Capitol Heights", "Old Cloverdale", "Deer Creek", "Hampstead", "Wynlakes", "Eastwood"]
    },
    {
        "name": "Huntsville",
        "slug": "huntsville",
        "county": "Madison County",
        "zip": "35801",
        "zips": ["35801", "35802", "35803", "35805", "35806", "35810", "35811", "35816", "35824"],
        "lat": "34.7304",
        "long": "-86.5861",
        "neighborhoods": ["Five Points", "Blossomwood", "Hampton Cove", "Jones Valley", "Providence", "South Huntsville", "Twickenham", "Monte Sano"]
    },
    {
        "name": "Tuscaloosa",
        "slug": "tuscaloosa",
        "county": "Tuscaloosa County",
        "zip": "35401",
        "zips": ["35401", "35404", "35405", "35406", "35453", "35456", "35473", "35475", "35476", "35487"],
        "lat": "33.2098",
        "long": "-87.5692",
        "neighborhoods": ["Historic District", "The Strip", "Druid City", "Forest Lake", "Alberta City", "Hillcrest", "Northport", "Woodland Forest"]
    },
    {
        "name": "Hoover",
        "slug": "hoover",
        "county": "Jefferson County",
        "zip": "35216",
        "zips": ["35216", "35226", "35244", "35236", "35022", "35124"],
        "lat": "33.4054",
        "long": "-86.8114",
        "neighborhoods": ["Ross Bridge", "Greystone", "The Preserve", "Bluff Park", "Trace Crossings", "Inverness", "Riverchase"]
    },
    {
        "name": "Dothan",
        "slug": "dothan",
        "county": "Houston County",
        "zip": "36301",
        "zips": ["36301", "36303", "36305", "36321", "36350"],
        "lat": "31.2232",
        "long": "-85.3905",
        "neighborhoods": ["Garden District", "Highland Park", "Westgate", "Chapelwood", "Timbercreek", "Woodland Heights", "Meadow Lakes"]
    },
    {
        "name": "Auburn",
        "slug": "auburn",
        "county": "Lee County",
        "zip": "36830",
        "zips": ["36830", "36832", "36849", "36801", "36879"],
        "lat": "32.6099",
        "long": "-85.4808",
        "neighborhoods": ["Moores Mill", "Camden Ridge", "Grove Hill", "Yarbrough Farms", "Asheton Lakes", "Cary Woods", "Shelton Park"]
    },
    {
        "name": "Decatur",
        "slug": "decatur",
        "county": "Morgan County",
        "zip": "35601",
        "zips": ["35601", "35603", "35699", "35640", "35670"],
        "lat": "34.6059",
        "long": "-86.9833",
        "neighborhoods": ["Delano Park", "Burningtree", "Austinville", "Old Decatur", "Albany", "Russell Forest"]
    },
    {
        "name": "Madison",
        "slug": "madison",
        "county": "Madison County",
        "zip": "35758",
        "zips": ["35758", "35756", "35757", "35896"],
        "lat": "34.6993",
        "long": "-86.7483",
        "neighborhoods": ["Clift Farm", "Town Madison", "Rainbow Mountain", "Edgewater", "Highland Lakes", "Shiloh Creek"]
    },
    {
        "name": "Florence",
        "slug": "florence",
        "county": "Lauderdale County",
        "zip": "35630",
        "zips": ["35630", "35633", "35634", "35617", "35645"],
        "lat": "34.7998",
        "long": "-87.6773",
        "neighborhoods": ["Seven Points", "McFarland Heights", "Hickory Hills", "Forest Hills", "Downtown Florence", "Heathrow"]
    },
    # Phase 2 Cities (Tier 2)
    {
        "name": "Phenix City",
        "slug": "phenix-city",
        "county": "Russell County",
        "zip": "36867",
        "zips": ["36867", "36868", "36869"],
        "lat": "32.4709",
        "long": "-85.0007",
        "neighborhoods": ["Kaolin", "Ladonia", "Three Points", "Girard", "Summerville", "Brickyard"]
    },
    {
        "name": "Prattville",
        "slug": "prattville",
        "county": "Autauga County",
        "zip": "36067",
        "zips": ["36066", "36067", "36068"],
        "lat": "32.4640",
        "long": "-86.4597",
        "neighborhoods": ["Highland Ridge", "Glennbrooke", "Hedgefield", "Silver Hills", "Capitol Hill", "The Ridge"]
    },
    {
        "name": "Gadsden",
        "slug": "gadsden",
        "county": "Etowah County",
        "zip": "35901",
        "zips": ["35901", "35903", "35904", "35905"],
        "lat": "34.0143",
        "long": "-86.0066",
        "neighborhoods": ["Noccalula Falls", "Clubview Heights", "Alabama City", "East Gadsden", "Walex", "Mountainboro"]
    },
    {
        "name": "Vestavia Hills",
        "slug": "vestavia-hills",
        "county": "Jefferson County",
        "zip": "35216",
        "zips": ["35216", "35226", "35242", "35243"],
        "lat": "33.4487",
        "long": "-86.7878",
        "neighborhoods": ["Liberty Park", "Cahaba Heights", "Rocky Ridge", "Tanglewood", "Country Club", "Dolly Ridge"]
    },
    {
        "name": "Alabaster",
        "slug": "alabaster",
        "county": "Shelby County",
        "zip": "35007",
        "zips": ["35007", "35114"],
        "lat": "33.2442",
        "long": "-86.8163",
        "neighborhoods": ["Weatherly", "Siluria", "Navajo Hills", "Saddle Lake Farms", "Sterling Gate", "Park Place"]
    },
    {
        "name": "Opelika",
        "slug": "opelika",
        "county": "Lee County",
        "zip": "36801",
        "zips": ["36801", "36804"],
        "lat": "32.6454",
        "long": "-85.3782",
        "neighborhoods": ["Northside", "Floral Park", "Historic District", "Glenn", "Pepperell", "Grand National"]
    },
    {
        "name": "Enterprise",
        "slug": "enterprise",
        "county": "Coffee County",
        "zip": "36330",
        "zips": ["36330", "36331"],
        "lat": "31.3151",
        "long": "-85.8552",
        "neighborhoods": ["Shellfield Area", "Tartar Lake", "Boll Weevil", "Yancey Parker", "College Street", "Dauphin"]
    },
    {
        "name": "Bessemer",
        "slug": "bessemer",
        "county": "Jefferson County",
        "zip": "35020",
        "zips": ["35020", "35022", "35023"],
        "lat": "33.4018",
        "long": "-86.9544",
        "neighborhoods": ["Hopewell", "Greenwood", "Eastern Valley", "McCalla", "Lakewood", "Shannon"]
    },
    {
        "name": "Homewood",
        "slug": "homewood",
        "county": "Jefferson County",
        "zip": "35209",
        "zips": ["35209", "35259"],
        "lat": "33.4717",
        "long": "-86.8008",
        "neighborhoods": ["Edgewood", "Hollywood", "Rosedale", "West Homewood", "Mayfair", "Oak Grove"]
    },
    {
        "name": "Athens",
        "slug": "athens",
        "county": "Limestone County",
        "zip": "35611",
        "zips": ["35611", "35613", "35614"],
        "lat": "34.8028",
        "long": "-86.9716",
        "neighborhoods": ["Canebrake", "Lindsay Lane", "Downtown Athens", "Frenchs Mill", "Oakdale", "Country Club"]
    },
    {
        "name": "Northport",
        "slug": "northport",
        "county": "Tuscaloosa County",
        "zip": "35473",
        "zips": ["35473", "35475", "35476"],
        "lat": "33.2290",
        "long": "-87.5772",
        "neighborhoods": ["Northwood Lake", "Clear Creek", "Grand Pointe", "Shirley Farms", "Huntington Place", "Forest Glen"]
    },
    {
        "name": "Anniston",
        "slug": "anniston",
        "county": "Calhoun County",
        "zip": "36201",
        "zips": ["36201", "36206", "36207"],
        "lat": "33.6598",
        "long": "-85.8316",
        "neighborhoods": ["Golden Springs", "Saks", "Weaver", "Oxford Lake", "Glen Addie", "Lenlock"]
    },
    {
        "name": "Oxford",
        "slug": "oxford",
        "county": "Calhoun County",
        "zip": "36203",
        "zips": ["36203"],
        "lat": "33.6146",
        "long": "-85.8350",
        "neighborhoods": ["Choccolocco", "Bynum", "Coldwater", "DeArmanville", "Friendship", "Leonards"]
    },
    {
        "name": "Albertville",
        "slug": "albertville",
        "county": "Marshall County",
        "zip": "35950",
        "zips": ["35950", "35951"],
        "lat": "34.2676",
        "long": "-86.2089",
        "neighborhoods": ["Horton", "Asbury", "Martling", "Saratoga", "High Point", "Country Club"]
    },
    {
        "name": "Selma",
        "slug": "selma",
        "county": "Dallas County",
        "zip": "36701",
        "zips": ["36701", "36703"],
        "lat": "32.4073",
        "long": "-87.0211",
        "neighborhoods": ["Old Town Historic District", "Valley Creek", "West Selma", "Riverview", "Byrd Siding", "Burnsville"]
    },
    # Phase 3 Cities (Tier 3)
    {
        "name": "Foley",
        "slug": "foley",
        "county": "Baldwin County",
        "zip": "36535",
        "zips": ["36535", "36536"],
        "lat": "30.4066",
        "long": "-87.6836",
        "neighborhoods": ["Glenlakes", "Cottages on the Greene", "Ashford Park", "Ledgewick", "River Oaks", "Live Oak Village"]
    },
    {
        "name": "Mountain Brook",
        "slug": "mountain-brook",
        "county": "Jefferson County",
        "zip": "35213",
        "zips": ["35213", "35223"],
        "lat": "33.4859",
        "long": "-86.7461",
        "neighborhoods": ["Crestline Village", "English Village", "Mountain Brook Village", "Cherokee Bend", "Brookwood Forest", "Overton"]
    },
    {
        "name": "Cullman",
        "slug": "cullman",
        "county": "Cullman County",
        "zip": "35055",
        "zips": ["35055", "35056", "35057", "35058"],
        "lat": "34.1748",
        "long": "-86.8436",
        "neighborhoods": ["Heritage Park", "East Point", "West Point", "Good Hope", "South Cullman", "Bolte"]
    },
    {
        "name": "Troy",
        "slug": "troy",
        "county": "Pike County",
        "zip": "36081",
        "zips": ["36081", "36079"],
        "lat": "31.8088",
        "long": "-85.9697",
        "neighborhoods": ["College Hill", "Heritage Ridge", "North Hills", "Lakeview", "Southland", "Oak Park"]
    },
    {
        "name": "Helena",
        "slug": "helena",
        "county": "Shelby County",
        "zip": "35080",
        "zips": ["35080", "35022"],
        "lat": "33.2965",
        "long": "-86.8417",
        "neighborhoods": ["Hillsboro", "Old Cahaba", "Riverwoods", "Fieldstone Park", "Silver Lakes", "Long Leaf Lake"]
    },
    {
        "name": "Calera",
        "slug": "calera",
        "county": "Shelby County",
        "zip": "35040",
        "zips": ["35040"],
        "lat": "33.1021",
        "long": "-86.7533",
        "neighborhoods": ["Timberline", "Waterford", "The Enclave", "Savannah Pointe", "Camden Cove", "Emerald Ridge"]
    },
    {
        "name": "Muscle Shoals",
        "slug": "muscle-shoals",
        "county": "Colbert County",
        "zip": "35661",
        "zips": ["35661", "35662"],
        "lat": "34.7448",
        "long": "-87.6675",
        "neighborhoods": ["Highland Park", "Rivermont", "Ford City", "Avalon", "Webster", "Wilson Dam"]
    },
    {
        "name": "Saraland",
        "slug": "saraland",
        "county": "Mobile County",
        "zip": "36571",
        "zips": ["36571"],
        "lat": "30.8207",
        "long": "-88.0706",
        "neighborhoods": ["Celeste", "Kali Oka", "Shelton Beach", "Bayou Sara", "Shadow Creek", "Spartan"]
    },
    {
        "name": "Gardendale",
        "slug": "gardendale",
        "county": "Jefferson County",
        "zip": "35071",
        "zips": ["35071"],
        "lat": "33.6457",
        "long": "-86.8117",
        "neighborhoods": ["Fieldstown", "Mt. Olive", "Snow Rogers", "Pinemeadow", "Moncrief", "Bragg"]
    },
    {
        "name": "Chelsea",
        "slug": "chelsea",
        "county": "Shelby County",
        "zip": "35043",
        "zips": ["35043"],
        "lat": "33.3421",
        "long": "-86.6297",
        "neighborhoods": ["Chelsea Park", "Yellowleaf", "Forest Lakes", "Highland Lakes", "Chesser", "Liberty Park"]
    },
    {
        "name": "Hueytown",
        "slug": "hueytown",
        "county": "Jefferson County",
        "zip": "35023",
        "zips": ["35023"],
        "lat": "33.4392",
        "long": "-86.9972",
        "neighborhoods": ["Virginia Mines", "Edenwood", "Garywood", "North Highlands", "Brooklane", "Dolomite"]
    },
    {
        "name": "Millbrook",
        "slug": "millbrook",
        "county": "Elmore County",
        "zip": "36054",
        "zips": ["36054"],
        "lat": "32.4787",
        "long": "-86.3683",
        "neighborhoods": ["Grandview Pines", "Cobblestone", "Mill Ridge", "Deatsville", "Coosada", "Thornfield"]
    },
    {
        "name": "Tillmans Corner",
        "slug": "tillmans-corner",
        "county": "Mobile County",
        "zip": "36619",
        "zips": ["36619"],
        "lat": "30.5891",
        "long": "-88.1764",
        "neighborhoods": ["Cypress Shores", "Theodore", "Belle Fontaine", "Rangeline", "Three Notch", "Meadow Lake"]
    },
    {
        "name": "Hartselle",
        "slug": "hartselle",
        "county": "Morgan County",
        "zip": "35640",
        "zips": ["35640"],
        "lat": "34.4443",
        "long": "-86.9333",
        "neighborhoods": ["Crestline", "Sparkman", "Walker", "Bethel", "Shoal Creek", "Somerville"]
    },
    {
        "name": "Fort Payne",
        "slug": "fort-payne",
        "county": "DeKalb County",
        "zip": "35967",
        "zips": ["35967", "35968"],
        "lat": "34.4440",
        "long": "-85.7197",
        "neighborhoods": ["Beeson", "Wills Valley", "Desoto", "Minvale", "Allen", "Chavies"]
    }
]

# Services Data
# Note: We assume the source template exists in services/[slug]/index.html
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


def create_matrix():
    new_sitemap_entries = []

    for city in cities:
        print(f"Processing City: {city['name']}...")
        
        for svc in services:
            # Source Template Path
            # We look for the service template in services/[slug]/index.html
            # Note: For 'Detailing-Mobile-AL', the folder is 'Detailing-Mobile-AL'
            source_dir = os.path.join('services', svc['slug'])
            source_file = os.path.join(source_dir, 'index.html')
            
            if not os.path.exists(source_file):
                print(f"  Skipping {svc['slug']}: Template not found at {source_file}")
                # Fallback: maybe the folder name doesn't match the slug exactly?
                # For now, skip.
                continue

            # Target Directory: [city]/[service]/
            # But wait, [service] slug might be long or have 'Mobile-AL' in it.
            # We should probably clean up the target slug.
            # E.g. 'Detailing-Mobile-AL' -> 'detailing' for the subfolder?
            # User request: "location x service matrix".
            # Usually structure is: birmingham/house-cleaning/
            # For 'Detailing-Mobile-AL', we should probably rename it to just 'detailing' or keep it?
            # Keeping it simple: reuse the slug, but maybe strip '-Mobile-AL' or similar if present.
            
            target_svc_slug = svc['slug']
            if target_svc_slug.endswith('-Mobile-AL'):
                 target_svc_slug = target_svc_slug.replace('-Mobile-AL', '')
            if target_svc_slug.endswith('-mobile-al'):
                 target_svc_slug = target_svc_slug.replace('-mobile-al', '')
            
            target_dir = os.path.join(city['slug'], target_svc_slug)
            target_file = os.path.join(target_dir, 'index.html')
            
            # Create Directory
            if not os.path.exists(target_dir):
                os.makedirs(target_dir)

            # Read Template
            with open(source_file, 'r', encoding='utf-8') as f:
                content = f.read()

            # --- REPLACEMENTS ---
            
            # 1. City Name Replacement
            # Robust replacements for "Mobile"
            # Order matters: Specific to general
            
            # "Mobile, AL" -> "Birmingham, AL"
            content = content.replace('Mobile, AL', f"{city['name']}, AL")
            
            # "Mobile AL" -> "Birmingham AL" (Common in keywords)
            content = content.replace('Mobile AL', f"{city['name']} AL")
            
            # "Mobile Alabama" -> "Birmingham Alabama"
            content = content.replace('Mobile Alabama', f"{city['name']} Alabama")
            
            # "in Mobile" -> "in Birmingham"
            content = content.replace('in Mobile', f"in {city['name']}")
            
            # "Serving Mobile" -> "Serving Birmingham"
            content = content.replace('Serving Mobile', f"Serving {city['name']}")
            
            # "Mobile &" -> "Birmingham &" (e.g. "Mobile & Baldwin County")
            content = content.replace('Mobile &', f"{city['name']} &")
            
            # "cleaning Mobile" -> "cleaning Birmingham"
            content = content.replace('cleaning Mobile', f'cleaning {city["name"]}')
            
            # "cleaners Mobile" -> "cleaners Birmingham"
            content = content.replace('cleaners Mobile', f'cleaners {city["name"]}')
            
            # "company Mobile" -> "company Birmingham"
            content = content.replace('company Mobile', f'company {city["name"]}')
            
            # "service Mobile" -> "service Birmingham"
            content = content.replace('service Mobile', f'service {city["name"]}')
            
            # General "Mobile" replace is risky due to "Mobile Home", but let's see.
            # "Mobile Home" -> "Manufactured Home" to avoid confusion? 
            # Or just skip generic "Mobile".
            
            # 2. County Replacement
            content = content.replace('Baldwin County', city['county'])
            
            # 3. Zip Codes
            content = content.replace('36602', city['zip']) # Main zip
            
            # Service Zips Array
            zip_pattern = r'const serviceZips = \[[^\]]*\];'
            new_zips_js = 'const serviceZips = [\n      ' + ', '.join([f'"{z}"' for z in city['zips']]) + '\n    ];'
            content = re.sub(zip_pattern, new_zips_js, content)

            # 4. Geo Coordinates
            # Template might have Mobile coords: 30.6944, -88.0431
            # We should find and replace them.
            # We can look for the schema block or just replacing known values.
            # Mobile Lat/Long approx
            content = content.replace('30.6944', city['lat'])
            content = content.replace('-88.0431', city['long'])
            
            # 5. URL / Canonical / Links
            # The template might refer to its own canonical: href=".../house-cleaning/"
            # We need to change it to: href=".../birmingham/house-cleaning/"
            
            # Canonical
            # <link rel="canonical" href="https://www.zoiriscleaningservices.com/house-cleaning/">
            # Regex or replace
            # Note: svc['slug'] is the original slug (e.g., 'house-cleaning')
            old_canonical_slug = svc['slug']
            if not old_canonical_slug.endswith('/'):
                old_canonical_slug += '/'
            
            # So just fix Canonical and OG:URL if present.
            kanonical_regex = r'<link rel="canonical" href="https://www.zoiriscleaningservices.com/([^"]+)"'
            # We construct the new URL:
            new_url = f"https://www.zoiriscleaningservices.com/{city['slug']}/{target_svc_slug}/"
            
            content = re.sub(kanonical_regex, f'<link rel="canonical" href="{new_url}"', content)
            
            # Schema ID/URL
            content = content.replace(f"https://www.zoiriscleaningservices.com/{svc['slug']}/", new_url)

            # 6. SAFETY CLEANUP (Remove Hidden Text)
            # Remove <div style="display:none;">...</div> blocks
            # This is critical for Google Safety compliance
            content = re.sub(r'<div style="display:none;">.*?</div>', '', content, flags=re.DOTALL)
            
            # --- ADVANCED SEO INJECTION ---
            
            # 7. Neighborhoods Injection
            # Create a comma-separated list of neighborhoods
            hoods_list = ", ".join(city['neighborhoods'])
            
            # Inject into Meta Description (if space permits, or just general)
            # "Serving Mobile & Jefferson County" -> "Serving Birmingham, Avondale, Highland Park & Jefferson County"
            # Getting a bit long, let's just ensure it's in the body.
            
            # Inject Detailed "Areas Served" Paragraph
            # We look for a good spot. The template usually ends with some content.
            # We will append a section before the footer or near the bottom of the main content.
            # Let's look for the </main> tag if it exists, or just before </body>?
            # The template is simple. Let's start by preparing the HTML.
            
            areas_served_html = f'''
            <section class="py-10 bg-white">
              <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                <h2 class="text-3xl font-bold text-gray-900 mb-6">Proudly Serving {city['name']} Neighborhoods</h2>
                <p class="text-lg text-gray-700">
                  Zoiris Cleaning Services is your trusted local cleaner in <strong>{city['name']}</strong>. 
                  We actively serve residents and businesses in <strong>{hoods_list}</strong>, and surrounding areas. 
                  Whether you are in {city['neighborhoods'][0]} or {city['neighborhoods'][-1]}, our team is ready to help.
                </p>
              </div>
            </section>
            '''
            
            # 8. Internal Linking Silo ("Services in [City]")
            # Generate a list of links to OTHER services in THIS city.
            links_html = f'<div class="grid grid-cols-1 md:grid-cols-3 gap-4 mt-4">'
            for s in services:
                # Build URL: /[city_slug]/[service_slug]/
                # Handle the 'Detailing' edge case again if needed, but we standardized targets.
                # The target slug logic:
                s_target_slug = s['slug'].replace('-Mobile-AL', '').replace('-mobile-al', '')
                link_url = f"/{city['slug']}/{s_target_slug}/"
                links_html += f'<a href="{link_url}" class="text-blue-600 hover:text-blue-800 hover:underline">{s["name"]} in {city["name"]}</a>'
            links_html += '</div>'
            
            internal_links_section = f'''
            <section class="py-10 bg-gray-50">
              <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                <h2 class="text-2xl font-bold text-gray-900 mb-4">More Cleaning Services in {city['name']}</h2>
                {links_html}
              </div>
            </section>
            '''
            
            # INJECTION: We append these sections before the footer or body end.
            # Searching for a footer marker or just before </body>
            # We'll inject before `</body>`.
            # content = content.replace('</body>', f'{areas_served_html}\n{internal_links_section}\n</body>')

            # 9. Breadcrumb Schema
            # https://schema.org/BreadcrumbList
            breadcrumb_schema = f'''
            <script type="application/ld+json">
            {{
              "@context": "https://schema.org",
              "@type": "BreadcrumbList",
              "itemListElement": [
                {{
                  "@type": "ListItem",
                  "position": 1,
                  "name": "Home",
                  "item": "https://www.zoiriscleaningservices.com/"
                }},
                {{
                  "@type": "ListItem",
                  "position": 2,
                  "name": "{city['name']}",
                  "item": "https://www.zoiriscleaningservices.com/{city['slug']}/"
                }},
                {{
                  "@type": "ListItem",
                  "position": 3,
                  "name": "{svc['name']}",
                  "item": "{new_url}"
                }}
              ]
            }}
            </script>
            '''
            
            # Inject Breadcrumb Schema before </head>
            content = content.replace('</head>', f'{breadcrumb_schema}\n</head>')

            # 10. Enhance Area Served in LocalBusiness Schema
            # We already replaced "Birmingham, AL". Let's add the neighborhoods to the array.
            # We look for "servesLocation": [ ... ]
            # It currently has generics. We can try to replace the whole block or regex insert.
            # The block is:
            # "servesLocation": [
            #     "Birmingham, AL",
            #     "Jefferson County, AL",
            #     ...
            # ]
            # We can use regex to find `"servesLocation": \[` and insert our hoods.
            hoods_quoted = [f'"{h}, {city["name"]}, AL"' for h in city['neighborhoods']]
            hoods_json_str = ",\n    ".join(hoods_quoted)
            
            # Regex to find the start of the array and insert
            content = re.sub(r'("servesLocation":\s*\[)', f'\\1\n    {hoods_json_str},', content)

            # Schema specific replacements (Optimization of previous step)
            content = content.replace('"addressLocality": "Mobile"', f'"addressLocality": "{city["name"]}"')
            content = content.replace('"streetAddress": "Downtown Mobile"', f'"streetAddress": "Downtown {city["name"]}"')
            content = content.replace('"name": "Mobile"', f'"name": "{city["name"]}"') 

            with open(target_file, 'w', encoding='utf-8') as f:
                f.write(content)
            
            # Sitemap
            new_sitemap_entries.append(f'  <url>\n    <loc>{new_url}</loc>\n    <lastmod>2026-02-14</lastmod>\n    <changefreq>monthly</changefreq>\n    <priority>0.8</priority>\n  </url>')
            
            print(f"  Generated: {target_file}")

    # Update Sitemap (with Deduplication)
    sitemap_path = 'sitemap.xml'
    if os.path.exists(sitemap_path):
        with open(sitemap_path, 'r', encoding='utf-8') as f:
            sitemap_content = f.read()
        
        # Simple extraction of existing URLs to avoid duplicates
        existing_urls = set(re.findall(r'<loc>(.*?)</loc>', sitemap_content))
        
        unique_new_entries = []
        for entry in new_sitemap_entries:
            # Extract URL from the new entry string
            match = re.search(r'<loc>(.*?)</loc>', entry)
            if match:
                url = match.group(1)
                if url not in existing_urls:
                    unique_new_entries.append(entry)
                    existing_urls.add(url) # Add to set to prevent internal duplicates
        
        if unique_new_entries:
            if '</urlset>' in sitemap_content:
                new_block = '\n'.join(unique_new_entries)
                new_content = sitemap_content.replace('</urlset>', new_block + '\n</urlset>')
                
                with open(sitemap_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                print(f"Updated sitemap.xml with {len(unique_new_entries)} new entries.")
            else:
                print("Error: </urlset> not found in sitemap.xml")
        else:
            print("No new unique URLs to add to sitemap.")

        # Deduplication clean-up (Optional: strictly standardize file)
        # For now, the incremental add with check is sufficient.


if __name__ == "__main__":
    create_matrix()
