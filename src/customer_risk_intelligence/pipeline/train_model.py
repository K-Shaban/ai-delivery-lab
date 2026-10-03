from pathlib import Path

import joblib
import pandas as pd
from sklearn.model_selection import train_test_split

from customer_risk_intelligence.evaluation import evaluate_classifier
from customer_risk_intelligence.model import (
    CATEGORICAL_FEATURES,
    NUMERIC_FEATURES,
    build_logistic_model,
)


PROJECT_ROOT = Path(__file__).resolve().parents[3]

DATA_PATH = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "customer_training.csv"
)

MODEL_PATH = (
    PROJECT_ROOT
    / "artifacts"
    / "inactivity_risk_model.joblib"
)


def main() -> None:
    """Train the selected model and save it as an artifact."""

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

    model = build_logistic_model()

    model.fit(X_train, y_train)

    predictions = model.predict(X_test)
    probabilities = model.predict_proba(X_test)[:, 1]

    metrics = evaluate_classifier(
        y_test,
        predictions,
        probabilities,
    )

    MODEL_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    joblib.dump(
        model,
        MODEL_PATH,
    )

    print("\n--- Model Evaluation ---")

    for name, value in metrics.items():
        print(f"{name}: {value:.4f}")

    print(f"\nModel saved to: {MODEL_PATH}")


if __name__ == "__main__":
    main()
