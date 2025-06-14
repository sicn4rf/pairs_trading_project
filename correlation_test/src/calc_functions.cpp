// This file contains the implementations for every calculation function we
// intend to use in our correlation testing program.
#include "calc_functions.h"


// === TASK 1: Implement readCSV() ===
// Reads CSV file and extracts Date and Adj Close columns.
// Stores Date into dates[], raw Adj Close into raw_prices[], and log(Adj Close) into log_prices[].
bool readCSV(const string& file_name, StockData& temp_stock) 
{   
    // Create a file stream object for reading. In this case, "file_name" is actually,
    // "../../data_downloader/data/___.csv"
    ifstream read_file(file_name);

    // Test for filestream open failure. If failed, return false. DONT PUSH_BACK FAILED OBJECT READING
    if(read_file.is_open() != true)
    {
        return false;
    }

    // Create variables to hold current line and temporary values for reading
    string current_line;
    string date;
    string close;
    string temp; // Use this to hold Open, High, Low, Volume, Dividends, and Stock Splits
                // We only care about adj close price and date.

    getline(read_file, current_line); // do this to skip the first line (header)

    while(getline(read_file, current_line))
    {
        // Create a string stream variable of the current line so we can use getline
        // on it and treat it like a stream
        stringstream str_stream(current_line);

        // Recall: getline("an input stream", "a string variable for storage", 
        // "an optional delimiter, is \n by default")
        getline(str_stream, date, ',');
        getline(str_stream, temp, ','); // Open
        getline(str_stream, temp, ','); // High
        getline(str_stream, temp,',');  // Low
        getline(str_stream, close, ',');
        getline(str_stream, temp, ','); // Volume
        getline(str_stream, temp, ','); // Dividends
        getline(str_stream, temp, ','); // Stock Splits

        
        // if our date and close strings are non_empty. Store them into our temp_stock object
        if(date.empty() == false || close.empty() == false)
        {
            temp_stock.dates.push_back(date);
            
            // Close is a string, conver it to a double before pushing into objects vector
            double price = stod(close);

            temp_stock.raw_prices.push_back(price);

            // Push the value of the natural log of close price
            temp_stock.log_prices.push_back(log(price));
        }   
    }

    return true;
}



// === TASK 2: Implement alignDates() ===
// Takes all StockData objects and finds common dates shared across all stocks.
// Uses std::set and set_intersection() to compute the intersection.
// set<string> alignDates(...) {}
// NOT NEEDED FOR NOW SINCE WE DONT NEED TO ALIGN DATES^^^

//INSTEAD IMPLEMENT A FUNCTION THAT CHECKS IF ALL STOCKS ARE ALREADY ALIGNED, checkCommonDates()
// CHECK EACH DATE VECTOR OF STRINGS AND SEE THEY HAVE THE SAME VALUES AND SIZES
bool checkCommonDates(const vector<StockData>& stock_objects) 
{
    // First, find common_dates:
    // Set common_dates as the first StockData's date so that the loop will work.
    vector<string> common_dates = stock_objects[0].dates;

    // Iterate through each stock in stock_universe to compute intersection of all stock dates.
    for (const StockData& current_stock : stock_objects)
    {
        // temp_dates will store the current iteration's resulting intersection.
        vector<string> temp_dates;

        // Some notes about back_inserter():
        // back_inserter does not replace the contents of the vector, but appends it.
        set_intersection(current_stock.dates.begin(), current_stock.dates.end(), common_dates.begin(), common_dates.end(), back_inserter(temp_dates));
        
        // replace all of common_date's elements with temp_dates --> temp_dates will be wiped in the next iteration
        common_dates = temp_dates;
    }

    // Second, check if common_dates guarantees alignment:
    // If the size doesn't match, guarantees not aligned --> immediately return false;
    // In fact, we only need to worry about the size
    // Taking the intersection of all sets, common_date therefore contains what everyone shares.
    // Explanation:
    // If, at any time, any of the sizes of the stocks don't match the size of the common_date, that means there are more dates
    // that that stock has. Therefore, we only need to check if the sizes match, and do not have to iterate through every entry of
    // date that is in the .dates() vectors.
    for (int i = 0; i < stock_objects.size(); i++)
    {
        if (common_dates.size() < stock_objects[i].dates.size())
            return false;
    }

    return true;
}


// === TASK 3: Implement extractAlignedPrices() ===
// Given a StockData object and common date set,
// extracts raw_prices and log_prices that match those dates.
// You may implement 2 overloaded versions for raw and log prices.

/*
vector<double> extractAlignedPrices(StockData& stock_object,) 
{

}
*/
// NOT NEEDED FOR NOW SINCE WE DONT NEED TO ALIGN DATES^^^


// === TASK 4: Implement computeLogReturns() ===
// Takes a vector of log_prices and computes log returns:
// log_return[i] = log_price[i] - log_price[i-1]
// First value skipped (since no previous price).
void computeLogReturns(StockData& stock_object) 
{
    for (int i = 1; i < stock_object.log_prices.size(); i++)
    {
        stock_object.log_returns.push_back(stock_object.log_prices[i] - stock_object.log_prices[i-1]);
    }
    // end
} 



// === TASK 5: Implement mean() ===
// Takes a vector<double> and computes the mean.
double mean(const vector<double>& stock_values) 
{
    if(stock_values.empty())
    {
        return 0; // Return 0 if the vector is empty to avoid division by zero
    }

    double sum = 0.0;


    // Sum all values in the vector
    for(const double& value : stock_values)
    {
        sum += value;
    }

    return sum / stock_values.size(); // Return the sum of all values divided by the number of values
}



