"""
SignBridge AI - Part 3: Model Training (Step 3.1)
Loads the labelled landmark dataset and separates features from labels.
"""

import pandas as pd
import os
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.metrics import classification_report, confusion_matrix
import joblib

CSV_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "dataset", "landmarks.csv")
CSV_PATH = os.path.abspath(CSV_PATH)


def load_dataset():
    if not os.path.exists(CSV_PATH):
        raise FileNotFoundError(f"Dataset not found at {CSV_PATH}")

    df = pd.read_csv(CSV_PATH)
    return df


def main():
    df = load_dataset()

    print(f"Dataset loaded from: {CSV_PATH}")
    print(f"Shape (rows, columns): {df.shape}")

    feature_cols = [c for c in df.columns if c.startswith("feature_")]
    X = df[feature_cols]
    y = df["label"]

    print(f"\nFeature matrix X shape: {X.shape}")
    print(f"Label vector y shape: {y.shape}")
    print(f"Unique classes in y: {sorted(y.unique())}")

    # --- Train/Test Split ---
    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=0.2,      # 20% held out for testing
        random_state=42,    # fixed seed so the split is reproducible
        stratify=y          # keep class proportions the same in both sets
    )

    print(f"\nTraining set size: {X_train.shape[0]} samples")
    print(f"Test set size: {X_test.shape[0]} samples")

    print("\nTraining set class distribution:")
    print(y_train.value_counts())

    print("\nTest set class distribution:")
    print(y_test.value_counts())

        # --- Train the model ---
    print("\nTraining Random Forest Classifier...")
    model = RandomForestClassifier(
        n_estimators=100,   # number of decision trees in the forest
        random_state=42     # reproducibility
    )
    model.fit(X_train, y_train)
    print("Training complete.")

    # --- Quick evaluation on the test set ---
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"\nTest set accuracy: {accuracy * 100:.2f}%")

        # --- Detailed evaluation ---
    print("\nClassification Report (per-class precision/recall/F1):")
    print(classification_report(y_test, y_pred))

    print("Confusion Matrix:")
    labels_sorted = sorted(y.unique())
    cm = confusion_matrix(y_test, y_pred, labels=labels_sorted)
    print(f"Labels order: {labels_sorted}\n")
    print(cm)

        # --- Save the trained model ---
    model_dir = os.path.join(os.path.dirname(__file__), "..", "..", "models")
    model_dir = os.path.abspath(model_dir)
    os.makedirs(model_dir, exist_ok=True)

    model_path = os.path.join(model_dir, "sign_model.pkl")
    joblib.dump(model, model_path)

    print(f"\nModel saved to: {model_path}")


if __name__ == "__main__":
    main()