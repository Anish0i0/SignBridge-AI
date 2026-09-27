"""
SignBridge AI - Part 1: Hand Detection Module
Detects a single hand via webcam using MediaPipe, draws the 21 landmarks,
extracts their x, y, z coordinates, and normalizes them relative to the wrist.
"""

import cv2
import mediapipe as mp

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

hands = mp_hands.Hands(
    static_image_mode=False,      # False = treat input as a video stream (faster, tracks between frames)
    max_num_hands=1,              # Only detect one hand (SignBridge AI Part 1 scope)
    min_detection_confidence=0.7, # Confidence threshold to first detect a hand
    min_tracking_confidence=0.5   # Confidence threshold to keep tracking an already-detected hand
)

# Open the webcam
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()

print("Hand detection started. Press 'q' to quit.")

frame_count = 0  # used to limit how often we print to the terminal

while True:
    ret, frame = cap.read()

    if not ret:
        print("Error: Failed to grab frame.")
        break

    # Flip the frame horizontally for a mirror-like view
    frame = cv2.flip(frame, 1)

    # MediaPipe expects RGB images, but OpenCV gives us BGR
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Run hand detection
    results = hands.process(rgb_frame)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            # Draw the landmarks and connections on the frame
            mp_drawing.draw_landmarks(
                frame,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS
            )

            # Extract x, y, z for each of the 21 landmarks
            landmark_list = [(lm.x, lm.y, lm.z) for lm in hand_landmarks.landmark]

            # Normalize landmarks relative to the wrist (landmark 0)
            wrist_x, wrist_y, wrist_z = landmark_list[0]
            normalized_landmarks = [
                (x - wrist_x, y - wrist_y, z - wrist_z)
                for (x, y, z) in landmark_list
            ]

            # Print status every 30 frames (~once a second) instead of every frame
            frame_count += 1
            if frame_count % 30 == 0:
                print(f"Landmarks: {len(normalized_landmarks)} | Index fingertip (normalized): {normalized_landmarks[8]}")

    # Show the video feed with landmarks drawn on it
    cv2.imshow("SignBridge AI - Hand Detection", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()