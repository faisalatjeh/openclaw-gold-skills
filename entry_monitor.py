#!/usr/bin/env python3
"""
Entry Monitor — Auto-action alerts for active positions
Monitors price vs entry/stop/target and generates actions
"""

import json
import os
from datetime import datetime

def load_entry():
    """Load active entry from file"""
    entry_file = '/Users/faisalk/.openclaw/workspace/active_entry.json'
    if os.path.exists(entry_file):
        with open(entry_file, 'r') as f:
            return json.load(f)
    return None

def load_current_price():
    """Load current price"""
    price_file = '/Users/faisalk/.openclaw/workspace/current_price.json'
    if os.path.exists(price_file):
        with open(price_file, 'r') as f:
            data = json.load(f)
            return data.get('price', 0)
    return 0

def calculate_pnl(entry, current_price):
    """Calculate P&L"""
    if entry['direction'] == 'SELL':
        return entry['entry_price'] - current_price
    else:  # BUY
        return current_price - entry['entry_price']

def determine_action(entry, current_price, pnl):
    """Determine action based on price position"""
    
    entry_price = entry['entry_price']
    sl = entry['stop_loss']
    tp1 = entry.get('take_profit_1')
    tp2 = entry.get('take_profit_2')
    tp3 = entry.get('take_profit_3')
    
    if entry['direction'] == 'SELL':
        # For SELL: profit when price goes down
        
        # Check TP3
        if tp3 and current_price <= tp3:
            return "CLOSE 100%", f"🎯 TP3 tercapai! Close all positions"
        
        # Check TP2
        if tp2 and current_price <= tp2:
            return "TP2 REACHED", f"🎯 TP2 tercapai! Close 100% atau move SL ke TP1"
        
        # Check TP1
        if tp1 and current_price <= tp1:
            return "TP1 REACHED", f"✅ TP1 tercapai! Pertimbangkan partial close 50%"
        
        # Check near TP1 (90%)
        if tp1:
            tp_distance = entry_price - tp1
            current_progress = entry_price - current_price
            if current_progress >= tp_distance * 0.9:
                return "NEAR TP1", f"📍 Dekat TP1! Siap-siap close atau partial"
        
        # Check breakeven (entry ± $2)
        if abs(current_price - entry_price) <= 2:
            return "BREAKEVEN", f"⚖️ Price di breakeven! Pertimbangkan pindah SL ke entry"
        
        # Check near SL (90%)
        sl_distance = sl - entry_price if entry['direction'] == 'SELL' else entry_price - sl
        if sl_distance > 0:
            if entry['direction'] == 'SELL' and current_price >= entry_price + (sl_distance * 0.9):
                return "WARNING", f"⚠️ Price mendekati SL! Hati-hati"
        
        # Default
        if pnl > 0:
            return "HOLD PROFIT", f"💰 Running profit ${pnl:.2f} — Hold ke TP"
        else:
            return "HOLD LOSS", f"📉 Floating loss ${abs(pnl):.2f} — Hold sesuai plan"
    
    else:  # BUY
        # For BUY: profit when price goes up
        
        # Check TP3
        if tp3 and current_price >= tp3:
            return "CLOSE 100%", f"🎯 TP3 tercapai! Close all positions"
        
        # Check TP2
        if tp2 and current_price >= tp2:
            return "TP2 REACHED", f"🎯 TP2 tercapai! Close 100% atau move SL ke TP1"
        
        # Check TP1
        if tp1 and current_price >= tp1:
            return "TP1 REACHED", f"✅ TP1 tercapai! Pertimbangkan partial close 50%"
        
        # Check near TP1
        if tp1:
            tp_distance = tp1 - entry_price
            current_progress = current_price - entry_price
            if current_progress >= tp_distance * 0.9:
                return "NEAR TP1", f"📍 Dekat TP1! Siap-siap close atau partial"
        
        # Check breakeven
        if abs(current_price - entry_price) <= 2:
            return "BREAKEVEN", f"⚖️ Price di breakeven! Pertimbangkan pindah SL ke entry"
        
        # Check near SL
        if current_price <= sl + ((entry_price - sl) * 0.1):
            return "WARNING", f"⚠️ Price mendekati SL! Hati-hati"
        
        # Default
        if pnl > 0:
            return "HOLD PROFIT", f"💰 Running profit ${pnl:.2f} — Hold ke TP"
        else:
            return "HOLD LOSS", f"📉 Floating loss ${abs(pnl):.2f} — Hold sesuai plan"

