from app import create_app, db
from app.models import Subject, StudentProfile

app = create_app('development')

with app.app_context():
    print("--- DEBUGGING DATA CONSISTENCY ---")
    
    # Check OS Subject
    os_sub = Subject.query.filter_by(name='OS').first()
    if os_sub:
        print(f"Subject: {os_sub.name}, Course: {os_sub.course_name}, Sem: {os_sub.semester}")
        
        # Check Students for this
        count = StudentProfile.query.filter_by(
            course_name=os_sub.course_name,
            semester=os_sub.semester
        ).count()
        print(f"Matching Students: {count}")
    else:
        print("Subject 'OS' not found.")

    print("\n--- Student Distribution ---")
    students = StudentProfile.query.all()
    dist = {}
    for s in students:
        key = f"{s.course_name}-Sem{s.semester}"
        dist[key] = dist.get(key, 0) + 1
    
    for k, v in dist.items():
        print(f"{k}: {v}")
