import os
from supabase import create_client, Client

# Initialize Supabase client
url = "https://dwxbzltxsdeshmmtcycv.supabase.co"
key = os.environ["SUPABASE_ANON_KEY"]  # You'll set this in GitHub Secrets

supabase: Client = create_client(url, key)

# Call the RPC function that generates the sitemap (as used on your site)
response = supabase.rpc("get_dynamic_sitemap").execute()

# The function returns the full XML as a string in the first row
if response.data and len(response.data) > 0:
    sitemap_xml = response.data[0]["get_dynamic_sitemap"]  # or just response.data[0] depending on return
else:
    raise Exception("No sitemap data returned from Supabase")

# Save to blog-sitemap.xml (this is the exact filename your site likely expects)
with open("blog-sitemap.xml", "w", encoding="utf-8") as f:
    f.write(sitemap_xml)

print("blog-sitemap.xml generated successfully!")
print("File content preview:")
print(sitemap_xml[:500] + "..." if len(sitemap_xml) > 500 else sitemap_xml)
