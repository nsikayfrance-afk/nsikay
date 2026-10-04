-- =====================================
-- NSIKAY PostgreSQL TABLE GENERATOR v2.0
-- =====================================

BEGIN;

CREATE TABLE IF NOT EXISTS core.user (
 id UUID PRIMARY KEY,
 email VARCHAR(255) UNIQUE NOT NULL,
 created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS certification.request (
 id UUID PRIMARY KEY,
 status VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS business.company (
 id UUID PRIMARY KEY,
 name VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS finance.wallet (
 id UUID PRIMARY KEY,
 currency VARCHAR(10),
 balance NUMERIC DEFAULT 0
);

CREATE TABLE IF NOT EXISTS finance.transaction (
 id UUID PRIMARY KEY,
 amount NUMERIC
);

CREATE TABLE IF NOT EXISTS wenze.account (
 id UUID PRIMARY KEY,
 status VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS media.content (
 id UUID PRIMARY KEY,
 title TEXT
);

CREATE TABLE IF NOT EXISTS marketing.campaign (
 id UUID PRIMARY KEY,
 name TEXT
);

CREATE TABLE IF NOT EXISTS ai.model (
 id UUID PRIMARY KEY,
 name TEXT
);

CREATE TABLE IF NOT EXISTS audit.audit_log (
 id UUID PRIMARY KEY,
 action TEXT
);

COMMIT;

