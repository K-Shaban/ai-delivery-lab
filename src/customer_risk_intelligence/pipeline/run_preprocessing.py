from customer_risk_intelligence.pipeline.preprocess import (
    clean_transactions,
    load_data,
    transaction_quality_report,
)


def main() -> None:
    raw = load_data()

    print(f"Raw rows: {len(raw):,}")

    transaction_quality_report(raw)

    cleaned = clean_transactions(raw)

    print(f"\nCleaned rows: {len(cleaned):,}")
    print(f"Rows removed: {len(raw) - len(cleaned):,}")
    print(f"Customers retained: {cleaned['CustomerID'].nunique():,}")
    print(f"Total revenue: ${cleaned['Revenue'].sum():,.2f}")


if __name__ == "__main__":
    main()
