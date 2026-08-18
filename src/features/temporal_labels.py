"""Leakage-safe observation/holdout features for repeat-purchase modeling."""
from __future__ import annotations
import pandas as pd


def build_temporal_dataset(sales: pd.DataFrame, cutoff: str | pd.Timestamp, holdout_days: int = 90) -> pd.DataFrame:
    data = sales.copy()
    data["invoice_date"] = pd.to_datetime(data["invoice_date"])
    cutoff = pd.Timestamp(cutoff)
    holdout_end = cutoff + pd.Timedelta(days=holdout_days)
    obs = data[data["invoice_date"] < cutoff].copy()
    future = data[(data["invoice_date"] >= cutoff) & (data["invoice_date"] < holdout_end)].copy()

    features = obs.groupby("customer_id").agg(
        recency_days=("invoice_date", lambda x: (cutoff - x.max()).days),
        frequency_orders=("invoice_no", "nunique"),
        monetary_value=("sales_amount", "sum"),
        units=("quantity", "sum"),
        unique_products=("stock_code", "nunique"),
        active_days=("invoice_date", lambda x: x.dt.date.nunique()),
        first_purchase=("invoice_date", "min"),
        last_purchase=("invoice_date", "max"),
    ).reset_index()
    features["tenure_days"] = (cutoff - features["first_purchase"]).dt.days
    features["avg_order_value"] = features["monetary_value"] / features["frequency_orders"].clip(lower=1)

    future_buyers = set(future["customer_id"].dropna().unique())
    features["repeat_purchase_next_window"] = features["customer_id"].isin(future_buyers).astype(int)
    features["cutoff_date"] = cutoff
    features["holdout_end"] = holdout_end
    return features
