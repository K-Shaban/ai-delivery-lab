# Demo: Customer Intelligence

## Scenario

The system is given a customer profile derived from historical transaction behaviour.

The customer has:

- **Country:** United Kingdom
- **Recency:** 180 days
- **Frequency:** 2 purchases
- **Total Quantity:** 30
- **Monetary Value:** £120
- **Average Order Value:** £60
- **Unique Products:** 5

The customer is evaluated by three machine-learning models:

```text
Customer Behaviour
        │
        ├── Logistic Regression
        ├── Random Forest
        └── Gradient Boosting
                │
                ▼
        Risk Aggregation
                │
                ▼
        73.8% Risk Probability
                │
                ▼
            High Risk
                │
                ▼
      Retention Outreach
                │
                ▼
       Claude / Bedrock
                │
                ▼
    Business Explanation
```

## Prediction

The three model probabilities are combined using a simple average.

The resulting aggregated inactivity-risk probability is:

**73.8%**

The customer is therefore classified as:

**High Risk**

The business recommendation is:

> Prioritise the customer for retention outreach.

## API Request

```json
{
  "Recency": 180,
  "Frequency": 2,
  "TotalQuantity": 30,
  "MonetaryValue": 120,
  "AverageOrderValue": 60,
  "UniqueProducts": 5,
  "Country": "United Kingdom"
}
```

## Customer Intelligence Response

```json
{
  "risk_assessment": {
    "risk_probability": 0.7377676804702497,
    "risk_level": "High",
    "summary": "Customer shows signs of potential inactivity based on purchasing behaviour."
  },
  "recommended_action": "Prioritise the customer for retention outreach."
}
```

## AI Explanation

Claude receives the model output and customer behavioural features and produces a business-facing explanation.

The successful response was:

> This UK-based customer has made 2 purchases with a total spend of £120, averaging £60 per order across 5 unique products, and has a recency score of 180 days. Based on these purchasing behaviours, the model has assigned a high risk probability of 73.8%, indicating signs of potential inactivity. It is recommended that this customer be prioritised for retention outreach.

## What the Demo Demonstrates

The demo shows the complete path from structured customer data to an operational business response:

```text
Customer Data
      ↓
Behavioural Features
      ↓
Multiple ML Models
      ↓
Risk Aggregation
      ↓
Customer Risk Assessment
      ↓
Business Recommendation
      ↓
Claude Explanation
```

The machine-learning models determine the underlying risk assessment. Claude is used to explain the supplied assessment in business language rather than determine the underlying risk score.