import pandas as pd

from ai_delivery_lab.pipeline.preprocess import clean_transactions


def test_clean_transactions_removes_duplicates_and_missing_customers():
    df = pd.DataFrame(
        {
            "InvoiceNo": ["A", "A", "B"],
            "StockCode": ["X", "X", "Y"],
            "Description": ["Item", "Item", "Item 2"],
            "Quantity": [1, 1, 2],
            "InvoiceDate": pd.to_datetime(
                ["2011-01-01", "2011-01-01", "2011-01-02"]
            ),
            "UnitPrice": [10.0, 10.0, 5.0],
            "CustomerID": [123.0, 123.0, None],
            "Country": ["UK", "UK", "UK"],
        }
    )

    cleaned = clean_transactions(df)

    assert len(cleaned) == 1
    assert cleaned.iloc[0]["CustomerID"] == "123"
    assert cleaned.iloc[0]["Revenue"] == 10.0