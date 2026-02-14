import os
import re

# Update Services Dropdown to include Laundry and Window Cleaning
# Current list includes Commercial ... Detailing.
# We add Laundry and Window Cleaning.

new_desktop_services = """
                  <a href="/commercial-cleaning/" class="contact-button text-lg hover:bg-blue-700">Commercial Cleaning</a>
                  <a href="/deep-cleaning/" class="contact-button text-lg hover:bg-blue-700">Deep Cleaning</a>
                  <a href="/house-cleaning/" class="contact-button text-lg hover:bg-blue-700">House Cleaning</a>
                  <a href="/move-in-cleaning/" class="contact-button text-lg hover:bg-blue-700">Move-In Cleaning</a>
                  <a href="/move-out-cleaning/" class="contact-button text-lg hover:bg-blue-700">Move-Out Cleaning</a>
                  <a href="/vacation-rental-cleaning/" class="contact-button text-lg hover:bg-blue-700">Vacation Rental Cleaning</a>
                  <a href="/airbnb-cleaning/" class="contact-button text-lg hover:bg-blue-700">Airbnb Cleaning</a>
                  <a href="/post-construction-cleanup/" class="contact-button text-lg hover:bg-blue-700">Post-Construction Cleanup</a>
                  <a href="/carpet-cleaning/" class="contact-button text-lg hover:bg-blue-700">Carpet Cleaning</a>
                  <a href="/pressure-washing/" class="contact-button text-lg hover:bg-blue-700">Pressure Washing</a>
                  <a href="/Detailing-Mobile-AL/" class="contact-button text-lg hover:bg-blue-700">Detailing</a>
                  <a href="/laundry-services/" class="contact-button text-lg hover:bg-blue-700">Laundry Services</a>
                  <a href="/window-cleaning/" class="contact-button text-lg hover:bg-blue-700">Window Cleaning</a>
"""

new_mobile_services = """
            <a href="/commercial-cleaning/" class="contact-button text-lg">Commercial Cleaning</a>
            <a href="/deep-cleaning/" class="contact-button text-lg">Deep Cleaning</a>
            <a href="/house-cleaning/" class="contact-button text-lg">House Cleaning</a>
            <a href="/move-in-cleaning/" class="contact-button text-lg">Move-In Cleaning</a>
            <a href="/move-out-cleaning/" class="contact-button text-lg">Move-Out Cleaning</a>
            <a href="/vacation-rental-cleaning/" class="contact-button text-lg">Vacation Rental Cleaning</a>
            <a href="/airbnb-cleaning/" class="contact-button text-lg">Airbnb Cleaning</a>
            <a href="/post-construction-cleanup/" class="contact-button text-lg">Post-Construction Cleanup</a>
            <a href="/carpet-cleaning/" class="contact-button text-lg">Carpet Cleaning</a>
            <a href="/pressure-washing/" class="contact-button text-lg">Pressure Washing</a>
            <a href="/Detailing-Mobile-AL/" class="contact-button text-lg">Detailing</a>
            <a href="/laundry-services/" class="contact-button text-lg">Laundry Services</a>
            <a href="/window-cleaning/" class="contact-button text-lg">Window Cleaning</a>
"""

def update_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content

        # Regex for Desktop Services Dropdown
        # Pattern: <!-- SERVICES Dropdown --> ... <div ...> (content) </div>
        desktop_pattern = r'(<!-- SERVICES Dropdown -->.*?<div class="absolute left-0 top-full hidden group-hover:flex flex-col w-56 z-50">)(.*?)(</div>)'
        content = re.sub(desktop_pattern, lambda m: m.group(1) + new_desktop_services + m.group(3), content, flags=re.DOTALL)
        
        # Regex for Mobile Services Dropdown
        # Pattern: <div id="mobile-services" ...> (content) </div>
        mobile_pattern = r'(<div id="mobile-services" class="hidden pl-4 space-y-1">)(.*?)(</div>)'
        content = re.sub(mobile_pattern, lambda m: m.group(1) + new_mobile_services + m.group(3), content, flags=re.DOTALL)

        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Updated: {filepath}")

    except Exception as e:
        print(f"Error processing {filepath}: {e}")

for root, dirs, files in os.walk('.'):
    for file in files:
        if file.endswith('.html'):
            filepath = os.path.join(root, file)
            update_file(filepath)
