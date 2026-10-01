import pandas as pd

from ai_delivery_lab.pipeline.features import build_customer_features


def test_build_customer_features():
    df = pd.DataFrame(
        {
            "CustomerID": ["A", "A", "B"],
            "InvoiceNo": ["100", "101", "200"],
            "StockCode": ["X", "Y", "Z"],
            "InvoiceDate": pd.to_datetime(
                [
                    "2011-01-01",
                    "2011-01-10",
                    "2011-01-05",
                ]
            ),
            "Quantity": [2, 3, 5],
            "Revenue": [20.0, 30.0, 50.0],
            "Country": ["UK", "UK", "France"],
        }
    )

    features = build_customer_features(df)

    assert len(features) == 2
    assert set(features["CustomerID"]) == {"A", "B"}

    customer_a = features[features["CustomerID"] == "A"].iloc[0]

    assert customer_a["Frequency"] == 2
    assert customer_a["TotalQuantity"] == 5
    assert customer_a["MonetaryValue"] == 50.0
    assert customer_a["UniqueProducts"] == 2