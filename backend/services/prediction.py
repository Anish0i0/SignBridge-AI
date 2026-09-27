"""
SignBridge AI - Part 4: Prediction Service
Takes a raw image, runs the SAME MediaPipe hand-detection and
normalization pipeline used in Part 1, and returns the 63-feature
vector ready for the ML model.
"""

import cv2
import numpy as np
import mediapipe as mp

mp_hands = mp.solutions.hands

# Same settings as Part 1 / Part 2 data collection
hands = mp_hands.Hands(
    static_image_mode=True,       # True: each call is treated as an independent image (no video tracking state)
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.5
)


def extract_normalized_landmarks(image_bgr):
    """
    Takes a BGR image (as read by OpenCV), detects a hand, and returns
    a flat list of 63 normalized features (same method as Part 1/2),
    or None if no hand is detected.
    """
    rgb_image = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_image)

    if not results.multi_hand_landmarks:
        return None

    # Only one hand expected (max_num_hands=1)
    hand_landmarks = results.multi_hand_landmarks[0]

    landmark_list = [(lm.x, lm.y, lm.z) for lm in hand_landmarks.landmark]
    wrist_x, wrist_y, wrist_z = landmark_list[0]

    normalized = []
    for (x, y, z) in landmark_list:
        normalized.extend([x - wrist_x, y - wrist_y, z - wrist_z])

    return normalized  # flat list of 63 numbers


def predict_sign(model, image_bgr):
    """
    Full pipeline: image -> landmarks -> normalization -> model prediction.
    Returns a dict with success/prediction/confidence, or an explanatory message.
    """
    features = extract_normalized_landmarks(image_bgr)

    if features is None:
        return {"success": False, "message": "No hand detected"}

    features_array = np.array(features).reshape(1, -1)  # model expects shape (1, 63)

    prediction = model.predict(features_array)[0]
    probabilities = model.predict_proba(features_array)[0]
    confidence = float(np.max(probabilities))

    return {
        "success": True,
        "prediction": str(prediction),
        "confidence": round(confidence, 4)
    }