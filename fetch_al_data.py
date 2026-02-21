import urllib.request
import csv
import json

url = "https://raw.githubusercontent.com/kelvins/US-Cities-Database/main/csv/us_cities.csv"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})

try:
    with urllib.request.urlopen(req) as response:
        lines = [l.decode('utf-8') for l in response.readlines()]
        reader = csv.DictReader(lines)
        al_cities = []
        for row in reader:
            if row['STATE_CODE'] == 'AL':
                al_cities.append({
                    "name": row['CITY'],
                    "slug": row['CITY'].lower().replace(' ', '-').replace("'", ""),
                    "county": row['COUNTY'] + " County",
                    "lat": row['LATITUDE'],
                    "long": row['LONGITUDE']
                })
        
        # We need to deduplicate cities (since the dataset might have multiple zips per city, though this specific one usually has one row per city/state)
        unique_cities = {}
        for c in al_cities:
            unique_cities[c['slug']] = c
            
        final_list = list(unique_cities.values())
        print(f"Found {len(final_list)} unique cities/towns in Alabama dataset.")
        
        with open('al_cities_raw.json', 'w') as f:
            json.dump(final_list, f, indent=4)
            
except Exception as e:
    print(f"Error fetching data: {e}")
