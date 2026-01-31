from flask import render_template
from flask_login import login_required, current_user
from . import student_bp
from app.models import StudentProfile, Attendance, Subject, Timetable, StudentResult, ExamPaper
from app.extensions import db

@student_bp.route('/dashboard')
@login_required
def dashboard():
    return render_template('student_dashboard.html')

# Placeholder Routes for Sidebar Navigation
@student_bp.route('/attendance')
@login_required
def attendance():
    from app.models import Attendance, Subject, Timetable, StudentProfile
    from sqlalchemy import func
    import math

    # 1. Get Student Context
    student = StudentProfile.query.filter_by(user_id=current_user.id).first_or_404()
    
    # 2. Get Overall Attendance (Daily)
    total_days = Attendance.query.filter_by(student_id=student.id).count()
    present_days = Attendance.query.filter_by(student_id=student.id, status='Present').count()
    
    overall_percent = (present_days / total_days * 100) if total_days > 0 else 0
    overall_status = "Excellent" if overall_percent >= 85 else "Good" if overall_percent >= 75 else "Critical"

    # 3. Derive Subject-Wise Data via Timetable Heuristic
    # Logic: If present on Monday, present for all Monday subjects.
    subjects = Subject.query.filter_by(course_name=student.course_name, semester=student.semester).all()
    timetable = Timetable.query.filter_by(course_name=student.course_name, semester=student.semester).all()
    
    # Map: DayName (0=Mon) -> [Subject_IDs]
    day_map = {0: [], 1: [], 2: [], 3: [], 4: [], 5: [], 6: []}
    weekdays_str_map = {'Mon': 0, 'Tue': 1, 'Wed': 2, 'Thu': 3, 'Fri': 4, 'Sat': 5, 'Sun': 6}
    
    for slot in timetable:
        d_idx = weekdays_str_map.get(slot.day_of_week)
        if d_idx is not None:
             day_map[d_idx].append(slot.subject_id)

    # Initialize Stats Container
    subject_stats = {} # {id: {name, total, present}}
    for sub in subjects:
        subject_stats[sub.id] = {'name': sub.name, 'total': 0, 'present': 0}

    # Iterate Attendance History
    records = Attendance.query.filter_by(student_id=student.id).all()
    
    for record in records:
        day_idx = record.date.weekday() # 0=Mon
        relevant_subjects = day_map.get(day_idx, [])
        
        for sub_id in relevant_subjects:
            if sub_id in subject_stats:
                subject_stats[sub_id]['total'] += 1
                if record.status == 'Present':
                    subject_stats[sub_id]['present'] += 1

    # 4. Final Calculations (Percent + Recovery)
    processed_subjects = []
    for sub_id, data in subject_stats.items():
        total = data['total']
        present = data['present']
        pct = (present / total * 100) if total > 0 else 0
        
        # Remark
        remark = "Excellent"
        color = "green"
        if pct < 75:
            remark = "Warning"
            color = "amber"
        if pct < 60:
            remark = "Critical"
            color = "red"

        # Recovery Logic: How many consecutive presents needed to hit 75%?
        # Eq: (Present + X) / (Total + X) = 0.75
        # Present + X = 0.75*Total + 0.75*X
        # 0.25*X = 0.75*Total - Present
        # X = (0.75*Total - Present) / 0.25
        recovery_needed = 0
        if pct < 75:
            target = 0.75
            x = (target * total - present) / (1 - target)
            recovery_needed = math.ceil(x) if x > 0 else 0

        processed_subjects.append({
            'name': data['name'],
            'total': total,
            'present': present,
            'percent': round(pct, 1),
            'remark': remark,
            'color': color,
            'recovery_needed': int(recovery_needed)
        })

    return render_template('student/attendance.html', 
                         overall_percent=round(overall_percent, 1),
                         overall_status=overall_status,
                         subjects=processed_subjects)

