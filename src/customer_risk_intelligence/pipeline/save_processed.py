from pathlib import Path

from customer_risk_intelligence.pipeline.preprocess import clean_transactions, load_data


PROJECT_ROOT = Path(__file__).resolve().parents[3]
OUTPUT_PATH = PROJECT_ROOT / "data" / "processed" / "transactions_clean.csv"


def main() -> None:
    raw = load_data()
    cleaned = clean_transactions(raw)

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    cleaned.to_csv(OUTPUT_PATH, index=False)

    print(f"Saved {len(cleaned):,} rows")
    print(f"Customers: {cleaned['CustomerID'].nunique():,}")
    print(f"Output: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
