import pandas as pd
from src.backtest.engine import backtest_long_flat, summary_stats

def test_backtest_shapes():
    # Minimal synthetic data to ensure pipeline works
    idx = pd.date_range("2024-01-01", periods=100, freq="H")
    df = pd.DataFrame({
        "close": (100 + pd.Series(range(100))*0.1).values,
        "position": [0]*50 + [1]*50
    }, index=idx)
    bt = backtest_long_flat(df, fee_bps=10.0)
    assert "equity" in bt.columns
    stats = summary_stats(bt)
    assert isinstance(stats, dict)
    assert stats["periods"] == 100
