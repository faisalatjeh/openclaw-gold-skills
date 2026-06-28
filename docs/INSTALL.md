# Installation Guide

## Prerequisites

- OpenClaw installed ([Installation Guide](https://docs.openclaw.ai))
- Python 3.9+
- Telegram bot token (optional, for Telegram notifications)

## Step-by-Step Installation

### 1. Clone Repository
```bash
git clone https://github.com/yourusername/openclaw-gold-skills.git
cd openclaw-gold-skills
```

### 2. Install Dependencies
```bash
pip3 install playwright yfinance websockets
python3 -m playwright install chromium
```

### 3. Copy Skills to OpenClaw
```bash
cp -r skills/* ~/.openclaw/workspace/skills/
```

### 4. Enable Skills
```bash
openclaw skills enable tradingview-scraper
openclaw skills enable gold-analysis
openclaw skills enable telegram-formatting-guide
```

### 5. Configure Telegram (Optional)
Edit `~/.openclaw/openclaw.json`:
```json
{
  "channels": {
    "telegram": {
      "enabled": true,
      "richMessages": true,
      "botToken": "YOUR_BOT_TOKEN"
    }
  }
}
```

### 6. Setup Deriv Token (Optional)
```bash
echo "YOUR_DERIV_TOKEN" > ~/.deriv_api_token
```

### 7. Restart Gateway
```bash
openclaw gateway restart
```

## Verification

Test installation:
```bash
python3 ~/.openclaw/workspace/skills/tradingview-scraper/scripts/gold_master_analysis.py
```

Expected output: HTML table formatted report

## Troubleshooting

| Issue | Solution |
|:---|:---|
| Script not found | Check `~/.openclaw/workspace/skills/` path |
| Import error | Install requirements: `pip3 install -r requirements.txt` |
| Telegram not formatting | Enable `richMessages: true` in config |
| Deriv API error | Check `~/.deriv_api_token` file |

## Next Steps

See [USAGE.md](USAGE.md) for usage examples.
