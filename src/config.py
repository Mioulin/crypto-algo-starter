"""
Shared config utilities.
"""
from __future__ import annotations
from dataclasses import dataclass

@dataclass
class BacktestConfig:
    symbol: str = "BTC/USDT"
    timeframe: str = "1h"
    limit: int = 2000
    short: int = 20
    long: int = 50
    fee_bps: float = 10.0  # 10 basis points = 0.10% per transaction

def bps_to_decimal(bps: float) -> float:
    return bps / 10000.0
