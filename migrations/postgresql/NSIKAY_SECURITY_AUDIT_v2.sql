-- =====================================
-- NSIKAY SECURITY AUDIT v2.0
-- =====================================

BEGIN;


CREATE TABLE IF NOT EXISTS audit.change_history
(
    id SERIAL PRIMARY KEY,
    table_name TEXT NOT NULL,
    operation TEXT NOT NULL,
    changed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    changed_by TEXT
);


CREATE TABLE IF NOT EXISTS audit.security_event
(
    id SERIAL PRIMARY KEY,
    user_id BIGINT,
    event_type TEXT,
    event_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    details JSONB
);


CREATE TABLE IF NOT EXISTS audit.admin_action
(
    id SERIAL PRIMARY KEY,
    administrator TEXT,
    action TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


CREATE INDEX IF NOT EXISTS idx_security_event_user
ON audit.security_event(user_id);


CREATE INDEX IF NOT EXISTS idx_admin_action_date
ON audit.admin_action(created_at);


COMMIT;
