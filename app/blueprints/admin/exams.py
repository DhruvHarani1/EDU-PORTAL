from flask import render_template, request, flash, redirect, url_for
from flask_login import login_required
from app.extensions import db
from app.models import Exam
from datetime import datetime
from . import admin_bp

@admin_bp.route('/exams')
@login_required
def exams_list():
    exams = Exam.query.order_by(Exam.date.asc()).all()
    return render_template('admin/exams/list.html', exams=exams)

@admin_bp.route('/exams/add', methods=['GET', 'POST'])
@login_required
def add_exam():
    if request.method == 'POST':
        course_name = request.form.get('course_name')
        date_str = request.form.get('date')
        time_str = request.form.get('time')
        duration = request.form.get('duration')
        location = request.form.get('location')

        try:
            date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
            time_obj = datetime.strptime(time_str, '%H:%M').time()
            
            exam = Exam(
                course_name=course_name, 
                date=date_obj, 
                time=time_obj, 
                duration_minutes=duration,
                location=location
            )
            db.session.add(exam)
            db.session.commit()
            flash('Exam scheduled successfully!', 'success')
            return redirect(url_for('admin.exams_list'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error scheduling exam: {str(e)}', 'error')

    return render_template('admin/exams/add.html')