// === TASK 6: Implement variance() ===
// Takes a vector<double> and its mean, computes sample variance.
double variance(const vector<double>& stock_values, double mean_value) 
{
    double var = 0.0;

    // Summation of (X_i - X_bar) ^ 2
    for (double current_stock_value : stock_values)
    {
        var += pow((current_stock_value - mean_value),2);
    }

    var /= stock_values.size() - 1;

    return var;
}



// === TASK 7: Implement stddev() ===
// Takes a vector<double> and its mean, returns standard deviation.
double stddev(vector<double>& stock_values, double mean_value) 
{
    if(stock_values.empty())
    {
        return 0; // Return 0 if the vector is empty to avoid division by zero
    }

    return sqrt(variance(stock_values, mean_value)); // Standard deviation is the square root of variance
}


// === TASK 8: Implement iqr() ===
// Takes a vector<double>, sorts it, and computes interquartile range.
// IQR = Q3 - Q1
double iqr(const vector<double>& stock_values) 
{
    // Create copy 
    vector<double> copy_vector = stock_values;

    // Sort the values in ascending order
    sort(copy_vector.begin(), copy_vector.end());

    // Find Q1 and Q3's indices
    int quarter1_index = stock_values.size()/4;
    int quarter3_index = 3 * quarter1_index;

    // IQR == Q3 - Q1
    return stock_values[quarter3_index] - stock_values[quarter1_index];
}



// === TASK 9: Implement spread() ===
// Takes a vector<double>, returns (max - min).
double spread(vector<double>& stock_values) 
{
    double min = stock_values[0];
    double max = stock_values[0];

    // Simple greedy algorithm to find max and min of a given vector of doubles
    for(const double& current_value : stock_values)
    {
        if(current_value < min)
        {
            min = current_value;
        }
        
        if(current_value > max)
        {
            max = current_value;
        }
    }

    return (max - min);  // returns spread
}



// === TASK 10: Implement pearsonCorrelation() ===
// Takes two vectors of log returns, computes Pearson correlation coefficient.
double pearsonCorrelation(const vector<double>& log_returnX, const vector<double>& log_returnY) 
{
    // Compute mean of X and Y, which we will call X_bar and Y_bar respectively
    double x_bar = mean(log_returnX), y_bar = mean(log_returnY);

    double numerator=0, denominator1=0, denominator2=0;

    for (int i = 0; i < log_returnX.size(); i++)
    {
        double xi_minus_xbar = log_returnX[i] - x_bar;
        double yi_minus_ybar = log_returnY[i] - y_bar;

        numerator += xi_minus_xbar * yi_minus_ybar;
        denominator1 += pow(xi_minus_xbar, 2);
        denominator2 += pow(yi_minus_ybar, 2);
    }

    // return r (correl coeff)
    return numerator / ( sqrt(denominator1 * denominator2) );
}



// === TASK 11: Implement linearRegression() ===
// Given two log price vectors, compute:
// - beta
// - alpha
// - residuals for each point
// Follows OLS regression formulas.
void linearRegression(const vector<double>& stock_valuesX, const vector<double>& stock_valuesY, vector<double>& refResiduals) 
{
    // Declare mean values for stocks X and Y
    double mean_stockX = mean(stock_valuesX);
    double mean_stockY = mean(stock_valuesY);

    double numerator = 0;
    double denominator = 0;

    double residual;

    // Compute numerator and denominator for beta
    for(int i = 0; i < stock_valuesX.size(); i++)
    {
        // [X(at time) - X(mean)] * [Y(at time) - Y(mean)]
        numerator += ((stock_valuesX[i] - mean_stockX) * (stock_valuesY[i] - mean_stockY));
        // [X(at time) - X(mean)]^2
        denominator += pow((stock_valuesX[i] - mean_stockX), 2);
    }

    double refBeta = numerator / denominator;
    double refAlpha = mean_stockY - (refBeta * mean_stockX);

    // Loop through every value in the pair of stocks and use alpha and beta to calculate residuals
    // Store these residuals in a vector
    for(int i = 0; i < stock_valuesX.size(); i++)
    {
        residual = stock_valuesY[i] - (refAlpha + (refBeta * stock_valuesX[i]));

        refResiduals.push_back(residual);
    }
}



// === TASK 12: Implement exportResidualCSV() ===
// Writes CSV file for a valid pair:
// Columns: Date, Stock1 log price, Stock2 log price, Residual.
// filename includes path and .csv
void exportResidualCSV(const string& filename, const vector<string>& dates, const vector<double>& log_priceX, const vector<double>& log_priceY) 
{
    // Re-extract ticker name from 'filename'
    size_t start_pos = filename.find_last_of('/') + 1;      // after '/'
    size_t end_pos = filename.find(".csv");                 // start of ".csv"
    size_t length = end_pos - start_pos;                    // number of characters between

    string cleaner_string = filename.substr(start_pos, length);  // "XXXX_YYYY"
    string ticker1 = cleaner_string.substr(0, cleaner_string.find('_'));
    string ticker2 = cleaner_string.substr(cleaner_string.find('_') + 1);
    
    // Compute residuals
    vector<double> residuals;
    linearRegression(log_priceX, log_priceY, residuals);

    // Output stream create
    ofstream outfile(filename);
    if (!outfile.is_open()) 
    {
        cerr << "Error: Could not open file - " << filename << " for writing.\n";
        return;
    }   


    // Header Row
    //           1                 2                           3               4
    outfile << "Date," << ticker1 << " Log Price," << ticker2 << " Log Price,Residual\n";

    for (int i = 0; i < log_priceX.size(); i++)
    {
        outfile << dates[i] << ',' << log_priceX[i] << ',' << log_priceY[i] << ',' << residuals[i] << '\n';
    }

    outfile.close();
}
