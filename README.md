# 🥇 OpenClaw Gold Skills

Complete XAUUSD (Gold) analysis system for OpenClaw with real-time price, technical analysis, and entry monitoring.

## ✨ Features

- **Real-time price** from TradingView (on-demand)
- **Multi-timeframe analysis** (1m, 5m, 15m, 30m, 1h, 4h, 1d)
- **Fundamental analysis** (Fed, CPI, DXY, COT, ETF)
- **News sentiment** analysis
- **Smart Money Concepts** (SMC)
- **Entry monitoring** with auto-action alerts
- **HTML table formatting** for Telegram

## 📁 Files

| File | Description |
|:---|:---|
| `tradingview_cron.py` | Real-time price fetcher |
| `tradingview_realtime.py` | Manual price fetcher |
| `entry_monitor_v2.py` | Entry monitor (original style) |
| `entry_monitor_smart.py` | Smart monitor (anti-spam) |
| `SOUL.md` | Agent personality & policies |
| `current_price.json` | Latest price data |

## 📁 Skills

| Skill | Version | Description |
|:---|:---|:---|
| [gold-analysis](skills/gold-analysis/) | v1.5.1 | Fundamental + entry monitor |
| [tradingview-scraper](skills/tradingview-scraper/) | v2.2.1 | Real-time price + technicals |
| [telegram-formatting-guide](skills/telegram-formatting-guide/) | v1.2.0 | HTML table formatting |

## 📋 Cron Jobs

| Job | Schedule | Description |
|:---|:---|:---|
| entry-monitor-4064 | Every 2 minutes | Active entry monitor |
| xauusd-daily-analysis | 06:00 AM | Daily market analysis |
| xauusd-evening-update | 03:00 PM | Evening update |
| xauusd-pre-events | 12:00 AM | Pre-market events |
| xauusd-weekly-outlook | Sunday 18:00 | Weekly outlook |

## 🚀 Quick Start

### Fetch Real-time Price
```bash
python3 tradingview_cron.py
```

### Run Analysis
```bash
python3 skills/tradingview-scraper/scripts/gold_master_analysis.py
```

### Monitor Entry
```bash
# Create entry config
echo '{"symbol":"XAUUSD","direction":"SELL","entry_price":4064,"stop_loss":4080,"take_profit_1":4045}' > active_entry.json

# Run monitor
python3 entry_monitor_v2.py
```

## 📖 Documentation

- [Installation](docs/INSTALL.md)
- [Usage](docs/USAGE.md)
- [Examples](examples/)

## 📄 License

MIT License - See [LICENSE](LICENSE)

## 🔗 Repository

https://github.com/faisalatjeh/openclaw-gold-skills