import os
from pathlib import Path

import joblib
import pandas as pd


MODEL_PATH = Path(
    os.getenv(
        "MODEL_PATH",
        "artifacts/inactivity_risk_model.joblib",
    )
)


def load_model():
    """Load the trained model artifact."""

    return joblib.load(MODEL_PATH)


def predict_inactivity_risk(customer_data: pd.DataFrame) -> pd.DataFrame:
    """Predict inactivity risk for customer feature data."""

    model = load_model()

    predictions = model.predict(customer_data)
    probabilities = model.predict_proba(customer_data)[:, 1]

    results = customer_data.copy()

    results["at_risk"] = predictions
    results["risk_probability"] = probabilities

    return results