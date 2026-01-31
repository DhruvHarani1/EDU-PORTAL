# EduPortal - Functional Specification & User Guide

## 1. Project Vision
**EduPortal** is a Next-Generation University Management System (UMS) designed to bridge the gap between simple record-keeping and intelligent decision-making. Unlike legacy ERPs, EduPortal leverages **AI-driven Analytics** to provide actionable insights into student performance and faculty effectiveness.

---

## 2. User Personas & Capabilities

### 👑 The Administrator (Superuser)
*   **Role**: Total System Control.
*   **Key Capabilities**:
    *   **User Management**: Onboard students and hire faculty.
    *   **Academic Configuration**: Create Courses (B.Tech, MBA), Subjects, and Semesters.
    *   **Exam Controller**: Schedule "Exam Events", publish results, and declare holidays.
    *   **Intelligence Viewer**: Access the "Future Sight" prediction engine to see batch performance trends.

### 🎓 The Faculty (Teacher)
*   **Role**: Academic Delivery & Assessment.
*   **Key Capabilities**:
    *   **Attendance Marking**: Log daily class attendance (Present/Absent).
    *   **Result Entry**: Input marks for their specific subjects after exams.
    *   **Notice Board**: Post course-specific announcements (e.g., "Assignment Due").
    *   **Timetable View**: View their personal weekly schedule.

### 🎒 The Student (End User)
*   **Role**: Consumer of information.
*   **Key Capabilities**:
    *   **Performance View**: See their own grades and GPA trends.
    *   **Attendance Tracker**: View their innovative "Warning Bar" if attendance drops <75%.
    *   **Notice Board**: Read university and course announcements.
    *   **Profile**: Manage personal details.

---

## 3. Module Breakdown (In-Depth)

### A. The Academic Engine
This module manages the core university structure.
*   **Functionality**:
    *   **Dynamic Timetable**: Automatically detects conflicts. If Prof. Smith is busy on Monday 9AM, the system won't let you book him for another class.
    *   **Attendance Registry**: Real-time aggregation. It calculates percentages instantly, coloring students as **Green (Safe)**, **Yellow (Warning)**, or **Red (Critical)**.

### B. The Examination System
A hierarchical system designed for flexibility.
1.  **Event Creation**: Admin creates "Winter Semester Finals 2024".
2.  **Paper Scheduling**: Admin schedules "Maths I" on Dec 10th, "Physics" on Dec 12th.
3.  **Result Entry**: Faculty enters marks for their respective papers.
4.  **Result Publishing**: Admin clicks "Publish", and students can instantly see their Spider Charts.

### C. The Intelligence Suite (Unique Feature)
This is the USP (Unique Selling Point) of EduPortal.
1.  **Career Prediction**: Using Monte Carlo simulations, the system predicts the "Future Salary" of a student based on their consistency and grades.
2.  **Radar Analysis**: A 5-point spider chart that evaluates a student not just on grades, but on "Consistency" and "Attendance".
3.  **Equity Index**: A metric for Faculty. It calculates how "Inclusive" a teacher is. (Low Standard Deviation in class marks = High Equity).

---

## 4. End-to-End User Journeys

### Journey 1: The "Exam Season" Flow
1.  **Admin** creates `ExamEvent`: "Mid-Terms".
2.  **Admin** adds `ExamPaper`s for all subjects.
3.  **Students** view the Date Sheet on their dashboard.
4.  Exams happen offline.
5.  **Faculty** logs in and sees "Pending Marks Entry". They input scores.
6.  **Admin** reviews the "Batch Average". If it's too low, they may request moderation.
7.  **Admin** publishes results.
8.  **System** automatically updates the "Placement Prediction" for the batch based on new grades.

### Journey 2: The "At-Risk" Intervention
1.  **System** scans Attendance daily.
2.  Student "John Doe" drops to 58% attendance.
3.  **Admin Dashboard** shows John in the "Critical List" (Quick Actions).
4.  **Admin** clicks John's profile -> "Send Warning Notice".
5.  **John** receives a notification on his dashboard.
