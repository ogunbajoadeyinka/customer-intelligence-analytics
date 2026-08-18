"""Download the UCI Online Retail II dataset without committing raw data to Git.

Usage:
    python scripts/download_data.py

The script downloads the official UCI-hosted ZIP, verifies the archive can be
opened, extracts the Excel workbook into data/raw, and prints the resulting path.
"""
from __future__ import annotations

import io
from pathlib import Path
import shutil
import urllib.request
import zipfile

DATA_URL = "https://archive.ics.uci.edu/static/public/502/online+retail+ii.zip"
RAW_DIR = Path("data/raw")
EXPECTED_XLSX = RAW_DIR / "online_retail_II.xlsx"


def download() -> Path:
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    if EXPECTED_XLSX.exists():
        print(f"Dataset already exists: {EXPECTED_XLSX}")
        return EXPECTED_XLSX

    print("Downloading Online Retail II from the UCI Machine Learning Repository...")
    request = urllib.request.Request(DATA_URL, headers={"User-Agent": "CustomerIQ/1.0"})
    with urllib.request.urlopen(request, timeout=120) as response:
        payload = response.read()

    with zipfile.ZipFile(io.BytesIO(payload)) as archive:
        xlsx_members = [n for n in archive.namelist() if n.lower().endswith(".xlsx")]
        if not xlsx_members:
            raise RuntimeError("UCI archive did not contain an .xlsx workbook")
        member = xlsx_members[0]
        with archive.open(member) as src, EXPECTED_XLSX.open("wb") as dst:
            shutil.copyfileobj(src, dst)

    print(f"Saved dataset to {EXPECTED_XLSX} ({EXPECTED_XLSX.stat().st_size / 1_000_000:.1f} MB)")
    return EXPECTED_XLSX


if __name__ == "__main__":
    download()
