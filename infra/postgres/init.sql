-- Each service owns its own database. No service is granted access to
-- another's — cross-service data access happens over HTTP, never SQL.
CREATE DATABASE auth_db;
CREATE DATABASE interview_db;
CREATE DATABASE conversation_db;
CREATE DATABASE report_db;
