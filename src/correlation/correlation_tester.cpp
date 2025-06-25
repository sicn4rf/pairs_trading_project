#include "calc_functions.h"
#include "ticker_macros.h"
#include "cli_ui.h"

int main(void)
{
    header("CORRELATION TEST");

    // === TASK 1: Read CSVs into StockData objects ===
    // For each of the 10 CSV files, read raw adjusted close prices, compute log prices,
    // and store them into StockData objects containing dates, raw_prices, log_prices.
    
    // Read what sector user chose.
    string sector_choice = readSector("../../data/results/sector_choice.txt");

    // Declare a vector of ticker names along with an empty vector of StockData objects where we shall store
    // an object storing the data from the .csv files of every ticker we have.
    vector<string> tickers;
    vector<StockData> stock_universe;


    // PREPROCESSOR MACROS CANNOT BE ACCESSED AT RUNTIME... so we have to resort to this monstrosity for now
    if (sector_choice == "TECH") 
    {
        tickers = {TECH};
    }
    else if (sector_choice == "NRG") 
    {
        tickers = {NRG};
    }
    else if (sector_choice == "PHARMA") 
    {
        tickers = {PHARMA};
    }
    else if (sector_choice == "INSUR") 
    {
        tickers = {INSUR};
    }
    else if (sector_choice == "FASTF") 
    {
        tickers = {FASTF};
    }
    else 
    {
        cerr << "Unknown sector: " << sector_choice << endl;
        exit(EXIT_FAILURE);
    }

    // Loop through every ticker in our tickers vector.
    for(const string& current_ticker : tickers)
    {
        // Create a temporary stockData object to read our values into.
        StockData temp_object;

        // readCSV returns a boolean value of whether reading was successful or not. if it was, push that 
        // current temporary object into our stock_universe vector. readCSV takes in 2 arguments, a string
        // file name which will be used to open our filestream to read from and a StockData object which will
        // be passed by reference
        if(readCSV("../../data/raw/" + current_ticker + ".csv", temp_object) == true)
        {
            // set temp_objects ticker to be the name of the current ticker
            temp_object.ticker_name = current_ticker;

            stock_universe.push_back(temp_object);
        }
    }

    if (stock_universe.empty()) {
        keyval("Error:", "No CSVs loaded — check downloader step");
        return 1;
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

    // Edit directory (Delete pairs folder)
    string filepath1 = "../../data/results";

    // Delete pairs if it exists
    if (std::__fs::filesystem::exists(filepath1))
    {
        std::__fs::filesystem::remove_all(filepath1);
    }

    // Create new pairs
    std::__fs::filesystem::create_directory(filepath1);

    // Open a results file to write the statistics
    ofstream results_file("../../data/results/results.txt");
    if(!results_file.is_open())
    {
        cerr << "Error opening results file." << endl;
        return 1; // Exit if file cannot be opened
    }

    for(StockData& current_stock : stock_universe)
    {
        // Calculate statistics for the current stock's raw_prices
        // Assuming raw_prices is already aligned with the common dates
        double mean_value = mean(current_stock.raw_prices);
        double variance_value = variance(current_stock.raw_prices, mean_value);
        double stddev_value = stddev(current_stock.raw_prices, mean_value);
        double iqr_value = iqr(current_stock.raw_prices);
        double spread_value = spread(current_stock.raw_prices);

        // Output the statistics to a text file named after the stock ticker
        results_file << "Ticker: " << current_stock.ticker_name << endl;
        results_file << "Mean: " << mean_value << endl;
        results_file << "Variance: " << variance_value << endl;
        results_file << "Standard Deviation: " << stddev_value << endl;
        results_file << "IQR: " << iqr_value << endl;
        results_file << "Spread: " << spread_value << endl;
        results_file << "----------------------------------------" << endl;
    }

    // End of task 3
    results_file.close(); // Close the results file after writing all statistics
    


    // === TASK 4: Calculate log returns for each stock ===
    // - Compute log returns by subtracting previous day's log price.
    // - Store log returns for correlation calculations. (STORE IN VECTOR STOCK DATA OBJECT)
    for (StockData& current_stock : stock_universe)
    {
        computeLogReturns(current_stock);
    }

    // === TASK 5: Compute Pearson correlation for all stock pairs ===
    // Delete 'pairs' folder, and make new 'pairs' folder (to make sure previous .csv's are gone)
    // Loop through all 45 unique stock pairs:
    // - For each pair, compute Pearson correlation using their log returns.
    // - If absolute correlation >= 0.7, consider this pair valid for cointegration.

    // Edit directory (Delete pairs folder)
    string filepath2 = "../../data/processed";

    // Delete pairs if it exists
    if (std::__fs::filesystem::exists(filepath2))
    {
        std::__fs::filesystem::remove_all(filepath2);
    }

    // Create new pairs
    std::__fs::filesystem::create_directory(filepath2);

    int total_count = 0;
    int corr_count = 0;

    // Pearson Correlation
    for(int i = 0; i < stock_universe.size(); i++)
    {
        for(int j = 0; j < stock_universe.size(); j++)
        {
            if(i == j)
            {
                // avoid self-pair
                continue;
            }
            // counter to count total pairs
            total_count++;

            double corr_coeff = pearsonCorrelation(stock_universe[i].log_returns, stock_universe[j].log_returns);

            // Create three folders
            std::__fs::filesystem::create_directory(filepath2 + "/successes/");
            std::__fs::filesystem::create_directory(filepath2 + "/failures/");
            std::__fs::filesystem::create_directory(filepath2 + "/misfits/");

            if(corr_coeff >= 0.7)
            {
                // TASK 6 linearRegression(log prices of both stocks; also store in proper folder based on correlation)
                //vector<double> current_residuals;
                //linearRegression(stock_universe[i].log_prices, stock_universe[j].log_prices, current_residuals);

                corr_count++;

                string filename = "../../data/processed/successes/" + stock_universe[i].ticker_name + "_" + stock_universe[j].ticker_name + ".csv";
                exportResidualCSV(filename, stock_universe[i], stock_universe[j]);
            }
            else
            {
                string filename = "../../data/processed/failures/" + stock_universe[i].ticker_name + "_" + stock_universe[j].ticker_name + ".csv";
                exportResidualCSV(filename, stock_universe[i], stock_universe[j]);
            }

        }
    }

    // === TASK 6: Run linear regression on valid pairs using log prices ===
    // For each valid pair:
    // - Compute beta, alpha, and residuals from the regression of log prices.
    // - Export the results into a CSV file with columns: Date, Stock1 Price, Stock2 Price, Residual.

    // This loop is able to find all combinations of pairs of stocks

    // === TASK 7: Complete program and wrap up ===
    // Ensure all files are properly closed, and print any summary or status messages.
    keyval("Pairs tested:", to_string(total_count), BOLD);

    string passed  = to_string(corr_count) +
                        " (~" +
                        to_string(static_cast<int>(
                            100.0 * corr_count / total_count)) +
                        "%)";

    keyval("ρ > 0.7 passed:", passed, GREEN);

    cout << '\n';          
    return 0;
}
