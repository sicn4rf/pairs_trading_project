#include "calc_functions.h"


int main(void)
{
    // === TASK 1: Read CSVs into StockData objects ===
    // For each of the 10 CSV files, read raw adjusted close prices, compute log prices,
    // and store them into StockData objects containing dates, raw_prices, log_prices.
    
    // Declare a vector of ticker names along with an empty vector of StockData objects where we shall store
    // an object storing the data from the .csv files of every ticker we have.
    vector<string> tickers = {"AAPL", "MSFT", "AMZN", "GOOG", "META", "NVDA", "TSLA", "INTC", "CSCO", "ORCL"};
    vector<StockData> stock_universe;


    // Loop through every ticker in our tickers vector.
    for(const string& current_ticker : tickers)
    {
        // Create a temporary stockData object to read our values into.
        StockData temp_object;

        // readCSV returns a boolean value of whether reading was successful or not. if it was, push that 
        // current temporary object into our stock_universe vector. readCSV takes in 2 arguments, a string
        // file name which will be used to open our filestream to read from and a StockData object which will
        // be passed by reference
        if(readCSV("../../data_downloader/data/" + current_ticker + ".csv", temp_object) == true)
        {
            // set temp_objects ticker to be the name of the current ticker
            temp_object.ticker_name = current_ticker;

            stock_universe.push_back(temp_object);
        }
    }
    // End of task 1



    // === TASK 2: Align dates across all stocks ===
    // Build a master set of common dates that exist across all 10 stocks.
    // Use set intersection to ensure perfect alignment of dates.
    // After alignment, extract the corresponding raw_prices and log_prices for each stock.

    // REMEMBER NOW WE DONT NEED A COMMON INTERSECTION OF DATES, 
    // WE JUST NEED TO SEE IF THEYRE ALREADY ALIGNED. IF NOT, END THE PROGRAM.
    if (!checkCommonDates(stock_universe))
    {
        cerr << "Size of common dates is smaller. Stopping program." << endl;
        return 1;
    }


    // === TASK 3: Calculate per-stock statistics on raw prices ===
    // For each stock's raw_prices vector:
    // - Compute mean, variance, standard deviation, IQR, and spread (range).
    // - Output these statistics into a .txt file.

    // Open a results file to write the statistics
    ofstream results_file("../results/results.txt");
    if(!results_file.is_open())
    {
        cerr << "Error opening results file." << endl;
        return 1; // Exit if file cannot be opened
    }

    for(StockData& current_stock : stock_universe)
    {
        // Calculate statistics for the current stock's raw_prices
        // Assuming raw_prices is already aligned with the common dates
        double mean = mean(current_stock.raw_prices);
        double variance = variance(current_stock.raw_prices, mean);
        double stddev = stddev(current_stock.raw_prices, mean);
        double iqr_value = iqr(current_stock.raw_prices);
        double spread_value = spread(current_stock.raw_prices);

        // Output the statistics to a text file named after the stock ticker
        results_file << "Ticker: " << current_stock.ticker_name << endl;
        results_file << "Mean: " << mean << endl;
        results_file << "Variance: " << variance << endl;
        results_file << "Standard Deviation: " << stddev << endl;
        results_file << "IQR: " << iqr_value << endl;
        results_file << "Spread: " << spread_value << endl;
        results_file << "----------------------------------------" << endl;
    }

    // End of task 3
    results_file.close(); // Close the results file after writing all statistics
    


    // === TASK 4: Calculate log returns for each stock ===
    // - Compute log returns by subtracting previous day's log price.
    // - Store log returns for correlation calculations. (STORE IN VECTOR STOCK DATA OBJECT)

    // === TASK 5: Compute Pearson correlation for all stock pairs ===
    // Loop through all 45 unique stock pairs:
    // - For each pair, compute Pearson correlation using their log returns.
    // - If absolute correlation >= 0.7, consider this pair valid for cointegration.
    for(int i = 0; i < stock_universe.size() - 1; i++)
    {
        for(int j = i + 1; i < stock_universe.size(); i++)
        {
            double corr_coeff = pearsonCorrelation(stock_universe[i].log_returns, stock_universe[j].log_returns);

            if(pow(corr_coeff, 2) >= 0.7)
            {
                // TASK 6 linearRegression(log prices of both stocks)
            }
        }
    }

    // === TASK 6: Run linear regression on valid pairs using log prices ===
    // For each valid pair:
    // - Compute beta, alpha, and residuals from the regression of log prices.
    // - Export the results into a CSV file with columns: Date, Stock1 Price, Stock2 Price, Residual.

    // === TASK 7: Complete program and wrap up ===
    // Ensure all files are properly closed, and print any summary or status messages.
}
