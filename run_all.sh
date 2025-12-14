#!/usr/bin/env bash
set -e

echo "=== Pairs Trading Pipeline ==="

# Ensure required directories exist
mkdir -p data/raw data/processed/successes data/processed/failures data/processed/misfits data/results

echo "[1/4] Downloading stock data..."
cd src/downloader
python3 download_stock_data.py
cd ../../

echo "[2/4] Running correlation test..."
cd src/correlation/
g++ -std=c++17 -o correlation_tester correlation_tester.cpp calc_functions.cpp
./correlation_tester
cd ../../

echo "[3/4] Running cointegration test..."
cd src/cointegration
python3 cointegration_tester.py
cd ../../

echo "[4/4] Running backtester..."
cd src/backtester/
python3 backtester.py
cd ../../

echo "=== Pipeline complete! ==="