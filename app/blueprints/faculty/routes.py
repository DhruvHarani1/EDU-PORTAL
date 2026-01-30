from flask import render_template
from flask_login import login_required
from . import faculty_bp

@faculty_bp.route('/dashboard')
@login_required
def dashboard():
    return render_template('faculty/dashboard.html')
