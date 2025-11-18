#Flask + SocketIO App 


from flask import Flask, render_template, request
from flask_socketio import SocketIO
from .camera_worker import CameraStream
import os

def create_app():
    app = Flask(__name__, template_folder="../../pwa/templates", static_folder="../../pwa/static")
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret')

    socketio = SocketIO(app, cors_allowed_origins="*", async_mode='eventlet')

    cameras = {}

    @app.route('/')
    def index():
        return render_template('index.html')

    @socketio.on('add_camera')
    def add_camera(data):
        rtsp = data['rtsp']
        cam_id = data['id']
        if cam_id not in cameras:
            stream = CameraStream(rtsp, cam_id, socketio)
            cameras[cam_id] = stream
            stream.start()

    return app, socketio
