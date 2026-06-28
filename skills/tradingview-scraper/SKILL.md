---
name: "tradingview-scraper"
description: "TradingView scraper with real-time price fetch"
---

# SKILL: tradingview-scraper

## Description
Fetches real-time gold price from TradingView using Playwright browser automation and generates comprehensive technical analysis.

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

## Scripts

### tradingview_cron.py
- Fetches real-time XAUUSD from TradingView Pepperstone
- Uses Playwright headless browser
- Saves to current_price.json

### gold_master_analysis.py
- Multi-timeframe analysis (1m, 5m, 15m, 30m, 1h, 4h, 1d)
- Fundamental data (Fed, CPI, DXY, COT)
- News sentiment analysis
- Smart Money Concepts (SMC)
- TradingView technicals

## Output Format
- HTML tables with `|:---|:---|` alignment
- Bold for key values and signals
- Emoji headers for sections
- Never ASCII art tables

## Area Setup Generation
When user asks "Area setup", automatically:
1. Fetch real-time price
2. Get technical levels (support/resistance)
3. Generate:
   - Entry zones
   - Stop loss
   - Take profit targets
   - Risk:Reward ratios

## Files
- `~/.openclaw/workspace/tradingview_cron.py`
- `~/.openclaw/workspace/tradingview_realtime.py`
- `~/.openclaw/workspace/skills/tradingview-scraper/scripts/gold_master_analysis.py`

## Version
2.1.1
