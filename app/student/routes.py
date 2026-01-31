from flask import render_template
from flask_login import login_required
from . import student_bp

@student_bp.route('/dashboard')
@login_required
def dashboard():
    return render_template('student_dashboard.html')

# Placeholder Routes for Sidebar Navigation
@student_bp.route('/attendance')
@login_required
def attendance():
    return render_template('student_dashboard.html') # TODO: Create attendance.html

@student_bp.route('/academics')
@login_required
def academics():
    return render_template('student_dashboard.html') # TODO: Create academics.html

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
