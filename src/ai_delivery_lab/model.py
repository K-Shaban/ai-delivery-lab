from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler


NUMERIC_FEATURES = [
    "Recency",
    "Frequency",
    "TotalQuantity",
    "MonetaryValue",
    "AverageOrderValue",
    "UniqueProducts",
]

CATEGORICAL_FEATURES = [
    "Country",
]


def build_preprocessor() -> ColumnTransformer:
    """Build the shared feature preprocessing pipeline."""

    numeric_pipeline = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler()),
        ]
    )

    categorical_pipeline = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="most_frequent")),
            ("onehot", OneHotEncoder(handle_unknown="ignore")),
        ]
    )

    return ColumnTransformer(
        transformers=[
            ("numeric", numeric_pipeline, NUMERIC_FEATURES),
            ("categorical", categorical_pipeline, CATEGORICAL_FEATURES),
        ]
    )


def build_logistic_model() -> Pipeline:
    """Build the baseline logistic regression model."""

    return Pipeline(
        steps=[
            ("preprocessor", build_preprocessor()),
            ("classifier", LogisticRegression(max_iter=1000)),
        ]
    )


def build_random_forest_model() -> Pipeline:
    """Build the Random Forest candidate model."""

    return Pipeline(
        steps=[
            ("preprocessor", build_preprocessor()),
            (
                "classifier",
                RandomForestClassifier(
                    n_estimators=200,
                    random_state=42,
                    n_jobs=-1,
                ),
            ),
        ]
    )


# Backwards-compatible name for the existing baseline code.
def build_model() -> Pipeline:
    """Build the baseline inactivity-risk model."""

    return build_logistic_model()