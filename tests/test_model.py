from sklearn.pipeline import Pipeline

from customer_risk_intelligence.model import (
    build_logistic_model,
    build_random_forest_model,
)


def test_build_logistic_model():
    model = build_logistic_model()

    assert isinstance(model, Pipeline)
    assert "preprocessor" in model.named_steps
    assert "classifier" in model.named_steps


def test_build_random_forest_model():
    model = build_random_forest_model()

    assert isinstance(model, Pipeline)
    assert "preprocessor" in model.named_steps
    assert "classifier" in model.named_steps
