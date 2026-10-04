Write-Host "===== NSIKAY POSTGRESQL MIGRATION ENGINE v2.0 ====="

$Root = Split-Path $PSScriptRoot -Parent

$MatrixFile = "$Root\matrices\postgresql_matrix.json"
$Output = "$Root\migrations\postgresql"

if (!(Test-Path $MatrixFile)) {
    Write-Host "ERREUR : matrice absente"
    exit
}

New-Item -ItemType Directory -Force -Path $Output | Out-Null

$Matrix = Get-Content $MatrixFile -Raw | ConvertFrom-Json

$Date = Get-Date -Format "yyyyMMdd_HHmmss"

$SQLFile = "$Output\NSIKAY_MIGRATION_$Date.sql"

$sql = "-- NSIKAY PostgreSQL Migration v2.0`n`nBEGIN;`n`n"

foreach ($schema in $Matrix.schemas) {
    $sql += "CREATE SCHEMA IF NOT EXISTS $($schema.schema);`n"
}

$sql += "`nCOMMIT;"

$sql | Set-Content $SQLFile -Encoding UTF8

Write-Host "Migration créée :"
Write-Host $SQLFile
