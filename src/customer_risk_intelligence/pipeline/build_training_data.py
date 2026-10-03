from pathlib import Path

import pandas as pd

from customer_risk_intelligence.pipeline.features import build_customer_features
from customer_risk_intelligence.pipeline.target import build_inactivity_target


PROJECT_ROOT = Path(__file__).resolve().parents[3]

DATA_PATH = PROJECT_ROOT / "data" / "processed" / "transactions_clean.csv"
OUTPUT_PATH = PROJECT_ROOT / "data" / "processed" / "customer_training.csv"

REFERENCE_DATE = pd.Timestamp("2011-09-01")
OBSERVATION_DAYS = 90


def main() -> None:
    df = pd.read_csv(
        DATA_PATH,
        parse_dates=["InvoiceDate"],
    )

    print(f"Transactions: {len(df):,}")
    print(f"Reference date: {REFERENCE_DATE.date()}")
    print(f"Observation window: {OBSERVATION_DAYS} days")

    # Only transactions available at prediction time.
    feature_transactions = df[
        df["InvoiceDate"] <= REFERENCE_DATE
    ].copy()

    features = build_customer_features(
        feature_transactions,
        reference_date=REFERENCE_DATE,
    )

    target = build_inactivity_target(
        df,
        reference_date=REFERENCE_DATE,
        observation_days=OBSERVATION_DAYS,
    )

    training_data = features.merge(
        target,
        on="CustomerID",
        how="inner",
    )

    OUTPUT_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    training_data.to_csv(
        OUTPUT_PATH,
        index=False,
    )

    print(f"\nFeature customers: {len(features):,}")
    print(f"Target customers: {len(target):,}")
    print(f"Training rows: {len(training_data):,}")

    print("\nTarget distribution:")
    print(training_data["at_risk"].value_counts())

    print("\nTarget proportions:")
    print(training_data["at_risk"].value_counts(normalize=True))

    print(f"\nSaved to: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
