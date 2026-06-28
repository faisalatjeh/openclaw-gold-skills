#!/usr/bin/env python3
"""
Smart Money Concepts (SMC) Analyzer for XAUUSD
Extracted and adapted from XAU/USD Signal Bot (Kiran-Kumbar)
Uses yfinance data instead of TwelveData
"""

import yfinance as yf
import numpy as np
from datetime import datetime


def get_candles(symbol="GC=F", period="5d", interval="5m"):
    """Fetch candles from yfinance"""
    data = yf.download(symbol, period=period, interval=interval, progress=False)
    if len(data) == 0:
        return None
    
    candles = []
    for idx, row in data.iterrows():
        candles.append({
            "time": idx,
            "open": float(row["Open"].iloc[0]),
            "high": float(row["High"].iloc[0]),
            "low": float(row["Low"].iloc[0]),
            "close": float(row["Close"].iloc[0])
        })
    return candles


def find_swing_highs(candles, lookback=5):
    """Find swing highs (local maxima)"""
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
    """Find swing lows (local minima)"""
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
    """
    Analyze market structure using BOS/Break of Structure
    Returns: "BULLISH", "BEARISH", or "NEUTRAL"
    """
    if len(candles) < lookback + 10:
        return "NEUTRAL", 0

    recent_candles = candles[-lookback:]
    swing_highs = find_swing_highs(recent_candles, lookback=3)
    swing_lows = find_swing_lows(recent_candles, lookback=3)

    if len(swing_highs) < 2 or len(swing_lows) < 2:
        return "NEUTRAL", 0

    # Compare last two swing highs and lows
    sh1, sh2 = swing_highs[-2][1], swing_highs[-1][1]
    sl1, sl2 = swing_lows[-2][1], swing_lows[-1][1]

    bullish_score = 0
    bearish_score = 0

    # Higher highs = bullish
    if sh2 > sh1:
        bullish_score += 1
    else:
        bearish_score += 1

    # Higher lows = bullish
    if sl2 > sl1:
        bullish_score += 1
    else:
        bearish_score += 1

    # Recent price direction
    recent_closes = [c["close"] for c in candles[-5:]]
    if recent_closes[-1] > recent_closes[0]:
        bullish_score += 1
    else:
        bearish_score += 1

    # EMA comparison (fast vs slow)
    closes = [c["close"] for c in candles]
    ema_fast = sum(closes[-10:]) / 10
    ema_slow = sum(closes[-30:]) / 30
    if ema_fast > ema_slow:
        bullish_score += 1
    else:
        bearish_score += 1

    if bullish_score >= 3:
        return "BULLISH", bullish_score
    elif bearish_score >= 3:
        return "BEARISH", bearish_score
    else:
        return "NEUTRAL", 0


def detect_liquidity_grab(candles):
    """
    Detect liquidity grabs (wick rejections beyond extremes)
    Returns: grab_type, score
    """
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

    # Bearish liquidity grab: wick above highs, close down
    if prev["high"] > max_high:
        wick_size = prev["high"] - max(prev["open"], prev["close"])
        body_size = abs(prev["open"] - prev["close"])
        if wick_size > body_size * 1.5:
            if curr["close"] < curr["open"]:
                return "BEARISH_GRAB", 2

    # Bullish liquidity grab: wick below lows, close up
    if prev["low"] < min_low:
        wick_size = min(prev["open"], prev["close"]) - prev["low"]
        body_size = abs(prev["open"] - prev["close"])
        if wick_size > body_size * 1.5:
            if curr["close"] > curr["open"]:
                return "BULLISH_GRAB", 2

    return None, 0


def detect_fvg(candles):
    """
    Detect Fair Value Gaps (imbalance zones)
    Returns: fvg_type, score
    """
    if len(candles) < 3:
        return None, 0

    c1 = candles[-3]
    c3 = candles[-1]

    # Bullish FVG: c1 high < c3 low (gap up)
    if c1["high"] < c3["low"]:
        return "BULLISH_FVG", 1

    # Bearish FVG: c1 low > c3 high (gap down)
    if c1["low"] > c3["high"]:
        return "BEARISH_FVG", 1

    return None, 0


