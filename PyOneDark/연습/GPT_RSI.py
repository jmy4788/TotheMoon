from binance.client import Client
import pandas as pd
import talib

# Initialize the Binance API client
client = Client("api_key", "api_secret")

# Retrieve historical candlestick data for the symbol BTCUSDT
klines = client.fetch_ohlcv("BTCUSDT", interval=Client.KLINE_INTERVAL_1HOUR)

# Convert the klines data to a pandas DataFrame
df = pd.DataFrame(klines, columns=["timestamp", "open", "high", "low", "close", "volume", "close_time", "quote_asset_volume", "trades", "taker_buy_base_asset_volume", "taker_buy_quote_asset_volume", "ignore"])

# Convert the timestamp to a datetime
df["timestamp"] = pd.to_datetime(df["timestamp"], unit='ms')

# Set the timestamp as the DataFrame index
df.set_index("timestamp", inplace=True)

# Calculate the RSI
df["rsi"] = talib.RSI(df["close"], timeperiod=14)

# print the DataFrame
print(df)

df["ma"] = talib.MA(df["close"], timeperiod=14)
df["ema"] = talib.EMA(df["close"], timeperiod=14)
