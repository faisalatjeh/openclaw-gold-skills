#!/usr/bin/env python3
"""
TradingView Technical Analysis Scraper
Uses Playwright to render TradingView technicals page and extract indicator data
Supports: XAUUSD, BTCUSDT, EURUSD, and any TV-supported symbol
"""

import asyncio
import json
import sys
import argparse
from playwright.async_api import async_playwright


async def scrape_tv_technicals(symbol="XAUUSD", interval="1h"):
    """
    Scrape TradingView technical analysis for any symbol
    
    Args:
        symbol: TradingView symbol (e.g., XAUUSD, BTCUSDT, EURUSD)
        interval: Timeframe (1m, 5m, 15m, 30m, 1h, 2h, 4h, 1d, 1w, 1M)
    
    Returns:
        dict: Structured technical analysis data
    """
    url = f"https://www.tradingview.com/symbols/{symbol}/technicals/"
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            viewport={"width": 1920, "height": 1080}
        )
        page = await context.new_page()
        
        try:
            response = await page.goto(url, wait_until="domcontentloaded", timeout=30000)
            await asyncio.sleep(5)  # Wait for JS to load
            
            page_text = await page.evaluate("() => document.body.innerText")
            
            import re
            from collections import Counter
            
            # Extract price
            price_match = re.search(r'([0-9]{3,5}\.[0-9]{2,3})', page_text)
            price = price_match.group(1) if price_match else None
            
            # Extract recommendation counts
            all_recs = re.findall(r'(Strong Buy|Buy|Neutral|Sell|Strong Sell)', page_text)
            rec_counts = Counter(all_recs)
            
            # Determine overall signal
            total_signals = sum(rec_counts.values())
            if total_signals > 0:
                if rec_counts['Sell'] + rec_counts['Strong Sell'] > rec_counts['Buy'] + rec_counts['Strong Buy']:
                    overall = "SELL"
                elif rec_counts['Buy'] + rec_counts['Strong Buy'] > rec_counts['Sell'] + rec_counts['Strong Sell']:
                    overall = "BUY"
                else:
                    overall = "NEUTRAL"
            else:
                overall = "UNKNOWN"
            
            # Extract oscillator details
            oscillators = {}
            osc_section = re.search(r'Oscillators.*?Name\tValue\tAction(.*?)(?=Moving Averages)', page_text, re.DOTALL)
            if osc_section:
                osc_text = osc_section.group(1)
                # Parse each oscillator line
                for line in osc_text.strip().split('\n'):
                    parts = line.split('\t')
                    if len(parts) >= 3:
                        name = parts[0].strip()
                        value = parts[1].strip()
                        action = parts[2].strip()
                        if name and value and action:
                            oscillators[name] = {"value": value, "action": action}
            
            # Extract MA details - more robust parsing
            moving_averages = {}
            # Find the MA section by looking for the header pattern
            ma_start = page_text.find('Moving Averages')            
            if ma_start != -1:
                ma_text = page_text[ma_start:ma_start+3000]
                # Parse lines that look like: Name\tValue\tAction
                for line in ma_text.split('\n'):
                    parts = line.split('\t')
                    if len(parts) >= 3:
                        name = parts[0].strip()
                        value = parts[1].strip()
                        action = parts[2].strip()
                        # Filter valid MA names and actions
                        valid_actions = ['Buy', 'Sell', 'Neutral', 'Strong Buy', 'Strong Sell']
                        if name and value and action in valid_actions:
                            # Skip if this looks like a pivot or oscillator
                            if any(x in name for x in ['Moving Average', 'Ichimoku', 'Weighted', 'Hull']):
                                moving_averages[name] = {"value": value, "action": action}
            
            # Extract pivot levels
            pivots = {}
            pivot_match = re.search(r'Pivot\tClassic\tFibonacci.*?\n(.*?)(?=\n\n|\Z)', page_text, re.DOTALL)
            if pivot_match:
                pivot_text = pivot_match.group(1)
                for line in pivot_text.split('\n'):
                    parts = line.split('\t')
                    if len(parts) >= 2 and parts[0] in ['R3', 'R2', 'R1', 'P', 'S1', 'S2', 'S3']:
                        pivots[parts[0]] = {
                            "classic": parts[1] if len(parts) > 1 else "",
                            "fibonacci": parts[2] if len(parts) > 2 else ""
                        }
            
            await browser.close()
            
            return {
                "symbol": symbol,
                "interval": interval,
                "price": price,
                "timestamp": str(__import__('datetime').datetime.now()),
                "summary": {
                    "overall": overall,
                    "counts": dict(rec_counts),
                    "total_signals": total_signals
                },
                "oscillators": oscillators,
                "moving_averages": moving_averages,
                "pivots": pivots
            }
            
        except Exception as e:
            await browser.close()
            import traceback
            return {"error": str(e), "traceback": traceback.format_exc(), "symbol": symbol}


def print_formatted(data):
    """Print analysis in human-readable format"""
    if "error" in data:
        print(f"❌ Error: {data['error']}")
        return
    
    print(f"\n📊 TradingView Technical Analysis — {data['symbol']}")
    print(f"💰 Price: ${data['price']}" if data['price'] else "")
    print(f"⏰ Time: {data.get('timestamp', 'N/A')}")
    
    print(f"\n🎯 Overall Signal: {data['summary']['overall']}")
    counts = data['summary']['counts']
    print(f"   Buy: {counts.get('Buy', 0) + counts.get('Strong Buy', 0)} | "
          f"Neutral: {counts.get('Neutral', 0)} | "
          f"Sell: {counts.get('Sell', 0) + counts.get('Strong Sell', 0)}")
    
    print(f"\n📈 Oscillators ({len(data['oscillators'])} indicators):")
    for name, info in list(data['oscillators'].items())[:10]:
        emoji = "🟢" if info['action'] == 'Buy' else "🔴" if info['action'] == 'Sell' else "🟡"
        print(f"   {emoji} {name}: {info['value']} ({info['action']})")
    
    print(f"\n📉 Moving Averages ({len(data['moving_averages'])} indicators):")
    buy_count = sum(1 for v in data['moving_averages'].values() if v['action'] == 'Buy')
    sell_count = sum(1 for v in data['moving_averages'].values() if v['action'] == 'Sell')
    neutral_count = sum(1 for v in data['moving_averages'].values() if v['action'] == 'Neutral')
    print(f"   🟢 Buy: {buy_count} | 🟡 Neutral: {neutral_count} | 🔴 Sell: {sell_count}")
    
    if data['pivots']:
        print(f"\n🎯 Key Pivot Levels:")
        for level, values in data['pivots'].items():
            print(f"   {level}: {values.get('classic', 'N/A')} (Classic)")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="TradingView Technical Analysis Scraper")
    parser.add_argument("--symbol", default="XAUUSD", help="TradingView symbol (default: XAUUSD)")
    parser.add_argument("--interval", default="4h", help="Timeframe (default: 4h)")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    
    args = parser.parse_args()
    
    result = asyncio.run(scrape_tv_technicals(args.symbol, args.interval))
    
    if args.json:
        print(json.dumps(result, indent=2, default=str))
    else:
        print_formatted(result)
