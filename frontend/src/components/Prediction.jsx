// Display-only helper: "THUMBS_UP" -> "THUMBS UP"
const formatLabel = (label) => String(label).replace(/_/g, " ");

function Prediction({ prediction, isPredicting }) {
  let tone = "neutral";
  let statusText = "Ready";
  let body = null;

  if (!prediction) {
    // Nothing received yet
    tone = isPredicting ? "info" : "neutral";
    statusText = isPredicting ? "Recognizing..." : "Ready";
    body = (
      <div className="result-state">
        <div className="waiting-icon" aria-hidden="true">
          <svg
            viewBox="0 0 24 24"
            width="30"
            height="30"
            fill="none"
            stroke="currentColor"
            strokeWidth="1.6"
            strokeLinecap="round"
            strokeLinejoin="round"
          >
            <path d="M18 11V6a2 2 0 0 0-4 0v5" />
            <path d="M14 10V4a2 2 0 0 0-4 0v6" />
            <path d="M10 10.5V6a2 2 0 0 0-4 0v8" />
            <path d="M18 8a2 2 0 1 1 4 0v6a8 8 0 0 1-8 8h-2c-2.8 0-4.5-.9-5.9-2.4L3.4 16a2 2 0 0 1 3.2-2.4L8 15" />
          </svg>
        </div>
        <p className="state-title">Waiting for gesture...</p>
        <p className="state-text">
          Start the camera and show one of the supported gestures.
        </p>
      </div>
    );
  } else if (typeof prediction.success !== "boolean") {
    // Defensive guard: malformed/unexpected response
    tone = "error";
    statusText = "Invalid response";
    body = (
      <p className="alert alert-error">
        Received an unexpected response from the server.
      </p>
    );
  } else if (!prediction.success) {
    const isNoHand = prediction.message === "No hand detected";

    if (isPredicting) {
      tone = "info";
      statusText = "Recognizing...";
    } else if (isNoHand) {
      tone = "warning";
      statusText = "No hand detected";
    } else {
      tone = "error";
      statusText = "Recognition server unavailable";
    }

    body = isNoHand ? (
      <p className="alert alert-warning">
        No hand detected. Please show a supported gesture.
      </p>
    ) : (
      <p className="alert alert-error">{prediction.message}</p>
    );
  } else {
    // Successful prediction: everything shown comes from the API response
    const confidencePercent = Math.round(prediction.confidence * 100);
    const barWidth = Math.min(100, Math.max(0, confidencePercent));

    tone = isPredicting ? "info" : "success";
    statusText = isPredicting ? "Recognizing..." : "Hand detected";

    body = (
      <div className="result-state">
        <p className="result-caption">Recognized gesture</p>
        <p className="result-label">{formatLabel(prediction.prediction)}</p>

        <div className="confidence">
          <div className="confidence-head">
            <span>Confidence</span>
            <span className="confidence-value">{confidencePercent}%</span>
          </div>
          <div
            className="confidence-track"
            role="progressbar"
            aria-label="Prediction confidence"
            aria-valuemin={0}
            aria-valuemax={100}
            aria-valuenow={barWidth}
          >
            <div
              className="confidence-fill"
              style={{ width: `${barWidth}%` }}
            />
          </div>
        </div>
      </div>
    );
  }

  return (
    <section
      className="card prediction-card"
      aria-labelledby="recognition-title"
    >
      <div className="card-header">
        <h2 id="recognition-title" className="card-title">
          Recognition
        </h2>
        <span className={`status-pill tone-${tone}`}>
          <span className="status-dot" aria-hidden="true" />
          {statusText}
        </span>
      </div>

      <div className="result-area" aria-live="polite">
        {body}
      </div>
    </section>
  );
}

export default Prediction;
