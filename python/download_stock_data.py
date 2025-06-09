import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

tickers = ['AAPL', 'MSFT', 'AMZN', 'GOOG', 'META', 'NVDA', 'TSLA', 'INTC', 'CSCO', 'ORCL']

# Task 1: setup start and end date

end_date = datetime.today()
start_date = end_date - timedelta(days=365)

# Task 2: iterate through list, and use yfinance to read and pandas to store into csv.
