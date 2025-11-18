from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from ..extensions import db
from ..models import User, Camera
from datetime import datetime, timedelta

admin = Blueprint('admin', __name__, url_prefix='/admin')

@admin.before_request
@login_required
def restrict_to_admin():
    if not current_user.is_admin:
        flash('Admin access only')
        return redirect('/')

@admin.route('/')
def dashboard():
    users = User.query.all()
    total = User.query.count()
    paying = User.query.filter(User.plan != 'free').count()
    suspended = User.query.filter_by(suspended=True).count()
    return render_template('admin/dashboard.html', users=users, total=total, paying=paying, suspended=suspended)

@admin.route('/user/<int:user_id>/toggle')
def toggle_user(user_id):
    user = User.query.get_or_404(user_id)
    user.suspended = not user.suspended
    db.session.commit()
    flash(f"User {user.username} {'suspended' if user.suspended else 'activated'}")
    return redirect(url_for('admin.dashboard'))

@admin.route('/user/<int:user_id>/extend', methods=['POST'])
def extend_subscription(user_id):
    user = User.query.get_or_404(user_id)
    days = int(request.form['days'])
    user.active_until = datetime.utcnow() + timedelta(days=days)
    user.suspended = False
    db.session.commit()
    flash(f"Extended {days} days for {user.username}")
    return redirect(url_for('admin.dashboard'))
