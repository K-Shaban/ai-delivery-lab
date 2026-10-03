def build_customer_insight(
    risk_probability: float,
    at_risk: int,
) -> dict[str, float | str]:
    """Convert model output into a simple business-facing insight."""

    if risk_probability >= 0.70:
        risk_level = "High"
        recommended_action = "Prioritise the customer for retention outreach."
    elif risk_probability >= 0.40:
        risk_level = "Medium"
        recommended_action = "Consider targeted engagement with the customer."
    else:
        risk_level = "Low"
        recommended_action = "Continue normal customer engagement."

    if at_risk == 1:
        summary = (
            "Customer shows signs of potential inactivity "
            "based on purchasing behaviour."
        )
    else:
        summary = (
            "Customer currently shows no elevated inactivity risk "
            "based on purchasing behaviour."
    )

    return {
        "risk_probability": risk_probability,
        "risk_level": risk_level,
        "customer_summary": summary,
        "recommended_action": recommended_action,
    }
