from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from flask_login import login_required
from app.extensions import db
from app.models import ExamEvent, ExamPaper, Subject, StudentProfile, StudentResult
from datetime import datetime

exams_bp = Blueprint('exams', __name__)

@exams_bp.route('/exams', methods=['GET'])
@login_required
def exams_dashboard():
    # List all exam events
    events = ExamEvent.query.order_by(ExamEvent.start_date.desc()).all()
    return render_template('exams/dashboard.html', events=events)

@exams_bp.route('/exams/create', methods=['GET', 'POST'])
@login_required
def create_exam_event():
    if request.method == 'POST':
        name = request.form.get('name')
        course = request.form.get('course')
        semester = request.form.get('semester')
        academic_year = request.form.get('academic_year')
        start_date = datetime.strptime(request.form.get('start_date'), '%Y-%m-%d').date()
        end_date = datetime.strptime(request.form.get('end_date'), '%Y-%m-%d').date()
        
        event = ExamEvent(
            name=name,
            course_name=course,
            semester=semester,
            academic_year=academic_year,
            start_date=start_date,
            end_date=end_date
        )
        db.session.add(event)
        db.session.commit()
        flash('Exam Event Created!', 'success')
        return redirect(url_for('.schedule_exam', event_id=event.id))

    courses = db.session.query(StudentProfile.course_name).distinct().all()
    courses = [c[0] for c in courses]
    return render_template('exams/create_event.html', courses=courses)

@exams_bp.route('/exams/<int:event_id>/schedule', methods=['GET', 'POST'])
@login_required
def schedule_exam(event_id):
    event = ExamEvent.query.get_or_404(event_id)
    subjects = Subject.query.filter_by(course_name=event.course_name, semester=event.semester).all()
    
    if request.method == 'POST':
        # Form handling for creating Papers
        for sub in subjects:
            date_str = request.form.get(f'date_{sub.id}')
            start_str = request.form.get(f'start_{sub.id}')
            end_str = request.form.get(f'end_{sub.id}')
            
            if date_str and start_str and end_str:
                # Check if paper exists
                paper = ExamPaper.query.filter_by(exam_event_id=event.id, subject_id=sub.id).first()
                
                date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
                start_obj = datetime.strptime(start_str, '%H:%M').time()
                end_obj = datetime.strptime(end_str, '%H:%M').time()
                
                if paper:
                    paper.date = date_obj
                    paper.start_time = start_obj
                    paper.end_time = end_obj
                else:
                    paper = ExamPaper(
                        exam_event_id=event.id,
                        subject_id=sub.id,
                        date=date_obj,
                        start_time=start_obj,
                        end_time=end_obj,
                        total_marks=100
                    )
                    db.session.add(paper)
        
        if request.form.get('action') == 'publish':
            event.is_published = True
            flash('Schedule published successfully!', 'success')
        else:
            flash('Schedule updated successfully!', 'success')
        
        db.session.commit()
    
    # Pre-fetch existing papers logic for template
    existing_papers = {p.subject_id: p for p in event.papers}
    
    return render_template('exams/schedule_exam.html', event=event, subjects=subjects, papers=existing_papers)

@exams_bp.route('/exams/export', methods=['GET', 'POST'])
@login_required
def export_results():
    if request.method == 'POST':
        import csv
        from io import StringIO
        from flask import Response

        course = request.form.get('course')
        semester = int(request.form.get('semester'))
        academic_year = request.form.get('academic_year')
        subject_id = request.form.get('subject_id')

        # 1. Fetch Students
        students = StudentProfile.query.filter_by(course_name=course, semester=semester).order_by(StudentProfile.enrollment_number).all()

        # 2. Prepare CSV
        si = StringIO()
        cw = csv.writer(si)

        # Header
        if subject_id:
            subject = Subject.query.get(subject_id)
            subject_name = subject.name if subject else "Unknown Subject"
            cw.writerow(['Enrollment No', 'Name', 'Course', 'Semester', 'Academic Year', 'Subject', 'Marks Obtained', 'Total Marks', 'Status'])
        else:
            # Consolidated (Dynamic Columns? Keep it simple for now, maybe just list students)
            # User asked for "result of all the student"
            cw.writerow(['Enrollment No', 'Name', 'Course', 'Semester', 'Academic Year', 'Subject', 'Marks Obtained', 'Status'])

        # Data
        if subject_id:
             subject = Subject.query.get(subject_id)
             for student in students:
                 # TODO: Fetch actual Result if exists? 
                 # Current request implies generating the sheet to BE filled or viewing it.
                 # Since we skipped result entry, this acts as a template or view of empty results.
                 cw.writerow([student.enrollment_number, student.display_name, course, semester, academic_year, subject.name, '', '100', ''])
        else:
            # All subjects
            subjects = Subject.query.filter_by(course_name=course, semester=semester).all()
            for student in students:
                for sub in subjects:
                    cw.writerow([student.enrollment_number, student.display_name, course, semester, academic_year, sub.name, '', '', ''])

        output =  Response(si.getvalue(), mimetype="text/csv")
        output.headers["Content-Disposition"] = f"attachment; filename=results_{course}_{semester}_{academic_year}.csv"
        return output

    # GET: Show Form
    courses = db.session.query(StudentProfile.course_name).distinct().all()
    courses = [c[0] for c in courses]
    all_subjects = Subject.query.order_by(Subject.name).all() # Should be filtered by JS ideally, but loading all for now
    
    return render_template('exams/export_results.html', courses=courses, subjects=all_subjects)
