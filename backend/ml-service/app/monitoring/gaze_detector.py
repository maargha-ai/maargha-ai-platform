# app/gaze_detector.py
import base64
from typing import Optional

import cv2
import mediapipe as mp
import numpy as np

# Tasks API imports
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

MODEL_PATH = "app/monitoring/models/face_landmarker.task"

BaseOptions = mp.tasks.BaseOptions
FaceLandmarker = mp.tasks.vision.FaceLandmarker
FaceLandmarkerOptions = mp.tasks.vision.FaceLandmarkerOptions
VisionRunningMode = mp.tasks.vision.RunningMode

_landmarker: Optional[FaceLandmarker] = None


def _get_landmarker() -> Optional[FaceLandmarker]:
    """Get or create landmarker lazily, return None if model file missing"""
    global _landmarker
    if _landmarker is None:
        try:
            options = FaceLandmarkerOptions(
                base_options=BaseOptions(model_asset_path=MODEL_PATH),
                running_mode=VisionRunningMode.IMAGE,
                num_faces=1,
            )
            _landmarker = FaceLandmarker.create_from_options(options)
        except (FileNotFoundError, Exception):
            # Model file not found or other error
            return None
    return _landmarker


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
    landmarker = _get_landmarker()
    if landmarker is None:
        # Model not available, assume user is looking (no malpractice)
        return False
        
    img = _decode_image(frame_b64)
    if img is None:
        return True

    rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # Create MediaPipe Image object properly
    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb)

    try:
        result = landmarker.detect(mp_image)
    except Exception as e:
        # Model hiccup on a single frame should not trigger malpractice.
        print(f"MediaPipe detection error: {e}")
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
    except Exception as e:
        print(f"Error accessing landmarks: {e}")
        return False

    # Face box too small -> likely far/out of frame
    xs = [p.x for p in lm]
    ys = [p.y for p in lm]
    face_w = max(xs) - min(xs)
    face_h = max(ys) - min(ys)
    face_area = face_w * face_h

    # More sensitive face area threshold (increased from 0.008)
    if face_area < 0.012:
        return True

    # Check if face is too close to edges (partial face view)
    min_x = min(xs)
    max_x = max(xs)
    min_y = min(ys)
    max_y = max(ys)

    # Face too close to any edge indicates partial view
    if min_x < 0.05 or max_x > 0.95 or min_y < 0.05 or max_y > 0.95:
        return True

    # Eye openness ratio (very low on both eyes means closed/covered/not visible)
    left_eye_h = np.linalg.norm(
        np.array([left_upper.x, left_upper.y]) - np.array([left_lower.x, left_lower.y])
    )
    left_eye_w = np.linalg.norm(
        np.array([left_eye_outer.x, left_eye_outer.y])
        - np.array([left_eye_inner.x, left_eye_inner.y])
    )
    right_eye_h = np.linalg.norm(
        np.array([right_upper.x, right_upper.y])
        - np.array([right_lower.x, right_lower.y])
    )
    right_eye_w = np.linalg.norm(
        np.array([right_eye_outer.x, right_eye_outer.y])
        - np.array([right_eye_inner.x, right_eye_inner.y])
    )

    left_ratio = left_eye_h / max(left_eye_w, 1e-6)
    right_ratio = right_eye_h / max(right_eye_w, 1e-6)
    eyes_hidden = left_ratio < 0.045 and right_ratio < 0.045
    eyes_hidden_strong = left_ratio < 0.02 and right_ratio < 0.02

    # Very small inter-eye distance -> extreme yaw / partial face
    eye_center_left = np.array(
        [
            (left_eye_outer.x + left_eye_inner.x) / 2,
            (left_eye_outer.y + left_eye_inner.y) / 2,
        ]
    )
    eye_center_right = np.array(
        [
            (right_eye_outer.x + right_eye_inner.x) / 2,
            (right_eye_outer.y + right_eye_inner.y) / 2,
        ]
    )
    inter_eye = np.linalg.norm(eye_center_left - eye_center_right)
    head_turned = inter_eye < 0.04

    # More sensitive nose off-center detection (expanded thresholds)
    off_center = nose.x < 0.20 or nose.x > 0.80 or nose.y < 0.10 or nose.y > 0.90

    # Strong eye occlusion signal.
    if eyes_hidden_strong:
        return True

    # More aggressive detection - any single condition should trigger
    if eyes_hidden:
        return True
    if head_turned:
        return True
    if off_center:
        return True

    # Combined conditions for higher confidence
    if eyes_hidden and off_center:
        return True
    if head_turned and off_center:
        return True

    return False
