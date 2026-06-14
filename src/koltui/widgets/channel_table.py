"""Sortable channel data table widget."""

from __future__ import annotations

from textual.widgets import DataTable
from textual.message import Message

from koltui.data import Channel
from koltui.theme import format_number


COLUMNS = [
    ("Handle", "handle", str),
    ("Plat", "platform", str),
    ("Region", "region", str),
    ("Subs", "subscribers", int),
    ("Reach", "reach", int),
    ("ER%", "er_pct", float),
    ("CPM $", "cpm", float),
    ("Posts/wk", "frequency", float),
    ("Flags", "fraud_flags", list),
]


class ChannelTable(DataTable):
    """Sortable DataTable of KOL channels."""

    class ChannelSelected(Message):
        """Emitted when a row is selected."""

        def __init__(self, channel: Channel) -> None:
            super().__init__()
            self.channel = channel

    def __init__(self, channels: list[Channel] | None = None, **kwargs):
        super().__init__(**kwargs)
        self._channels: list[Channel] = channels or []
        self._sort_key: str = "cpm"
        self._sort_reverse: bool = False

    def on_mount(self) -> None:
        self.cursor_type = "row"
        for label, _, _ in COLUMNS:
            self.add_column(label, key=label)
        self.refresh_data(self._channels)

    def refresh_data(self, channels: list[Channel]) -> None:
        """Update the table with new channel data."""
        self._channels = channels
        self.clear()
        for ch in channels:
            flags_str = "⚠" if ch.fraud_flags else "✓"
            self.add_row(
                ch.handle,
                ch.platform,
                ch.region or "—",
                format_number(ch.subscribers),
                format_number(ch.reach),
                f"{ch.er_pct:.1f}" if ch.er_pct is not None else "—",
                f"${ch.cpm:.1f}" if ch.cpm is not None else "—",
                f"{ch.frequency:.1f}" if ch.frequency is not None else "—",
                flags_str,
            )

    def on_data_table_header_selected(self, event: DataTable.HeaderSelected) -> None:
        """Sort by clicked column."""
        col_idx = event.column_index
        if col_idx >= len(COLUMNS):
            return
        _, attr, _ = COLUMNS[col_idx]

        if self._sort_key == attr:
            self._sort_reverse = not self._sort_reverse
        else:
            self._sort_key = attr
            self._sort_reverse = attr in ("cpm",)  # Lower CPM is better, sort ascending by default

        self._channels.sort(
            key=lambda ch: getattr(ch, attr) or (0 if isinstance(getattr(ch, attr, 0), (int, float)) else ""),
            reverse=self._sort_reverse,
        )
        self.refresh_data(self._channels)

    def on_data_table_row_selected(self, event: DataTable.RowSelected) -> None:
        """Emit channel selected message."""
        idx = event.cursor_row
        if 0 <= idx < len(self._channels):
            self.post_message(self.ChannelSelected(self._channels[idx]))
