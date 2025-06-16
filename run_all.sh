echo "Compiling and running data_downloader.py..."
cd data_downloader/src/
python download_stock_data.py
cd ../../

echo "Compiling and running correlation_tester..."
cd correlation_test/src/
g++ -std=c++11 correlation_tester.cpp calc_functions.cpp
./a.out
cd ../../

echo "Compiling and running cointegration tester..."
cd cointegration_test/src
python cointegration_tester.py
cd ../../
