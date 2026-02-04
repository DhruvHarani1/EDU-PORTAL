-- Initial Seed Data
-- Note: Passwords must be hashed in the actual application. These are placeholders.

INSERT INTO users (email, password_hash, role) VALUES
('admin@edu.com', '<hashed_password>', 'admin'),
('faculty@edu.com', '<hashed_password>', 'faculty'),
('student@edu.com', '<hashed_password>', 'student');
