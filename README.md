# KOL Analytics TUI Dashboard

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.11+](https://img.shields.io/badge/python-3.11%2B-blue.svg)](https://www.python.org/downloads/)

Terminal dashboard for KOL/influencer analytics built with [Textual](https://textual.textualize.io/). Reads CSV/JSON exports from [kol-toolkit](https://github.com/Mnilax/kol-toolkit) and provides interactive data exploration.

Try the included [sample CSV](examples/sample.csv) to explore the dashboard.

## Features

- **Sortable DataTable** — click any column header to sort (ascending/descending toggle)
- **Live filter panel** — filter by region, max CPM, min ER% with instant updates
- **Search** — case-insensitive substring search by channel handle
- **Detail pane** — select a row to see expanded metrics and fraud flag explanations
- **Color-coded flags** — red for high-severity fraud, yellow for medium, green for clean
- **Keyboard shortcuts** — `q` quit, `f` toggle filters, `/` focus search

## Install

```bash
pip install -e .
```

## Usage

```bash
# From kol-toolkit CSV export
kol-tui report.csv

# From JSON export
kol-tui enriched.json

# With sample data
kol-tui examples/sample.csv
```

## Keyboard Shortcuts

| Key | Action |
|-----|--------|
| `q` | Quit |
| `f` | Toggle filter panel |
| `/` | Focus search input |
| `↑`/`↓` | Navigate rows |
| `Enter` | Select row for detail view |

## Data Format

The TUI reads CSV or JSON files with these columns:

```
handle, platform, region, subscribers, reach, avg_views,
er_pct, cpm, frequency, price, fraud_flags
```

Generate compatible data with `kol report enriched.json --csv report.csv` from [kol-toolkit](https://github.com/Mnilax/kol-toolkit).

## Architecture

```
src/koltui/
├── app.py                # Textual App: layout, bindings, event handling
├── data.py               # CSV/JSON loader
├── theme.py              # Color schemes for flags, CPM, ER
└── widgets/
    ├── channel_table.py  # Sortable DataTable
    ├── filters.py        # Side panel with region/CPM/ER inputs
    └── detail_pane.py    # Expanded channel detail view
```

## License

MIT
