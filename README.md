# 🥇 OpenClaw Gold Skills

Real-time XAUUSD (Gold) analysis system for OpenClaw with clean HTML-table formatting for Telegram.

## ✨ Features

- **Real-time price** from TradingView (on-demand fetch)
- **Multi-timeframe analysis** (1m, 5m, 15m, 30m, 1h, 4h, 1d)
- **Fundamental analysis** (Fed, CPI, DXY, COT, ETF)
- **News sentiment** analysis
- **Smart Money Concepts** (SMC)
- **Area setup** generation (entry/stop/target)
- **HTML table formatting** for Telegram

## 🚀 Quick Start

### 1. Price Fetch (On-Demand)
```bash
# Fetch real-time price from TradingView
python3 tradingview_cron.py

# Read the price
cat current_price.json
```

### 2. Full Analysis
```bash
# Generate comprehensive analysis
cd ~/.openclaw/workspace && python3 skills/tradingview-scraper/scripts/gold_master_analysis.py
```

### 3. Area Setup
Automatically generated when you request "Area setup" - includes:
- Entry zones
- Stop loss
- Take profit targets
- Risk:Reward ratios

## 📁 Skills

| Skill | Version | Description |
|:---|:---|:---|
| [gold-analysis](skills/gold-analysis/) | v1.2.1 | Fundamental analysis |
| [tradingview-scraper](skills/tradingview-scraper/) | v2.1.1 | Real-time price + technicals |
| [telegram-formatting-guide](skills/telegram-formatting-guide/) | v1.1.1 | HTML table formatting |

## 📋 Price Policy

**ON-DEMAND ONLY** - Never auto-fetch in background.

When you request any trading analysis:
1. System fetches real-time price from TradingView
2. Uses that price for analysis
3. Never uses cached/stale data

## 🛠️ Installation

See [docs/INSTALL.md](docs/INSTALL.md)

## 📖 Usage

See [docs/USAGE.md](docs/USAGE.md)

## 📄 License

MIT License - See [LICENSE](LICENSE)

## 🔗 Repository

https://github.com/faisalatjeh/openclaw-gold-skills
