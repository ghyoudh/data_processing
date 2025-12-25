# data_processing

Data analytics pipeline for orders data.

- CLI scripts:
  - [scripts/run_load.py](scripts/run_load.py) — load raw CSVs into parquet
  - [scripts/run_clean.py](scripts/run_clean.py) — clean + normalize, write `orders_clean.parquet`
  - [scripts/run_build_analytics.py](scripts/run_build_analytics.py) — join, compute analytics table and reports

- Outputs and reports:
  - processed data: `data/processed/*` (e.g. [data/processed/_run_meta.json](data/processed/_run_meta.json))
  - reports: [reports/summary.md](reports/summary.md) and `reports/figures/`

## Quickstart
### Create virtualenv and install deps:
```bash
python -m venv .venv
.venv/bin/pip install -r requirements.txt
```

### Load raw CSVs to parquet
``bash
python scripts/run_load.py
``

### Clean & normalize
``bash
python scripts/run_clean.py
``

### Build analytics and reports
``bash
python scripts/run_build_analytics.py
``

## Notbooks View
```bash
cd .\notbooks\
jupyter lab
```
- [eda.ipynb](notbooks/eda.ipynb) : Data Quality & Discovery.
- [orders_clear.ipynb](notbooks/orders_clean.ipynb) : The Table of The Data Cleansing & Transformation.
- [orders_load.ipynb](notbooks/orders_load.ipynb) : The Table of The Data Loading.
