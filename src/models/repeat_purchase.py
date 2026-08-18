"""Interpretable repeat-purchase propensity baseline with time-derived labels."""
from __future__ import annotations
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score, average_precision_score, classification_report
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

FEATURES = ["recency_days", "frequency_orders", "monetary_value", "units", "unique_products", "active_days", "tenure_days", "avg_order_value"]
TARGET = "repeat_purchase_next_window"


def fit_repeat_purchase(train: pd.DataFrame, test: pd.DataFrame):
    pre = ColumnTransformer([("numeric", Pipeline([
        ("impute", SimpleImputer(strategy="median")),
        ("scale", StandardScaler()),
    ]), FEATURES)])
    model = Pipeline([
        ("preprocess", pre),
        ("model", LogisticRegression(max_iter=2000, class_weight="balanced")),
    ])
    model.fit(train[FEATURES], train[TARGET])
    prob = model.predict_proba(test[FEATURES])[:, 1]
    pred = (prob >= 0.5).astype(int)
    metrics = {
        "roc_auc": roc_auc_score(test[TARGET], prob),
        "pr_auc": average_precision_score(test[TARGET], prob),
        "classification_report": classification_report(test[TARGET], pred, output_dict=True),
    }
    scored = test[["customer_id", TARGET]].copy()
    scored["purchase_probability"] = prob
    return model, metrics, scored
