$RootDir = "c:\Users\lucia\OneDrive\Desktop\ZOIRISCLEANING"
$path = "$RootDir\maid-service-mobile-al\index.html"

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

$info = Get-PageInfo $path
Write-Host "Info Type: $($info.Type)"
Write-Host "Info Loc: $($info.Location)"

$loc = $info.Location
$srv = $info.Service

$title = "#1 $loc Cleaning Service | Top-Rated Cleaners | Zoiris"
$desc = "Need a trusted cleaning service in $loc? Zoiris Cleaning offers the highest-rated residential and commercial cleaning in $loc. Fast, affordable, and spotless. Call (251) 930-8621 today!"
$h1 = "Expert Cleaning Services in $loc"

$content = [System.IO.File]::ReadAllText($path, [System.Text.Encoding]::UTF8)
$originalContent = $content

$titleRegex = [regex]'(?is)<title>.*?</title>'
if ($titleRegex.IsMatch($content)) {
    $content = $titleRegex.Replace($content, "<title>$title</title>")
    Write-Host "Title matched."
}

$descRegex = [regex]'(?is)<meta[^>]*name=["'']description["''][^>]*>'
$newDesc = '<meta name="description" content="{0}">' -f $desc
if ($descRegex.IsMatch($content)) {
    $content = $descRegex.Replace($content, $newDesc)
    Write-Host "Desc matched."
}

$h1Regex = [regex]'(?<=(?is)<h1[^>]*>).*?(?=</h1>)'
if ($h1Regex.IsMatch($content)) {
    $content = $h1Regex.Replace($content, $h1)
    Write-Host "H1 matched."
}

if ($content -ne $originalContent) {
    Write-Host "DIFFERENT"
} else {
    Write-Host "SAME"
}
