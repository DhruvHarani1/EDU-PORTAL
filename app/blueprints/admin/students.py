from flask import render_template, request, flash, redirect, url_for
from flask_login import login_required
from app.extensions import db
from app.models import User, StudentProfile
from . import admin_bp

@admin_bp.route('/students')
@login_required
def students_list():
    students = StudentProfile.query.all()
    return render_template('admin/students/list.html', students=students)

@admin_bp.route('/students/add', methods=['GET', 'POST'])
@login_required
def add_student():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        enrollment = request.form.get('enrollment_number')
        course = request.form.get('course_name')
        semester = request.form.get('semester')

        if User.query.filter_by(email=email).first():
            flash('Email already exists.', 'error')
            return redirect(url_for('admin.add_student'))

        try:
            # Create User
            user = User(email=email, role='student')
            user.set_password(password)
            db.session.add(user)
            db.session.flush() # Flush to get user.id

            # Create Profile
            student = StudentProfile(
                user_id=user.id,
                enrollment_number=enrollment,
                course_name=course,
                semester=semester
            )
            db.session.add(student)
            db.session.commit()
            flash('Student added successfully!', 'success')
            return redirect(url_for('admin.students_list'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error adding student: {str(e)}', 'error')

    return render_template('admin/students/add.html')
