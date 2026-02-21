$RootDir = "c:\Users\lucia\OneDrive\Desktop\ZOIRISCLEANING"

$path = "$RootDir\maid-service-mobile-al\index.html"
$content = [System.IO.File]::ReadAllText($path, [System.Text.Encoding]::UTF8)
$originalContent = $content

$titleRegex = [regex]'(?is)<title>.*?</title>'
if ($titleRegex.IsMatch($content)) {
    Write-Host "Title Matches!"
    $content = $titleRegex.Replace($content, "<title>TEST TITLE</title>")
} else {
    Write-Host "Title No Match"
}

$descRegex = [regex]'(?is)<meta[^>]*name=["'']description["''][^>]*>'
if ($descRegex.IsMatch($content)) {
    Write-Host "Desc Matches!"
    $content = $descRegex.Replace($content, '<meta name="description" content="TEST DESC">')
}

$h1Regex = [regex]'(?<=(?is)<h1[^>]*>).*?(?=</h1>)'
if ($h1Regex.IsMatch($content)) {
    Write-Host "H1 Matches!"
    $content = $h1Regex.Replace($content, "TEST H1")
}

Write-Host "Original length: $($originalContent.Length)"
Write-Host "New length: $($content.Length)"

if ($content -ne $originalContent) {
    Write-Host "DIFFERENT"
} else {
    Write-Host "SAME"
}
