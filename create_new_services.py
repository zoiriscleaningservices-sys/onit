import os
import re
import shutil

# Services that use the House Cleaning template (Residential/Property Management)
residential_services = [
    {"slug": "luxury-estate-cleaning", "name": "Luxury Estate Cleaning", "desc": "Premium luxury estate cleaning services. Meticulous, discrete, and thorough cleaning for high-end properties and large estates."},
    {"slug": "luxury-estate-management", "name": "Luxury Estate Management", "desc": "Comprehensive luxury estate management services. We handle maintenance, cleaning, and day-to-day property oversight for premium homes."},
    {"slug": "home-watch-services", "name": "Home Watch Services", "desc": "Professional home watch services. We provide routine inspections and maintenance checks for unoccupied homes and vacation properties."},
    {"slug": "property-management-janitorial", "name": "Property Management Janitorial", "desc": "Reliable janitorial services for property managers. Keep your managed properties spotless and well-maintained with our professional team."},
    {"slug": "property-maintenance", "name": "Property Maintenance", "desc": "Complete property maintenance services. From minor repairs to routine upkeep, we ensure your residential or commercial property stays in top condition."},
    {"slug": "airbnb-vacation-rental-management", "name": "Airbnb & Vacation Rental Management", "desc": "Full-service Airbnb and vacation rental management. We handle cleanings, restocking, and property maintenance to keep your guests happy."},
    {"slug": "gutter-cleaning", "name": "Gutter Cleaning", "desc": "Professional gutter cleaning services. Protect your property from water damage with our safe and effective gutter clearing out."}
]

# Services that use the Commercial Cleaning template (Commercial/Industrial)
commercial_services = [
    {"slug": "office-janitorial-services", "name": "Office Janitorial Services", "desc": "Top-rated office janitorial services. We provide daily, weekly, or monthly cleaning to keep your workspace pristine and professional."},
    {"slug": "janitorial-cleaning-services", "name": "Janitorial Cleaning Services", "desc": "Comprehensive janitorial cleaning services for businesses of all sizes. Dependable, thorough, and customized to your facility's needs."},
    {"slug": "medical-dental-facility-cleaning", "name": "Medical & Dental Facility Cleaning", "desc": "Specialized medical and dental facility cleaning. We adhere to strict hygiene and sanitation standards to maintain a safe healthcare environment."},
    {"slug": "industrial-warehouse-cleaning", "name": "Industrial & Warehouse Cleaning", "desc": "Heavy-duty industrial and warehouse cleaning services. We handle large-scale sweeping, scrubbing, and degreasing for safe operations."},
    {"slug": "floor-stripping-waxing", "name": "Floor Stripping & Waxing", "desc": "Professional floor stripping and waxing. Restore the shine and protect your commercial floors with our expert care."},
    {"slug": "gym-fitness-center-cleaning", "name": "Gym & Fitness Center Cleaning", "desc": "Thorough gym and fitness center cleaning. We sanitize equipment, locker rooms, and workout floors to provide a safe space for your members."},
    {"slug": "school-daycare-cleaning", "name": "School & Daycare Cleaning", "desc": "Safe and effective school and daycare cleaning. We use non-toxic products to disinfect classrooms, play areas, and restrooms."},
    {"slug": "church-worship-center-cleaning", "name": "Church & Worship Center Cleaning", "desc": "Respectful church and worship center cleaning services. We ensure your sanctuary and gathering spaces are welcoming and pristine."},
    {"slug": "solar-panel-cleaning", "name": "Solar Panel Cleaning", "desc": "Professional solar panel cleaning services. Maximize your energy efficiency safely with our spotless, streak-free washing techniques."}
]

def create_pages(services, template_dir, placeholder_name):
    template_path = os.path.join('services', template_dir, 'index.html')
    if not os.path.exists(template_path):
        print(f"Template not found: {template_path}")
        return

    with open(template_path, 'r', encoding='utf-8') as f:
        template_content = f.read()

    for svc in services:
        target_dir = os.path.join('services', svc['slug'])
        target_file = os.path.join(target_dir, 'index.html')
        
        if not os.path.exists(target_dir):
            os.makedirs(target_dir)

        content = template_content
        
        # We need to replace instances of the template's service name with in the new one
        # Because we don't want to mess up HTML tags, let's do targeted replacements.
        
        # Title
        content = re.sub(r'<title>.*?</title>', f'<title>Best {svc["name"]} in Mobile | 5-Star Rated</title>', content)
        
        # Meta description
        content = re.sub(r'<meta name="description" content=".*?">', f'<meta name="description" content="{svc["desc"]}">', content)
        
        # Replace the literal string like "Professional House Cleaning" or "House Cleaning"
        content = content.replace(placeholder_name, svc['name'])
        
        # Sometimes it might be lowercase inside URLs or specific elements? Let's just do safe replacements.
        content = content.replace(f"/{template_dir}/", f"/{svc['slug']}/")

        with open(target_file, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Generated: {target_file}")

if __name__ == "__main__":
    print("Generating Residential / Property Services...")
    create_pages(residential_services, 'house-cleaning', 'House Cleaning')
    
    print("\nGenerating Commercial / Industrial Services...")
    create_pages(commercial_services, 'commercial-cleaning', 'Commercial Cleaning')

