import pytest
from customer_risk_intelligence.risk_aggregation import aggregate_risk


def test_aggregate_risk():
    result = aggregate_risk(
        logistic_probability=0.60,
        random_forest_probability=0.70,
        gradient_boosting_probability=0.80,
    )

    assert result == pytest.approx(0.70)
