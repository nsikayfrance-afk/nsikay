BEGIN;

-- SCHEMAS NSIKAY
CREATE SCHEMA IF NOT EXISTS association;
CREATE SCHEMA IF NOT EXISTS app_center;
CREATE SCHEMA IF NOT EXISTS profile;
CREATE SCHEMA IF NOT EXISTS streaming;
CREATE SCHEMA IF NOT EXISTS jobs;
CREATE SCHEMA IF NOT EXISTS advertising;


-- PROFILS UTILISATEURS
CREATE TABLE IF NOT EXISTS profile.public_profiles (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    profile_type VARCHAR(50),
    bio TEXT,
    phone_public VARCHAR(50),
    visibility VARCHAR(30) DEFAULT 'public',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE IF NOT EXISTS profile.business_cards (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    name VARCHAR(255),
    function VARCHAR(255),
    phone VARCHAR(50),
    email VARCHAR(255),
    social_links JSONB,
    qr_code TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


-- ARTISTES ET STREAMING
CREATE TABLE IF NOT EXISTS streaming.artist_profiles (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    artist_type VARCHAR(50),
    certification_status VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE IF NOT EXISTS streaming.contents (
    id SERIAL PRIMARY KEY,
    artist_id INTEGER,
    content_type VARCHAR(50),
    title VARCHAR(255),
    url TEXT,
    views BIGINT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE IF NOT EXISTS streaming.rewards (
    id SERIAL PRIMARY KEY,
    artist_id INTEGER,
    reward_type VARCHAR(100),
    amount NUMERIC(12,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


-- EMPLOIS ET OFFRES
CREATE TABLE IF NOT EXISTS jobs.offers (
    id SERIAL PRIMARY KEY,
    owner_id INTEGER,
    title VARCHAR(255),
    description TEXT,
    offer_type VARCHAR(50),
    status VARCHAR(50) DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


-- PUBLICITE
CREATE TABLE IF NOT EXISTS advertising.campaigns (
    id SERIAL PRIMARY KEY,
    owner_id INTEGER,
    title VARCHAR(255),
    budget NUMERIC(12,2),
    target JSONB,
    status VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


-- ASSOCIATION
CREATE TABLE IF NOT EXISTS association.membership_types (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) UNIQUE
);


CREATE TABLE IF NOT EXISTS association.members (
    id SERIAL PRIMARY KEY,
    user_id INTEGER,
    membership_type_id INTEGER,
    status VARCHAR(50),
    joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE IF NOT EXISTS association.subscriptions (
    id SERIAL PRIMARY KEY,
    member_id INTEGER,
    amount NUMERIC(12,2),
    currency VARCHAR(10),
    payment_status VARCHAR(50),
    paid_at TIMESTAMP
);


CREATE TABLE IF NOT EXISTS association.donations (
    id SERIAL PRIMARY KEY,
    user_id INTEGER,
    amount NUMERIC(12,2),
    currency VARCHAR(10),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


-- APPLICATIONS
CREATE TABLE IF NOT EXISTS app_center.applications (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255),
    platform VARCHAR(50),
    active BOOLEAN DEFAULT TRUE
);


CREATE TABLE IF NOT EXISTS app_center.app_versions (
    id SERIAL PRIMARY KEY,
    application_id INTEGER,
    version VARCHAR(50),
    download_url TEXT,
    release_notes TEXT,
    mandatory BOOLEAN DEFAULT FALSE,
    released_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE IF NOT EXISTS app_center.update_history (
    id SERIAL PRIMARY KEY,
    version_id INTEGER,
    user_id INTEGER,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


-- INDEX
CREATE INDEX IF NOT EXISTS idx_profile_user
ON profile.public_profiles(user_id);

CREATE INDEX IF NOT EXISTS idx_streaming_artist
ON streaming.contents(artist_id);

CREATE INDEX IF NOT EXISTS idx_jobs_owner
ON jobs.offers(owner_id);

CREATE INDEX IF NOT EXISTS idx_ads_owner
ON advertising.campaigns(owner_id);

CREATE INDEX IF NOT EXISTS idx_members_user
ON association.members(user_id);

COMMIT;