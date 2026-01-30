from flask import render_template
from flask_login import login_required
from . import student_bp

@student_bp.route('/dashboard')
@login_required
def dashboard():
    return render_template('student/dashboard.html')
