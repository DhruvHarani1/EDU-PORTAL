from app import create_app, db
from app.models import StudentResult, StudentProfile, ExamEvent, ExamPaper, Attendance
from sqlalchemy import func
import statistics

app = create_app()

def debug():
    with app.app_context():
        print("--- Debugging Reports Data ---")
        
        # 1. Count Basic Records
        s_count = StudentProfile.query.count()
        r_count = StudentResult.query.count()
        e_count = ExamEvent.query.count()
        p_count = ExamPaper.query.count()
        a_count = Attendance.query.count()
        
        print(f"Students: {s_count}")
        print(f"Results: {r_count}")
        print(f"Exam Events: {e_count}")
        print(f"Exam Papers: {p_count}")
        print(f"Attendance: {a_count}")
        
        if r_count == 0:
            print("CRITICAL: No results found. Seeding failed.")
            return

        # 2. Test the 'Growth Velocity' Query
        print("\n--- Testing Semester Averaging Query ---")
        sem_avgs = db.session.query(
            StudentResult.student_id, 
            ExamEvent.semester, 
            func.avg(StudentResult.marks_obtained)
        ).select_from(StudentResult).join(ExamPaper).join(ExamEvent).group_by(StudentResult.student_id, ExamEvent.semester).all()
        
        print(f"Query returned {len(sem_avgs)} semester-average records.")
        if len(sem_avgs) > 0:
            print(f"Sample: {sem_avgs[:5]}")
        else:
            print("CRITICAL: Join Query returned nothing. Check FKs.")
            # Check relationships manually
            first_res = StudentResult.query.first()
            if first_res:
                print(f"First Result: {first_res}")
                if first_res.paper:
                    print(f"  -> Linked Paper: {first_res.paper}")
                    if first_res.paper.exam_event:
                        print(f"    -> Linked Event: {first_res.paper.exam_event}")
                    else:
                        print("    -> FAIL: No Event linked to paper")
                else:
                    print("  -> FAIL: No Paper linked to result")

        # 3. Simulate Consistency Logic
        print("\n--- Simulating Logic ---")
        student_data = {}
        students = {s.id: s for s in StudentProfile.query.all()}
        
        results = db.session.query(StudentResult).all()
        for r in results:
             sid = r.student_id
             if sid not in student_data:
                 name = students.get(sid).display_name if students.get(sid) else "Unknown"
                 student_data[sid] = {'marks': [], 'name': name}
             if r.marks_obtained is not None:
                 student_data[sid]['marks'].append(r.marks_obtained)
        
        consistency = []
        for sid, data in student_data.items():
            if len(data['marks']) > 1:
                avg = statistics.mean(data['marks'])
                std = statistics.stdev(data['marks'])
                consistency.append({'name': data['name'], 'x': avg, 'y': std})
        
        print(f"Generated {len(consistency)} consistency points.")
        if len(consistency) == 0 :
            print("FAIL: No student has > 1 mark?")

if __name__ == "__main__":
    debug()
