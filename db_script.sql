
-- Create Database
CREATE DATABASE resume_ai_db;

-- Connect to the database
\c auth_db;

-- Create ENUM type for user roles
CREATE TYPE user_role AS ENUM ('admin', 'user');

-- Create users table
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    username VARCHAR(100) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    role user_role DEFAULT 'user',
    is_active BOOLEAN DEFAULT FALSE,
    is_verified BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE
);

-- Create indexes for users table
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_username ON users(username);

-- Create otps table
CREATE TABLE otps (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) NOT NULL,
    otp_code VARCHAR(10) NOT NULL,
    purpose VARCHAR(50) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP WITH TIME ZONE NOT NULL,
    is_used BOOLEAN DEFAULT FALSE
);

-- Create index for otps table
CREATE INDEX idx_otps_email ON otps(email);

-- Create function to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Create trigger for users table
CREATE TRIGGER update_users_updated_at
    BEFORE UPDATE ON users
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Insert sample admin user (password: admin123)
-- Note: This is a bcrypt hash of 'admin123'
INSERT INTO users (email, username, hashed_password, role, is_active, is_verified)
VALUES (
    'admin@example.com',
    'admin',
    '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5UpgSVQXYz7EO',
    'admin',
    TRUE,
    TRUE
);

-- Verify tables created
SELECT table_name FROM information_schema.tables 
WHERE table_schema = 'public';

-- Check users table structure
\d users

-- Check otps table structure
\d otps


CREATE TABLE t_job_details (
    -- Primary Key: Auto-generated, sequential integer
    id SERIAL PRIMARY KEY,

    -- Admin-provided unique job identifier (VARCHAR(50) and unique index)
    job_id VARCHAR(50) NOT NULL UNIQUE,

    -- Human-readable job name (VARCHAR(255))
    job_name VARCHAR(255) NOT NULL,

    -- Detailed description of the job (TEXT, equivalent to SQLAlchemy's String for long content)
    job_details TEXT NOT NULL,

    -- Timestamp for when the record was created
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,

    -- Timestamp for when the record was last updated
    updated_at TIMESTAMP WITH TIME ZONE
);

-- CREATE TABLE IF NOT EXISTS t_user_details (
--     id SERIAL PRIMARY KEY,
--     first_name VARCHAR(100) NOT NULL,
--     last_name VARCHAR(100) NOT NULL,
--     phone VARCHAR(20) NOT NULL, -- using VARCHAR for phone to preserve leading zeros/formatting
--     gender VARCHAR(20) NOT NULL,
--     city VARCHAR(100) NOT NULL,
--     state_province VARCHAR(100) NOT NULL,
--     qualification VARCHAR(255) NOT NULL,
--     skills TEXT NOT NULL,       -- TEXT type for potentially long lists of skills
--     cv_file_url VARCHAR(512),   -- Stores the filename or S3/Cloud storage URL
--     created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
-- );

-- -- Optional: Create an index on phone or email if you plan to search by them frequently
-- CREATE INDEX idx_user_details_phone ON t_user_details(phone);

CREATE TABLE IF NOT EXISTS t_user_details (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    gender VARCHAR(20),
    phone VARCHAR(20),
    city VARCHAR(100),
    state_province VARCHAR(100),
    qualification VARCHAR(200),
    skills TEXT,
    
    -- File Storage Columns
    cv_filename VARCHAR(255),
    cv_content_type VARCHAR(100),
    cv_file_data BYTEA, -- This stores the Blob
    
    -- Constraints
    CONSTRAINT fk_user_details_users FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    CONSTRAINT uq_user_details_user_id UNIQUE (user_id)
);

