# Database Schema Documentation

## Overview
The database is normalized to 3NF standards where possible. We use **SQLAlchemy** as the ORM.

### 1. Authentication & Users
The system separates **Authentication Credentials** from **User Data**.

#### `User` Table (`app/models/user.py`)
*   **Purpose**: Stores login info.
*   **Fields**:
    *   `id` (PK): Integer.
    *   `email`: Unique String.
    *   `password_hash`: Scrypt hashed string.
    *   `role`: Enum ('admin', 'student', 'faculty').

#### `StudentProfile` Table (`app/models/profiles.py`)
*   **Purpose**: Academic identity.
*   **Fields**:
    *   `id` (PK): Integer.
    *   `user_id` (FK): Links to `User.id`.
    *   `enrollment_number`: Unique (e.g., "STU2024001").
    *   `course_name`: (e.g., "B.Tech").
    *   `semester`: Integration current semester.
*   **Relationships**: `user` (backref).

#### `FacultyProfile` Table
*   **Purpose**: Staff identity.
*   **Fields**: `designation`, `department`, `specialization`.

---

### 2. Academic Core

#### `Subject` Table
*   **Purpose**: Represents a specific course module (e.g., "Data Structures").
*   **Fields**:
    *   `faculty_id`: Who teaches this?
    *   `semester`, `course_name`: Which batch is it for?
    *   `weekly_lectures`: Expected load.

#### `Attendance` Table (`app/models/academics.py`)
*   **Purpose**: Daily log.
*   **Volume**: High (One row per student per day).
*   **Fields**:
    *   `student_id` (FK).
    *   `date`: Date object.
    *   `status`: 'Present', 'Absent', 'Late'.
    *   `course_name`: Denormalized for faster querying.

---

### 3. Examination System (Complex Hierarchy)

The exam system is hierarchical to support flexibility.

1.  **`ExamEvent`**: The "Season".
    *   *Example*: "Winter Semester Finals 2025"
    *   Attributes: `start_date`, `end_date`, `is_published`.

2.  **`ExamPaper`**: The specific "Test".
    *   *Example*: "Mathematics I - Paper A"
    *   Linked to `ExamEvent`.
    *   Attributes: `date`, `time`, `total_marks`.
    *   Linked to `Subject` (So we know it's a Math test).

3.  **`StudentResult`**: The "Score".
    *   *Example*: "John scored 85 in Math".
    *   Linked to `ExamPaper` AND `StudentProfile`.
    *   Attributes: `marks_obtained`, `is_fail`.

---

### 4. Communication

#### `Notice` Table
*   **Purpose**: System-wide announcements.
*   **Fields**:
    *   `category`: 'university', 'course', 'emergency'.
    *   `target_course`: Optional filter (e.g., only show to 'MBA').
    *   `target_faculty_id`: Optional filter.
    *   `content`: HTML/Text body.
