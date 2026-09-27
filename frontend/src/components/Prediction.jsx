function Prediction({ prediction, isPredicting }) {
  // No prediction yet at all (camera not started / first request still pending)
  if (!prediction) {
    return (
      <div className="prediction-section">
        <h2>Recognition</h2>
        <p className="camera-status status-off">
          {isPredicting ? "Recognizing..." : "Ready"}
        </p>
        <div className="prediction-box">
          <p className="prediction-label placeholder">Waiting for gesture...</p>
        </div>
      </div>
    );
  }

  // Backend/network/model failure (not the same as "no hand" - distinguished by message content)
  if (!prediction.success) {
    const isNoHand = prediction.message === "No hand detected";

    return (
      <div className="prediction-section">
        <h2>Recognition</h2>
        <p
          className={`camera-status ${isNoHand ? "status-off" : "status-error"}`}
        >
          {isPredicting
            ? "Recognizing..."
            : isNoHand
              ? "No hand detected"
              : "Recognition server unavailable"}
        </p>
        <div className="prediction-box">
          <p className="prediction-message">
            {isNoHand
              ? "No hand detected. Please show a supported gesture."
              : prediction.message}
          </p>
        </div>
      </div>
    );
  }

  // Defensive guard: if the response is malformed/unexpected, treat it like a failure
  if (typeof prediction.success !== "boolean") {
    return (
      <div className="prediction-section">
        <h2>Recognition</h2>
        <p className="camera-status status-error">Invalid response</p>
        <div className="prediction-box">
          <p className="prediction-message">
            Received an unexpected response from the server.
          </p>
        </div>
      </div>
    );
  }

  // Successful prediction
  const confidencePercent = Math.round(prediction.confidence * 100);

  return (
    <div className="prediction-section">
      <h2>Recognition</h2>
      <p className="camera-status status-active">
        {isPredicting ? "Recognizing..." : "● Hand detected"}
      </p>
      <div className="prediction-box">
        <p className="recognized-label">Recognized Gesture</p>
        <p className="prediction-label">{prediction.prediction}</p>

        <p className="confidence-caption">Confidence</p>
        <div className="confidence-bar-track">
          <div
            className="confidence-bar-fill"
            style={{ width: `${confidencePercent}%` }}
          />
        </div>
        <p className="confidence-label">{confidencePercent}%</p>
      </div>
    </div>
  );
}

export default Prediction;
