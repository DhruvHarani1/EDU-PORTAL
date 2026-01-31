from flask import render_template
from flask_login import login_required
from app.models import StudentProfile, FacultyProfile, Notice, User
from app.extensions import db
from . import admin_bp
from sqlalchemy import func

@admin_bp.route('/dashboard')
@login_required
def dashboard():
    # 1. Counts
    total_students = StudentProfile.query.count()
    total_faculty = FacultyProfile.query.count()
    # Count distinct courses
    # distinct_courses = db.session.query(StudentProfile.course_name).distinct().count() 
    # Better: list of courses + count
    
    # 2. Pie Chart Data (Student vs Course)
    # result = [(course_name, count), ...]
    course_stats = db.session.query(
        StudentProfile.course_name, 
        func.count(StudentProfile.id)
    ).group_by(StudentProfile.course_name).all()
    
    # Process for Chart.js
    course_labels = [stat[0] for stat in course_stats]
    course_counts = [stat[1] for stat in course_stats]
    total_courses = len(course_labels)

    # 3. Recent Activity (Latest Notices)
    recent_notices = Notice.query.order_by(Notice.created_at.desc()).limit(5).all()

    return render_template(
        'admin_dashboard.html',
        total_students=total_students,
        total_faculty=total_faculty,
        total_courses=total_courses,
        course_labels=course_labels,
        course_counts=course_counts,
        recent_notices=recent_notices
    )

@admin_bp.route('/dashboard/download_report')
@login_required
def download_dashboard_report():
    import csv
    import io
    from flask import Response
    from datetime import datetime
    
    # Gather Data
    total_students = StudentProfile.query.count()
    total_faculty = FacultyProfile.query.count()
    courses = db.session.query(StudentProfile.course_name, func.count(StudentProfile.id)).group_by(StudentProfile.course_name).all()
    
    # Create CSV in memory
    output = io.StringIO()
    writer = csv.writer(output)
    
    # Header
    writer.writerow(['EduPortal System Report', f'Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}'])
    writer.writerow([])
    
    # Section 1: Key Metrics
    writer.writerow(['--- KEY METRICS ---'])
    writer.writerow(['Metric', 'Value'])
    writer.writerow(['Total Students', total_students])
    writer.writerow(['Total Faculty', total_faculty])
    writer.writerow([])
    
    # Section 2: Enrollment
    writer.writerow(['--- ENROLLMENT DISTRIBUTION ---'])
    writer.writerow(['Course', 'Count'])
    for c in courses:
        writer.writerow([c[0], c[1]])
    writer.writerow([])
    
    # Section 3: Recent Notices
    writer.writerow(['--- RECENT ACTIVITY ---'])
    notices = Notice.query.order_by(Notice.created_at.desc()).limit(5).all()
    writer.writerow(['Date', 'Title', 'Audience'])
    for n in notices:
        writer.writerow([n.created_at.strftime('%Y-%m-%d'), n.title, n.category])
        
    # Return Response
    return Response(
        output.getvalue(),
        mimetype="text/csv",
        headers={"Content-disposition": "attachment; filename=eduportal_summary_report.csv"}
    )