def get_sr_levels(candles_1h, candles_5m, near_threshold=8.0):
    """
    Calculate support and resistance levels
    Returns: support, resistance, near_support, near_resistance
    """
    if not candles_1h or not candles_5m:
        return None, None, False, False

    # Get recent highs/lows from 1h candles
    h1_highs = sorted([c["high"] for c in candles_1h[-30:]], reverse=True)
    h1_lows = sorted([c["low"] for c in candles_1h[-30:]])

    resistance = h1_highs[2] if len(h1_highs) > 2 else h1_highs[0]
    support = h1_lows[2] if len(h1_lows) > 2 else h1_lows[0]

    current = candles_5m[-1]["close"]

    dist_resistance = abs(resistance - current)
    dist_support = abs(current - support)

    near_resistance = dist_resistance < near_threshold
    near_support = dist_support < near_threshold

    return support, resistance, near_support, near_resistance


def check_candle_pattern(candles):
    """
    Detect candlestick patterns
    Returns: pattern_name, score
    """
    if len(candles) < 3:
        return None, 0

    c2 = candles[-2]  # Previous candle
    c3 = candles[-1]  # Current candle

    score = 0
    pattern = None

    # Bearish Engulfing
    if (c2["open"] < c2["close"] and
        c3["open"] > c3["close"] and
        c3["open"] >= c2["close"] and
        c3["close"] <= c2["open"]):
        pattern = "BEARISH_ENGULF"
        score = 2

    # Bullish Engulfing
    elif (c2["open"] > c2["close"] and
          c3["open"] < c3["close"] and
          c3["open"] <= c2["close"] and
          c3["close"] >= c2["open"]):
        pattern = "BULLISH_ENGULF"
        score = 2

    # Shooting Star (bearish reversal)
    elif (c3["high"] - max(c3["open"], c3["close"])) > (2 * abs(c3["open"] - c3["close"])):
        pattern = "SHOOTING_STAR"
        score = 1

    # Hammer (bullish reversal)
    elif (min(c3["open"], c3["close"]) - c3["low"]) > (2 * abs(c3["open"] - c3["close"])):
        pattern = "HAMMER"
        score = 1

    return pattern, score


def calculate_rsi(candles, period=14):
    """Calculate RSI (Relative Strength Index)"""
    if len(candles) < period + 1:
        return 50

    closes = [c["close"] for c in candles[-(period+1):]]
    gains = []
    losses = []

    for i in range(1, len(closes)):
        diff = closes[i] - closes[i-1]
        if diff > 0:
            gains.append(diff)
            losses.append(0)
        else:
            gains.append(0)
            losses.append(abs(diff))

    avg_gain = sum(gains) / period
    avg_loss = sum(losses) / period

    if avg_loss == 0:
        return 100

    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return round(rsi, 2)


