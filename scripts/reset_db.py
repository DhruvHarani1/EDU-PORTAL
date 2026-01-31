import sys
import os
import random
from datetime import date, timedelta, datetime
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app, db
from app.models import User, StudentProfile, FacultyProfile, Notice, Subject, Timetable, Attendance, ExamEvent, ExamPaper, StudentResult, UniversityEvent

app = create_app('development')

with app.app_context():
    try:
        print("Dropping all tables...")
        db.drop_all()
        print("Creating all tables...")
        db.create_all()
        
        print("1. Creating Users...")
        # Admin
        admin = User(email='admin@edu.com', role='admin')
        admin.set_password('password')
        
        # Faculty
        fac1 = User(email='faculty@edu.com', role='faculty')
        fac1.set_password('password')
        
        # Student
        stu1 = User(email='student@edu.com', role='student')
        stu1.set_password('password')
        
        db.session.add_all([admin, fac1, stu1])
        db.session.flush()

        print("2. Creating Profiles...")
        # Faculty Profile
        fp1 = FacultyProfile(user_id=fac1.id, display_name='Dr. Smith', designation='Professor', department='CS')
        db.session.add(fp1)
        db.session.flush()

        # Student Profile
        sp1 = StudentProfile(user_id=stu1.id, display_name='John Doe', enrollment_number='STU001', course_name='B.Tech', semester=1)
        db.session.add(sp1)
        db.session.flush()

        print("3. Creating Subjects (B.Tech Sem 1)...")
        # 5 Subjects with Notes Links
        s1 = Subject(name='Mathematics-I', course_name='B.Tech', semester=1, faculty_id=fp1.id, weekly_lectures=4, resource_link='https://drive.google.com/drive/folders/maths1-dummy')
        s2 = Subject(name='Physics', course_name='B.Tech', semester=1, faculty_id=fp1.id, weekly_lectures=3, resource_link='https://drive.google.com/drive/folders/phy-dummy')
        s3 = Subject(name='Programming in C', course_name='B.Tech', semester=1, faculty_id=fp1.id, weekly_lectures=4, resource_link='https://drive.google.com/drive/folders/cprog-dummy')
        s4 = Subject(name='Engineering Graphics', course_name='B.Tech', semester=1, faculty_id=fp1.id, weekly_lectures=2, resource_link='https://drive.google.com/drive/folders/graphics-dummy')
        s5 = Subject(name='Communication Skills', course_name='B.Tech', semester=1, faculty_id=fp1.id, weekly_lectures=2, resource_link='https://drive.google.com/drive/folders/comm-dummy')
        
        db.session.add_all([s1, s2, s3, s4, s5])
        db.session.flush()

        print("4. Creating Timetable...")
        # Mon: Math, Phy
        # Tue: Prog, Graph
        # Wed: Math, Comm
        # Thu: Phy, Prog
        # Fri: Math, Prog
        days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri']
        tt_entries = [
            (s1, 'Mon', 1), (s2, 'Mon', 2),
            (s3, 'Tue', 1), (s4, 'Tue', 2),
            (s1, 'Wed', 1), (s5, 'Wed', 2),
            (s2, 'Thu', 1), (s3, 'Thu', 2),
            (s1, 'Fri', 1), (s3, 'Fri', 2)
        ]
        
        for sub, day, period in tt_entries:
            t = Timetable(
                course_name='B.Tech', semester=1, day_of_week=day, period_number=period,
                subject_id=sub.id, faculty_id=fp1.id
            )
            db.session.add(t)
        db.session.flush()

        print("5. Simulating Attendance (Last 60 Days)...")
        start_date = date.today() - timedelta(days=60)
        
        for i in range(60):
            current_date = start_date + timedelta(days=i)
            day_idx = current_date.weekday() # 0=Mon, 6=Sun
            
            if day_idx > 4: continue # Skip Weekends
            
            # Attendance Logic to create variety
            # Math (Mon, Wed, Fri) -> High Attendance
            # Physics (Mon, Thu) -> Medium
            # Programming (Tue, Thu, Fri) -> LOW Attendance (Critical)
            
            status = 'Present'
            
            # Randomization with Bias
            chance = random.random()
            
            # If Mon/Wed/Fri (Math days mainly), he attends 90%
            if day_idx in [0, 2, 4]:
                if chance > 0.9: status = 'Absent'
            
            # If Thu (Physics/Prog), he skips often (60% attendance)
            elif day_idx == 3:
                if chance > 0.6: status = 'Absent'
                
            # If Tue (Prog/Graphics), he skips very often (40% attendance)
            elif day_idx == 1:
                if chance > 0.4: status = 'Absent'

            att = Attendance(
                student_id=sp1.id,
                course_name='B.Tech',
                date=current_date,
                status=status
            )
            db.session.add(att)

        # Add Notices
        n1 = Notice(title='Welcome', content='Welcome to the new semester', category='university')
        db.session.add(n1)
        db.session.flush()

        # --- University Events ---
        print("5.5 Creating Events...")
        
        # Helper to read image bytes
        DEFAULT_ARTIFACT_PATH = r"C:\Users\TEST\.gemini\antigravity\brain\ea4b25ed-125c-45de-b3a1-50f6629eceb7"
        
        def get_image_data(filename):
            try:
                path = os.path.join(DEFAULT_ARTIFACT_PATH, filename)
                with open(path, 'rb') as f:
                    return f.read()
            except Exception as e:
                print(f"Warning: Could not read image {filename}: {e}")
                return None

        ev1 = UniversityEvent(
            title='TechNova 2026',
            description='Annual Technical Symposium featuring Hackathons, Robotics workshops, and AI seminars.',
            date=start_date + timedelta(days=10),
            time=datetime.strptime('09:00', '%H:%M').time(),
            location='Main Auditorium',
            category='Tech',
            image_data=get_image_data('event_tech_symposium_1769855435285.png'),
            image_mimetype='image/png'
        )
        ev2 = UniversityEvent(
            title='Inter-College Cricket Tournament',
            description='The biggest sports showdown of the year.',
            date=start_date + timedelta(days=15),
            time=datetime.strptime('14:00', '%H:%M').time(),
            location='University Stadium',
            category='Sports',
            image_data=get_image_data('event_sports_tournament_1769855453905.png'),
            image_mimetype='image/png'
        )
        ev3 = UniversityEvent(
            title='Cultural Night: Rhythm 2026',
            description='A night of music, dance, and drama.',
            date=start_date + timedelta(days=25),
            time=datetime.strptime('18:00', '%H:%M').time(),
            location='Open Air Theatre',
            category='Cultural',
            image_data=get_image_data('event_cultural_night_1769855474733.png'),
            image_mimetype='image/png'
        )
        db.session.add_all([ev1, ev2, ev3])
        db.session.flush()

        # --- Semester 1 Exams ---
        print("6. Simulating Sem 1 Exams...")
        exam_event = ExamEvent(
            name='Winter Semester End Exams 2025',
            academic_year='2025-2026',
            course_name='B.Tech',
            semester=1,
            start_date=start_date + timedelta(days=50),
            end_date=start_date + timedelta(days=60),
            is_published=True
        )
        db.session.add(exam_event)
        db.session.flush()

        papers = []
        # Reuse S1-S5
        for i, sub in enumerate([s1, s2, s3, s4, s5]):
            paper = ExamPaper(
                exam_event_id=exam_event.id,
                subject_id=sub.id,
                date=exam_event.start_date + timedelta(days=i*2),
                start_time=datetime.strptime('10:00', '%H:%M').time(),
                end_time=datetime.strptime('13:00', '%H:%M').time(),
                total_marks=100
            )
            db.session.add(paper)
            papers.append(paper)
        db.session.flush()

        # Sem 1 Results
        marks_data = [92, 78, 88, 85, 90]
        for i, paper in enumerate(papers):
            res = StudentResult(
                exam_paper_id=paper.id,
                student_id=sp1.id,
                marks_obtained=marks_data[i],
                status='Present',
                is_fail=False
            )
            db.session.add(res)

        # --- Semester 2 Exams ---
        print("7. Simulating Sem 2 Exams...")
        
        # Create Sem 2 Subjects
        s6 = Subject(name='Data Structures', course_name='B.Tech', semester=2, faculty_id=fp1.id, weekly_lectures=4)
        s7 = Subject(name='Digital Electronics', course_name='B.Tech', semester=2, faculty_id=fp1.id, weekly_lectures=3)
        s8 = Subject(name='Discrete Math', course_name='B.Tech', semester=2, faculty_id=fp1.id, weekly_lectures=3)
        db.session.add_all([s6, s7, s8])
        db.session.flush()

        exam_event_2 = ExamEvent(
            name='Summer Semester End Exams 2026',
            academic_year='2025-2026',
            course_name='B.Tech',
            semester=2,
            start_date=start_date + timedelta(days=200),
            end_date=start_date + timedelta(days=210),
            is_published=True
        )
        db.session.add(exam_event_2)
        db.session.flush()

        papers_2 = []
        for i, sub in enumerate([s6, s7, s8]):
            paper = ExamPaper(
                exam_event_id=exam_event_2.id,
                subject_id=sub.id,
                date=exam_event_2.start_date + timedelta(days=i*2),
                start_time=datetime.strptime('10:00', '%H:%M').time(),
                end_time=datetime.strptime('13:00', '%H:%M').time(),
                total_marks=100
            )
            db.session.add(paper)
            papers_2.append(paper)
        db.session.flush()

        # Sem 2 Results
        marks_data_2 = [85, 88, 95] 
        for i, paper in enumerate(papers_2):
            res = StudentResult(
                exam_paper_id=paper.id,
                student_id=sp1.id,
                marks_obtained=marks_data_2[i],
                status='Present',
                is_fail=False
            )
            db.session.add(res)

        db.session.commit()
        print("Seed Complete!")
        print("Student Credentials: student@edu.com / password")

    except Exception as e:
        db.session.rollback()
        print(f"Error: {e}")
