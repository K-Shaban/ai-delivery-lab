def aggregate_risk(
    logistic_probability: float,
    random_forest_probability: float,
    gradient_boosting_probability: float,
) -> float:
    """Combine model risk probabilities using a simple average."""
    return (
        logistic_probability
        + random_forest_probability
        + gradient_boosting_probability
    ) / 3