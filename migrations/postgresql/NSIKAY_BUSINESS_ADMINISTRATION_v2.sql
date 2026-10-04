BEGIN;

CREATE SCHEMA IF NOT EXISTS business;


-- TYPES D'ENTREPRISES
CREATE TABLE IF NOT EXISTS business.company_types (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL,
    description TEXT
);


-- SECTEURS D'ACTIVITÉ
CREATE TABLE IF NOT EXISTS business.sectors (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL,
    description TEXT
);


-- ENTREPRISES
CREATE TABLE IF NOT EXISTS business.companies (
    id SERIAL PRIMARY KEY,
    owner_id INTEGER NOT NULL,
    company_type_id INTEGER,
    sector_id INTEGER,
    legal_name VARCHAR(255) NOT NULL,
    logo TEXT,
    description TEXT,
    country VARCHAR(100),
    website TEXT,
    status VARCHAR(50) DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


-- PROFIL PUBLIC ENTREPRISE
CREATE TABLE IF NOT EXISTS business.public_profiles (
    id SERIAL PRIMARY KEY,
    company_id INTEGER NOT NULL,
    public_description TEXT,
    phone VARCHAR(50),
    social_links JSONB,
    visible BOOLEAN DEFAULT TRUE
);


-- ESPACE PRIVÉ ENTREPRISE
CREATE TABLE IF NOT EXISTS business.company_dashboards (
    id SERIAL PRIMARY KEY,
    company_id INTEGER NOT NULL,
    dashboard_settings JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


-- EMPLOYÉS
CREATE TABLE IF NOT EXISTS business.employees (
    id SERIAL PRIMARY KEY,
    company_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    position VARCHAR(100),
    status VARCHAR(50) DEFAULT 'active'
);


-- RÔLES ENTREPRISE
CREATE TABLE IF NOT EXISTS business.roles (
    id SERIAL PRIMARY KEY,
    company_id INTEGER,
    name VARCHAR(100) NOT NULL
);


-- PERMISSIONS
CREATE TABLE IF NOT EXISTS business.permissions (
    id SERIAL PRIMARY KEY,
    role_id INTEGER,
    permission_name VARCHAR(100)
);


-- SERVICES
CREATE TABLE IF NOT EXISTS business.services (
    id SERIAL PRIMARY KEY,
    company_id INTEGER,
    name VARCHAR(255),
    description TEXT,
    price NUMERIC(12,2)
);


-- PRODUITS
CREATE TABLE IF NOT EXISTS business.products (
    id SERIAL PRIMARY KEY,
    company_id INTEGER,
    name VARCHAR(255),
    description TEXT,
    price NUMERIC(12,2),
    stock INTEGER DEFAULT 0
);


-- PUBLICITÉS
CREATE TABLE IF NOT EXISTS business.advertisements (
    id SERIAL PRIMARY KEY,
    company_id INTEGER,
    title VARCHAR(255),
    budget NUMERIC(12,2),
    target JSONB,
    status VARCHAR(50)
);


-- OFFRES D'EMPLOI
CREATE TABLE IF NOT EXISTS business.job_offers (
    id SERIAL PRIMARY KEY,
    company_id INTEGER,
    title VARCHAR(255),
    description TEXT,
    status VARCHAR(50) DEFAULT 'active'
);


-- ÉVÉNEMENTS ENTREPRISE
CREATE TABLE IF NOT EXISTS business.events (
    id SERIAL PRIMARY KEY,
    company_id INTEGER,
    title VARCHAR(255),
    event_date TIMESTAMP,
    description TEXT
);


-- CERTIFICATION ENTREPRISE
CREATE TABLE IF NOT EXISTS business.certifications (
    id SERIAL PRIMARY KEY,
    company_id INTEGER,
    document TEXT,
    status VARCHAR(50),
    validated_at TIMESTAMP
);


-- AUDIT ENTREPRISE
CREATE TABLE IF NOT EXISTS business.audit_logs (
    id SERIAL PRIMARY KEY,
    company_id INTEGER,
    action VARCHAR(255),
    performed_by INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


-- DONNÉES INITIALES
INSERT INTO business.company_types(name)
VALUES
('Entreprise'),
('Banque'),
('Assurance'),
('Commerce'),
('Technologie'),
('Santé'),
('Transport'),
('Média')
ON CONFLICT DO NOTHING;


INSERT INTO business.sectors(name)
VALUES
('Finance'),
('Assurance'),
('Commerce'),
('Technologie'),
('Santé'),
('Transport'),
('Tourisme'),
('Industrie')
ON CONFLICT DO NOTHING;


-- INDEX
CREATE INDEX IF NOT EXISTS idx_company_owner
ON business.companies(owner_id);

CREATE INDEX IF NOT EXISTS idx_company_sector
ON business.companies(sector_id);

CREATE INDEX IF NOT EXISTS idx_products_company
ON business.products(company_id);

CREATE INDEX IF NOT EXISTS idx_services_company
ON business.services(company_id);

CREATE INDEX IF NOT EXISTS idx_jobs_company
ON business.job_offers(company_id);


COMMIT;