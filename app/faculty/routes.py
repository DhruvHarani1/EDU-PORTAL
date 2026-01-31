from flask import render_template, request
from flask_login import login_required
from datetime import datetime
from app.models import FeeRecord, StudentQuery, QueryMessage, FacultyProfile
from flask_login import current_user, login_required
from flask import render_template, request, redirect, url_for, flash
from app.extensions import db
from . import faculty_bp

@faculty_bp.route('/dashboard')
@login_required
def dashboard():
    return render_template('faculty_dashboard.html')

@faculty_bp.route('/fees')
@login_required
def fees():
    # Fetch all fee records (In a real app, filter by faculty's students)
    records = FeeRecord.query.order_by(FeeRecord.due_date.desc()).all()
    return render_template('faculty/fees.html', records=records)

@faculty_bp.route('/fees/mark_paid/<int:fee_id>', methods=['POST'])
@login_required
def mark_paid(fee_id):
    fee = FeeRecord.query.get_or_404(fee_id)
    fee.status = 'Paid'
    fee.payment_date = datetime.utcnow()
    fee.payment_mode = 'Cash/Office'
    fee.transaction_reference = f"OFFICE-MANUAL-{fee.id}-{int(datetime.utcnow().timestamp())}"
    db.session.commit()
    return {'status': 'success'}

@faculty_bp.route('/queries')
@login_required
def queries():
    faculty = FacultyProfile.query.filter_by(user_id=current_user.id).first_or_404()
    
    # Check for filters
    status = request.args.get('status', 'all')
    
    query = StudentQuery.query.filter_by(faculty_id=faculty.id)
    if status != 'all':
        query = query.filter_by(status=status.capitalize())
        
    queries = query.order_by(StudentQuery.updated_at.desc()).all()
    
    return render_template('faculty/queries.html', queries=queries, filter=status)

@faculty_bp.route('/queries/<int:query_id>', methods=['GET', 'POST'])
@login_required
def query_chat(query_id):
    faculty = FacultyProfile.query.filter_by(user_id=current_user.id).first_or_404()
    query = StudentQuery.query.get_or_404(query_id)
    
    if query.faculty_id != faculty.id:
        return "Unauthorized", 403

    if request.method == 'POST':
        content = request.form.get('content')
        if content:
            msg = QueryMessage(
                query_id=query.id,
                sender_type='faculty',
                content=content
            )
            db.session.add(msg)
            
            # Update status to Answered
            if query.status == 'Pending':
                 query.status = 'Answered'
            
            query.updated_at = datetime.utcnow()
            db.session.commit()
            return redirect(url_for('faculty.query_chat', query_id=query_id))

    return render_template('faculty/query_chat.html', query=query)
