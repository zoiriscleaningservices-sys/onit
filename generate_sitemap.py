import os
from supabase import create_client

supabase = create_client(
    "https://dwxbzltxsdeshmmtcycv.supabase.co",
    os.environ["SUPABASE_ANON_KEY"]
)

response = supabase.rpc("get_dynamic_sitemap").execute()

sitemap_xml = response.data[0]

with open("sitemap.xml", "w", encoding="utf-8") as f:
    f.write(sitemap_xml)

print("sitemap.xml generated successfully!")
