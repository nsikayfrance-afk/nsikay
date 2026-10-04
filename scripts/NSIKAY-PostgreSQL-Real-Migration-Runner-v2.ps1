$Root = Split-Path $PSScriptRoot -Parent

$ConfigFile = "$Root\config\postgresql_config.json"
$MigrationPath = "$Root\migrations\postgresql"
$ReportPath = "$Root\reports"

$PSQL = "C:\Program Files\PostgreSQL\17\bin\psql.exe"

$Date = Get-Date -Format "yyyyMMdd_HHmmss"
$Report = "$ReportPath\NSIKAY_REAL_MIGRATION_$Date.log"

New-Item -ItemType Directory -Force -Path $ReportPath | Out-Null

Write-Host "===== NSIKAY POSTGRESQL REAL MIGRATION v2.0 ====="


$config = Get-Content $ConfigFile -Raw | ConvertFrom-Json


if (!(Test-Path $PSQL)) {

    Write-Host "psql introuvable"
    exit

}


"NSIKAY REAL MIGRATION v2.0" | Set-Content $Report


$Files = Get-ChildItem $MigrationPath -Filter "*.sql" | Sort-Object Name


foreach ($file in $Files) {


    Write-Host ""
    Write-Host "Execution :" $file.Name


    Add-Content $Report "EXECUTION : $($file.Name)"


    & $PSQL `
    -h $config.host `
    -p $config.port `
    -U $config.username `
    -d $config.database `
    -v ON_ERROR_STOP=1 `
    -f $file.FullName


    if ($LASTEXITCODE -ne 0) {

        Write-Host "ERREUR SQL :" $file.Name

        Add-Content $Report "ERREUR : $($file.Name)"

        exit 1
    }


    Add-Content $Report "OK : $($file.Name)"
}


Write-Host ""
Write-Host "===== MIGRATION NSIKAY TERMINEE ====="

Add-Content $Report "MIGRATION COMPLETE"

Write-Host "Rapport : $Report"


Read-Host "Appuyez sur ENTREE pour fermer"


