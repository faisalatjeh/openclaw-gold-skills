#!/usr/bin/env python3
"""
Auto-fetch XAUUSD price from TradingView - Cron version
"""
from playwright.sync_api import sync_playwright
import json
import re
from datetime import datetime
import sys

def fetch_price():
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            
            page.goto('https://www.tradingview.com/symbols/XAUUSD/?exchange=PEPPERSTONE', wait_until='networkidle')
            page.wait_for_timeout(5000)
            
            price = None
            selectors = [
                '[class*="price"]',
                '[class*="last"]',
                '[class*="close"]',
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
                    'source': 'TradingView',
                    'timestamp': datetime.now().isoformat()
                }
                
                with open('/Users/faisalk/.openclaw/workspace/current_price.json', 'w') as f:
                    json.dump(data, f, indent=2)
                
                print(f"✅ {datetime.now().strftime('%H:%M:%S')} | XAUUSD: ${price:,.2f}")
                return True
            else:
                print(f"❌ {datetime.now().strftime('%H:%M:%S')} | Failed to fetch price")
                return False
                
    except Exception as e:
        print(f"❌ {datetime.now().strftime('%H:%M:%S')} | Error: {e}")
        return False

if __name__ == '__main__':
    fetch_price()
