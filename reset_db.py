from app import create_app, db
from app.models import User
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
        
        # Faculty
        faculty = User(email='faculty@edu.com', role='faculty')
        faculty.set_password('password')
        db.session.add(faculty)
        
        # Student
        student = User(email='student@edu.com', role='student')
        student.set_password('password')
        db.session.add(student)
        db.session.flush()

        from app.models import StudentProfile, FacultyProfile
        
        # Seed Profile for Student
        student_profile = StudentProfile(
            user_id=student.id,
            display_name='John Doe',
            enrollment_number='STU001',
            course_name='B.Tech',
            semester=1
        )
        db.session.add(student_profile)

        # Seed Profile for Faculty
        # Start by finding the faculty user created earlier
        # But wait, I can just create profile right after user
        
        db.session.commit()
        print("Database reset and seeded successfully!")
        print("Credentials: admin@edu.com / password")
    except Exception as e:
        db.session.rollback()
        print(f"Error: {e}")
