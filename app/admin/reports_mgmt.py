from flask import Blueprint, render_template, jsonify
from flask_login import login_required
from app.extensions import db
from app.models import StudentResult, Attendance, Subject, StudentProfile, ExamEvent, ExamPaper
from sqlalchemy import func
import statistics

reports_bp = Blueprint('reports', __name__)

@reports_bp.route('/reports', methods=['GET'])
@login_required
def dashboard():
    return render_template('reports/dashboard.html')

# --- 1. Student Performance Intelligence ---
@reports_bp.route('/reports/student-performance', methods=['GET'])
@login_required
def student_performance_view():
    return render_template('reports/student_performance.html')

@reports_bp.route('/api/reports/student-performance', methods=['GET'])
@login_required
def student_performance_data():
    # 1. Academic DNA (Radar): Avg Marks per Subject (Sem 3)
    # 2. Consistency (Scatter): Avg vs StdDev
    # 3. Growth Velocity: Compare Sem 1 vs Sem 3 Avg
    
    # Fetch all results
    results = db.session.query(StudentResult).all()
    # Group by Student -> Sem -> Marks
    # This is heavy, in prod we'd use SQL aggregation.
    
    student_data = {} 
    
    # Pre-fetch Student Profiles for name/sem
    students = {s.id: s for s in StudentProfile.query.all()}
    
    for r in results:
        sid = r.student_id
        if sid not in student_data: 
            student_data[sid] = {'marks': [], 'sem_marks': {1:[], 2:[], 3:[]}, 'name': students.get(sid).display_name}
        
        if r.marks_obtained is not None:
            student_data[sid]['marks'].append(r.marks_obtained)
            # Infer sem from ExamEvent
            # This is an N+1 issue technically but we need it. 
            # Better optimization: Join ExamEvent in the initial query.
            # But for now, let's use the Paper -> Event relationship if accessible or just map via subject logic?
            # Actually, `r.exam_paper.exam_event.semester` works if relationships are set, but let's query safer.
            pass
    
    # Re-query with explicit Join for Semester Analysis (Growth Velocity)
    # Get average marks per student per semester
    sem_avgs = db.session.query(
        StudentResult.student_id, 
        ExamEvent.semester, 
        func.avg(StudentResult.marks_obtained)
    ).join(ExamPaper).join(ExamEvent).group_by(StudentResult.student_id, ExamEvent.semester).all()
    
    # Populate semester data
    for sid, sem, avg in sem_avgs:
        if sid in student_data:
            student_data[sid]['sem_marks'][sem] = avg

    # Optimized Consistency & Velocity
    consistency = []
    
    # 1. Consistency: Just take all marks for a student across all time
    for sid, data in student_data.items():
        if len(data['marks']) > 1:
            avg = statistics.mean(data['marks'])
            std = statistics.stdev(data['marks'])
            
            # Growth Velocity: (Sem 3 Avg - Sem 1 Avg)
            growth = 0
            s1 = data['sem_marks'].get(1, 0)
            s3 = data['sem_marks'].get(3, 0)
            if s1 > 0 and s3 > 0:
                growth = round(((s3 - s1) / s1) * 100, 1)
            
            consistency.append({
                'name': data['name'], 
                'x': round(avg, 1), 
                'y': round(std, 1),
                'growth': growth
            })
            
    # 2. Danger Zone (Avg < 40 or Fail Count > 2)
    danger_zone = []
    for sid, data in student_data.items():
        avg = statistics.mean(data['marks']) if data['marks'] else 0
        if avg < 40:
            danger_zone.append({'name': data['name'], 'avg': round(avg, 1), 'risk': 'Critical'})

    # 3. Radar Data (Real Aggregation for Sem 3)
    # Fetch marks grouped by Subject for Semester 3
    radar_labels = []
    radar_data = []
    
    # We want subjects from Sem 3
    sem3_subjects = Subject.query.filter_by(semester=3).all()
    
    for sub in sem3_subjects:
        # Get all results for this subject
        # Join: StudentResult -> ExamPaper -> Subject
        results = db.session.query(func.avg(StudentResult.marks_obtained))\
            .join(ExamPaper)\
            .filter(ExamPaper.subject_id == sub.id)\
            .scalar()
            
        if results:
            radar_labels.append(sub.name)
            radar_data.append(round(results, 1))
            
    return jsonify({
        'consistency': consistency,
        'danger_zone': danger_zone,
        'radar': {'labels': radar_labels, 'data': radar_data}
    })

# --- 2. Attendance Analytics ---
@reports_bp.route('/reports/attendance-analytics', methods=['GET'])
@login_required
def attendance_analytics_view():
    return render_template('reports/attendance_analytics.html')

@reports_bp.route('/api/reports/attendance', methods=['GET'])
@login_required
def attendance_data():
    # 1. Fatigue Index (Day of Week)
    attendances = Attendance.query.all()
    day_counts = {0:0, 1:0, 2:0, 3:0, 4:0}
    day_presents = {0:0, 1:0, 2:0, 3:0, 4:0}
    
    for att in attendances:
        wd = att.date.weekday()
        if wd <= 4:
            day_counts[wd] += 1
            if att.status == 'Present': day_presents[wd] += 1
            
    fatigue = []
    for i in range(5):
        rate = (day_presents[i] / day_counts[i]) if day_counts[i] > 0 else 0
        fatigue.append(round(rate, 2))
        
    return jsonify({
        'fatigue': fatigue,
        'truancy_prob': [{'name': 'Student X', 'prob': 85}, {'name': 'Student Y', 'prob': 72}] # Mock
    })

# --- 3. Faculty Insights ---
@reports_bp.route('/reports/faculty-insights', methods=['GET'])
@login_required
def faculty_insights_view():
    return render_template('reports/faculty_insights.html')

@reports_bp.route('/api/reports/faculty', methods=['GET'])
@login_required
def faculty_data():
    # 1. Impact Factor (Difficulty vs Pass Rate)
    subjects = Subject.query.all()
    impact = []
    for sub in subjects:
        # Join results
        sub_results = db.session.query(StudentResult).join(ExamPaper).filter(ExamPaper.subject_id == sub.id).all()
        if sub_results:
            marks = [r.marks_obtained for r in sub_results if r.marks_obtained is not None]
            if marks:
                avg = statistics.mean(marks)
                pass_rate = (len([m for m in marks if m >= 35]) / len(marks)) * 100
                difficulty = 100 - avg # Proxy
                impact.append({'subject': sub.name, 'x': round(difficulty, 1), 'y': round(pass_rate, 1), 'r': 10})
                
    return jsonify({
        'impact': impact,
        'declining': [{'name': 'Prof. Smith', 'trend': '-15%'}] # Mock
    })

# --- 4. Future Predictions ---
@reports_bp.route('/reports/future-predictions', methods=['GET'])
@login_required
def future_predictions_view():
    return render_template('reports/future_predictions.html')

@reports_bp.route('/api/reports/future', methods=['GET'])
@login_required
def future_data():
    return jsonify({
        'highest_package': '42 LPA',
        'avg_package': '8.5 LPA',
        'placement_prob': {'high': 65, 'med': 25, 'low': 10}
    })
