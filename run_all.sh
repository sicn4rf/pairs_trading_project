cd src/downloader
python download_stock_data.py
cd ../../

cd src/correlation/
g++ -std=c++11 correlation_tester.cpp calc_functions.cpp
./a.out
cd ../

cd cointegration
python cointegration_tester.py
cd ../../

#echo "Running Jupyter Notebooke Visualizer..."
#jupyter nbconvert --to notebook --execute src/visualization/raw_ot.ipynb --inplace

cd src/backtester/
python backtester.py
cd ../../