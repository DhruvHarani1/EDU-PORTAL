from datetime import datetime
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
