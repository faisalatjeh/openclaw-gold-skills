#!/usr/bin/env python3
"""
GOLD MASTER ANALYSIS — Multi-Timeframe Unified Report
Combines ALL gold analysis skills with multi-timeframe support:
Timeframes: D1, H4, H1, M30, M15, M5, M1
Sources: Deriv API (real-time) + yfinance (fallback)
"""

import asyncio
import json
import sys
import os
import subprocess
import argparse
from datetime import datetime


# ============================================
# PART 1: MULTI-TIMEFRAME PRICE DATA
# ============================================
async def get_multi_timeframe_data(symbol="frxXAUUSD"):
    """
    Fetch multi-timeframe data from Deriv API
    Falls back to yfinance if Deriv fails
    """
    timeframes = {
        "1d": {"style": "candles", "granularity": 86400, "count": 20},
        "4h": {"style": "candles", "granularity": 14400, "count": 30},
        "1h": {"style": "candles", "granularity": 3600, "count": 50},
        "30m": {"style": "candles", "granularity": 1800, "count": 50},
        "15m": {"style": "candles", "granularity": 900, "count": 50},
        "5m": {"style": "candles", "granularity": 300, "count": 50},
        "1m": {"style": "candles", "granularity": 60, "count": 50}
    }
    
    result = {}
    
    # Try Deriv API for each timeframe
    try:
        import websockets
    except ImportError:
        print("   websockets not installed, using yfinance fallback", file=sys.stderr)
        return get_yfinance_multi_timeframe()
    
    # Try to get token from file
    token_path = os.path.expanduser("~/.deriv_api_token")
    token = None
    try:
        with open(token_path, 'r') as f:
            token = f.read().strip()
    except:
        pass
    
    uri = "wss://ws.binaryws.com/websockets/v3?app_id=1089"
    
    try:
        async with websockets.connect(uri) as websocket:
            # Authorize if token exists
            if token:
                auth_msg = {"authorize": token}
                await websocket.send(json.dumps(auth_msg))
                auth_resp = json.loads(await websocket.recv())
                if "error" in auth_resp:
                    print(f"   Auth warning: {auth_resp['error']['message']}", file=sys.stderr)
            
            # Request candles for each timeframe
            for tf_name, tf_config in timeframes.items():
                try:
                    msg = {
                        "ticks_history": symbol,
                        "adjust_start_time": 1,
                        "count": tf_config["count"],
                        "end": "latest",
                        "start": 1,
                        "style": "candles",
                        "granularity": tf_config["granularity"]
                    }
                    await websocket.send(json.dumps(msg))
                    resp = json.loads(await websocket.recv())
                    
                    if "error" in resp:
                        result[tf_name] = {"error": resp["error"]["message"]}
                    else:
                        candles = resp.get("candles", [])
                        if candles:
                            latest = candles[-1]
                            result[tf_name] = {
                                "open": latest.get("open", 0),
                                "high": latest.get("high", 0),
                                "low": latest.get("low", 0),
                                "close": latest.get("close", 0),
                                "epoch": latest.get("epoch", 0),
                                "count": len(candles),
                                "source": "Deriv API"
                            }
                        else:
                            result[tf_name] = {"error": "No candles"}
                            
                except Exception as e:
                    result[tf_name] = {"error": str(e)}
                    
    except Exception as e:
        print(f"   Deriv connection failed: {e}", file=sys.stderr)
        # Fallback to yfinance
        return get_yfinance_multi_timeframe()
    
    return result