def generate_monitor_report():
    """Generate full monitor report"""
    
    entry = load_entry()
    if not entry:
        print("❌ Tidak ada active entry. Buat dulu dengan:")
        print("   echo '{...}' > ~/.openclaw/workspace/active_entry.json")
        return
    
    current_price = load_current_price()
    if not current_price:
        print("❌ Current price tidak tersedia. Fetch dulu:")
        print("   python3 ~/.openclaw/workspace/tradingview_cron.py")
        return
    
    pnl = calculate_pnl(entry, current_price)
    action, description = determine_action(entry, current_price, pnl)
    
    # Calculate distances
    if entry['direction'] == 'SELL':
        tp1_distance = entry['entry_price'] - current_price if entry.get('take_profit_1') else 0
        sl_distance = current_price - entry['stop_loss']
    else:
        tp1_distance = current_price - entry['entry_price'] if entry.get('take_profit_1') else 0
        sl_distance = entry['stop_loss'] - current_price
    
    report = f"""
📊 ENTRY MONITOR — {entry['symbol']} {entry['direction']}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🎯 Entry: {entry['direction']} ${entry['entry_price']:,.2f}
📍 Current: ${current_price:,.2f}
💰 P&L: ${pnl:,.2f} ({'Profit' if pnl > 0 else 'Loss' if pnl < 0 else 'Breakeven'})
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⚡ ACTION: {action}
📝 {description}

🎯 TARGETS:
• TP1: ${entry.get('take_profit_1', 'N/A'):,.2f} {'✅ REACHED' if entry.get('take_profit_1') and ((entry['direction'] == 'SELL' and current_price <= entry['take_profit_1']) or (entry['direction'] == 'BUY' and current_price >= entry['take_profit_1'])) else ''}
• TP2: ${entry.get('take_profit_2', 'N/A'):,.2f}
• TP3: ${entry.get('take_profit_3', 'N/A'):,.2f}

🛑 STOP LOSS: ${entry['stop_loss']:,.2f} ({sl_distance:,.2f} pips)

📊 Position Size: {entry.get('position_size', 'Unknown')}
🕐 Created: {entry.get('created_at', 'Unknown')}
⏰ Updated: {datetime.now().strftime('%H:%M:%S')}

💡 Saran: {get_saran(action)}
"""
    
    print(report)
    
    # Save status
    status = {
        'symbol': entry['symbol'],
        'current_price': current_price,
        'pnl': pnl,
        'action': action,
        'description': description,
        'timestamp': datetime.now().isoformat()
    }
    
    with open('/Users/faisalk/.openclaw/workspace/entry_status.json', 'w') as f:
        json.dump(status, f, indent=2)

def get_saran(action):
    """Get suggestion based on action"""
    saran = {
        "CLOSE 100%": "🎯 Target tercapai! Close semua posisi dan ambil profit.",
        "TP2 REACHED": "✅ TP2 tercapai! Close 100% atau pindah SL ke TP1 untuk trail.",
        "TP1 REACHED": "💡 TP1 tercapai! Pertimbangkan close 50%, sisanya hold ke TP2.",
        "NEAR TP1": "📍 Siap-siap! Bisa partial close atau pindah SL ke breakeven.",
        "BREAKEVEN": "⚖️ Pindah SL ke entry price untuk protect capital.",
        "WARNING": "⚠️ Jangan tambah posisi! Pertimbangkan cut loss jika plan invalid.",
        "HOLD PROFIT": "💰 Bagus! Hold ke target atau trailing stop.",
        "HOLD LOSS": "📉 Tunggu konfirmasi. Jangan panic exit sebelum SL tercapai."
    }
    return saran.get(action, "Monitor terus price action.")

if __name__ == '__main__':
    generate_monitor_report()