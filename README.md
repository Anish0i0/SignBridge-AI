# SignBridge AI — Sign Language Recognition and Communication Assistant

BCA Minor Project — AI/ML and Computer Vision based web application to help
reduce communication barriers for sign language users.

## Part 1 — Project Setup + Hand Detection (Completed)

This part demonstrates the core computer-vision pipeline on a normal laptop:

Webcam → OpenCV → MediaPipe Hand Detection → 21 Hand Landmarks →
Landmark Coordinates → Normalization

### What works

- Python virtual environment set up (`venv`)
- Webcam access via OpenCV (`backend/test_camera.py`)
- Real-time hand detection via MediaPipe (`backend/hand_detection.py`)
- Extraction of 21 hand landmarks (x, y, z) — 63 features per frame
- Normalization of landmarks relative to the wrist

### Tech used

- Python
- OpenCV (`opencv-python`)
- MediaPipe (`mediapipe==0.10.9` — pinned; newer versions removed the
  `mp.solutions` API used here)

### Known limitations (observed during testing)

- Fast hand movement can cause temporary loss of detection (motion blur)
- Detection requires the hand to be fully visible within the frame
- Only single-hand detection is enabled (project scope)

### How to run

```bash
# Activate the virtual environment first
python backend/test_camera.py       # basic webcam test
python backend/hand_detection.py    # hand detection + landmark extraction
```

### Next: Part 2 — Dataset Collection
