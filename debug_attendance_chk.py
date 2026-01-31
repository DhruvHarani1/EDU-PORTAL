from app import create_app, db
from app.models import StudentProfile, Attendance
from sqlalchemy import func

app = create_app()

def check_data():
    with app.app_context():
        print("--- DIAGNOSTIC: ATTENDANCE DATA ---")
        
        # 1. Check Counts
        s_count = StudentProfile.query.count()
        a_count = Attendance.query.count()
        print(f"Total Students: {s_count}")
        print(f"Total Attendance Records: {a_count}")
        
        if a_count == 0:
            print("CRITICAL: Attendance table is empty!")
            return

        # 2. Check Linkage
        # Get a few student IDs
        students = StudentProfile.query.limit(5).all()
        print(f"\nSample Students:")
        for s in students:
            print(f" - ID: {s.id} | Name: {s.display_name}")
            # Check records for this student
            rec_count = Attendance.query.filter_by(student_id=s.id).count()
            print(f"   -> Found {rec_count} attendance records.")
            
        # 3. Check Orphan Records
        # Are there attendance records pointing to non-existent students?
        distinct_ids = db.session.query(Attendance.student_id).distinct().limit(5).all()
        print(f"\nSample Distinct Student IDs in Attendance Table:")
        for (sid,) in distinct_ids:
            print(f" - Attendance.student_id: {sid}")

if __name__ == "__main__":
    check_data()
