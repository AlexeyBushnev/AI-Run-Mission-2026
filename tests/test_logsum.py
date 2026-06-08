
import csv
from pathlib import Path

import src.logsum as logsum


def write_input(tmp_path: Path, csv_text: str) -> tuple[Path, Path]:
    input_path = tmp_path / "events.csv"
    output_path = tmp_path / "summary.csv"
    input_path.write_text(csv_text, encoding="utf-8")
    return input_path, output_path


def read_csv(path: Path):
    with path.open("r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def run_main(input_path: Path, output_path: Path):
    return logsum.main(["src.logsum", str(input_path), str(output_path)])


def test_groups_by_normalized_level_service_and_message(tmp_path):
    csv_text = """timestamp,level,service,message
2026-06-08T09:00:00Z,info,checkout, Payment failed for order 123
2026-06-08T09:05:00Z,INFO,checkout,Payment   failed for order 123
"""
    input_path, output_path = write_input(tmp_path, csv_text)
    rc = run_main(input_path, output_path)
    assert rc == 0
    rows = read_csv(output_path)
    assert len(rows) == 1
    assert rows[0]["level"] == "INFO"
    assert rows[0]["service"] == "checkout"
    assert rows[0]["message_normalized"] == "Payment failed for order 123"
    assert rows[0]["count"] == "2"
    assert rows[0]["first_seen"] == "2026-06-08T09:00:00Z"
    assert rows[0]["last_seen"] == "2026-06-08T09:05:00Z"


def test_missing_level_is_grouped_as_unknown(tmp_path):
    csv_text = """timestamp,level,service,message
2026-06-08T09:10:00Z,,auth,Token refresh needed
"""
    input_path, output_path = write_input(tmp_path, csv_text)
    rc = run_main(input_path, output_path)
    assert rc == 0
    rows = read_csv(output_path)
    assert len(rows) == 1
    assert rows[0]["level"] == "UNKNOWN"


def test_malformed_timestamp_row_is_skipped_with_warning(tmp_path, capsys):
    csv_text = """timestamp,level,service,message
not-a-timestamp,warn,inventory,Stock sync delayed
2026-06-08T09:20:00Z,error,checkout,Card declined
"""
    input_path, output_path = write_input(tmp_path, csv_text)
    rc = run_main(input_path, output_path)
    captured = capsys.readouterr()
    assert rc == 0
    assert "skipped 1 row" in captured.err.lower()
    rows = read_csv(output_path)
    assert len(rows) == 1
    assert rows[0]["level"] == "ERROR"


def test_empty_input_with_header_only_writes_header_only_output(tmp_path):
    csv_text = "timestamp,level,service,message\n"
    input_path, output_path = write_input(tmp_path, csv_text)
    rc = run_main(input_path, output_path)
    assert rc == 0
    assert output_path.read_text(encoding="utf-8").strip() == "level,service,message_normalized,count,first_seen,last_seen"


def test_completely_empty_file_returns_validation_error(tmp_path, capsys):
    input_path, output_path = write_input(tmp_path, "")
    rc = run_main(input_path, output_path)
    captured = capsys.readouterr()
    assert rc == 1
    assert not output_path.exists()
    assert "header" in captured.err.lower() or "empty" in captured.err.lower()


def test_missing_required_column_returns_validation_error(tmp_path, capsys):
    csv_text = """timestamp,level,service
2026-06-08T09:20:00Z,error,checkout
"""
    input_path, output_path = write_input(tmp_path, csv_text)
    rc = run_main(input_path, output_path)
    captured = capsys.readouterr()
    assert rc == 1
    assert not output_path.exists()
    assert "missing required columns" in captured.err.lower()


def test_duplicate_rows_are_counted_normally(tmp_path):
    csv_text = """timestamp,level,service,message
2026-06-08T09:20:00Z,error,checkout,Card declined
2026-06-08T09:20:00Z,error,checkout,Card declined
"""
    input_path, output_path = write_input(tmp_path, csv_text)
    rc = run_main(input_path, output_path)
    assert rc == 0
    rows = read_csv(output_path)
    assert rows[0]["count"] == "2"


def test_cli_usage_error_when_args_missing(capsys):
    rc = logsum.main(["src.logsum"])
    captured = capsys.readouterr()
    assert rc == 1
    assert "usage:" in captured.err.lower()


def test_service_is_trimmed_but_case_sensitive(tmp_path):
    csv_text = """timestamp,level,service,message
2026-06-08T09:00:00Z,info, checkout ,Hello
2026-06-08T09:01:00Z,INFO,Checkout,Hello
"""
    input_path, output_path = write_input(tmp_path, csv_text)
    rc = run_main(input_path, output_path)
    assert rc == 0
    rows = read_csv(output_path)
    assert len(rows) == 2
    assert {row["service"] for row in rows} == {"checkout", "Checkout"}
