# SignBridge AI — Trained Model

## Overview

`sign_model.pkl` is a trained scikit-learn RandomForestClassifier that
predicts one of 8 static hand gestures from 63 normalized MediaPipe
landmark features (21 landmarks × x, y, z, relative to the wrist).

## Training details

- Algorithm: RandomForestClassifier (n_estimators=100, random_state=42)
- Dataset: dataset/landmarks.csv (2,474 samples, 8 classes)
- Train/test split: 80/20, stratified by class
- Training set: 1,979 samples | Test set: 495 samples

## Evaluation results

- Test accuracy: 97.78%
- Per-class precision/recall/F1: all between 0.92–1.00 (no weak classes)
- Main observed confusion: ROCK_ON occasionally misclassified as
  I_LOVE_YOU (5/64 test samples) — both gestures extend the index and
  pinky fingers, so their landmark geometry is genuinely similar. This
  is a real, explainable limitation rather than a bug.
- Minor, low-count confusions also observed between OK/STOP/PEACE and
  FIST/THUMBS_UP (1–2 samples each), not systemic.

## How it was saved

Serialized with `joblib.dump()` after training in
`backend/ml/train_model.py`.

## Next step (Part 4)

This model will be loaded by the FastAPI backend to serve live
predictions from webcam-captured landmark features.
