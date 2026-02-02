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
    date_of_birth DATE,
    batch_year VARCHAR(20),
    phone_number VARCHAR(15),
    address TEXT,
    guardian_name VARCHAR(100),
    guardian_contact VARCHAR(15),
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
    subject_id INTEGER,
    faculty_id INTEGER,
    FOREIGN KEY (student_id) REFERENCES student_profile (id),
    FOREIGN KEY (subject_id) REFERENCES subject (id),
    FOREIGN KEY (faculty_id) REFERENCES faculty_profile (id)
);

-- Subjects Schema
CREATE TABLE subject (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    course_name VARCHAR(100),
    semester INTEGER,
    academic_year VARCHAR(20),
    faculty_id INTEGER,
    weekly_lectures INTEGER DEFAULT 3,
    credits INTEGER DEFAULT 3,
    resource_link VARCHAR(500),
    FOREIGN KEY (faculty_id) REFERENCES faculty_profile (id)
);

-- Syllabus Schema
CREATE TABLE syllabus (
    id SERIAL PRIMARY KEY,
    subject_id INTEGER NOT NULL,
    filename VARCHAR(255) NOT NULL,
    file_data BYTEA NOT NULL,
    upload_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (subject_id) REFERENCES subject (id)
);

-- Timetable Schema
CREATE TABLE timetable (
    id SERIAL PRIMARY KEY,
    course_name VARCHAR(100) NOT NULL,
    semester INTEGER NOT NULL,
    day_of_week VARCHAR(10) NOT NULL,
    period_number INTEGER NOT NULL,
    subject_id INTEGER NOT NULL,
    faculty_id INTEGER NOT NULL, 
    room_number VARCHAR(20) DEFAULT 'Room 101',
    FOREIGN KEY (subject_id) REFERENCES subject (id),
    FOREIGN KEY (faculty_id) REFERENCES faculty_profile (id)
);

-- Schedule Settings Schema
CREATE TABLE schedule_settings (
    id SERIAL PRIMARY KEY,
    course_name VARCHAR(100) NOT NULL,
    semester INTEGER NOT NULL,
    start_time TIME NOT NULL,
    end_time TIME NOT NULL,
    slots_per_day INTEGER DEFAULT 8,
    days_per_week INTEGER DEFAULT 5
);

-- Exam Event Schema
CREATE TABLE exam_event (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    academic_year VARCHAR(20) NOT NULL,
    course_name VARCHAR(100) NOT NULL,
    semester INTEGER NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    is_published BOOLEAN DEFAULT FALSE
);

-- Exam Paper Schema
CREATE TABLE exam_paper (
    id SERIAL PRIMARY KEY,
    exam_event_id INTEGER NOT NULL,
    subject_id INTEGER NOT NULL,
    date DATE NOT NULL,
    start_time TIME NOT NULL,
    end_time TIME NOT NULL,
    total_marks INTEGER DEFAULT 100,
    FOREIGN KEY (exam_event_id) REFERENCES exam_event (id),
    FOREIGN KEY (subject_id) REFERENCES subject (id)
);

-- Student Result Schema
CREATE TABLE student_result (
    id SERIAL PRIMARY KEY,
    exam_paper_id INTEGER NOT NULL,
    student_id INTEGER NOT NULL,
    marks_obtained FLOAT,
    status VARCHAR(20) DEFAULT 'Present',
    is_fail BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (exam_paper_id) REFERENCES exam_paper (id),
    FOREIGN KEY (student_id) REFERENCES student_profile (id)
);

-- University Event Schema
CREATE TABLE university_event (
    id SERIAL PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    date DATE NOT NULL,
    time TIME WITHOUT TIME ZONE,
    location VARCHAR(100),
    organizer VARCHAR(100) DEFAULT 'University Admin',
    category VARCHAR(50) DEFAULT 'General',
    image_data BYTEA,
    image_mimetype VARCHAR(50),
    is_upcoming BOOLEAN DEFAULT TRUE
);

-- Event Registration Schema
CREATE TABLE event_registration (
    id SERIAL PRIMARY KEY,
    event_id INTEGER NOT NULL,
    student_id INTEGER NOT NULL,
    registered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (event_id) REFERENCES university_event (id),
    FOREIGN KEY (student_id) REFERENCES student_profile (id),
    UNIQUE(event_id, student_id)
);

-- Fee Record Schema
CREATE TABLE fee_record (
    id SERIAL PRIMARY KEY,
    student_id INTEGER NOT NULL,
    semester INTEGER NOT NULL,
    academic_year VARCHAR(20) NOT NULL,
    amount_due FLOAT NOT NULL,
    amount_paid FLOAT DEFAULT 0.0,
    due_date DATE NOT NULL,
    status VARCHAR(20) DEFAULT 'Pending',
    payment_date TIMESTAMP,
    payment_mode VARCHAR(50),
    transaction_reference VARCHAR(100),
    FOREIGN KEY (student_id) REFERENCES student_profile (id)
);

-- Student Query (Support) Schema
CREATE TABLE student_query (
    id SERIAL PRIMARY KEY,
    student_id INTEGER NOT NULL,
    faculty_id INTEGER NOT NULL,
    subject_id INTEGER,
    title VARCHAR(200) NOT NULL,
    status VARCHAR(20) DEFAULT 'Pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES student_profile (id),
    FOREIGN KEY (faculty_id) REFERENCES faculty_profile (id),
    FOREIGN KEY (subject_id) REFERENCES subject (id)
);

CREATE TABLE query_message (
    id SERIAL PRIMARY KEY,
    query_id INTEGER NOT NULL,
    sender_type VARCHAR(20) NOT NULL,
    content TEXT,
    image_data BYTEA,
    image_mimetype VARCHAR(50),
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (query_id) REFERENCES student_query (id)
);
