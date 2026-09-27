"""
SignBridge AI - Part 4: FastAPI Backend
Main application entry point.
"""

import os
import joblib
import cv2
import numpy as np
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from backend.services.prediction import predict_sign

MODEL_PATH = os.path.join(os.path.dirname(__file__), "..", "models", "sign_model.pkl")
MODEL_PATH = os.path.abspath(MODEL_PATH)

app = FastAPI(title="SignBridge AI API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vite's default dev server address
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

model = None


@app.on_event("startup")
def load_model():
    global model
    if not os.path.exists(MODEL_PATH):
        raise RuntimeError(f"Model file not found at {MODEL_PATH}. Cannot start server without it.")

    model = joblib.load(MODEL_PATH)
    print(f"Model loaded successfully from: {MODEL_PATH}")
    print(f"Model expects {model.n_features_in_} features")
    print(f"Classes: {list(model.classes_)}")


@app.get("/health")
def health_check():
    model_status = "loaded" if model is not None else "not loaded"
    return {"status": "ok", "model": model_status}


@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    if model is None:
        return {"success": False, "message": "Model not loaded"}

    # Read the uploaded file into bytes, then decode into an OpenCV image
    contents = await file.read()

    if not contents:
        return {"success": False, "message": "Empty file received"}

    file_bytes = np.frombuffer(contents, np.uint8)
    image_bgr = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

    if image_bgr is None:
        return {"success": False, "message": "Invalid image file"}

    result = predict_sign(model, image_bgr)
    return result