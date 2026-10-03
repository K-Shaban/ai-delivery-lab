import pandas as pd
import numpy as np
import pytest

from customer_risk_intelligence.predict import predict_inactivity_risk


def test_predict_inactivity_risk(monkeypatch):
    class FakeModel:
        def __init__(self, probability):
            self.probability = probability

        def predict_proba(self, customer):
            return np.array([[1 - self.probability, self.probability]])

    monkeypatch.setattr(
        "customer_risk_intelligence.predict.load_models",
        lambda: {
            "logistic": FakeModel(0.60),
            "random_forest": FakeModel(0.70),
            "gradient_boosting": FakeModel(0.80),
        },
    )

    customer = pd.DataFrame(
        {
            "Recency": [10],
            "Frequency": [5],
            "TotalQuantity": [100],
            "MonetaryValue": [500.0],
            "AverageOrderValue": [100.0],
            "UniqueProducts": [10],
            "Country": ["United Kingdom"],
        }
    )

    result = predict_inactivity_risk(customer)

    assert "at_risk" in result.columns
    assert "risk_probability" in result.columns

    assert result["at_risk"].iloc[0] in [0, 1]
    assert result["risk_probability"].iloc[0] == pytest.approx(0.70)
