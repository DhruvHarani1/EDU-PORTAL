from app import create_app, db
from app.models import User

app = create_app('development')

with app.app_context():
    # Helper to create user if not exists
    def create_user_if_not_exists(email, password, role):
        if not User.query.filter_by(email=email).first():
            user = User(email=email, role=role)
            user.set_password(password)
            db.session.add(user)
            print(f"Created {role} user: {email}")
        else:
            print(f"User {email} already exists")

    create_user_if_not_exists('admin@edu.com', 'password', 'admin')
    create_user_if_not_exists('faculty@edu.com', 'password', 'faculty')
    create_user_if_not_exists('student@edu.com', 'password', 'student')

    db.session.commit()
    print("Database seeded!")
