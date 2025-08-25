# Crypto Algo Starter 🚀

An educational starter project for **algorithmic trading in cryptocurrency markets**, built with Python.  
It provides clean and modular implementations of **data handling, trading strategies, and backtesting**.

---

## ✨ Features
- 📈 Load and preprocess crypto OHLCV data (via APIs or CSV)
- 🧮 Implement classical trading strategies (e.g., Moving Average Crossover)
- 🤖 Experiment with **machine learning approaches** such as Hidden Markov Models
- 🔄 Backtest strategies with realistic transaction cost assumptions
- 📊 Visualize performance with Sharpe ratio, drawdowns, and equity curves

---

## Project Structure 

├── README.md                   # prject description
├── requirements.txt            # dependencies Python
├── src
│   ├── backtest
│   │   └── engine.py           # ядро бэктестера: цикл по барам, сделки, pnl
│   ├── config.py               # конфиг: тикер, таймфрейм, комиссии, пути
│   ├── data
│   │   ├── binance_client.py   # клиент/обертка для данных (вероятно Binance)
│   │   └── fetch.py            # функции загрузки OHLCV и сохранения в csv/parquet
│   ├── live
│   │   └── README.md           # задел под лайв‑трейдинг
│   ├── run_backtest.py         # CLI-скрипт: собирает всё и запускает engine
│   └── strategies
│       └── ma_crossover.py     # стратегия Moving Average Crossover
└── tests
    └── test_backtest_engine.py # базовые тесты для движка


## 🚀 Getting Started
Clone the repository and install dependencies in a virtual environment:

```bash
git clone https://github.com/mioulin/crypto-algo-starter.git
cd crypto-algo-starter

python -m venv .venv
source .venv/bin/activate   # On Linux/Mac
.venv\Scripts\activate      # On Windows

pip install -r requirements.txt

📜 License
This project is licensed under the MIT License.
