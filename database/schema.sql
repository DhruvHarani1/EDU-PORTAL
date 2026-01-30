-- Users Table Schema
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(120) UNIQUE NOT NULL,
    password_hash VARCHAR(256),
    role VARCHAR(20) NOT NULL
);

-- Indexes
CREATE INDEX ix_users_email ON users (email);

-- Student Profile Schema
CREATE TABLE student_profile (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL UNIQUE,
    display_name VARCHAR(100) NOT NULL,
    enrollment_number VARCHAR(20) NOT NULL UNIQUE,
    course_name VARCHAR(100) NOT NULL,
    semester INTEGER DEFAULT 1,
    FOREIGN KEY (user_id) REFERENCES users (id)
);

-- Faculty Profile Schema
CREATE TABLE faculty_profile (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL UNIQUE,
    designation VARCHAR(100) NOT NULL,
    department VARCHAR(100) NOT NULL,
    display_name VARCHAR(100) NOT NULL,
    experience INTEGER,
    specialization VARCHAR(200),
    assigned_subject VARCHAR(100),
    photo_data BYTEA,
    photo_mimetype VARCHAR(50),
    FOREIGN KEY (user_id) REFERENCES users (id)
);

-- Notice Schema
CREATE TABLE notice (
    id SERIAL PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    content TEXT NOT NULL,
    category VARCHAR(50) DEFAULT 'general',
    target_course VARCHAR(100),
    target_faculty_id INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (target_faculty_id) REFERENCES faculty_profile (id)
);

-- Exam Schema
CREATE TABLE exam (
    id SERIAL PRIMARY KEY,
    course_name VARCHAR(100) NOT NULL,
    date DATE NOT NULL,
    time TIME WITHOUT TIME ZONE NOT NULL,
    duration_minutes INTEGER NOT NULL,
    location VARCHAR(100) NOT NULL
);

-- Attendance Schema
CREATE TABLE attendance (
    id SERIAL PRIMARY KEY,
    student_id INTEGER NOT NULL,
    course_name VARCHAR(100) NOT NULL,
    date DATE NOT NULL,
    status VARCHAR(20) NOT NULL,
    FOREIGN KEY (student_id) REFERENCES student_profile (id)
);
