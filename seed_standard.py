
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
        print("--- Resetting Database for Universal Standard Data ---")
        db.drop_all()
        db.create_all()

        # 1. Admins
        print("Seeding Admins...")
        for i in [f"admin@edu.com", "admin2@edu.com"]:
            u = User(email=i, role='admin')
            u.set_password('123')
            db.session.add(u)
        
        # 2. Faculty
        print("Seeding Faculty...")
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
        db.session.flush()

        # 3. Subjects & Schedule Settings (Ensure for ALL Course/Sem combinations)
        print("Seeding Subjects & Timetable Settings...")
        subject_map = {} # (course, sem) -> [Subject]
        
        for course in COURSES:
            for sem in range(1, 5): # 1 to 4 semesters for each course
                # a. Schedule Settings
                settings = ScheduleSettings(
                    course_name=course, semester=sem,
                    start_time=time(9,0), end_time=time(17,0),
                    slots_per_day=8, days_per_week=5,
                    recess_duration=60, recess_after_slot=4
                )
                db.session.add(settings)
                
                # b. Subjects
                subj_list = []
                names = ["Programming", "Mathematics", "Science", "Professional Arts", "Database", "Networking"]
                random.shuffle(names)
                for i in range(4): # 4 subjects per combination
                    s = Subject(
                        name=f"{names[i]} {course}-{sem}",
                        course_name=course, semester=sem,
                        academic_year="2024-2025", faculty_id=random.choice(faculty_objs).id,
                        weekly_lectures=4, credits=3
                    )
                    db.session.add(s)
                    subj_list.append(s)
                subject_map[(course, sem)] = subj_list
                db.session.flush()
                
                # c. Timetable slots
                for d in ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']: # Added Sat for visual parity
                    for p in range(1, 8): # 7 periods per day - ensures recess (after 4) is in the middle
                        sub = random.choice(subj_list)
                        slot = Timetable(
                            course_name=course, semester=sem,
                            day_of_week=d, period_number=p,
                            subject_id=sub.id, faculty_id=sub.faculty_id
                        )
                        db.session.add(slot)
        
        db.session.flush()

        # 4. Students (Ensure distributed across courses)
        print("Seeding Students...")
        student_objs = []
        for i in range(1, 41): # 40 students
            u = User(email=f"student{i}@edu.com", role='student')
            u.set_password('123')
            db.session.add(u)
            db.session.flush()

            # Cycle thru course/sem combinations
            idx = (i-1) % 12
            course = COURSES[idx // 4]
            sem = (idx % 4) + 1
            
            s = StudentProfile(
                user_id=u.id, display_name=get_random_name(),
                enrollment_number=f"EN{2024000+i:07d}",
                course_name=course,
                semester=sem,
                date_of_birth=date(2003, 1, 1),
                mentor_id=random.choice(faculty_objs).id
            )
            db.session.add(s)
            student_objs.append(s)
        db.session.flush()

        # 5. Attendance & Results (For all students)
        print("Seeding Attendance & Trends...")
        for s in student_objs:
            relevant_subs = subject_map.get((s.course_name, s.semester), [])
            for sub in relevant_subs:
                # Attendance (Last 10 days)
                for d in range(10):
                    att = Attendance(
                        student_id=s.id, course_name=s.course_name,
                        date=date.today() - timedelta(days=d+1),
                        status="Present" if random.random() > 0.1 else "Absent",
                        subject_id=sub.id, faculty_id=sub.faculty_id
                    )
                    db.session.add(att)
                
                # Results
                res = StudentResult(
                    exam_paper_id=None, # Not using ExamPaper/Event for simple test
                    student_id=s.id,
                    marks_obtained=random.randint(60, 95),
                    status="Present"
                )
                # Note: StudentResult usually needs an exam_paper_id, but some reports might handle Null
                # For safety, let's seed one Exam Event per course
        
        # 6. Exam Logic (Simple)
        print("Seeding Exams...")
        for course in COURSES:
            ee = ExamEvent(
                name=f"Standard Exam - {course}", academic_year="2024-2025",
                course_name=course, semester=1,
                start_date=date.today() - timedelta(days=30),
                end_date=date.today() - timedelta(days=25),
                is_published=True
            )
            db.session.add(ee)
            db.session.flush()
            
            # Add one paper and results for Sem 1 students
            sub = subject_map[(course, 1)][0]
            ep = ExamPaper(
                exam_event_id=ee.id, subject_id=sub.id,
                date=ee.start_date + timedelta(days=1),
                start_time=time(10,0), end_time=time(13,0)
            )
            db.session.add(ep)
            db.session.flush()
            
            relevant_students = [st for st in student_objs if st.course_name == course and st.semester == 1]
            for st in relevant_students:
                res = StudentResult(
                    exam_paper_id=ep.id, student_id=st.id,
                    marks_obtained=random.gauss(75, 8), status="Present"
                )
                db.session.add(res)

        db.session.commit()
        print("--- Universal Standard Data Seeded! ---")

if __name__ == "__main__":
    seed_data()
