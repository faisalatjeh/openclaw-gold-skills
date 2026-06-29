---
name: "telegram-formatting-guide"
description: "Telegram formatting guide with entry monitor support"
---

# SKILL: telegram-formatting-guide

## Description
Universal formatting guide for all Telegram messages. Ensures clean HTML table output, proper price data handling, and entry monitor display.

## Formatting Rules

### Tables
- Always use **HTML table format** with `|:---|:---|` alignment
- Use `**bold**` for important values
- Use emoji headers (## 📊)
- Keep tables minimalis and clean

### Entry Monitor Format

```
📊 ENTRY MONITOR — XAUUSD SELL
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🎯 Entry: SELL $4,070.00
📍 Current: $4,053.35
💰 P&L: +$16.65 (Profit)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⚡ ACTION: HOLD PROFIT ✅
📝 Running profit $16.65 — Hold ke TP

🎯 TARGETS:
• TP1: $4,040.00 (±$13)
• TP2: $4,010.00 (±$43)
• TP3: $3,990.00 (±$63)

🛑 STOP LOSS: $4,085.00 (±$31)

💡 Saran: Hold ke target atau trailing stop
⏰ Update: 20:04:48
```

## Price Data Policy

**ON-DEMAND ONLY** - Never auto-fetch in background.

When user requests any trading analysis:
1. Run: `python3 tradingview_cron.py`
2. Read: `cat current_price.json`
3. Use that price for analysis

## Area Setup Format

| Parameter | Setup |
|:---|:---|
| **Entry Zone** | $X,XXX - $X,XXX |
| **Stop Loss** | $X,XXX |
| **Target 1** | $X,XXX |
| **Risk:Reward** | 1:X |

## Version
1.2.0
