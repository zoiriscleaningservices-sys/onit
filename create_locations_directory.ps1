$DatasetPath = "c:\Users\lucia\OneDrive\Desktop\ZOIRISCLEANING\al_cities_raw.json"
$Cities = Get-Content $DatasetPath | ConvertFrom-Json | Sort-Object Name

# Generate Alphabetical Links Grid
$LinksHtml = @"
<section class="py-16 bg-white shrink-0">
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
    <h1 class="text-5xl font-extrabold text-center text-gray-900 mb-6 tracking-tight">Communities We Serve in Alabama</h1>
    <p class="text-center text-xl text-gray-600 mb-12 max-w-4xl mx-auto">
      Zoiris Cleaning Services proudly covers the entire state of Alabama. Select your city below to discover our luxury residential and commercial cleaning packages tailored for your area.
    </p>
    <div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
"@

foreach ($City in $Cities) {
    $LinksHtml += "      <a href=`"/$($City.Slug)/`" class=`"text-blue-700 hover:text-blue-900 font-semibold p-2 border rounded-lg hover:shadow-md transition bg-gray-50 text-center`">$($City.Name), AL</a>`n"
}

$LinksHtml += @"
    </div>
  </div>
</section>
"@

$TemplateContent = [System.IO.File]::ReadAllText("c:\Users\lucia\OneDrive\Desktop\ZOIRISCLEANING\foley\index.html", [System.Text.Encoding]::UTF8)

$Title = "All Service Locations in Alabama | Zoiris Cleaning"
$Desc = "View our complete list of over 580 premium house cleaning and commercial cleaning service locations across Alabama. Zoiris Cleaning serves the entire state!"

$Result = $TemplateContent -replace '(?is)<title>.*?</title>', "<title>$Title</title>"
$Result = $Result -replace '(?is)<meta[^>]*name=["'']description["''][^>]*>', "<meta name=""description"" content=""$Desc"">"

# Using split strategy for Foley
$SplitBySection = $Result -split '<!-- HERO -->'
if ($SplitBySection.Count -gt 1) {
    $Top = $SplitBySection[0]
    $SplitByFooter = $SplitBySection[1] -split '<footer'
    if ($SplitByFooter.Count -gt 1) {
        $Result = $Top + "`n$LinksHtml`n<footer" + $SplitByFooter[1]
    }
}

$TargetDir = "c:\Users\lucia\OneDrive\Desktop\ZOIRISCLEANING\locations"
if (-not (Test-Path $TargetDir)) { New-Item -ItemType Directory -Path $TargetDir | Out-Null }
[System.IO.File]::WriteAllText("$TargetDir\index.html", $Result, [System.Text.Encoding]::UTF8)
Write-Host "Locations Directory created at /locations/index.html"
