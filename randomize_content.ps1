$RootDir = "c:\Users\lucia\OneDrive\Desktop\ZOIRISCLEANING"
$Cities = Get-Content "$RootDir\al_cities_raw.json" | ConvertFrom-Json

$Adjectives = @("top-rated", "professional", "premium", "expert", "trusted", "reliable", "elite", "highest-quality", "exceptional", "five-star")
$Intros = @(
    "Are you looking for",
    "In need of",
    "Searching for",
    "Discover the best",
    "Experience"
)
$Outros = @(
    "Contact us today for a free estimate.",
    "Reach out to our team to get started.",
    "Call us now to book your appointment.",
    "Get your customized quote today.",
    "Schedule your service with us right away."
)

$Services = Get-ChildItem -Path "$RootDir\services" -Directory

Write-Host "Starting Content Randomization across 17,000+ files..."
$Count = 0

foreach ($City in $Cities) {
    # 1. Randomize Hub Page
    $HubPath = "$RootDir\$($City.Slug)\index.html"
    if (Test-Path $HubPath) {
        $Content = [System.IO.File]::ReadAllText($HubPath, [System.Text.Encoding]::UTF8)
        
        $Adj = $Adjectives | Get-Random
        $Intro = $Intros | Get-Random
        $Outro = $Outros | Get-Random
        
        # Inject minor variations into the hero or description tags
        $Content = $Content -replace 'professional cleaning', "$Adj cleaning"
        $Content = $Content -replace 'top-rated', "$Adj"
        
        # This is a basic form of spinning. A more advanced version would parse the actual paragraph text.
        # For now, we will inject a hidden span or slightly alter the visible text to break exact match duplication.
        $Content = $Content -replace '(?is)(<h1[^>]*>.*?)(</h1>)', "`${1} - $Adj Service`${2}"
        
        [System.IO.File]::WriteAllText($HubPath, $Content, [System.Text.Encoding]::UTF8)
        $Count++
    }
    
    # 2. Randomize Service Pages
    foreach ($SvcDir in $Services) {
        $SvcPath = "$RootDir\$($City.Slug)\$($SvcDir.Name)\index.html"
        if (Test-Path $SvcPath) {
            $Content = [System.IO.File]::ReadAllText($SvcPath, [System.Text.Encoding]::UTF8)
            
            $Adj = $Adjectives | Get-Random
            $Intro = $Intros | Get-Random
            $Outro = $Outros | Get-Random
            
            $Content = $Content -replace 'professional cleaning', "$Adj cleaning"
            $Content = $Content -replace 'top-rated', "$Adj"
            $Content = $Content -replace '(?is)(<h2[^>]*>.*?)(</h2>)', "`${1} - $Adj Experts`${2}"
            
            [System.IO.File]::WriteAllText($SvcPath, $Content, [System.Text.Encoding]::UTF8)
            $Count++
        }
    }
}

Write-Host "Content randomization completed on $Count pages."
