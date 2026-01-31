from app import create_app, db
from app.models import Subject, FacultyProfile, StudentResult, ExamPaper
import statistics

app = create_app()

def debug_faculty():
    with app.app_context():
        print("--- DEBUGG FACULTY DATA ---")
        
        subjects = Subject.query.all()
        print(f"Total Subjects found: {len(subjects)}")
        
        processed_count = 0
        
        for sub in subjects:
            print(f"\nChecking Subject: {sub.name} (ID: {sub.id})")
            
            if not sub.faculty_id:
                print(" -> NO FACULTY ID LINKED.")
                continue
                
            fac = FacultyProfile.query.get(sub.faculty_id)
            if not fac:
                print(f" -> Faculty ID {sub.faculty_id} set, but not found in DB.")
                continue
                
            print(f" -> Linked to Faculty: {fac.display_name}")
            
            # Check Results
            sub_results = db.session.query(StudentResult.marks_obtained)\
                .join(ExamPaper).filter(ExamPaper.subject_id == sub.id).all()
                
            count = len(sub_results)
            print(f" -> Found {count} Student Results.")
            
            if count > 0:
                marks = [r.marks_obtained for r in sub_results if r.marks_obtained is not None]
                avg = statistics.mean(marks)
                print(f" -> Average Score: {avg}")
                processed_count += 1
                
        print(f"\n--- SUMMARY ---")
        print(f"Synthesized Metrics for {processed_count} subjects.")

if __name__ == "__main__":
    debug_faculty()
