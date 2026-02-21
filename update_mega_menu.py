import os
import re

desktop_menu = """<div class="absolute -left-32 top-full hidden group-hover:grid grid-cols-3 gap-4 w-[900px] z-50 pt-2">
  <div class="flex flex-col space-y-2 bg-white/95 p-4 rounded-xl shadow-2xl backdrop-blur-md border border-gray-200">
      <h4 class="text-xl font-bold text-gray-900 border-b-2 border-indigo-500 pb-2 mb-2 text-center">Residential & Property</h4>
      <a class="contact-button text-sm hover:scale-105 transition-transform text-center py-2" href="/services/house-cleaning/">House Cleaning</a>
      <a class="contact-button text-sm hover:scale-105 transition-transform text-center py-2" href="/services/deep-cleaning/">Deep Cleaning</a>
      <a class="contact-button text-sm hover:scale-105 transition-transform text-center py-2" href="/services/move-in-cleaning/">Move-In Cleaning</a>
      <a class="contact-button text-sm hover:scale-105 transition-transform text-center py-2" href="/services/move-out-cleaning/">Move-Out Cleaning</a>
      <a class="contact-button text-sm hover:scale-105 transition-transform text-center py-2" href="/services/carpet-cleaning/">Carpet Cleaning</a>
      <a class="contact-button text-sm hover:scale-105 transition-transform text-center py-2" href="/services/window-cleaning/">Window Cleaning</a>
      <a class="contact-button text-sm hover:scale-105 transition-transform text-center py-2" href="/services/pressure-washing/">Pressure Washing</a>
      <a class="contact-button text-sm hover:scale-105 transition-transform text-center py-2" href="/services/luxury-estate-cleaning/">Luxury Estate Cleaning</a>
      <a class="contact-button text-sm hover:scale-105 transition-transform text-center py-2" href="/services/laundry-services/">Laundry Services</a>
      <a class="contact-button text-sm hover:scale-105 transition-transform text-center py-2" href="/services/Detailing-Mobile-AL/">Detailing</a>
  </div>

  <div class="flex flex-col space-y-2 bg-white/95 p-4 rounded-xl shadow-2xl backdrop-blur-md border border-gray-200">
      <h4 class="text-xl font-bold text-gray-900 border-b-2 border-purple-500 pb-2 mb-2 text-center">Commercial & Industrial</h4>
      <a class="contact-button text-sm hover:scale-105 transition-transform text-center py-2" href="/services/commercial-cleaning/">Commercial Cleaning</a>
      <a class="contact-button text-sm hover:scale-105 transition-transform text-center py-2" href="/services/office-janitorial-services/">Office Janitorial Services</a>
      <a class="contact-button text-sm hover:scale-105 transition-transform text-center py-2" href="/services/janitorial-cleaning-services/">Janitorial Cleaning Services</a>
      <a class="contact-button text-sm hover:scale-105 transition-transform text-center py-2" href="/services/medical-dental-facility-cleaning/">Medical Facility Cleaning</a>
      <a class="contact-button text-sm hover:scale-105 transition-transform text-center py-2" href="/services/industrial-warehouse-cleaning/">Industrial & Warehouse Cleaning</a>
      <a class="contact-button text-sm hover:scale-105 transition-transform text-center py-2" href="/services/floor-stripping-waxing/">Floor Stripping & Waxing</a>
      <a class="contact-button text-sm hover:scale-105 transition-transform text-center py-2" href="/services/gym-fitness-center-cleaning/">Gym & Fitness Center Cleaning</a>
      <a class="contact-button text-sm hover:scale-105 transition-transform text-center py-2" href="/services/school-daycare-cleaning/">School & Daycare Cleaning</a>
      <a class="contact-button text-sm hover:scale-105 transition-transform text-center py-2" href="/services/church-worship-center-cleaning/">Church & Worship Cleaning</a>
      <a class="contact-button text-sm hover:scale-105 transition-transform text-center py-2" href="/services/solar-panel-cleaning/">Solar Panel Cleaning</a>
  </div>

  <div class="flex flex-col space-y-2 bg-white/95 p-4 rounded-xl shadow-2xl backdrop-blur-md border border-gray-200">
      <h4 class="text-xl font-bold text-gray-900 border-b-2 border-pink-500 pb-2 mb-2 text-center">Property Management</h4>
      <a class="contact-button text-sm hover:scale-105 transition-transform text-center py-2" href="/services/vacation-rental-cleaning/">Vacation Rental Cleaning</a>
      <a class="contact-button text-sm hover:scale-105 transition-transform text-center py-2" href="/services/airbnb-cleaning/">Airbnb Cleaning</a>
      <a class="contact-button text-sm hover:scale-105 transition-transform text-center py-2" href="/services/airbnb-vacation-rental-management/">Airbnb & Rental Management</a>
      <a class="contact-button text-sm hover:scale-105 transition-transform text-center py-2" href="/services/post-construction-cleanup/">Post-Construction Cleanup</a>
      <a class="contact-button text-sm hover:scale-105 transition-transform text-center py-2" href="/services/property-management-janitorial/">Property Management Janitorial</a>
      <a class="contact-button text-sm hover:scale-105 transition-transform text-center py-2" href="/services/property-maintenance/">Property Maintenance</a>
      <a class="contact-button text-sm hover:scale-105 transition-transform text-center py-2" href="/services/home-watch-services/">Home Watch Services</a>
      <a class="contact-button text-sm hover:scale-105 transition-transform text-center py-2" href="/services/luxury-estate-management/">Luxury Estate Management</a>
      <a class="contact-button text-sm hover:scale-105 transition-transform text-center py-2" href="/services/gutter-cleaning/">Gutter Cleaning</a>
  </div>
</div>"""

