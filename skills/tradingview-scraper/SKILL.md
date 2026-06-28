---
name: "tradingview-scraper"
description: "Unified gold analysis with HTML table formatting for Telegram Rich Messages"
---

# TradingView Scraper + SMC Unified Skill (v2)

Advanced gold analysis combining **7 timeframe data sources**, **Smart Money Concepts**, **TradingView technicals**, **fundamental data**, and **news sentiment**.

## What's New in v2

- ✅ **Multi-timeframe**: D1, H4, H1, M30, M15, M5, M1
- ✅ **Deriv API**: Real-time price from Deriv.com
- ✅ **Unified Report**: All analysis in 1 script
- ✅ **Auto-fallback**: Deriv → yfinance → gold-monitor
- ✅ **HTML Table Formatting**: Clean table display for Telegram Rich Messages

## Components

| Script | Purpose |
|--------|---------|
| `gold_master_analysis.py` | **Main** — Complete unified report |
| `deriv_connector.py` | Deriv API connector |
| `tv_scrape.py` | TradingView technicals |
| `smc_analyzer.py` | SMC patterns |

## Features

1. **Multi-Timeframe Price** (7 TF): Deriv API + yfinance fallback
2. **TradingView Technicals**: 11+ oscillators, 15+ MAs, pivot levels
3. **SMC**: Structure, Liquidity, FVG, S/R, candlestick patterns
4. **HTML Table Formatting**: Clean table display for Telegram Rich Messages

## Setup

```bash
pip3 install playwright yfinance websockets
python3 -m playwright install chromium
```

Optional Deriv token:
```bash
echo "YOUR_DERIV_TOKEN" > ~/.deriv_api_token
```

## Usage

```bash
# Complete analysis
python3 scripts/gold_master_analysis.py

# JSON output
python3 scripts/gold_master_analysis.py --json

# Individual components
python3 scripts/deriv_connector.py --symbol frxXAUUSD
python3 scripts/tv_scrape.py --symbol XAUUSD
python3 scripts/smc_analyzer.py
```

## Output Format

When `richMessages: true` is enabled in Telegram config, the script automatically outputs HTML tables for clean display:

### Example HTML Table Format:
```html
<h3>💰 MULTI-TIMEFRAME PRICE DATA</h3>
| Timeframe | Open | High | Low | Close | Source |
|:---|:---|:---|:---|:---|:---|
| **1d** | $4,014.68 | $4,095.97 | $3,983.17 | **$4,081.45** | Deriv API |
```

### Key Formatting Rules:
- Use `|:---|:---|` for left-aligned columns
- Use `**bold**` for important values
- Keep columns minimal (max 6 columns per table)
- Use emoji headers for visual distinction

## Verdict Logic

| TV | SMC | News | Result |
|----|-----|------|--------|
| SELL | Short | Bearish | 🔴 Strong Sell |
| BUY | Long | Bullish | 🟢 Strong Buy |
| SELL | Mixed | Bearish | 🟠 Sell |
| BUY | Mixed | Bearish | 🟡 Buy |
| NEUTRAL | Any | Mixed | ⚪ Neutral |

## Data Sources

| Source | Data | Delay |
|--------|------|-------|
| Deriv API | Real-time ticks | ~0ms |
| yfinance | COMEX futures | ~15min |
| TradingView | Technicals | Real-time scrape |
| FRED | Macro | Daily |
| CFTC | COT | Weekly |
| SSGA | ETF | Daily |
| News RSS | Headlines | Real-time |

## Notes

- Deriv API: token required for full access
- TV scraping: headless Chromium, ~10-15s
- Weekend: XAUUSD closed, use OTC_Gold
- For analysis, not direct trading

## Credits

- SMC: Kiran Kumbar XAU/USD Signal Bot
- TV scraping: Playwright
- Deriv: Binary.com/Deriv.com API
- Data: FRED, CFTC, SSGA, Google/Bing News
