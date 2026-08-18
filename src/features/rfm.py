"""RFM feature engineering and interpretable customer labels."""
from __future__ import annotations
import pandas as pd


def build_rfm(sales: pd.DataFrame, snapshot_date: pd.Timestamp | None = None) -> pd.DataFrame:
    data = sales.copy()
    data["invoice_date"] = pd.to_datetime(data["invoice_date"])
    if snapshot_date is None:
        snapshot_date = data["invoice_date"].max() + pd.Timedelta(days=1)

    rfm = data.groupby("customer_id").agg(
        recency=("invoice_date", lambda x: (snapshot_date - x.max()).days),
        frequency=("invoice_no", "nunique"),
        monetary=("sales_amount", "sum"),
    ).reset_index()

    # Rank-based qcut is robust to duplicate raw values common in frequency.
    rfm["r_score"] = pd.qcut(rfm["recency"].rank(method="first"), 5, labels=[5,4,3,2,1]).astype(int)
    rfm["f_score"] = pd.qcut(rfm["frequency"].rank(method="first"), 5, labels=[1,2,3,4,5]).astype(int)
    rfm["m_score"] = pd.qcut(rfm["monetary"].rank(method="first"), 5, labels=[1,2,3,4,5]).astype(int)
    rfm["rfm_score"] = rfm[["r_score", "f_score", "m_score"]].sum(axis=1)
    rfm["rfm_code"] = rfm["r_score"].astype(str) + rfm["f_score"].astype(str) + rfm["m_score"].astype(str)
    rfm["rfm_segment"] = rfm.apply(_segment, axis=1)
    return rfm


def _segment(row: pd.Series) -> str:
    r, f, m = row["r_score"], row["f_score"], row["m_score"]
    if r >= 4 and f >= 4 and m >= 4:
        return "Champions"
    if r >= 3 and f >= 4:
        return "Loyal"
    if r >= 4 and f <= 3:
        return "Promising"
    if r <= 2 and f >= 4 and m >= 3:
        return "At Risk - High Value"
    if r <= 2 and f <= 2:
        return "Dormant"
    if m >= 4:
        return "High Value"
    return "Core"
