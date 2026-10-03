from customer_risk_intelligence import assistant


def test_generate_ai_summary_uses_bedrock(monkeypatch):
    class FakeBedrockClient:
        def converse(self, **kwargs):
            assert kwargs["modelId"] == assistant.BEDROCK_MODEL_ID
            assert kwargs["messages"][0]["role"] == "user"

            return {
                "output": {
                    "message": {
                        "content": [
                            {"text": "Test customer summary"}
                        ]
                    }
                }
            }

    monkeypatch.setattr(
        assistant,
        "bedrock_client",
        FakeBedrockClient(),
    )

    brief = {
        "customer": {
            "Country": "United Kingdom",
            "Recency": 30,
            "Frequency": 5,
            "TotalQuantity": 100,
            "MonetaryValue": 500,
            "AverageOrderValue": 100,
            "UniqueProducts": 20,
        },
        "risk_assessment": {
            "risk_probability": 0.2856,
            "risk_level": "Low",
            "summary": "Customer currently shows relatively low inactivity risk.",
        },
        "recommended_action": "Continue normal customer engagement.",
    }

    result = assistant.generate_ai_summary(brief)

    assert result == "Test customer summary"