@student_bp.route('/academics')
@login_required
def academics():
    student = StudentProfile.query.filter_by(user_id=current_user.id).first_or_404()
    
    # Fetch all results
    results = StudentResult.query.filter_by(student_id=student.id).all()
    
    # Group by Exam Event
    exams_data = {}
    
    for res in results:
        exam_event = res.paper.exam_event
        if exam_event.id not in exams_data:
            exams_data[exam_event.id] = {
                'event': exam_event,
                'results': [],
                'total_credits': 0,
                'total_points': 0,
                'spi': 0.0
            }
        
        # Calculate Grade Points (Simple Logic for now)
        # >90: 10, >80: 9, >70: 8, >60: 7, >50: 6, >40: 5, <40: 0
        marks = res.marks_obtained or 0
        points = 0
        grade = 'F'
        if marks >= 90: points, grade = 10, 'AA'
        elif marks >= 80: points, grade = 9, 'AB'
        elif marks >= 70: points, grade = 8, 'BB'
        elif marks >= 60: points, grade = 7, 'BC'
        elif marks >= 50: points, grade = 6, 'CC'
        elif marks >= 40: points, grade = 5, 'CD'
        else: points, grade = 0, 'FF'
        
        # Assuming 3 credits per subject for simplicity if not defined
        credits = res.paper.subject.weekly_lectures or 3
        
        exams_data[exam_event.id]['results'].append({
            'subject': res.paper.subject.name,
            'marks': marks,
            'total': res.paper.total_marks,
            'grade': grade,
            'points': points,
            'credits': credits
        })
        
        exams_data[exam_event.id]['total_credits'] += credits
        exams_data[exam_event.id]['total_points'] += (points * credits)

    # Calculate SPI for each exam
    overall_points = 0
    overall_credits = 0
    
    events_list = []
    for eid, data in exams_data.items():
        if data['total_credits'] > 0:
            data['spi'] = round(data['total_points'] / data['total_credits'], 2)
        
        overall_points += data['total_points']
        overall_credits += data['total_credits']
        events_list.append(data)
        
    cgpi = round(overall_points / overall_credits, 2) if overall_credits > 0 else 0.0

    return render_template('student/academics.html', 
                           student=student, 
                           exams=events_list, 
                           cgpi=cgpi)

@student_bp.route('/academics/marksheet/<int:exam_id>')
@login_required
def download_marksheet(exam_id):
    student = StudentProfile.query.filter_by(user_id=current_user.id).first_or_404()
    
    results = StudentResult.query.filter_by(student_id=student.id).join(ExamPaper).filter(ExamPaper.exam_event_id == exam_id).all()
    
    if not results:
        return "Marksheet not found", 404
        
    exam_event = results[0].paper.exam_event
    
    processed_results = []
    total_credits = 0
    total_points = 0
    total_marks_obtained = 0
    total_max_marks = 0
    
    for res in results:
        marks = res.marks_obtained or 0
        points = 0
        grade = 'F'
        if marks >= 90: points, grade = 10, 'AA'
        elif marks >= 80: points, grade = 9, 'AB'
        elif marks >= 70: points, grade = 8, 'BB'
        elif marks >= 60: points, grade = 7, 'BC'
        elif marks >= 50: points, grade = 6, 'CC'
        elif marks >= 40: points, grade = 5, 'CD'
        else: points, grade = 0, 'FF'
        
        # Assuming credits based on weekly lectures
        credits = res.paper.subject.weekly_lectures or 3
        
        processed_results.append({
            'code': f"SUB{res.paper.subject.id}",
            'subject': res.paper.subject.name,
            'marks': marks,
            'max_marks': res.paper.total_marks,
            'grade': grade,
            'points': points,
            'credits': credits
        })
        
        total_credits += credits
        total_points += (points * credits)
        total_marks_obtained += marks
        total_max_marks += res.paper.total_marks

    spi = round(total_points / total_credits, 2) if total_credits > 0 else 0.0
    
    return render_template('student/marksheet_print.html',
                           student=student,
                           exam=exam_event,
                           results=processed_results,
                           spi=spi,
                           total_marks_obtained=total_marks_obtained,
                           total_max_marks=total_max_marks)

@student_bp.route('/notes')
@login_required
def notes():
    return render_template('student_dashboard.html') # TODO: Create notes.html

@student_bp.route('/events')
@login_required
def events():
    return render_template('student_dashboard.html') # TODO: Create events.html

@student_bp.route('/notices')
@login_required
def notices():
    return render_template('student_dashboard.html') # TODO: Create notices.html

@student_bp.route('/fees')
@login_required
def fees():
    return render_template('student_dashboard.html') # TODO: Create fees.html

@student_bp.route('/queries')
@login_required
def queries():
    return render_template('student_dashboard.html') # TODO: Create queries.html

@student_bp.route('/exams')
@login_required
def exams():
    return render_template('student_dashboard.html') # TODO: Create exams.html

@student_bp.route('/clubs')
@login_required
def clubs():
    return render_template('student_dashboard.html') # TODO: Create clubs.html

@student_bp.route('/id-card')
@login_required
def id_card():
    return render_template('student_dashboard.html') # TODO: Create id_card.html

@student_bp.route('/timetable')
@login_required
def timetable():
    return render_template('student_dashboard.html') # TODO: Create timetable.html

@student_bp.route('/scholarship')
@login_required
def scholarship():
    return render_template('student_dashboard.html') # TODO: Create scholarship.html

@student_bp.route('/settings')
@login_required
def settings():
    return render_template('student_dashboard.html') # TODO: Create settings.html
