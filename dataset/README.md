# SignBridge AI — Dataset

## Overview

This dataset contains normalized MediaPipe hand-landmark features paired
with gesture labels, collected via `backend/scripts/collect_data.py`.

## Format

- File: `landmarks.csv`
- 64 columns: `feature_1` ... `feature_63` (21 landmarks × x, y, z), `label`
- Features are normalized relative to the wrist (landmark 0), following
  the same approach used in Part 1

## Classes (8 total)

Static, single-hand poses — chosen because Part 1's pipeline captures a
single still frame, not motion or sequences:

- OK
- I_LOVE_YOU
- STOP
- PEACE
- CALL_ME
- ROCK_ON
- THUMBS_UP
- FIST

## Dataset statistics (as of collection)

- Total samples: 2,065
- Samples per class: 244–278 (imbalance ratio 1.14 — well balanced)
- Missing values: 0
- Duplicate rows: 0
- All feature values numeric, in expected range

## Known limitation

Per-class sample count (244–278) is below the originally targeted
300–500 range. The dataset is clean and balanced but smaller than ideal;
this may limit model robustness and is a deliberate scope decision for
this prototype stage, not an oversight.

## Collection method

Samples were captured live via webcam using MediaPipe hand detection.
No synthetic or fabricated data was used. Natural variation (hand
distance, angle, position) was introduced during collection.
