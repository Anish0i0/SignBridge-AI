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
          message: "Backend unavailable. Make sure FastAPI is running.",
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
  useEffect(() => {
    onPredictingChange(isPredicting);
  }, [isPredicting]);

  const getStatusText = () => {
    if (cameraError) return "Camera Permission Required";
    if (isCameraOn) return "● Camera Active";
    return "Camera Off";
  };

  const getStatusClass = () => {
    if (cameraError) return "camera-status status-error";
    if (isCameraOn) return "camera-status status-active";
    return "camera-status status-off";
  };

  return (
    <div className="camera-section">
      <h2>Camera</h2>
      <p className={getStatusClass()}>{getStatusText()}</p>

      <div className="camera-placeholder">
        <video
          ref={videoRef}
          autoPlay
          playsInline
          muted
          className="camera-video"
          style={{ display: isCameraOn ? "block" : "none" }}
        />
        {!isCameraOn && <p>Camera feed will appear here</p>}
      </div>

      <canvas ref={canvasRef} style={{ display: "none" }} />

      {cameraError && <p className="camera-error">{cameraError}</p>}

      <button
        className="start-btn"
        onClick={isCameraOn ? stopCamera : startCamera}
      >
        {isCameraOn ? "Stop Camera" : "Start Camera"}
      </button>
    </div>
  );
}

export default Camera;
