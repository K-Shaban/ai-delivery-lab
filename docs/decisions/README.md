# Architecture & ML Decisions

## ADR-001: Customer Inactivity Risk as the MVP ML Problem

**Status:** Accepted

### Context

The Online Retail dataset contains transactional purchase history but does not provide an explicit customer churn label.

The project needs a supervised machine learning problem that:

- can be derived reproducibly from transaction history
- produces a meaningful customer-level prediction
- can be exposed through an API
- can support an AI analyst agent
- demonstrates a realistic Data & AI delivery workflow

### Decision

The MVP will model **customer inactivity risk**.

A customer will be labelled `at_risk = 1` when they make no purchase during the defined future observation window.

The initial observation window will use historical transaction behaviour, followed by a **90-day future window** for target creation.

### Planned customer features

The initial feature set will include:

- Recency
- Purchase frequency
- Number of unique invoices
- Total quantity purchased
- Total monetary value
- Average order value
- Number of unique products
- Country

### Rationale

This creates a reproducible supervised learning problem directly from the available transaction history while keeping the MVP understandable and business-oriented.

The target definition and feature-generation logic will be implemented as code rather than manually created labels.

### Consequences

The model will depend on a clearly defined temporal split to avoid using future information when generating features.

The target definition may be revised in a later version if model evaluation or business requirements indicate that another definition is more appropriate.


# ADR-002: AWS Container Deployment

## Status

Accepted

## Context

The prediction service needs to move from local development into a cloud environment where it can run as a containerised API.

The initial AWS deployment approach considered ECS Express Mode because it provides a simplified path for deploying containerised applications.

During implementation, the Express Mode deployment encountered infrastructure provisioning permission failures while creating the required load-balancing resources.

Rather than spending additional time debugging the managed Express Mode provisioning workflow, the deployment approach was changed to standard Amazon ECS with AWS Fargate.

## Decision

Use **Amazon ECS with AWS Fargate** as the initial cloud runtime for the prediction service.

The deployment consists of:

- Amazon ECR for container image storage
- Amazon ECS for service and task orchestration
- AWS Fargate for container execution
- Amazon CloudWatch Logs for application logs
- Amazon VPC networking
- EC2 security groups for network access

The initial MVP uses a public Fargate task so that the deployed API can be directly validated.

## Rationale

Standard ECS/Fargate provides explicit control over:

- task definitions
- container configuration
- CPU and memory allocation
- networking
- security groups
- service desired count
- deployment behaviour
- logging configuration

This provides a straightforward path from the locally tested Docker container to a running cloud service without introducing unnecessary infrastructure complexity.

## Consequences

### Positive

- The same Docker image can be used locally and in AWS.
- The deployment configuration is explicit and reproducible.
- Fargate removes the need to manage EC2 instances.
- ECS provides a natural path toward service scaling and deployment automation.
- CloudWatch provides a central location for container logs.
- The architecture can later be extended with an Application Load Balancer.

### Trade-offs

- Standard ECS requires more infrastructure configuration than ECS Express Mode.
- The current MVP exposes the task directly rather than using an Application Load Balancer.
- The current public network configuration is intended for MVP validation rather than a hardened production deployment.

## Validation

The deployed service was validated through the live API.

Health check:

```text
GET /health
HTTP 200
{"status":"ok"}
```

ML inference:

```text
POST /predict
HTTP 200
{"at_risk":0,"risk_probability":0.28558297991606035}
```

The deployment therefore successfully runs the trained model inside an AWS Fargate task and serves live predictions through FastAPI.

## Future Evolution

The deployment can later be hardened by introducing:

- Application Load Balancer
- private application networking
- tighter security-group rules
- HTTPS
- automated ECS deployment through CI/CD
- autoscaling
- improved monitoring and alerting