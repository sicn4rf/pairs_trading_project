// This header file contains all the function prototypes for our correlation
// testing program


// === TASK 1: Define StockData struct ===
// struct StockData {
//     vector<string> dates;
//     vector<double> log_prices;
//     string ticker;
// };

// === TASK 2: Declare all functions ===
// Function prototypes for:
// - bool readCSV(const string&, StockData&);
// - set<string> getCommonDates(const vector<StockData>&);
// - vector<double> extractAlignedPrices(const StockData&, const set<string>&);
// - double mean(const vector<double>&);
// - double variance(const vector<double>&, double);
// - double stddev(const vector<double>&, double);
// - double iqr(vector<double>);
// - double pearson(const vector<double>&, const vector<double>&);
// - void exportResidualCSV(...);

// === TASK 3: Include headers and namespace ===
// Use #include guards or #pragma once
// Include standard libraries used in both .cpp files:
// <vector>, <string>, <set>, etc.
// Use: `using namespace std;` or declare std:: explicitly
