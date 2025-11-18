# backend/create_app.py
from app import create_app as _create_app

def create_app():
    """
    Gunicorn looks for a callable named 'create_app' by default when using:
    gunicorn -c gunicorn.conf.py "create_app:create_app()"
    """
    app, socketio = _create_app()

    # Important: Wrap Socket.IO with the Flask app for Gunicorn + eventlet
    # This allows Socket.IO to work perfectly behind multiple workers
    from flask_socketio import SocketIO
    return socketio.run(app) if __name__ == "__main__" else app
