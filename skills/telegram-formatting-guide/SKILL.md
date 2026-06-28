---
name: "telegram-formatting-guide"
description: "Always use HTML table formatting for all messages in Telegram"
---

# Telegram Formatting Guide

## Overview

This skill ensures all outgoing messages to Telegram use **HTML table formatting** with minimalis style (clean boxes, not dashed lines).

## Formatting Rules (MUST FOLLOW)

### 1. Tables
Always use HTML table format with `|:---|:---|` alignment:

```markdown
| Header 1 | Header 2 | Header 3 |
|:---|:---|:---|
| Value 1 | Value 2 | Value 3 |
| **Bold** | Normal | **Bold** |
```

**NOT allowed:**
- ASCII art tables (gabungan `+`, `-`, `|`)
- Code block tables
- Dashed lines (`---`)

### 2. Headers
Use emoji headers for sections:

```markdown
## 📊 Section Title
## 🎯 Key Points
## ⚠️ Warnings
```

### 3. Emphasis
- Use `**bold**` for important values, prices, signals
- Use `*italic*` for secondary info
- Use 🔴 🟢 🟡 ⚪ for status indicators

### 4. Lists
Use bullet points with emoji:

```markdown
• Point 1
• Point 2
• Point 3
```

### 5. Examples

**Good (HTML Table):**
```markdown
| Timeframe | Open | Close |
|:---|:---|:---|
| **1d** | $4,014 | **$4,081** |
```

**Bad (ASCII Art):**
```markdown
+-----------+--------+--------+
| Timeframe | Open   | Close  |
+-----------+--------+--------+
| 1d        | $4,014 | $4,081 |
+-----------+--------+--------+
```

## When to Use Tables

Use tables for:
- Price data
- Comparisons
- Statistics
- Schedules
- Configurations
- Any structured data

## When NOT to Use Tables

Don't use tables for:
- Simple chat/greetings
- Short answers (< 3 items)
- Casual conversation

## Channel-Specific

### Telegram
- Requires `richMessages: true` in config
- Renders HTML tables natively
- Supports bold, italic, links in tables

### Other Channels
- Fallback to bullet points if tables not supported
- Keep same minimalis style

## Examples by Category

### Financial Analysis
```markdown
## 💰 Price Data
| Timeframe | Open | High | Low | Close |
|:---|:---|:---|:---|:---|
| **1d** | $4,014 | $4,095 | $3,983 | **$4,081** |
```

### Status Report
```markdown
## 📊 System Status
| Component | Status | Detail |
|:---|:---|:---|
| **Gateway** | 🟢 Online | Port 18789 |
| **Telegram** | 🟢 Connected | Bot active |
```

### Schedule
```markdown
## 📅 Weekly Schedule
| Day | Task | Time |
|:---|:---|:---|
| **Monday** | Market Analysis | 08:00 ET |
| **Friday** | Weekly Review | 18:00 ET |
```

## Validation

Before sending, check:
- [ ] Tables use `|:---|:---|` format
- [ ] No ASCII art borders (`+`, `-` repeated)
- [ ] Important values are **bold**
- [ ] Emoji headers used
- [ ] Clean, minimalis appearance

## Notes

- Keep columns minimal (max 6 per table)
- Use consistent alignment (left-align recommended)
- Bold key data points for quick scanning
- Always consider mobile view (narrow tables)
