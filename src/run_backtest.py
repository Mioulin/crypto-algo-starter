"""
CLI entrypoint to run a MA crossover backtest on Binance spot OHLCV.
"""
from __future__ import annotations
import argparse
import pandas as pd
from data.fetch import fetch_ohlcv_df
from strategies.ma_crossover import generate_signals_ma_crossover
from backtest.engine import backtest_long_flat, summary_stats

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--symbol", type=str, default="BTC/USDT")
    parser.add_argument("--timeframe", type=str, default="1h")
    parser.add_argument("--limit", type=int, default=2000)
    parser.add_argument("--short", type=int, default=20)
    parser.add_argument("--long", type=int, default=50)
    parser.add_argument("--fee_bps", type=float, default=10.0)
    parser.add_argument("--csv", type=str, default="")  # optional path to save results
    args = parser.parse_args()

    df = fetch_ohlcv_df(args.symbol, args.timeframe, args.limit)
    df = generate_signals_ma_crossover(df, short=args.short, long=args.long)
    bt = backtest_long_flat(df, fee_bps=args.fee_bps)

    stats = summary_stats(bt)
    print("=== SUMMARY ===")
    for k, v in stats.items():
        print(f"{k:18s}: {v}")

    if args.csv:
        bt.to_csv(args.csv)
        print(f"Saved backtest dataframe to: {args.csv}")

if __name__ == "__main__":
    main()
