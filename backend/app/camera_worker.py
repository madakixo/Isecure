import threading
import cv2
import time
from .utils.yolo_detector import detect_and_recognize, load_known_faces_once
from .tasks import save_unknown_face, backup_to_gdrive

def camera_loop(rtsp_url, cam_id, socketio):
    load_known_faces_once()
    cap = cv2.VideoCapture(rtsp_url)
    cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)

    while True:
        ret, frame = cap.read()
        if not ret:
            time.sleep(2)
            cap = cv2.VideoCapture(rtsp_url)
            continue

        annotated_frame, detections = detect_and_recognize(frame)

        _, jpeg = cv2.imencode('.jpg', annotated_frame, [int(cv2.IMWRITE_JPEG_QUALITY), 75])
        socketio.emit('newframe', {
            'cam_id': cam_id,
            'image': jpeg.tobytes().hex(),
            'detections': detections
        })

        for det in detections:
            if det['name'] == 'Unknown':
                crop = frame[det['bbox'][1]:det['bbox'][3], det['bbox'][0]:det['bbox'][2]]
                save_unknown_face.delay(crop.tobytes(), det['bbox'], cam_id)
                backup_to_gdrive.delay(crop.tobytes(), cam_id)

        time.sleep(0.04)  # 25 FPS max per camera

def start_camera_thread(rtsp_url, cam_id, socketio):
    t = threading.Thread(target=camera_loop, args=(rtsp_url, cam_id, socketio), daemon=True)
    t.start()
