from app import create_app, db
from app.models import User, StudentProfile, FacultyProfile
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
        
        # Student
        student = User(email='student@edu.com', role='student')
        student.set_password('password')
        db.session.add(student)
        db.session.flush()

        db.session.flush()
        
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
