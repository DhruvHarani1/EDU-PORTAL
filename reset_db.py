
import sys
import os

sys.path.append(os.getcwd())

from app import create_app, db
from app.models import User, FacultyProfile, StudentProfile

app = create_app()

def reset_database():
    with app.app_context():
        print("--- Resetting Database ---")
        db.drop_all()
        db.create_all()
        
        # Seed Admin
        admin_email = "admin@edu.com"
        if not User.query.filter_by(email=admin_email).first():
            u = User(email=admin_email, role='admin')
            u.set_password('123')
            db.session.add(u)
            db.session.commit()
            print(f"[✓] Created Admin: {admin_email} / 123")

if __name__ == "__main__":
    reset_database()
