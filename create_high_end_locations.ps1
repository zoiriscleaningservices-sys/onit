$TemplateDir = "foley"
$TemplateFile = "index.html"

$Cities = @(
    @{ Name="Pensacola Beach"; Slug="pensacola-beach"; County="Escambia County"; Zip="32561"; Zips=@("32561"); Lat="30.3323"; Long="-87.1408" },
    @{ Name="Gulf Breeze"; Slug="gulf-breeze"; County="Santa Rosa County"; Zip="32561"; Zips=@("32561", "32562"); Lat="30.3582"; Long="-87.1724" },
    @{ Name="Destin"; Slug="destin"; County="Okaloosa County"; Zip="32541"; Zips=@("32541", "32540"); Lat="30.3935"; Long="-86.4753" },
    @{ Name="Santa Rosa Beach"; Slug="santa-rosa-beach"; County="Walton County"; Zip="32459"; Zips=@("32459"); Lat="30.4011"; Long="-86.2238" },
    @{ Name="Seaside"; Slug="seaside"; County="Walton County"; Zip="32459"; Zips=@("32459"); Lat="30.3204"; Long="-86.1365" },
    @{ Name="Rosemary Beach"; Slug="rosemary-beach"; County="Walton County"; Zip="32461"; Zips=@("32461"); Lat="30.2785"; Long="-85.9658" },
    @{ Name="Alys Beach"; Slug="alys-beach"; County="Walton County"; Zip="32461"; Zips=@("32461"); Lat="30.2858"; Long="-85.9814" }
)

$AllServices = @(
    @{ Slug="commercial-cleaning"; Name="Commercial Cleaning" },
    @{ Slug="deep-cleaning"; Name="Deep Cleaning" },
    @{ Slug="house-cleaning"; Name="House Cleaning" },
    @{ Slug="move-in-cleaning"; Name="Move-In Cleaning" },
    @{ Slug="move-out-cleaning"; Name="Move-Out Cleaning" },
    @{ Slug="vacation-rental-cleaning"; Name="Vacation Rental Cleaning" },
    @{ Slug="airbnb-cleaning"; Name="Airbnb Cleaning" },
    @{ Slug="post-construction-cleanup"; Name="Post-Construction Cleanup" },
    @{ Slug="carpet-cleaning"; Name="Carpet Cleaning" },
    @{ Slug="pressure-washing"; Name="Pressure Washing" },
    @{ Slug="Detailing-Mobile-AL"; Name="Detailing" },
    @{ Slug="laundry-services"; Name="Laundry Services" },
    @{ Slug="window-cleaning"; Name="Window Cleaning" },
    @{ Slug="luxury-estate-cleaning"; Name="Luxury Estate Cleaning" },
    @{ Slug="luxury-estate-management"; Name="Luxury Estate Management" },
    @{ Slug="home-watch-services"; Name="Home Watch Services" },
    @{ Slug="property-management-janitorial"; Name="Property Management Janitorial" },
    @{ Slug="property-maintenance"; Name="Property Maintenance" },
    @{ Slug="airbnb-vacation-rental-management"; Name="Airbnb & Vacation Rental Management" },
    @{ Slug="gutter-cleaning"; Name="Gutter Cleaning" },
    @{ Slug="office-janitorial-services"; Name="Office Janitorial Services" },
    @{ Slug="janitorial-cleaning-services"; Name="Janitorial Cleaning Services" },
    @{ Slug="medical-dental-facility-cleaning"; Name="Medical & Dental Facility Cleaning" },
    @{ Slug="industrial-warehouse-cleaning"; Name="Industrial & Warehouse Cleaning" },
    @{ Slug="floor-stripping-waxing"; Name="Floor Stripping & Waxing" },
    @{ Slug="gym-fitness-center-cleaning"; Name="Gym & Fitness Center Cleaning" },
    @{ Slug="school-daycare-cleaning"; Name="School & Daycare Cleaning" },
    @{ Slug="church-worship-center-cleaning"; Name="Church & Worship Center Cleaning" },
    @{ Slug="solar-panel-cleaning"; Name="Solar Panel Cleaning" }
)

$TemplatePath = Join-Path $TemplateDir $TemplateFile
if (-not (Test-Path $TemplatePath)) {
    Write-Host "Error: Template not found at $TemplatePath"
    exit
}

