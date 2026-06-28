# Usage Examples

## Basic Commands

### Manual Analysis
```bash
# Complete analysis with HTML tables
python3 ~/.openclaw/workspace/skills/tradingview-scraper/scripts/gold_master_analysis.py

# JSON output for automation
python3 ~/.openclaw/workspace/skills/tradingview-scraper/scripts/gold_master_analysis.py --json
```

### Individual Components
```bash
# Deriv API data
python3 ~/.openclaw/workspace/skills/tradingview-scraper/scripts/deriv_connector.py --symbol frxXAUUSD

# TradingView technicals
python3 ~/.openclaw/workspace/skills/tradingview-scraper/scripts/tv_scrape.py --symbol XAUUSD

# SMC analysis
python3 ~/.openclaw/workspace/skills/tradingview-scraper/scripts/smc_analyzer.py
```

## Chat Commands

### Telegram/OpenClaw
```
User: Analisa xauusd
Agent: [HTML table report]

User: xauusd setup
Agent: [Support/resistance zones table]

User: news xauusd
Agent: [News sentiment table]
```

## Cron Jobs

### Daily Analysis (08:00 ET)
```cron
0 8 * * * cd ~/.openclaw/workspace/skills/tradingview-scraper/scripts && python3 gold_master_analysis.py
```

### Evening Update (17:00 ET)
```cron
0 17 * * 1-5 cd ~/.openclaw/workspace/skills/tradingview-scraper/scripts && python3 gold_master_analysis.py
```

## Output Format

### HTML Table Example
```markdown
## 💰 MULTI-TIMEFRAME PRICE DATA

| Timeframe | Open | High | Low | Close | Source |
|:---|:---|:---|:---|:---|:---|
| **1d** | $4,014.68 | $4,095.97 | $3,983.17 | **$4,081.45** | Deriv API |
| **4h** | $4,071.82 | $4,082.19 | $4,064.79 | **$4,081.45** | Deriv API |
```

### Sections Included
1. 💰 Multi-Timeframe Price Data
2. 🏛️ Fundamental Analysis
3. 📰 News Sentiment
4. 🧠 Smart Money Concepts
5. 📈 TradingView Technicals
6. 🎯 Final Verdict
7. 📅 Upcoming Events
8. 💡 Trading Plan

## Customization

### Add Custom Indicators
Edit `~/.openclaw/workspace/skills/tradingview-scraper/scripts/gold_master_analysis.py`:
```python
# Add your custom indicator
result["custom"] = get_custom_indicator()
```

### Change Schedule
Edit cron jobs:
```bash
crontab -e
```

## Tips

1. **Weekend**: XAUUSD closed, analysis uses last known data
2. **Events**: Always check upcoming events before trading
3. **Multiple Sources**: Cross-verify data for accuracy
4. **Risk Management**: Always use stop loss!

## API Reference

See individual SKILL.md files for detailed API documentation.
