$RootDir = "c:\Users\lucia\OneDrive\Desktop\ZOIRISCLEANING"
$ExcludeDirs = @('.git', '.github', 'tmp', '.gemini', 'upload', 'favicon', 'Gallery', 'about', 'contact', 'blog', 'apply')

$files = @()
$files += "$RootDir\index.html"
$dirs = Get-ChildItem -Path $RootDir -Directory | Where-Object { $_.Name -notin $ExcludeDirs }

foreach ($dir in $dirs) {
    if (Test-Path (Join-Path $dir.FullName "index.html")) { $files += Join-Path $dir.FullName "index.html" }
    foreach ($subDir in Get-ChildItem -Path $dir.FullName -Directory) {
        if (Test-Path (Join-Path $subDir.FullName "index.html")) { $files += Join-Path $subDir.FullName "index.html" }
    }
}

$updatedCount = 0

$pattern = '(?is)href="/services/gutter-cleaning/">Gutter Cleaning</a>\s*</div>\s*</div>\s*<!-- LOCATIONS Dropdown -->'
$replacement = "href=`"/services/gutter-cleaning/`">Gutter Cleaning</a>`n  </div>`n</div>`n</div>`n<!-- LOCATIONS Dropdown -->"

foreach ($path in $files) {
    $content = [System.IO.File]::ReadAllText($path, [System.Text.Encoding]::UTF8)
    
    if ($content -match $pattern) {
        $content = $content -replace $pattern, $replacement
        [System.IO.File]::WriteAllText($path, $content, [System.Text.Encoding]::UTF8)
        $updatedCount++
    }
}

Write-Host "Fixed Desktop Navigation Bug on $updatedCount pages."
