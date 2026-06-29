---
name: "gold-analysis-v2"
description: "Gold analysis with original entry monitor style (alert every 2 minutes)"
---

# SKILL: gold-analysis-v2

## Description
Fetches and analyzes gold fundamental data from FRED, CFTC, SPDR ETF, and Fed RSS. Returns structured JSON with macro indicators, COT positioning, ETF holdings, Fed stance, upcoming events, and ENTRY MONITORING with ORIGINAL style (alert every 2 minutes).

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

## Monitor Style: ORIGINAL (Alert Every 2 Minutes)

### User Preference:
User prefers **original monitor style** that sends full report every 2 minutes regardless of price change.

### Output Format:
```
📊 ENTRY MONITOR — XAUUSD SELL
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🎯 Entry: SELL $4,064.00
📍 Current: $4,060.80
💰 P&L: +$3.20 (Profit)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⚡ ACTION: HOLD PROFIT ✅
📝 Running profit $3.20 — Hold ke TP

🎯 TARGETS:
• TP1: $4,045.00 (±$16 dari sekarang)
• TP2: $4,020.00 (±$41 dari sekarang)
• TP3: $4,000.00 (±$61 dari sekarang)

🛑 STOP LOSS: $4,080.00 (±$19)

📊 MARKET ANALYSIS:
• Trend: Bearish
• DXY: 120.4
• SMC Structure: Bullish on H1 ⚠️
• Reversal Risk: LOW ✅

💡 SARAN: 💰 Bagus! Hold ke target atau pasang trailing stop. SMC: Bullish on H1
🔄 Next Check: 2 menit
```

## Files
- `~/.openclaw/workspace/tradingview_cron.py` - Real-time price fetcher
- `~/.openclaw/workspace/entry_monitor_v2.py` - Entry monitor (original style)
- `~/.openclaw/workspace/active_entry.json` - Active entry config (created per request)
- `~/.openclaw/workspace/entry_status.json` - Monitor status output
- `~/.openclaw/workspace/skills/tradingview-scraper/scripts/gold_master_analysis.py` - Full analysis

## Version
1.5.1
