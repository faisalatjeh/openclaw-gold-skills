#!/usr/bin/env python3
"""
Entry Monitor v2 — Integrated with Market Analysis
Monitors price vs entry + checks market conditions + generates smart alerts
"""

import json
import os
import subprocess
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

def get_market_analysis():
    """Get brief market analysis"""
    # Check if analysis file exists
    analysis_file = '/Users/faisalk/.openclaw/workspace/latest_analysis.json'
    if os.path.exists(analysis_file):
        with open(analysis_file, 'r') as f:
            return json.load(f)
    
    # Default analysis
    return {
        'trend': 'Bearish',
        'dxy': 120.40,
        'smc_structure': 'Bullish on H1',
        'reversal_risk': 'LOW',
        'news_risk': 'MEDIUM'
    }

def calculate_pnl(entry, current_price):
    """Calculate P&L"""
    if entry['direction'] == 'SELL':
        return entry['entry_price'] - current_price
    else:
        return current_price - entry['entry_price']

def determine_action(entry, current_price, pnl, analysis):
    """Determine action based on price + market analysis"""
    
    entry_price = entry['entry_price']
    sl = entry['stop_loss']
    tp1 = entry.get('take_profit_1')
    tp2 = entry.get('take_profit_2')
    tp3 = entry.get('take_profit_3')
    
    # Check reversal risk from analysis
    reversal_risk = analysis.get('reversal_risk', 'LOW')
    smc = analysis.get('smc_structure', '')
    
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
        
        # Check reversal risk
        if reversal_risk == 'HIGH' and 'Bullish' in smc:
            return "REVERSAL WARNING", f"⚠️ Trend berubah! Pertimbangkan close dini atau pindah SL"
        
        # Check near TP1 (90%)
        if tp1:
            tp_distance = entry_price - tp1
            current_progress = entry_price - current_price
            if current_progress >= tp_distance * 0.9:
                return "NEAR TP1", f"📍 Dekat TP1! Siap-siap close atau partial"
        
        # Check breakeven
        if abs(current_price - entry_price) <= 2:
            return "BREAKEVEN", f"⚖️ Price di breakeven! Pindah SL ke entry"
        
        # Check near SL
        if current_price >= sl - ((sl - entry_price) * 0.1):
            return "WARNING", f"⚠️ Price mendekati SL! Hati-hati"
        
        # Default with analysis context
        if pnl > 0:
            if reversal_risk == 'MEDIUM':
                return "HOLD WITH CAUTION", f"💰 Profit ${pnl:.2f} tapi reversal risk {reversal_risk} — Pertimbangkan trailing stop"
            return "HOLD PROFIT", f"💰 Running profit ${pnl:.2f} — Hold ke TP"
        else:
            return "HOLD LOSS", f"📉 Floating loss ${abs(pnl):.2f} — Hold sesuai plan"
    
    else:  # BUY
        # For BUY: profit when price goes up
        
        if tp3 and current_price >= tp3:
            return "CLOSE 100%", f"🎯 TP3 tercapai! Close all positions"
        
        if tp2 and current_price >= tp2:
            return "TP2 REACHED", f"🎯 TP2 tercapai! Close 100% atau move SL"
        
        if tp1 and current_price >= tp1:
            return "TP1 REACHED", f"✅ TP1 tercapai! Pertimbangkan partial close 50%"
        
        # Check reversal
        if reversal_risk == 'HIGH' and 'Bearish' in smc:
            return "REVERSAL WARNING", f"⚠️ Trend berubah! Pertimbangkan close dini"
        
        if abs(current_price - entry_price) <= 2:
            return "BREAKEVEN", f"⚖️ Price di breakeven! Pindah SL ke entry"
        
        if current_price <= sl + ((entry_price - sl) * 0.1):
            return "WARNING", f"⚠️ Price mendekati SL! Hati-hati"
        
        if pnl > 0:
            if reversal_risk == 'MEDIUM':
                return "HOLD WITH CAUTION", f"💰 Profit ${pnl:.2f} tapi reversal risk {reversal_risk}"
            return "HOLD PROFIT", f"💰 Running profit ${pnl:.2f} — Hold ke TP"
        else:
            return "HOLD LOSS", f"📉 Floating loss ${abs(pnl):.2f} — Hold sesuai plan"

def generate_integrated_report():
    """Generate monitor + analysis report"""
    
    entry = load_entry()
    if not entry:
        print("❌ Tidak ada active entry.")
        print("   Buat dengan: echo '{...}' > active_entry.json")
        return
    
    current_price = load_current_price()
    if not current_price:
        print("❌ Current price tidak tersedia.")
        return
    
    analysis = get_market_analysis()
    pnl = calculate_pnl(entry, current_price)
    action, description = determine_action(entry, current_price, pnl, analysis)
    
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
• TP1: ${entry.get('take_profit_1', 'N/A'):,.2f}
• TP2: ${entry.get('take_profit_2', 'N/A'):,.2f}
• TP3: ${entry.get('take_profit_3', 'N/A'):,.2f}

🛑 STOP LOSS: ${entry['stop_loss']:,.2f}

📊 MARKET ANALYSIS:
• Trend: {analysis.get('trend', 'Unknown')}
• DXY: {analysis.get('dxy', 'Unknown')}
• SMC Structure: {analysis.get('smc_structure', 'Unknown')}
• Reversal Risk: {analysis.get('reversal_risk', 'Unknown')} {'⚠️' if analysis.get('reversal_risk') in ['HIGH', 'MEDIUM'] else '✅'}

💡 SARAN: {get_saran(action, analysis)}
⏰ Updated: {datetime.now().strftime('%H:%M:%S')}
"""
    
    print(report)
    
    # Save status
    status = {
        'symbol': entry['symbol'],
        'current_price': current_price,
        'pnl': pnl,
        'action': action,
        'description': description,
        'analysis': analysis,
        'timestamp': datetime.now().isoformat()
    }
    
    with open('/Users/faisalk/.openclaw/workspace/entry_status.json', 'w') as f:
        json.dump(status, f, indent=2)

def get_saran(action, analysis):
    """Get smart suggestion based on action + analysis"""
    reversal = analysis.get('reversal_risk', 'LOW')
    smc = analysis.get('smc_structure', '')
    
    if action == "REVERSAL WARNING":
        return f"🚨 Trend berubah! SMC: {smc}. Pertimbangkan close dini atau pindah SL ke breakeven."
    elif action == "HOLD WITH CAUTION":
        return f"⚠️ Profit ada tapi risk {reversal}. Pertimbangkan trailing stop atau partial close."
    elif action == "CLOSE 100%":
        return f"🎯 Target tercapai! Ambil profit dan tunggu setup baru."
    elif action == "TP1 REACHED":
        return f"✅ TP1 tercapai! Close 50%, sisanya hold ke TP2 dengan SL di breakeven."
    elif action == "BREAKEVEN":
        return f"⚖️ Pindah SL ke entry price (${analysis.get('entry_price', 'N/A')}) untuk protect capital."
    elif action == "WARNING":
        return f"⚠️ Hati-hati! Jangan tambah posisi. Pertimbangkan cut loss jika plan invalid."
    elif "HOLD PROFIT" in action:
        return f"💰 Bagus! Hold ke target atau pasang trailing stop. SMC: {smc}"
    else:
        return f"📊 Monitor terus. Reversal risk: {reversal}. SMC: {smc}"

if __name__ == '__main__':
    generate_integrated_report()