from flask import render_template, request
from flask_login import login_required
from datetime import datetime, date, timedelta
from app.models import FeeRecord, StudentQuery, QueryMessage, FacultyProfile
from flask_login import current_user, login_required
from flask import render_template, request, redirect, url_for, flash, send_file
import io
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

from app.models import FeeRecord, StudentQuery, QueryMessage, FacultyProfile, Subject, Syllabus, StudentProfile, Timetable, Attendance, ExamEvent, ExamPaper, StudentResult
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

@faculty_bp.route('/attendance', methods=['GET', 'POST'])
@login_required
def attendance():
    faculty = FacultyProfile.query.filter_by(user_id=current_user.id).first_or_404()
    subjects = Subject.query.filter_by(faculty_id=faculty.id).all()
    
    # Defaults
    selected_subject_id = request.args.get('subject_id', type=int)
    selected_date_str = request.args.get('date')
    page = request.args.get('page', 1, type=int)
    
    attendance_data = []
    stats = {'present': 0, 'absent': 0, 'total': 0, 'percentage': 0}
    selected_subject = None
    lecture_history = []
    pagination = {}
    
    # Check for Pending Attendance (For Notification)
    today = date.today()
    pending_count = 0
    # Quick check for today's lectures
    day_name = today.strftime('%A')
    todays_slots = Timetable.query.filter_by(faculty_id=faculty.id, day_of_week=day_name).all()
    for slot in todays_slots:
        is_marked = Attendance.query.filter_by(subject_id=slot.subject_id, date=today).first()
        if not is_marked:
            pending_count += 1

    if request.method == 'POST':
        # Handle Attendance Submission
        subj_id = request.form.get('subject_id')
        date_val = request.form.get('date')
        
        # Re-fetch for safety
        target_subject = Subject.query.get_or_404(subj_id)
        
        # iterate form
        for key in request.form:
            if key.startswith('status_'):
                student_id = int(key.split('_')[1])
                status = request.form[key]
                
                # Check Existing
                att = Attendance.query.filter_by(
                    student_id=student_id,
                    subject_id=subj_id,
                    date=datetime.strptime(date_val, '%Y-%m-%d').date()
                ).first()
                
                if att:
                    att.status = status
                else:
                    new_att = Attendance(
                        student_id=student_id,
                        course_name=target_subject.course_name, # Fallback
                        date=datetime.strptime(date_val, '%Y-%m-%d').date(),
                        status=status,
                        subject_id=subj_id,
                        faculty_id=faculty.id
                    )
                    db.session.add(new_att)
        
        db.session.commit()
        flash('Attendance updated successfully!', 'success')
        return redirect(url_for('faculty.attendance', subject_id=subj_id, date=date_val))

    # If parameters provided, load Marking View
    if selected_subject_id and selected_date_str:
        selected_date = datetime.strptime(selected_date_str, '%Y-%m-%d').date()
        selected_subject = Subject.query.get_or_404(selected_subject_id)
        
        # 1. Fetch Students
        students = StudentProfile.query.filter_by(
            course_name=selected_subject.course_name,
            semester=selected_subject.semester
        ).order_by(StudentProfile.enrollment_number).all()
        
        # 2. Fetch Existing
        existing_records = Attendance.query.filter_by(
            subject_id=selected_subject_id,
            date=selected_date
        ).all()
        
        status_map = {att.student_id: att.status for att in existing_records}
        
        for student in students:
            current_status = status_map.get(student.id, 'Present') 
            attendance_data.append({'student': student, 'status': current_status})
            if current_status == 'Present': stats['present'] += 1
            else: stats['absent'] += 1
                
        stats['total'] = len(students)
        if stats['total'] > 0:
            stats['percentage'] = round((stats['present'] / stats['total']) * 100, 1)

        # 4. Calculate Low Attendance List (< 75%)
        # Fetch ALL historical attendance for this subject
        low_attendance_list = []
        all_subject_attendance = Attendance.query.filter_by(subject_id=selected_subject_id).all()
        
        # Aggregation
        student_stats = {} # { id: {total: 0, present: 0} }
        for rec in all_subject_attendance:
            if rec.student_id not in student_stats: student_stats[rec.student_id] = {'total': 0, 'present': 0}
            student_stats[rec.student_id]['total'] += 1
            if rec.status == 'Present':
                student_stats[rec.student_id]['present'] += 1
        
        for student in students:
            s_stat = student_stats.get(student.id, {'total': 0, 'present': 0})
            if s_stat['total'] > 0:
                pct = (s_stat['present'] / s_stat['total']) * 100
            else:
                pct = 100.0 # Default safe
            
            if pct < 75:
                low_attendance_list.append({
                    'student': student,
                    'percentage': round(pct, 1),
                    'attended': s_stat['present'],
                    'total': s_stat['total']
                })

    else:
        # Load Dashboard View: Recent Lectures Table
        # Generate last 30 days history
        today = date.today()
        # Look back 30 days
        all_lectures = []
        
        # Optimize: Filter dict of faculty's timetable slots by day
        # Map: 'Monday' -> [Slot1, Slot2]
        timetable_map = {}
        slots = Timetable.query.filter_by(faculty_id=faculty.id).all()
        for slot in slots:
            if slot.day_of_week not in timetable_map: timetable_map[slot.day_of_week] = []
            timetable_map[slot.day_of_week].append(slot)
            
        # Iterate dates descending
        for i in range(30):
            curr_date = today - timedelta(days=i)
            day_name = curr_date.strftime('%A')
            
            if day_name in timetable_map:
                for slot in timetable_map[day_name]:
                    # Check if marked
                    marked_count = Attendance.query.filter_by(
                        subject_id=slot.subject_id,
                        date=curr_date
                    ).count()
                    
                    status = 'Marked' if marked_count > 0 else 'Pending'
                    
                    all_lectures.append({
                        'date': curr_date,
                        'date_str': curr_date.strftime('%Y-%m-%d'),
                        'subject': slot.subject,
                        'time': f"{9 + (slot.period_number-1)}:00 - {10 + (slot.period_number-1)}:00", # Approx logic
                        'status': status
                    })
        
        # Pagination Logic (Manual list pagination)
        per_page = 5
        total_items = len(all_lectures)
        start = (page - 1) * per_page
        end = start + per_page
        lecture_history = all_lectures[start:end]
        
        pagination = {
            'page': page,
            'total_pages': (total_items + per_page - 1) // per_page,
            'has_next': end < total_items,
            'has_prev': start > 0
        }

    return render_template(
        'faculty/attendance.html', 
        lecture_history=lecture_history,
        pagination=pagination,
        subjects=subjects, 
        selected_subject=selected_subject,
        selected_date=selected_date_str, # Keep valid if selected
        attendance_data=attendance_data,
        stats=stats,
        pending_count=pending_count,
        low_attendance_list=locals().get('low_attendance_list', [])
    )

