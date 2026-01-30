from flask import render_template, request, flash, redirect, url_for
from flask_login import login_required
from app.extensions import db
from app.models import Exam, Attendance, StudentProfile
from datetime import datetime
from . import admin_bp


# --- Attendance Management ---
@admin_bp.route('/attendance')
@login_required
def attendance_list():
    records = Attendance.query.order_by(Attendance.date.desc()).all()
    return render_template('attendance_list.html', records=records)

@admin_bp.route('/attendance/mark', methods=['GET', 'POST'])
@login_required
def mark_attendance():
    students = StudentProfile.query.all()
    if request.method == 'POST':
        student_id = request.form.get('student_id')
        course_name = request.form.get('course_name')
        date_str = request.form.get('date')
        status = request.form.get('status')

        try:
            date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
            
            attendance = Attendance(
                student_id=student_id,
                course_name=course_name,
                date=date_obj,
                status=status
            )
            db.session.add(attendance)
            db.session.commit()
            flash('Attendance marked successfully!', 'success')
            return redirect(url_for('admin.attendance_list'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error marking attendance: {str(e)}', 'error')

    return render_template('attendance_add.html', students=students)
