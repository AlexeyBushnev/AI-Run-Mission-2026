
from __future__ import annotations

import csv
import json
from dataclasses import dataclass
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import Iterable, List, Dict

import duckdb


@dataclass
class SCD2Config:
    base_dir: Path
    db_path: Path
    source_csv: Path


class SCD2Loader:
    def __init__(self, config: SCD2Config):
        self.config = config
        self.db_path = config.db_path
        self.source_csv = config.source_csv

    def connect(self):
        return duckdb.connect(str(self.db_path))

    def setup_table(self):
        con = self.connect()
        try:
            con.execute("""
                CREATE SEQUENCE IF NOT EXISTS seq_product_key START 1;
            """)
            con.execute("""
                CREATE TABLE IF NOT EXISTS dim_products (
                    product_key INTEGER DEFAULT nextval('seq_product_key'),
                    product_id VARCHAR NOT NULL,
                    product_name VARCHAR NOT NULL,
                    product_category VARCHAR NOT NULL,
                    valid_from DATE NOT NULL,
                    valid_to DATE,
                    is_current BOOLEAN NOT NULL
                );
            """)
        finally:
            con.close()

    def generate_initial_csv(self):
        self.source_csv.parent.mkdir(parents=True, exist_ok=True)
        rows = [["product_id", "product_name", "product_category"]]
        categories = [
            "Electronics", "Home", "Beauty", "Sports", "Toys",
            "Books", "Garden", "Fashion", "Office", "Groceries"
        ]
        for i in range(1, 21):
            pid = f"PROD-{i:03d}"
            pname = f"Product {i:03d}"
            cat = categories[(i - 1) % len(categories)]
            rows.append([pid, pname, cat])
        with self.source_csv.open("w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerows(rows)

    def initial_load(self, valid_from: str = "2024-01-01"):
        self.setup_table()
        con = self.connect()
        try:
            current_count = con.execute("SELECT COUNT(*) FROM dim_products").fetchone()[0]
            if current_count > 0:
                return {"skipped": True, "existing_rows": current_count}
            con.execute(f"""
                INSERT INTO dim_products (product_id, product_name, product_category, valid_from, valid_to, is_current)
                SELECT
                    product_id,
                    product_name,
                    product_category,
                    DATE '{valid_from}' AS valid_from,
                    NULL AS valid_to,
                    TRUE AS is_current
                FROM read_csv_auto('{self.source_csv.as_posix()}')
            """)
            row_count = con.execute("SELECT COUNT(*) FROM dim_products").fetchone()[0]
            return {"skipped": False, "row_count": row_count}
        finally:
            con.close()

    def incremental_load(self, updates: List[Dict[str, str]], change_date: str):
        self.setup_table()
        con = self.connect()
        changed = 0
        skipped = 0
        change_dt = datetime.strptime(change_date, "%Y-%m-%d").date()
        prev_dt = (change_dt - timedelta(days=1)).isoformat()

        try:
            for upd in updates:
                pid = upd["product_id"]
                pname = upd["product_name"]
                pcat = upd["product_category"]

                current_row = con.execute("""
                    SELECT product_id, product_name, product_category, valid_from, valid_to, is_current
                    FROM dim_products
                    WHERE product_id = ? AND is_current = TRUE
                """, [pid]).fetchone()

                if current_row is None:
                    # allow late new inserts if ever needed
                    exists_same_version = con.execute("""
                        SELECT COUNT(*)
                        FROM dim_products
                        WHERE product_id = ? AND valid_from = CAST(? AS DATE) AND product_category = ?
                    """, [pid, change_date, pcat]).fetchone()[0]
                    if exists_same_version == 0:
                        con.execute("""
                            INSERT INTO dim_products (product_id, product_name, product_category, valid_from, valid_to, is_current)
                            VALUES (?, ?, ?, CAST(? AS DATE), NULL, TRUE)
                        """, [pid, pname, pcat, change_date])
                        changed += 1
                    else:
                        skipped += 1
                    continue

                _, current_name, current_category, current_valid_from, _, _ = current_row

                # unchanged record => do nothing
                if current_name == pname and current_category == pcat:
                    skipped += 1
                    continue

                # idempotency guard: if target version already exists, do not insert again or modify old row again
                exists_same_version = con.execute("""
                    SELECT COUNT(*)
                    FROM dim_products
                    WHERE product_id = ? AND valid_from = CAST(? AS DATE) AND product_category = ?
                """, [pid, change_date, pcat]).fetchone()[0]

                if exists_same_version > 0:
                    skipped += 1
                    continue

                # close old current row only once
                con.execute("""
                    UPDATE dim_products
                    SET valid_to = CAST(? AS DATE), is_current = FALSE
                    WHERE product_id = ? AND is_current = TRUE
                """, [prev_dt, pid])

                con.execute("""
                    INSERT INTO dim_products (product_id, product_name, product_category, valid_from, valid_to, is_current)
                    VALUES (?, ?, ?, CAST(? AS DATE), NULL, TRUE)
                """, [pid, pname, pcat, change_date])
                changed += 1

            return {"changed_rows": changed, "skipped_rows": skipped}
        finally:
            con.close()

    def verification_queries(self):
        con = self.connect()
        try:
            row_count = con.execute("SELECT COUNT(*) FROM dim_products").fetchone()[0]
            current_count = con.execute("SELECT COUNT(*) FROM dim_products WHERE is_current = TRUE").fetchone()[0]
            distinct_product_ids = con.execute("SELECT COUNT(DISTINCT product_id) FROM dim_products").fetchone()[0]
            historical_count = con.execute("SELECT COUNT(*) FROM dim_products WHERE is_current = FALSE").fetchone()[0]
            duplicate_current = con.execute("""
                SELECT COUNT(*)
                FROM (
                    SELECT product_id
                    FROM dim_products
                    WHERE is_current = TRUE
                    GROUP BY product_id
                    HAVING COUNT(*) > 1
                ) t
            """).fetchone()[0]
            top_changed = con.execute("""
                SELECT product_id, COUNT(*) AS row_count
                FROM dim_products
                GROUP BY product_id
                ORDER BY row_count DESC, product_id
                LIMIT 5
            """).fetchall()
            old_rows = con.execute("""
                SELECT product_id, product_name, product_category, valid_from, valid_to, is_current
                FROM dim_products
                WHERE is_current = FALSE
                ORDER BY product_id
            """).fetchall()
            return {
                "row_count": row_count,
                "current_count": current_count,
                "distinct_product_ids": distinct_product_ids,
                "historical_count": historical_count,
                "duplicate_current_count": duplicate_current,
                "top_changed": top_changed,
                "old_rows": old_rows,
            }
        finally:
            con.close()


def run_all(base_dir: str):
    base = Path(base_dir)
    cfg = SCD2Config(
        base_dir=base,
        db_path=base / "scd2.duckdb",
        source_csv=base / "source" / "products.csv",
    )
    if cfg.db_path.exists():
        cfg.db_path.unlink()

    loader = SCD2Loader(cfg)
    loader.generate_initial_csv()

    initial = loader.initial_load(valid_from="2024-01-01")
    after_initial = loader.verification_queries()

    updates = [
        {"product_id": "PROD-001", "product_name": "Product 001", "product_category": "Home Tech"},
        {"product_id": "PROD-007", "product_name": "Product 007", "product_category": "Fitness"},
        {"product_id": "PROD-015", "product_name": "Product 015", "product_category": "Smart Home"},
    ]

    first_incremental = loader.incremental_load(updates, change_date="2024-06-01")
    after_first_incremental = loader.verification_queries()

    second_incremental = loader.incremental_load(updates, change_date="2024-06-01")
    after_second_incremental = loader.verification_queries()

    # leap-year boundary verification helper
    leap_updates = [
        {"product_id": "PROD-002", "product_name": "Product 002", "product_category": "Home Living"}
    ]
    leap_first = loader.incremental_load(leap_updates, change_date="2024-03-01")
    leap_snapshot = loader.verification_queries()
    con = loader.connect()
    try:
        leap_old = con.execute("""
            SELECT product_id, valid_to
            FROM dim_products
            WHERE product_id = 'PROD-002' AND is_current = FALSE
            ORDER BY valid_from
            LIMIT 1
        """).fetchone()
    finally:
        con.close()

    return {
        "initial": initial,
        "after_initial": after_initial,
        "first_incremental": first_incremental,
        "after_first_incremental": after_first_incremental,
        "second_incremental": second_incremental,
        "after_second_incremental": after_second_incremental,
        "leap_first": leap_first,
        "leap_old_row": leap_old,
    }


if __name__ == "__main__":
    import sys
    out = run_all(sys.argv[1] if len(sys.argv) > 1 else ".")
    print(json.dumps(out, indent=2, default=str))
