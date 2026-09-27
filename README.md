# SignBridge AI

SignBridge AI is a camera-based sign language recognition prototype that detects a predefined set of static hand gestures in real time and displays the recognized gesture along with a confidence score.

## Overview

Communication barriers between sign language users and others often stem from a lack of accessible, low-cost recognition tools. SignBridge AI addresses this on a small scale by recognizing a limited vocabulary of static hand gestures using nothing but a laptop webcam.

The system works as follows:
- The React frontend captures frames from the user's webcam.
- Each frame is sent to a FastAPI backend.
- The backend uses MediaPipe to detect the hand and extract 21 hand landmarks.
- The landmark coordinates are normalized and passed to a trained Random Forest classifier.
- The predicted gesture and its confidence score are returned to the frontend and displayed live.

SignBridge AI is a limited-vocabulary prototype. It recognizes a fixed set of 8 static hand gestures and does **not** perform continuous sign-language sentence translation or full sign-language interpretation.

## Features

- Real-time webcam input via the browser (`getUserMedia`)
- Hand detection and 21-landmark extraction using MediaPipe
- Landmark normalization (relative to the wrist)
- Gesture classification using a trained Random Forest model
- Prediction confidence score, displayed as a percentage and a progress bar
- Camera status indicators: Camera Off / Camera Active / Camera Permission Required
- Recognition status indicators: Ready / Recognizing / Hand Detected / No Hand Detected / Recognition Server Unavailable
- Graceful error handling for camera permission issues, backend unavailability, and malformed responses
- Responsive interface (side-by-side layout on larger screens, stacked layout on mobile)
- FastAPI backend with `/health` and `/predict` endpoints
- Interactive Swagger API documentation at `/docs`

## How It Works

```
Webcam
  → React (frame capture)
  → FastAPI (POST /predict)
  → OpenCV (image decoding)
  → MediaPipe (hand detection, 21 landmarks)
  → Normalization (landmark coordinates relative to the wrist)
  → Random Forest Classifier
  → Predicted gesture + confidence
  → JSON response
  → React UI (display)
```

1. **Webcam capture** — The browser accesses the user's camera and displays a live feed.
2. **Frame capture** — At a fixed interval, the current video frame is drawn to a hidden canvas and converted to a JPEG image.
3. **Upload to backend** — The image is sent as `multipart/form-data` to the FastAPI `POST /predict` endpoint.
4. **Hand detection** — The backend decodes the image with OpenCV and runs MediaPipe Hands to detect a single hand and its 21 landmarks (x, y, z coordinates each).
5. **Normalization** — All 21 landmarks are made relative to the wrist landmark, so the same gesture produces similar feature values regardless of the hand's position in the frame.
6. **Classification** — The 63 resulting numerical features (21 landmarks × 3 coordinates) are passed to a trained Random Forest classifier, which predicts one of the 8 supported gesture classes along with a confidence score.
7. **Response and display** — FastAPI returns the prediction as JSON, and the React frontend updates the UI accordingly.

## Machine Learning Model

- **Algorithm:** Random Forest Classifier (scikit-learn)
- **Input features:** 63 numerical values per sample — the (x, y, z) coordinates of 21 hand landmarks detected by MediaPipe, normalized relative to the wrist landmark
- **Output:** One of 8 supported static gesture classes, with a confidence score (from `predict_proba`)
- **Note:** MediaPipe is used only for hand detection and landmark extraction. It is not the classification algorithm — the Random Forest model performs the actual gesture classification based on the landmark features MediaPipe provides.

### Supported gesture classes
`OK`, `I_LOVE_YOU`, `STOP`, `PEACE`, `CALL_ME`, `ROCK_ON`, `THUMBS_UP`, `FIST`

### Evaluation
The model was trained on a labelled dataset collected via webcam (see `dataset/`) and evaluated on a held-out, stratified test split.

- Test accuracy: **97.78%**
- Per-class precision/recall/F1: all between 0.92 and 1.00
- Observed confusion: `ROCK_ON` is occasionally misclassified as `I_LOVE_YOU` (and vice versa), since both gestures extend the index and pinky fingers and produce similar landmark geometry. This is a documented, explainable limitation rather than a general model failure.

## Technology Stack

**Frontend**
- React
- Vite
- JavaScript
- HTML / CSS

**Backend**
- Python
- FastAPI
- Uvicorn

**Computer Vision**
- OpenCV
- MediaPipe (Hands)

**Machine Learning**
- scikit-learn (RandomForestClassifier)
- NumPy
- Pandas
- joblib (model serialization)

**Development Tools**
- Visual Studio Code
- Git / GitHub

## Project Structure

```
SignBridge-AI/
│
├── backend/
│   ├── main.py                    # FastAPI app: /health, /predict, CORS, model loading
│   ├── test_camera.py             # Basic OpenCV webcam test (Part 1)
│   ├── hand_detection.py          # MediaPipe hand detection + landmark extraction (Part 1)
│   ├── services/
│   │   └── prediction.py          # Preprocessing + prediction pipeline used by /predict
│   ├── ml/
│   │   ├── train_model.py         # Loads dataset, trains and evaluates the Random Forest model
│   │   └── inspect_model.py       # Inspects the saved model (features, classes, capabilities)
│   └── scripts/
│       ├── collect_data.py        # Webcam-based dataset collection tool
│       └── validate_dataset.py    # Dataset validation/quality checks
│
├── dataset/
│   └── landmarks.csv              # Labelled landmark dataset (63 features + label per row)
│
├── models/
│   └── sign_model.pkl             # Trained Random Forest model (joblib)
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── Navbar.jsx
│   │   │   ├── Camera.jsx
│   │   │   └── Prediction.jsx
│   │   ├── App.jsx
│   │   ├── App.css
│   │   └── main.jsx
│   ├── index.html
│   ├── package.json
│   └── vite.config.js
│
├── requirements.txt
├── .gitignore
└── README.md
```

