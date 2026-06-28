# 🥇 OpenClaw Gold Skills

[![Version](https://img.shields.io/badge/version-2.0.0-blue.svg)](https://github.com/yourusername/openclaw-gold-skills)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/platform-OpenClaw-orange.svg)](https://openclaw.ai)

> **Professional gold analysis skills for OpenClaw with clean HTML table formatting**

## ✨ Features

| Feature | Detail |
|:---|:---|
| **Multi-Timeframe** | D1, H4, H1, M30, M15, M5, M1 |
| **Real-time Data** | Deriv API + yfinance fallback |
| **HTML Tables** | Clean `\|:---|:---\|` format |
| **Smart Money** | SMC patterns & structure |
| **Auto-Analysis** | Cron jobs ready |
| **Telegram Ready** | Rich messages enabled |

## 📸 Screenshot

**Before (ASCII Art):**
```
+-----------+--------+
| Timeframe | Price  |
+-----------+--------+
| 1d        | $4,081 |
+-----------+--------+
```

**After (HTML Table):**
```markdown
| Timeframe | Price |
|:---|:---|
| **1d** | **$4,081** |
```

## 📦 Skills Included

| Skill | Version | Purpose |
|:---|:---|:---|
| [tradingview-scraper](skills/tradingview-scraper/) | v2 | Multi-timeframe technical analysis |
| [gold-analysis](skills/gold-analysis/) | v1.1 | Comprehensive gold fundamental analysis |
| [telegram-formatting-guide](skills/telegram-formatting-guide/) | v1.0 | Universal HTML table formatting |

## 🚀 Installation

### Quick Install
```bash
# Clone repository
git clone https://github.com/yourusername/openclaw-gold-skills.git

# Copy to OpenClaw workspace
cp -r openclaw-gold-skills/skills/* ~/.openclaw/workspace/skills/

# Enable skills
openclaw skills enable tradingview-scraper
openclaw skills enable gold-analysis
openclaw skills enable telegram-formatting-guide
```

### Enable Rich Messages (Telegram)
Add to `~/.openclaw/openclaw.json`:
```json
{
  "channels": {
    "telegram": {
      "enabled": true,
      "richMessages": true
    }
  }
}
```

## 📊 Usage

### Manual Analysis
```bash
# Complete analysis
python3 ~/.openclaw/workspace/skills/tradingview-scraper/scripts/gold_master_analysis.py

# JSON output
python3 ~/.openclaw/workspace/skills/tradingview-scraper/scripts/gold_master_analysis.py --json
```

### In Chat
```
User: Analisa xauusd
Agent: 🥇 GOLD MASTER ANALYSIS — XAUUSD
       [HTML tables with multi-timeframe data]
```

## 📅 Auto-Analysis Schedule

| Job | Schedule | Description |
|:---|:---|:---|
| Daily Analysis | 08:00 ET | Complete morning report |
| Evening Update | 17:00 ET | Daily recap & setup |
| Pre-Events | 07:00 ET | Economic calendar |
| Weekly Outlook | Fri 18:00 ET | Week ahead preview |

Setup: See [examples/cron-setup.md](examples/cron-setup.md)

## 🛠️ Requirements

```bash
pip3 install playwright yfinance websockets
python3 -m playwright install chromium
```

Optional Deriv token:
```bash
echo "YOUR_DERIV_TOKEN" > ~/.deriv_api_token
```

## 📋 Data Sources

| Source | Data | Delay |
|:---|:---|:---|
| Deriv API | Real-time ticks | ~0ms |
| yfinance | COMEX futures | ~15min |
| TradingView | Technicals | Real-time |
| FRED | Macro | Daily |
| CFTC | COT | Weekly |
| SSGA | ETF | Daily |
| News RSS | Headlines | Real-time |

## 🤝 Contributing

1. Fork repository
2. Create feature branch (`git checkout -b feature/amazing`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing`)
5. Open Pull Request

## 📄 License

MIT License - see [LICENSE](LICENSE) for details

## 🙏 Credits

- SMC: Kiran Kumbar XAU/USD Signal Bot
- TV scraping: Playwright
- Deriv: Binary.com/Deriv.com API
- Data: FRED, CFTC, SSGA, Google/Bing News

---

**Made with ❤️ for OpenClaw users**
