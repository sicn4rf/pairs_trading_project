import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

tickers = ['AAPL', 'MSFT', 'AMZN', 'GOOG', 'META', 'NVDA', 'TSLA', 'INTC', 'CSCO', 'ORCL']

# Task 1: setup start and end date

end_date = datetime.today()
start_date = end_date - timedelta(days=365)

# Task 2: iterate through list, and use yfinance to read and pandas to store into csv.

print("Gathering data from yfinance...")

for tick in tickers:
    current_tick = yf.Ticker(tick)
    data_frame = current_tick.history(start=start_date.strftime('%Y-%m-%d'),end=end_date.strftime('%Y-%m-%d'),interval='1d',auto_adjust=True)

    # Task 3: Store into /data folder not python.

    data_frame.to_csv(f"../data/{tick}.csv")

print("Done pookie <3")


