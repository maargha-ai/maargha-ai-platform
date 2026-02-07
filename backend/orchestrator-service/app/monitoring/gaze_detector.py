# app/monitoring/gaze_detector.py
import base64
import cv2
import numpy as np
import mediapipe as mp

# Tasks API imports
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

# Path to the .task model you downloaded
MODEL_PATH = "app/monitoring/models/face_landmarker.task"

# Create the FaceLandmarker task (video/IMAGE mode depends on usage; we'll use IMAGE per-frame)
BaseOptions = mp.tasks.BaseOptions
FaceLandmarker = mp.tasks.vision.FaceLandmarker
FaceLandmarkerOptions = mp.tasks.vision.FaceLandmarkerOptions
VisionRunningMode = mp.tasks.vision.RunningMode

_options = FaceLandmarkerOptions(
    base_options=BaseOptions(model_asset_path=MODEL_PATH),
    running_mode=VisionRunningMode.IMAGE,
    num_faces=1
)

_landmarker = FaceLandmarker.create_from_options(_options)


def _decode_image(frame_base64: str):
    header, encoded = frame_base64.split(",", 1)
    data = base64.b64decode(encoded)
    arr = np.frombuffer(data, dtype=np.uint8)
    img = cv2.imdecode(arr, cv2.IMREAD_COLOR)
    return img


def is_looking_away(frame_b64: str) -> bool:
    """
    Returns True if the frame indicates 'looking away' or no-face.
    Uses FaceLandmarker to get landmarks; applies simple yaw/pitch heuristics.
    """
    img = _decode_image(frame_b64)
    if img is None:
        return True

    # Convert BGR -> RGB as MediaPipe expects RGB numpy array.
    rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # Create MediaPipe Image packet from numpy array (packet_creator helper)
    mp_image_packet = mp.packet_creator.create_image(rgb)

    # Run inference (image mode)
    try:
        result = _landmarker.detect(mp_image_packet)
    except Exception as e:
        # If the task fails for any reason, be conservative and treat as malpractice
        print("[gaze_detector] face landmarker error:", e)
        return True

    # No face detected -> malpractice
    if not result.face_landmarks:
        return True

    # Access landmarks (first face)
    face = result.face_landmarks[0]
    lm = face  # shorthand

    # Example landmark indices:
    # nose tip index may vary by model; typical example: use landmark 1 for nose in legacy
    # For Tasks FaceLandmarker, result.landmarks list contains coordinates.
    # We'll use left/right eye outer points and nose-ish point — tune as needed.

    # NOTE: adapt indices per model - this is a heuristic
    try:
        left_eye = lm[33]   # approximate landmark index (verify on your model)
        right_eye = lm[263]
        nose = lm[1]
    except Exception:
        # if indices not present, fallback to 'face present' = attentive
        return False

    # yaw approximation (horizontal eye separation change)
    yaw = abs(left_eye.x - right_eye.x)
    # pitch approximation from nose y (normalized)
    pitch = nose.y
    # thresholds — tune for your camera and distance
    if yaw < 0.03 or pitch > 0.62:
        print("-------------------------------")
        print("[Gaze Detector] Detection True")
        return True

    return False
