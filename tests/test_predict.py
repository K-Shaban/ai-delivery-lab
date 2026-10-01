import pandas as pd

from ai_delivery_lab.predict import predict_inactivity_risk


def test_predict_inactivity_risk():
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
    assert 0 <= result["risk_probability"].iloc[0] <= 1