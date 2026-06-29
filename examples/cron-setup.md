# Cron Jobs Setup

## Scheduled Reports (Always Active)

| Job | ID | Schedule | Description |
|:---|:---|:---|:---|
| xauusd-pre-events | `44f1c9ab-d45f-45aa-a0ab-5af8c4dd928b` | 12:00 AM | Pre-market events |
| xauusd-daily-analysis | `c2f324d4-71f8-4c84-ac00-261c1ca5e9a8` | 06:00 AM | Daily analysis |
| xauusd-evening-update | `8b847b8a-5f51-4917-afb3-26f9780e4247` | 03:00 PM | Evening update |
| xauusd-weekly-outlook | `f44fd1a7-fede-4f8a-b1fd-c84f925909a3` | Sunday 18:00 | Weekly outlook |

## Entry Monitor (On-Demand)

### Activation
```bash
# User says: "Saya ada entry SELL $4,064 SL $4,080"
# System creates active_entry.json
# System asks: "Mau di-monitor?"
# User says: "Ya, setiap 2 menit"
```

### Cron Expression
```bash
*/2 * * * * cd ~/.openclaw/workspace && python3 tradingview_cron.py && python3 entry_monitor_v2.py
```

### Deactivation
```bash
# User says: "Close entry" or "Stop monitor"
# System removes cron job
```

## Setup Commands

### Create Scheduled Reports
```bash
# Pre-events
cron add --name xauusd-pre-events --schedule "0 0 * * *" --script "xauusd_pre_events.py"

# Daily analysis
cron add --name xauusd-daily-analysis --schedule "0 6 * * *" --script "xauusd_daily_analysis.py"

# Evening update
cron add --name xauusd-evening-update --schedule "0 15 * * *" --script "xauusd_evening_update.py"

# Weekly outlook
cron add --name xauusd-weekly-outlook --schedule "0 18 * * 0" --script "xauusd_weekly_outlook.py"
```

### Create Entry Monitor (On-Demand)
```bash
# Only when user requests
cron add --name entry-monitor --schedule "*/2 * * * *" --script "entry_monitor_v2.py"
```

## Timezone
All cron jobs use: **Asia/Jakarta** (WIB)

## Status
Check status:
```bash
cron list
```