> Note: the `venv/` and `node_modules/` folders are intentionally excluded from the repository (see `.gitignore`) and must be created locally.

## Installation

### Prerequisites
- Python 3.x
- Node.js and npm

### Clone the repository

```bash
git clone https://github.com/Anish0i0/SignBridge-AI.git
cd SignBridge-AI
```

### Backend setup

The `venv/` folder is not stored in this repository. Create your own virtual environment locally:

```bash
python -m venv venv
```

Activate it:

```bash
# Windows
venv\Scripts\Activate.ps1

# macOS/Linux
source venv/bin/activate
```

Install backend dependencies:

```bash
pip install -r requirements.txt
```

### Frontend setup

```bash
cd frontend
npm install
```

## Running the Project

Both the backend and frontend need to run at the same time, in separate terminals.

### Backend

From the project root, with the virtual environment activated:

```bash
uvicorn backend.main:app --reload
```

The API will be available at `http://127.0.0.1:8000`, with interactive documentation at `http://127.0.0.1:8000/docs`.

### Frontend

From the `frontend/` folder:

```bash
npm run dev
```

The application will be available at `http://localhost:5173`.

## API Endpoints

### `GET /health`

Returns server and model status.

```json
{ "status": "ok", "model": "loaded" }
```

### `POST /predict`

Accepts an image file as `multipart/form-data` under the field name `file`, containing a hand gesture.

**Successful prediction:**
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

CORS is configured to allow requests from `http://localhost:5173` (the default Vite development server address).

## User Interface

The interface consists of two main panels, displayed side-by-side on larger screens and stacked on smaller ones:

- **Camera panel** — shows the live webcam feed, a status indicator (Camera Off / ● Camera Active / Camera Permission Required), and Start/Stop controls.
- **Recognition panel** — shows the current recognition status (Ready / Recognizing... / ● Hand Detected / No Hand Detected / Recognition Server Unavailable), the recognized gesture label, and a confidence percentage with a progress bar.

If no gesture has been recognized yet, the panel displays a "Waiting for gesture..." placeholder rather than any hard-coded value. All displayed predictions and confidence values come directly from the backend's API response.

## Testing

The following functional tests were performed and passed:

| Test Case | Input | Expected Result |
|---|---|---|
| Application loads | Open the app in a browser | React application opens successfully |
| Camera starts | Click "Start Camera" | Webcam feed appears, status shows Camera Active |
| Camera stops | Click "Stop Camera" | Feed stops, camera hardware is released |
| Supported gesture | Show a trained gesture | Correct prediction is displayed |
| Confidence display | Same as above | Actual confidence percentage and bar are shown |
| No hand | Move hand out of frame | "No hand detected" message is shown |
| Backend stopped | Stop the FastAPI server | UI shows "Recognition Server Unavailable" gracefully |
| Camera permission denied | Deny the browser prompt | Readable camera error is shown |
| Prediction loading | During normal use | "Recognizing..." status appears briefly |
| Responsive layout | Resize browser / use a mobile viewport | Interface remains usable, no overflow |

## Real-World Testing and Limitations

The application was tested under a range of practical conditions, in addition to the functional tests above:

- **Lighting:** Recognition is reliable under normal/good lighting across all 8 supported gestures. In low-light conditions, recognition of most gestures remained stable, but occasional misclassification was observed between the two most visually similar gestures (`ROCK_ON` and `I_LOVE_YOU`), consistent with the model's evaluation results.
- **Similar gestures:** `ROCK_ON` and `I_LOVE_YOU` can be confused with each other, since both involve extending the index and pinky fingers. This is a known, documented limitation rather than a random failure.

**Scope limitations:**
- The system recognizes a fixed vocabulary of 8 static hand gestures.
- It does not perform continuous sign-language sentence translation or full sign-language interpretation.
- It relies on a single, static hand pose per prediction rather than motion or sequence-based signs.

These limitations reflect the current scope of a BCA minor project prototype rather than defects in the implementation.

## Future Scope

The following are potential directions for future work and are **not** currently implemented:

- Text-to-speech output for recognized gestures
- Deployment to a hosted environment
- An expanded gesture vocabulary
- A larger, more diverse dataset (more samples, lighting/background variation)
- Improved robustness under low-light conditions and for visually similar gestures
- Continuous, sequence-based sign-language recognition (rather than single static poses)

## Screenshots

Screenshots are not yet included in this repository. This section can be updated with images such as the main interface, an active recognition example, the no-hand and backend-unavailable states, and the FastAPI Swagger documentation, for example:

```markdown
### Main Interface
![SignBridge AI Interface](screenshots/main-interface.png)
```

## Project Status

The core SignBridge AI application is complete:

- Frontend: complete
- Backend: complete
- Machine learning pipeline: complete
- UI/UX: complete
- Functional testing: complete

**Text-to-Speech:** not currently implemented (future scope)
**Deployment:** not currently implemented (future scope)

## Academic Context

SignBridge AI was developed as a BCA (Bachelor of Computer Applications) minor project.

## Author

**Anish0i0** — [GitHub](https://github.com/Anish0i0)
