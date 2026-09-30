# Data

This directory contains data used by the AI Delivery Lab project.

## Data source

The initial use case uses the **Online Retail** transactional dataset.

The dataset contains historical customer transactions including:

- Invoice number
- Product description
- Quantity
- Invoice date
- Unit price
- Customer ID
- Country

## Data handling

Raw source data is intentionally not committed to Git.

The pipeline will progressively transform the raw transactional data into reproducible customer-level features for machine learning.

## Planned data flow

```text
Raw Online Retail Data
        ↓
Data Validation
        ↓
Cleaning
        ↓
Feature Engineering
        ↓
Customer-Level Dataset
        ↓
Machine Learning