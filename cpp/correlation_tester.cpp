#include <iostream>
#include <vector>


int main(void)
{
    // === TASK 1: Load all CSVs into StockData structs ===
    // Loop over all tickers and call readCSV() from calc_functions.cpp.
    // Each CSV file is in data/, and contains log(close) prices.
    // Store all loaded StockData structs into a vector.

    // === TASK 2: Align dates across all stocks ===
    // Call getCommonDates() and extractAlignedPrices() for each stock.
    // Make sure all log_price vectors are aligned to the same date set.
    // Store aligned price arrays in a 2D vector: aligned_prices[i][j].

    // === TASK 3: Write per-stock statistics to stock_stats.txt ===
    // For each stock, compute mean, variance, stddev, and IQR
    // using functions from calc_functions.cpp.
    // Save results to a text file (not stdout).

    // === TASK 4: Loop through all 45 unique stock pairs ===
    // For each pair, calculate Pearson correlation.
    // If abs(correlation) > 0.7, consider them correlated.

    // === TASK 5: For each correlated pair, perform linear regression ===
    // Compute alpha, beta, residuals of the pair (y = alpha + beta * x).
    // Export a CSV file for each selected pair with columns:
    // Date, Stock1, Stock2, Residual

    // === TASK 6: Wrap up ===
    // Exit gracefully, maybe print summary to a file if needed.

}
