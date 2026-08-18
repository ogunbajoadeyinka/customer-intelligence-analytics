"""Prepare the UCI Online Retail II workbook for CustomerIQ analytics.

Usage:
    python -m src.data.prepare_retail --input data/raw/online_retail_II.xlsx

The script keeps the raw file immutable, standardizes both workbook sheets,
flags cancellations/returns, removes unusable customer records for customer-level
analytics, and writes transaction- and customer-ready parquet/CSV outputs.
"""
from __future__ import annotations

import argparse
from pathlib import Path
import pandas as pd

COLUMN_MAP = {
    "Invoice": "invoice_no",
    "StockCode": "stock_code",
    "Description": "description",
    "Quantity": "quantity",
    "InvoiceDate": "invoice_date",
    "Price": "unit_price",
    "Customer ID": "customer_id",
    "Country": "country",
}


def load_workbook(path: Path) -> pd.DataFrame:
    sheets = pd.read_excel(path, sheet_name=None)
    frames = []
    for sheet_name, frame in sheets.items():
        frame = frame.rename(columns=COLUMN_MAP).copy()
        frame["source_sheet"] = str(sheet_name)
        frames.append(frame)
    return pd.concat(frames, ignore_index=True)


def clean_transactions(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    out.columns = [str(c).strip().lower().replace(" ", "_") for c in out.columns]
    out["invoice_no"] = out["invoice_no"].astype("string").str.strip()
    out["stock_code"] = out["stock_code"].astype("string").str.strip()
    out["description"] = out["description"].astype("string").str.strip()
    out["country"] = out["country"].astype("string").str.strip()
    out["invoice_date"] = pd.to_datetime(out["invoice_date"], errors="coerce")
    out["quantity"] = pd.to_numeric(out["quantity"], errors="coerce")
    out["unit_price"] = pd.to_numeric(out["unit_price"], errors="coerce")
    out["customer_id"] = pd.to_numeric(out["customer_id"], errors="coerce").astype("Int64")

    out["is_cancelled"] = out["invoice_no"].str.upper().str.startswith("C", na=False)
    out["is_return"] = out["quantity"].lt(0) | out["is_cancelled"]
    out["gross_line_value"] = out["quantity"] * out["unit_price"]

    # Keep a traceable cleaned transaction layer; analytical sales exclude
    # returns/cancellations, non-positive prices, and missing customer IDs.
    out = out.dropna(subset=["invoice_no", "stock_code", "invoice_date"])
    out = out.drop_duplicates()
    return out.sort_values(["invoice_date", "invoice_no", "stock_code"]).reset_index(drop=True)


def analytical_sales(cleaned: pd.DataFrame) -> pd.DataFrame:
    mask = (
        cleaned["customer_id"].notna()
        & ~cleaned["is_return"]
        & cleaned["quantity"].gt(0)
        & cleaned["unit_price"].gt(0)
    )
    sales = cleaned.loc[mask].copy()
    sales["sales_amount"] = sales["quantity"] * sales["unit_price"]
    sales["order_date"] = sales["invoice_date"].dt.date
    sales["year_month"] = sales["invoice_date"].dt.to_period("M").astype(str)
    return sales.reset_index(drop=True)


def build_customer_summary(sales: pd.DataFrame) -> pd.DataFrame:
    snapshot = sales["invoice_date"].max() + pd.Timedelta(days=1)
    customers = sales.groupby("customer_id").agg(
        first_purchase=("invoice_date", "min"),
        last_purchase=("invoice_date", "max"),
        orders=("invoice_no", "nunique"),
        units=("quantity", "sum"),
        revenue=("sales_amount", "sum"),
        unique_products=("stock_code", "nunique"),
        country=("country", lambda s: s.mode().iloc[0] if not s.mode().empty else s.iloc[0]),
    ).reset_index()
    customers["recency_days"] = (snapshot - customers["last_purchase"]).dt.days
    customers["tenure_days"] = (snapshot - customers["first_purchase"]).dt.days
    customers["avg_order_value"] = customers["revenue"] / customers["orders"].clip(lower=1)
    return customers.sort_values("revenue", ascending=False).reset_index(drop=True)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, default=Path("data/processed"))
    args = parser.parse_args()

    args.output.mkdir(parents=True, exist_ok=True)
    raw = load_workbook(args.input)
    cleaned = clean_transactions(raw)
    sales = analytical_sales(cleaned)
    customers = build_customer_summary(sales)

    cleaned.to_csv(args.output / "transactions_clean.csv", index=False)
    sales.to_csv(args.output / "sales_analytical.csv", index=False)
    customers.to_csv(args.output / "customer_summary.csv", index=False)

    print({
        "raw_rows": len(raw),
        "clean_rows": len(cleaned),
        "analytical_sales_rows": len(sales),
        "customers": int(customers["customer_id"].nunique()),
        "sales_start": str(sales["invoice_date"].min()),
        "sales_end": str(sales["invoice_date"].max()),
    })


if __name__ == "__main__":
    main()
