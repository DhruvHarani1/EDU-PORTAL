from app.extensions import db

class StudentProfile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), unique=True, nullable=False)
    display_name = db.Column(db.String(100), nullable=False)
    enrollment_number = db.Column(db.String(20), unique=True, nullable=False)
    course_name = db.Column(db.String(100), nullable=False) # e.g., B.Tech, MBA
    semester = db.Column(db.Integer, default=1)
    
    # Extended Profile Fields
    date_of_birth = db.Column(db.Date, nullable=True)
    batch_year = db.Column(db.String(20), nullable=True) # e.g. "2023-2027"
    phone_number = db.Column(db.String(15), nullable=True)
    address = db.Column(db.Text, nullable=True)
    guardian_name = db.Column(db.String(100), nullable=True)
    guardian_contact = db.Column(db.String(15), nullable=True)
    
    # Mentor Relationship
    mentor_id = db.Column(db.Integer, db.ForeignKey('faculty_profile.id'), nullable=True)
    mentor = db.relationship('FacultyProfile', backref=db.backref('mentees', lazy=True))

    # Relationship with User
    user = db.relationship('User', backref=db.backref('student_profile', uselist=False))

    def __repr__(self):
        return f'<StudentProfile {self.enrollment_number}>'

class FacultyProfile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), unique=True, nullable=False)
    display_name = db.Column(db.String(100), nullable=False)
    designation = db.Column(db.String(100), nullable=False) # e.g., Professor, Assistant Professor
    department = db.Column(db.String(100), nullable=False) # e.g., Computer Science
    experience = db.Column(db.Integer) # Years of experience
    specialization = db.Column(db.String(200)) # e.g., AI, ML
    assigned_subject = db.Column(db.String(100)) # e.g., Data Structures
    photo_data = db.Column(db.LargeBinary) # Binary data for photo
    photo_mimetype = db.Column(db.String(50)) # Mimetype e.g. 'image/jpeg'
    
    # Relationship with User
    user = db.relationship('User', backref=db.backref('faculty_profile', uselist=False))

    def __repr__(self):
        return f'<FacultyProfile {self.user.email}>'
