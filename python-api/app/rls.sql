-- Enable row level security on applicable tables and create policies.
-- Assumes: a GUC app.current_tenant is set via SET LOCAL for each request.

ALTER TABLE IF EXISTS tenants ENABLE ROW LEVEL SECURITY;
ALTER TABLE IF EXISTS users ENABLE ROW LEVEL SECURITY;
ALTER TABLE IF EXISTS accounts ENABLE ROW LEVEL SECURITY;
ALTER TABLE IF EXISTS contacts ENABLE ROW LEVEL SECURITY;
ALTER TABLE IF EXISTS deals ENABLE ROW LEVEL SECURITY;
ALTER TABLE IF EXISTS notes ENABLE ROW LEVEL SECURITY;
ALTER TABLE IF EXISTS tasks ENABLE ROW LEVEL SECURITY;
ALTER TABLE IF EXISTS attachments ENABLE ROW LEVEL SECURITY;
ALTER TABLE IF EXISTS custom_field_definitions ENABLE ROW LEVEL SECURITY;
ALTER TABLE IF EXISTS custom_field_values ENABLE ROW LEVEL SECURITY;
ALTER TABLE IF EXISTS audit_logs ENABLE ROW LEVEL SECURITY;
ALTER TABLE IF EXISTS subscriptions ENABLE ROW LEVEL SECURITY;

-- Create simple tenant_id based policy
DO $$
DECLARE t text;
BEGIN
  FOREACH t IN ARRAY ARRAY['tenants','users','accounts','contacts','deals','notes','tasks'] LOOP
    EXECUTE format('DROP POLICY IF EXISTS p_%s ON %I', t, t);
    EXECUTE format('CREATE POLICY p_%s ON %I USING (tenant_id::text = current_setting(''app.current_tenant'', true))', t, t);
  END LOOP;
END $$;
