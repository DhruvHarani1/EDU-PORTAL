import sys
import os
import random
from datetime import date, timedelta, datetime
from sqlalchemy import text

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app, db
from app.models import User, StudentProfile, FacultyProfile, Notice, Subject, Timetable, Attendance, ExamEvent, ExamPaper, StudentResult, UniversityEvent, EventRegistration, FeeRecord, StudentQuery, QueryMessage, Syllabus

app = create_app('development')

def get_random_names(count):
    first_names = ["James", "Mary", "John", "Patricia", "Robert", "Jennifer", "Michael", "Linda", "William", "Elizabeth", "David", "Barbara", "Richard", "Susan", "Joseph", "Jessica", "Thomas", "Sarah", "Charles", "Karen"]
    last_names = ["Smith", "Johnson", "Williams", "Jones", "Brown", "Davis", "Miller", "Wilson", "Moore", "Taylor", "Anderson", "Thomas", "Jackson", "White", "Harris", "Martin", "Thompson", "Garcia", "Martinez", "Robinson"]
    names = []
    for _ in range(count):
        names.append(f"{random.choice(first_names)} {random.choice(last_names)}")
    return names

with app.app_context():
    try:
        print("Dropping all tables...")
        # Force drop legacy/removed tables
        try:
            db.session.execute(text("DROP TABLE IF EXISTS study_material CASCADE"))
            db.session.commit()
        except:
            pass
            
        db.drop_all()
        print("Creating all tables...")
        db.create_all()
        
        # --- 1. Admin ---
        print("1. Creating Admin...")
        admin = User(email='admin@edu.com', role='admin')
        admin.set_password('password')
        db.session.add(admin)

        # --- 2. Faculty (5 Members) ---
        print("2. Creating Faculty...")
        faculty_users = []
        faculty_profiles = []
        dept_list = ['Computer Science', 'Electronics', 'Mathematics', 'Humanities', 'Mechanical']
        
        # Default Faculty for Login
        f_def = User(email='faculty@edu.com', role='faculty')
        f_def.set_password('password')
        db.session.add(f_def)
        db.session.flush()
        
        fp_def = FacultyProfile(user_id=f_def.id, display_name='Prof. Default', designation='Professor', department='Computer Science')
        db.session.add(fp_def)
        faculty_profiles.append(fp_def)

        for i in range(1, 5):
            u = User(email=f'faculty{i}@edu.com', role='faculty')
            u.set_password('password')
            db.session.add(u)
            faculty_users.append(u)
        db.session.flush()

        for i, user in enumerate(faculty_users):
            fp = FacultyProfile(
                user_id=user.id,
                display_name=f'Prof. {get_random_names(1)[0]}',
                designation=random.choice(['Assistant Professor', 'Associate Professor', 'Professor']),
                department=dept_list[i]
            )
            db.session.add(fp)
            faculty_profiles.append(fp)
        db.session.flush()

        # --- 3. Subjects ---
        print("3. Creating Subjects...")
        subjects = []
        subject_names = [
            # CSE
            ('Data Structures', 'CS'), ('Algorithms', 'CS'), ('OS', 'CS'), ('DBMS', 'CS'), ('Networks', 'CS'),
            # ECE
            ('Digital Electronics', 'EC'), ('Signals', 'EC'), ('Microprocessors', 'EC'),
            # Math
            ('Calculus', 'Math'), ('Linear Algebra', 'Math'), ('Statistics', 'Math'),
            # Other
            ('English', 'Hum'), ('Economics', 'Hum'), ('Thermodynamics', 'Mech')
        ]
        
        for name, dept in subject_names:
            # Assign random faculty from same dept roughly, but here random is fine
            fac = random.choice(faculty_profiles)
            sub = Subject(
                name=name,
                course_name='B.Tech',
                semester=random.choice([1, 2, 3, 4, 5, 6]),
                faculty_id=fac.id,
                weekly_lectures=random.randint(2, 5),
                credits=random.randint(2, 4),
                resource_link='https://google.com'
            )
            db.session.add(sub)
            subjects.append(sub)
        db.session.flush()

        # --- 4. Students (50 Students) ---
        print("4. Creating 50 Students...")
        students = []
        
        # Default Student
        s_def = User(email='student@edu.com', role='student')
        s_def.set_password('password')
        db.session.add(s_def)
        db.session.flush()
        
        sp_def = StudentProfile(
            user_id=s_def.id,
            display_name='John Doe',
            enrollment_number='STU001',
            course_name='B.Tech',
            semester=3, # Matches some subjects
            batch_year='2025-2029',
            phone_number='9999999999',
            address='123 Main St',
            guardian_name='Mr. Doe',
            guardian_contact='8888888888'
        )
        db.session.add(sp_def)
        students.append(sp_def)

        for i in range(2, 51):
            u = User(email=f'student{i}@edu.com', role='student')
            u.set_password('password')
            db.session.add(u)
            db.session.flush()
            
            enroll = f"STU{i:03d}"
            sp = StudentProfile(
                user_id=u.id,
                display_name=get_random_names(1)[0],
                enrollment_number=enroll,
                course_name='B.Tech',
                semester=random.choice([1, 2, 3, 4, 5, 6, 7, 8]),
                batch_year=random.choice(['2024-2028', '2025-2029', '2023-2027', '2022-2026']),
                phone_number=str(random.randint(7000000000, 9999999999)),
                guardian_name=f'Guardian of {enroll}',
                guardian_contact=str(random.randint(7000000000, 9999999999))
            )
            db.session.add(sp)
            students.append(sp)
        db.session.flush()

        # --- 5. Timetable ---
        print("5. Creating Timetables...")
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
        for fac in faculty_profiles:
            # Each faculty teaches 2-4 slots per day
            fac_subs = Subject.query.filter_by(faculty_id=fac.id).all()
            if not fac_subs: continue
            
            for day in days:
                slots = random.sample(range(1, 8), random.randint(2, 5)) # Slots 1-8
                for slot_num in slots:
                    sub = random.choice(fac_subs)
                    tt = Timetable(
                        course_name=sub.course_name,
                        semester=sub.semester,
                        day_of_week=day,
                        period_number=slot_num,
                        subject_id=sub.id,
                        faculty_id=fac.id,
                        room_number=f"Room {random.randint(101, 305)}"
                    )
                    db.session.add(tt)
        db.session.flush()

        # --- 6. Attendance (Last 30 Days) ---
        print("6. Creating Attendance Records...")
        start_date = date.today() - timedelta(days=30)
        attendance_opts = ['Present', 'Present', 'Present', 'Absent'] # 75% bias
        
        for i in range(30):
            curr = start_date + timedelta(days=i)
            if curr.weekday() > 4: continue # Skip weekend
            
            # For each student, mark attendance for 2 random subjects he is likely enrolled in
            # For simplicity, we assume all students take all subjects (or random subset)
            for stu in students:
                # Pick 2 random subjects
                daily_subs = random.sample(subjects, 2)
                
                for sub in daily_subs:
                    status = random.choice(attendance_opts)
                    att = Attendance(
                        student_id=stu.id,
                        course_name=sub.course_name,
                        date=curr,
                        status=status,
                        subject_id=sub.id,
                        faculty_id=sub.faculty_id
                    )
                    db.session.add(att)
        db.session.flush()

        # --- 7. Fee Records ---
        print("7. Creating Fee Records...")
        for stu in students:
            # Sem 1 Paid
            f1 = FeeRecord(
                student_id=stu.id, semester=1, academic_year='2024-2025',
                amount_due=50000, amount_paid=50000, status='Paid', due_date=date(2024, 8, 1)
            )
            # Sem 2 Mixed
            status = random.choice(['Paid', 'Pending', 'Partial'])
            paid = 50000 if status == 'Paid' else (25000 if status == 'Partial' else 0)
            f2 = FeeRecord(
                student_id=stu.id, semester=2, academic_year='2025-2026',
                amount_due=50000, amount_paid=paid, status=status, due_date=date(2025, 1, 15)
            )
            db.session.add_all([f1, f2])
        db.session.flush()

        # --- 8. Notices ---
        print("8. Creating Notices...")
        notice_titles = [
            ('Exam Schedule Released', 'exam'),
            ('Holiday Announcement', 'general'),
            ('Tech Fest Registration', 'event'),
            ('Library Due Date', 'admin'),
            ('Guest Lecture on AI', 'academic')
        ]
        for t, cat in notice_titles:
            n = Notice(title=t, content=f"This is a detail content for {t}.", category=cat)
            db.session.add(n)
        db.session.flush()

        # --- 9. Exams ---
        print("9. Creating Exams...")
        # Event
        mid_sem = ExamEvent(
            name="Mid Semester Exam 2026",
            academic_year="2025-2026",
            course_name="B.Tech",
            semester=3, # Mixed, but flagging mainly
            start_date=date.today() - timedelta(days=5),
            end_date=date.today() + timedelta(days=10),
            is_published=True
        )
        db.session.add(mid_sem)
        db.session.flush()

        # Papers for all subjects
        for sub in subjects:
            # Random date within exam range
            p_date = mid_sem.start_date + timedelta(days=random.randint(0, 15))
            paper = ExamPaper(
                exam_event_id=mid_sem.id,
                subject_id=sub.id,
                date=p_date,
                start_time=datetime.strptime("10:00", "%H:%M").time(),
                end_time=datetime.strptime("13:00", "%H:%M").time(),
                total_marks=50
            )
            db.session.add(paper)
        db.session.flush()

        # --- 10. Student Queries ---
        print("10. Creating Student Queries...")
        query_titles = [
            "Doubt in Lecture 3",
            "Assignment submission issue",
            "Request for extra class",
            "Clarification on syllabus",
            "Project partner request"
        ]
        
        for i in range(10): # Create 10 queries
            stu = random.choice(students)
            sub = random.choice(subjects) # Assume link exists or loose coupling
            fac_id = sub.faculty_id
            
            q = StudentQuery(
                student_id=stu.id,
                faculty_id=fac_id,
                subject_id=sub.id,
                title=random.choice(query_titles),
                status=random.choice(['Pending', 'Answered', 'Resolved'])
            )
            db.session.add(q)
            db.session.flush()
            
            # Initial Message
            m1 = QueryMessage(
                query_id=q.id,
                sender_type='student',
                content=f"Hello Professor, I have a question regarding {sub.name}."
            )
            db.session.add(m1)
            
            if q.status != 'Pending':
                m2 = QueryMessage(
                    query_id=q.id,
                    sender_type='faculty',
                    content="Sure, please visit my cabin or ask here."
                )
                db.session.add(m2)
                
        db.session.flush()

        db.session.commit()
        print("--- SEEDING COMPLETE ---")
        print("Admin: admin@edu.com")
        print("Faculty: faculty@edu.com (and faculty1..4)")
        print("Student: student@edu.com (and student2..50)")
        
    except Exception as e:
        print(f"Error seeding: {e}")
        import traceback
        traceback.print_exc()
        db.session.rollback()
