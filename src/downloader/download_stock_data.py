import yfinance as yf
import pandas as pd
import os, shutil, sys
from datetime import datetime, timedelta

# Add root directory to current path.
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))


from config.ticker_macros import SECTORS


# Display available sectors
print("Available sectors:")
for key in SECTORS:
    print(f" - {key}")


# Ask user which sector to run. use strip to remove any leading or trailing space
# use upper to make it not case sensitive
choice = input("Enter the sector you want to run: ").strip().upper()

# Validate and get tickers
if choice not in SECTORS:
    print("Invalid sector name. Exiting.")
    exit(1)

tickers = SECTORS[choice]

with open("../../data/results/sector_choice.txt", "w") as outFile:
    outFile.write(choice + "\n")


# Creating two datetime objects using the datetime library. End date being current date
# and start date being 365 days ago. we do this using .today() and timedelta() functions
end_date = datetime.today()
start_date = end_date - timedelta(365)

folder = '../../data/raw'

if os.path.exists(folder):
    shutil.rmtree(folder)
    os.makedirs(folder)
else:
    os.makedirs(folder)

print("Gathering data from yfinance...")

# Iterate through every ticker in our tickers list
for tick in tickers:
    # Create a ticker object for our current company
    # .Ticker() takes in a string as an argument and returns a ticker object for that particular company
    current_tick = yf.Ticker(tick)

    # Store the stocks historical data into a pandas data frame.
    # We do this by using the current ticker object to call .history() which returns the OHLCV data
    # of that particular stock from a start to end date, which we store in a data frame using pandas.
    data_frame = current_tick.history(start=start_date.strftime('%Y-%m-%d'), end=end_date.strftime('%Y-%m-%d'),interval='1d',auto_adjust=True)

    # Make it so that our data frame for date only includes the date and not the time
    data_frame.index = data_frame.index.date

    data_frame.drop(columns=["Volume", "Dividends", "Stock Splits"], inplace=True)
    
    # Use pandas to store the historical data from the data frame into a .csv file, index_label="Date" means that the index of the data frame will be used as the first column in the csv file
    data_frame.to_csv(f"../../data/raw/{tick}.csv", index_label="Date")

print("Done collecting data.")