$TemplateContent = [System.IO.File]::ReadAllText($TemplatePath, [System.Text.Encoding]::UTF8)
$NewSitemapEntries = @()

foreach ($City in $Cities) {
    Write-Host "Generating Hub Page for $($City.Name)..."
    if (-not (Test-Path $City.Slug)) {
        New-Item -ItemType Directory -Path $City.Slug | Out-Null
    }

    $Content = $TemplateContent
    $Content = $Content -replace 'Foley', $City.Name
    $Content = $Content -replace '36535', $City.Zip
    $Content = $Content -replace 'Baldwin County', $City.County
    $Content = $Content -replace '30\.4066', $City.Lat
    $Content = $Content -replace '-87\.6836', $City.Long
    $Content = $Content -replace '/foley/', "/$($City.Slug)/"

    $ZipsJs = 'const serviceZips = [' + [Environment]::NewLine
    $ZipsList = @()
    foreach ($z in $City.Zips) { $ZipsList += "`"$z`"" }
    $ZipsJs += '      ' + ($ZipsList -join ', ') + [Environment]::NewLine + '    ];'

    $ZipPattern = '(?is)const serviceZips = \[[^\]]*\];'
    $Content = $Content -replace $ZipPattern, $ZipsJs

    $HiddenTextPattern = '(?is)<div style="display:none;">.*?</div>'
    $Content = $Content -replace $HiddenTextPattern, ''

    $LinksHtml = '<div class="grid grid-cols-1 md:grid-cols-3 gap-4 mt-4 text-center">'
    foreach ($Svc in $AllServices) {
        $SlugTarget = $Svc.Slug -replace '-Mobile-AL', '' -replace '-mobile-al', ''
        $LinkUrl = "/$($City.Slug)/$SlugTarget/"
        $LinksHtml += "<a href=`"$LinkUrl`" class=`"block p-4 bg-gray-50 hover:bg-blue-100 rounded-lg transition border border-gray-200 text-blue-900 font-semibold`">$($Svc.Name) in $($City.Name)</a>"
    }
    $LinksHtml += '</div>'

    $ServicesSection = @"
<section class="py-16 bg-white shrink-0">
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
    <h2 class="text-3xl font-bold text-center text-gray-900 mb-8">Professional Cleaning Services in $($City.Name)</h2>
    <p class="text-center text-lg text-gray-600 mb-10 max-w-3xl mx-auto">
      We offer a complete range of luxury residential and commercial cleaning solutions tailored to $($City.Name) properties. 
    </p>
    $LinksHtml
  </div>
</section>
"@

    if ($Content -match '<footer') {
        $Content = $Content -replace '(?is)<footer', "$ServicesSection`n<footer"
    } else {
        $Content = $Content -replace '(?is)</body>', "$ServicesSection`n</body>"
    }

    $TargetFile = Join-Path $City.Slug 'index.html'
    [System.IO.File]::WriteAllText($TargetFile, $Content, [System.Text.Encoding]::UTF8)

    $NewSitemapEntries += "  <url>`n    <loc>https://www.zoiriscleaningservices.com/$($City.Slug)/</loc>`n    <lastmod>$(Get-Date -Format 'yyyy-MM-dd')</lastmod>`n    <changefreq>weekly</changefreq>`n    <priority>0.9</priority>`n  </url>"
}

$SitemapPath = 'sitemap.xml'
if (Test-Path $SitemapPath) {
    $SitemapContent = [System.IO.File]::ReadAllText($SitemapPath, [System.Text.Encoding]::UTF8)
    $FinalEntries = @()
    foreach ($Entry in $NewSitemapEntries) {
        if ($Entry -match '<loc>(.*?)</loc>') {
            $Url = $matches[1]
            if (-not ($SitemapContent -match [regex]::Escape($Url))) {
                $FinalEntries += $Entry
            }
        }
    }
    if ($FinalEntries.Count -gt 0) {
        $SitemapContent = $SitemapContent -replace '(?is)</urlset>', ($FinalEntries -join "`n") + "`n</urlset>"
        [System.IO.File]::WriteAllText($SitemapPath, $SitemapContent, [System.Text.Encoding]::UTF8)
        Write-Host "Added $($FinalEntries.Count) new high-end hub pages to sitemap.xml."
    }
}
