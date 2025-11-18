from ultralytics import YOLO
import insightface
import cv2
import numpy as np

# Global models (loaded once)
yolo_model = YOLO('/app/yolov8n-face.pt')  # download: ultralytics.com/models/yolov8n-face.pt
face_recognizer = insightface.app.FaceAnalysis(providers=['CUDAExecutionProvider', 'CPUExecutionProvider'])
face_recognizer.prepare(ctx_id=0 if torch.cuda.is_available() else -1)

known_encodings = {}  # name: np.array

def load_known_faces():
    import os
    from pathlib import Path
    for file in Path("/app/known_faces").glob("*.jpg"):
        img = cv2.imread(str(file))
        faces = face_recognizer.get(img)
        if faces:
            known_encodings[file.stem.replace("_", " ")] = faces[0].normed_embedding

def detect_and_recognize(frame):
    results = yolo_model(frame, conf=0.6, classes=[0])[0]
    detections = []
    for box in results.boxes:
        x1, y1, x2, y2 = map(int, box.xyxy[0])
        face_crop = frame[y1:y2, x1:x2]
        faces = face_recognizer.get(frame, bbox=[x1,y1,x2,y2])
        name = "Unknown"
        if faces and len(faces) > 0:
            emb = faces[0].normed_embedding
            for known_name, known_emb in known_encodings.items():
                dist = np.linalg.norm(emb - known_emb)
                if dist < 0.45:  # tight threshold
                    name = known_name
                    break
        detections.append({
            "bbox": [x1,y1,x2,y2],
            "name": name,
            "confidence": float(box.conf)
        })
        # Draw
        color = (0,255,0) if name != "Unknown" else (0,0,255)
        cv2.rectangle(frame, (x1,y1), (x2,y2), color, 2)
        cv2.putText(frame, name, (x1,y1-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)
    return frame, detections
