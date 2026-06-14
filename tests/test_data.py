"""Smoke tests for KOL TUI data loading."""

from pathlib import Path

from koltui.data import Channel, load_csv, load_file


SAMPLE_CSV = Path(__file__).resolve().parent.parent / "examples" / "sample.csv"


class TestLoadCSV:
    def test_loads_sample_csv(self):
        """Smoke test: sample.csv loads without errors."""
        channels = load_csv(str(SAMPLE_CSV))
        assert len(channels) > 0

    def test_channel_fields(self):
        """Each loaded channel has required fields populated."""
        channels = load_csv(str(SAMPLE_CSV))
        for ch in channels:
            assert isinstance(ch, Channel)
            assert ch.handle  # non-empty handle

    def test_load_file_autodetect(self):
        """load_file auto-detects CSV format."""
        channels = load_file(str(SAMPLE_CSV))
        assert len(channels) > 0


class TestChannelDataclass:
    def test_defaults(self):
        ch = Channel(handle="@test")
        assert ch.platform == "tg"
        assert ch.subscribers == 0
        assert ch.fraud_flags == []

    def test_fraud_flags_list(self):
        ch = Channel(handle="@flagged", fraud_flags=["LOW_REACH_RATIO"])
        assert len(ch.fraud_flags) == 1
