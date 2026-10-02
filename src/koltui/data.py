"""Data loading for KOL TUI — reads CSV/JSON exports from kol-toolkit."""

from __future__ import annotations

import csv
import json
import math
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class Channel:
    """Unified channel record for the TUI."""

    handle: str
    platform: str = "tg"
    region: str = ""
    subscribers: int = 0
    reach: int = 0
    avg_views: float = 0.0
    er_pct: float | None = None
    cpm: float | None = None
    frequency: float | None = None
    fraud_flags: list[str] = field(default_factory=list)
    price: float | None = None


def load_csv(path: str) -> list[Channel]:
    """Load channels from a CSV file."""
    channels = []
    with open(path, newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for row in reader:
            channels.append(_row_to_channel(row))
    return channels


def load_json(path: str) -> list[Channel]:
    """Load channels from a JSON file."""
    with open(path, encoding="utf-8-sig") as f:
        data = json.load(f)

    if isinstance(data, list) and all(isinstance(item, dict) for item in data):
        return [_row_to_channel(item) for item in data]

    raise ValueError("Channel JSON must contain a list of objects")


def load_file(path: str) -> list[Channel]:
    """Auto-detect format and load."""
    p = Path(path)
    if p.suffix.lower() == ".json":
        return load_json(path)
    return load_csv(path)


def _row_to_channel(row: dict) -> Channel:
    """Convert a dict row to a Channel dataclass."""
    flags_raw = row.get("fraud_flags", row.get("Fraud Flags", ""))
    if isinstance(flags_raw, list):
        flags = [str(f.get("message", f.get("code", ""))) if isinstance(f, dict) else str(f) for f in flags_raw]
    elif isinstance(flags_raw, str) and flags_raw:
        flags = [f.strip() for f in flags_raw.split(";") if f.strip()]
    else:
        flags = []

    return Channel(
        handle=row.get("handle", row.get("Handle", "")),
        platform=row.get("platform", row.get("Platform", "tg")),
        region=row.get("region", row.get("Region", "")),
        subscribers=_int(row.get("subscribers", row.get("Subscribers", 0))),
        reach=_int(row.get("reach", row.get("Reach", 0))),
        avg_views=_float(row.get("avg_views", row.get("Avg Views", 0))),
        er_pct=_float_or_none(row.get("er_pct", row.get("ER%"))),
        cpm=_float_or_none(row.get("cpm", row.get("CPM ($)"))),
        frequency=_float_or_none(row.get("frequency", row.get("frequency_per_week", row.get("Posts/week")))),
        fraud_flags=flags,
        price=_float_or_none(row.get("price", row.get("Price ($)"))),
    )


def _int(val) -> int:
    try:
        result = float(str(val).replace(",", ""))
        return int(result) if math.isfinite(result) and result >= 0 else 0
    except (ValueError, TypeError, OverflowError):
        return 0


def _float(val) -> float:
    try:
        result = float(str(val).replace(",", ""))
        return result if math.isfinite(result) and result >= 0 else 0.0
    except (ValueError, TypeError):
        return 0.0


def _float_or_none(val) -> float | None:
    if val is None or val == "":
        return None
    try:
        result = float(str(val).replace(",", ""))
        return result if math.isfinite(result) and result >= 0 else None
    except (ValueError, TypeError):
        return None
