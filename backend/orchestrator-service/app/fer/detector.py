import cv2
import os
import time
from ultralytics import YOLO
from app.fer.emotion_buffer import push_emotion
from app.fer.active_user import get_active_user

# Load model
RUN_NAME = "facial_emotion_fer2013_v12"
model_path = os.path.join(
    "app", "fer", "runs", "classify", RUN_NAME, "weights", "best.pt"
)
emotion_model = YOLO(model_path)

# Face detection
face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)
emotion_classes = emotion_model.names


def start_camera_loop(stop_event):
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("[FER] Webcam not accessible")
        return

    print("[FER] Camera started")

    try:
        while not stop_event.is_set():
            print("[FER] Loop tick")
            ret, frame = cap.read()
            if not ret:
                continue

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(
                gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30)
            )
            print("[FER] Faces detected:", len(faces))

            user_id = get_active_user()
            if not user_id:
                time.sleep(0.2)
                continue

            for (x, y, w, h) in faces:
                face_roi = gray[y:y + h, x:x + w]
                resized = cv2.resize(face_roi, (48, 48))
                input_face = cv2.cvtColor(resized, cv2.COLOR_GRAY2BGR)

                results = emotion_model.predict(input_face, verbose=False)
                probs = results[0].probs

                emotion_id = probs.top1
                confidence = float(probs.top1conf)
                emotion = emotion_classes[emotion_id]
                
                print("[FER] Emotion:", emotion, "Confidence:", confidence)

                # ✅ STORE emotion with user_id
                push_emotion(user_id, emotion, confidence)

            time.sleep(0.2)

    finally:
        cap.release()
        print("[FER] Camera stopped")
