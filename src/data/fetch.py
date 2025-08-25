"""
Fetch OHLCV data as a pandas DataFrame.
"""
from __future__ import annotations
import pandas as pd
from .binance_client import get_public_client

def fetch_ohlcv_df(symbol: str, timeframe: str = "1h", limit: int = 2000) -> pd.DataFrame:
    client = get_public_client()
    ohlcv = client.fetch_ohlcv(symbol, timeframe=timeframe, limit=limit)
    df = pd.DataFrame(ohlcv, columns=["timestamp", "open", "high", "low", "close", "volume"])
    # Convert ms -> UTC datetime
    df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms", utc=True)
    df.set_index("timestamp", inplace=True)
    df = df.astype({
        "open": "float64",
        "high": "float64",
        "low": "float64",
        "close": "float64",
        "volume": "float64"
    })
    # Drop duplicate timestamps and sort
    df = df[~df.index.duplicated(keep="last")].sort_index()
    return df
