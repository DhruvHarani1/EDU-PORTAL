
import sys
import os
import random
import click
from datetime import datetime, date, timedelta, time
from flask.cli import FlaskGroup

sys.path.append(os.getcwd())

from app import create_app, db
from app.models import (
    User, StudentProfile, FacultyProfile, Subject, 
    Attendance, Notice, FeeRecord, StudentQuery, 
    QueryMessage, ExamEvent, ExamPaper, StudentResult, Timetable, ScheduleSettings
)

def create_manage_app(*args, **kwargs):
    return create_app()

@click.group(cls=FlaskGroup, create_app=create_manage_app)
def cli():
    """Management script for EduPortal"""
    pass

@cli.command("seed")
def seed():
    """Seed the database with optimized standard data."""
    with create_app().app_context():
        print("--- Resetting Database for Universal Standard Data ---")
        db.drop_all()
        db.create_all()

        # 1. Admins
        print("Seeding Admins...")
        for i in [f"admin@edu.com", "admin2@edu.com"]:
            u = User(email=i, role='admin')
            u.set_password('123')
            db.session.add(u)
        
        # 2. Faculty
        print("Seeding Faculty...")
        faculty_objs = []
        for i in range(1, 11):
            u = User(email=f"faculty{i}@edu.com", role='faculty')
            u.set_password('123')
            db.session.add(u)
            db.session.flush()

            f = FacultyProfile(
                user_id=u.id, 
                display_name=f"Prof. {random.choice(['James', 'Mary', 'Robert', 'Patricia'])} {random.choice(['Smith', 'Johnson', 'Williams'])}",
                department=random.choice(["CS", "Electronics", "Math"]),
                designation="Asst. Professor"
            )
            db.session.add(f)
            faculty_objs.append(f)
        db.session.flush()

        # 3. Universal Structure (All courses/sems)
        courses = ["B.Tech", "BCA", "MCA"]
        for course in courses:
            for sem in range(1, 4):
                # Schedule
                settings = ScheduleSettings(
                    course_name=course, semester=sem,
                    start_time=time(9,0), end_time=time(17,0),
                    recess_duration=60, recess_after_slot=4
                )
                db.session.add(settings)
                
                # Subjects
                subs = []
                names = ["Programming", "Logic", "Networks", "Databases"]
                for n in names:
                    s = Subject(name=f"{n} {course}-{sem}", course_name=course, semester=sem, faculty_id=random.choice(faculty_objs).id)
                    db.session.add(s)
                    subs.append(s)
                db.session.flush()
                
                # Timetable (4-Recess-3 pattern)
                for day in ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']:
                    for p in range(1, 8):
                        slot = Timetable(course_name=course, semester=sem, day_of_week=day, period_number=p, subject_id=random.choice(subs).id, faculty_id=random.choice(faculty_objs).id)
                        db.session.add(slot)

        # 4. Students
        print("Seeding 40 Students...")
        for i in range(1, 41):
            u = User(email=f"student{i}@edu.com", role='student')
            u.set_password('123')
            db.session.add(u)
            db.session.flush()
            
            idx = (i-1) % 9
            c = courses[idx // 3]
            s = (idx % 3) + 1
            
            sp = StudentProfile(user_id=u.id, display_name=f"Student {i}", enrollment_number=f"EN{2024000+i:07d}", course_name=c, semester=s)
            db.session.add(sp)

        db.session.commit()
        print("--- Standard Seeding Complete ---")

if __name__ == "__main__":
    cli()
