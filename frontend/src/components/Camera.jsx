import { useRef, useState, useEffect } from "react";

const API_URL = "http://127.0.0.1:8000";
const PREDICTION_INTERVAL_MS = 800; // how often we send a frame for prediction

function Camera({ onPrediction = () => {}, onPredictingChange = () => {} }) {
  const videoRef = useRef(null);
  const canvasRef = useRef(null);
  const streamRef = useRef(null);
  const intervalRef = useRef(null);

  const [isCameraOn, setIsCameraOn] = useState(false);
  const [cameraError, setCameraError] = useState(null);
  const [isPredicting, setIsPredicting] = useState(false);

  const startCamera = async () => {
    setCameraError(null);
    try {
      const stream = await navigator.mediaDevices.getUserMedia({
        video: { width: 640, height: 480 },
        audio: false,
      });

      streamRef.current = stream;
      if (videoRef.current) {
        videoRef.current.srcObject = stream;
      }
      setIsCameraOn(true);
    } catch (err) {
      if (err.name === "NotAllowedError") {
        setCameraError("Camera permission was denied.");
      } else if (err.name === "NotFoundError") {
        setCameraError("No camera device found.");
      } else {
        setCameraError("Unable to access camera.");
      }
      console.error("Camera error:", err);
    }
  };

  const stopCamera = () => {
    if (streamRef.current) {
      streamRef.current.getTracks().forEach((track) => track.stop());
      streamRef.current = null;
    }
    setIsCameraOn(false);
  };

  const captureAndPredict = async () => {
    const video = videoRef.current;
    const canvas = canvasRef.current;
    if (!video || !canvas || video.readyState < 2) return;

    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    const ctx = canvas.getContext("2d");
    ctx.drawImage(video, 0, 0, canvas.width, canvas.height);

    canvas.toBlob(async (blob) => {
      if (!blob) return;

      const formData = new FormData();
      formData.append("file", blob, "frame.jpg");

      setIsPredicting(true);
      try {
        const response = await fetch(`${API_URL}/predict`, {
          method: "POST",
          body: formData,
        });

        if (!response.ok) {
          onPrediction({
            success: false,
            message: "Recognition server unavailable.",
          });
          return;
        }

        const data = await response.json();
        onPrediction(data);
      } catch (err) {
        console.error("Prediction request failed:", err);
        onPrediction({
          success: false,
          message: "Recognition server unavailable.",
        });
      } finally {
        setIsPredicting(false);
      }
    }, "image/jpeg");
  };

  // Start/stop the periodic prediction loop whenever the camera turns on/off
  useEffect(() => {
    if (isCameraOn) {
      intervalRef.current = setInterval(
        captureAndPredict,
        PREDICTION_INTERVAL_MS,
      );
    } else {
      clearInterval(intervalRef.current);
    }
    return () => clearInterval(intervalRef.current);
  }, [isCameraOn]);

  // Report loading state up to App
  useEffect(() => {
    onPredictingChange(isPredicting);
  }, [isPredicting]);

  // ---- Presentation only below this line ----
  let status = { label: "Camera Off", tone: "neutral" };
  if (cameraError) {
    status = { label: "Camera Permission Required", tone: "error" };
  } else if (isCameraOn) {
    status = { label: "Camera Active", tone: "success" };
  }

  return (
    <section className="card camera-card" aria-labelledby="camera-title">
      <div className="card-header">
        <h2 id="camera-title" className="card-title">
          Camera
        </h2>
        <span className={`status-pill tone-${status.tone}`}>
          <span className="status-dot" aria-hidden="true" />
          {status.label}
        </span>
      </div>

      <div className="camera-frame">
        <video
          ref={videoRef}
          autoPlay
          playsInline
          muted
          className="camera-video"
          aria-label="Live webcam preview"
          style={{ display: isCameraOn ? "block" : "none" }}
        />

        {!isCameraOn && (
          <div className="camera-placeholder">
            <svg
              viewBox="0 0 24 24"
              width="40"
              height="40"
              fill="none"
              stroke="currentColor"
              strokeWidth="1.6"
              strokeLinecap="round"
              strokeLinejoin="round"
              aria-hidden="true"
            >
              <path d="M23 7l-7 5 7 5V7z" />
              <rect x="1" y="5" width="15" height="14" rx="2" ry="2" />
            </svg>
            <p className="placeholder-title">Camera is off</p>
            <p className="placeholder-text">
              Start the camera, then show a gesture to begin recognition.
            </p>
          </div>
        )}
      </div>

      {/* Hidden canvas used only for capturing frames - never shown to the user */}
      <canvas ref={canvasRef} style={{ display: "none" }} />

      {cameraError && (
        <p className="alert alert-error" role="alert">
          {cameraError}
        </p>
      )}

      <div className="button-row">
        <button
          type="button"
          className="btn btn-primary"
          onClick={startCamera}
          disabled={isCameraOn}
        >
          Start Camera
        </button>
        <button
          type="button"
          className="btn btn-secondary"
          onClick={stopCamera}
          disabled={!isCameraOn}
        >
          Stop Camera
        </button>
      </div>
    </section>
  );
}

export default Camera;
