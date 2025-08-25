"""
A tiny vectorized backtest engine for long/flat strategies on spot.
- Buys when position goes from 0 -> 1
- Sells when position goes from 1 -> 0
- Applies fee per trade in basis points (bps)
- No leverage, no shorting
"""
from __future__ import annotations
import pandas as pd
import numpy as np
from ..config import bps_to_decimal

def backtest_long_flat(df: pd.DataFrame, fee_bps: float = 10.0) -> pd.DataFrame:
    out = df.copy()
    out["returns"] = out["close"].pct_change().fillna(0.0)

    # Ensure valid position in {0,1}
    pos = out["position"].fillna(0).clip(lower=0, upper=1)

    # Entries and exits
    entry = (pos > pos.shift(1).fillna(0)).astype(int)
    exit_ = (pos < pos.shift(1).fillna(0)).astype(int)

    fee = bps_to_decimal(fee_bps)
    trade_cost = (entry + exit_) * fee

    out["strategy_ret"] = pos * out["returns"] - trade_cost
    out["equity"] = (1.0 + out["strategy_ret"]).cumprod()

    # Buy & hold benchmark
    out["bench_equity"] = (1.0 + out["returns"]).cumprod()

    return out

def _annualization_factor(index: pd.DatetimeIndex) -> int:
    # Heuristic: if frequency contains 'H' use 24*365, if 'T' (minutes) use 60*24*365, else daily 365
    try:
        freq = pd.infer_freq(index)
    except Exception:
        freq = None
    if freq is None:
        return 365
    f = freq.upper()
    if "H" in f:
        return 24*365
    if "T" in f or "MIN" in f:
        return 60*24*365
    if "S" in f:
        return 60*60*24*365
    return 365

def summary_stats(bt: pd.DataFrame) -> dict:
    if bt.empty:
        return {"error": "Empty backtest dataframe"}

    ann = _annualization_factor(bt.index)
    strat = bt["strategy_ret"].fillna(0.0).to_numpy()
    bench = bt["returns"].fillna(0.0).to_numpy()

    def _ann_stats(ret):
        mu = np.mean(ret)
        sig = np.std(ret, ddof=1) if len(ret) > 1 else 0.0
        cum = np.prod(1.0 + ret) - 1.0
        sharpe = (mu * ann) / (sig * (ann**0.5)) if sig > 0 else float("nan")
        return mu, sig, cum, sharpe

    mu_s, sig_s, cum_s, sharpe_s = _ann_stats(strat)
    mu_b, sig_b, cum_b, sharpe_b = _ann_stats(bench)

    # Max drawdown
    eq = bt["equity"].to_numpy()
    peak = np.maximum.accumulate(eq)
    dd = (eq - peak) / peak
    max_dd = dd.min() if len(dd) else 0.0

    return {
        "periods": int(len(bt)),
        "ann_factor": int(ann),
        "equity_final": float(bt["equity"].iloc[-1]),
        "bench_equity_final": float(bt["bench_equity"].iloc[-1]),
        "cum_return": float(cum_s),
        "bench_cum_return": float(cum_b),
        "ann_mean_ret": float(mu_s * ann),
        "ann_vol": float(sig_s * (ann**0.5)),
        "sharpe": float(sharpe_s),
        "max_drawdown": float(max_dd),
        "trades": int((bt["position"].shift(1).fillna(0) != bt["position"]).sum())
    }
