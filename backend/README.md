# SignBridge AI — Backend API

## Overview

FastAPI backend that loads the trained model from Part 3 and serves
live gesture predictions from uploaded images.

## Endpoints

### GET /health

Returns server and model status.

```json
{ "status": "ok", "model": "loaded" }
```

### POST /predict

Accepts an image file (multipart/form-data) containing a hand gesture.

Pipeline: image → decode → MediaPipe hand detection → wrist-relative
landmark normalization (same method as Part 1/2) → trained
RandomForestClassifier → predicted class + confidence.

**Success response:**

```json
{ "success": true, "prediction": "THUMBS_UP", "confidence": 0.91 }
```

**No hand detected:**

```json
{ "success": false, "message": "No hand detected" }
```

**Invalid file:**

```json
{ "success": false, "message": "Invalid image file" }
```

## Architecture notes

- The model is loaded once at server startup (not per-request) for
  performance — see `load_model()` in `main.py`
- Preprocessing in `services/prediction.py` intentionally mirrors
  Part 1/2 exactly (wrist-relative normalization) so the backend's
  features match what the model was trained on
- `static_image_mode=True` is used here (vs. `False` in Part 1),
  since each API request is an independent image, not a video stream
- No separate scaler/preprocessor exists — normalization is purely
  the manual wrist-subtraction method, confirmed in Step 4.1

## CORS

Configured to allow requests from `http://localhost:5173` (Vite's
default dev server), in preparation for the Part 5 React frontend.

## Running the server

```bash
uvicorn backend.main:app --reload
```

Docs available at `http://127.0.0.1:8000/docs`

## Tested scenarios (Part 4)

- Valid gesture image → correct prediction + confidence
- No hand in image → correctly flagged, not treated as a prediction
- Invalid/non-image file → correctly rejected
