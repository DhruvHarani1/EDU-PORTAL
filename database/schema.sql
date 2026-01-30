-- Users Table Schema
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(120) UNIQUE NOT NULL,
    password_hash VARCHAR(128),
    role VARCHAR(20) NOT NULL
);

-- Indexes
CREATE INDEX ix_users_email ON users (email);
