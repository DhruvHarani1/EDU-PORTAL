from app.extensions import db

class StudentProfile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), unique=True, nullable=False)
    enrollment_number = db.Column(db.String(20), unique=True, nullable=False)
    course_name = db.Column(db.String(100), nullable=False) # e.g., B.Tech, MBA
    semester = db.Column(db.Integer, default=1)
    
    # Relationship with User
    user = db.relationship('User', backref=db.backref('student_profile', uselist=False))

    def __repr__(self):
        return f'<StudentProfile {self.enrollment_number}>'
