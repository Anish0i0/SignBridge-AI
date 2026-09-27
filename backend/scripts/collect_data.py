"""
SignBridge AI - Part 2: Dataset Collection
Captures normalized hand-landmark features via webcam and saves them,
along with a gesture label, into dataset/landmarks.csv.

Controls:
    SPACE -> capture one sample for the current class
    N     -> move to the next class
    Q     -> quit
"""

import cv2
import mediapipe as mp
import csv
import os

# ---------------------------------------------------------
# CONFIG
# ---------------------------------------------------------

CLASSES = [
    "OK",
    "I_LOVE_YOU",
    "STOP",
    "PEACE",
    "CALL_ME",
    "ROCK_ON",
    "THUMBS_UP",
    "FIST",
]

TARGET_SAMPLES_PER_CLASS = 500

# CSV file lives in dataset/, one level up from backend/scripts/
CSV_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "dataset", "landmarks.csv")
CSV_PATH = os.path.abspath(CSV_PATH)

# ---------------------------------------------------------
# CSV SETUP
# ---------------------------------------------------------

def ensure_csv_exists():
    """Create the CSV with a header row if it doesn't already exist."""
    if not os.path.exists(CSV_PATH):
        header = [f"feature_{i+1}" for i in range(63)] + ["label"]
        with open(CSV_PATH, mode="w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(header)
        print(f"Created new dataset file at: {CSV_PATH}")
    else:
        print(f"Using existing dataset file at: {CSV_PATH}")


def count_existing_samples(label):
    """Count how many rows already exist for a given class label."""
    if not os.path.exists(CSV_PATH):
        return 0
    count = 0
    with open(CSV_PATH, mode="r", newline="") as f:
        reader = csv.reader(f)
        next(reader, None)  # skip header
        for row in reader:
            if row and row[-1] == label:
                count += 1
    return count


def append_sample(features, label):
    """Append one row (63 features + label) to the CSV."""
    with open(CSV_PATH, mode="a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(features + [label])

# ---------------------------------------------------------
# MEDIAPIPE SETUP (same approach as Part 1)
# ---------------------------------------------------------

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.5
)


def extract_normalized_landmarks(hand_landmarks):
    """Same normalization approach as Part 1: relative to the wrist (landmark 0)."""
    landmark_list = [(lm.x, lm.y, lm.z) for lm in hand_landmarks.landmark]
    wrist_x, wrist_y, wrist_z = landmark_list[0]

    normalized = []
    for (x, y, z) in landmark_list:
        normalized.extend([x - wrist_x, y - wrist_y, z - wrist_z])

    return normalized  # flat list of 63 numbers

# ---------------------------------------------------------
# MAIN COLLECTION LOOP
# ---------------------------------------------------------

def main():
    ensure_csv_exists()

    class_index = 0
    current_label = CLASSES[class_index]
    samples_collected = count_existing_samples(current_label)

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open webcam.")
        return

    print("Data collection started.")
    print("SPACE = capture | N = next class | Q = quit")

    hand_detected = False
    current_features = None

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Failed to grab frame.")
            break

        frame = cv2.flip(frame, 1)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(rgb_frame)

        hand_detected = False
        current_features = None

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                current_features = extract_normalized_landmarks(hand_landmarks)
                hand_detected = True

        # --- Overlay info on the frame ---
        cv2.rectangle(frame, (0, 0), (400, 110), (0, 0, 0), -1)
        cv2.putText(frame, "SIGNBRIDGE DATA COLLECTOR", (10, 20),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        cv2.putText(frame, f"Class: {current_label}", (10, 45),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
        cv2.putText(frame, f"Samples: {samples_collected}/{TARGET_SAMPLES_PER_CLASS}", (10, 70),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
        detected_text = "YES" if hand_detected else "NO"
        detected_color = (0, 255, 0) if hand_detected else (0, 0, 255)
        cv2.putText(frame, f"Hand Detected: {detected_text}", (10, 95),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, detected_color, 2)

        cv2.imshow("SignBridge AI - Data Collector", frame)

        key = cv2.waitKey(1) & 0xFF

        if key == ord('q'):
            break

        elif key == ord(' '):  # SPACE -> capture
            if hand_detected and current_features is not None:
                append_sample(current_features, current_label)
                samples_collected += 1
                print(f"Captured sample {samples_collected} for class '{current_label}'")
            else:
                print("No hand detected - sample NOT captured.")

        elif key == ord('n'):  # N -> next class
            class_index = (class_index + 1) % len(CLASSES)
            current_label = CLASSES[class_index]
            samples_collected = count_existing_samples(current_label)
            print(f"Switched to class: {current_label} (existing samples: {samples_collected})")

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()