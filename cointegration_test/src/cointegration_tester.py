# Cointegration Tester (Boilerplate)
# This file processes residual CSV files from C++ output and tests for cointegration.

# ======================
# IMPORT LIBRARIES
# ======================

# Task 1a: Import os (used for directory/file handling)
import os
import pandas as pd
from statsmodels.tsa.stattools import adfuller
import shutil


# ======================
# DEFINE INPUT DIRECTORY
# ======================

# Task 2: Set the directory path where your residual CSV files are stored.
data_directory = "../../data/processed"


# ======================
# ITERATE THROUGH FILES
# ======================

# Task 3: Loop through all files in the directory

# listdir is like saying "ls" in your terminal and then we can store all those files in a list

success_dir = os.path.join(data_directory, "successes")
failure_dir = os.path.join(data_directory, "failures")

# This function allows us to process both the successes and failures directories by defining the process as a function.
def process_csv(file_path, file_name, isSuccess):
    # Task 3a: Check if file ends with '.csv' (only process residual files)
    if file_name.endswith(".csv"):
        # Task 3b: Build full file path using os.path.join

        # this links the two strings together like for example
        # data_directory is: "../../correlation_tester/pairs" and file_name is "MSFT_AMZN_residuals.csv"
        # file_path would be ../../correlation_tester/pairs/MSFT_AMZN_residuals"
        file_path = os.path.join(file_path, file_name)


        # ======================
        # PARSE STOCK NAMES
        # ======================

        # Task 4: Extract stock1 and stock2 names from filename
        # Hint: remove '_residuals.csv' suffix, then split by '_'
        current_stock_pair = file_name.replace(".csv", "")
        stock1, stock2 = current_stock_pair.split("_")

        # ======================
        # READ CSV FILE
        # ======================

        # Task 5a: Read CSV file into pandas dataframe

        # Read currentl file into a data fram

        data_frame = pd.read_csv(file_path)


        # Task 5b: Extract 'Residual' column and drop any missing (NaN) values

        # this lets you store the column of residuals into a 1D array

        residuals = data_frame['Residual']

        # ======================
        # RUN ADF TEST
        # ======================

        # Task 6a: Run Augmented Dickey-Fuller test on residuals
        adf_result = adfuller(residuals)

        # Task 6b: Extract p-value from the test result
        p_val = adf_result[1]

        # Task 6c: Add p-value column to .csv file
        # NOT DONE ––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––– (!!!)

        data_frame['P-value'] = p_val

        # ======================
        # OUTPUT RESULTS
        # ======================

        # Task 7: Apply decision rule and print formatted result to screen AND final_results.txt in final_results directory
        if isSuccess:
            if p_val < 0.05:
                print(f"{stock1} and {stock2} are LIKELY cointegrated. p-value is {p_val:.4f}\n")
            else:
                print(f"{stock1} and {stock2} are not cointegrated. p-value is {p_val:.4f}\n")

                # shutil library allows us to move files (less error prone than os library)
                shutil.move(file_path, f"../../data/processed/failures/{file_name}")


# Runs process_csv() function and processes .csv's in both directories
for file_name in os.listdir(failure_dir):
    process_csv(failure_dir, file_name, isSuccess=False)
for file_name in os.listdir(success_dir):
    process_csv(success_dir, file_name, isSuccess=True)