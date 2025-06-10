// This file contains the implementations for every calculation function we
// intend to use in our correlation testing program.



// === TASK 1: Implement readCSV() ===
// Reads a CSV file with yfinance format
// Extracts Date and Close columns, stores log(Close)
// Populates StockData struct (dates[], log_prices[])
... readCSV(...)
{

}

// === TASK 2: Implement getCommonDates() ===
// Takes all StockData and finds dates present in *all* stocks
// Uses std::set and set_intersection()
... getCommonDates(...)
{

}

// === TASK 3: Implement extractAlignedPrices() ===
// Given a StockData and a set of common dates
// Extracts log prices that match those dates (in order)
... extractAlignedPrices(...)
{

}

// === TASK 4: Implement mean(), variance(), stddev(), iqr() ===
// Each takes a vector<double> and returns a double
// IQR uses sorting and indexes Q1, Q3
... mean(...)
{

}

... variance(...)
{

}

... stddev(...)
{

}

... inter_quartile_range(...)
{

}

// === TASK 5: Implement pearson() ===
// Takes two vectors (x, y) and returns Pearson correlation
// Use greedy implementation (manual sums)
... pearson(...)
{

}

// === TASK 6: Implement exportResidualCSV() ===
// Run linear regression: y = alpha + beta * x
// Compute residuals (y_i - predicted_y_i)
// Write date, stock1, stock2, residual to a CSV file
... exportResidualCSV(...)
{

}
