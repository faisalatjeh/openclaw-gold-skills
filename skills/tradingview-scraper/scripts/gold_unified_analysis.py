#!/usr/bin/env python3
"""
Unified Gold Analysis — TradingView + SMC + Real-time Data
Combines:
1. TradingView Technical Analysis (RSI, MACD, MA, Pivot levels)
2. Smart Money Concepts (SMC) — Structure, Liquidity, FVG
3. Real-time price data (gold-monitor API)
4. yfinance indicators

Usage:
    python3 gold_unified_analysis.py [--symbol XAUUSD] [--json]
"""

import asyncio
import json
import sys
import argparse
import subprocess
import os
from datetime import datetime

# ============================================
# PART 1: REAL-TIME PRICE (yfinance — COMEX futures)
# ============================================
def get_realtime_price():
    """Fetch real-time gold price from yfinance (COMEX GC=F)"""
    import yfinance as yf
    
    try:
        # Get COMEX Gold futures (GC=F) — most accurate for XAUUSD
        data = yf.download("GC=F", period="1d", interval="1m", progress=False)
        if len(data) == 0:
            # Fallback to gold-monitor if yfinance fails
            return get_price_from_monitor()
        
        latest = data.iloc[-1]
        current_price = float(latest["Close"].iloc[0]) if hasattr(latest["Close"], "iloc") else float(latest["Close"])
        prev_price = float(data.iloc[-2]["Close"].iloc[0]) if hasattr(data.iloc[-2]["Close"], "iloc") else float(data.iloc[-2]["Close"])
        
        change = current_price - prev_price
        change_pct = (change / prev_price) * 100
        
        return {
            "price": round(current_price, 2),
            "change": round(change, 2),
            "change_pct": round(change_pct, 2),
            "unit": "USD/oz",
            "source": "yfinance (COMEX GC=F)",
            "update_time": str(data.index[-1])
        }
    except Exception as e:
        # Fallback to gold-monitor
        return get_price_from_monitor()


def get_price_from_monitor():
    """Fallback price from gold-monitor skill"""
    try:
        result = subprocess.run(
            ["python3", os.path.expanduser("~/.openclaw/workspace/skills/gold-monitor/query.py"), "XAUUSD"],
            capture_output=True, text=True, timeout=30
        )
        data = json.loads(result.stdout)
        return {
            "price": data.get("price", 0),
            "change": data.get("change", 0),
            "change_pct": data.get("change_pct", 0),
            "unit": data.get("unit", "USD/oz"),
            "source": "gold-monitor (Sina Finance)",
            "update_time": data.get("update_time", "")
        }
    except Exception as e:
        return {"error": str(e), "source": "failed"}


# ============================================
# PART 2: TRADINGVIEW TECHNICALS
# ============================================
async def scrape_tv_technicals(symbol="XAUUSD"):
    """Scrape TradingView technical analysis"""
    from playwright.async_api import async_playwright
    
    url = f"https://www.tradingview.com/symbols/{symbol}/technicals/"
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
            viewport={"width": 1920, "height": 1080}
        )
        page = await context.new_page()
        
        try:
            await page.goto(url, wait_until="domcontentloaded", timeout=30000)
            await asyncio.sleep(5)
            
            page_text = await page.evaluate("() => document.body.innerText")
            
            import re
            from collections import Counter
            
            # Extract recommendations
            all_recs = re.findall(r'(Strong Buy|Buy|Neutral|Sell|Strong Sell)', page_text)
            rec_counts = Counter(all_recs)
            
            total = sum(rec_counts.values())
            if total > 0:
                sell_count = rec_counts.get('Sell', 0) + rec_counts.get('Strong Sell', 0)
                buy_count = rec_counts.get('Buy', 0) + rec_counts.get('Strong Buy', 0)
                neutral_count = rec_counts.get('Neutral', 0)
                
                if sell_count > buy_count:
                    overall = "SELL"
                elif buy_count > sell_count:
                    overall = "BUY"
                else:
                    overall = "NEUTRAL"
            else:
                overall = "UNKNOWN"
            
            # Extract oscillators
            oscillators = {}
            osc_match = re.search(r'Oscillators.*?Name\tValue\tAction(.*?)(?=Moving Averages)', page_text, re.DOTALL)
            if osc_match:
                for line in osc_match.group(1).strip().split('\n'):
                    parts = line.split('\t')
                    if len(parts) >= 3:
                        oscillators[parts[0]] = {"value": parts[1], "action": parts[2]}
            
            # Extract MAs
            mas = {}
            ma_match = re.search(r'Moving Averages.*?Name\tValue\tAction(.*?)(?=Pivots)', page_text, re.DOTALL)
            if ma_match:
                for line in ma_match.group(1).strip().split('\n'):
                    parts = line.split('\t')
                    if len(parts) >= 3:
                        mas[parts[0]] = {"value": parts[1], "action": parts[2]}
            
            # Extract pivots
            pivots = {}
            pivot_match = re.search(r'Pivot\tClassic\tFibonacci.*?\n(.*?)(?=\n\n|\Z)', page_text, re.DOTALL)
            if pivot_match:
                for line in pivot_match.group(1).strip().split('\n'):
                    parts = line.split('\t')
                    if len(parts) >= 2 and parts[0] in ['R3','R2','R1','P','S1','S2','S3']:
                        pivots[parts[0]] = {"classic": parts[1], "fibonacci": parts[2] if len(parts) > 2 else ""}
            
            await browser.close()
            
            return {
                "overall": overall,
                "counts": dict(rec_counts),
                "oscillators": oscillators,
                "moving_averages": mas,
                "pivots": pivots
            }
            
        except Exception as e:
            await browser.close()
            return {"error": str(e)}


