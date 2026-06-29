# SKILL: gold-analysis

## Description
Fetches and analyzes gold fundamental data from FRED, CFTC, SPDR ETF, and Fed RSS. Returns structured JSON with macro indicators, COT positioning, ETF holdings, Fed stance, upcoming events, and INTEGRATED ENTRY MONITORING with market analysis.

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

## Smart Monitor (Anti-Spam)

### Rules:
- **Alert hanya jika** ada perubahan signifikan
- **Silent** jika price stagnan

| Kondisi | Alert? | Alasan |
|:---|:---|:---|
| Price berubah ≥ $2 | ✅ YES | Significant movement |
| Action berubah (TP/SL) | ✅ YES | Trigger reached |
| 30 menit tanpa alert | ✅ YES | Summary |
| Price stagnan | ❌ NO | Skip (anti-spam) |

### Output:
```
📊 ENTRY MONITOR — XAUUSD SELL
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🎯 Entry: SELL $4,064.00
📍 Current: $4,060.80
💰 P&L: +$3.20 (Profit)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⚡ ACTION: HOLD PROFIT ✅
📝 Running profit $3.20 — Hold ke TP

🎯 TARGETS:
• TP1: $4,045.00
• TP2: $4,020.00
• TP3: $4,000.00

🛑 STOP LOSS: $4,080.00

📊 MARKET ANALYSIS:
• Trend: Bearish
• DXY: 120.4
• SMC Structure: Bullish on H1
• Reversal Risk: LOW ✅

💡 SARAN: Hold ke target
⏰ Update: 20:04:48
```

## Files
- `~/.openclaw/workspace/tradingview_cron.py` - Real-time price fetcher
- `~/.openclaw/workspace/entry_monitor_smart.py` - Smart entry monitor (anti-spam)
- `~/.openclaw/workspace/active_entry.json` - Active entry config (created per request)
- `~/.openclaw/workspace/entry_status.json` - Monitor status output
- `~/.openclaw/workspace/skills/tradingview-scraper/scripts/gold_master_analysis.py` - Full analysis

## Version
1.5.0