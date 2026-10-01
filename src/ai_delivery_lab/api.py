from typing import Any

import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel

from ai_delivery_lab.assistant import (
    build_customer_brief,
    generate_ai_summary,
)
from ai_delivery_lab.predict import predict_inactivity_risk
from ai_delivery_lab.customer_intelligence import build_customer_insight
from ai_delivery_lab.monitoring import log_prediction, prediction_summary


app = FastAPI(
    title="AI Delivery Lab",
    description="Customer inactivity risk prediction API",
    version="0.1.0",
)


class CustomerFeatures(BaseModel):
    Recency: float
    Frequency: float
    TotalQuantity: float
    MonetaryValue: float
    AverageOrderValue: float
    UniqueProducts: float
    Country: str


class PredictionResponse(BaseModel):
    at_risk: int
    risk_probability: float
    risk_level: str
    customer_summary: str
    recommended_action: str


@app.get("/health")
def health() -> dict[str, str]:
    """Health check endpoint."""

    return {"status": "ok"}


@app.post("/predict", response_model=PredictionResponse)
def predict(customer: CustomerFeatures) -> dict[str, Any]:
    """Predict inactivity risk for a customer."""

    customer_data = pd.DataFrame(
        [customer.model_dump()]
    )

    result = predict_inactivity_risk(customer_data)

    log_prediction(
        at_risk=int(result["at_risk"].iloc[0]),
        risk_probability=float(result["risk_probability"].iloc[0]),
    )
    insight = build_customer_insight(
        risk_probability=float(result["risk_probability"].iloc[0]),
        at_risk=int(result["at_risk"].iloc[0]),
    )
    brief = build_customer_brief(
        customer=customer.model_dump(),
        insight=insight,
    )
    return {
        "at_risk": int(result["at_risk"].iloc[0]),
        "risk_probability": float(result["risk_probability"].iloc[0]),
        **insight,
        "customer_brief": brief,
    }

@app.get("/monitoring")
def monitoring() -> dict[str, float | int]:
    return prediction_summary()

@app.post("/customer-intelligence")
def customer_intelligence(customer: CustomerFeatures) -> dict[str, Any]:
    customer_data = pd.DataFrame([customer.model_dump()])
    result = predict_inactivity_risk(customer_data)

    insight = build_customer_insight(
        risk_probability=float(result["risk_probability"].iloc[0]),
        at_risk=int(result["at_risk"].iloc[0]),
    )

    brief = build_customer_brief(
        customer=customer.model_dump(),
        insight=insight,
    )

    brief["ai_summary"] = generate_ai_summary(brief)

    return brief