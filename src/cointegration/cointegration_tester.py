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
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from utils.cli_ui import header, keyval, cointegration_table, GREEN 


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
def process_csv(file_path, file_name, isSuccess) -> float:
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

        data_frame.to_csv(file_path)

        # ======================
        # OUTPUT RESULTS
        # ======================

        # Task 7: Apply decision rule and print formatted result to screen AND final_results.txt in final_results directory
        if isSuccess:
            if p_val < 0.05:                
                return p_val
            else:
                # print(f"{stock1} and {stock2} are not cointegrated. p-value is {p_val:.4f}\n")

                # shutil library allows us to move files (less error prone than os library)
                shutil.move(file_path, f"../../data/processed/failures/{file_name}")
                return None


        if not isSuccess:
            if p_val < 0.05:
                shutil.move(file_path, f"../../data/processed/misfits/{file_name}")
                return None

        return None


header("COINTEGRATION TEST")

# declare counter variables
tested = 0

# Runs process_csv() function and processes .csv's in both directories
fail_csv = [f for f in os.listdir(failure_dir) if f.endswith(".csv")]
success_csv = [f for f in os.listdir(success_dir) if f.endswith(".csv")]

likely_pairs  = []          # ← list of tuples (pair_str, p_val)

if not fail_csv:
    print("Failures folder is empty...")
else:
    for file_name in fail_csv:
        process_csv(failure_dir, file_name, isSuccess=False)


if not success_csv:
    print("Successes folder is emtpy... no correlated pairs :(...")
else:
    for file_name in success_csv:

        tested += 1

        p_val = process_csv(success_dir, file_name, isSuccess=True)
        if p_val is not None:
            pair = file_name.replace(".csv", "").replace("_", " / ")
            likely_pairs.append((pair, p_val))

likely_pairs.sort(key=lambda t: t[1])
cointegration_table(likely_pairs)
passed = f"{len(likely_pairs)} out of {tested} (~{int(100 * len(likely_pairs) / tested)}%)\n"

print('\n')

keyval("Total likely pairs:", passed, GREEN)