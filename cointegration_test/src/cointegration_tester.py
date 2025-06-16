# Cointegration Tester (Boilerplate)
# This file processes residual CSV files from C++ output and tests for cointegration.

# ======================
# IMPORT LIBRARIES
# ======================

# Task 1a: Import os (used for directory/file handling)
import os
import pandas as pd
from statsmodels import adfuller


# ======================
# DEFINE INPUT DIRECTORY
# ======================

# Task 2: Set the directory path where your residual CSV files are stored.
residual_directory = "../../correlation_test/pairs/"


# ======================
# ITERATE THROUGH FILES
# ======================

# Task 3: Loop through all files in the directory

# listdir is like saying "ls" in your terminal and then we can store all those files in a list

file_list = os.listdir(data_directory)

for file_name in file_list:

    # Task 3a: Check if file ends with '_residuals.csv' (only process residual files)
    if file_name.endswith("_residuals.csv") :
        # Task 3b: Build full file path using os.path.join

        # this links the two strings together like for example
        # data_directory is: "../../correlation_tester/pairs" and file_name is "MSFT_AMZN_residuals.csv"
        # file_path would be ../../correlation_tester/pairs/MSFT_AMZN_residuals"
        file_path = os.path.join(data_directory, file_name)


        # ======================
        # PARSE STOCK NAMES
        # ======================

        # Task 4: Extract stock1 and stock2 names from filename
        # Hint: remove '_residuals.csv' suffix, then split by '_'
        current_stock_pair = file_name.replace("_residuals.csv", "")
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

        # ======================
        # OUTPUT RESULTS
        # ======================

        # Task 7: Apply decision rule and print formatted result to screen AND final_results.txt in final_results directory

        if p_val < 0.05:
            print(f"{stock1} and {stock2} are likely cointegrated. p-value is {p_val:.4f}")
        else:
            print(f"{stock1} and {stock2} are not cointegrated. p-value is {p_val:.4f}")