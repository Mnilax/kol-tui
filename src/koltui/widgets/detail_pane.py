"""Detail panel showing expanded info for a selected channel."""

from __future__ import annotations

from textual.app import ComposeResult
from textual.containers import Vertical
from textual.widgets import Static

from koltui.data import Channel
from koltui.theme import format_number


class DetailPane(Vertical):
    """Expanded detail view for a selected channel."""

    DEFAULT_CSS = """
    DetailPane {
        height: 12;
        background: $surface;
        padding: 1 2;
        border-top: solid $accent;
    }
    """

    def compose(self) -> ComposeResult:
        yield Static("[dim]Select a channel to see details[/dim]", id="detail-content")

    def show_channel(self, ch: Channel) -> None:
        """Update the detail pane with channel info."""
        parts = [f"[b]{ch.handle}[/b] ({ch.platform})"]
        if ch.region:
            parts[0] += f"  {ch.region}"
        parts.append("")

        metrics = []
        metrics.append(f"Subscribers: {format_number(ch.subscribers)}")
        metrics.append(f"Reach: {format_number(ch.reach)}")
        metrics.append(f"Avg Views: {format_number(ch.avg_views)}")
        if ch.er_pct is not None:
            metrics.append(f"ER%: {ch.er_pct:.1f}%")
        if ch.cpm is not None:
            metrics.append(f"CPM: ${ch.cpm:.1f}")
        if ch.price is not None:
            metrics.append(f"Price: ${ch.price:.0f}")
        if ch.frequency is not None:
            metrics.append(f"Posts/week: {ch.frequency:.1f}")
        parts.append("  |  ".join(metrics))

        if ch.fraud_flags:
            parts.append("")
            parts.append("[b]Fraud Flags:[/b]")
            for f in ch.fraud_flags:
                parts.append(f"  [red]⚠ {f}[/red]")
        else:
            parts.append("\n[green]✓ No fraud flags[/green]")

        content = "\n".join(parts)
        self.query_one("#detail-content", Static).update(content)
