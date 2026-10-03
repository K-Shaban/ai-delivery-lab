# AI Delivery Lab

## Customer Intelligence & Inactivity Risk

### Business Problem

Customer-facing businesses need to identify customers whose purchasing activity is declining so that retention teams can intervene before those customers become inactive.

The challenge is turning historical transaction data into an operational signal that can answer:

> **Which customers are showing signs of inactivity, and how likely are they to become inactive?**

This project develops a data and AI solution for that problem, taking the process from raw transaction data through customer-level risk modelling and into a deployable prediction service and AI-assisted customer intelligence layer.

---

## Solution

The solution converts historical transaction records into customer-level behavioural features, evaluates inactivity risk using multiple machine-learning models, aggregates their predictions, and uses Claude via Amazon Bedrock to explain the resulting assessment.

```text
Transaction History
        │
        ▼
Data Quality & Cleaning
        │
        ▼
Customer Behaviour Features
        │
        ▼
Multiple Risk Models
        │
        ▼
Risk Aggregation
        │
        ▼
Customer Intelligence
        │
        ├── Business Rules
        │
        └── Claude / Amazon Bedrock
        │
        ▼
FastAPI
        │
        ▼
Cloud Deployment
```

The system provides a foundation for:

- identifying customers requiring retention attention
- prioritising customer outreach
- understanding customer purchasing behaviour
- providing risk predictions to downstream applications
- generating business-facing explanations of model outputs

---

## Customer Intelligence

The risk model provides a quantitative assessment, while the customer intelligence layer converts that assessment into a business-facing response.

The workflow is:

```text
Customer Features
       │
       ▼
Three ML Models
       │
       ▼
Aggregated Risk
       │
       ▼
Business Risk Assessment
       │
       ▼
Claude via Amazon Bedrock
       │
       ▼
Business Explanation
```

The business layer assigns a risk level and recommended action based on the aggregated risk probability.

Claude receives the supplied customer features and model assessment and generates a concise explanation.

The LLM does **not** determine the underlying risk probability.

### Example

For a customer with:

```text
Recency:            180 days
Frequency:          2 purchases
Total Quantity:     30
Monetary Value:     £120
Average Order Value: £60
Unique Products:    5
Country:            United Kingdom
```

the system produced:

```text
Risk probability: 73.8%
Risk level:       High
```

with the recommended action:

```text
Prioritise the customer for retention outreach.
```

Claude then produced a business-facing explanation grounded in the supplied customer behaviour and model assessment.

See [the demo](docs/demo/README.md) for the complete example.

---

## Data

The implementation uses the **Online Retail** transaction dataset.

The raw dataset contains:

- Invoice information
- Product information
- Transaction quantities
- Unit prices
- Transaction dates
- Customer identifiers
- Customer countries

The data is transformed from individual transactions into customer-level behavioural information.

### Data preparation

The pipeline addresses issues including:

- duplicate transactions
- missing customer identifiers
- cancelled purchases
- invalid quantities
- invalid prices
- revenue calculation

The cleaned transaction data is then used to construct the modelling dataset.

---

## Customer Behaviour

For each customer, the system calculates behavioural features including:

| Feature | Description |
|---|---|
| Recency | Days since the customer's most recent purchase |
| Frequency | Number of unique invoices |
| Total Quantity | Total quantity purchased |
| Monetary Value | Total customer revenue |
| Average Order Value | Monetary value divided by purchase frequency |
| Unique Products | Number of distinct products purchased |
| Country | Customer country |

These features provide a compact representation of customer purchasing behaviour.

---

## Inactivity Risk

The modelling problem is defined using a temporal observation window.

Customer behaviour is measured up to a cutoff date of **1 September 2011**.

A subsequent **90-day observation period** is then used to determine whether the customer makes another purchase.

```text
Historical behaviour
        │
        │ feature window
        ▼
1 September 2011
        │
        │ 90-day observation period
        ▼
Future purchasing behaviour
```

A customer is labelled:

```text
at_risk = 1
```

when no purchase occurs during the future observation period.

This approach avoids defining inactivity using the same information used to create the prediction features.

---

## Machine-Learning Models

The system evaluates three classification models:

- Logistic Regression
- Random Forest
- Gradient Boosting

Current evaluation results:

| Model | Accuracy | Precision | Recall | F1 | ROC-AUC |
|---|---:|---:|---:|---:|---:|
| Logistic Regression | 0.6762 | 0.6242 | 0.6564 | 0.6399 | 0.7353 |
| Random Forest | 0.6461 | 0.5972 | 0.5911 | 0.5941 | 0.6979 |
| Gradient Boosting | 0.6566 | 0.6061 | 0.6186 | 0.6122 | 0.7178 |

The models are persisted as separate artifacts and used together during prediction.

### Risk aggregation

Each model produces an inactivity-risk probability.

The current implementation combines the three probabilities using a simple arithmetic mean:

```text
aggregated risk =
    (logistic risk
     + random forest risk
     + gradient boosting risk)
    / 3
```

The aggregated probability is then used to produce the `at_risk` classification.

