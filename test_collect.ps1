$RootDir = "c:\Users\lucia\OneDrive\Desktop\ZOIRISCLEANING"
$ExcludeDirs = @('.git', '.github', 'tmp', '.gemini', 'upload', 'favicon', 'Gallery', 'about', 'contact', 'blog', 'apply')

$files = @()
$dirs = Get-ChildItem -Path $RootDir -Directory | Where-Object { $_.Name -notin $ExcludeDirs }

foreach ($dir in $dirs) {
    $hubIndex = Join-Path $dir.FullName "index.html"
    if (Test-Path $hubIndex) { $files += $hubIndex }
}

Write-Host "Found $($files.Count) files."
if ($files.Count -gt 0) {
    Write-Host "First file: $($files[0])"
    
    $path = $files[0]
    $relPath = $path -replace [regex]::Escape($RootDir), ""
    $relPath = $relPath.Trim('\')
    
    Write-Host "RelPath: $relPath"
}
