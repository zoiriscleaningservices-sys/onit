$RootDir = "c:\Users\lucia\OneDrive\Desktop\ZOIRISCLEANING"
$ExcludeDirs = @('.git', '.github', 'tmp', '.gemini', 'upload', 'favicon', 'Gallery', 'about', 'contact', 'blog', 'apply')

function Format-Name ($slug) {
    if ([string]::IsNullOrWhiteSpace($slug)) { return "" }
    $words = $slug -split '-'
    $capitalized = $words | ForEach-Object {
        if ($_.Length -gt 0) {
            $_.Substring(0,1).ToUpper() + $_.Substring(1).ToLower()
        }
    }
    return $capitalized -join ' '
}

function Get-PageInfo ($filepath) {
    $relPath = $filepath -replace [regex]::Escape($RootDir), ""
    $relPath = $relPath.Trim('\')
    $parts = $relPath -split '\\'
    
    if ($parts.Count -eq 1 -and $parts[0].ToLower() -eq 'index.html') {
        return @{ Type="home"; Location="Mobile, AL"; Service="Cleaning" }
    }
    if ($parts.Count -eq 2 -and $parts[1].ToLower() -eq 'index.html') {
        return @{ Type="location_hub"; Location=(Format-Name $parts[0]); Service="Cleaning" }
    }
    if ($parts.Count -eq 3 -and $parts[2].ToLower() -eq 'index.html') {
        $srvSlug = $parts[1]
        if ($srvSlug.ToLower() -eq 'detailing-mobile-al') {
            $srvSlug = 'Detailing'
        }
        return @{ Type="service"; Location=(Format-Name $parts[0]); Service=(Format-Name $srvSlug) }
    }
    return $null
}

function Generate-SeoContent ($info) {
    $loc = $info.Location
    $srv = $info.Service
    
    if ($info.Type -eq "home") {
        $title = "Top-Rated Cleaning Service in Mobile, AL | Zoiris Cleaning"
        $desc = "Looking for the best cleaning service in Mobile, AL? Zoiris Cleaning Services offers highly-rated house and commercial cleaning. Call (251) 930-8621 for a free quote!"
        $h1 = "Top-Rated Cleaning Service in Mobile, AL"
    }
    elseif ($info.Type -eq "location_hub") {
        $title = "Expert $loc Cleaning Service | Top-Rated Cleaners | Zoiris"
        $desc = "Trusted cleaning service in $loc. Zoiris Cleaning offers the highest-rated residential and commercial cleaning in $loc. Call (251) 930-8621 today!"
        $h1 = "Expert Cleaning Services in $loc"
    }
    else {
        $srvName = $srv
        if (-not ($srv -match "Cleaning")) {
            $srvName = "$srv Cleaning"
        }
        $title = "Best $srvName in $loc | 5-Star Rated | Zoiris Cleaning"
        $desc = "Professional $srvName in $loc. We are the top-rated local experts. Affordable, reliable, and guaranteed spotless. Call (251) 930-8621!"
        $h1 = "Professional $srvName in $loc"
    }
    
    return @{ Title=$title; Desc=$desc; H1=$h1 }
}

$count = 0
$updated = 0

$filesToProcess = @("$RootDir\index.html")
$dirs = Get-ChildItem -Path $RootDir -Directory | Where-Object { $_.Name -notin $ExcludeDirs }

foreach ($dir in $dirs) {
    $hubIndex = Join-Path $dir.FullName "index.html"
    if (Test-Path $hubIndex) { $filesToProcess += $hubIndex }
    
    $subDirs = Get-ChildItem -Path $dir.FullName -Directory
    foreach ($subDir in $subDirs) {
        $svcIndex = Join-Path $subDir.FullName "index.html"
        if (Test-Path $svcIndex) { $filesToProcess += $svcIndex }
    }
}

foreach ($path in $filesToProcess) {
    if (-not (Test-Path $path)) { continue }
    
    $info = Get-PageInfo $path
    if ($null -eq $info) { continue }
    
    $seo = Generate-SeoContent $info
    
    $content = [System.IO.File]::ReadAllText($path, [System.Text.Encoding]::UTF8)
    $originalContent = $content
    
    # 1. Title
    $safeTitle = $seo.Title.Replace('$', '$$')
    $content = $content -replace '(?is)<title>.*?</title>', "<title>$safeTitle</title>"
    
    # 2. Description
    $safeDesc = $seo.Desc.Replace('$', '$$')
    $content = $content -replace '(?is)<meta[^>]*name=["'']description["''][^>]*>', "<meta name=""description"" content=""$safeDesc"">"
    
    # 3. H1
    $safeH1 = $seo.H1.Replace('$', '$$')
    $content = $content -replace '(?<=(?is)<h1[^>]*>).*?(?=</h1>)', "$safeH1"
    
    if ($content -ne $originalContent) {
        [System.IO.File]::WriteAllText($path, $content, [System.Text.Encoding]::UTF8)
        $updated++
    }
    $count++
}

Write-Host "Processed $count pages. Updated $updated pages."
