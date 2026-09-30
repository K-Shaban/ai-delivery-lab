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