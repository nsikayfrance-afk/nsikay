$Root = Split-Path $PSScriptRoot -Parent

$Output = "$Root\migrations\postgresql"

New-Item -ItemType Directory -Force -Path $Output | Out-Null

$Date = Get-Date -Format "yyyyMMdd_HHmmss"

$SQLFile = "$Output\NSIKAY_SECURITY_AUDIT_$Date.sql"

$sql = @"
-- =====================================
-- NSIKAY PostgreSQL SECURITY AUDIT v2.0
-- =====================================

BEGIN;

-- =====================================
-- AUDIT TRAIL TABLES
-- =====================================

CREATE TABLE IF NOT EXISTS audit.audit_event (
    id UUID PRIMARY KEY,
    user_id UUID,
    action VARCHAR(100) NOT NULL,
    entity VARCHAR(100),
    entity_id UUID,
    ip_address VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE IF NOT EXISTS audit.security_event (
    id UUID PRIMARY KEY,
    user_id UUID,
    event_type VARCHAR(100) NOT NULL,
    severity VARCHAR(50),
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


-- =====================================
-- SECURITY CONSTRAINTS
-- =====================================

ALTER TABLE core.user
ADD CONSTRAINT chk_user_email_not_empty
CHECK (email <> '');


ALTER TABLE finance.wallet
ADD CONSTRAINT chk_wallet_balance_positive
CHECK (balance >= 0);


ALTER TABLE finance.transaction
ADD CONSTRAINT chk_transaction_amount_positive
CHECK (amount > 0);


ALTER TABLE certification.request
ADD CONSTRAINT chk_certification_status
CHECK (
status IN (
'pending',
'approved',
'rejected',
'expired'
)
);


-- =====================================
-- ROLE SECURITY
-- =====================================

CREATE ROLE nsikay_readonly;

CREATE ROLE nsikay_application;


GRANT USAGE ON SCHEMA core TO nsikay_application;
GRANT USAGE ON SCHEMA finance TO nsikay_application;
GRANT USAGE ON SCHEMA audit TO nsikay_application;


-- =====================================
-- AUDIT INDEXES
-- =====================================

CREATE INDEX IF NOT EXISTS idx_audit_event_user
ON audit.audit_event(user_id);


CREATE INDEX IF NOT EXISTS idx_audit_event_date
ON audit.audit_event(created_at);


CREATE INDEX IF NOT EXISTS idx_security_event_type
ON audit.security_event(event_type);


-- =====================================
-- UPDATED TIMESTAMP SUPPORT
-- =====================================

CREATE OR REPLACE FUNCTION audit.update_timestamp()
RETURNS TRIGGER AS \$\$
BEGIN
NEW.updated_at = CURRENT_TIMESTAMP;
RETURN NEW;
END;
\$\$ LANGUAGE plpgsql;


COMMIT;

"@

$sql | Set-Content $SQLFile -Encoding UTF8

Write-Host "Migration SECURITY AUDIT créée :"
Write-Host $SQLFile
