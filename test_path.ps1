$RootDir = "c:\Users\lucia\OneDrive\Desktop\ZOIRISCLEANING"

$path = "$RootDir\maid-service-mobile-al\index.html"
$relPath = $path -replace [regex]::Escape($RootDir), ""
$relPath = $relPath.Trim('\')
$parts = $relPath -split '\\'

Write-Host "Relpath: $relPath"
Write-Host "Parts count: $($parts.Count)"
Write-Host "Part 0: $($parts[0])"
Write-Host "Part 1: $($parts[1])"
