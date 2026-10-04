-- =====================================
-- NSIKAY FOREIGN KEYS v2.0 SAFE
-- =====================================

BEGIN;


DO $$
BEGIN

IF EXISTS (
SELECT 1 FROM information_schema.columns
WHERE table_schema='core'
AND table_name='user_role'
AND column_name='user_id'
)
THEN
ALTER TABLE core.user_role
ADD CONSTRAINT fk_user_role_user
FOREIGN KEY (user_id)
REFERENCES core.user(id);
END IF;


IF EXISTS (
SELECT 1 FROM information_schema.columns
WHERE table_schema='core'
AND table_name='user_permission'
AND column_name='role_id'
)
THEN
ALTER TABLE core.user_permission
ADD CONSTRAINT fk_user_permission_role
FOREIGN KEY (role_id)
REFERENCES core.user_role(id);
END IF;


IF EXISTS (
SELECT 1 FROM information_schema.columns
WHERE table_schema='certification'
AND table_name='request'
AND column_name='user_id'
)
THEN
ALTER TABLE certification.request
ADD CONSTRAINT fk_certification_user
FOREIGN KEY (user_id)
REFERENCES core.user(id);
END IF;


END $$;


COMMIT;
