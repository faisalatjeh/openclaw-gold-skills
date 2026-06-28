---
name: "gold-analysis"
description: "Gold fundamental analysis with real-time price from TradingView only"
metadata:
  version: 1.0.0
  author: FMouse
  tags: gold, trading, analysis, finance
---

# SKILL: gold-analysis

## Description
Fetches and analyzes gold fundamental data from FRED, CFTC, SPDR ETF, and Fed RSS. Returns structured JSON with macro indicators, COT positioning, ETF holdings, Fed stance, and upcoming events.

## Price Data Policy

**Real-time price is fetched ON-DEMAND only** - never auto-fetch in background.

When user requests:
- **Analysis** (analisis, analysis, technical)
- **Trading signals** (signal, sinyal, buy, sell)
- **Price check** (harga, price, berapa)
- **Area setup** (setup, area, entry, zone)
- **Any trading-related request**

**ALWAYS fetch real-time price first** using:
- `tradingview_cron.py` (Playwright browser fetch from TradingView)

Then read the price:
```bash
cat ~/.openclaw/workspace/current_price.json
```

**Never** use cached/stale price for trading analysis.

## Output Formatting

**For Telegram (primary channel):**
- Always use **HTML table format** with `|:---|:---|` alignment
- Use `**bold**` for important values, prices, signals
- Use emoji headers (## 📊) for sections
- **NEVER use ASCII art** tables (+, -, dashed lines)
- Keep tables minimalis and clean
- All structured data MUST be in tables

## Procedure

### Step 1: Fetch Real-time Price
```bash
cd ~/.openclaw/workspace && python3 tradingview_cron.py
```

### Step 2: Read Price Data
```bash
cat ~/.openclaw/workspace/current_price.json
```

### Step 3: Execute Analysis
```bash
cd ~/.openclaw/workspace && python3 skills/tradingview-scraper/scripts/gold_master_analysis.py
```

### Step 4: Generate Area Setup
Based on real-time price + technical levels:
- Entry zones
- Stop loss
- Take profit targets
- Risk:Reward ratio

## Files
- `~/.openclaw/workspace/tradingview_cron.py` - Real-time price fetcher (TradingView only)
- `~/.openclaw/workspace/skills/tradingview-scraper/scripts/gold_master_analysis.py` - Full analysis

## Version
1.2.1
