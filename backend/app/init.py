from flask import Flask
from flask_socketio import SocketIO
import eventlet
eventlet.monkey_patch()
from redis import Redis
import os

socketio = SocketIO(
    async_mode='eventlet',
    cors_allowed_origins="*",
    message_queue=os.getenv("REDIS_URL", None)  # Enables multi-worker real-time!
)

def create_app():
    app = Flask(__name__, template_folder="../../pwa/templates", static_folder="../../pwa/static")
    app.config['SECRET_KEY'] = 'change-me-to-something-very-strong'

    from .main import bp as main_bp
    app.register_blueprint(main_bp)

    socketio.init_app(app)
    return app, socketio
