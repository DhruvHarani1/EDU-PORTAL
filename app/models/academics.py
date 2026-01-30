from datetime import date, datetime
from app.extensions import db

class Exam(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    course_name = db.Column(db.String(100), nullable=False)
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time, nullable=False)
    duration_minutes = db.Column(db.Integer, nullable=False)
    location = db.Column(db.String(100), nullable=False) # Room number or 'Online'

    def __repr__(self):
        return f'<Exam {self.course_name} on {self.date}>'

class Attendance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student_profile.id'), nullable=False)
    course_name = db.Column(db.String(100), nullable=False)
    date = db.Column(db.Date, default=date.today, nullable=False)
    status = db.Column(db.String(20), nullable=False) # 'Present', 'Absent', 'Late'

    # Relationship
    student = db.relationship('StudentProfile', backref=db.backref('attendance_records', lazy=True))

    def __repr__(self):
        return f'<Attendance {self.student.enrollment_number} - {self.date} - {self.status}>'
