$RootDir = "c:\Users\lucia\OneDrive\Desktop\ZOIRISCLEANING"
$ExcludeDirs = @('.git', '.github', 'tmp', '.gemini', 'upload', 'favicon', 'Gallery', 'about', 'contact', 'blog', 'apply')

$count = 0
$updated = 0

$filesToProcess = @("$RootDir\index.html")
$dirs = Get-ChildItem -Path $RootDir -Directory | Where-Object { $_.Name -notin $ExcludeDirs }

foreach ($dir in $dirs) {
    if (Test-Path (Join-Path $dir.FullName "index.html")) { $filesToProcess += Join-Path $dir.FullName "index.html" }
    foreach ($subDir in Get-ChildItem -Path $dir.FullName -Directory) {
        if (Test-Path (Join-Path $subDir.FullName "index.html")) { $filesToProcess += Join-Path $subDir.FullName "index.html" }
    }
}

foreach ($path in $filesToProcess) {
    $content = [System.IO.File]::ReadAllText($path, [System.Text.Encoding]::UTF8)
    
    # Check if FAQPage already exists
    if ($content -match '"@type"\s*:\s*"FAQPage"') { continue }
    
    # Extract location if possible
    $loc = "Mobile, AL"
    $relPath = ($path -replace [regex]::Escape($RootDir), "").Trim('\')
    $parts = $relPath -split '\\'
    if ($parts.Count -ge 2 -and -not [string]::IsNullOrWhiteSpace($parts[0])) {
        $locSlug = $parts[0]
        $words = $locSlug -split '-'
        $loc = ($words | ForEach-Object { if ($_.Length -gt 0) { $_.Substring(0,1).ToUpper() + $_.Substring(1).ToLower() } }) -join ' '
    }

    $schema = @"
<!-- FAQ Schema -->
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "Do you offer same-day cleaning in $loc?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Yes! Zoiris Cleaning Service provides same-day cleaning for homes, apartments, offices, and Airbnb rentals across $loc and surrounding areas. Call (251) 930-8621."
      }
    },
    {
      "@type": "Question",
      "name": "Do you use eco-friendly cleaning products in $loc?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Yes! We exclusively use eco-friendly, non-toxic cleaning products that are safe for kids, pets, and the environment in $loc."
      }
    }
  ]
}
</script>
</head>
"@

    $content = $content -replace '(?i)</head>', $schema
    [System.IO.File]::WriteAllText($path, $content, [System.Text.Encoding]::UTF8)
    $updated++
    $count++
}

Write-Host "Injected FAQ Schema on $updated out of $($filesToProcess.Count) pages!"