def generate_smc_signal(candles_5m, candles_1h, min_confidence=80):
    """
    Generate SMC signal based on multiple confluences
    Returns: signal dict or None
    """
    if not candles_5m or not candles_1h:
        return None

    current_price = candles_5m[-1]["close"]

    # Analyze structure
    h1_structure, h1_score = analyze_structure(candles_1h)
    m5_structure, m5_score = analyze_structure(candles_5m)

    # Detect patterns
    liquidity, liq_score = detect_liquidity_grab(candles_5m)
    pattern, pat_score = check_candle_pattern(candles_5m)
    fvg, fvg_score = detect_fvg(candles_5m)
    support, resistance, near_support, near_resistance = get_sr_levels(candles_1h, candles_5m)
    rsi = calculate_rsi(candles_5m)

    # Calculate long score
    long_score = 0
    long_reasons = []

    if h1_structure == "BULLISH":
        long_score += 30
        long_reasons.append("H1 Bullish Structure")
    if m5_structure == "BULLISH":
        long_score += 15
        long_reasons.append("M5 Bullish Structure")
    if liquidity == "BULLISH_GRAB":
        long_score += 20
        long_reasons.append("Bullish Liquidity Grab")
    if pattern in ["BULLISH_ENGULF", "HAMMER"]:
        long_score += pat_score * 8
        long_reasons.append(f"Pattern: {pattern}")
    if fvg == "BULLISH_FVG":
        long_score += 10
        long_reasons.append("Bullish FVG")
    if near_support:
        long_score += 10
        long_reasons.append("Near Support Level")
    if rsi < 40:
        long_score += 10
        long_reasons.append(f"RSI Oversold ({rsi})")

    # Calculate short score
    short_score = 0
    short_reasons = []

    if h1_structure == "BEARISH":
        short_score += 30
        short_reasons.append("H1 Bearish Structure")
    if m5_structure == "BEARISH":
        short_score += 15
        short_reasons.append("M5 Bearish Structure")
    if liquidity == "BEARISH_GRAB":
        short_score += 20
        short_reasons.append("Bearish Liquidity Grab")
    if pattern in ["BEARISH_ENGULF", "SHOOTING_STAR"]:
        short_score += pat_score * 8
        short_reasons.append(f"Pattern: {pattern}")
    if fvg == "BEARISH_FVG":
        short_score += 10
        short_reasons.append("Bearish FVG")
    if near_resistance:
        short_score += 10
        short_reasons.append("Near Resistance Level")
    if rsi > 60:
        short_score += 10
        short_reasons.append(f"RSI Overbought ({rsi})")

    # Determine signal
    signal = None
    score = 0
    reasons = []

    if long_score > short_score and long_score >= min_confidence:
        signal = "LONG"
        score = min(long_score, 99)
        reasons = long_reasons
    elif short_score > long_score and short_score >= min_confidence:
        signal = "SHORT"
        score = min(short_score, 99)
        reasons = short_reasons

    if not signal:
        return None

    # Calculate SL/TP
    if signal == "LONG":
        sl_dollars = current_price - support if support else current_price * 0.01
        tp_dollars = sl_dollars * 2
    else:
        sl_dollars = resistance - current_price if resistance else current_price * 0.01
        tp_dollars = sl_dollars * 2

    return {
        "signal": signal,
        "price": current_price,
        "sl_dollars": round(sl_dollars, 2),
        "tp_dollars": round(tp_dollars, 2),
        "confidence": score,
        "reasons": reasons,
        "rsi": rsi,
        "support": support,
        "resistance": resistance,
        "h1_bias": h1_structure,
        "pattern": pattern or "None",
        "liquidity": liquidity or "None",
        "fvg": fvg or "None",
        "m5_structure": m5_structure
    }


def main():
    """Main function to test SMC analysis"""
    print("🚀 SMC Analyzer Starting...")
    print("Fetching data...")

    # Fetch data
    candles_5m = get_candles("GC=F", period="5d", interval="5m")
    candles_1h = get_candles("GC=F", period="30d", interval="1h")

    if not candles_5m or not candles_1h:
        print("❌ Failed to fetch data")
        return

    print(f"✅ Data fetched: {len(candles_5m)} 5m candles, {len(candles_1h)} 1h candles")

    # Generate signal
    signal = generate_smc_signal(candles_5m, candles_1h)

    # Print analysis details regardless of signal
    print(f"\n📊 ANALYSIS:")
    print(f"💰 Price: ${candles_5m[-1]['close']:.2f}")
    
    h1_structure, h1_score = analyze_structure(candles_1h)
    m5_structure, m5_score = analyze_structure(candles_5m)
    liquidity, liq_score = detect_liquidity_grab(candles_5m)
    pattern, pat_score = check_candle_pattern(candles_5m)
    fvg, fvg_score = detect_fvg(candles_5m)
    support, resistance, near_support, near_resistance = get_sr_levels(candles_1h, candles_5m)
    rsi = calculate_rsi(candles_5m)
    
    print(f"📈 H1 Structure: {h1_structure} (score: {h1_score})")
    print(f"📉 M5 Structure: {m5_structure} (score: {m5_score})")
    print(f"💧 Liquidity: {liquidity}")
    print(f"🕯 Pattern: {pattern}")
    print(f"⚖️ FVG: {fvg}")
    print(f"📊 RSI: {rsi}")
    print(f"🟢 Support: ${support:.2f}" if support else "")
    print(f"🔴 Resistance: ${resistance:.2f}" if resistance else "")
    print(f"📍 Near Support: {near_support} | Near Resistance: {near_resistance}")
    
    if signal:
        print(f"\n🎯 SIGNAL: {signal['signal']}")
        print(f"🎯 Confidence: {signal['confidence']}%")
        print(f"🛑 SL: ${signal['sl_dollars']:.2f}")
        print(f"🎯 TP: ${signal['tp_dollars']:.2f}")
        print(f"\n📋 Reasons:")
        for reason in signal['reasons']:
            print(f"   ✅ {reason}")
    else:
        print(f"\n❌ No signal (need 80+ confidence)")


if __name__ == "__main__":
    main()
