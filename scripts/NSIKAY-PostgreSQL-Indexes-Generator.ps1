$Root = Split-Path $PSScriptRoot -Parent

$Output = "$Root\migrations\postgresql"

New-Item -ItemType Directory -Force -Path $Output | Out-Null

$Date = Get-Date -Format "yyyyMMdd_HHmmss"

$SQLFile = "$Output\NSIKAY_INDEXES_$Date.sql"

$sql = @"
-- =====================================
-- NSIKAY PostgreSQL INDEXES v2.0
-- =====================================

BEGIN;

-- CORE
CREATE INDEX IF NOT EXISTS idx_user_email
ON core.user(email);

CREATE INDEX IF NOT EXISTS idx_user_profile_user_id
ON core.user_profile(user_id);

-- CERTIFICATION
CREATE INDEX IF NOT EXISTS idx_certification_user_id
ON certification.request(user_id);

CREATE INDEX IF NOT EXISTS idx_certification_status
ON certification.request(status);

-- BUSINESS
CREATE INDEX IF NOT EXISTS idx_company_name
ON business.company(name);

-- FINANCE
CREATE INDEX IF NOT EXISTS idx_wallet_owner_id
ON finance.wallet(owner_id);

CREATE INDEX IF NOT EXISTS idx_wallet_currency
ON finance.wallet(currency);

CREATE INDEX IF NOT EXISTS idx_transaction_wallet_id
ON finance.transaction(wallet_id);

CREATE INDEX IF NOT EXISTS idx_transaction_created_at
ON finance.transaction(created_at);

-- WENZE
CREATE INDEX IF NOT EXISTS idx_wenze_user_id
ON wenze.account(user_id);

-- MEDIA
CREATE INDEX IF NOT EXISTS idx_media_content_created_by
ON media.content(created_by);

CREATE INDEX IF NOT EXISTS idx_media_content_title
ON media.content(title);

-- MARKETING
CREATE INDEX IF NOT EXISTS idx_campaign_created_by
ON marketing.campaign(created_by);

CREATE INDEX IF NOT EXISTS idx_campaign_dates
ON marketing.campaign(start_date,end_date);

-- AI
CREATE INDEX IF NOT EXISTS idx_ai_model_name
ON ai.model(name);

-- AUDIT
CREATE INDEX IF NOT EXISTS idx_audit_user_id
ON audit.audit_log(user_id);

CREATE INDEX IF NOT EXISTS idx_audit_created_at
ON audit.audit_log(created_at);

COMMIT;

"@

$sql | Set-Content $SQLFile -Encoding UTF8

Write-Host "Migration INDEXES créée :"
Write-Host $SQLFile
