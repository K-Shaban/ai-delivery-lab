# AI Delivery Lab

## Customer Intelligence & Inactivity Risk

### Business Problem

Customer-facing businesses need to identify customers whose purchasing activity is declining so that retention teams can intervene before those customers become inactive.

The challenge is turning historical transaction data into an operational signal that can answer:

> **Which customers are showing signs of inactivity, and how likely are they to become inactive?**

This project develops a data and AI solution for that problem, taking the process from raw transaction data through customer-level risk modelling and into a deployable prediction service.

---

## Solution

The solution converts historical transaction records into customer-level behavioural features and uses them to estimate inactivity risk.

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
Inactivity Risk Model
        │
        ▼
Risk Prediction API
        │
        ▼
Cloud Deployment
        │
        ▼
Future: AI-assisted Customer Intelligence
```

The current system provides a foundation for applications such as:

- identifying customers requiring retention attention
- prioritising customer outreach
- understanding customer purchasing behaviour
- supporting customer intelligence workflows
- providing risk predictions to downstream applications

---

## Data

The initial implementation uses the **Online Retail** transaction dataset.

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

The initial pipeline addresses issues including:

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

## Model

The current implementation compares Logistic Regression and Random Forest models.

| Model | Accuracy | Precision | Recall | F1 | ROC-AUC |
|---|---:|---:|---:|---:|---:|
| Logistic Regression | 0.6762 | 0.6242 | 0.6564 | 0.6399 | 0.7353 |
| Random Forest | 0.6461 | 0.5972 | 0.5911 | 0.5941 | 0.6979 |

The current prediction service uses the Logistic Regression model.

The model produces:

- an inactivity-risk classification
- a probability representing the estimated risk

---

## Prediction Service

The model is exposed through a FastAPI service.

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

Example response:

```json
{
  "at_risk": 0,
  "risk_probability": 0.2856
}
```

The API provides a simple interface for applications or future AI agents to consume the model.

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

The current deployment consists of a Fargate service running the prediction container with CloudWatch logging and an HTTP health check.

### Deployment validation

The deployed service has been tested through both endpoints.

Health check:

```text
HTTP 200
{"status":"ok"}
```

Live model inference:

```text
HTTP 200
{"at_risk":0,"risk_probability":0.28558297991606035}
```

This confirms that the trained model is running successfully within the cloud deployment.

---

## From Prediction to Customer Intelligence

A risk score is useful, but by itself it does not answer the broader business questions a customer operations team may have.

The next stage is to build an AI-assisted customer intelligence layer around the existing data and model.

The planned workflow is:

```text
Business Question
       │
       ▼
AI Agent
       │
       ├── Customer data
       │
       ├── Behaviour analysis
       │
       ├── Inactivity risk model
       │
       └── Business/project knowledge
       │
       ▼
Customer Intelligence Response
```

For example, a future user could ask:

> "Which customers appear most at risk, and what purchasing behaviour is contributing to that assessment?"

The agent would be able to combine customer data, behavioural features, and model predictions rather than relying solely on a language model's generated response.

---

## System Architecture

The current system separates the major stages of the solution:

```text
                    ┌──────────────────┐
                    │  Raw Transactions│
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │ Data Preparation │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │ Feature Pipeline │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │   ML Model       │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │   FastAPI        │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │ Docker / ECR     │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │ ECS / Fargate    │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │ Prediction API   │
                    └──────────────────┘
```

---

## Engineering & Delivery

The solution is structured so that each stage can be developed, tested, and deployed independently.

Current capabilities include:

- reproducible data preparation
- automated tests
- model evaluation
- persisted model artifact
- FastAPI inference service
- Docker containerisation
- GitHub Actions CI
- Amazon ECR
- Amazon ECS / Fargate
- CloudWatch logging
- container health checks

The repository also contains architecture and decision documentation to record how the solution evolves.

---

## Project Structure

```text
ai-delivery-lab/
├── src/
│   └── ai_delivery_lab/
│       ├── model.py
│       ├── evaluation.py
│       ├── predict.py
│       ├── api.py
│       └── pipeline/
├── tests/
├── data/
├── artifacts/
├── notebooks/
├── docs/
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
- [x] Model training and comparison
- [x] Persisted prediction model
- [x] FastAPI prediction service
- [x] Automated tests
- [x] Docker containerisation
- [x] GitHub Actions CI
- [x] Amazon ECR deployment
- [x] ECS/Fargate deployment
- [x] CloudWatch logging
- [x] Live API health validation
- [x] Live ML inference validation

### In Progress

- [ ] AI-assisted customer intelligence
- [ ] Data and ML tools for the AI agent
- [ ] Project knowledge / RAG
- [ ] Monitoring and observability
- [ ] Production deployment hardening
- [ ] End-to-end architecture documentation

---

## Roadmap

The solution will evolve through several stages:

```text
Customer Transaction Data
          │
          ▼
Customer Behaviour
          │
          ▼
Inactivity Risk
          │
          ▼
Operational Prediction API
          │
          ▼
AI-assisted Customer Intelligence
          │
          ▼
Monitoring & Continuous Improvement
```

The objective is to turn historical transaction data into an increasingly useful decision-support capability, while keeping the underlying data, modelling, and operational components traceable and reproducible.