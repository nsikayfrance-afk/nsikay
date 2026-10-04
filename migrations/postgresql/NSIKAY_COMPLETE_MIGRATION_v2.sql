
-- ==========================================
-- NSIKAY COMPLETE MIGRATION v2.0
-- PostgreSQL
-- 13 MODULES
-- ==========================================

BEGIN;


-- ==========================================
-- 1. SCHEMAS
-- ==========================================

CREATE SCHEMA IF NOT EXISTS core;
CREATE SCHEMA IF NOT EXISTS certification;
CREATE SCHEMA IF NOT EXISTS business;
CREATE SCHEMA IF NOT EXISTS finance;
CREATE SCHEMA IF NOT EXISTS wenze;
CREATE SCHEMA IF NOT EXISTS media;
CREATE SCHEMA IF NOT EXISTS marketing;
CREATE SCHEMA IF NOT EXISTS ai;
CREATE SCHEMA IF NOT EXISTS audit;


-- ==========================================
-- 2. TABLES
-- ==========================================


CREATE TABLE IF NOT EXISTS core.users
(
id BIGSERIAL PRIMARY KEY,
email VARCHAR(255) UNIQUE NOT NULL,
created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE IF NOT EXISTS certification.certification
(
id BIGSERIAL PRIMARY KEY,
user_id BIGINT,
status VARCHAR(50),
created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE IF NOT EXISTS business.company
(
id BIGSERIAL PRIMARY KEY,
name TEXT,
created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE IF NOT EXISTS finance.wallet
(
id BIGSERIAL PRIMARY KEY,
user_id BIGINT,
balance NUMERIC(18,2) DEFAULT 0,
created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE IF NOT EXISTS finance.transaction
(
id BIGSERIAL PRIMARY KEY,
wallet_id BIGINT,
amount NUMERIC(18,2),
created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE IF NOT EXISTS wenze.transfer
(
id BIGSERIAL PRIMARY KEY,
sender_id BIGINT,
receiver_id BIGINT,
amount NUMERIC(18,2),
created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE IF NOT EXISTS media.content
(
id BIGSERIAL PRIMARY KEY,
title TEXT,
created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE IF NOT EXISTS marketing.campaign
(
id BIGSERIAL PRIMARY KEY,
name TEXT,
created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE IF NOT EXISTS marketing.event
(
id BIGSERIAL PRIMARY KEY,
name TEXT,
created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE IF NOT EXISTS ai.model
(
id BIGSERIAL PRIMARY KEY,
name TEXT,
created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE IF NOT EXISTS audit.audit_log
(
id BIGSERIAL PRIMARY KEY,
action TEXT,
created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


-- ==========================================
-- 3. FOREIGN KEYS
-- ==========================================


ALTER TABLE certification.certification
DROP CONSTRAINT IF EXISTS fk_certification_user;

ALTER TABLE certification.certification
ADD CONSTRAINT fk_certification_user
FOREIGN KEY(user_id)
REFERENCES core.users(id);



ALTER TABLE finance.wallet
DROP CONSTRAINT IF EXISTS fk_wallet_user;

ALTER TABLE finance.wallet
ADD CONSTRAINT fk_wallet_user
FOREIGN KEY(user_id)
REFERENCES core.users(id);



ALTER TABLE finance.transaction
DROP CONSTRAINT IF EXISTS fk_transaction_wallet;

ALTER TABLE finance.transaction
ADD CONSTRAINT fk_transaction_wallet
FOREIGN KEY(wallet_id)
REFERENCES finance.wallet(id);



-- ==========================================
-- 4. INDEX POSTGRESQL
-- ==========================================

CREATE INDEX IF NOT EXISTS idx_users_email
ON core.users(email);


CREATE INDEX IF NOT EXISTS idx_wallet_user
ON finance.wallet(user_id);


CREATE INDEX IF NOT EXISTS idx_transaction_created
ON finance.transaction(created_at);


CREATE INDEX IF NOT EXISTS idx_audit_created
ON audit.audit_log(created_at);



-- ==========================================
-- 5. SECURITY
-- ==========================================

CREATE TABLE IF NOT EXISTS audit.security_event
(
id BIGSERIAL PRIMARY KEY,
event_type TEXT,
created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);



-- ==========================================
-- 6. AUDIT TRAIL
-- ==========================================

CREATE TABLE IF NOT EXISTS audit.change_history
(
id BIGSERIAL PRIMARY KEY,
table_name TEXT,
operation TEXT,
created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);



-- ==========================================
-- 7. VALIDATION
-- ==========================================

CREATE TABLE IF NOT EXISTS audit.migration_control
(
id BIGSERIAL PRIMARY KEY,
migration_name TEXT,
executed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);



COMMIT;


-- ==========================================
-- NSIKAY COMPLETE MIGRATION FINISHED
-- ==========================================
