
import sys
import os
import random
from datetime import datetime, date, timedelta, time

sys.path.append(os.getcwd())

from app import create_app, db
from app.models import (
    User, StudentProfile, FacultyProfile, Subject, 
    Attendance, Notice, FeeRecord, StudentQuery, 
    QueryMessage, ExamEvent, ExamPaper, StudentResult, Timetable, ScheduleSettings
)

app = create_app()

FIRST_NAMES = ["James", "Mary", "Robert", "Patricia", "John", "Jennifer", "Michael", "Linda", "William"]
LAST_NAMES = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller"]
DEPTS = ["Computer Science", "Mechanical Engineering", "Electronics", "Management"]
COURSES = ["B.Tech", "BCA", "MCA"]
CATEGORIES = ["University", "Placement", "Department"]

def get_random_name():
    return f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}"

def seed_data():
    with app.app_context():
        print("--- Resetting Database for Standard Data ---")
        db.drop_all()
        db.create_all()

        # 1. Admins
        print("Seeding 2 Admins...")
        for i in [f"admin@edu.com", "admin2@edu.com"]:
            u = User(email=i, role='admin')
            u.set_password('123')
            db.session.add(u)
        
        # 2. Faculty
        print("Seeding 10 Faculty...")
        faculty_objs = []
        for i in range(1, 11):
            u = User(email=f"faculty{i}@edu.com", role='faculty')
            u.set_password('123')
            db.session.add(u)
            db.session.flush()

            f = FacultyProfile(
                user_id=u.id, display_name=get_random_name(),
                department=random.choice(DEPTS),
                designation="Asst. Professor", experience=random.randint(2, 15),
                specialization="Core Engineering"
            )
            db.session.add(f)
            faculty_objs.append(f)
        
        # 3. Subjects
        print("Seeding 20 Subjects...")
        subject_objs = []
        subj_names = ["Math", "Physics", "DSA", "DBMS", "OS", "AI", "Cloud", "Networking"]
        for i in range(20):
            course = random.choice(COURSES)
            sem = random.randint(1, 4)
            s = Subject(
                name=f"{random.choice(subj_names)} {random.randint(1,2)}",
                course_name=course, semester=sem,
                academic_year="2024-2025", faculty_id=random.choice(faculty_objs).id,
                weekly_lectures=4, credits=3
            )
            db.session.add(s)
            subject_objs.append(s)
        db.session.flush()

        # 4. Students
        print("Seeding 50 Students...")
        student_objs = []
        for i in range(1, 51):
            u = User(email=f"student{i}@edu.com", role='student')
            u.set_password('123')
            db.session.add(u)
            db.session.flush()

            s = StudentProfile(
                user_id=u.id, display_name=get_random_name(),
                enrollment_number=f"EN{2024000+i:07d}",
                course_name=random.choice(COURSES),
                semester=random.randint(1, 4),
                date_of_birth=date(2003, 1, 1),
                mentor_id=random.choice(faculty_objs).id
            )
            db.session.add(s)
            student_objs.append(s)
        db.session.flush()

        # 5. Attendance & Results
        print("Seeding Trends...")
        for s in student_objs:
            relevant_subs = [sb for sb in subject_objs if sb.course_name == s.course_name and sb.semester == s.semester]
            for sub in relevant_subs[:3]:
                # Attendance
                for d in range(5):
                    att = Attendance(
                        student_id=s.id, course_name=s.course_name,
                        date=date.today() - timedelta(days=d+1),
                        status="Present", subject_id=sub.id, faculty_id=sub.faculty_id
                    )
                    db.session.add(att)

        # 6. Timetable (B.Tech Sem 1)
        print("Seeding Sample Timetable...")
        settings = ScheduleSettings(
            course_name="B.Tech", semester=1,
            start_time=time(9,0), end_time=time(17,0),
            slots_per_day=8, days_per_week=5,
            recess_duration=60, recess_after_slot=4
        )
        db.session.add(settings)
        db.session.flush()

        bt_subs = [sb for sb in subject_objs if sb.course_name == "B.Tech" and sb.semester == 1]
        if bt_subs:
            for d in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']:
                for p in range(1, 5):
                    sub = random.choice(bt_subs)
                    slot = Timetable(
                        course_name="B.Tech", semester=1,
                        day_of_week=d, period_number=p,
                        subject_id=sub.id, faculty_id=sub.faculty_id
                    )
                    db.session.add(slot)

        db.session.commit()
        print("--- Standard Data Seeded! ---")

if __name__ == "__main__":
    seed_data()
