// This header file contains all the function prototypes for our correlation
// testing program


// === TASK 1: Define StockData struct ===
// struct StockData {
//     vector<string> dates;
//     vector<double> raw_prices;
//     vector<double> log_prices;
// };

// === TASK 2: Declare all function prototypes ===
// Declare functions for:
// - bool readCSV(const string&, StockData&);
// - set<string> alignDates(const vector<StockData>&);
// - vector<double> extractAlignedPrices(const StockData&, const set<string>&, bool useLog);
// - vector<double> computeLogReturns(const vector<double>&);
// - double mean(const vector<double>&);
// - double variance(const vector<double>&, double);
// - double stddev(const vector<double>&, double);
// - double iqr(vector<double>);
// - double spread(const vector<double>&);
// - double pearsonCorrelation(const vector<double>&, const vector<double>&);
// - void linearRegression(const vector<double>&, const vector<double>&, double&, double&, vector<double>&);
// - void exportResidualCSV(...);

// === TASK 3: Include standard libraries and namespace ===
// Include necessary headers:
// <iostream>, <fstream>, <sstream>, <vector>, <string>, <cmath>, <algorithm>, <set>, <map>
// Use include guards (#pragma once or #ifndef ... #endif).
// Declare 'using namespace std;' or qualify with std::.
