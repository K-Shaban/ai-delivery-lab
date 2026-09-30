from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[3]
DATA_PATH = PROJECT_ROOT / "data" / "raw" / "Online Retail.xlsx"


def load_data() -> pd.DataFrame:
    """Load the raw Online Retail dataset."""
    return pd.read_excel(DATA_PATH)


def clean_transactions(df: pd.DataFrame) -> pd.DataFrame:
    """Clean transactions for customer-level purchase analysis."""
    cleaned = df.copy()

    # Remove exact duplicate transactions.
    cleaned = cleaned.drop_duplicates()

    # Customer-level modelling requires a known customer ID.
    cleaned = cleaned.dropna(subset=["CustomerID"])

    # Keep completed purchases for the MVP.
    cleaned = cleaned[cleaned["Quantity"] > 0]

    # Exclude invalid negative prices.
    cleaned = cleaned[cleaned["UnitPrice"] >= 0]

    # Standardise customer ID representation.
    cleaned["CustomerID"] = cleaned["CustomerID"].astype(int).astype(str)

    # Calculate transaction revenue.
    cleaned["Revenue"] = cleaned["Quantity"] * cleaned["UnitPrice"]

    return cleaned

def transaction_quality_report(df: pd.DataFrame) -> None:
    """Print transaction-level quality statistics."""
    print("\n--- Transaction Quality ---")

    print(f"Negative quantities: {(df['Quantity'] < 0).sum():,}")
    print(f"Zero quantities: {(df['Quantity'] == 0).sum():,}")

    print(f"Negative unit prices: {(df['UnitPrice'] < 0).sum():,}")
    print(f"Zero unit prices: {(df['UnitPrice'] == 0).sum():,}")

    cancellations = df["InvoiceNo"].astype(str).str.startswith("C")
    print(f"Cancellation invoices: {cancellations.sum():,}")

    print("\n--- Quantity Statistics ---")
    print(df["Quantity"].describe())

    print("\n--- Unit Price Statistics ---")
    print(df["UnitPrice"].describe())