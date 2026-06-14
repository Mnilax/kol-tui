"""Filter panel widget for the KOL TUI."""

from __future__ import annotations

from textual.app import ComposeResult
from textual.containers import Vertical
from textual.message import Message
from textual.widgets import Input, Label, Select, Static


class FilterPanel(Vertical):
    """Side panel with filter inputs."""

    DEFAULT_CSS = """
    FilterPanel {
        width: 30;
        background: $surface;
        padding: 1 2;
    }
    FilterPanel Label {
        margin-top: 1;
        color: $text-muted;
    }
    FilterPanel Input {
        margin-bottom: 1;
    }
    """

    class FiltersChanged(Message):
        """Emitted when any filter value changes."""

        def __init__(
            self,
            region: str = "",
            max_cpm: float | None = None,
            min_er: float | None = None,
            search: str = "",
        ) -> None:
            super().__init__()
            self.region = region
            self.max_cpm = max_cpm
            self.min_er = min_er
            self.search = search

    def __init__(self, regions: list[str] | None = None, **kwargs):
        super().__init__(**kwargs)
        self._regions = regions or []

    def compose(self) -> ComposeResult:
        yield Static("[b]Filters[/b]", classes="title")
        yield Label("Search")
        yield Input(placeholder="Handle...", id="search-input")
        yield Label("Region")
        region_options = [("All", "")] + [(r, r) for r in self._regions if r]
        yield Select(region_options, id="region-select", value="")
        yield Label("Max CPM ($)")
        yield Input(placeholder="e.g. 20", id="max-cpm-input")
        yield Label("Min ER (%)")
        yield Input(placeholder="e.g. 3", id="min-er-input")

    def _emit_filters(self) -> None:
        search = self.query_one("#search-input", Input).value
        region_select = self.query_one("#region-select", Select)
        region = str(region_select.value) if region_select.value != Select.BLANK else ""

        max_cpm_str = self.query_one("#max-cpm-input", Input).value
        min_er_str = self.query_one("#min-er-input", Input).value

        try:
            max_cpm = float(max_cpm_str) if max_cpm_str else None
        except ValueError:
            max_cpm = None

        try:
            min_er = float(min_er_str) if min_er_str else None
        except ValueError:
            min_er = None

        self.post_message(self.FiltersChanged(
            region=region,
            max_cpm=max_cpm,
            min_er=min_er,
            search=search,
        ))

    def on_input_changed(self, event: Input.Changed) -> None:
        self._emit_filters()

    def on_select_changed(self, event: Select.Changed) -> None:
        self._emit_filters()
