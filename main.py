import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

inputs_dir = "inputs"
outputs_dir = "outputs"

df = pd.read_csv(inputs_dir + "/BTCUSDT_price_data_2024-01-24.csv")
df = df.sort_index()
prices = df['mid_price']

# Visualization
print(df.head())
print(df.describe())

fig, ax = plt.subplots()
ax.plot(df.index, df['mid_price'])
ax.set_title("BTCUSDT Price")
ax.set_xlabel("Time")
ax.set_ylabel("Price")
# plt.show()

# 1. Compute 1 minute relative returns defined as:
df['r'] = prices.diff() / prices.shift(1)

# 2. Compute a 10-period simple moving average (SMA) of the price.
df['sma10']= prices.rolling(window=10).mean()
ax.plot(df.index, df['sma10'])
# plt.show()

# 3. Define trading signals (SMA crossing)
buy_signal = (prices.shift(1) <= df['sma10'].shift(1)) & (prices > df['sma10'])
sell_signal = (prices.shift(1) >= df['sma10'].shift(1)) & (prices < df['sma10'])
df['signal'] = 0
df.loc[sell_signal, 'signal'] = -1
df.loc[buy_signal,  'signal'] = 1

# 3'. Visualization of the signals
buy_idxs  = df.index[df['signal'] == 1]
sell_idxs = df.index[df['signal'] == -1]
for t in buy_idxs:
    ax.axvline(t, color='green', alpha=0.6, linewidth=1)
for t in sell_idxs:
    ax.axvline(t, color='red', alpha=0.6, linewidth=1)
ax.legend()
plt.show()

# 4. Backtest the strategy


print("Finished")
