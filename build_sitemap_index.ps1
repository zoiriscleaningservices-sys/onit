$IndexContent = @"
<?xml version="1.0" encoding="UTF-8"?>
<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <sitemap>
    <loc>https://www.zoiriscleaningservices.com/sitemap.xml</loc>
    <lastmod>$(Get-Date -Format 'yyyy-MM-dd')</lastmod>
  </sitemap>
  <sitemap>
    <loc>https://www.zoiriscleaningservices.com/sitemap_alabama.xml</loc>
    <lastmod>$(Get-Date -Format 'yyyy-MM-dd')</lastmod>
  </sitemap>
</sitemapindex>
"@

[System.IO.File]::WriteAllText("c:\Users\lucia\OneDrive\Desktop\ZOIRISCLEANING\sitemap_index.xml", $IndexContent, [System.Text.Encoding]::UTF8)
Write-Host "Created sitemap_index.xml linking sitemap.xml and sitemap_alabama.xml."
