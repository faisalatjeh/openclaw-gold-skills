---
name: "tradingview-scraper"
description: "TradingView scraper with entry monitor, auto-action alerts, and position management"
---

# SKILL: tradingview-scraper

## Description
Fetches real-time gold price from TradingView using Playwright browser automation. Generates comprehensive technical analysis, area setup, and ENTRY MONITORING with auto-action alerts.

## Price Data Policy

**Real-time price is fetched ON-DEMAND only** - never auto-fetch in background.

When user requests:
- **Analysis** (analisis, analysis, technical)
- **Trading signals** (signal, sinyal, buy, sell)
- **Price check** (harga, price, berapa)
- **Area setup** (setup, area, entry, zone)
- **Entry monitor** (monitor, pantau, entry, posisi)
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

## Entry Monitor Feature

### Setup Entry Monitoring
When user provides entry details, create monitor:

```bash
# Save entry to file
cat > ~/.openclaw/workspace/active_entry.json << 'EOF'
{
  "symbol": "XAUUSD",
  "direction": "SELL",
  "entry_price": 4070.00,
  "stop_loss": 4085.00,
  "take_profit_1": 4040.00,
  "take_profit_2": 4010.00,
  "take_profit_3": 3990.00,
  "position_size": "1 lot",
  "created_at": "2026-06-28T19:30:00",
  "status": "ACTIVE"
}
EOF
```

### Monitor Script
File: `~/.openclaw/workspace/entry_monitor.py`

Features:
- Check price every 1 minute
- Compare with entry/stop/target
- Generate action alerts:
  - **HOLD** - Price dalam range aman
  - **CLOSE** - TP tercapai
  - **MOVE SL** - Price mendekati TP, pindah SL ke breakeven
  - **PARTIAL CLOSE** - 50% close, 50% hold ke TP berikutnya
  - **CUT LOSS** - Price mendekati SL (warning)
- Send alert message

### Auto-Actions Rules:

| Kondisi | Action | Deskripsi |
|:---|:---|:---|
| Price ≥ TP1 | CLOSE 50% | Close separuh posisi |
| Price ≥ TP2 | CLOSE 100% atau MOVE SL | Full close atau trail |
| Price ≥ TP3 | CLOSE 100% | Target tercapai |
| Price mendekati SL (90%) | WARNING | Alert cut loss |
| Price di entry ±$2 | BREAKEVEN | Pindah SL ke entry |
| Price dalam range 50% | HOLD | Tunggu development |

### Output Format (Entry Monitor):

```
📊 ENTRY MONITOR — XAUUSD
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🎯 Entry: SELL $4,070.00
📍 Current: $4,053.35
💰 P&L: +$16.65 (Running Profit)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⚡ STATUS: PROFIT ✅
📊 Progress: 55% menuju TP1

🎯 TARGETS:
• TP1: $4,040 (±$13 dari sekarang)
• TP2: $4,010 (±$43 dari sekarang)  
• TP3: $3,990 (±$63 dari sekarang)

🛑 STOP LOSS: $4,085 (±$31)

💡 ACTION: HOLD — Price masih dalam trend bearish
🔄 Next Check: 1 menit

📈 Saran: Pertimbangkan partial close 50% di TP1
```

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
- Auto-generate action alerts
- Send notifications

### gold_master_analysis.py
- Multi-timeframe analysis
- Fundamental data
- News sentiment
- SMC patterns

## Files
- `~/.openclaw/workspace/tradingview_cron.py`
- `~/.openclaw/workspace/tradingview_realtime.py`
- `~/.openclaw/workspace/entry_monitor.py` — NEW
- `~/.openclaw/workspace/active_entry.json` — NEW
- `~/.openclaw/workspace/skills/tradingview-scraper/scripts/gold_master_analysis.py`

## Version
2.2.0
