// This file contains the implementations for every calculation function we
// intend to use in our correlation testing program.



// === TASK 1: Implement readCSV() ===
// Reads CSV file and extracts Date and Adj Close columns.
// Stores Date into dates[], raw Adj Close into raw_prices[], and log(Adj Close) into log_prices[].
bool readCSV(...) 
{

}



// === TASK 2: Implement alignDates() ===
// Takes all StockData objects and finds common dates shared across all stocks.
// Uses std::set and set_intersection() to compute the intersection.
set<string> alignDates(...) 
{

}



// === TASK 3: Implement extractAlignedPrices() ===
// Given a StockData object and common date set,
// extracts raw_prices and log_prices that match those dates.
// You may implement 2 overloaded versions for raw and log prices.
vector<double> extractAlignedPrices(...) 
{

}



// === TASK 4: Implement computeLogReturns() ===
// Takes a vector of log_prices and computes log returns:
// log_return[i] = log_price[i] - log_price[i-1]
// First value skipped (since no previous price).
vector<double> computeLogReturns(...) 
{

}



// === TASK 5: Implement mean() ===
// Takes a vector<double> and computes the mean.
double mean(...) 
{

}



// === TASK 6: Implement variance() ===
// Takes a vector<double> and its mean, computes variance.
double variance(...) 
{

}



// === TASK 7: Implement stddev() ===
// Takes a vector<double> and its mean, returns standard deviation.
double stddev(...) 
{

}



// === TASK 8: Implement iqr() ===
// Takes a vector<double>, sorts it, and computes interquartile range.
// IQR = Q3 - Q1
double iqr(...) 
{

}



// === TASK 9: Implement spread() ===
// Takes a vector<double>, returns (max - min).
double spread(...) 
{

}



// === TASK 10: Implement pearsonCorrelation() ===
// Takes two vectors of log returns, computes Pearson correlation coefficient.
double pearsonCorrelation(...) 
{

}



// === TASK 11: Implement linearRegression() ===
// Given two log price vectors, compute:
// - beta
// - alpha
// - residuals for each point
// Follows OLS regression formulas.
void linearRegression(...) 
{

}



// === TASK 12: Implement exportResidualCSV() ===
// Writes CSV file for a valid pair:
// Columns: Date, Stock1 log price, Stock2 log price, Residual.
void exportResidualCSV(...) 
{

}