mobile_menu = """<div class="hidden space-y-3 mt-4" id="mobile-services">
  <div class="bg-gray-50 rounded-lg p-3">
      <h4 class="font-bold text-gray-800 border-b border-gray-300 pb-2 mb-2">Residential & Property</h4>
      <div class="grid grid-cols-1 gap-2">
          <a class="contact-button text-sm w-full text-center m-0 py-2" href="/services/house-cleaning/">House Cleaning</a>
          <a class="contact-button text-sm w-full text-center m-0 py-2" href="/services/deep-cleaning/">Deep Cleaning</a>
          <a class="contact-button text-sm w-full text-center m-0 py-2" href="/services/move-in-cleaning/">Move-In Cleaning</a>
          <a class="contact-button text-sm w-full text-center m-0 py-2" href="/services/move-out-cleaning/">Move-Out Cleaning</a>
          <a class="contact-button text-sm w-full text-center m-0 py-2" href="/services/carpet-cleaning/">Carpet Cleaning</a>
          <a class="contact-button text-sm w-full text-center m-0 py-2" href="/services/window-cleaning/">Window Cleaning</a>
          <a class="contact-button text-sm w-full text-center m-0 py-2" href="/services/pressure-washing/">Pressure Washing</a>
          <a class="contact-button text-sm w-full text-center m-0 py-2" href="/services/luxury-estate-cleaning/">Luxury Estate Cleaning</a>
          <a class="contact-button text-sm w-full text-center m-0 py-2" href="/services/laundry-services/">Laundry Services</a>
          <a class="contact-button text-sm w-full text-center m-0 py-2" href="/services/Detailing-Mobile-AL/">Detailing</a>
      </div>
  </div>

  <div class="bg-gray-50 rounded-lg p-3">
      <h4 class="font-bold text-gray-800 border-b border-gray-300 pb-2 mb-2">Commercial & Industrial</h4>
      <div class="grid grid-cols-1 gap-2">
          <a class="contact-button text-sm w-full text-center m-0 py-2" href="/services/commercial-cleaning/">Commercial Cleaning</a>
          <a class="contact-button text-sm w-full text-center m-0 py-2" href="/services/office-janitorial-services/">Office Janitorial</a>
          <a class="contact-button text-sm w-full text-center m-0 py-2" href="/services/janitorial-cleaning-services/">Janitorial Cleaning</a>
          <a class="contact-button text-sm w-full text-center m-0 py-2" href="/services/medical-dental-facility-cleaning/">Medical Facility</a>
          <a class="contact-button text-sm w-full text-center m-0 py-2" href="/services/industrial-warehouse-cleaning/">Industrial & Warehouse</a>
          <a class="contact-button text-sm w-full text-center m-0 py-2" href="/services/floor-stripping-waxing/">Floor Stripping & Waxing</a>
          <a class="contact-button text-sm w-full text-center m-0 py-2" href="/services/gym-fitness-center-cleaning/">Gym & Fitness Cleaning</a>
          <a class="contact-button text-sm w-full text-center m-0 py-2" href="/services/school-daycare-cleaning/">School & Daycare Cleaning</a>
          <a class="contact-button text-sm w-full text-center m-0 py-2" href="/services/church-worship-center-cleaning/">Church Cleaning</a>
          <a class="contact-button text-sm w-full text-center m-0 py-2" href="/services/solar-panel-cleaning/">Solar Panel Cleaning</a>
      </div>
  </div>

  <div class="bg-gray-50 rounded-lg p-3">
      <h4 class="font-bold text-gray-800 border-b border-gray-300 pb-2 mb-2">Property Management</h4>
      <div class="grid grid-cols-1 gap-2">
          <a class="contact-button text-sm w-full text-center m-0 py-2" href="/services/vacation-rental-cleaning/">Vacation Rental Cleaning</a>
          <a class="contact-button text-sm w-full text-center m-0 py-2" href="/services/airbnb-cleaning/">Airbnb Cleaning</a>
          <a class="contact-button text-sm w-full text-center m-0 py-2" href="/services/airbnb-vacation-rental-management/">Airbnb Management</a>
          <a class="contact-button text-sm w-full text-center m-0 py-2" href="/services/post-construction-cleanup/">Post-Construction Cleanup</a>
          <a class="contact-button text-sm w-full text-center m-0 py-2" href="/services/property-management-janitorial/">Property Management Janitorial</a>
          <a class="contact-button text-sm w-full text-center m-0 py-2" href="/services/property-maintenance/">Property Maintenance</a>
          <a class="contact-button text-sm w-full text-center m-0 py-2" href="/services/home-watch-services/">Home Watch Services</a>
          <a class="contact-button text-sm w-full text-center m-0 py-2" href="/services/luxury-estate-management/">Luxury Estate Management</a>
          <a class="contact-button text-sm w-full text-center m-0 py-2" href="/services/gutter-cleaning/">Gutter Cleaning</a>
      </div>
  </div>
</div>"""