def get_yfinance_multi_timeframe():
    """Fallback multi-timeframe from yfinance"""
    import yfinance as yf
    
    result = {}
    intervals = {
        "1d": "1d",
        "4h": "1h",  # yfinance doesn't have 4h, use 1h
        "1h": "1h",
        "30m": "30m",
        "15m": "15m",
        "5m": "5m",
        "1m": "1m"
    }
    
    for tf, yf_interval in intervals.items():
        try:
            data = yf.download("GC=F", period="5d", interval=yf_interval, progress=False)
            if len(data) > 0:
                latest = data.iloc[-1]
                result[tf] = {
                    "open": float(latest["Open"].iloc[0]) if hasattr(latest["Open"], "iloc") else float(latest["Open"]),
                    "high": float(latest["High"].iloc[0]) if hasattr(latest["High"], "iloc") else float(latest["High"]),
                    "low": float(latest["Low"].iloc[0]) if hasattr(latest["Low"], "iloc") else float(latest["Low"]),
                    "close": float(latest["Close"].iloc[0]) if hasattr(latest["Close"], "iloc") else float(latest["Close"]),
                    "source": "yfinance (COMEX GC=F) [Fallback]"
                }
            else:
                result[tf] = {"error": "No data"}
        except Exception as e:
            result[tf] = {"error": str(e)}
    
    return result


# ============================================
# PART 2-6: Other analysis functions (same as before)
# ============================================
def get_fundamental_data():
    """Fetch fundamental data"""
    try:
        result = subprocess.run(
            ["python3", os.path.expanduser("~/.openclaw/workspace/skills/gold-fundamental-analysis/scripts/get_gold_fundamental_data.py")],
            capture_output=True, text=True, timeout=60
        )
        data = json.loads(result.stdout)
        macro = data.get("macro", {})
        cot = data.get("cot", {})
        etf = data.get("etf", {})
        return {
            "fed_rate": macro.get("fed_rate", {}).get("current", "N/A"),
            "cpi": macro.get("cpi", {}).get("current", "N/A"),
            "core_cpi": macro.get("core_cpi", {}).get("current", "N/A"),
            "us10y": macro.get("us10y_yield", {}).get("current", "N/A"),
            "real_yield": macro.get("real_yield", {}).get("current", "N/A"),
            "dxy": macro.get("dxy", {}).get("current", "N/A"),
            "cot_net": cot.get("net_position", "N/A"),
            "cot_label": cot.get("net_position_label", "N/A"),
            "etf_aum": etf.get("aum_usd_millions", "N/A"),
            "etf_tonnes": etf.get("estimated_tonnes", "N/A"),
            "upcoming_events": data.get("economic_calendar", {}).get("upcoming_events", [])[:3]
        }
    except Exception as e:
        return {"error": str(e)}


def get_news_sentiment():
    """Fetch news sentiment"""
    try:
        result = subprocess.run(
            ["python3", os.path.expanduser("~/.openclaw/workspace/skills/gold-news-sentiment/scripts/fetch_news.py"), "--hours", "48", "--limit", "15"],
            capture_output=True, text=True, timeout=60
        )
        data = json.loads(result.stdout)
        items = data.get("items", [])
        bullish_keywords = ["rise", "gain", "bullish", "surge", "climb", "rally", "support", "buy"]
        bearish_keywords = ["fall", "decline", "bearish", "drop", "plunge", "sell", "pressure", "weak"]
        bullish_count = 0
        bearish_count = 0
        headlines = []
        for item in items[:10]:
            title = item.get("title", "").lower()
            headlines.append({
                "title": item.get("title", ""),
                "source": item.get("source", ""),
                "age_hours": round(item.get("age_hours", 0), 1)
            })
            if any(kw in title for kw in bullish_keywords):
                bullish_count += 1
            elif any(kw in title for kw in bearish_keywords):
                bearish_count += 1
        if bullish_count > bearish_count * 1.5:
            sentiment = "BULLISH"
        elif bearish_count > bullish_count * 1.5:
            sentiment = "BEARISH"
        else:
            sentiment = "MIXED"
        return {"sentiment": sentiment, "bullish_count": bullish_count, "bearish_count": bearish_count, "headlines": headlines[:5]}
    except Exception as e:
        return {"error": str(e), "sentiment": "UNKNOWN"}


