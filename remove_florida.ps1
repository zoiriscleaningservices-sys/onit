$FloridaCities = @("destin", "seaside", "pensacola-beach", "panama-city-beach", "miramar-beach", "30a", "santa-rosa-beach", "bradenton-fl", "tampa", "tampa-fl")
$RootDir = "c:\Users\lucia\OneDrive\Desktop\ZOIRISCLEANING"

Write-Host "Searching for Florida directories..."
foreach ($City in $FloridaCities) {
    # Check exact match
    $DirPath = Join-Path $RootDir $City
    if (Test-Path $DirPath) {
        Write-Host "Deleting Florida directory: $City"
        Remove-Item -Path $DirPath -Recurse -Force
    }
}

# Also check if there are any other directories with "-fl" in the name and delete them
$FlDirs = Get-ChildItem -Path $RootDir -Directory -Filter "*-fl"
foreach ($Dir in $FlDirs) {
    Write-Host "Deleting Florida directory: $($Dir.Name)"
    Remove-Item -Path $Dir.FullName -Recurse -Force
}

$FlDirs2 = Get-ChildItem -Path $RootDir -Directory -Filter "*florida*"
foreach ($Dir in $FlDirs2) {
    Write-Host "Deleting Florida directory: $($Dir.Name)"
    Remove-Item -Path $Dir.FullName -Recurse -Force
}

Write-Host "Done deleting Florida directories."
