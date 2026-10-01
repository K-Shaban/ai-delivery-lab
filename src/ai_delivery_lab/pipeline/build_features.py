from pathlib import Path

import pandas as pd

from ai_delivery_lab.pipeline.features import build_customer_features


PROJECT_ROOT = Path(__file__).resolve().parents[3]
DATA_PATH = PROJECT_ROOT / "data" / "processed" / "transactions_clean.csv"


def main() -> None:
    df = pd.read_csv(DATA_PATH, parse_dates=["InvoiceDate"])

    print(f"Transactions: {len(df):,}")
    print(f"Customers: {df['CustomerID'].nunique():,}")
    print(f"Date range: {df['InvoiceDate'].min()} to {df['InvoiceDate'].max()}")

    features = build_customer_features(df)

    print(f"\nCustomer feature rows: {len(features):,}")
    print("\nFeature columns:")
    print(features.columns.tolist())

    print("\nFeature sample:")
    print(features.head())

    print("\nNumeric feature summary:")
    print(
        features[
            [
                "Recency",
                "Frequency",
                "TotalQuantity",
                "MonetaryValue",
                "AverageOrderValue",
                "UniqueProducts",
            ]
        ].describe()
    )


if __name__ == "__main__":
    main()