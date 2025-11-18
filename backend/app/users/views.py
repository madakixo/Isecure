# User Dashboard + Register Camera


from flask import Blueprint, render_template, request, flash, redirect
from flask_login import login_required, current_user
from ..extensions import db
from ..models import Camera

user = Blueprint('user', __name__, url_prefix='/dashboard')

@user.route('/')
@login_required
def dashboard():
    if not current_user.is_active:
        flash('Your account is suspended or expired. Contact admin.')
        return redirect('/logout')
    cameras = Camera.query.filter_by(user_id=current_user.id).all()
    return render_template('user/dashboard.html', cameras=cameras)

@user.route('/add-camera', methods=['POST'])
@login_required
def add_camera():
    if len(current_user.cameras) >= current_user.cameras_allowed:
        flash('Upgrade your plan to add more cameras')
        return redirect('/dashboard')

    rtsp = f"rtsp://{request.form['username']}:{request.form['password']}@{request.form['ip']}:{request.form['port']}/Streaming/Channels/101"
    camera = Camera(
        name=request.form['name'],
        rtsp_url=rtsp,
        registered_ip=request.form['ip'],
        user_id=current_user.id
    )
    db.session.add(camera)
    db.session.commit()
    flash('Camera added successfully!')
    return redirect('/dashboard')
