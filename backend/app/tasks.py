from celery import Celery
import os
from datetime import datetime

celery = Celery(__name__, broker=os.getenv('REDIS_URL', 'redis://localhost:6379/0'))

@celery.task(name='save_unknown_face')
def save_unknown_face(face_bytes, bbox, cam_id):
    os.makedirs("/app/unknown_faces", exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    path = f"/app/unknown_faces/unknown_{cam_id}_{ts}.jpg"
    with open(path, "wb") as f:
        f.write(face_bytes)

@celery.task(name='backup_to_gdrive')
def backup_to_gdrive(face_bytes, cam_id):
    # Optional Google Drive upload (skip if no credentials)
    pass
