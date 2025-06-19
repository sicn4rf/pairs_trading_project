import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import statsmodels.api as sm
from statsmodels.tsa.stattools import coint, adfuller

RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
BOLD = "\033[1m"
RESET = "\033[0m"

# ================================================
# USER PARAMETERS
# ================================================
def calc_pairs(stock1, stock2, path):
    df = pd.read_csv(f"{path}{stock1}_{stock2}.csv")


    residuals = df["Residual"].dropna().values

    # ADF Test
    pvalue = adfuller(residuals)[1]

    # Extract stock names from filename
    window = 60  # Rolling window size for z-score
    entry_threshold = 1.0  # Entry threshold for z-score
    exit_threshold = 0.0  # Exit threshold to close positions


    # print(f"Cointegration p-value: {pvalue:.4f}")
    if pvalue > 0.05:
        print("WARNING: Pair may not be cointegrated.")

    # ================================================
    # HEDGE RATIO ESTIMATION (OLS)
    # ================================================
    beta = df['Beta'].iloc[0]
    # Calculate spread
    df['spread'] = df[f'{stock2} Log Price'] - (beta * df[f'{stock1} Log Price'])

    # ================================================
    # CALCULATE ROLLING Z-SCORE
    # ================================================
    df['spread_mean'] = df['spread'].rolling(window).mean()
    df['spread_std'] = df['spread'].rolling(window).std()
    df['zscore'] = (df['spread'] - df['spread_mean']) / df['spread_std']

    # ================================================
    # TRADE SIGNAL GENERATION WITH POSITION HOLDING LOGIC
    # ================================================
    df['position'] = 0

    # Initialize position
    for i in range(window, len(df)):
        if df.loc[i, 'zscore'] > entry_threshold:
            df.loc[i, 'position'] = -1  # short spread
        elif df.loc[i, 'zscore'] < -entry_threshold:
            df.loc[i, 'position'] = 1  # long spread
        else:
            # Carry forward previous position (hold until exit threshold crossed)
            df.loc[i, 'position'] = df.loc[i-1, 'position']
            # Flat when zscore crosses exit threshold
            if abs(df.loc[i, 'zscore']) < exit_threshold:
                df.loc[i, 'position'] = 0

    # ================================================
    # RETURNS CALCULATION
    # ================================================
    df['ret_stock1'] = df[f'{stock1} Raw Price'].pct_change()
    df['ret_stock2'] = df[f'{stock2} Raw Price'].pct_change()

    # Apply hedge ratio to second stock return
    df['spread_return'] = df['position'] * (df['ret_stock2'] - beta * df['ret_stock1'])
    df['spread_return'] = df['spread_return'].fillna(0)

    # Cumulative returns
    df['cum_return'] = (1 + df['spread_return']).cumprod()

    # ================================================
    # PERFORMANCE METRICS
    # ================================================
    days = df.shape[0]
    total_return = df['cum_return'].iloc[-1] - 1
    annual_return = (1 + total_return) ** (252 / days) - 1

    print(f"Annualized return: ")
    if annual_return > 0:
        print(f"{GREEN}{annual_return * 100:.2f}%\n{RESET}")
    else:
        print(f"{RED}{annual_return * 100:.2f}%\n{RESET}")

    # ================================================
    # PLOT RESULTS
    # ================================================
    # plt.figure(figsize=(12, 6))
    # plt.plot(df['Date'], df['cum_return'], label='Strategy')
    # plt.title(f"Pairs Trading Backtest: {stock1} vs {stock2}")
    # plt.xlabel("Date")
    # plt.ylabel("Cumulative Return")
    # plt.legend()
    # plt.grid()
    # plt.show()

data_directory = "./data/processed/successes/"
print("Backtester loading...\n")

for pair in os.listdir(data_directory):
    stock_name = pair.replace(".csv", "")
    stockX_name, stockY_name = stock_name.split("_")

    print(f"{BOLD}{CYAN}{stockX_name} and {stockY_name}:{RESET}")

    calc_pairs(stockX_name, stockY_name, data_directory)

print("\nTESTING MISFITS\n")
data_directory = "./data/processed/misfits/"

for pair in os.listdir(data_directory):
    stock_name = pair.replace(".csv", "")
    stockX_name, stockY_name = stock_name.split("_")

    print(f"{BOLD}{CYAN}{stockX_name} and {stockY_name}:{RESET}")

    calc_pairs(stockX_name, stockY_name, data_directory)