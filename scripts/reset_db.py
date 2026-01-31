import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app, db
from app.models import User, StudentProfile, FacultyProfile, Notice, Subject, Timetable, ScheduleSettings, ExamEvent, ExamPaper, StudentResult
from sqlalchemy import text

app = create_app('development')

with app.app_context():
    try:
        print("Dropping all tables...")
        db.drop_all()
        print("Creating all tables...")
        db.create_all()
        
        print("Seeding users...")
        # Admin
        admin = User(email='admin@edu.com', role='admin')
        admin.set_password('password')
        db.session.add(admin)
        
        faculty = User(email='faculty@edu.com', role='faculty')
        faculty.set_password('password')
        db.session.add(faculty)
        db.session.flush()

        # Helper to get default image data
        import os
        default_img_path = os.path.join(app.root_path, 'static', 'img', 'default_user.png')
        if not os.path.exists(default_img_path):
             # Create a dummy file if not exists for seeding purpose or just pass None
             # For now let's assume we skip or use None
             photo_data = None
             mimetype = None
        else:
             with open(default_img_path, 'rb') as f:
                 photo_data = f.read()
             mimetype = 'image/png'

        faculty_profile = FacultyProfile(
             user_id=faculty.id,
             display_name='Dr. Alice Smith',
             designation='Professor',
             department='Computer Science',
             experience=10,
             specialization='Artificial Intelligence',
             assigned_subject='Introduction to AI',
             photo_data=photo_data,
             photo_mimetype=mimetype
        )
        db.session.add(faculty_profile)
        
        # Additional Faculty 1
        faculty2 = User(email='faculty2@edu.com', role='faculty')
        faculty2.set_password('password')
        db.session.add(faculty2)
        
        # Additional Faculty 2
        faculty3 = User(email='faculty3@edu.com', role='faculty')
        faculty3.set_password('password')
        db.session.add(faculty3)
        
        db.session.flush()

        faculty_profile2 = FacultyProfile(
             user_id=faculty2.id,
             display_name='Prof. Bob Johnson',
             designation='Associate Professor',
             department='Mechanical Engineering',
             experience=15,
             specialization='Thermodynamics',
             assigned_subject='Thermodynamics I',
             photo_data=photo_data,
             photo_mimetype=mimetype
        )
        db.session.add(faculty_profile2)

        faculty_profile3 = FacultyProfile(
             user_id=faculty3.id,
             display_name='Dr. Clara Oswald',
             designation='Assistant Professor',
             department='Computer Science',
             experience=5,
             specialization='Machine Learning',
             assigned_subject='Deep Learning',
             photo_data=photo_data,
             photo_mimetype=mimetype
        )
        db.session.add(faculty_profile3)
        
        # Student 1
        student = User(email='student@edu.com', role='student')
        student.set_password('password')
        db.session.add(student)
        
        # Student 2
        student2 = User(email='student2@edu.com', role='student')
        student2.set_password('password')
        db.session.add(student2)

        # Student 3
        student3 = User(email='student3@edu.com', role='student')
        student3.set_password('password')
        db.session.add(student3)

        db.session.flush()
        
        # Seed Profile for Student 1
        student_profile = StudentProfile(
            user_id=student.id,
            display_name='John Doe',
            enrollment_number='STU001',
            course_name='B.Tech',
            semester=1
        )
        db.session.add(student_profile)

        # Seed Profile for Student 2
        student_profile2 = StudentProfile(
            user_id=student2.id,
            display_name='Jane Smith',
            enrollment_number='STU002',
            course_name='B.Tech',
            semester=2
        )
        db.session.add(student_profile2)

        # Seed Profile for Student 3
        student_profile3 = StudentProfile(
            user_id=student3.id,
            display_name='Mike Ross',
            enrollment_number='MBA001',
            course_name='MBA',
            semester=1
        )
        db.session.add(student_profile3)

        # Seed Profile for Faculty
        # Start by finding the faculty user created earlier
        # But wait, I can just create profile right after user
        # Seed Notices
        db.session.flush() # Ensure faculty_profile.id is available

        n1 = Notice(title='Welcome to New Term', content='Classes start next week.', category='university')
        n2 = Notice(title='Fire Drill', content='Evacuate immediately.', category='emergency')
        n3 = Notice(title='B.Tech Schedule', content='Exam schedule released.', category='course', target_course='B.Tech')
        
        
        db.session.add_all([n1, n2, n3])
        db.session.flush()

        # Seed Subjects for B.Tech Sem 1
        s1 = Subject(name='Mathematics-I', course_name='B.Tech', semester=1, faculty_id=faculty_profile.id, weekly_lectures=4)
        s2 = Subject(name='Physics', course_name='B.Tech', semester=1, faculty_id=faculty_profile.id, weekly_lectures=3)
        s3 = Subject(name='Intro to Programming', course_name='B.Tech', semester=1, faculty_id=faculty_profile.id, weekly_lectures=4)
        
        db.session.add_all([s1, s2, s3])

        # Seed Subjects for B.Tech Sem 2
        s4 = Subject(name='Data Structures', course_name='B.Tech', semester=2, faculty_id=faculty_profile.id, weekly_lectures=4)
        s5 = Subject(name='Digital Electronics', course_name='B.Tech', semester=2, faculty_id=faculty_profile2.id, weekly_lectures=3)
        s6 = Subject(name='Discrete Math', course_name='B.Tech', semester=2, faculty_id=faculty_profile3.id, weekly_lectures=3)
        
        # Seed Subjects for MBA Sem 1
        s7 = Subject(name='Management Principles', course_name='MBA', semester=1, faculty_id=faculty_profile2.id, weekly_lectures=3)
        s8 = Subject(name='Business Stats', course_name='MBA', semester=1, faculty_id=faculty_profile.id, weekly_lectures=3)

        db.session.add_all([s4, s5, s6, s7, s8])

        db.session.commit()
        print("Database reset and seeded successfully!")
        print("Credentials: admin@edu.com / password")
    except Exception as e:
        db.session.rollback()
        print(f"Error: {e}")
