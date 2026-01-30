from datetime import datetime
from app.extensions import db

class Notice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(50), nullable=False, default='general') # university, course, exam, emergency, faculty
    target_course = db.Column(db.String(100)) # For course-wise notices
    target_faculty_id = db.Column(db.Integer, db.ForeignKey('faculty_profile.id')) # For specific faculty
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Notice {self.title}>'
