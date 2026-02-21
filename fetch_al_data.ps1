$Url = "https://raw.githubusercontent.com/kelvins/US-Cities-Database/main/csv/us_cities.csv"
$OutputJson = "c:\Users\lucia\OneDrive\Desktop\ZOIRISCLEANING\al_cities_raw.json"
$OutputCsv = "$env:TEMP\us_cities.csv"

Write-Host "Downloading US Cities database..."
Invoke-WebRequest -Uri $Url -OutFile $OutputCsv

Write-Host "Parsing CSV..."
$CsvData = Import-Csv $OutputCsv

$AlCities = @{}

foreach ($Row in $CsvData) {
    if ($Row.STATE_CODE -eq 'AL') {
        $Slug = $Row.CITY.ToLower() -replace ' ', '-' -replace "'", ""
        if (-not $AlCities.ContainsKey($Slug)) {
            $AlCities[$Slug] = @{
                Name = $Row.CITY
                Slug = $Slug
                County = "$($Row.COUNTY) County"
                Lat = $Row.LATITUDE
                Long = $Row.LONGITUDE
            }
        }
    }
}

$FinalList = $AlCities.Values | ForEach-Object { $_ }
$JsonContent = $FinalList | ConvertTo-Json -Depth 5 -Compress

[System.IO.File]::WriteAllText($OutputJson, $JsonContent, [System.Text.Encoding]::UTF8)

Write-Host ("Found {0} unique cities/towns in Alabama database." -f $FinalList.Count)
