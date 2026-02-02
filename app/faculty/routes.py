from flask import render_template, request
from flask_login import login_required
from datetime import datetime
from app.models import FeeRecord, StudentQuery, QueryMessage, FacultyProfile
from flask_login import current_user, login_required
from flask import render_template, request, redirect, url_for, flash
from app.extensions import db
from . import faculty_bp

@faculty_bp.route('/dashboard')
@login_required
def dashboard():
    return render_template('faculty_dashboard.html')

@faculty_bp.route('/fees')
@login_required
def fees():
    # Fetch all fee records (In a real app, filter by faculty's students)
    records = FeeRecord.query.order_by(FeeRecord.due_date.desc()).all()
    return render_template('faculty/fees.html', records=records)

@faculty_bp.route('/fees/mark_paid/<int:fee_id>', methods=['POST'])
@login_required
def mark_paid(fee_id):
    fee = FeeRecord.query.get_or_404(fee_id)
    fee.status = 'Paid'
    fee.payment_date = datetime.utcnow()
    fee.payment_mode = 'Cash/Office'
    fee.transaction_reference = f"OFFICE-MANUAL-{fee.id}-{int(datetime.utcnow().timestamp())}"
    db.session.commit()
    return {'status': 'success'}

@faculty_bp.route('/queries')
@login_required
def queries():
    faculty = FacultyProfile.query.filter_by(user_id=current_user.id).first_or_404()
    
    # Check for filters
    status = request.args.get('status', 'all')
    
    query = StudentQuery.query.filter_by(faculty_id=faculty.id)
    if status != 'all':
        query = query.filter_by(status=status.capitalize())
        
    queries = query.order_by(StudentQuery.updated_at.desc()).all()
    
    return render_template('faculty/queries.html', queries=queries, filter=status)

@faculty_bp.route('/queries/<int:query_id>', methods=['GET', 'POST'])
@login_required
def query_chat(query_id):
    faculty = FacultyProfile.query.filter_by(user_id=current_user.id).first_or_404()
    query = StudentQuery.query.get_or_404(query_id)
    
    if query.faculty_id != faculty.id:
        return "Unauthorized", 403

    if request.method == 'POST':
        content = request.form.get('content')
        if content:
            msg = QueryMessage(
                query_id=query.id,
                sender_type='faculty',
                content=content
            )
            db.session.add(msg)
            
            # Update status to Answered
            if query.status == 'Pending':
                 query.status = 'Answered'
            
            query.updated_at = datetime.utcnow()
            db.session.commit()
            return redirect(url_for('faculty.query_chat', query_id=query_id))

    return render_template('faculty/query_chat.html', query=query)

# --- New Faculty Routes Placeholders ---

from app.models import FeeRecord, StudentQuery, QueryMessage, FacultyProfile, Subject, Syllabus, StudentProfile
from werkzeug.utils import secure_filename

# ... (existing imports)

@faculty_bp.route('/classes', methods=['GET', 'POST'])
@login_required
def classes():
    faculty = FacultyProfile.query.filter_by(user_id=current_user.id).first_or_404()
    
    if request.method == 'POST':
        if 'syllabus_file' in request.files:
            file = request.files['syllabus_file']
            subject_id = request.form.get('subject_id')
            
            if file and file.filename != '' and subject_id:
                filename = secure_filename(file.filename)
                # Ensure only PDF
                if not filename.lower().endswith('.pdf'):
                    flash('Only PDF files are allowed.', 'error')
                else:
                    file_data = file.read()
                    
                    # check if exists
                    existing = Syllabus.query.filter_by(subject_id=subject_id).first()
                    if existing:
                        existing.filename = filename
                        existing.file_data = file_data
                        existing.upload_date = datetime.utcnow()
                    else:
                        new_syllabus = Syllabus(subject_id=subject_id, filename=filename, file_data=file_data)
                        db.session.add(new_syllabus)
                    
                    db.session.commit()
                    flash('Syllabus uploaded successfully!', 'success')
            else:
                flash('No file selected.', 'error')
        
        elif 'search_enrollment' in request.form:
             enrollment_id = request.form.get('search_enrollment').strip()
             student = StudentProfile.query.filter_by(enrollment_number=enrollment_id).first()
             if student:
                 return redirect(url_for('faculty.student_detail', student_id=student.id))
             else:
                 flash('Student not found with that Enrollment ID.', 'error')
                 
        return redirect(url_for('faculty.classes'))

    # Fetch Subjects
    subjects = Subject.query.filter_by(faculty_id=faculty.id).all()
    
    # Enrich with student count
    subject_data = []
    for sub in subjects:
        # Count students in this course & semester
        # Assuming course_name and semester match
        count = StudentProfile.query.filter_by(
            course_name=sub.course_name,
            semester=sub.semester
        ).count()
        
        subject_data.append({
            'subject': sub,
            'student_count': count
        })

    return render_template('faculty/classes.html', subject_data=subject_data)

@faculty_bp.route('/student/<int:student_id>')
@login_required
def student_detail(student_id):
    student = StudentProfile.query.get_or_404(student_id)
    return render_template('faculty/student_detail.html', student=student)

@faculty_bp.route('/classes/syllabus/<int:subject_id>')
@login_required
def download_syllabus(subject_id):
    syllabus = Syllabus.query.filter_by(subject_id=subject_id).first_or_404()
    from flask import send_file
    import io
    return send_file(
        io.BytesIO(syllabus.file_data),
        mimetype='application/pdf',
        as_attachment=True,
        download_name=syllabus.filename
    )

@faculty_bp.route('/attendance')
@login_required
def attendance():
    return render_template('faculty/attendance.html')

@faculty_bp.route('/material')
@login_required
def material():
    return render_template('faculty/material.html')

@faculty_bp.route('/marks')
@login_required
def marks():
    return render_template('faculty/marks.html')

@faculty_bp.route('/mentorship')
@login_required
def mentorship():
    return render_template('faculty/mentorship.html')

@faculty_bp.route('/notices')
@login_required
def notices():
    return render_template('faculty/notices.html')

@faculty_bp.route('/schedule')
@login_required
def schedule():
    return render_template('faculty/schedule.html')

@faculty_bp.route('/timetable')
@login_required
def timetable():
    return render_template('faculty/timetable.html')
