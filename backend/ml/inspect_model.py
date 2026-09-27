"""
SignBridge AI - Part 4, Step 4.1
Inspects the trained model saved in Part 3 to confirm exactly what
input it expects and what capabilities it has, before building the API.
"""

import joblib
import os

MODEL_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "models", "sign_model.pkl")
MODEL_PATH = os.path.abspath(MODEL_PATH)


def main():
    if not os.path.exists(MODEL_PATH):
        print(f"Error: Model not found at {MODEL_PATH}")
        return

    model = joblib.load(MODEL_PATH)

    print(f"Model loaded from: {MODEL_PATH}")
    print(f"\nModel type: {type(model)}")
    print(f"Number of input features expected: {model.n_features_in_}")
    print(f"Class labels (model.classes_): {list(model.classes_)}")
    print(f"Number of classes: {len(model.classes_)}")
    print(f"\nSupports predict_proba(): {hasattr(model, 'predict_proba')}")
    print(f"Number of trees (n_estimators): {model.n_estimators}")

    # Check if a separate scaler/preprocessor file exists
    models_dir = os.path.dirname(MODEL_PATH)
    print(f"\nFiles in models/ directory: {os.listdir(models_dir)}")


if __name__ == "__main__":
    main()