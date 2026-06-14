"""KOL Analytics TUI Dashboard — main application."""

from __future__ import annotations

import sys
from pathlib import Path

from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Horizontal, Vertical
from textual.widgets import Footer, Header

from koltui.data import Channel, load_file
from koltui.widgets.channel_table import ChannelTable
from koltui.widgets.detail_pane import DetailPane
from koltui.widgets.filters import FilterPanel


class KOLDashboard(App):
    """Terminal dashboard for KOL influencer analytics."""

    TITLE = "KOL Analytics Dashboard"
    CSS = """
    Screen {
        layout: vertical;
    }
    #main-area {
        height: 1fr;
    }
    #table-container {
        width: 1fr;
    }
    """

    BINDINGS = [
        Binding("q", "quit", "Quit"),
        Binding("f", "toggle_filters", "Filters"),
        Binding("/", "focus_search", "Search"),
    ]

    def __init__(self, data_path: str | None = None, **kwargs):
        super().__init__(**kwargs)
        self._data_path = data_path
        self._all_channels: list[Channel] = []
        self._show_filters = True

    def compose(self) -> ComposeResult:
        yield Header()
        with Horizontal(id="main-area"):
            regions = sorted(set(ch.region for ch in self._all_channels if ch.region))
            yield FilterPanel(regions=regions, id="filter-panel")
            with Vertical(id="table-container"):
                yield ChannelTable(self._all_channels, id="channel-table")
        yield DetailPane(id="detail-pane")
        yield Footer()

    def on_mount(self) -> None:
        if self._data_path:
            self._all_channels = load_file(self._data_path)
            table = self.query_one("#channel-table", ChannelTable)
            table.refresh_data(self._all_channels)

    def on_filter_panel_filters_changed(self, event: FilterPanel.FiltersChanged) -> None:
        """Apply filters to the channel table."""
        filtered = self._all_channels

        if event.search:
            search_lower = event.search.lower()
            filtered = [ch for ch in filtered if search_lower in ch.handle.lower()]

        if event.region:
            filtered = [ch for ch in filtered if ch.region == event.region]

        if event.max_cpm is not None:
            filtered = [ch for ch in filtered if ch.cpm is not None and ch.cpm <= event.max_cpm]

        if event.min_er is not None:
            filtered = [ch for ch in filtered if ch.er_pct is not None and ch.er_pct >= event.min_er]

        table = self.query_one("#channel-table", ChannelTable)
        table.refresh_data(filtered)

    def on_channel_table_channel_selected(self, event: ChannelTable.ChannelSelected) -> None:
        """Show selected channel in detail pane."""
        detail = self.query_one("#detail-pane", DetailPane)
        detail.show_channel(event.channel)

    def action_toggle_filters(self) -> None:
        """Toggle the filter panel visibility."""
        panel = self.query_one("#filter-panel", FilterPanel)
        panel.display = not panel.display

    def action_focus_search(self) -> None:
        """Focus the search input."""
        try:
            from textual.widgets import Input
            search = self.query_one("#search-input", Input)
            search.focus()
        except Exception:
            pass


def main():
    """CLI entry point."""
    data_path = sys.argv[1] if len(sys.argv) > 1 else None

    if data_path and not Path(data_path).exists():
        print(f"Error: file not found: {data_path}")
        sys.exit(1)

    app = KOLDashboard(data_path=data_path)
    app.run()


if __name__ == "__main__":
    main()
