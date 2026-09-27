import { useState } from "react";
import Navbar from "./components/Navbar";
import Camera from "./components/Camera";
import Prediction from "./components/Prediction";
import "./App.css";

function App() {
  const [prediction, setPrediction] = useState(null);
  const [isPredicting, setIsPredicting] = useState(false);

  return (
    <div className="app">
      <Navbar />

      <main className="main-content">
        <div className="panels">
          <Camera
            onPrediction={setPrediction}
            onPredictingChange={setIsPredicting}
          />
          <Prediction prediction={prediction} isPredicting={isPredicting} />
        </div>
      </main>
    </div>
  );
}

export default App;
