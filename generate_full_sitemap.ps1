$BaseUrl = "https://www.zoiriscleaningservices.com"
$RootDir = "c:\Users\lucia\OneDrive\Desktop\ZOIRISCLEANING"
$Today = Get-Date -Format 'yyyy-MM-dd'

$ExcludeDirs = @('.git', '.github', 'upload', 'favicon', 'tmp', '.gemini')

Write-Host "Generating complete sitemap.xml..."

$HtmlFiles = @()
$HtmlFiles += "$RootDir\index.html"
$dirs = Get-ChildItem -Path $RootDir -Directory | Where-Object { $_.Name -notin $ExcludeDirs }

foreach ($dir in $dirs) {
    if (Test-Path (Join-Path $dir.FullName "index.html")) { $HtmlFiles += Join-Path $dir.FullName "index.html" }
    foreach ($subDir in Get-ChildItem -Path $dir.FullName -Directory) {
        if (Test-Path (Join-Path $subDir.FullName "index.html")) { $HtmlFiles += Join-Path $subDir.FullName "index.html" }
    }
}

$Urls = @()

foreach ($f in $HtmlFiles) {
    $RelPath = $f -replace [regex]::Escape($RootDir), ""
    $RelPath = $RelPath.Trim('\').Replace('\', '/')
    
    if ($RelPath -eq "index.html") {
        $Url = "$BaseUrl/"
        $Priority = "1.0"
        $ChangeFreq = "weekly"
    } else {
        $DirPart = $RelPath -replace '/index.html', ''
        $Url = "$BaseUrl/$DirPart/"
        
        if ($DirPart -match "^services/") {
            $Priority = "0.95"
            $ChangeFreq = "weekly"
        } elseif (-not ($DirPart -match "/")) {
            $Priority = "0.9"
            $ChangeFreq = "weekly"
        } else {
            $Priority = "0.8"
            $ChangeFreq = "monthly"
        }
    }
    
    $Urls += @{ Loc=$Url; LastMod=$Today; ChangeFreq=$ChangeFreq; Priority=$Priority }
}

$Urls = $Urls | Sort-Object { $_.Loc }

$Xml = @()
$Xml += '<?xml version="1.0" encoding="UTF-8"?>'
$Xml += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">'

foreach ($u in $Urls) {
    $Xml += '  <url>'
    $Xml += "    <loc>$($u.Loc)</loc>"
    $Xml += "    <lastmod>$($u.LastMod)</lastmod>"
    $Xml += "    <changefreq>$($u.ChangeFreq)</changefreq>"
    $Xml += "    <priority>$($u.Priority)</priority>"
    $Xml += '  </url>'
}
$Xml += '</urlset>'

[System.IO.File]::WriteAllText("$RootDir\sitemap.xml", ($Xml -join "`n"), [System.Text.Encoding]::UTF8)

Write-Host "Sitemap generated with $($Urls.Count) URLs."
