from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_user, logout_user, login_required, current_user
from ..extensions import db
from ..models import User

auth = Blueprint('auth', __name__)

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        if User.query.filter_by(email=email).first():
            flash('Email already registered')
            return redirect(url_for('auth.register'))
        user = User(username=username, email=email, plan='basic', cameras_allowed=5, active_until=datetime.utcnow() + timedelta(days=30))
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        flash('Registration successful! You have 30 days free.')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html')

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(email=request.form['email']).first()
        if user and user.check_password(request.form['password']) and user.is_active:
            login_user(user)
            return redirect(url_for('user.dashboard'))
        flash('Invalid credentials or account suspended')
    return render_template('auth/login.html')

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
