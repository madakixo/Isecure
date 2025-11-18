from flask import Flask
from flask_socketio import SocketIO
import eventlet
eventlet.monkey_patch()
from redis import Redis
import os

def create_app():
    app = Flask(__name__, template_folder="../../pwa/templates", static_folder="../../pwa/static")
    app.config['SECRET_KEY'] = 'change-me-to-something-very-strong'

    from .main import bp as main_bp
    app.register_blueprint(main_bp)

    socketio.init_app(app)
    return app, socketio


@app.cli.command("create-admin")
def create_admin():
    admin = User(username='admin', email='admin@secureeye.com', is_admin=True, plan='pro', cameras_allowed=999)
    admin.set_password('SuperStrongPassword2025')
    db.session.add(admin)
    db.session.commit()
    print("Admin created: admin@secureeye.com / SuperStrongPassword2025")
socketio = SocketIO(
    async_mode='eventlet',
    cors_allowed_origins="*",
    message_queue=os.getenv("REDIS_URL", None)  # Enables multi-worker real-time!
)