def get_smc_analysis():
    """SMC analysis"""
    import yfinance as yf
    
    def get_candles(symbol="GC=F", period="5d", interval="5m"):
        data = yf.download(symbol, period=period, interval=interval, progress=False)
        if len(data) == 0:
            return None
        candles = []
        for idx, row in data.iterrows():
            candles.append({
                "time": idx,
                "open": float(row["Open"].iloc[0]) if hasattr(row["Open"], "iloc") else float(row["Open"]),
                "high": float(row["High"].iloc[0]) if hasattr(row["High"], "iloc") else float(row["High"]),
                "low": float(row["Low"].iloc[0]) if hasattr(row["Low"], "iloc") else float(row["Low"]),
                "close": float(row["Close"].iloc[0]) if hasattr(row["Close"], "iloc") else float(row["Close"])
            })
        return candles
    
    def find_swing_highs(candles, lookback=5):
        swings = []
        for i in range(lookback, len(candles) - lookback):
            if all(candles[i]["high"] >= candles[i-j]["high"] and candles[i]["high"] >= candles[i+j]["high"] for j in range(1, lookback+1)):
                swings.append((i, candles[i]["high"]))
        return swings
    
    def find_swing_lows(candles, lookback=5):
        swings = []
        for i in range(lookback, len(candles) - lookback):
            if all(candles[i]["low"] <= candles[i-j]["low"] and candles[i]["low"] <= candles[i+j]["low"] for j in range(1, lookback+1)):
                swings.append((i, candles[i]["low"]))
        return swings
    
    def analyze_structure(candles, lookback=50):
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
    
    try:
        candles_5m = get_candles("GC=F", "5d", "5m")
        candles_1h = get_candles("GC=F", "30d", "1h")
        if not candles_5m or not candles_1h:
            return {"error": "No data"}
        h1_struct, _ = analyze_structure(candles_1h)
        m5_struct, _ = analyze_structure(candles_5m)
        current = candles_5m[-1]["close"]
        return {"price": current, "h1_structure": h1_struct, "m5_structure": m5_struct}
    except Exception as e:
        return {"error": str(e)}


