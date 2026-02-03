
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

FIRST_NAMES = ["James", "Mary", "Robert", "Patricia", "John", "Jennifer", "Michael", "Linda", "William", "Elizabeth", "David", "Barbara", "Richard", "Susan", "Joseph", "Jessica", "Thomas", "Sarah", "Charles", "Karen", "Christopher", "Nancy", "Daniel", "Lisa", "Matthew", "Betty", "Anthony", "Margaret", "Mark", "Sandra"]
LAST_NAMES = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis", "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez", "Wilson", "Anderson", "Thomas", "Taylor", "Moore", "Jackson", "Martin", "Lee", "Perez", "Thompson", "White", "Harris", "Sanchez", "Clark", "Ramirez", "Lewis", "Robinson"]
DEPTS = ["Computer Science", "Mechanical Engineering", "Electronics", "Civil Engineering", "Information Technology", "Basic Sciences", "Management"]
COURSES = ["B.Tech", "M.Tech", "BCA", "MCA", "B.Sc", "M.Sc"]
CATEGORIES = ["University", "Placement", "Department", "Cultural", "Sports"]

def get_random_name():
    return f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}"

def seed_data():
    with app.app_context():
        print("--- Wiping Database ---")
        db.drop_all()
        db.create_all()

        # 1. Admins (10)
        print("Seeding 10 Admins...")
        for i in range(1, 11):
            email = f"admin{i}@edu.com"
            u = User(email=email, role='admin')
            u.set_password('123')
            db.session.add(u)
        
        # Default admin
        u_def = User(email="admin@edu.com", role='admin')
        u_def.set_password('123')
        db.session.add(u_def)

        # 2. Faculty (60)
        print("Seeding 60 Faculty...")
        faculty_objs = []
        for i in range(1, 61):
            email = f"faculty{i}@edu.com"
            u = User(email=email, role='faculty')
            u.set_password('123')
            db.session.add(u)
            db.session.flush()

            name = get_random_name()
            f = FacultyProfile(
                user_id=u.id,
                display_name=name,
                department=random.choice(DEPTS),
                designation=random.choice(["Professor", "Asst. Professor", "Lecturer"]),
                experience=random.randint(2, 25),
                specialization=f"Expert in {random.choice(DEPTS)}."
            )
            db.session.add(f)
            faculty_objs.append(f)
        
        db.session.flush()

        # 3. Subjects (100)
        print("Seeding 100 Subjects...")
        subject_objs = []
        subj_names = ["Mathematics", "Physics", "Data Structures", "Algorithms", "Networking", "Database Systems", "Operating Systems", "Software Engineering", "AI", "Cloud Computing", "Microprocessors", "Digital Circuits", "Thermodynamics", "Fluid Mechanics", "Structural Analysis", "Geotechnical Engineering", "Economics", "Soft Skills", "Cyber Security", "Machine Learning"]
        
        for i in range(100):
            course = random.choice(COURSES)
            sem = random.randint(1, 8)
            name = f"{random.choice(subj_names)} {random.randint(1,4)}"
            fac = random.choice(faculty_objs)
            
            s = Subject(
                name=name,
                course_name=course,
                semester=sem,
                academic_year="2024-2025",
                faculty_id=fac.id,
                weekly_lectures=random.randint(3, 5),
                credits=random.randint(2, 4)
            )
            db.session.add(s)
            subject_objs.append(s)
        
        db.session.flush()

        # 4. Students (1000)
        print("Seeding 1000 Students...")
        student_objs = []
        for i in range(1, 1001):
            email = f"student{i}@edu.com"
            u = User(email=email, role='student')
            u.set_password('123')
            db.session.add(u)
            db.session.flush()

            name = get_random_name()
            course = random.choice(COURSES)
            sem = random.randint(1, 4) if "M" in course else random.randint(1, 8)
            
            s = StudentProfile(
                user_id=u.id,
                display_name=name,
                enrollment_number=f"EN{2024000+i:07d}",
                course_name=course,
                semester=sem,
                date_of_birth=date(random.randint(2000, 2006), random.randint(1,12), random.randint(1,28)),
                phone_number=f"+91 {random.randint(7000, 9999)}{random.randint(100000, 999999)}",
                address="Student Hostel Building, Campus Road",
                mentor_id=random.choice(faculty_objs).id
            )
            db.session.add(s)
            student_objs.append(s)
        
        db.session.flush()

        # 5. Attendance (5000)
        print("Seeding 5000 Attendance Records...")
        today = date.today()
        for i in range(5000):
            stu = random.choice(student_objs)
            rel_subs = [sb for sb in subject_objs if sb.course_name == stu.course_name and sb.semester == stu.semester]
            if not rel_subs: continue
            
            sub = random.choice(rel_subs)
            att_date = today - timedelta(days=random.randint(0, 45))
            if att_date.weekday() >= 5: att_date -= timedelta(days=2)
            
            a = Attendance(
                student_id=stu.id,
                course_name=stu.course_name,
                date=att_date,
                status=random.choices(["Present", "Absent", "Late"], weights=[85, 12, 3])[0],
                subject_id=sub.id,
                faculty_id=sub.faculty_id
            )
            db.session.add(a)

        # 6. Notices (100)
        print("Seeding 100 Notices...")
        for i in range(100):
            fac = random.choice([None] + faculty_objs)
            target = random.choice(["all", "faculty", "class", "individual"])
            n = Notice(
                title=f"Announcement {i+1}",
                content="Notice content goes here.",
                category=random.choice(CATEGORIES),
                target_type=target,
                sender_faculty_id=fac.id if fac else None
            )
            db.session.add(n)

        # 7. Fee Records (500)
        print("Seeding 500 Fee Records...")
        for i in range(500):
            stu = random.choice(student_objs)
            f = FeeRecord(
                student_id=stu.id,
                semester=stu.semester,
                academic_year="2024-2025",
                amount_due=random.choice([25000, 50000]),
                due_date=today + timedelta(days=random.randint(-10, 30)),
                status=random.choice(["Paid", "Pending"])
            )
            db.session.add(f)

        # 8. Student Queries (100)
        print("Seeding 100 Queries...")
        for i in range(100):
            stu = random.choice(student_objs)
            fac = random.choice(faculty_objs)
            q = StudentQuery(student_id=stu.id, faculty_id=fac.id, title="Query", status="Pending")
            db.session.add(q)

        # 9. Exam Events (Sem 1 & 3)
        print("Seeding 10 Exam Events...")
        for course in COURSES:
            for sem in [1, 3]:
                ee = ExamEvent(
                    name=f"Final Exam {course} S{sem}",
                    academic_year="2024-2025",
                    course_name=course,
                    semester=sem,
                    start_date=date.today() - timedelta(days=120),
                    end_date=date.today() - timedelta(days=110),
                    is_published=True
                )
                db.session.add(ee)
                db.session.flush()
                
                relevant_subs = [s for s in subject_objs if s.course_name == course and s.semester == sem]
                for sub in relevant_subs[:4]:
                    ep = ExamPaper(
                        exam_event_id=ee.id,
                        subject_id=sub.id,
                        date=ee.start_date + timedelta(days=2),
                        start_time=time(10,0),
                        end_time=time(13,0)
                    )
                    db.session.add(ep)

        db.session.flush()

        # 10. Student Results (6000)
        print("Seeding 6000 Results...")
        papers = ExamPaper.query.all()
        for p in papers:
            event = p.exam_event
            rel_students = [s for s in student_objs if s.course_name == event.course_name and s.semester == event.semester]
            for s in rel_students:
                m = random.gauss(65 if event.semester==1 else 72, 10)
                m = max(0, min(100, m))
                res = StudentResult(
                    exam_paper_id=p.id,
                    student_id=s.id,
                    marks_obtained=m,
                    status="Present",
                    is_fail=(m < 35)
                )
                db.session.add(res)

        db.session.commit()
        print("--- DONE ---")

if __name__ == "__main__":
    seed_data()
