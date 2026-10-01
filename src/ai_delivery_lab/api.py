from typing import Any

import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel

from ai_delivery_lab.predict import predict_inactivity_risk


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

    return {
        "at_risk": int(result["at_risk"].iloc[0]),
        "risk_probability": float(
            result["risk_probability"].iloc[0]
        ),
    }