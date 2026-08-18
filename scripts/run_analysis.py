"""Run CustomerIQ V1 analysis after the UCI workbook is downloaded locally."""
from pathlib import Path
import json
import joblib
import pandas as pd

from src.data.prepare_retail import load_workbook, clean_transactions, analytical_sales, build_customer_summary
from src.features.rfm import build_rfm
from src.models.segmentation import fit_segmentation
from src.features.temporal_labels import build_temporal_dataset
from src.models.repeat_purchase import fit_repeat_purchase

RAW = Path("data/raw/online_retail_II.xlsx")
OUT = Path("data/processed")
MODELS = Path("models")


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    MODELS.mkdir(parents=True, exist_ok=True)
    raw = load_workbook(RAW)
    clean = clean_transactions(raw)
    sales = analytical_sales(clean)
    customers = build_customer_summary(sales)
    rfm = build_rfm(sales)
    segmented, cluster_profile, cluster_model, k_scores = fit_segmentation(rfm)

    # Two chronological windows: train labels earlier, evaluate on a later period.
    train = build_temporal_dataset(sales, cutoff="2011-06-01", holdout_days=90)
    test = build_temporal_dataset(sales, cutoff="2011-09-01", holdout_days=90)
    common_train = train[train["customer_id"].isin(set(test["customer_id"]))].copy()
    model, metrics, scored = fit_repeat_purchase(common_train, test)

    sales.to_csv(OUT / "fact_sales.csv", index=False)
    customers.to_csv(OUT / "dim_customer_base.csv", index=False)
    segmented.to_csv(OUT / "customer_segments.csv", index=False)
    cluster_profile.to_csv(OUT / "cluster_profile.csv", index=False)
    scored.to_csv(OUT / "customer_scores.csv", index=False)
    if k_scores is not None:
        k_scores.to_csv(OUT / "cluster_validation.csv", index=False)
    joblib.dump(cluster_model, MODELS / "kmeans_rfm.joblib")
    joblib.dump(model, MODELS / "repeat_purchase_logistic.joblib")

    summary = {
        "rows_raw": len(raw),
        "rows_sales": len(sales),
        "customers": int(sales.customer_id.nunique()),
        "orders": int(sales.invoice_no.nunique()),
        "revenue": float(sales.sales_amount.sum()),
        "repeat_purchase_roc_auc": metrics["roc_auc"],
        "repeat_purchase_pr_auc": metrics["pr_auc"],
    }
    (OUT / "analysis_summary.json").write_text(json.dumps(summary, indent=2))
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
