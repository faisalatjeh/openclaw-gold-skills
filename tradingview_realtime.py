#!/usr/bin/env python3
"""
Real-time XAUUSD price fetcher from TradingView using Playwright
"""
from playwright.sync_api import sync_playwright
import json
import re
from datetime import datetime

def fetch_tradingview_realtime():
    """Fetch real-time price from TradingView"""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        print("📡 Fetching TradingView XAUUSD...")
        page.goto('https://www.tradingview.com/symbols/XAUUSD/?exchange=PEPPERSTONE', wait_until='networkidle')
        page.wait_for_timeout(5000)  # Wait 5 seconds for full load
        
        # Extract price
        price = None
        selectors = [
            '[class*="price"]',
            '[class*="last"]',
            '[class*="close"]',
            '.tv-symbol-price-quote__value',
            '.tv-symbol-header__price-value',
        ]
        
        for selector in selectors:
            try:
                element = page.query_selector(selector)
                if element:
                    text = element.inner_text()
                    match = re.search(r'(\d{1,2},?\d{3}\.\d{2})', text)
                    if match:
                        price = float(match.group(1).replace(',', ''))
                        break
            except:
                continue
        
        browser.close()
        
        if price:
            data = {
                'symbol': 'XAUUSD',
                'price': price,
                'source': 'TradingView Pepperstone',
                'timestamp': datetime.now().isoformat()
            }
            
            # Save to file
            with open('current_price.json', 'w') as f:
                json.dump(data, f, indent=2)
            
            print(f"✅ Price fetched: ${price:,.2f}")
            return data
        else:
            print("❌ Failed to fetch price")
            return None

if __name__ == '__main__':
    result = fetch_tradingview_realtime()
    if result:
        print(f"\n💾 Saved to current_price.json")
        print(f"📊 Price: ${result['price']:,.2f}")
