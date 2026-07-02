
from __future__ import annotations

import csv
import hashlib
import json
import logging
import shutil
import time
from contextlib import contextmanager
from dataclasses import dataclass
from datetime import datetime, timedelta
from pathlib import Path
from typing import Callable, Iterable, List, Tuple

import duckdb

EXPECTED_SCHEMA = {
    "order_id": str,
    "customer_id": int,
    "order_date": str,
    "product_category": str,
    "amount": float,
    "quantity": int,
    "status": str,
}

@dataclass
class IngestionConfig:
    base_dir: Path
    source_file: Path
    db_path: Path
    bronze_table: str = "bronze_transactions"

def setup_logger(base_dir: Path) -> logging.Logger:
    logger = logging.getLogger("retail_ingestion")
    logger.setLevel(logging.INFO)
    logger.handlers.clear()

    log_path = base_dir / "logs" / "ingestion.log"
    log_path.parent.mkdir(parents=True, exist_ok=True)

    formatter = logging.Formatter("%(asctime)s %(levelname)s %(message)s")

    fh = logging.FileHandler(log_path, encoding="utf-8")
    fh.setFormatter(formatter)
    logger.addHandler(fh)

    sh = logging.StreamHandler()
    sh.setFormatter(formatter)
    logger.addHandler(sh)
    return logger

def md5_file(path: Path) -> str:
    h = hashlib.md5()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()

def retry_with_backoff(max_retries: int = 3, exception_type=IOError):
    def decorator(func: Callable):
        def wrapper(*args, **kwargs):
            logger = kwargs.get("logger") or getattr(args[0], "logger", None)
            last_exc = None
            for attempt in range(1, max_retries + 1):
                try:
                    return func(*args, **kwargs)
                except exception_type as exc:
                    last_exc = exc
                    if attempt == max_retries:
                        msg = f"Source read failed after {max_retries} retries: {exc}"
                        if logger:
                            logger.error(msg)
                        raise IOError(msg) from exc
                    wait_seconds = 2 ** attempt
                    if logger:
                        logger.warning(f"Transient source read failure on attempt {attempt}/{max_retries}. Retrying in {wait_seconds}s. Error: {exc}")
                    time.sleep(wait_seconds)
            raise last_exc
        return wrapper
    return decorator

