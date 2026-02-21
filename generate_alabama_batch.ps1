$DatasetPath = "c:\Users\lucia\OneDrive\Desktop\ZOIRISCLEANING\al_cities_raw.json"
$Cities = Get-Content $DatasetPath | ConvertFrom-Json

$TemplateDir = "foley"
$HubTemplate = [System.IO.File]::ReadAllText("$TemplateDir\index.html", [System.Text.Encoding]::UTF8)

$ServicesDirs = Get-ChildItem -Path "services" -Directory

$CitiesToProcess = $Cities | Select-Object -First 2
$TotalCities = $CitiesToProcess.Count
$Count = 0

$SitemapEntries = @()
$Today = Get-Date -Format 'yyyy-MM-dd'

foreach ($City in $CitiesToProcess) {
    $Count++
    Write-Host "[$Count/$TotalCities] Generating Hub + Services for $($City.Name)..."
    
    if (-not (Test-Path $City.Slug)) {
        New-Item -ItemType Directory -Path $City.Slug | Out-Null
    }
    
    # 1. Generate Hub
    $Content = $HubTemplate
    $Content = $Content -replace 'Foley', $City.Name
    $Content = $Content -replace '36535', ''
    $Content = $Content -replace 'Baldwin County', $City.County
    $Content = $Content -replace '30\.4066', $City.Lat
    $Content = $Content -replace '-87\.6836', $City.Long
    $Content = $Content -replace '/foley/', "/$($City.Slug)/"
    
    [System.IO.File]::WriteAllText("$($City.Slug)\index.html", $Content, [System.Text.Encoding]::UTF8)
    $SitemapEntries += "  <url>`n    <loc>https://www.zoiriscleaningservices.com/$($City.Slug)/</loc>`n    <lastmod>$Today</lastmod>`n    <changefreq>weekly</changefreq>`n    <priority>0.8</priority>`n  </url>"
    
    # 2. Generate Services
    foreach ($SvcDir in $ServicesDirs) {
        $SvcSlug = $SvcDir.Name
        $TargetDir = "$($City.Slug)\$SvcSlug"
        if (-not (Test-Path $TargetDir)) {
            New-Item -ItemType Directory -Path $TargetDir | Out-Null
        }
        
        $SvcContent = [System.IO.File]::ReadAllText($SvcDir.FullName + "\index.html", [System.Text.Encoding]::UTF8)
        
        $SvcName = $SvcSlug -replace '-', ' '
        $SvcName = (Get-Culture).TextInfo.ToTitleCase($SvcName)
        if ($SvcSlug.ToLower() -eq 'detailing-mobile-al') { $SvcName = "Detailing" }
        if (-not ($SvcName -match "Cleaning")) { $SvcName = "$SvcName Cleaning" }
        
        $Title = "Best $SvcName in $($City.Name) | 5-Star Rated | Zoiris Cleaning"
        $Desc = "Professional $SvcName in $($City.Name). We are the top-rated local experts. Affordable, reliable, and guaranteed spotless. Call (251) 930-8621!"
        $H1 = "Professional $SvcName in $($City.Name)"
        
        $SvcContent = $SvcContent -replace '(?is)<title>.*?</title>', "<title>$Title</title>"
        $SvcContent = $SvcContent -replace '(?is)<meta[^>]*name=["'']description["''][^>]*>', "<meta name=""description"" content=""$Desc"">"
        $SvcContent = $SvcContent -replace '(?is)(<h1[^>]*>).*?(</h1>)', "`${1}$H1`${2}"
        
        $SvcContent = $SvcContent -replace '(?i) in Services', " in $($City.Name)"
        $SvcContent = $SvcContent -replace '(?i)Services, AL', "$($City.Name), AL"
        
        $SvcContent = $SvcContent -replace "href=`"https://www.zoiriscleaningservices.com/services/$SvcSlug/`"", "href=`"https://www.zoiriscleaningservices.com/$($City.Slug)/$SvcSlug/`""
        
        [System.IO.File]::WriteAllText("$TargetDir\index.html", $SvcContent, [System.Text.Encoding]::UTF8)
        $SitemapEntries += "  <url>`n    <loc>https://www.zoiriscleaningservices.com/$($City.Slug)/$SvcSlug/</loc>`n    <lastmod>$Today</lastmod>`n    <changefreq>monthly</changefreq>`n    <priority>0.7</priority>`n  </url>"
    }
}

Write-Host "Success! Created $($Count * ($ServicesDirs.Count + 1)) pages."
