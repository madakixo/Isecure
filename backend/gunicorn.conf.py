# backend/gunicorn.conf.py
import multiprocessing
import os

# Bind to port 8000 inside the container
bind = "0.0.0.0:8000"

# Optimal workers: (2 x CPU cores) + 1
workers = multiprocessing.cpu_count() * 2 + 1

# Use eventlet worker for Socket.IO real-time performance
worker_class = "eventlet"

# Maximum connections per worker (for Socket.IO)
worker_connections = 1000

# Restart workers after this many requests (prevents memory leaks)
max_requests = 1000
max_requests_jitter = 100

# Timeout
timeout = 120
keepalive = 5

# Logging
accesslog = "-"
errorlog = "-"
loglevel = "info"

# Preload app to share YOLO/InsightFace models in memory (huge RAM + speed win)
preload_app = True

# Optional: Run as specific user/group inside container
# uid = "nobody"
# gid = "nogroup"
