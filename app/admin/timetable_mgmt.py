from flask import render_template, request, flash, redirect, url_for, jsonify
from flask_login import login_required
from app.extensions import db
from app.models import Subject, Timetable, FacultyProfile, StudentProfile
from . import admin_bp
import random
import math

@admin_bp.route('/timetable', methods=['GET'])
@login_required
def timetable_landing():
    # step 1: Select Course and Semester
    courses = db.session.query(StudentProfile.course_name).distinct().all()
    courses = [c[0] for c in courses]
    return render_template('timetable_landing.html', courses=courses)

@admin_bp.route('/timetable/setup', methods=['GET', 'POST'])
@login_required
def timetable_setup():
    course = request.args.get('course') or request.form.get('course')
    semester = request.args.get('semester') or request.form.get('semester')
    
    if not course or not semester:
        flash('Please select course and semester.', 'error')
        return redirect(url_for('admin.timetable_landing'))

    semester = int(semester)
    
    # Fetch existing subjects
    subjects = Subject.query.filter_by(course_name=course, semester=semester).all()
    faculty_members = FacultyProfile.query.all()
    
    return render_template('timetable_setup.html', 
                           course=course, 
                           semester=semester, 
                           subjects=subjects, 
                           faculty_members=faculty_members)

@admin_bp.route('/timetable/add_subject', methods=['POST'])
@login_required
def add_subject():
    # Helper to add subject via AJAX or Form
    course = request.form.get('course')
    semester = request.form.get('semester')
    name = request.form.get('name')
    faculty_id = request.form.get('faculty_id')
    lectures = request.form.get('lectures')
    
    try:
        subject = Subject(
            name=name,
            course_name=course,
            semester=semester,
            faculty_id=faculty_id,
            weekly_lectures=lectures
        )
        db.session.add(subject)
        db.session.commit()
        flash('Subject added successfully', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error adding subject: {e}', 'error')
        
    return redirect(url_for('admin.timetable_setup', course=course, semester=semester))

@admin_bp.route('/timetable/generate', methods=['POST'])
@login_required
def generate_timetable():
    course = request.form.get('course')
    semester = int(request.form.get('semester'))
    days_per_week = int(request.form.get('days_per_week', 5)) # Default 5
    slots_per_day = int(request.form.get('slots_per_day', 8)) # Default 8
    
    # 1. Clear existing timetable for this course/sem
    Timetable.query.filter_by(course_name=course, semester=semester).delete()
    
    # 2. Get Subjects
    subjects = Subject.query.filter_by(course_name=course, semester=semester).all()
    
    # 3. Simple Greedy Allocation (Proof of Concept)
    # A real algorithm would use backtracking/CSP, but let's start with a simpler filling strategy
    # to ensure we produce a valid result first.
    
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'][:days_per_week]
    total_slots = days_per_week * slots_per_day
    
    # Create a pool of "Subject Instances" based on weekly_lectures
    pool = []
    
    # 1. Add minimum required lectures
    for sub in subjects:
        for _ in range(sub.weekly_lectures):
            pool.append(sub)
            
    # 2. FILL LOGIC: If pool is smaller than total slots, keep adding subjects
    # We cycle through subjects to distribute the extra load evenly
    if subjects and len(pool) < total_slots:
        while len(pool) < total_slots:
             for sub in subjects:
                 if len(pool) >= total_slots:
                     break
                 pool.append(sub)
            
    # Shuffle for randomness
    random.shuffle(pool)
    
    # Calculate constraints
    # If we have 20 instances of Math over 5 days, we need approx 4 per day.
    # Set limit to ceil(count / days) + 1 (buffer)
    subject_daily_limits = {}
    for sub in subjects:
        count = pool.count(sub)
        subject_daily_limits[sub.id] = math.ceil(count / days_per_week)
    
    # Initialize grid tracking
    # mapping: day -> period -> subject
    schedule = {day: {p: None for p in range(1, slots_per_day + 1)} for day in days}
    
    # ... (Faculty Busy check logic would be same)
    
    # Attempt to place
    unplaced = []
    
    for item in pool:
        placed = False
        # Try to find a slot
        for day in days:
            if placed: break
            
            # Count lectures of this subject on this day
            daily_count = sum(1 for p in range(1, slots_per_day+1) 
                              if schedule[day][p] and schedule[day][p].id == item.id)
            
            # Dynamic Limit Check
            limit = subject_daily_limits.get(item.id, 2)
            if daily_count >= limit:
                continue 
                
            for period in range(1, slots_per_day + 1):
                # Check if empty
                if schedule[day][period] is None:
                    # Check Faculty Availability (Global check would go here)
                    # For now, assume free if local grid is free
                    
                    schedule[day][period] = item
                    placed = True
                    break
        
        if not placed:
            unplaced.append(item.name)
            
    # 4. Save to DB
    for day in days:
        for period in range(1, slots_per_day + 1):
            sub = schedule[day][period]
            if sub:
                slot = Timetable(
                    course_name=course,
                    semester=semester,
                    day_of_week=day,
                    period_number=period,
                    subject_id=sub.id,
                    faculty_id=sub.faculty_id
                )
                db.session.add(slot)
    
    db.session.commit()
    
    if unplaced:
        flash(f"Warning: Could not place {len(unplaced)} lectures due to constraints.", 'warning')
    else:
        flash('Timetable generated successfully!', 'success')
        
    return redirect(url_for('admin.view_timetable', course=course, semester=semester))

@admin_bp.route('/timetable/view', methods=['GET', 'POST'])
@login_required
def view_timetable():
    course = request.args.get('course')
    semester = request.args.get('semester')
    
    if not course or not semester:
        return redirect(url_for('admin.timetable_landing'))
        
    slots = Timetable.query.filter_by(course_name=course, semester=int(semester)).all()
    
    # Structure for Template: Grid[Day][Period] = Slot
    # Determine max period to render grid correctly
    max_period = 8
    if slots:
        max_period = max([s.period_number for s in slots] + [8])
        
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
    # Filter days that actually have slots or default to Mon-Fri
    active_days = set([s.day_of_week for s in slots]) 
    if not active_days:
        # Default view
        grid_days = days[:5]
    else:
         # Keep order
         grid_days = [d for d in days if d in active_days]
         if len(grid_days) < 5: grid_days = days[:5] # Min 5 days view
    
    grid = {day: {p: None for p in range(1, max_period + 1)} for day in grid_days}
    
    for s in slots:
        if s.day_of_week in grid and s.period_number in grid[s.day_of_week]:
            grid[s.day_of_week][s.period_number] = s
            
    # For Edit Mode: Need list of subjects to populate dropdowns
    subjects = Subject.query.filter_by(course_name=course, semester=int(semester)).all()

    # Handle Edit Saving
    if request.method == 'POST':
        # Logic to update specific slot
        # Expecting JSON or Form data: slot_day_period = subject_id
        pass

    return render_template('timetable_view.html', 
                           grid=grid, 
                           days=grid_days, 
                           periods=range(1, max_period+1),
                           course=course,
                           semester=semester,
                           subjects=subjects)

@admin_bp.route('/timetable/update_slot', methods=['POST'])
@login_required
def update_slot():
    # AJAX Endpoint for drag-drop or dropdown change
    data = request.json
    slot_id = data.get('slot_id') # If editing existing
    day = data.get('day')
    period = data.get('period')
    subject_id = data.get('subject_id')
    course = data.get('course')
    semester = data.get('semester')
    
    if not subject_id:
        # Clear slot
        if slot_id:
            Timetable.query.filter_by(id=slot_id).delete()
    else:
        subject = Subject.query.get(subject_id)
        if slot_id:
            slot = Timetable.query.get(slot_id)
            slot.subject_id = subject_id
            slot.faculty_id = subject.faculty_id
        else:
            # Create new
            slot = Timetable(
                course_name=course,
                semester=semester,
                day_of_week=day,
                period_number=period,
                subject_id=subject_id,
                faculty_id=subject.faculty_id
            )
            db.session.add(slot)
            
    db.session.commit()
    return jsonify({'status': 'success'})
