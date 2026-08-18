# Data

Raw datasets are intentionally excluded from Git.

## Core source — Online Retail II

CustomerIQ uses the UCI Machine Learning Repository **Online Retail II** dataset as its historical transaction source.

- Provider: UCI Machine Learning Repository
- Dataset: Online Retail II
- DOI: https://doi.org/10.24432/C5CG6D
- License: CC BY 4.0
- Source page: https://archive.ics.uci.edu/dataset/502/online+retail+ii

The dataset contains real transactions from a UK-based non-store retailer. CustomerIQ does not claim that these historical transactions are current.

## Reproducible download

From the repository root run:

```bash
python scripts/download_data.py
```

This downloads the official UCI archive and extracts the workbook to:

```text
data/raw/online_retail_II.xlsx
```

Then run the analytical preparation pipeline:

```bash
python -m src.data.prepare_retail --input data/raw/online_retail_II.xlsx
```

Raw and generated analytical data are gitignored. This keeps the repository lightweight while preserving reproducibility and provenance.

## Current/live context

A separate current-data layer is planned for public economic indicators. These will be clearly identified as current contextual data and will not be merged into 2009–2011 transactions as if they were contemporaneous customer features.
