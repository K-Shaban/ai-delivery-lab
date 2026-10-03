from customer_risk_intelligence.evaluation import evaluate_classifier


def test_evaluate_classifier():
    y_true = [0, 0, 1, 1]
    predictions = [0, 1, 1, 1]
    probabilities = [0.1, 0.6, 0.8, 0.9]

    metrics = evaluate_classifier(
        y_true,
        predictions,
        probabilities,
    )

    assert metrics["accuracy"] == 0.75
    assert metrics["precision"] == 2 / 3
    assert metrics["recall"] == 1.0
    assert "roc_auc" in metrics
