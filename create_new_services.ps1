$ResidentialServices = @(
    @{ Slug="luxury-estate-cleaning"; Name="Luxury Estate Cleaning"; Desc="Premium luxury estate cleaning services. Meticulous, discrete, and thorough cleaning for high-end properties and large estates." },
    @{ Slug="luxury-estate-management"; Name="Luxury Estate Management"; Desc="Comprehensive luxury estate management services. We handle maintenance, cleaning, and day-to-day property oversight for premium homes." },
    @{ Slug="home-watch-services"; Name="Home Watch Services"; Desc="Professional home watch services. We provide routine inspections and maintenance checks for unoccupied homes and vacation properties." },
    @{ Slug="property-management-janitorial"; Name="Property Management Janitorial"; Desc="Reliable janitorial services for property managers. Keep your managed properties spotless and well-maintained with our professional team." },
    @{ Slug="property-maintenance"; Name="Property Maintenance"; Desc="Complete property maintenance services. From minor repairs to routine upkeep, we ensure your residential or commercial property stays in top condition." },
    @{ Slug="airbnb-vacation-rental-management"; Name="Airbnb & Vacation Rental Management"; Desc="Full-service Airbnb and vacation rental management. We handle cleanings, restocking, and property maintenance to keep your guests happy." },
    @{ Slug="gutter-cleaning"; Name="Gutter Cleaning"; Desc="Professional gutter cleaning services. Protect your property from water damage with our safe and effective gutter clearing out." }
)

$CommercialServices = @(
    @{ Slug="office-janitorial-services"; Name="Office Janitorial Services"; Desc="Top-rated office janitorial services. We provide daily, weekly, or monthly cleaning to keep your workspace pristine and professional." },
    @{ Slug="janitorial-cleaning-services"; Name="Janitorial Cleaning Services"; Desc="Comprehensive janitorial cleaning services for businesses of all sizes. Dependable, thorough, and customized to your facility's needs." },
    @{ Slug="medical-dental-facility-cleaning"; Name="Medical & Dental Facility Cleaning"; Desc="Specialized medical and dental facility cleaning. We adhere to strict hygiene and sanitation standards to maintain a safe healthcare environment." },
    @{ Slug="industrial-warehouse-cleaning"; Name="Industrial & Warehouse Cleaning"; Desc="Heavy-duty industrial and warehouse cleaning services. We handle large-scale sweeping, scrubbing, and degreasing for safe operations." },
    @{ Slug="floor-stripping-waxing"; Name="Floor Stripping & Waxing"; Desc="Professional floor stripping and waxing. Restore the shine and protect your commercial floors with our expert care." },
    @{ Slug="gym-fitness-center-cleaning"; Name="Gym & Fitness Center Cleaning"; Desc="Thorough gym and fitness center cleaning. We sanitize equipment, locker rooms, and workout floors to provide a safe space for your members." },
    @{ Slug="school-daycare-cleaning"; Name="School & Daycare Cleaning"; Desc="Safe and effective school and daycare cleaning. We use non-toxic products to disinfect classrooms, play areas, and restrooms." },
    @{ Slug="church-worship-center-cleaning"; Name="Church & Worship Center Cleaning"; Desc="Respectful church and worship center cleaning services. We ensure your sanctuary and gathering spaces are welcoming and pristine." },
    @{ Slug="solar-panel-cleaning"; Name="Solar Panel Cleaning"; Desc="Professional solar panel cleaning services. Maximize your energy efficiency safely with our spotless, streak-free washing techniques." }
)

function Create-Pages($Services, $TemplateDir, $PlaceholderName) {
    # Ensure correct working directory path if running from root relative
    $TemplatePath = Join-Path "services" (Join-Path $TemplateDir "index.html")
    if (-not (Test-Path $TemplatePath)) {
        Write-Host "Template not found: $TemplatePath"
        return
    }

    $TemplateContent = [System.IO.File]::ReadAllText($TemplatePath, [System.Text.Encoding]::UTF8)

    foreach ($Svc in $Services) {
        $TargetDir = Join-Path "services" $Svc.Slug
        if (-not (Test-Path $TargetDir)) {
            New-Item -ItemType Directory -Path $TargetDir | Out-Null
        }

        $TargetFile = Join-Path $TargetDir "index.html"
        $Content = $TemplateContent

        # Replace Title
        $NewTitle = "<title>Best $($Svc.Name) in Mobile | 5-Star Rated</title>"
        $TitleRegex = [regex]'(?is)<title>.*?</title>'
        $Content = $TitleRegex.Replace($Content, $NewTitle)

        # Replace Meta Description
        $NewDesc = "<meta name=""description"" content=""$($Svc.Desc)"">"
        $DescRegex = [regex]'(?is)<meta[^>]*name=["'']description["''][^>]*>'
        $Content = $DescRegex.Replace($Content, $NewDesc)

        # Replace Placeholder Name (e.g., "House Cleaning" or "Commercial Cleaning")
        $Content = $Content -replace $PlaceholderName, $Svc.Name

        # Fix relative links specific to this service path
        $Content = $Content -replace "/$TemplateDir/", "/$($Svc.Slug)/"

        [System.IO.File]::WriteAllText($TargetFile, $Content, [System.Text.Encoding]::UTF8)
        Write-Host "Generated: $TargetFile"
    }
}

Write-Host "Generating Residential / Property Services..."
Create-Pages $ResidentialServices "house-cleaning" "House Cleaning"

Write-Host "Generating Commercial / Industrial Services..."
Create-Pages $CommercialServices "commercial-cleaning" "Commercial Cleaning"
