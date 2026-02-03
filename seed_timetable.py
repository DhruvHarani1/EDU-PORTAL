
import sys
import os
import random
from datetime import time, datetime

sys.path.append(os.getcwd())

from app import create_app, db
from app.models import Subject, Timetable, ScheduleSettings, FacultyProfile

app = create_app()

def seed_timetable():
    with app.app_context():
        print("--- Seeding Timetable Data ---")
        
        # 1. Target Course/Sem
        target_course = "B.Tech"
        target_sem = 1
        
        # 2. Create ScheduleSettings if not exists
        settings = ScheduleSettings.query.filter_by(course_name=target_course, semester=target_sem).first()
        if not settings:
            print(f"Creating ScheduleSettings for {target_course} Sem {target_sem}...")
            settings = ScheduleSettings(
                course_name=target_course,
                semester=target_sem,
                start_time=time(9, 0),
                end_time=time(17, 0),
                slots_per_day=8,
                days_per_week=5,
                recess_duration=60,
                recess_after_slot=4
            )
            db.session.add(settings)
            db.session.commit()
        
        # 3. Get Subjects for this course/sem
        subjects = Subject.query.filter_by(course_name=target_course, semester=target_sem).all()
        if not subjects:
            print("No subjects found for B.Tech Sem 1. Please run seed_massive_data.py first.")
            return
            
        # 4. Clear existing slots for this course/sem to avoid duplicates
        Timetable.query.filter_by(course_name=target_course, semester=target_sem).delete()
        
        # 5. Seed some random slots
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
        for day in days:
            print(f"Seeding {day}...")
            # Pick 6 random slots out of 8 (some free periods)
            active_periods = random.sample(range(1, 9), 6)
            for p in active_periods:
                sub = random.choice(subjects)
                slot = Timetable(
                    course_name=target_course,
                    semester=target_sem,
                    day_of_week=day,
                    period_number=p,
                    subject_id=sub.id,
                    faculty_id=sub.faculty_id
                )
                db.session.add(slot)
        
        db.session.commit()
        print(f"--- Timetable Seeded for {target_course} Semester {target_sem}! ---")
        print("You can now view this in the Admin Timetable section.")

if __name__ == "__main__":
    seed_timetable()
