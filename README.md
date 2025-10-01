# 🚀 Simple Binance EMA Trading Bot

![Python](https://img.shields.io/badge/Python-3.x-blue?logo=python)
![CCXT](https://img.shields.io/badge/CCXT-Binance-yellow)
![License](https://img.shields.io/badge/License-MIT-green)

🔗 Visit [Psyll.com](https://psyll.com/en) for best trading bots on the market

Automated cryptocurrency trading can save time ⏱️, reduce emotional mistakes 😅, and execute trades faster than human reaction allows.
This Python bot implements a **simple EMA crossover strategy** for Binance – perfect for beginners in algorithmic trading.


---

## ✨ Features

- 🔒 Secure connection to Binance via API keys
- 📊 Real-time candlestick (OHLCV) data
- 📈 Calculates short-term and long-term EMAs
- 🔴 Detects buy signals & sell signals automatically
- ⚡ Executes market orders instantly
- 🔄 Continuous loop with error handling for uninterrupted trading

---

## 📖 How It Works

### EMA Crossover Strategy

The **Exponential Moving Average (EMA)** gives more weight to recent prices, reacting faster than the Simple Moving Average (SMA).

- **Short EMA:** reacts quickly to price changes
- **Long EMA:** smooths long-term trends

**Trading signals:**
- **Buy:** Short EMA crosses above Long EMA
- **Sell:** Short EMA crosses below Long EMA

---

## 🛠 Prerequisites
- Binance API keys with trading & balance permissions only (do not enable withdrawal)
- Python 3.x
- Libraries:

```bash
pip install ccxt pandas
```




## ⚙️ Configuration

Edit the settings in the script:

```python
# ---------------- SETTINGS ----------------
API_KEY = "YOUR_API_KEY"
API_SECRET = "YOUR_SECRET_KEY"
SYMBOL = "BTC/USDC"
TIMEFRAME = "1m"
EMA_SHORT_PERIOD = 12
EMA_LONG_PERIOD = 26
TRADE_AMOUNT = 0.1
SLEEP_INTERVAL = 5
# ------------------------------------------
```

## Parameter guide:
| Parameter         | Description                                      |
|------------------|-------------------------------------------------|
| SYMBOL            | Trading pair (e.g., BTC/USDC)                  |
| TIMEFRAME         | Candle interval (1m, 5m, etc.)                 |
| EMA_SHORT_PERIOD  | Short EMA period (sensitivity)                 |
| EMA_LONG_PERIOD   | Long EMA period (trend smoothing)              |
| TRADE_AMOUNT      | Amount per trade (start small)                 |
| SLEEP_INTERVAL    | Delay between iterations to respect API limits |

## 🚀 Getting Started

### Connect to Binance:
```python
import ccxt

exchange = ccxt.binance({
    "apiKey": API_KEY,
    "secret": API_SECRET,
    "enableRateLimit": True,
    "options": {"defaultType": "spot"},
})

balance = exchange.fetch_balance()
print("Connected! USDC balance:", balance["USDC"]["free"])
```

### Fetch candlestick data:
```python
import pandas as pd

def fetch_ohlcv(symbol=SYMBOL, timeframe=TIMEFRAME, limit=100):
    ohlcv = exchange.fetch_ohlcv(symbol, timeframe, limit=limit)
    df = pd.DataFrame(ohlcv, columns=["timestamp", "open", "high", "low", "close", "volume"])
    df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
    return df
```

### Calculate EMAs:
```python
def calculate_emas(df, short_period=EMA_SHORT_PERIOD, long_period=EMA_LONG_PERIOD):
    df["ema_short"] = df["close"].ewm(span=short_period, adjust=False).mean()
    df["ema_long"] = df["close"].ewm(span=long_period, adjust=False).mean()
    df["ema_diff"] = df["ema_short"] - df["ema_long"]
    return df
```

### Detect trade signals:
```python
def check_for_trade(df):
    last = df.iloc[-1]
    prev = df.iloc[-2]
    if prev["ema_short"] < prev["ema_long"] and last["ema_short"] > last["ema_long"]:
        return "buy"
    elif prev["ema_short"] > prev["ema_long"] and last["ema_short"] < last["ema_long"]:
        return "sell"
    return None
```

### Execute trades in a loop:

```python
import time

position = None

while True:
    try:
        df = fetch_ohlcv(SYMBOL, TIMEFRAME)
        df = calculate_emas(df)
        action = check_for_trade(df)
        current_price = df["close"].iloc[-1]
        print(f"Price: {current_price:.2f} | EMA Short: {df['ema_short'].iloc[-1]:.2f} | EMA Long: {df['ema_long'].iloc[-1]:.2f}")

        if action == "buy" and position != "long":
            order = exchange.create_market_buy_order(SYMBOL, TRADE_AMOUNT)
            print("BUY executed:", order)
            position = "long"
        elif action == "sell" and position == "long":
            order = exchange.create_market_sell_order(SYMBOL, TRADE_AMOUNT)
            print("SELL executed:", order)
            position = None

        time.sleep(SLEEP_INTERVAL)

    except Exception as e:
        print("Error:", e)
        time.sleep(SLEEP_INTERVAL)
```
## ✅ Conclusion

This bot provides a hands-on introduction to algorithmic trading by:

- 🔑 Connecting to Binance via API
- 📊 Fetching & analyzing candlestick data
- 📈 Calculating EMAs for trend detection
- 🔴 Automating trades and managing positions

While simple, it sets the foundation for more advanced strategies: multi-pair trading, stop-loss/take-profit, logging, notifications, etc.

⚠️ Risk Warning: Trading cryptocurrency is inherently risky. This bot does not guarantee profits. Use at your own risk and start with small amounts.