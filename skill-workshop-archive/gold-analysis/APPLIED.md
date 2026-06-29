# GOLD-ANALYSIS — Applied

## Overview

Gold fundamental analysis with real-time price from TradingView and ENTRY MONITORING.

## Price Policy

**ON-DEMAND ONLY** - Never auto-fetch in background.

When user requests:
- Analysis (analisis, technical)
- Trading signals (signal, buy, sell)
- Price check (harga, price)
- Area setup (setup, entry, zone)
- Entry monitor (monitor, pantau, posisi)
- Any trading-related request

**ALWAYS fetch real-time price first** using TradingView only.

## Entry Monitor Feature

### Auto-Actions:
- **CLOSE 50%** — When TP1 reached
- **CLOSE 100%** — When TP2/TP3 reached
- **MOVE SL** — Trail stop to breakeven or TP1
- **WARNING** — When price near SL
- **HOLD** — Price within normal range

### Setup:
1. Create `active_entry.json` with entry details
2. Cron runs every 1 minute
3. Auto-generate action alerts

## Files
- `tradingview_cron.py` — Real-time price fetcher
- `entry_monitor.py` — Entry monitor + auto-actions
- `active_entry.json` — Active entry config
- `entry_status.json` — Monitor output

## Version: 1.3.0
## Applied: 2026-06-28
## Status: ACTIVE