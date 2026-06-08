"""
Tiny CLI that reads events.csv and writes summary.csv with one row per event group.

Usage:
    python -m src.logsum data/sample_events.csv data/summary.csv
"""
from __future__ import annotations

import csv
import re
import sys
from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Iterable, List, Tuple


REQUIRED_COLUMNS = ("timestamp", "level", "service", "message")


@dataclass
class GroupState:
    count: int = 0
    first_seen: datetime | None = None
    last_seen: datetime | None = None


def normalize_level(value: str | None) -> str:
    text = (value or "").strip()
    return text.upper() if text else "UNKNOWN"


def normalize_service(value: str | None) -> str:
    return (value or "").strip()


def normalize_message(value: str | None) -> str:
    text = (value or "").strip()
    return re.sub(r"\s+", " ", text)


def parse_timestamp(raw: str) -> datetime:
    text = raw.strip()
    # Support ISO 8601 with trailing Z.
    if text.endswith("Z"):
        text = text[:-1] + "+00:00"
    return datetime.fromisoformat(text)


def format_timestamp(dt: datetime) -> str:
    if dt.tzinfo is None:
        return dt.isoformat()
    return dt.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


def validate_header(fieldnames: List[str] | None) -> None:
    if not fieldnames:
        raise ValueError("Input file is empty or missing a header row.")
    missing = [name for name in REQUIRED_COLUMNS if name not in fieldnames]
    if missing:
        raise ValueError(f"Missing required columns: {', '.join(missing)}")


def summarize_rows(rows: Iterable[dict]) -> tuple[list[tuple[str, str, str, GroupState]], int]:
    groups: Dict[Tuple[str, str, str], GroupState] = defaultdict(GroupState)
    skipped = 0

    for row in rows:
        try:
            ts = parse_timestamp(row["timestamp"])
        except Exception:
            skipped += 1
            continue

        level = normalize_level(row.get("level"))
        service = normalize_service(row.get("service"))
        message = normalize_message(row.get("message"))
        key = (level, service, message)

        state = groups[key]
        state.count += 1
        if state.first_seen is None or ts < state.first_seen:
            state.first_seen = ts
        if state.last_seen is None or ts > state.last_seen:
            state.last_seen = ts

    ordered = sorted(groups.items(), key=lambda item: (item[0][0], item[0][1], item[0][2]))
    return [(lvl, svc, msg, state) for (lvl, svc, msg), state in ordered], skipped


def write_summary(output_path: Path, grouped_rows: list[tuple[str, str, str, GroupState]]) -> None:
    with output_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["level", "service", "message_normalized", "count", "first_seen", "last_seen"])
        for level, service, message, state in grouped_rows:
            writer.writerow([
                level,
                service,
                message,
                state.count,
                format_timestamp(state.first_seen) if state.first_seen else "",
                format_timestamp(state.last_seen) if state.last_seen else "",
            ])


def main(argv: list[str]) -> int:
    if len(argv) != 3:
        print("Usage: python -m src.logsum <input.csv> <output.csv>", file=sys.stderr)
        return 1

    input_path = Path(argv[1])
    output_path = Path(argv[2])

    try:
        with input_path.open("r", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            validate_header(reader.fieldnames)
            grouped_rows, skipped = summarize_rows(reader)
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 1
    except Exception as exc:
        print(f"Unexpected processing error: {exc}", file=sys.stderr)
        return 2

    try:
        write_summary(output_path, grouped_rows)
    except Exception as exc:
        print(f"Unexpected processing error: {exc}", file=sys.stderr)
        return 2

    if skipped:
        print(f"Warning: skipped {skipped} row(s) with malformed timestamps.", file=sys.stderr)

    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
