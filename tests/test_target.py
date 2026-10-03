import pandas as pd

from customer_risk_intelligence.pipeline.target import build_inactivity_target


def test_build_inactivity_target():
    df = pd.DataFrame(
        {
            "CustomerID": ["A", "A", "B", "C"],
            "InvoiceDate": pd.to_datetime(
                [
                    "2011-08-01",
                    "2011-09-10",
                    "2011-08-15",
                    "2011-10-15",
                ]
            ),
        }
    )

    target = build_inactivity_target(
        df,
        reference_date=pd.Timestamp("2011-09-01"),
        observation_days=30,
    )

    result = dict(zip(target["CustomerID"], target["at_risk"]))

    assert result["A"] == 0
    assert result["B"] == 1
