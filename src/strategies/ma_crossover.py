"""
Classic Moving Average Crossover strategy.
Generates positions: 1 (long) or 0 (flat). For simplicity, no shorting here.
"""
from __future__ import annotations
import pandas as pd

def generate_signals_ma_crossover(df: pd.DataFrame, short: int = 20, long: int = 50) -> pd.DataFrame:
    out = df.copy()
    out[f"MA_{short}"] = out["close"].rolling(window=short, min_periods=short).mean()
    out[f"MA_{long}"] = out["close"].rolling(window=long, min_periods=long).mean()
    # Signal: 1 if short MA > long MA else 0
    out["signal"] = (out[f"MA_{short}"] > out[f"MA_{long}"]).astype(int)
    # Position is previous signal (enter on next candle)
    out["position"] = out["signal"].shift(1).fillna(0)
    return out
