import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

is_visualize = True
is_pos_lag = True # add lag between signal and buy/sell operation (since we can't trade at signal time)

inputs_dir = "inputs"
outputs_dir = "outputs"

df = pd.read_csv(inputs_dir + "/BTCUSDT_price_data_2024-01-24.csv")
ts = pd.to_numeric(
    df['timestamp'].astype(str).str.extract(r'(\d+)').iloc[:, 0],
    errors='coerce'
)
df['date'] = pd.to_datetime(ts, unit='ms', utc=True)
df['date'] = df['date'].dt.strftime('%Y-%m-%d %H:%M')
df = df.sort_values('date')
prices = df['mid_price']

# 1. Compute 1 minute relative returns defined as:
df['r'] = prices.diff() / prices.shift(1)

# 2. Compute a 10-period simple moving average (SMA) of the price.
df['sma10']= prices.rolling(window=10).mean()

# 3. Define trading signals (SMA crossing)
buy_signal = (prices.shift(1) <= df['sma10'].shift(1)) & (prices > df['sma10'])
sell_signal = (prices.shift(1) >= df['sma10'].shift(1)) & (prices < df['sma10'])
df['signal'] = 0
df.loc[sell_signal, 'signal'] = -1
df.loc[buy_signal,  'signal'] = 1

# 4. Backtest the strategy
start_capital = 100_000
fee = 0.0002  # 0.02% per trade

df['pos'] = pd.Series(df['signal']).replace(0, np.nan).ffill().fillna(0)
if is_pos_lag:
    df['pos'] = df['pos'].shift(1).fillna(0) 
# print(df.head(30))

# Calculate returns (cumulatively, could be done selectively on pos switches for potentially faster calculations)
df['returns'] = df['pos'] * df['r']
df['equity'] = start_capital * (1 + df['returns']).cumprod()
# print(df.tail(30))

# 5.Track and output these performance metrics:
# o	Total return (%)
# o	Number of trades
# o	Maximum drawdown
# o	Sharpe ratio (Optional)

end_capital = df['equity'].iloc[-1]
total_return = end_capital / start_capital - 1
df['trade'] = df['pos'].diff().fillna(0) != 0
df['trade'] = df['trade'].astype(int)
n_trades = df['trade'].sum() 
print(df.head(35))

# Max drawdown: peak-to-trough
rollmax = df['equity'].cummax()
drawdown = df['equity']/rollmax - 1
max_dd = drawdown.min()

# Sharpe ratio: for such short period (~1440 minutes), r_f is basically zero, thus
sharpe = df['returns'].mean() / df['returns'].std()
# Could be annualized for fair evaluation. Assuming BTCUSDT trades 24/7 in a trading year
sharpe_ann = sharpe * np.sqrt(60*24*365)

print(f"Total return: {total_return*100:.2f}%, from ${start_capital:,.2f} to ${end_capital:,.2f}")
print(f"Number of trades: {n_trades}")
print(f"Max drawdown: {max_dd*100:.2f}%")
print(f"Sharpe ratio: {sharpe:.2f} (annualized: {sharpe_ann:.2f} - unrealistic since tiny sample and no fees)")


if is_visualize:
    # Price and SMA
    fig, ax = plt.subplots()
    ax.plot(df.index, df['mid_price'])
    ax.plot(df.index, df['sma10'])
    ax.set_title("BTCUSDT Price")
    ax.set_xlabel("Time")
    ax.set_ylabel("Price")
    ax.legend(['Price', 'SMA10'])

    # Buy/sell signals
    buy_idxs  = df.index[df['signal'] == 1]
    sell_idxs = df.index[df['signal'] == -1]
    for t in buy_idxs:
        ax.axvline(t, color='green', alpha=0.6, linewidth=1)
    for t in sell_idxs:
        ax.axvline(t, color='red', alpha=0.6, linewidth=1)
    # ax.legend(['Buy', 'Sell'])

    # 6. PnL curve
    fig, ax = plt.subplots()
    ax.plot(df.index, df['equity'], label='Equity')
    ax.axhline(start_capital, linestyle='--', linewidth=1, alpha=0.6, label='Start')
    ax.set_ylabel('Equity (USD)')
    ax.set_title('Cumulative PnL (Equity)') 
    ax.legend()
    plt.show()


print("--------- Finished ---------")
