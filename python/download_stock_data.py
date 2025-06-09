import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

tickers = ['AAPL', 'MSFT', 'AMZN', 'GOOG', 'META', 'NVDA', 'TSLA', 'INTC', 'CSCO', 'ORCL']

end_date = datetime.today()
start_date = end_date - timedelta(days=365)