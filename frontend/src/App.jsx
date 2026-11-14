import { useState } from "react";
import Navbar from "./components/Navbar";
import Camera from "./components/Camera";
import Prediction from "./components/Prediction";
import "./App.css";

const SUPPORTED_GESTURES = [
  "OK",
  "I LOVE YOU",
  "STOP",
  "PEACE",
  "CALL ME",
  "ROCK ON",
  "THUMBS UP",
  "FIST",
];

function App() {
  const [prediction, setPrediction] = useState(null);
  const [isPredicting, setIsPredicting] = useState(false);

  return (
    <div className="app">
      <Navbar />

      <main className="container main">
        <section className="hero">
          <h1>
            Sign Language{" "}
            <span className="hero-accent">Recognition Assistant</span>
          </h1>
          <p>
            Show a supported hand gesture to your webcam and SignBridge AI will
            recognize it in real time, along with a confidence score.
          </p>
        </section>

        <div className="panels">
          <Camera
            onPrediction={setPrediction}
            onPredictingChange={setIsPredicting}
          />
          <Prediction prediction={prediction} isPredicting={isPredicting} />
        </div>

        <section className="gestures" aria-labelledby="gestures-title">
          <h2 id="gestures-title" className="gestures-title">
            Supported gestures
          </h2>
          <ul className="chip-list">
            {SUPPORTED_GESTURES.map((g) => (
              <li key={g} className="chip">
                {g}
              </li>
            ))}
          </ul>
        </section>
      </main>

      <footer className="footer">
        <div className="container">
          Limited-vocabulary prototype: recognizes 8 static hand gestures, not
          full sign language.
        </div>
      </footer>
    </div>
  );
}

export default App;
