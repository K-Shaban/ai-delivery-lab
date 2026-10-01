from fastapi.testclient import TestClient

from ai_delivery_lab.api import app


client = TestClient(app)


def test_health():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_predict():
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