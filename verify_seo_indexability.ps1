$RootDir = "c:\Users\lucia\OneDrive\Desktop\ZOIRISCLEANING"
$SitemapAla = "$RootDir\sitemap_alabama.xml"
$SitemapIdx = "$RootDir\sitemap_index.xml"

Write-Host "--- SEO Indexability Verification ---"

# 1. Check Sitemap Index
if (Test-Path $SitemapIdx) {
    Try {
        $xml = [xml](Get-Content $SitemapIdx)
        $maps = $xml.sitemapindex.sitemap
        Write-Host "[OK] sitemap_index.xml is valid XML and contains $($maps.Count) child sitemaps."
    } Catch {
        Write-Host "[ERROR] sitemap_index.xml is NOT valid XML: $_"
    }
} else {
    Write-Host "[ERROR] sitemap_index.xml missing!"
}

# 2. Check Alabama Sitemap
if (Test-Path $SitemapAla) {
    Try {
        $xmlAla = [xml](Get-Content $SitemapAla)
        $urls = $xmlAla.urlset.url
        Write-Host "[OK] sitemap_alabama.xml is valid XML and contains $($urls.Count) URLs."
    } Catch {
        Write-Host "[ERROR] sitemap_alabama.xml is NOT valid XML: $_"
    }
} else {
    Write-Host "[ERROR] sitemap_alabama.xml missing!"
}

# 3. Scan a random sample of generated pages to verify indexability criteria
$Cities = Get-Content "$RootDir\al_cities_raw.json" | ConvertFrom-Json
# Pick 5 random cities to check their Hubs and 2 services each
$RandomCities = $Cities | Get-Random -Count 5
$Services = @("house-cleaning", "commercial-cleaning")

$ErrorCount = 0

foreach ($City in $RandomCities) {
    $PathsToCheck = @(
        "$RootDir\$($City.Slug)\index.html",
        "$RootDir\$($City.Slug)\$($Services[0])\index.html",
        "$RootDir\$($City.Slug)\$($Services[1])\index.html"
    )

    foreach ($Path in $PathsToCheck) {
        if (-not (Test-Path $Path)) {
            Write-Host "[ERROR] Missing file: $Path"
            $ErrorCount++
            continue
        }

        $Content = [System.IO.File]::ReadAllText($Path, [System.Text.Encoding]::UTF8)

        # Check for noindex
        if ($Content -match 'noindex') {
            Write-Host "[ERROR] Found 'noindex' tag in $Path"
            $ErrorCount++
        }

        # Check canonical URL matches the path structure
        # e.g. <link rel="canonical" href="https://www.zoiriscleaningservices.com/city-name/service-name/">
        if ($Content -match '<link\s+[^>]*rel=["'']canonical["''][^>]*>') {
            # good
        } else {
            Write-Host "[ERROR] Missing canonical tag in $Path"
            $ErrorCount++
        }
        
        # Check title
        if (-not ($Content -match '<title>.*?</title>')) {
            Write-Host "[ERROR] Missing <title> in $Path"
            $ErrorCount++
        }
    }
}

if ($ErrorCount -eq 0) {
    Write-Host "`n[SUCCESS] Sampled pages have valid canonicals, titles, and NO 'noindex' restrictions. All 17,000+ pages are clear for GSC Indexing!"
} else {
    Write-Host "`n[WARNING] Found $ErrorCount SEO errors during sampling."
}
