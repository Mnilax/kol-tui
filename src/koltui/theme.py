"""Color theme and flag formatting for the KOL TUI."""

from __future__ import annotations

from rich.text import Text


def flag_color(flags: list[str]) -> str:
    """Return a color name based on fraud flag severity."""
    if not flags:
        return "green"
    text = " ".join(flags).lower()
    if "extreme" in text or "ghost" in text or "likely" in text:
        return "red"
    if "high" in text or "spike" in text:
        return "yellow"
    return "yellow"


def cpm_style(cpm_val: float | None) -> str:
    """Color CPM value — lower is better."""
    if cpm_val is None:
        return "dim"
    if cpm_val < 5:
        return "green bold"
    if cpm_val < 15:
        return ""
    if cpm_val < 30:
        return "yellow"
    return "red"


def er_style(er_pct: float | None) -> str:
    """Color ER% value — higher is better."""
    if er_pct is None:
        return "dim"
    if er_pct >= 8:
        return "green bold"
    if er_pct >= 3:
        return "green"
    if er_pct >= 1:
        return ""
    return "red"


def format_number(n: int | float | None) -> str:
    """Format large numbers with K/M suffixes."""
    if n is None:
        return "—"
    if n >= 1_000_000:
        return f"{n/1_000_000:.1f}M"
    if n >= 1_000:
        return f"{n/1_000:.1f}K"
    return str(int(n))
