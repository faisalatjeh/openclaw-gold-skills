#!/usr/bin/env python3
"""
Smart Entry Monitor — Only alert on significant changes
Avoids spam when price is stagnant
"""

import json
import os
from datetime import datetime

def load_entry():
    entry_file = '/Users/faisalk/.openclaw/workspace/active_entry.json'
    if os.path.exists(entry_file):
        with open(entry_file, 'r') as f:
            return json.load(f)
    return None

def load_current_price():
    price_file = '/Users/faisalk/.openclaw/workspace/current_price.json'
    if os.path.exists(price_file):
        with open(price_file, 'r') as f:
            data = json.load(f)
            return data.get('price', 0)
    return 0

def load_last_status():
    status_file = '/Users/faisalk/.openclaw/workspace/entry_status.json'
    if os.path.exists(status_file):
        with open(status_file, 'r') as f:
            return json.load(f)
    return None

def should_alert(current_price, last_status):
    """Determine if we should send alert"""
    if not last_status:
        return True, "First check"
    
    last_price = last_status.get('current_price', 0)
    last_action = last_status.get('action', '')
    last_time = datetime.fromisoformat(last_status.get('timestamp', datetime.now().isoformat()))
    time_diff = (datetime.now() - last_time).total_seconds()
    
    # Alert if price changed significantly (> $2)
    price_diff = abs(current_price - last_price)
    if price_diff >= 2:
        return True, f"Price changed ${price_diff:.2f}"
    
    # Alert if action changed
    current_action = determine_action_simple(current_price)
    if current_action != last_action:
        return True, f"Action changed: {last_action} → {current_action}"
    
    # Alert every 30 minutes even if no change (summary)
    if time_diff >= 1800:  # 30 minutes
        return True, "30 min summary"
    
    # Don't alert
    return False, f"No significant change (price diff: ${price_diff:.2f})"

def determine_action_simple(current_price):
    """Simple action determination"""
    entry = load_entry()
    if not entry:
        return "NO ENTRY"
    
    entry_price = entry['entry_price']
    sl = entry['stop_loss']
    tp1 = entry.get('take_profit_1')
    
    if entry['direction'] == 'SELL':
        if tp1 and current_price <= tp1:
            return "TP1 REACHED"
        if current_price >= sl:
            return "STOP LOSS"
        if current_price <= entry_price:
            return "PROFIT"
        return "HOLD"
    else:
        if tp1 and current_price >= tp1:
            return "TP1 REACHED"
        if current_price <= sl:
            return "STOP LOSS"
        if current_price >= entry_price:
            return "PROFIT"
        return "HOLD"

def generate_smart_report():
    """Generate report only if significant change"""
    
    entry = load_entry()
    if not entry:
        print("❌ Tidak ada active entry.")
        return
    
    current_price = load_current_price()
    if not current_price:
        print("❌ Current price tidak tersedia.")
        return
    
    last_status = load_last_status()
    should_send, reason = should_alert(current_price, last_status)
    
    if not should_send:
        # Silent — no alert needed
        print(f"⏸️ No alert: {reason}")
        return
    
    # Calculate P&L
    if entry['direction'] == 'SELL':
        pnl = entry['entry_price'] - current_price
    else:
        pnl = current_price - entry['entry_price']
    
    action = determine_action_simple(current_price)
    
    # Generate report
    report = f"""
📊 ENTRY MONITOR — {entry['symbol']} {entry['direction']}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🎯 Entry: {entry['direction']} ${entry['entry_price']:,.2f}
📍 Current: ${current_price:,.2f}
💰 P&L: ${pnl:,.2f} ({'Profit' if pnl > 0 else 'Loss' if pnl < 0 else 'Breakeven'})
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⚡ ACTION: {action}
📝 {get_action_description(action, pnl)}

🎯 TARGETS:
• TP1: ${entry.get('take_profit_1', 'N/A'):,.2f}
• TP2: ${entry.get('take_profit_2', 'N/A'):,.2f}
• TP3: ${entry.get('take_profit_3', 'N/A'):,.2f}

🛑 STOP LOSS: ${entry['stop_loss']:,.2f}

⏰ Update: {datetime.now().strftime('%H:%M:%S')}
💡 Alert: {reason}
"""
    
    print(report)
    
    # Save status
    status = {
        'symbol': entry['symbol'],
        'current_price': current_price,
        'pnl': pnl,
        'action': action,
        'timestamp': datetime.now().isoformat()
    }
    
    with open('/Users/faisalk/.openclaw/workspace/entry_status.json', 'w') as f:
        json.dump(status, f, indent=2)

def get_action_description(action, pnl):
    """Get description for action"""
    descriptions = {
        "TP1 REACHED": "🎯 TP1 tercapai! Pertimbangkan partial close",
        "TP2 REACHED": "🎯 TP2 tercapai! Close 100% atau trail SL",
        "TP3 REACHED": "🎯 TP3 tercapai! Close all positions",
        "STOP LOSS": "🛑 STOP LOSS hit! Cut loss sekarang",
        "PROFIT": f"💰 Running profit ${pnl:.2f} — Hold ke target",
        "HOLD": f"⏳ P&L: ${pnl:.2f} — Tunggu development",
        "NO ENTRY": "Tidak ada active entry"
    }
    return descriptions.get(action, "Monitor terus")

if __name__ == '__main__':
    generate_smart_report()