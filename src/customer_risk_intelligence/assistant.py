from typing import Any

import boto3

BEDROCK_REGION = "ap-southeast-2"
BEDROCK_MODEL_ID = "au.anthropic.claude-sonnet-4-6"

bedrock_client = boto3.client(
    "bedrock-runtime",
    region_name=BEDROCK_REGION,
)


def build_customer_brief(
    customer: dict[str, Any],
    insight: dict[str, str],
) -> dict[str, Any]:
    """Build a structured customer briefing from model and business outputs."""

    return {
        "customer": customer,
        "risk_assessment": {
            "risk_probability": insight["risk_probability"],
            "risk_level": insight["risk_level"],
            "summary": insight["customer_summary"],
        },
        "recommended_action": insight["recommended_action"],
    }

def generate_ai_summary(brief: dict[str, Any]) -> str:
    """Generate a business-facing summary using Claude via Amazon Bedrock."""

    risk = brief["risk_assessment"]
    customer = brief["customer"]

    prompt = f"""
You are a customer intelligence assistant.

Explain the following customer risk assessment to a business user.

Customer country: {customer["Country"]}
Recency: {customer["Recency"]}
Frequency: {customer["Frequency"]}
Total quantity: {customer["TotalQuantity"]}
Monetary value: {customer["MonetaryValue"]}
Average order value: {customer["AverageOrderValue"]}
Unique products: {customer["UniqueProducts"]}

Model risk probability: {risk["risk_probability"]:.1%}
Risk level: {risk["risk_level"]}
Model summary: {risk["summary"]}
Recommended action: {brief["recommended_action"]}

Write a concise business explanation in 2-3 sentences.

Rules:
- Only state facts directly supported by the supplied customer features.
- Do not infer when individual purchases occurred from Recency or Frequency.
- Do not describe Frequency as a number of orders within a particular time period.
- Do not invent trends, causes, customer intent, or future behaviour.
- Do not change or reinterpret the model's risk level or probability.
- Do not introduce a different recommended action.
- Treat the supplied risk level as authoritative.
- Describe a Medium risk as medium risk, not low risk.
- Do not use wording that contradicts the supplied risk level.
"""

    response = bedrock_client.converse(
        modelId=BEDROCK_MODEL_ID,
        messages=[
            {
                "role": "user",
                "content": [{"text": prompt}],
            }
        ],
        inferenceConfig={
            "maxTokens": 200,
            "temperature": 0.2,
        },
    )

    return response["output"]["message"]["content"][0]["text"]
