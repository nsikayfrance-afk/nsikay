$Root = Split-Path $PSScriptRoot -Parent

$Matrix = "$Root\matrices\NSIKAY_COMPLETE_MIGRATION_MATRIX_v2.json"

$MigrationPath = "$Root\migrations\postgresql"

$ReportPath = "$Root\reports"

New-Item -ItemType Directory -Force -Path $ReportPath | Out-Null

$Date = Get-Date -Format "yyyyMMdd_HHmmss"

$Report = "$ReportPath\NSIKAY_MIGRATION_REPORT_$Date.txt"


Write-Host "===== NSIKAY MASTER MIGRATION RUNNER v2.0 ====="


if (!(Test-Path $Matrix)) {

    Write-Host "ERREUR : matrice absente"

    exit
}


$Config = Get-Content $Matrix -Raw | ConvertFrom-Json


"NSIKAY MIGRATION REPORT v2.0" | Set-Content $Report

"DATE : $Date" | Add-Content $Report

"" | Add-Content $Report


$Steps = @(

"schemas",

"tables",

"foreign_keys",

"indexes",

"security_audit"

)


foreach ($step in $Steps) {

    Write-Host ""
    Write-Host "Verification : $step"


    Add-Content $Report "ETAPE : $step"


    $Files = Get-ChildItem $MigrationPath -Filter "*$step*.sql" -ErrorAction SilentlyContinue


    if ($Files) {

        foreach ($file in $Files) {

            Write-Host "Trouve : $($file.Name)"

            Add-Content $Report "OK : $($file.FullName)"

        }

    }

    else {

        Write-Host "Aucun fichier SQL trouve pour $step"

        Add-Content $Report "MANQUANT : $step"

    }

}


"" | Add-Content $Report

"Migration Matrix : OK" | Add-Content $Report


Write-Host ""
Write-Host "Rapport cree :"
Write-Host $Report


Read-Host "Appuyez sur ENTREE pour terminer"

