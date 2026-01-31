from flask import render_template, request
from flask_login import login_required
from datetime import datetime
from app.models import FeeRecord
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
