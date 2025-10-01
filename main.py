import ccxt
import pandas as pd
import time

# ---------------- SETTINGS ----------------
API_KEY =    'ENTER YOU BINANCE PUBLIC API KEY'
API_SECRET = 'ENTER YOU BINANCE SECRET API KEY'

SYMBOL = "BTC/USDC"
TIMEFRAME = "1m"
EMA_SHORT_PERIOD = 2
EMA_LONG_PERIOD = 3
TRADE_AMOUNT = 0.1
SLEEP_INTERVAL = 5
# ------------------------------------------

exchange = ccxt.binance({
    "apiKey": API_KEY,
    "secret": API_SECRET,
    "enableRateLimit": True,
    "options": {"defaultType": "spot"},
})

def fetch_ohlcv(symbol=SYMBOL, timeframe=TIMEFRAME, limit=100):
    ohlcv = exchange.fetch_ohlcv(symbol, timeframe, limit=limit)
    df = pd.DataFrame(ohlcv, columns=["timestamp", "open", "high", "low", "close", "volume"])
    df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
    return df

def calculate_emas(df, short_period=EMA_SHORT_PERIOD, long_period=EMA_LONG_PERIOD):
    df["ema_short"] = df["close"].ewm(span=short_period, adjust=False).mean()
    df["ema_long"] = df["close"].ewm(span=long_period, adjust=False).mean()
    df["ema_diff"] = df["ema_short"] - df["ema_long"]
    return df

def check_for_trade(df):
    last = df.iloc[-1]
    prev = df.iloc[-2]
    if prev["ema_short"] < prev["ema_long"] and last["ema_short"] > last["ema_long"]:
        return "buy"
    elif prev["ema_short"] > prev["ema_long"] and last["ema_short"] < last["ema_long"]:
        return "sell"
    return None

balance = exchange.fetch_balance()
print("Connection successful! USDC balance:", balance["USDC"]["free"])

position = None

while True:
    try:
        df = fetch_ohlcv(SYMBOL, TIMEFRAME)
        df = calculate_emas(df, EMA_SHORT_PERIOD, EMA_LONG_PERIOD)

        current_price = df["close"].iloc[-1]
        ema_short = df["ema_short"].iloc[-1]
        ema_long = df["ema_long"].iloc[-1]
        ema_diff = df["ema_diff"].iloc[-1]

        print(f"Price: {current_price:.2f} USDC | EMA short: {ema_short:.2f} | EMA long: {ema_long:.2f} | Distance to cross: {ema_diff:.5f}")

        action = check_for_trade(df)

        if action == "buy" and position != "long":
            print(f"Placing BUY order for {TRADE_AMOUNT} BTC...")
            order = exchange.create_market_buy_order(SYMBOL, TRADE_AMOUNT)
            print("BUY order executed:", order)
            position = "long"

        elif action == "sell" and position == "long":
            print(f"Placing SELL order for {TRADE_AMOUNT} BTC...")
            order = exchange.create_market_sell_order(SYMBOL, TRADE_AMOUNT)
            print("SELL order executed:", order)
            position = None

        time.sleep(SLEEP_INTERVAL)

    except Exception as e:
        print("Error:", e)
        time.sleep(SLEEP_INTERVAL)