class DuckDBIngestionModule:
    def __init__(self, config: IngestionConfig):
        self.config = config
        self.base_dir = config.base_dir
        self.source_file = config.source_file
        self.db_path = config.db_path
        self.dead_dir = self.base_dir / "dead_letter"
        self.check_dir = self.base_dir / "checkpoints"
        self.logs_dir = self.base_dir / "logs"
        self.dead_dir.mkdir(parents=True, exist_ok=True)
        self.check_dir.mkdir(parents=True, exist_ok=True)
        self.logs_dir.mkdir(parents=True, exist_ok=True)
        self.logger = setup_logger(self.base_dir)

    @contextmanager
    def connect(self):
        con = duckdb.connect(str(self.db_path))
        try:
            yield con
        finally:
            con.close()

    @retry_with_backoff(max_retries=3, exception_type=IOError)
    def read_source_rows(self, logger=None):
        if not self.source_file.exists():
            raise IOError(f"Source file not found: {self.source_file}")
        with self.source_file.open("r", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            rows = list(reader)
            headers = reader.fieldnames or []
        return headers, rows

    def validate_schema(self, headers: List[str], rows: List[dict]):
        missing = [col for col in EXPECTED_SCHEMA if col not in headers]
        extra = [col for col in headers if col not in EXPECTED_SCHEMA]
        if missing:
            raise ValueError(f"Schema validation failed: missing columns {missing}")
        if extra:
            self.logger.info(f"Extra columns detected and ignored at ingestion: {extra}")

        type_errors = []
        for idx, row in enumerate(rows[:20], start=1):
            for col, typ in EXPECTED_SCHEMA.items():
                raw = row.get(col)
                if raw is None or raw == "":
                    continue
                try:
                    if typ is int:
                        int(raw)
                    elif typ is float:
                        float(raw)
                    else:
                        str(raw)
                except Exception:
                    type_errors.append(f"row {idx} column {col} value {raw!r} not castable to {typ.__name__}")
        if type_errors:
            raise ValueError("Schema validation failed: " + "; ".join(type_errors[:5]))

    def validate_volume(self, rows: List[dict]):
        count = len(rows)
        if count == 0 or count > 10000:
            raise ValueError(f"Volume validation failed: row count {count} is outside allowed range 1..10000")
        if count > 5000:
            self.logger.warning(f"Volume validation warning: row count {count} exceeds 5000")
        self.logger.info(f"Volume validation passed for {count} rows")

    def validate_freshness(self, rows: List[dict]):
        max_date = max(datetime.strptime(r["order_date"], "%Y-%m-%d").date() for r in rows if r.get("order_date"))
        if max_date < (datetime.utcnow().date() - timedelta(days=7)):
            raise ValueError(f"Freshness validation failed: max(order_date)={max_date} is more than 7 days old")
        self.logger.info(f"Freshness validation passed with latest order_date={max_date}")

    def split_valid_invalid_rows(self, rows: List[dict]) -> Tuple[List[dict], List[dict]]:
        valid_rows = []
        invalid_rows = []
        now = datetime.utcnow().isoformat()
        for row in rows:
            reasons = []
            if row.get("order_id") in (None, ""):
                reasons.append("null order_id")
            try:
                amount = float(row.get("amount") or 0)
                if amount < -10000:
                    reasons.append("amount < -10000")
            except Exception:
                reasons.append("invalid amount")
            if reasons:
                invalid_rows.append({
                    "original_row": json.dumps(row, ensure_ascii=False),
                    "rejection_reason": "; ".join(reasons),
                    "rejected_at": now,
                })
            else:
                valid_rows.append(row)
        return valid_rows, invalid_rows

    def write_dead_letter(self, invalid_rows: List[dict]) -> Path | None:
        if not invalid_rows:
            self.logger.info("Dead-letter count: 0")
            return None
        ts = datetime.utcnow().strftime("%Y%m%dT%H%M%S")
        path = self.dead_dir / f"rejected_{ts}.csv"
        with path.open("w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=["original_row", "rejection_reason", "rejected_at"])
            writer.writeheader()
            writer.writerows(invalid_rows)
        self.logger.info(f"Dead-letter count: {len(invalid_rows)} written to {path}")
        return path

    def load_bronze(self, valid_rows: List[dict]):
        with self.connect() as con:
            con.execute(f"""
                CREATE TABLE IF NOT EXISTS {self.config.bronze_table} (
                    order_id VARCHAR,
                    customer_id INTEGER,
                    order_date VARCHAR,
                    product_category VARCHAR,
                    amount DOUBLE,
                    quantity INTEGER,
                    status VARCHAR
                )
            """)
            con.executemany(
                f"INSERT INTO {self.config.bronze_table} VALUES (?, ?, ?, ?, ?, ?, ?)",
                [
                    (
                        r["order_id"],
                        int(r["customer_id"]),
                        r["order_date"],
                        r["product_category"],
                        float(r["amount"]),
                        int(r["quantity"]),
                        r["status"],
                    )
                    for r in valid_rows
                ],
            )
        self.logger.info(f"Loaded {len(valid_rows)} valid rows to bronze table {self.config.bronze_table}")

    def write_checkpoint(self, row_count: int):
        checkpoint = {
            "batch_id": datetime.utcnow().strftime("batch_%Y%m%dT%H%M%S"),
            "timestamp": datetime.utcnow().isoformat(),
            "row_count": row_count,
            "source_file_hash": md5_file(self.source_file),
        }
        path = self.check_dir / "last_successful.json"
        path.write_text(json.dumps(checkpoint, indent=2), encoding="utf-8")
        self.logger.info(f"Checkpoint written: {path}")
        return path

    def run_ingestion(self):
        self.logger.info("Batch start")
        headers, rows = self.read_source_rows(logger=self.logger)
        self.validate_schema(headers, rows)
        self.validate_volume(rows)
        self.validate_freshness(rows)
        valid_rows, invalid_rows = self.split_valid_invalid_rows(rows)
        self.write_dead_letter(invalid_rows)
        self.load_bronze(valid_rows)
        checkpoint = self.write_checkpoint(len(valid_rows))
        return {
            "valid_rows": len(valid_rows),
            "invalid_rows": len(invalid_rows),
            "checkpoint": str(checkpoint),
        }

def reset_environment(config: IngestionConfig):
    for p in [config.base_dir / "dead_letter", config.base_dir / "checkpoints", config.base_dir / "logs"]:
        if p.exists():
            for child in p.iterdir():
                if child.is_file():
                    child.unlink()
    if config.db_path.exists():
        config.db_path.unlink()

def write_csv(path: Path, rows: List[List[str]]):
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerows(rows)

def read_bronze_count(config: IngestionConfig) -> int:
    if not config.db_path.exists():
        return 0
    con = duckdb.connect(str(config.db_path))
    try:
        try:
            return con.execute(f"SELECT COUNT(*) FROM {config.bronze_table}").fetchone()[0]
        except Exception:
            return 0
    finally:
        con.close()

def latest_dead_letter(config: IngestionConfig):
    files = sorted((config.base_dir / "dead_letter").glob("rejected_*.csv"))
    return files[-1] if files else None

def test_clean_run(config: IngestionConfig):
    reset_environment(config)
    mod = DuckDBIngestionModule(config)
    result = mod.run_ingestion()
    dead_files = list((config.base_dir / "dead_letter").glob("rejected_*.csv"))
    cp = config.base_dir / "checkpoints" / "last_successful.json"
    return {
        "result": result,
        "bronze_count": read_bronze_count(config),
        "checkpoint_exists": cp.exists(),
        "dead_letter_files": len(dead_files),
    }

def test_schema_failure(config: IngestionConfig):
    reset_environment(config)
    backup = config.source_file.with_suffix(".schema_backup.csv")
    shutil.copy2(config.source_file, backup)
    with config.source_file.open("r", newline="", encoding="utf-8") as f:
        rows = list(csv.reader(f))
    rows[0][0] = "id"
    write_csv(config.source_file, rows)
    try:
        mod = DuckDBIngestionModule(config)
        try:
            mod.run_ingestion()
            return {"raised": False, "message": "No failure raised"}
        except Exception as e:
            return {
                "raised": True,
                "message": str(e),
                "bronze_count": read_bronze_count(config),
                "checkpoint_exists": (config.base_dir / "checkpoints" / "last_successful.json").exists(),
            }
    finally:
        shutil.move(str(backup), str(config.source_file))

def test_dead_letter(config: IngestionConfig):
    reset_environment(config)
    backup = config.source_file.with_suffix(".dead_backup.csv")
    shutil.copy2(config.source_file, backup)
    with config.source_file.open("r", newline="", encoding="utf-8") as f:
        rows = list(csv.reader(f))
    for i in range(1, min(6, len(rows))):
        rows[i][0] = ""
    write_csv(config.source_file, rows)
    try:
        mod = DuckDBIngestionModule(config)
        result = mod.run_ingestion()
        dl = latest_dead_letter(config)
        dl_count = 0
        reasons = []
        if dl:
            with dl.open("r", newline="", encoding="utf-8") as f:
                rr = list(csv.DictReader(f))
                dl_count = len(rr)
                reasons = sorted(set(r["rejection_reason"] for r in rr))
        return {
            "result": result,
            "bronze_count": read_bronze_count(config),
            "dead_letter_file": str(dl) if dl else None,
            "dead_letter_count": dl_count,
            "reasons": reasons,
        }
    finally:
        shutil.move(str(backup), str(config.source_file))

def test_retry_success(config: IngestionConfig):
    reset_environment(config)
    backup = config.source_file.with_suffix(".retry_backup.csv")
    shutil.copy2(config.source_file, backup)
    config.source_file.unlink()
    mod = DuckDBIngestionModule(config)

    import threading
    def restore():
        time.sleep(3)
        shutil.copy2(backup, config.source_file)
    t = threading.Thread(target=restore, daemon=True)
    t.start()
    try:
        result = mod.run_ingestion()
        return {
            "result": result,
            "bronze_count": read_bronze_count(config),
            "checkpoint_exists": (config.base_dir / "checkpoints" / "last_successful.json").exists(),
        }
    finally:
        if backup.exists():
            backup.unlink()

def main():
    base_dir = Path(__file__).resolve().parent
    config = IngestionConfig(
        base_dir=base_dir,
        source_file=base_dir / "source" / "transactions_batch.csv",
        db_path=base_dir / "retail_ingestion.duckdb",
    )
    out = test_clean_run(config)
    print(json.dumps(out, indent=2))

if __name__ == "__main__":
    main()