async def get_tradingview_data(max_retries=3):
    """TradingView technicals with retry"""
    from playwright.async_api import async_playwright
    url = "https://www.tradingview.com/symbols/XAUUSD/technicals/"
    for attempt in range(max_retries):
        try:
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=True)
                context = await browser.new_context(user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36", viewport={"width": 1920, "height": 1080})
                page = await context.new_page()
                try:
                    await page.goto(url, wait_until="domcontentloaded", timeout=30000)
                    await asyncio.sleep(5)
                    page_text = await page.evaluate("() => document.body.innerText")
                    import re
                    from collections import Counter
                    all_recs = re.findall(r'(Strong Buy|Buy|Neutral|Sell|Strong Sell)', page_text)
                    rec_counts = Counter(all_recs)
                    total = sum(rec_counts.values())
                    if total > 0:
                        sell_count = rec_counts.get('Sell', 0) + rec_counts.get('Strong Sell', 0)
                        buy_count = rec_counts.get('Buy', 0) + rec_counts.get('Strong Buy', 0)
                        if sell_count > buy_count: overall = "SELL"
                        elif buy_count > sell_count: overall = "BUY"
                        else: overall = "NEUTRAL"
                    else: overall = "UNKNOWN"
                    await browser.close()
                    return {"overall": overall, "counts": dict(rec_counts), "status": "success"}
                except Exception as e:
                    await browser.close()
                    if attempt < max_retries - 1:
                        print(f"   ⚠️ TV attempt {attempt+1} failed, retrying...", file=sys.stderr)
                        await asyncio.sleep(5)
                    else:
                        return {"error": str(e), "status": "failed"}
        except Exception as e:
            if attempt < max_retries - 1:
                print(f"   ⚠️ TV attempt {attempt+1} failed, retrying...", file=sys.stderr)
                await asyncio.sleep(5)
            else:
                return {"error": str(e), "status": "failed"}
    return {"error": "All retries exhausted", "status": "failed"}


# ============================================
# FORMATTED OUTPUT
# ============================================
def print_master_report(data):
    """Print comprehensive master report"""
    
    print("\n" + "="*70)
    print("🥇 GOLD MASTER ANALYSIS — XAUUSD (Multi-Timeframe)")
    print("="*70)
    print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # 1. MULTI-TIMEFRAME PRICE
    print("\n" + "-"*70)
    print("💰 MULTI-TIMEFRAME PRICE DATA")
    print("-"*70)
    mt = data.get("multi_timeframe", {})
    
    print(f"{'Timeframe':<10} {'Open':<12} {'High':<12} {'Low':<12} {'Close':<12} {'Source'}")
    print("-" * 70)
    
    for tf in ["1d", "4h", "1h", "30m", "15m", "5m", "1m"]:
        if tf in mt and "error" not in mt[tf]:
            tf_data = mt[tf]
            print(f"{tf:<10} ${tf_data.get('open', 0):<11,.2f} ${tf_data.get('high', 0):<11,.2f} ${tf_data.get('low', 0):<11,.2f} ${tf_data.get('close', 0):<11,.2f} {tf_data.get('source', 'N/A')}")
        else:
            error_msg = mt.get(tf, {}).get("error", "N/A") if tf in mt else "N/A"
            print(f"{tf:<10} {error_msg:<58}")
    
    # 2. FUNDAMENTAL
    print("\n" + "-"*70)
    print("🏛️ FUNDAMENTAL ANALYSIS")
    print("-"*70)
    fund = data.get("fundamental", {})
    if "error" not in fund:
        print(f"   Fed Rate: {fund.get('fed_rate', 'N/A')}%")
        print(f"   CPI: {fund.get('cpi', 'N/A')}")
        print(f"   Core CPI: {fund.get('core_cpi', 'N/A')}")
        print(f"   10Y Yield: {fund.get('us10y', 'N/A')}%")
        print(f"   Real Yield: {fund.get('real_yield', 'N/A')}%")
        print(f"   DXY: {fund.get('dxy', 'N/A')}")
        print(f"   COT Net: {fund.get('cot_net', 'N/A')} ({fund.get('cot_label', 'N/A')})")
        print(f"   ETF AUM: ${fund.get('etf_aum', 'N/A')}M")
        print(f"   ETF Tonnes: {fund.get('etf_tonnes', 'N/A')}t")
        events = fund.get("upcoming_events", [])
        if events:
            print(f"\n   📅 Upcoming Events:")
            for evt in events:
                print(f"      • {evt.get('event', '')}: {evt.get('date', '')[:10]}")
    else:
        print(f"   ⚠️ {fund.get('error', 'Data unavailable')}")
    
    # 3. NEWS
    print("\n" + "-"*70)
    print("📰 NEWS SENTIMENT (48h)")
    print("-"*70)
    news = data.get("news", {})
    if "error" not in news:
        print(f"   Overall: {news.get('sentiment', 'N/A')}")
        print(f"   Bullish Headlines: {news.get('bullish_count', 0)}")
        print(f"   Bearish Headlines: {news.get('bearish_count', 0)}")
        print(f"\n   Latest Headlines:")
        for item in news.get("headlines", [])[:5]:
            print(f"      • {item.get('title', '')[:60]}...")
            print(f"        ({item.get('source', '')} | {item.get('age_hours', 0)}h ago)")
    else:
        print(f"   ⚠️ {news.get('error', 'News unavailable')}")
    
    # 4. SMC
    print("\n" + "-"*70)
    print("🧠 SMART MONEY CONCEPTS")
    print("-"*70)
    smc = data.get("smc", {})
    if "error" not in smc:
        print(f"   H1 Structure: {smc.get('h1_structure', 'N/A')}")
        print(f"   M5 Structure: {smc.get('m5_structure', 'N/A')}")
    else:
        print(f"   ⚠️ {smc.get('error', 'SMC unavailable')}")
    
    # 5. TRADINGVIEW
    print("\n" + "-"*70)
    print("📈 TRADINGVIEW TECHNICALS")
    print("-"*70)
    tv = data.get("tradingview", {})
    if "error" not in tv:
        print(f"   Overall: {tv.get('overall', 'N/A')}")
        counts = tv.get('counts', {})
        print(f"   Buy: {counts.get('Buy', 0) + counts.get('Strong Buy', 0)} | "
              f"Neutral: {counts.get('Neutral', 0)} | "
              f"Sell: {counts.get('Sell', 0) + counts.get('Strong Sell', 0)}")
    else:
        print(f"   ⚠️ {tv.get('error', 'TV unavailable')}")
    
    # FINAL VERDICT
    print("\n" + "="*70)
    print("🎯 FINAL VERDICT")
    print("="*70)
    
    signals = []
    if "error" not in tv:
        signals.append(tv.get("overall", "NEUTRAL"))
    if "error" not in smc:
        if smc.get("h1_structure") == "BULLISH": signals.append("BULLISH_SMC")
        elif smc.get("h1_structure") == "BEARISH": signals.append("BEARISH_SMC")
    if "error" not in news:
        signals.append(news.get("sentiment", "NEUTRAL"))
    
    bullish = sum(1 for s in signals if "BUY" in s or "BULLISH" in s)
    bearish = sum(1 for s in signals if "SELL" in s or "BEARISH" in s)
    neutral = sum(1 for s in signals if "NEUTRAL" in s)
    
    print(f"   Technical (TV): {tv.get('overall', 'N/A')}")
    print(f"   Structure (SMC): {smc.get('h1_structure', 'N/A')}")
    print(f"   News Sentiment: {news.get('sentiment', 'N/A')}")
    print(f"\n   Consensus: {bullish} Bullish | {bearish} Bearish | {neutral} Neutral")
    
    if bearish > bullish:
        verdict = "🔴 BEARISH — Multiple sources align for downside"
    elif bullish > bearish:
        verdict = "🟢 BULLISH — Multiple sources align for upside"
    else:
        verdict = "🟡 NEUTRAL — Mixed signals, wait for confirmation"
    
    print(f"\n   {verdict}")
    print("="*70 + "\n")


# ============================================
# MAIN
# ============================================
async def main():
    parser = argparse.ArgumentParser(description="Gold Master Analysis - Multi-Timeframe")
    parser.add_argument("--json", action="store_true", help="Output JSON")
    args = parser.parse_args()
    
    print("🚀 Generating Gold Master Analysis (Multi-Timeframe)...")
    print("   (This may take 30-60 seconds)\n")
    
    result = {}
    
    # 1. Multi-timeframe data
    print("   [1/5] Fetching multi-timeframe data from Deriv...", file=sys.stderr)
    result["multi_timeframe"] = await get_multi_timeframe_data("frxXAUUSD")
    
    # 2. Fundamental
    print("   [2/5] Fetching fundamental data...", file=sys.stderr)
    result["fundamental"] = get_fundamental_data()
    
    # 3. News
    print("   [3/5] Fetching news sentiment...", file=sys.stderr)
    result["news"] = get_news_sentiment()
    
    # 4. SMC
    print("   [4/5] Analyzing SMC patterns...", file=sys.stderr)
    result["smc"] = get_smc_analysis()
    
    # 5. TradingView
    print("   [5/5] Scraping TradingView...", file=sys.stderr)
    result["tradingview"] = await get_tradingview_data()
    
    if args.json:
        print(json.dumps(result, indent=2, default=str))
    else:
        print_master_report(result)


if __name__ == "__main__":
    asyncio.run(main())
