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
    # Fields for assignment (Nullable for initial creation)
    course_name = db.Column(db.String(100), nullable=True) 
    semester = db.Column(db.Integer, nullable=True)
    academic_year = db.Column(db.String(20), nullable=True) # e.g. "2025-2026"
    faculty_id = db.Column(db.Integer, db.ForeignKey('faculty_profile.id'), nullable=True)
    weekly_lectures = db.Column(db.Integer, default=3)
    credits = db.Column(db.Integer, default=3) # Added Credits
    resource_link = db.Column(db.String(500), nullable=True) # Google Drive Link
    
    # Relationship
    faculty = db.relationship('FacultyProfile', backref=db.backref('subjects_taught', lazy=True))

    def __repr__(self):
        return f'<Subject {self.name}>'

class Syllabus(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subject_id = db.Column(db.Integer, db.ForeignKey('subject.id'), nullable=False)
    filename = db.Column(db.String(255), nullable=False)
    file_data = db.Column(db.LargeBinary, nullable=False) # Storing PDF as BLOB
    upload_date = db.Column(db.DateTime, default=datetime.utcnow)
    
    subject = db.relationship('Subject', backref=db.backref('syllabus', uselist=False, cascade="all, delete-orphan"))

    def __repr__(self):
        return f'<Syllabus {self.filename} for Subject {self.subject_id}>'

class Timetable(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    course_name = db.Column(db.String(100), nullable=False)
    semester = db.Column(db.Integer, nullable=False)
    day_of_week = db.Column(db.String(10), nullable=False) # Mon, Tue, ...
    period_number = db.Column(db.Integer, nullable=False) # 1, 2, ...
    subject_id = db.Column(db.Integer, db.ForeignKey('subject.id'), nullable=False)
    faculty_id = db.Column(db.Integer, db.ForeignKey('faculty_profile.id'), nullable=False)
    room_number = db.Column(db.String(20), default='Room 101') # Added Room
    
    # Relationship
    subject = db.relationship('Subject', backref=db.backref('timetable_slots', lazy=True))
    faculty = db.relationship('FacultyProfile', backref=db.backref('timetable_slots', lazy=True))

    def __repr__(self):
        return f'<Timetable {self.course_name} {self.day_of_week} P{self.period_number}>'

class ScheduleSettings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    course_name = db.Column(db.String(100), nullable=False)
    semester = db.Column(db.Integer, nullable=False)
    start_time = db.Column(db.Time, nullable=False) # e.g. 09:00
    end_time = db.Column(db.Time, nullable=False)   # e.g. 17:00
    slots_per_day = db.Column(db.Integer, default=8)
    days_per_week = db.Column(db.Integer, default=5)
    
    # Composite unique constraint could be useful but we'll handle in logic

class ExamEvent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False) # e.g. "End Semester Exam 2024"
    academic_year = db.Column(db.String(20), nullable=False) # "2023-2024"
    course_name = db.Column(db.String(100), nullable=False)
    semester = db.Column(db.Integer, nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    is_published = db.Column(db.Boolean, default=False)
    
    # Relationships
    papers = db.relationship('ExamPaper', backref='exam_event', lazy=True, cascade="all, delete-orphan")

    def __repr__(self):
        return f'<ExamEvent {self.name}>'

class ExamPaper(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    exam_event_id = db.Column(db.Integer, db.ForeignKey('exam_event.id'), nullable=False)
    subject_id = db.Column(db.Integer, db.ForeignKey('subject.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)
    total_marks = db.Column(db.Integer, default=100)
    
    # Relationships
    subject = db.relationship('Subject', backref='exam_papers')

    def __repr__(self):
        return f'<ExamPaper {self.subject.name} on {self.date}>'

class StudentResult(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    exam_paper_id = db.Column(db.Integer, db.ForeignKey('exam_paper.id'), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('student_profile.id'), nullable=False)
    marks_obtained = db.Column(db.Float, nullable=True) # Check for None if Absent
    status = db.Column(db.String(20), default='Present') # Present, Absent, Explelled
    is_fail = db.Column(db.Boolean, default=False)
    
    # Relationships
    paper = db.relationship('ExamPaper', backref=db.backref('results', lazy=True))
    student = db.relationship('StudentProfile', backref=db.backref('exam_results', lazy=True))

    def __repr__(self):
        return f'<Result {self.student.enrollment_number} - {self.marks_obtained}>'
