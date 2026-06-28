# Cron Jobs Setup

## Auto-Analysis Schedule

Add these to your crontab (`crontab -e`):

### Daily Analysis (08:00 ET)
```cron
0 8 * * * /usr/bin/python3 ~/.openclaw/workspace/skills/tradingview-scraper/scripts/gold_master_analysis.py --json > /tmp/xauusd_daily.json 2>&1
```

### Evening Update (17:00 ET, Weekdays)
```cron
0 17 * * 1-5 /usr/bin/python3 ~/.openclaw/workspace/skills/tradingview-scraper/scripts/gold_master_analysis.py --json > /tmp/xauusd_evening.json 2>&1
```

### Pre-Market Events (07:00 ET, Weekdays)
```cron
0 7 * * 1-5 /usr/bin/python3 ~/.openclaw/workspace/skills/tradingview-scraper/scripts/gold_master_analysis.py --json > /tmp/xauusd_events.json 2>&1
```

### Weekly Outlook (Friday 18:00 ET)
```cron
0 18 * * 5 /usr/bin/python3 ~/.openclaw/workspace/skills/tradingview-scraper/scripts/gold_master_analysis.py --json > /tmp/xauusd_weekly.json 2>&1
```

## OpenClaw Cron Jobs (Recommended)

Use OpenClaw built-in cron for better integration:

```bash
# Add via OpenClaw CLI
openclaw cron add --name "xauusd-daily" --schedule "0 8 * * *" --command "analisa xauusd"
```

Or use the API directly (see main repository).

## Event Alerts

### High Impact Events
```cron
# Check 1 hour before major events
0 7,9 * * 1-5 /usr/bin/python3 ~/.openclaw/workspace/skills/tradingview-scraper/scripts/fundamentals.py --events-only
```

### Price Alerts
```cron
# Check price every 15 minutes during market hours
*/15 6-17 * * 1-5 /usr/bin/python3 ~/.openclaw/workspace/skills/tradingview-scraper/scripts/price_alert.py --symbol XAUUSD
```

## Log Files

All outputs saved to `/tmp/`:
- `xauusd_daily.json` - Daily analysis
- `xauusd_evening.json` - Evening update
- `xauusd_events.json` - Pre-market events
- `xauusd_weekly.json` - Weekly outlook

## Monitoring

Check cron job status:
```bash
# List all cron jobs
crontab -l

# Check recent runs
tail -f /var/log/cron.log

# View latest analysis
cat /tmp/xauusd_daily.json | python3 -m json.tool
```

## Troubleshooting

| Issue | Solution |
|:---|:---|
| Cron not running | Check `crontab -l` for correct paths |
| Permission denied | Make scripts executable: `chmod +x *.py` |
| Output empty | Check Python path: `which python3` |
| Wrong timezone | Set TZ variable: `TZ=America/New_York` |

## Customization

### Modify Schedule
Edit timing in crontab entries above.

### Add More Symbols
Duplicate scripts and change symbol parameter:
```bash
python3 gold_master_analysis.py --symbol frxEURUSD
```

### Integration with Notifications
Add webhook or Telegram notification:
```bash
python3 gold_master_analysis.py --json | python3 send_telegram.py
```
