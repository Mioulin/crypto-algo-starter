"""
CCXT Binance client factory (no API keys needed for public OHLCV).
"""
from __future__ import annotations
import ccxt

def get_public_client():
    # Public client for reading data (no keys required)
    client = ccxt.binance({
        "enableRateLimit": True,
        "options": {"defaultType": "spot"}
    })
    return client
