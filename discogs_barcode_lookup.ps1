param (
    [string]$inputfile, 
    [string]$outputfile,    
    [string]$apitoken
)
# takes a list of barcodes in the input file, looks them up on discogs.com site
# and outputs the results to a csv file (output).
# Requires a API token from Discogs dev site.
# Used zbar barcode scanner to generate the barcodes (http://zbar.sourceforge.net)

if (Test-Path $outputfile) { del $outputfile }
foreach($line in Get-Content $inputfile) {
    $barcode = $line.replace("EAN-13:", "")
    $a = Invoke-RestMethod -Uri "https://api.discogs.com/database/search?q=${barcode}&barcode&token=${apitoken}" -UserAgent lps-finder

    if ($a.results.Length -eq 0) { write-output "No results returned for $barcode" }
    foreach ($item in $a.results) {$item | select-object catno,year,title,id |  export-csv -Path $outputfile -Append }
}