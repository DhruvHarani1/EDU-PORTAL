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

class Subject(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    course_name = db.Column(db.String(100), nullable=False) # e.g., B.Tech
    semester = db.Column(db.Integer, nullable=False)
    faculty_id = db.Column(db.Integer, db.ForeignKey('faculty_profile.id'), nullable=False)
    weekly_lectures = db.Column(db.Integer, default=3)
    
    # Relationship
    faculty = db.relationship('FacultyProfile', backref=db.backref('subjects_taught', lazy=True))

    def __repr__(self):
        return f'<Subject {self.name}>'

class Timetable(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    course_name = db.Column(db.String(100), nullable=False)
    semester = db.Column(db.Integer, nullable=False)
    day_of_week = db.Column(db.String(10), nullable=False) # Mon, Tue, ...
    period_number = db.Column(db.Integer, nullable=False) # 1, 2, ...
    subject_id = db.Column(db.Integer, db.ForeignKey('subject.id'), nullable=False)
    faculty_id = db.Column(db.Integer, db.ForeignKey('faculty_profile.id'), nullable=False)
    
    # Relationship
    subject = db.relationship('Subject', backref=db.backref('timetable_slots', lazy=True))
    faculty = db.relationship('FacultyProfile', backref=db.backref('timetable_slots', lazy=True))

    def __repr__(self):
        return f'<Timetable {self.course_name} {self.day_of_week} P{self.period_number}>'
