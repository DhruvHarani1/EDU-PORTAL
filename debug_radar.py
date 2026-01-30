from app import create_app, db
from app.models import StudentResult, ExamPaper, Subject
from sqlalchemy import func

app = create_app()

def debug_radar():
    with app.app_context():
        print("--- Debugging Radar Data ---")
        
        # 1. Check Sem 3 Subjects
        sem3_subs = Subject.query.filter_by(semester=3).all()
        print(f"Found {len(sem3_subs)} subjects for Sem 3")
        for s in sem3_subs:
            print(f" - {s.name} (ID: {s.id})")
            
        # 2. Check Exam Papers for these subjects
        print("\n--- Checking Exam Papers ---")
        for s in sem3_subs:
            papers = ExamPaper.query.filter_by(subject_id=s.id).all()
            print(f"Subject {s.name}: {len(papers)} papers found.")
            for p in papers:
                 res_count = StudentResult.query.filter_by(exam_paper_id=p.id).count()
                 print(f"   -> Paper ID {p.id}: {res_count} results linked.")
                 
                 # Test the AVG query
                 avg_score = db.session.query(func.avg(StudentResult.marks_obtained))\
                     .filter(StudentResult.exam_paper_id == p.id)\
                     .scalar()
                 print(f"   -> Avg Score Direct: {avg_score}")

        # 3. Test the exact Join Query from reports_mgmt.py
        print("\n--- Testing Join Query ---")
        for sub in sem3_subs:
             # Logic from Code:
             # results = db.session.query(func.avg(StudentResult.marks_obtained))\
             #    .join(ExamPaper)\
             #    .filter(ExamPaper.subject_id == sub.id)\
             #    .scalar()
             
             # Being explicit with join condition just in case
             results = db.session.query(func.avg(StudentResult.marks_obtained))\
                .select_from(StudentResult)\
                .join(ExamPaper, StudentResult.exam_paper_id == ExamPaper.id)\
                .filter(ExamPaper.subject_id == sub.id)\
                .scalar()
             
             print(f"Subject {sub.name} Join Query Avg: {results}")

if __name__ == "__main__":
    debug_radar()
