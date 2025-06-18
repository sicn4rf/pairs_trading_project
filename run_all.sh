echo "Compiling and running DATA SCRAPER..."
cd src/downloader/
python download_stock_data.py
cd ../

echo "Compiling and running CORRELATION TEST..."
cd correlation/
g++ -std=c++11 correlation_tester.cpp calc_functions.cpp
./a.out
cd ../

echo "Compiling and running COINTEGRATION TEST...\n"
cd cointegration
python cointegration_tester.py
cd ../../

python tester.py