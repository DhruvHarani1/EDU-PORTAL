from flask import render_template, request, flash, redirect, url_for
from flask_login import login_required
from app.extensions import db
from app.models import Notice, FacultyProfile, StudentProfile
from . import admin_bp

@admin_bp.route('/notices')
@login_required
def notices_list():
    notices = Notice.query.order_by(Notice.created_at.desc()).all()
    return render_template('notices_list.html', notices=notices)

@admin_bp.route('/notices/add', methods=['GET', 'POST'])
@login_required
def add_notice():
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        category = request.form.get('category')
        
        target_course = None
        target_faculty_id = None
        
        if category == 'course':
             target_course = request.form.get('target_course')
        elif category == 'faculty':
             target_faculty_id = request.form.get('target_faculty_id')
        
        try:
            notice = Notice(
                title=title,
                content=content,
                category=category,
                target_course=target_course,
                target_faculty_id=target_faculty_id
            )
            db.session.add(notice)
            db.session.commit()
            flash('Notice published successfully!', 'success')
            return redirect(url_for('admin.notices_list'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error adding notice: {str(e)}', 'error')
            
    # Get faculty list for the dropdown
    faculty_members = FacultyProfile.query.all()
    # Get distinct courses
    courses = db.session.query(StudentProfile.course_name).distinct().all()
    courses = [c[0] for c in courses]
    
    return render_template('notice_add.html', faculty_members=faculty_members, courses=courses)
