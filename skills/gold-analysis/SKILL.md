---
name: "gold-analysis"
description: "Gold fundamental analysis with entry monitor and real-time price"
metadata:
  version: 1.0.0
  author: FMouse
  tags: gold, trading, analysis, finance
---

# SKILL: gold-analysis

## Description
Fetches and analyzes gold fundamental data from FRED, CFTC, SPDR ETF, and Fed RSS. Returns structured JSON with macro indicators, COT positioning, ETF holdings, Fed stance, upcoming events, and ENTRY MONITORING.

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
When user provides entry details, create monitor file:

```bash
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
  "created_at": "2026-06-28T20:00:00",
  "status": "ACTIVE"
}
EOF
```

### Auto-Actions Rules:

| Kondisi | Action | Deskripsi |
|:---|:---|:---|
| Price ≥ TP1 | CLOSE 50% | Close separuh posisi |
| Price ≥ TP2 | CLOSE 100% atau MOVE SL | Full close atau trail |
| Price ≥ TP3 | CLOSE 100% | Target tercapai |
| Price mendekati SL (90%) | WARNING | Alert cut loss |
| Price di entry ±$2 | BREAKEVEN | Pindah SL ke entry |
| Price dalam range 50% | HOLD | Tunggu development |

### Monitor Output Format:

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

### Step 5: Monitor Entry (if active)
```bash
cd ~/.openclaw/workspace && python3 entry_monitor.py
```

## Files
- `~/.openclaw/workspace/tradingview_cron.py` - Real-time price fetcher
- `~/.openclaw/workspace/entry_monitor.py` - Entry monitor + auto-actions
- `~/.openclaw/workspace/active_entry.json` - Active entry config
- `~/.openclaw/workspace/entry_status.json` - Monitor status output
- `~/.openclaw/workspace/skills/tradingview-scraper/scripts/gold_master_analysis.py` - Full analysis

## Cron Jobs

### entry-monitor
- Schedule: Setiap 1 menit
- Action: Fetch price + Run monitor
- Output: Entry status + Action alerts

## Version
1.3.0
