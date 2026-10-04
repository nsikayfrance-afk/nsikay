$Root = Split-Path $PSScriptRoot -Parent

$Output = "$Root\migrations\postgresql"

New-Item -ItemType Directory -Force -Path $Output | Out-Null

$Date = Get-Date -Format "yyyyMMdd_HHmmss"

$SQLFile = "$Output\NSIKAY_FOREIGN_KEYS_$Date.sql"

$sql = @"
-- =====================================
-- NSIKAY PostgreSQL FOREIGN KEYS v2.0
-- =====================================

BEGIN;

ALTER TABLE IF EXISTS core.user_profile
ADD CONSTRAINT fk_user_profile_user
FOREIGN KEY (user_id)
REFERENCES core.user(id);

ALTER TABLE IF EXISTS certification.request
ADD CONSTRAINT fk_certification_user
FOREIGN KEY (user_id)
REFERENCES core.user(id);

ALTER TABLE IF EXISTS business.company
ADD CONSTRAINT fk_company_owner
FOREIGN KEY (id)
REFERENCES core.user(id);

ALTER TABLE IF EXISTS finance.wallet
ADD CONSTRAINT fk_wallet_owner
FOREIGN KEY (owner_id)
REFERENCES core.user(id);

ALTER TABLE IF EXISTS finance.transaction
ADD CONSTRAINT fk_transaction_wallet
FOREIGN KEY (wallet_id)
REFERENCES finance.wallet(id);

ALTER TABLE IF EXISTS wenze.account
ADD CONSTRAINT fk_wenze_user
FOREIGN KEY (user_id)
REFERENCES core.user(id);

ALTER TABLE IF EXISTS media.content
ADD COLUMN IF NOT EXISTS created_by UUID;

ALTER TABLE IF EXISTS media.content
ADD CONSTRAINT fk_media_creator
FOREIGN KEY (created_by)
REFERENCES core.user(id);

ALTER TABLE IF EXISTS marketing.campaign
ADD COLUMN IF NOT EXISTS created_by UUID;

ALTER TABLE IF EXISTS marketing.campaign
ADD CONSTRAINT fk_campaign_creator
FOREIGN KEY (created_by)
REFERENCES core.user(id);

ALTER TABLE IF EXISTS ai.model
ADD COLUMN IF NOT EXISTS created_by UUID;

ALTER TABLE IF EXISTS ai.model
ADD CONSTRAINT fk_ai_creator
FOREIGN KEY (created_by)
REFERENCES core.user(id);

ALTER TABLE IF EXISTS audit.audit_log
ADD COLUMN IF NOT EXISTS user_id UUID;

ALTER TABLE IF EXISTS audit.audit_log
ADD CONSTRAINT fk_audit_user
FOREIGN KEY (user_id)
REFERENCES core.user(id);

COMMIT;

"@

$sql | Set-Content $SQLFile -Encoding UTF8

Write-Host "Migration FOREIGN KEYS créée :"
Write-Host $SQLFile
