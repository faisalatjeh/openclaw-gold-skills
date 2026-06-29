# TRADINGVIEW-SCRAPER — Applied

## Overview

Fetches real-time XAUUSD price from TradingView using Playwright browser automation. Includes area setup generation and ENTRY MONITORING with auto-action alerts.

## Price Policy

**ON-DEMAND ONLY** - Never auto-fetch in background.

When user requests any trading analysis:
1. Run: `python3 tradingview_cron.py`
2. Read: `cat current_price.json`
3. Use that price for analysis

## Entry Monitor Feature

### Auto-Actions Rules:
| Kondisi | Action |
|:---|:---|
| Price ≥ TP1 | CLOSE 50% |
| Price ≥ TP2 | CLOSE 100% atau MOVE SL |
| Price ≥ TP3 | CLOSE 100% |
| Price dekat SL | WARNING |
| Price di entry ±$2 | BREAKEVEN |
| Default | HOLD |

### Scripts:
- `tradingview_cron.py` — Fetch real-time price
- `tradingview_realtime.py` — Manual version
- `entry_monitor.py` — Monitor + auto-actions
- `scripts/gold_master_analysis.py` — Full analysis

## Version: 2.2.0
## Applied: 2026-06-28
## Status: ACTIVE