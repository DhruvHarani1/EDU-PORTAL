from app import create_app, db
from app.models import StudentProfile, Attendance
from datetime import date, timedelta
import random

app = create_app()

def fix_attendance():
    with app.app_context():
        print("--- FIXING ATTENDANCE DATA ---")
        
        students = StudentProfile.query.all()
        print(f"Found {len(students)} students.")
        
        updated_count = 0
        
        for s in students:
            # Check existing count
            count = Attendance.query.filter_by(student_id=s.id).count()
            
            if count < 10: # No data or very little
                print(f"Generating data for {s.display_name} (ID: {s.id})...")
                
                # Generate 60 days back
                start_date = date.today() - timedelta(days=90)
                
                buffer = []
                for i in range(60):
                    day = start_date + timedelta(days=i)
                    if day.weekday() >= 5: continue # Skip weekend
                    
                    # Random status (80% present avg)
                    status = 'Present' if random.random() > 0.2 else 'Absent'
                    
                    att = Attendance(
                        student_id=s.id,
                        course_name=s.course_name or "B.Tech",
                        date=day,
                        status=status
                    )
                    buffer.append(att)
                
                db.session.add_all(buffer)
                updated_count += 1
                
        db.session.commit()
        print(f"--- COMPLETE ---")
        print(f"Generated attendance for {updated_count} students.")

if __name__ == "__main__":
    fix_attendance()
