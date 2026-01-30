from flask import render_template, request, flash, redirect, url_for
from flask_login import login_required
from app.extensions import db
from app.models import User, FacultyProfile
from . import admin_bp

@admin_bp.route('/faculty')
@login_required
def faculty_list():
    faculty_members = FacultyProfile.query.all()
    return render_template('admin/faculty/list.html', faculty_members=faculty_members)

@admin_bp.route('/faculty/add', methods=['GET', 'POST'])
@login_required
def add_faculty():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        designation = request.form.get('designation')
        department = request.form.get('department')

        if User.query.filter_by(email=email).first():
            flash('Email already exists.', 'error')
            return redirect(url_for('admin.add_faculty'))

        try:
            # Create User
            user = User(email=email, role='faculty')
            user.set_password(password)
            db.session.add(user)
            db.session.flush()

            # Create Profile
            faculty = FacultyProfile(
                user_id=user.id,
                designation=designation,
                department=department
            )
            db.session.add(faculty)
            db.session.commit()
            flash('Faculty added successfully!', 'success')
            return redirect(url_for('admin.faculty_list'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error adding faculty: {str(e)}', 'error')

    return render_template('admin/faculty/add.html')
