import numpy as np
from fastapi.testclient import TestClient

from customer_risk_intelligence.api import app


client = TestClient(app)


def test_health():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_predict(monkeypatch):
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

    payload = {
        "Recency": 10,
        "Frequency": 5,
        "TotalQuantity": 100,
        "MonetaryValue": 500,
        "AverageOrderValue": 100,
        "UniqueProducts": 10,
        "Country": "United Kingdom",
    }

    response = client.post(
        "/predict",
        json=payload,
    )

    assert response.status_code == 200

    result = response.json()

    assert "at_risk" in result
    assert "risk_probability" in result

    assert result["at_risk"] in [0, 1]
    assert 0 <= result["risk_probability"] <= 1
