-- =====================================
-- NSIKAY INDEXES v2.0 SAFE FINAL
-- =====================================

BEGIN;

DO $$

BEGIN

IF EXISTS (
SELECT 1 FROM information_schema.columns
WHERE table_schema='core'
AND table_name='user'
AND column_name='email'
)
THEN
CREATE INDEX IF NOT EXISTS idx_user_email
ON core.user(email);
END IF;


IF EXISTS (
SELECT 1 FROM information_schema.columns
WHERE table_schema='core'
AND table_name='user_role'
AND column_name='user_id'
)
THEN
CREATE INDEX IF NOT EXISTS idx_user_role_user
ON core.user_role(user_id);
END IF;


IF EXISTS (
SELECT 1 FROM information_schema.columns
WHERE table_schema='finance'
AND table_name='transaction'
AND column_name='created_at'
)
THEN
CREATE INDEX IF NOT EXISTS idx_transaction_date
ON finance.transaction(created_at);
END IF;


IF EXISTS (
SELECT 1 FROM information_schema.columns
WHERE table_schema='media'
AND table_name='publication'
AND column_name='created_at'
)
THEN
CREATE INDEX IF NOT EXISTS idx_media_publication_date
ON media.publication(created_at);
END IF;


IF EXISTS (
SELECT 1 FROM information_schema.columns
WHERE table_schema='audit'
AND table_name='system_log'
AND column_name='created_at'
)
THEN
CREATE INDEX IF NOT EXISTS idx_audit_log_date
ON audit.system_log(created_at);
END IF;


END $$;

COMMIT;

