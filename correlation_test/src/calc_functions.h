// This header file contains all the function prototypes for our correlation
// testing program
#pragma once

#include <iostream>
#include <vector>
#include <fstream>
#include <sstream>
#include <string>
#include <cmath>
#include <algorithm>
#include <set>
#include <map>

using namespace std;

// === TASK 1: Define StockData struct ===

struct StockData
{
    vector<string> dates;
    vector<double> raw_prices;
    vector<double> log_prices;
    vector<double> log_returns;
    string ticker_name;
};

// === TASK 2: Declare all function prototypes ===
// Declare functions for:
bool readCSV(const string& file_name, StockData& temp_stock);
bool checkCommonDates(const vector<StockData>& stock_objects);
void computeLogReturns(StockData& stock_object);
double mean(const vector<double>& stock_values);
double variance(const vector<double>& stock_values, double mean_value);
double stddev(const vector<double>& stock_values, double mean_value);
double iqr(vector<double> stock_values);
double spread(const vector<double>& stock_values);
double pearsonCorrelation(const vector<double>& log_returnX, const vector<double>& log_returnY);
void linearRegression(const vector<double>& stock_valuesX, const vector<double>& stock_valuesY, vector<double>& refResiduals);
void exportResidualCSV(const string& filename, const vector<string>& dates, const vector<double>& log_priceX, const vector<double>& log_priceY);

// - set<string> alignDates(const vector<StockData>&);
// - vector<double> extractAlignedPrices(const StockData&, const set<string>&, bool useLog);