def update_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content

        # Desktop Services Regex
        # Looking for existing dropdown div under <!-- SERVICES Dropdown -->
        # We need to gracefully match whatever the current class is, previously w-56, now maybe w-[900px] if we ran it before
        desktop_pattern = r'(<!-- SERVICES Dropdown -->.*?<div class="absolute[^>]*>).*?(</div>\s*</div>\s*<!-- LOCATIONS Dropdown -->)'
        
        # We replace the entire <div class="absolute..." >...</div> with our new desktop_menu
        # Let's use a simpler pattern: find start of dropdown, replace till LOCATIONS
        desktop_safe_pattern = r'(<!-- SERVICES Dropdown -->.*?)(<div class="absolute[^>]*z-50[^>]*>.*?)(?=<!-- LOCATIONS Dropdown -->)'
        
        if re.search(desktop_safe_pattern, content, flags=re.DOTALL):
            content = re.sub(desktop_safe_pattern, r'\g<1>' + desktop_menu + '\n</div>\n', content, flags=re.DOTALL)
        else:
            print(f"Skipping {filepath} - no desktop Services pattern matched")
            return

        # Mobile Services Regex
        # Look for <div ... id="mobile-services"> ... </div>
        # Keep it simple: find from id="mobile-services" to the next LOCATIONS DROPDOWN boundary
        mobile_safe_pattern = r'(<!-- SERVICES DROPDOWN \(Mobile\).*?)(<div[^>]*id="mobile-services"[^>]*>.*?)(?=<!-- LOCATIONS DROPDOWN \(Mobile\))'
        
        if re.search(mobile_safe_pattern, content, flags=re.DOTALL):
            content = re.sub(mobile_safe_pattern, r'\g<1>' + mobile_menu + '\n', content, flags=re.DOTALL)
        
        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Updated: {filepath}")

    except Exception as e:
        print(f"Error processing {filepath}: {e}")

exclusions = ['.git', '.github', 'tmp', '.gemini']

for root, dirs, files in os.walk('.'):
    dirs[:] = [d for d in dirs if d not in exclusions]
    for file in files:
        if file.endswith('.html'):
            filepath = os.path.join(root, file)
            update_file(filepath)

