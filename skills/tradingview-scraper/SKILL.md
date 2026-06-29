---
name: "tradingview-scraper"
description: "TradingView scraper with on-demand entry monitor"
---

# SKILL: tradingview-scraper

## Description
Fetches real-time gold price from TradingView using Playwright browser automation. Generates comprehensive technical analysis, area setup, and ON-DEMAND entry monitoring.

## Price Data Policy

**Real-time price is fetched ON-DEMAND only** - never auto-fetch in background.

When user requests:
- **Analysis** (analisis, analysis, technical)
- **Trading signals** (signal, sinyal, buy, sell)
- **Price check** (harga, price, berapa)
- **Area setup** (setup, area, entry, zone)
- **Any trading-related request**

**ALWAYS fetch real-time price first** using:
```bash
cd ~/.openclaw/workspace && python3 tradingview_cron.py
```

Then read the price:
```bash
cat ~/.openclaw/workspace/current_price.json
```

**Never** use cached/stale price for trading analysis.

## Entry Monitor Policy

**Entry monitor is ON-DEMAND only** - never auto-run in background.

### When to Activate Monitor:
- User explicitly says: "Saya ada entry", "Entry saya", "Monitor entry", "Saya dalam posisi"
- User provides entry details: "Entry SELL $4,070"

### When NOT to Activate:
- User does NOT mention having an entry
- Default state: NO MONITORING

### How to Activate:
1. User says: "Saya ada entry SELL $4,070 SL $4,085"
2. System creates `active_entry.json`
3. System asks: "Mau di-monitor otomatis setiap 1 menit?"
4. If user says YES → Create cron job
5. If user says NO → Manual check only

### How to Deactivate:
- User says: "Close entry", "Stop monitor", "Tidak ada entry lagi"
- System removes cron job and deletes `active_entry.json`

## Area Setup Generation
When user asks "Area setup", automatically:
1. Fetch real-time price
2. Get technical levels (support/resistance)
3. Generate:
   - Entry zones
   - Stop loss
   - Take profit targets
   - Risk:Reward ratios

## Scripts

### tradingview_cron.py
- Fetches real-time XAUUSD from TradingView
- Saves to current_price.json

### entry_monitor.py
- Monitor active entry positions
- Generate action alerts (ONLY when activated)
- Manual or cron-based (user choice)

### gold_master_analysis.py
- Multi-timeframe analysis
- Fundamental data
- News sentiment
- SMC patterns

## Files
- `~/.openclaw/workspace/tradingview_cron.py`
- `~/.openclaw/workspace/tradingview_realtime.py`
- `~/.openclaw/workspace/entry_monitor.py` - Manual/on-demand
- `~/.openclaw/workspace/active_entry.json` - Created per request
- `~/.openclaw/workspace/skills/tradingview-scraper/scripts/gold_master_analysis.py`

## Version
2.2.1
