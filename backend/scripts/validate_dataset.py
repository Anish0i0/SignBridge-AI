"""
SignBridge AI - Part 2: Dataset Validation
Checks the collected dataset/landmarks.csv for correctness before
it's used in Part 3 (model training).
"""

import pandas as pd
import os

CSV_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "dataset", "landmarks.csv")
CSV_PATH = os.path.abspath(CSV_PATH)

def main():
    if not os.path.exists(CSV_PATH):
        print(f"Error: Dataset not found at {CSV_PATH}")
        return

    df = pd.read_csv(CSV_PATH)

    print("=" * 50)
    print("SIGNBRIDGE AI - DATASET VALIDATION REPORT")
    print("=" * 50)

    # 1. Total samples
    print(f"\nTotal samples: {len(df)}")

    # 2. Total columns (expect 64: 63 features + label)
    print(f"Total columns: {len(df.columns)} (expected: 64)")

    # 3. Classes present
    classes = df["label"].unique()
    print(f"\nNumber of classes: {len(classes)}")
    print(f"Classes found: {list(classes)}")

    # 4. Samples per class
    print("\nSamples per class:")
    counts = df["label"].value_counts()
    print(counts.to_string())

    # 5. Class imbalance check
    max_count = counts.max()
    min_count = counts.min()
    imbalance_ratio = max_count / min_count if min_count > 0 else float("inf")
    print(f"\nMax class count: {max_count} | Min class count: {min_count}")
    print(f"Imbalance ratio: {imbalance_ratio:.2f} (closer to 1.0 = more balanced)")

    # 6. Missing values
    missing = df.isnull().sum().sum()
    print(f"\nMissing values: {missing}")

    # 7. Duplicate rows
    duplicates = df.duplicated().sum()
    print(f"Duplicate rows: {duplicates}")

    # 8. Feature column data type check (should all be numeric)
    feature_cols = [c for c in df.columns if c.startswith("feature_")]
    non_numeric = df[feature_cols].select_dtypes(exclude=["number"]).columns.tolist()
    print(f"\nNon-numeric feature columns (should be empty): {non_numeric}")

    # 9. Feature value range sanity check (normalized values should be small, roughly -1 to 1)
    print(f"\nFeature value range: min={df[feature_cols].values.min():.4f}, max={df[feature_cols].values.max():.4f}")

    print("\n" + "=" * 50)
    print("VALIDATION COMPLETE")
    print("=" * 50)


if __name__ == "__main__":
    main()