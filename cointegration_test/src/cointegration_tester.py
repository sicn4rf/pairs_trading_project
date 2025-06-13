# Cointegration Tester (Boilerplate)
# This file processes residual CSV files from C++ output and tests for cointegration.

# ======================
# IMPORT LIBRARIES
# ======================

# Task 1a: Import os (used for directory/file handling)


# Task 1b: Import pandas (used for CSV reading and dataframe manipulation)


# Task 1c: Import adfuller function from statsmodels (used for ADF stationarity test)



# ======================
# DEFINE INPUT DIRECTORY
# ======================

# Task 2: Set the directory path where your residual CSV files are stored.


# ======================
# ITERATE THROUGH FILES
# ======================

# Task 3: Loop through all files in the directory

    # Task 3a: Check if file ends with '_residuals.csv' (only process residual files)

        # Task 3b: Build full file path using os.path.join

        # ======================
        # PARSE STOCK NAMES
        # ======================

        # Task 4: Extract stock1 and stock2 names from filename
        # Hint: remove '_residuals.csv' suffix, then split by '_'

        # ======================
        # READ CSV FILE
        # ======================

        # Task 5a: Read CSV file into pandas dataframe


        # Task 5b: Extract 'Residual' column and drop any missing (NaN) values

        # ======================
        # RUN ADF TEST
        # ======================

        # Task 6a: Run Augmented Dickey-Fuller test on residuals

        # Task 6b: Extract p-value from the test result


        # ======================
        # OUTPUT RESULTS
        # ======================

        # Task 7: Apply decision rule and print formatted result to screen AND final_results.txt in final_results directory