@faculty_bp.route('/attendance/export/csv')
@login_required
def export_attendance_csv():
    import csv
    import io
    from flask import make_response

    subject_id = request.args.get('subject_id')
    date_str = request.args.get('date')
    
    if not subject_id or not date_str:
        flash('Please select a subject and date to export.', 'error')
        return redirect(url_for('faculty.attendance'))
        
    subject = Subject.query.get_or_404(subject_id)
    date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
    
    # Fetch Data (Reuse Logic or Refactor - Reusing for speed)
    existing_records = Attendance.query.filter_by(subject_id=subject_id, date=date_obj).all()
    record_map = {r.student_id: r.status for r in existing_records}
    
    students = StudentProfile.query.filter_by(
            course_name=subject.course_name,
            semester=subject.semester
        ).order_by(StudentProfile.enrollment_number).all()

    # Generate CSV
    si = io.StringIO()
    cw = csv.writer(si)
    cw.writerow(['Enrollment', 'Name', 'Status', 'Date', 'Subject', 'Course'])
    
    for stu in students:
        status = record_map.get(stu.id, 'Unmarked')
        cw.writerow([
            stu.enrollment_number, 
            stu.display_name, 
            status, 
            date_str, 
            subject.name, 
            f"{subject.course_name} Sem {subject.semester}"
        ])
        
    output = make_response(si.getvalue())
    output.headers["Content-Disposition"] = f"attachment; filename=attendance_{subject.name}_{date_str}.csv"
    output.headers["Content-type"] = "text/csv"
    return output

