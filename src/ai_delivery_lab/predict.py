import os
from pathlib import Path

import joblib
import pandas as pd

from ai_delivery_lab.risk_aggregation import aggregate_risk


ARTIFACTS_DIR = Path(
    os.getenv(
        "ARTIFACTS_DIR",
        "artifacts",
    )
)


MODEL_PATHS = {
    "logistic": ARTIFACTS_DIR / "logistic_regression_model.joblib",
    "random_forest": ARTIFACTS_DIR / "random_forest_model.joblib",
    "gradient_boosting": ARTIFACTS_DIR / "gradient_boosting_model.joblib",
}


def load_models() -> dict[str, object]:
    """Load the trained model artifacts."""

    return {
        name: joblib.load(path)
        for name, path in MODEL_PATHS.items()
    }


def predict_inactivity_risk(customer_data: pd.DataFrame) -> pd.DataFrame:
    """Predict inactivity risk using multiple models."""

    models = load_models()

    logistic_probability = models["logistic"].predict_proba(customer_data)[:, 1]
    random_forest_probability = models["random_forest"].predict_proba(customer_data)[:, 1]
    gradient_boosting_probability = models["gradient_boosting"].predict_proba(customer_data)[:, 1]

    aggregated_probability = aggregate_risk(
        logistic_probability=float(logistic_probability[0]),
        random_forest_probability=float(random_forest_probability[0]),
        gradient_boosting_probability=float(gradient_boosting_probability[0]),
    )

    results = customer_data.copy()

    results["risk_probability"] = aggregated_probability
    results["at_risk"] = int(aggregated_probability >= 0.5)

    return results