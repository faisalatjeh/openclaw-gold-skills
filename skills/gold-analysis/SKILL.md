---
name: "gold-analysis"
description: "Gold analysis with on-demand entry monitoring"
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
5. If user says NO → Manual check only (user asks "Status entry?")

### How to Deactivate:
- User says: "Close entry", "Stop monitor", "Tidak ada entry lagi"
- System removes cron job and deletes `active_entry.json`

### Auto-Actions (Only when monitor ACTIVE):
| Kondisi | Action |
|:---|:---|
| Price ≥ TP1 | CLOSE 50% alert |
| Price ≥ TP2 | CLOSE 100% atau MOVE SL |
| Price ≥ TP3 | CLOSE 100% |
| Price dekat SL | WARNING |
| Price di entry ±$2 | BREAKEVEN alert |
| Default | HOLD |

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

### Step 5: Monitor Entry (ONLY if user has active entry)
```bash
cd ~/.openclaw/workspace && python3 entry_monitor.py
```

## Files
- `~/.openclaw/workspace/tradingview_cron.py` - Real-time price fetcher
- `~/.openclaw/workspace/entry_monitor.py` - Entry monitor (manual/on-demand)
- `~/.openclaw/workspace/active_entry.json` - Active entry config (created per request)
- `~/.openclaw/workspace/entry_status.json` - Monitor status output
- `~/.openclaw/workspace/skills/tradingview-scraper/scripts/gold_master_analysis.py` - Full analysis

## Version
1.3.1
