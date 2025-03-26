-- Create tables for authentication
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    is_temp_password BOOLEAN DEFAULT TRUE,
    security_question TEXT,
    security_answer_hash VARCHAR(255),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP WITH TIME ZONE
);

-- Create initial admin user (password: changeme)
-- Password should be changed after first login
INSERT INTO users (username, email, password_hash, is_temp_password)
VALUES ('admin', 'admin@example.com', '$2b$12$SduS1.A9sBLMdT.T5Fhkx.VJkpU/KcZkTt1wRakSU/STtVJGHj9MK', TRUE)
ON CONFLICT (username) DO NOTHING;