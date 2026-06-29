#!/usr/bin/env python3
"""
Deriv API Connector for XAUUSD Real-time Data
Reads token from ~/.deriv_api_token
Usage:
    python3 deriv_connector.py --token-file ~/.deriv_api_token
"""

import asyncio
import json
import sys
import argparse
import os


async def get_deriv_ticks(token, symbol="frxXAUUSD"):
    """
    Connect to Deriv WebSocket and get real-time ticks for XAUUSD
    
    Args:
        token: Deriv API token
        symbol: Market symbol (default: frxXAUUSD for Gold/USD)
    
    Returns:
        dict: Latest tick data
    """
    try:
        import websockets
    except ImportError:
        print("❌ websockets module not installed. Run: pip3 install websockets")
        return {"error": "websockets not installed"}
    
    uri = "wss://ws.binaryws.com/websockets/v3?app_id=1089"
    
    try:
        async with websockets.connect(uri) as websocket:
            # Authorize
            auth_msg = {
                "authorize": token
            }
            await websocket.send(json.dumps(auth_msg))
            auth_response = json.loads(await websocket.recv())
            
            if "error" in auth_response:
                return {"error": auth_response["error"]["message"]}
            
            # Subscribe to ticks
            tick_msg = {
                "ticks": symbol,
                "subscribe": 1
            }
            await websocket.send(json.dumps(tick_msg))
            
            # Get first tick
            tick_response = json.loads(await websocket.recv())
            
            if "error" in tick_response:
                return {"error": tick_response["error"]["message"]}
            
            tick = tick_response.get("tick", {})
            
            return {
                "symbol": tick.get("symbol", symbol),
                "price": tick.get("quote", 0),
                "epoch": tick.get("epoch", 0),
                "pip_size": tick.get("pip_size", 0),
                "source": "Deriv API",
                "status": "success"
            }
            
    except Exception as e:
        return {"error": str(e), "status": "failed"}


def get_stored_token(path="~/.deriv_api_token"):
    """Read token from file"""
    full_path = os.path.expanduser(path)
    try:
        with open(full_path, 'r') as f:
            return f.read().strip()
    except FileNotFoundError:
        return None
    except Exception as e:
        return None


def print_tick_data(data):
    """Print tick data in human-readable format"""
    if "error" in data:
        print(f"❌ Error: {data['error']}")
        return
    
    print("\n📊 Deriv Real-time Tick Data")
    print("-" * 40)
    print(f"   Symbol: {data.get('symbol', 'N/A')}")
    print(f"   Price: {data.get('price', 0)}")
    print(f"   Epoch: {data.get('epoch', 0)}")
    print(f"   Pip Size: {data.get('pip_size', 0)}")
    print(f"   Source: {data.get('source', 'N/A')}")
    print("-" * 40)


def main():
    parser = argparse.ArgumentParser(description="Deriv API Connector")
    parser.add_argument("--token-file", default="~/.deriv_api_token", help="Path to token file")
    parser.add_argument("--token", help="API token (alternative to file)")
    parser.add_argument("--symbol", default="frxXAUUSD", help="Market symbol")
    parser.add_argument("--json", action="store_true", help="Output JSON")
    
    args = parser.parse_args()
    
    # Get token
    token = args.token
    if not token:
        token = get_stored_token(args.token_file)
    
    if not token:
        print("❌ No token provided. Either:")
        print("   1. Save token to ~/.deriv_api_token")
        print("   2. Use --token YOUR_TOKEN")
        sys.exit(1)
    
    print("🚀 Connecting to Deriv API...")
    result = asyncio.run(get_deriv_ticks(token, args.symbol))
    
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print_tick_data(result)


if __name__ == "__main__":
    main()