# ============================================
# PART 3: SMC ANALYSIS
# ============================================
def get_candles_yf(symbol="GC=F", period="5d", interval="5m"):
    """Fetch candles from yfinance"""
    import yfinance as yf
    
    data = yf.download(symbol, period=period, interval=interval, progress=False)
    if len(data) == 0:
        return None
    
    candles = []
    for idx, row in data.iterrows():
        candles.append({
            "time": idx,
            "open": float(row["Open"].iloc[0]) if hasattr(row["Open"], 'iloc') else float(row["Open"]),
            "high": float(row["High"].iloc[0]) if hasattr(row["High"], 'iloc') else float(row["High"]),
            "low": float(row["Low"].iloc[0]) if hasattr(row["Low"], 'iloc') else float(row["Low"]),
            "close": float(row["Close"].iloc[0]) if hasattr(row["Close"], 'iloc') else float(row["Close"])
        })
    return candles


def find_swing_highs(candles, lookback=5):
    """Find swing highs"""
    swings = []
    for i in range(lookback, len(candles) - lookback):
        is_swing = all(
            candles[i]["high"] >= candles[i-j]["high"] and
            candles[i]["high"] >= candles[i+j]["high"]
            for j in range(1, lookback+1)
        )
        if is_swing:
            swings.append((i, candles[i]["high"]))
    return swings


def find_swing_lows(candles, lookback=5):
    """Find swing lows"""
    swings = []
    for i in range(lookback, len(candles) - lookback):
        is_swing = all(
            candles[i]["low"] <= candles[i-j]["low"] and
            candles[i]["low"] <= candles[i+j]["low"]
            for j in range(1, lookback+1)
        )
        if is_swing:
            swings.append((i, candles[i]["low"]))
    return swings


def analyze_structure(candles, lookback=50):
    """Analyze market structure"""
    if len(candles) < lookback + 10:
        return "NEUTRAL", 0

    recent = candles[-lookback:]
    highs = find_swing_highs(recent, 3)
    lows = find_swing_lows(recent, 3)

    if len(highs) < 2 or len(lows) < 2:
        return "NEUTRAL", 0

    sh1, sh2 = highs[-2][1], highs[-1][1]
    sl1, sl2 = lows[-2][1], lows[-1][1]

    bullish = bearish = 0
    if sh2 > sh1: bullish += 1
    else: bearish += 1
    if sl2 > sl1: bullish += 1
    else: bearish += 1
    
    closes = [c["close"] for c in candles[-5:]]
    if closes[-1] > closes[0]: bullish += 1
    else: bearish += 1
    
    ema_fast = sum([c["close"] for c in candles[-10:]]) / 10
    ema_slow = sum([c["close"] for c in candles[-30:]]) / 30
    if ema_fast > ema_slow: bullish += 1
    else: bearish += 1

    if bullish >= 3: return "BULLISH", bullish
    elif bearish >= 3: return "BEARISH", bearish
    return "NEUTRAL", 0


