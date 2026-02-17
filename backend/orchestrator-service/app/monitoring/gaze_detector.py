# app/monitoring/gaze_detector.py
import base64
import cv2
import numpy as np
import mediapipe as mp

# Tasks API imports
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

MODEL_PATH = "app/monitoring/models/face_landmarker.task"

BaseOptions = mp.tasks.BaseOptions
FaceLandmarker = mp.tasks.vision.FaceLandmarker
FaceLandmarkerOptions = mp.tasks.vision.FaceLandmarkerOptions
VisionRunningMode = mp.tasks.vision.RunningMode

_options = FaceLandmarkerOptions(
    base_options=BaseOptions(model_asset_path=MODEL_PATH),
    running_mode=VisionRunningMode.IMAGE,
    num_faces=1,
)

_landmarker = FaceLandmarker.create_from_options(_options)


def _decode_image(frame_base64: str):
    _, encoded = frame_base64.split(",", 1)
    data = base64.b64decode(encoded)
    arr = np.frombuffer(data, dtype=np.uint8)
    img = cv2.imdecode(arr, cv2.IMREAD_COLOR)
    return img


def is_looking_away(frame_b64: str) -> bool:
    """
    True => malpractice suspected (face not visible / off screen / eyes not visible).
    """
    img = _decode_image(frame_b64)
    if img is None:
        return True

    rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    mp_image_packet = mp.packet_creator.create_image(rgb)

    try:
        result = _landmarker.detect(mp_image_packet)
    except Exception:
        # Model hiccup on a single frame should not trigger malpractice.
        return False

    if not result.face_landmarks:
        return True

    lm = result.face_landmarks[0]

    try:
        left_eye_outer = lm[33]
        left_eye_inner = lm[133]
        right_eye_inner = lm[362]
        right_eye_outer = lm[263]
        left_upper = lm[159]
        left_lower = lm[145]
        right_upper = lm[386]
        right_lower = lm[374]
        nose = lm[1]
    except Exception:
        return False

    # Face box too small -> likely far/out of frame
    xs = [p.x for p in lm]
    ys = [p.y for p in lm]
    face_w = max(xs) - min(xs)
    face_h = max(ys) - min(ys)
    face_area = face_w * face_h
    if face_area < 0.008:
        return True

    # Eye openness ratio (very low on both eyes means closed/covered/not visible)
    left_eye_h = np.linalg.norm(np.array([left_upper.x, left_upper.y]) - np.array([left_lower.x, left_lower.y]))
    left_eye_w = np.linalg.norm(np.array([left_eye_outer.x, left_eye_outer.y]) - np.array([left_eye_inner.x, left_eye_inner.y]))
    right_eye_h = np.linalg.norm(np.array([right_upper.x, right_upper.y]) - np.array([right_lower.x, right_lower.y]))
    right_eye_w = np.linalg.norm(np.array([right_eye_outer.x, right_eye_outer.y]) - np.array([right_eye_inner.x, right_eye_inner.y]))

    left_ratio = left_eye_h / max(left_eye_w, 1e-6)
    right_ratio = right_eye_h / max(right_eye_w, 1e-6)
    eyes_hidden = left_ratio < 0.045 and right_ratio < 0.045
    eyes_hidden_strong = left_ratio < 0.02 and right_ratio < 0.02

    # Very small inter-eye distance -> extreme yaw / partial face
    eye_center_left = np.array([(left_eye_outer.x + left_eye_inner.x) / 2, (left_eye_outer.y + left_eye_inner.y) / 2])
    eye_center_right = np.array([(right_eye_outer.x + right_eye_inner.x) / 2, (right_eye_outer.y + right_eye_inner.y) / 2])
    inter_eye = np.linalg.norm(eye_center_left - eye_center_right)
    head_turned = inter_eye < 0.04

    # Nose off-center -> looking away or mostly out of frame
    off_center = nose.x < 0.14 or nose.x > 0.86 or nose.y < 0.08 or nose.y > 0.92

    # Strong eye occlusion signal.
    if eyes_hidden_strong:
        return True

    # Medium-confidence conditions require corroboration to avoid false positives.
    if eyes_hidden and off_center:
        return True
    if head_turned and off_center:
        return True

    return False