This is intentionally a simple ensemble rather than a tuned or calibrated stacking system.

---

## Prediction Service

The model and customer intelligence functionality are exposed through FastAPI.

### Health

```text
GET /health
```

Response:

```json
{
  "status": "ok"
}
```

### Customer risk prediction

```text
POST /predict
```

Example request:

```json
{
  "Recency": 30,
  "Frequency": 5,
  "TotalQuantity": 100,
  "MonetaryValue": 500,
  "AverageOrderValue": 100,
  "UniqueProducts": 20,
  "Country": "United Kingdom"
}
```

The endpoint returns the aggregated risk assessment together with business-facing risk information.

### Customer intelligence

```text
POST /customer-intelligence
```

This endpoint runs the complete customer intelligence workflow:

```text
Customer Features
        ↓
ML Risk Models
        ↓
Risk Aggregation
        ↓
Business Risk Assessment
        ↓
Claude / Bedrock
        ↓
AI Summary
```

Example response structure:

```json
{
  "customer": {
    "Recency": 180,
    "Frequency": 2,
    "TotalQuantity": 30,
    "MonetaryValue": 120,
    "AverageOrderValue": 60,
    "UniqueProducts": 5,
    "Country": "United Kingdom"
  },
  "risk_assessment": {
    "risk_probability": 0.7378,
    "risk_level": "High",
    "summary": "Customer shows signs of potential inactivity based on purchasing behaviour."
  },
  "recommended_action": "Prioritise the customer for retention outreach.",
  "ai_summary": "Business-facing explanation generated from the supplied customer data and model assessment."
}
```

---

## Cloud Deployment

The prediction service is deployed to AWS using Amazon ECR, Amazon ECS, and AWS Fargate.

```text
Docker Image
     │
     ▼
Amazon ECR
     │
     ▼
ECS Task Definition
     │
     ▼
ECS Service
     │
     ▼
AWS Fargate
     │
     ▼
FastAPI
     │
     ▼
Customer Risk Prediction
```

The deployment consists of a Fargate service running the prediction container with CloudWatch logging and an HTTP health check.

### Deployment validation

The deployed service has been tested through both endpoints.

Health check:

```text
HTTP 200
{"status":"ok"}
```

Live model inference has also been validated successfully through the deployed service.

---

## Engineering & Delivery

The solution is structured so that each stage can be developed, tested, and deployed independently.

Current capabilities include:

- reproducible data preparation
- automated tests
- model evaluation
- three persisted model artifacts
- simple model risk aggregation
- FastAPI inference service
- customer intelligence workflow
- Claude via Amazon Bedrock
- Docker containerisation
- GitHub Actions CI
- Amazon ECR
- Amazon ECS / Fargate
- CloudWatch logging
- container health checks

The repository also contains architecture, decision, and demonstration documentation.

---

## Project Structure

```text
customer-risk-intelligence-pipeline/
├── src/
│   └── customer_risk_intelligence/
│       ├── model.py
│       ├── evaluation.py
│       ├── predict.py
│       ├── api.py
│       ├── customer_intelligence.py
│       ├── assistant.py
│       ├── monitoring.py
│       ├── risk_aggregation.py
│       └── pipeline/
├── tests/
├── data/
├── artifacts/
├── notebooks/
├── docs/
│   ├── architecture/
│   ├── decisions/
│   └── demo/
├── infrastructure/
├── scripts/
├── .github/
│   └── workflows/
├── Dockerfile
├── pyproject.toml
└── README.md
```

---

## Current Status

### Completed

- [x] Transaction data quality assessment
- [x] Transaction cleaning pipeline
- [x] Customer-level feature engineering
- [x] Temporal inactivity-risk definition
- [x] Logistic Regression evaluation
- [x] Random Forest evaluation
- [x] Gradient Boosting evaluation
- [x] Three persisted model artifacts
- [x] Risk probability aggregation
- [x] Customer risk assessment
- [x] FastAPI prediction service
- [x] Customer intelligence endpoint
- [x] Claude via Amazon Bedrock
- [x] Automated tests
- [x] Docker containerisation
- [x] GitHub Actions CI
- [x] Amazon ECR deployment
- [x] ECS/Fargate deployment
- [x] CloudWatch logging
- [x] Live API health validation
- [x] Live ML inference validation
- [x] End-to-end customer intelligence demo

### Future Improvements

- [ ] Production deployment hardening
- [ ] More comprehensive monitoring and observability
- [ ] Model calibration and ensemble evaluation
- [ ] Additional customer intelligence capabilities

---

## Roadmap

The current system establishes a path from transaction data to operational AI-assisted customer intelligence:

```text
Customer Transaction Data
          │
          ▼
Customer Behaviour
          │
          ▼
Multiple Risk Models
          │
          ▼
Risk Aggregation
          │
          ▼
Customer Intelligence
          │
          ▼
AI-assisted Business Explanation
          │
          ▼
Monitoring & Continuous Improvement
```

The objective is to turn historical transaction data into an increasingly useful decision-support capability while keeping the underlying data, modelling, and operational components traceable and reproducible.