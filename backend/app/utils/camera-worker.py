import cv2
import time
from flask_socketio import SocketIO
from .utils.yolo_detector import detect_and_recognize
from .tasks import save_unknown_face

class CameraStream:
    def __init__(self, rtsp_url, camera_id, socketio: SocketIO):
        self.url = rtsp_url
        self.id = camera_id
        self.socketio = socketio
        self.running = True

    def start(self):
        cap = cv2.VideoCapture(self.url)
        cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)

        while self.running:
            ret, frame = cap.read()
            if not ret:
                time.sleep(1)
                cap.open(self.url)
                continue

            processed_frame, detections = detect_and_recognize(frame)

            # Send JPEG to browser via Socket.IO
            _, buffer = cv2.imencode('.jpg', processed_frame, [int(cv2.IMWRITE_JPEG_QUALITY), 80])
            self.socketio.emit('frame', {
                'camera_id': self.id,
                'image': buffer.tobytes().hex(),
                'detections': detections
            })

            # Alert unknown
            for d in detections:
                if d['name'] == "Unknown":
                    save_unknown_face.delay(processed_frame[d['bbox'][1]:d['bbox'][3], d['bbox'][0]:d['bbox'][2]].tobytes(), d['bbox'])

            time.sleep(0.033)  # ~30 FPS
