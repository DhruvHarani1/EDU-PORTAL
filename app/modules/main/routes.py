from flask import render_template
from . import main_bp

@main_bp.route('/')
def index():
    return render_template('index.html')

@main_bp.route('/features/student')
def features_student():
    return render_template('features_student.html')

@main_bp.route('/features/faculty')
def features_faculty():
    return render_template('features_faculty.html')

@main_bp.route('/features/admin')
def features_admin():
    return render_template('features_admin.html')
