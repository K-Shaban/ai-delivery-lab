import pandas as pd


def build_inactivity_target(
    df: pd.DataFrame,
    reference_date: pd.Timestamp,
    observation_days: int = 90,
) -> pd.DataFrame:
    """
    Create a customer-level inactivity target.

    at_risk = 1 if the customer makes no purchase during the
    observation window after the reference date.
    """

    observation_end = reference_date + pd.Timedelta(days=observation_days)

    feature_transactions = df[df["InvoiceDate"] <= reference_date]

    future_transactions = df[
        (df["InvoiceDate"] > reference_date)
        & (df["InvoiceDate"] <= observation_end)
    ]

    customers = feature_transactions["CustomerID"].unique()

    future_customers = set(future_transactions["CustomerID"].unique())

    target = pd.DataFrame({"CustomerID": customers})

    target["at_risk"] = (
        ~target["CustomerID"].isin(future_customers)
    ).astype(int)

    return target
