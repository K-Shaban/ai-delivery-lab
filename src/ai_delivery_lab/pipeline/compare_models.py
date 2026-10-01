from pathlib import Path

import pandas as pd
from sklearn.model_selection import train_test_split

from ai_delivery_lab.evaluation import evaluate_classifier
from ai_delivery_lab.model import (
    CATEGORICAL_FEATURES,
    NUMERIC_FEATURES,
    build_logistic_model,
    build_random_forest_model,
)


PROJECT_ROOT = Path(__file__).resolve().parents[3]
DATA_PATH = PROJECT_ROOT / "data" / "processed" / "customer_training.csv"


def evaluate_model(name, model, X_train, X_test, y_train, y_test):
    """Train and evaluate a model."""

    model.fit(X_train, y_train)

    predictions = model.predict(X_test)
    probabilities = model.predict_proba(X_test)[:, 1]

    metrics = evaluate_classifier(
        y_test,
        predictions,
        probabilities,
    )

    print(f"\n--- {name} ---")

    for metric, value in metrics.items():
        print(f"{metric}: {value:.4f}")

    return metrics


def main() -> None:
    """Compare baseline and candidate models."""

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

    models = {
        "Logistic Regression": build_logistic_model(),
        "Random Forest": build_random_forest_model(),
    }

    results = {}

    for name, model in models.items():
        results[name] = evaluate_model(
            name,
            model,
            X_train,
            X_test,
            y_train,
            y_test,
        )

    comparison = pd.DataFrame(results).T

    print("\n--- Model Comparison ---")
    print(comparison.round(4))


if __name__ == "__main__":
    main()