def detect_liquidity_grab(candles):
    """Detect liquidity grabs"""
    if len(candles) < 10:
        return None, 0

    recent = candles[-10:]
    prev = candles[-2]
    curr = candles[-1]
    recent_highs = [c["high"] for c in recent[:-2]]
    recent_lows = [c["low"] for c in recent[:-2]]

    if not recent_highs or not recent_lows:
        return None, 0

    max_high = max(recent_highs)
    min_low = min(recent_lows)

    if prev["high"] > max_high:
        wick = prev["high"] - max(prev["open"], prev["close"])
        body = abs(prev["open"] - prev["close"])
        if wick > body * 1.5 and curr["close"] < curr["open"]:
            return "BEARISH_GRAB", 2

    if prev["low"] < min_low:
        wick = min(prev["open"], prev["close"]) - prev["low"]
        body = abs(prev["open"] - prev["close"])
        if wick > body * 1.5 and curr["close"] > curr["open"]:
            return "BULLISH_GRAB", 2

    return None, 0


def detect_fvg(candles):
    """Detect Fair Value Gaps"""
    if len(candles) < 3:
        return None, 0
    c1, c3 = candles[-3], candles[-1]
    if c1["high"] < c3["low"]: return "BULLISH_FVG", 1
    if c1["low"] > c3["high"]: return "BEARISH_FVG", 1
    return None, 0


def get_sr_levels(candles_1h, candles_5m, threshold=8.0):
    """Support/Resistance levels"""
    if not candles_1h or not candles_5m:
        return None, None, False, False

    h1_highs = sorted([c["high"] for c in candles_1h[-30:]], reverse=True)
    h1_lows = sorted([c["low"] for c in candles_1h[-30:]])

    resistance = h1_highs[2] if len(h1_highs) > 2 else h1_highs[0]
    support = h1_lows[2] if len(h1_lows) > 2 else h1_lows[0]
    current = candles_5m[-1]["close"]

    return support, resistance, abs(current-support) < threshold, abs(resistance-current) < threshold


def check_candle_pattern(candles):
    """Candlestick pattern detection"""
    if len(candles) < 3:
        return None, 0

    c2, c3 = candles[-2], candles[-1]
    
    if (c2["open"] < c2["close"] and c3["open"] > c3["close"] and
        c3["open"] >= c2["close"] and c3["close"] <= c2["open"]):
        return "BEARISH_ENGULF", 2
    elif (c2["open"] > c2["close"] and c3["open"] < c3["close"] and
          c3["open"] <= c2["close"] and c3["close"] >= c2["open"]):
        return "BULLISH_ENGULF", 2
    elif (c3["high"] - max(c3["open"], c3["close"])) > (2 * abs(c3["open"] - c3["close"])):
        return "SHOOTING_STAR", 1
    elif (min(c3["open"], c3["close"]) - c3["low"]) > (2 * abs(c3["open"] - c3["close"])):
        return "HAMMER", 1
    return None, 0


def calculate_rsi(candles, period=14):
    """RSI calculation"""
    if len(candles) < period + 1:
        return 50
    closes = [c["close"] for c in candles[-(period+1):]]
    gains, losses = [], []
    for i in range(1, len(closes)):
        diff = closes[i] - closes[i-1]
        gains.append(diff if diff > 0 else 0)
        losses.append(abs(diff) if diff < 0 else 0)
    avg_gain = sum(gains) / period
    avg_loss = sum(losses) / period
    if avg_loss == 0:
        return 100
    return round(100 - (100 / (1 + avg_gain / avg_loss)), 2)


