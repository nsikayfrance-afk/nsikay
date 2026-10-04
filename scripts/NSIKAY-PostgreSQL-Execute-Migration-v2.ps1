$Root = Split-Path $PSScriptRoot -Parent

$ConfigFile = "$Root\config\postgresql_config.json"

$MigrationPath = "$Root\migrations\postgresql"

$ReportPath = "$Root\reports"

New-Item -ItemType Directory -Force -Path $ReportPath | Out-Null

$Date = Get-Date -Format "yyyyMMdd_HHmmss"

$Report = "$ReportPath\NSIKAY_REAL_MIGRATION_$Date.log"


Write-Host "===== NSIKAY POSTGRESQL REAL MIGRATION RUNNER v2.0 ====="


if (!(Test-Path $ConfigFile)) {

    Write-Host "Configuration PostgreSQL absente"
    exit

}


$config = Get-Content $ConfigFile -Raw | ConvertFrom-Json


$env:PGPASSWORD = $config.password


$Psql = "psql"


$Files = Get-ChildItem $MigrationPath -Filter "*.sql" | Sort-Object Name


"NSIKAY REAL MIGRATION v2.0" | Set-Content $Report
"DATE : $Date" | Add-Content $Report
"" | Add-Content $Report


foreach ($file in $Files) {


    Write-Host ""
    Write-Host "Execution SQL :" $file.Name


    Add-Content $Report "EXECUTION : $($file.Name)"


    & $Psql `
    -h $config.host `
    -p $config.port `
    -U $config.username `
    -d $config.database `
    -v ON_ERROR_STOP=1 `
    -f $file.FullName


    if ($LASTEXITCODE -ne 0) {

        Write-Host "ERREUR migration :" $file.Name

        Add-Content $Report "ERREUR : $($file.Name)"

        exit 1

    }


    Add-Content $Report "OK : $($file.Name)"

}


Write-Host ""
Write-Host "Toutes les migrations PostgreSQL sont terminées"


Add-Content $Report "MIGRATION COMPLETE"


Write-Host "Rapport :"
Write-Host $Report


Read-Host "Appuyez sur ENTREE pour fermer"

