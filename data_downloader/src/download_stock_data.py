import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

# This creates a literal list of 10 big tech company tickers that we want to analyze
tickers = ['AAPL', 'MSFT', 'AMZN', 'GOOG', 'META', 'NVDA', 'TSLA', 'INTC', 'CSCO', 'ORCL']

# Creating two datetime objects using the datetime library. End date being current date
# and start date being 365 days ago. we do this using .today() and timedelta() functions
end_date = datetime.today()
start_date = end_date - timedelta(days=365)


print("Gathering data from yfinance...")

# Iterate through every ticker in our tickers list
for tick in tickers:
    # Create a ticker object for our current company
    # .Ticker() takes in a string as an argument and returns a ticker object for that particular company
    current_tick = yf.Ticker(tick)

    # Store the stocks historical data into a pandas data frame.
    # We do this by using the current ticker object to call .history() which returns the OHLCV data
    # of that particular stock from a start to end date, which we store in a data frame using pandas.
    data_frame = current_tick.history(start=start_date.strftime('%Y-%m-%d'),end=end_date.strftime('%Y-%m-%d'),interval='1d',auto_adjust=True)

    # Make it so that our data frame for date only includes the date and not the time
    data_frame.index = data_frame.index.date
    
    # Use pandas to store the historical data from the data frame into a .csv file
    data_frame.to_csv(f"../data/{tick}.csv")

print("Done collecting data.")


