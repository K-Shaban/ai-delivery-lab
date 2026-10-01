from pathlib import Path

import pandas as pd
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split

from ai_delivery_lab.evaluation import evaluate_classifier
from ai_delivery_lab.model import (
    CATEGORICAL_FEATURES,
    NUMERIC_FEATURES,
    build_model,
)


PROJECT_ROOT = Path(__file__).resolve().parents[3]
DATA_PATH = PROJECT_ROOT / "data" / "processed" / "customer_training.csv"


def main() -> None:
    """Train and evaluate the baseline inactivity-risk model."""

    df = pd.read_csv(DATA_PATH)

    feature_columns = NUMERIC_FEATURES + CATEGORICAL_FEATURES

    X = df[feature_columns]
    y = df["at_risk"]

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y,
    )

    model = build_model()

    model.fit(X_train, y_train)

    predictions = model.predict(X_test)
    probabilities = model.predict_proba(X_test)[:, 1]

    metrics = evaluate_classifier(
        y_test,
        predictions,
        probabilities,
    )

    print("\n--- Classification Report ---")
    print(classification_report(y_test, predictions))

    print("--- Evaluation Metrics ---")

    for name, value in metrics.items():
        print(f"{name}: {value:.4f}")


if __name__ == "__main__":
    main()