def generate_smc_analysis(candles_5m, candles_1h):
    """Generate full SMC analysis"""
    if not candles_5m or not candles_1h:
        return None

    current = candles_5m[-1]["close"]
    h1_struct, h1_score = analyze_structure(candles_1h)
    m5_struct, m5_score = analyze_structure(candles_5m)
    liq, liq_score = detect_liquidity_grab(candles_5m)
    pat, pat_score = check_candle_pattern(candles_5m)
    fvg, fvg_score = detect_fvg(candles_5m)
    support, resistance, near_s, near_r = get_sr_levels(candles_1h, candles_5m)
    rsi = calculate_rsi(candles_5m)

    # Long score
    long_score = 0
    long_reasons = []
    if h1_struct == "BULLISH":
        long_score += 30; long_reasons.append("H1 Bullish Structure")
    if m5_struct == "BULLISH":
        long_score += 15; long_reasons.append("M5 Bullish Structure")
    if liq == "BULLISH_GRAB":
        long_score += 20; long_reasons.append("Bullish Liquidity Grab")
    if pat in ["BULLISH_ENGULF", "HAMMER"]:
        long_score += pat_score * 8; long_reasons.append(f"Pattern: {pat}")
    if fvg == "BULLISH_FVG":
        long_score += 10; long_reasons.append("Bullish FVG")
    if near_s:
        long_score += 10; long_reasons.append("Near Support")
    if rsi < 40:
        long_score += 10; long_reasons.append(f"RSI Oversold ({rsi})")

    # Short score
    short_score = 0
    short_reasons = []
    if h1_struct == "BEARISH":
        short_score += 30; short_reasons.append("H1 Bearish Structure")
    if m5_struct == "BEARISH":
        short_score += 15; short_reasons.append("M5 Bearish Structure")
    if liq == "BEARISH_GRAB":
        short_score += 20; short_reasons.append("Bearish Liquidity Grab")
    if pat in ["BEARISH_ENGULF", "SHOOTING_STAR"]:
        short_score += pat_score * 8; short_reasons.append(f"Pattern: {pat}")
    if fvg == "BEARISH_FVG":
        short_score += 10; short_reasons.append("Bearish FVG")
    if near_r:
        short_score += 10; short_reasons.append("Near Resistance")
    if rsi > 60:
        short_score += 10; short_reasons.append(f"RSI Overbought ({rsi})")

    return {
        "price": current,
        "h1_structure": h1_struct,
        "m5_structure": m5_struct,
        "liquidity": liq,
        "pattern": pat,
        "fvg": fvg,
        "support": support,
        "resistance": resistance,
        "near_support": near_s,
        "near_resistance": near_r,
        "rsi": rsi,
        "long_score": long_score,
        "short_score": short_score,
        "long_reasons": long_reasons,
        "short_reasons": short_reasons
    }


