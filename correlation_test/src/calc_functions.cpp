// This file contains the implementations for every calculation function we
// intend to use in our correlation testing program.



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
        getline(str_stream, date, ",");
        getline(str_stream, temp, ","); // Open
        getline(str_stream, temp, ","); // High
        getline(str_stream, temp,",");  // Low
        getline(str_stream, close, ",");
        getline(str_stream, temp, ","); // Volume
        getline(str_stream, temp, ","); // Dividends
        getline(str_stream, temp, ","); // Stock Splits

        
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
set<string> alignDates(...) 
{

}

// NOT NEEDED FOR NOW SINCE WE DONT NEED TO ALIGN DATES^^^

//INSTEAD IMPLEMENT A FUNCTION THAT CHECKS IF ALL STOCKS ARE ALREADY ALIGNED, checkCommonDates()
// CHECK EACH DATE VECTOR OF STRINGS AND SEE THEY HAVE THE SAME VALUES AND SIZES
bool checkCommonDates(const vector<StockData>& stock_objects) 
{

}


// === TASK 3: Implement extractAlignedPrices() ===
// Given a StockData object and common date set,
// extracts raw_prices and log_prices that match those dates.
// You may implement 2 overloaded versions for raw and log prices.
vector<double> extractAlignedPrices(StockData& stock_object,) 
{

}

// NOT NEEDED FOR NOW SINCE WE DONT NEED TO ALIGN DATES^^^


// === TASK 4: Implement computeLogReturns() ===
// Takes a vector of log_prices and computes log returns:
// log_return[i] = log_price[i] - log_price[i-1]
// First value skipped (since no previous price).
vector<double> computeLogReturns(...) 
{

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
        sum += value
    }

    return sum / stock_values.size(); // Return the sum of all values divided by the number of values
}



// === TASK 6: Implement variance() ===
// Takes a vector<double> and its mean, computes variance.
double variance(...) 
{

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