@faculty_bp.route('/attendance/print')
@login_required
def print_attendance_report():
    subject_id = request.args.get('subject_id')
    date_str = request.args.get('date')
    
    if not subject_id or not date_str:
        return "Missing arguments", 400
        
    subject = Subject.query.get_or_404(subject_id)
    date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
    
    existing_records = Attendance.query.filter_by(subject_id=subject_id, date=date_obj).all()
    record_map = {r.student_id: r.status for r in existing_records}
    
    students = StudentProfile.query.filter_by(course_name=subject.course_name, semester=subject.semester).order_by(StudentProfile.enrollment_number).all()
    
    final_data = []
    stats = {'present': 0, 'absent': 0, 'total': 0}
    
    for stu in students:
        status = record_map.get(stu.id, 'Unmarked')
        final_data.append({'student': stu, 'status': status})
        if status == 'Present': stats['present'] += 1
        elif status == 'Absent': stats['absent'] += 1
    
    stats['total'] = len(students)
    
    return render_template(
        'faculty/attendance_print.html',
        subject=subject,
        date_str=date_str,
        data=final_data,
        stats=stats
    )

@faculty_bp.route('/material', methods=['GET', 'POST'])
@login_required
def material():
    faculty = FacultyProfile.query.filter_by(user_id=current_user.id).first_or_404()
    subjects = Subject.query.filter_by(faculty_id=faculty.id).all()
    
    if request.method == 'POST':
        subj_id = request.form.get('subject_id')
        link_url = request.form.get('resource_link')
        
        subject = Subject.query.get_or_404(subj_id)
        
        # Security: Ensure ownership
        if subject.faculty_id != faculty.id:
            flash('Unauthorized action.', 'error')
            return redirect(url_for('faculty.material'))

        if link_url:
             # Basic validation
            if not link_url.startswith(('http://', 'https://')):
                link_url = 'https://' + link_url
            subject.resource_link = link_url
            db.session.commit()
            flash(f'Resource link updated for {subject.name}.', 'success')
        else:
            # Clear link? Or error? Letting them clear it if empty
            subject.resource_link = None
            db.session.commit()
            flash(f'Resource link removed for {subject.name}.', 'info')
            
        return redirect(url_for('faculty.material'))

    return render_template('faculty/material.html', subjects=subjects)

# Download route removed (Links are external)

# Delete route removed (Managed via update)

