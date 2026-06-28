# TELEGRAM-FORMATTING-GUIDE — Applied

## Overview

All outgoing messages to Telegram MUST use **HTML table formatting** with minimalis style.

## Rules (STRICT)

### ✅ MUST DO:
- Use `|:---|:---|` for table alignment
- Use `**bold**` for important values
- Use emoji headers (## 📊)
- Keep tables clean and minimalis

### ❌ NEVER DO:
- ASCII art tables (+, -, | borders)
- Code block tables
- Dashed lines (`---`)

## Examples

**✅ Good:**
```markdown
| Name | Value | Status |
|:---|:---|:---|
| **Gold** | $4,081 | 🟢 Up |
```

**❌ Bad:**
```markdown
+------+-------+--------+
| Name | Value | Status |
+------+-------+--------+
| Gold | $4,081| Up     |
+------+-------+--------+
```

## Applied: 2026-06-28
## Status: ACTIVE
