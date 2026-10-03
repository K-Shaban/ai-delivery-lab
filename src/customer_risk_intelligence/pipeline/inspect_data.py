from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[3]
DATA_PATH = PROJECT_ROOT / "data" / "raw" / "Online Retail.xlsx"


def load_data() -> pd.DataFrame:
    """Load the raw Online Retail dataset."""
    return pd.read_excel(DATA_PATH)


def inspect_data(df: pd.DataFrame) -> None:
    """Print a basic data-quality and structure summary."""
    print("\n--- Dataset Shape ---")
    print(df.shape)

    print("\n--- Columns ---")
    print(df.columns.tolist())

    print("\n--- Data Types ---")
    print(df.dtypes)

    print("\n--- Missing Values ---")
    print(df.isna().sum())

    print("\n--- Duplicate Rows ---")
    print(df.duplicated().sum())

    print("\n--- Sample ---")
    print(df.head())


if __name__ == "__main__":
    data = load_data()
    inspect_data(data)
