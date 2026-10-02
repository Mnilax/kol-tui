import json

import pytest
from textual.widgets import Select, Static

from koltui.app import KOLDashboard
from koltui.data import load_csv, load_json
from koltui.widgets.channel_table import ChannelTable


def test_bom_nonfinite_and_uppercase_flags(tmp_path):
    source = tmp_path / "channels.csv"
    source.write_text("Handle,Subscribers,Reach,CPM ($),Fraud Flags\n@test,inf,nan,NaN,LOW_REACH_RATIO\n", encoding="utf-8-sig")
    channel = load_csv(str(source))[0]
    assert channel.handle == "@test"
    assert channel.subscribers == channel.reach == 0
    assert channel.cpm is None
    assert channel.fraud_flags == ["LOW_REACH_RATIO"]


def test_json_flags_from_mcp_and_invalid_shape(tmp_path):
    source = tmp_path / "channels.json"
    source.write_text(json.dumps([{"handle": "@test", "fraud_flags": [{"code": "LOW", "message": "Low reach"}], "frequency_per_week": 2}]), encoding="utf-8")
    channel = load_json(str(source))[0]
    assert channel.fraud_flags == ["Low reach"]
    assert channel.frequency == 2
    source.write_text("{}", encoding="utf-8")
    with pytest.raises(ValueError, match="list of objects"):
        load_json(str(source))


@pytest.mark.asyncio
async def test_regions_sorting_selection_and_filters(tmp_path):
    source = tmp_path / "channels.json"
    source.write_text(json.dumps([
        {"handle": "@missing", "region": "RU"},
        {"handle": "@high", "region": "US", "cpm": 10},
        {"handle": "[red]low", "region": "RU", "cpm": 2},
    ]), encoding="utf-8")
    app = KOLDashboard(str(source))
    async with app.run_test() as pilot:
        await pilot.pause()
        selector = app.query_one("#region-select", Select)
        selector.value = "RU"
        await pilot.pause()
        table = app.query_one("#channel-table", ChannelTable)
        assert table.row_count == 2
        event = type("HeaderEvent", (), {"column_index": 6})()
        table.on_data_table_header_selected(event)
        assert [ch.handle for ch in table._channels] == ["[red]low", "@missing"]
        table.on_data_table_header_selected(event)
        assert [ch.handle for ch in table._channels] == ["[red]low", "@missing"]
        app.query_one("#detail-pane").show_channel(table._channels[0])
        assert "[red]low" in str(app.query_one("#detail-content", Static).render())
        assert [ch.handle for ch in app._all_channels] == ["@missing", "@high", "[red]low"]