@faculty_bp.route('/marks', methods=['GET', 'POST'])
@login_required
def marks():
    faculty = FacultyProfile.query.filter_by(user_id=current_user.id).first_or_404()
    
    # 1. Fetch Active Exams
    # For now, fetching all. In real app, filter by date or 'is_active'
    exam_events = ExamEvent.query.order_by(ExamEvent.start_date.desc()).all()
    
    selected_exam_id = request.args.get('exam_id', type=int)
    selected_paper_id = request.args.get('paper_id', type=int)
    
    papers = []
    selected_exam = None
    selected_paper = None
    students_data = [] # List of {student, result_obj_or_none}
    
    # 2. If Exam Selected, Fetch Papers for this Faculty
    if selected_exam_id:
        selected_exam = ExamEvent.query.get_or_404(selected_exam_id)
        
        # Get subjects taught by faculty
        faculty_subject_ids = [s.id for s in faculty.subjects_taught]
        
        # Fetch papers for this exam AND taught by faculty
        papers = ExamPaper.query.filter(
            ExamPaper.exam_event_id == selected_exam_id,
            ExamPaper.subject_id.in_(faculty_subject_ids)
        ).all()
        
    # 3. If Paper Selected, Fetch Students and Results
    if selected_paper_id:
        selected_paper = ExamPaper.query.get_or_404(selected_paper_id)
        
        # Security: Ensure faculty teaches this subject
        if selected_paper.subject.faculty_id != faculty.id:
            flash('Unauthorized access to this paper.', 'error')
            return redirect(url_for('faculty.marks'))
            
        # Fetch Students (Course/Sem matches Paper's Subject)
        students = StudentProfile.query.filter_by(
            course_name=selected_paper.subject.course_name,
            semester=selected_paper.subject.semester
        ).order_by(StudentProfile.enrollment_number).all()
        
        # Fetch Existing Results
        existing_results = StudentResult.query.filter_by(exam_paper_id=selected_paper_id).all()
        result_map = {res.student_id: res for res in existing_results}
        
        for stu in students:
            students_data.append({
                'student': stu,
                'result': result_map.get(stu.id)
            })

    # 4. Handle POST (Save Marks)
    if request.method == 'POST':
        if not selected_paper:
             flash('No paper selected.', 'error')
             return redirect(url_for('faculty.marks'))
             
        count = 0
        for data in students_data:
            stu = data['student']
            input_name = f'marks_{stu.id}'
            
            if input_name in request.form:
                marks_val = request.form.get(input_name)
                
                # Logic: If empty, maybe treat as Absent or None?
                # If present, update or create
                
                res = data['result']
                if not res:
                    res = StudentResult(
                        exam_paper_id=selected_paper.id,
                        student_id=stu.id
                    )
                    db.session.add(res)
                
                if marks_val and marks_val.strip() != '':
                    try:
                        val = float(marks_val)
                        if val < 0 or val > selected_paper.total_marks:
                            flash(f'Invalid marks for {stu.enrollment_number}. Max is {selected_paper.total_marks}', 'error')
                            continue
                        res.marks_obtained = val
                        res.status = 'Present'
                        # Fail logic? If < 33%?
                        res.is_fail = (val < (selected_paper.total_marks * 0.33)) # Simple rule
                    except ValueError:
                         flash(f'Invalid number for {stu.enrollment_number}', 'error')
                else:
                    # If empty, mark as Null or Absent? 
                    # Let's say if unchecked 'present', it's absent.
                    # Simplified: If empty string, do nothing or set None
                    pass # Keep previous or ignore
                
                count += 1
        
        db.session.commit()
        flash(f'Updated marks for {count} students.', 'success')
        return redirect(url_for('faculty.marks', exam_id=selected_exam_id, paper_id=selected_paper_id))

    return render_template(
        'faculty/marks.html', 
        exam_events=exam_events, 
        papers=papers, 
        selected_exam=selected_exam,
        selected_paper=selected_paper,
        students_data=students_data
    )

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
    faculty = FacultyProfile.query.filter_by(user_id=current_user.id).first_or_404()
    
    # Get current day
    today_name = datetime.utcnow().strftime('%A') # e.g. "Monday"
    # For Demo purposes, if it's Sunday, show Monday's schedule so the user sees something
    if today_name == 'Sunday':
        today_name = 'Monday' # Demo fallback
        flash('Showing Monday Schedule (Weekend Override)', 'info')

    slots = Timetable.query.filter_by(
        faculty_id=faculty.id, 
        day_of_week=today_name
    ).order_by(Timetable.period_number).all()
    
    schedule_data = []
    current_time = datetime.utcnow().time() # UTC time, might need offset for display logic
    
    # Base Time: 9:00 AM
    base_hour = 9 
    
    for slot in slots:
        # Calculate Time
        start_h = base_hour + (slot.period_number - 1)
        end_h = start_h + 1
        
        # Format "9:00 - 10:00 AM"
        t_str = f"{start_h if start_h <= 12 else start_h-12}:00 - {end_h if end_h <= 12 else end_h-12}:00 {'AM' if start_h < 12 else 'PM'}"
        
        # Student Count
        count = StudentProfile.query.filter_by(
            course_name=slot.course_name,
            semester=slot.semester
        ).count()
        
        schedule_data.append({
            'time_str': t_str,
            'subject': slot.subject.name,
            'course_detail': f"{slot.course_name} • Sem {slot.semester}",
            'room': slot.room_number,
            'student_count': count,
            'attendance_marked': False # Placeholder logic
        })
        
    return render_template('faculty/schedule.html', schedule=schedule_data, day_name=today_name)

@faculty_bp.route('/timetable')
@login_required
def timetable():
    return render_template('faculty/timetable.html')
