---
name: "telegram-formatting-guide"
description: "Telegram formatting guide with TradingView-only price policy"
---

# SKILL: telegram-formatting-guide

## Description
Universal formatting guide for all Telegram messages. Ensures clean HTML table output and proper price data handling.

## Formatting Rules

### Tables
- Always use **HTML table format** with `|:---|:---|` alignment
- Use `**bold**` for important values, prices, signals
- Use emoji headers (## 📊) for sections
- **NEVER use ASCII art** tables (+, -, dashed lines)
- Keep tables minimalis and clean
- All structured data MUST be in tables

### Example Good Format:
```
| Timeframe | Open | Close |
|:---|:---|:---|
| **1d** | $4,014 | **$4,081** |
```

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

## Area Setup Format

| Parameter | Setup |
|:---|:---|
| **Entry Zone** | $X,XXX - $X,XXX |
| **Stop Loss** | $X,XXX |
| **Target 1** | $X,XXX |
| **Target 2** | $X,XXX |
| **Risk:Reward** | 1:X |

## Version
1.1.1
