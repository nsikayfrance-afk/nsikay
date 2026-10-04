BEGIN;

CREATE SCHEMA IF NOT EXISTS association;

CREATE TABLE IF NOT EXISTS association.membership_types (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL UNIQUE,
    description TEXT,
    active BOOLEAN DEFAULT TRUE
);

CREATE TABLE IF NOT EXISTS association.members (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    membership_type_id INTEGER NOT NULL,
    status VARCHAR(30) DEFAULT 'pending',
    joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_membership_type
    FOREIGN KEY (membership_type_id)
    REFERENCES association.membership_types(id)
);

CREATE TABLE IF NOT EXISTS association.subscriptions (
    id SERIAL PRIMARY KEY,
    member_id INTEGER NOT NULL,
    amount NUMERIC(12,2) NOT NULL,
    currency VARCHAR(10) DEFAULT 'EUR',
    payment_status VARCHAR(30) DEFAULT 'pending',
    paid_at TIMESTAMP,

    CONSTRAINT fk_subscription_member
    FOREIGN KEY (member_id)
    REFERENCES association.members(id)
);

CREATE TABLE IF NOT EXISTS association.donations (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    amount NUMERIC(12,2) NOT NULL,
    currency VARCHAR(10) DEFAULT 'EUR',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS association.member_cards (
    id SERIAL PRIMARY KEY,
    member_id INTEGER NOT NULL,
    card_number VARCHAR(100) UNIQUE,
    qr_code TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_member_card
    FOREIGN KEY (member_id)
    REFERENCES association.members(id)
);

CREATE TABLE IF NOT EXISTS association.benefits (
    id SERIAL PRIMARY KEY,
    membership_type_id INTEGER NOT NULL,
    title VARCHAR(255),
    description TEXT,

    CONSTRAINT fk_benefit_type
    FOREIGN KEY (membership_type_id)
    REFERENCES association.membership_types(id)
);

INSERT INTO association.membership_types(name, description)
VALUES
('Membre actif','Participation à la vie associative'),
('Membre donateur','Soutien financier à l’association')
ON CONFLICT DO NOTHING;

COMMIT;