# ============================================
# PART 4: FORMATTED OUTPUT
# ============================================
def print_analysis(data):
    """Print formatted analysis"""
    
    print("\n" + "="*60)
    print("📊 UNIFIED GOLD ANALYSIS — XAUUSD")
    print("="*60)
    
    # Price Section
    print("\n💰 REAL-TIME PRICE")
    print("-"*40)
    rt = data.get("realtime", {})
    if "error" not in rt:
        print(f"   Price: ${rt.get('price', 'N/A'):,.2f}")
        print(f"   Change: {rt.get('change', 0):+.2f} ({rt.get('change_pct', 0):+.2f}%)")
        print(f"   Updated: {rt.get('update_time', 'N/A')}")
    else:
        print(f"   ⚠️ {rt.get('error', 'Price unavailable')}")
    
    # TradingView Section
    print("\n📈 TRADINGVIEW TECHNICAL ANALYSIS")
    print("-"*40)
    tv = data.get("tradingview", {})
    if "error" not in tv:
        print(f"   Overall Signal: {tv.get('overall', 'N/A')}")
        counts = tv.get('counts', {})
        print(f"   Buy: {counts.get('Buy', 0) + counts.get('Strong Buy', 0)} | "
              f"Neutral: {counts.get('Neutral', 0)} | "
              f"Sell: {counts.get('Sell', 0) + counts.get('Strong Sell', 0)}")
        
        # Oscillators
        oscs = tv.get('oscillators', {})
        if oscs:
            print(f"\n   📊 Key Oscillators:")
            for name, info in list(oscs.items())[:5]:
                emoji = "🟢" if info.get('action') == 'Buy' else "🔴" if info.get('action') == 'Sell' else "🟡"
                print(f"      {emoji} {name}: {info.get('value', 'N/A')} ({info.get('action', 'N/A')})")
        
        # MAs
        mas = tv.get('moving_averages', {})
        if mas:
            buy_ma = sum(1 for v in mas.values() if v.get('action') == 'Buy')
            sell_ma = sum(1 for v in mas.values() if v.get('action') == 'Sell')
            print(f"\n   📉 Moving Averages: {buy_ma} Buy | {sell_ma} Sell")
        
        # Pivots
        pivots = tv.get('pivots', {})
        if pivots:
            print(f"\n   🎯 Key Levels:")
            for level in ['R2', 'R1', 'P', 'S1', 'S2']:
                if level in pivots:
                    print(f"      {level}: ${pivots[level].get('classic', 'N/A')}")
    else:
        print(f"   ⚠️ {tv.get('error', 'TV data unavailable')}")
    
    # SMC Section
    print("\n🧠 SMART MONEY CONCEPTS (SMC)")
    print("-"*40)
    smc = data.get("smc", {})
    if smc:
        print(f"   Price: ${smc.get('price', 0):,.2f}")
        print(f"   H1 Structure: {smc.get('h1_structure', 'N/A')} | M5 Structure: {smc.get('m5_structure', 'N/A')}")
        print(f"   Pattern: {smc.get('pattern', 'None')} | Liquidity: {smc.get('liquidity', 'None')}")
        print(f"   FVG: {smc.get('fvg', 'None')}")
        print(f"   RSI: {smc.get('rsi', 'N/A')}")
        print(f"   Support: ${smc.get('support', 0):,.2f} | Resistance: ${smc.get('resistance', 0):,.2f}")
        print(f"   Near Support: {smc.get('near_support', False)} | Near Resistance: {smc.get('near_resistance', False)}")
        
        print(f"\n   🟢 Long Score: {smc.get('long_score', 0)}")
        for reason in smc.get('long_reasons', []):
            print(f"      ✅ {reason}")
        
        print(f"   🔴 Short Score: {smc.get('short_score', 0)}")
        for reason in smc.get('short_reasons', []):
            print(f"      ✅ {reason}")
    
    # Conclusion
    print("\n" + "="*60)
    print("🎯 VERDICT")
    print("="*60)
    
    tv_signal = tv.get('overall', 'NEUTRAL') if 'error' not in tv else 'UNKNOWN'
    smc_long = smc.get('long_score', 0) if smc else 0
    smc_short = smc.get('short_score', 0) if smc else 0
    
    # Determine consensus
    if tv_signal == 'SELL' and smc_short > smc_long:
        verdict = "🔴 STRONG SELL — Both TV and SMC aligned bearish"
    elif tv_signal == 'BUY' and smc_long > smc_short:
        verdict = "🟢 STRONG BUY — Both TV and SMC aligned bullish"
    elif tv_signal == 'SELL':
        verdict = "🟠 SELL — Technical bearish, SMC mixed"
    elif tv_signal == 'BUY':
        verdict = "🟡 BUY — Technical bullish, SMC mixed"
    else:
        verdict = "⚪ NEUTRAL — Mixed signals, wait for confirmation"
    
    print(f"   {verdict}")
    print(f"   TV Signal: {tv_signal} | SMC Long: {smc_long} | SMC Short: {smc_short}")
    print("="*60 + "\n")


# ============================================
# MAIN
# ============================================
async def main():
    parser = argparse.ArgumentParser(description="Unified Gold Analysis")
    parser.add_argument("--json", action="store_true", help="Output JSON")
    args = parser.parse_args()
    
    print("🚀 Fetching unified gold analysis...")
    
    # 1. Real-time price
    print("   📡 Fetching real-time price...", file=sys.stderr)
    realtime = get_realtime_price()
    
    # 2. TradingView technicals
    print("   📊 Scraping TradingView...", file=sys.stderr)
    tv_data = await scrape_tv_technicals("XAUUSD")
    
    # 3. SMC analysis
    print("   🧠 Analyzing SMC patterns...", file=sys.stderr)
    candles_5m = get_candles_yf("GC=F", "5d", "5m")
    candles_1h = get_candles_yf("GC=F", "30d", "1h")
    smc_data = generate_smc_analysis(candles_5m, candles_1h) if candles_5m and candles_1h else None
    
    # Combine
    result = {
        "symbol": "XAUUSD",
        "timestamp": str(datetime.now()),
        "realtime": realtime,
        "tradingview": tv_data,
        "smc": smc_data
    }
    
    if args.json:
        print(json.dumps(result, indent=2, default=str))
    else:
        print_analysis(result)


if __name__ == "__main__":
    asyncio.run(main())
