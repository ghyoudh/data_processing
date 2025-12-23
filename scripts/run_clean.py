import logging
import sys
from pathlib import Path

from data_processing.config import make_paths
from data_processing.io import read_orders_csv, read_users_csv, write_parquet
from data_processing.transforms import (
    enforce_schema,
    missingness_report,
    add_missing_flags,
    normalize_text,
    apply_mapping,
)
from data_processing.quality import (
    require_columns,
    assert_non_empty,
)
from scripts.run_load import ROOT

log = logging.getLogger(__name__)
def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(name)s: %(message)s")
    p = make_paths(ROOT)

    log.info("Loading raw inputs")
    full_path = p.raw / "orders.csv"
    log.info(f"Checking for file at: {full_path.resolve()}")
    orders_raw = read_orders_csv(full_path)

    users = read_users_csv(p.raw / "users.csv")
    log.info("Rows: orders_raw=%s, users=%s", len(orders_raw), len(users))

    require_columns(orders_raw, ["order_id","user_id","amount","quantity","created_at","status"])
    require_columns(users, ["user_id","country","signup_date"])
    assert_non_empty(orders_raw, "orders_raw")
    assert_non_empty(users, "users")

    orders = enforce_schema(orders_raw)

    # Missingness artifact (do this early — before you “fix” missing values)
    rep = missingness_report(orders)
    reports_dir = ROOT / "reports"
    reports_dir.mkdir(parents=True, exist_ok=True)
    rep_path = reports_dir / "missingness_orders.csv"
    rep.to_csv(rep_path, index=True)
    log.info("Wrote missingness report: %s", rep_path)

    # Text normalization + controlled mapping
    status_norm = normalize_text(orders["status"])
    mapping = {"paid": "paid", "refund": "refund", "refunded": "refund"}
    status_clean = apply_mapping(status_norm, mapping)

    orders_clean = (
        orders.assign(status_clean=status_clean)
              .pipe(add_missing_flags, cols=["amount", "quantity"])
    )

    # Task 7: add at least one `assert_in_range(...)` check here (fail fast)

    write_parquet(orders_clean, p.processed / "orders_clean.parquet")
    write_parquet(users, p.processed / "users.parquet")
    log.info("Wrote processed outputs: %s", p.processed)

if __name__ == "__main__":
    main()