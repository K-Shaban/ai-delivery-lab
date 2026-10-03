import pandas as pd


def build_customer_features(
    df: pd.DataFrame,
    reference_date: pd.Timestamp | None = None,
) -> pd.DataFrame:
    """Build customer-level behavioural features from transactions."""

    if reference_date is None:
        reference_date = df["InvoiceDate"].max() + pd.Timedelta(days=1)

    customer_features = (
        df.groupby("CustomerID")
        .agg(
            Recency=("InvoiceDate", lambda x: (reference_date - x.max()).days),
            Frequency=("InvoiceNo", "nunique"),
            TotalQuantity=("Quantity", "sum"),
            MonetaryValue=("Revenue", "sum"),
            UniqueProducts=("StockCode", "nunique"),
            Country=("Country", "first"),
        )
        .reset_index()
    )

    customer_features["AverageOrderValue"] = (
        customer_features["MonetaryValue"]
        / customer_features["Frequency"]
    )

    return customer_features
