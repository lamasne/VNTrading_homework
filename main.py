import pandas as pd

inputs_dir = "inputs"
outputs_dir = "outputs"

df = pd.read_csv(inputs_dir + "/BTCUSDT_price_data_2024-01-24.csv")
print(df.head())
print(df.describe())

# 1. Compute 1 minute relative returns defined as:

