# Setup Guide

Here's how to get this thing running on your machine.

## What You Need

Make sure you have these installed first:

1. **Python 3.8 or higher** (Python 3.10+ recommended)
   - Check: `python3 --version`
   - Install: [python.org/downloads](https://www.python.org/downloads/)

2. **C++ Compiler with C++11 support**
   - **macOS**: Install Xcode Command Line Tools
     ```bash
     xcode-select --install
     ```
   - **Linux (Debian/Ubuntu)**:
     ```bash
     sudo apt update && sudo apt install g++ build-essential
     ```
   - **Linux (RHEL/CentOS)**:
     ```bash
     sudo yum install gcc-c++
     ```
   - **Windows**: Install [MinGW-w64](https://www.mingw-w64.org/) or Visual Studio with C++ support

3. **pip** (comes with Python usually)
   - Check: `pip3 --version`

4. **git** (to clone this repo)
   - Check: `git --version`
   - Install: [git-scm.com](https://git-scm.com/downloads)

## Getting Started

### 1. Clone the Repo

```bash
git clone https://github.com/sicn4rf/pairs_trading_project.git
cd pairs_trading_project
```

### 2. Set Up Virtual Environment (recommended)

This keeps dependencies isolated from your system Python:

```bash
# Create virtual environment
python3 -m venv venv

# Activate it
# On macOS/Linux:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

You should see `(venv)` prefix in your terminal prompt.

### 3. Install Python Dependencies

```bash
pip install -r requirements.txt
```

This grabs all the dependencies:
- pandas, numpy, scipy for data work
- statsmodels for cointegration tests
- yfinance to pull stock data
- matplotlib, seaborn for charts
- jupyter for notebooks

### 4. Create Directories

The pipeline needs these folders:

**On macOS/Linux:**
```bash
mkdir -p data/raw data/processed/successes data/processed/failures data/processed/misfits data/results
```

**On Windows (Command Prompt):**
```cmd
mkdir data\raw
mkdir data\processed\successes
mkdir data\processed\failures
mkdir data\processed\misfits
mkdir data\results
```

**On Windows (PowerShell):**
```powershell
New-Item -ItemType Directory -Force -Path data/raw, data/processed/successes, data/processed/failures, data/processed/misfits, data/results
```

### 5. Make Run Script Executable (macOS/Linux only)

```bash
chmod +x run_all.sh
```

## Running It

### Option A: Use the Shell Script (macOS/Linux)

```bash
./run_all.sh
```

This runs everything in order:
1. Downloads stock data for whatever sector you pick
2. Runs correlation analysis (the C++ part)
3. Tests for cointegration
4. Backtests the strategies

### Option B: Run Steps Manually (Windows or if script fails)

```bash
# Step 1: Download data
cd src/downloader
python3 download_stock_data.py
cd ../..

# Step 2: Correlation analysis
cd src/correlation
g++ -std=c++11 -o correlation_tester correlation_tester.cpp calc_functions.cpp
./correlation_tester  # On Windows: correlation_tester.exe
cd ../..

# Step 3: Cointegration testing
cd src/cointegration
python3 cointegration_tester.py
cd ../..

# Step 4: Backtesting
cd src/backtester
python3 backtester.py
cd ../..
```

## Check Your Results

### Backtest Output

Results are in `src/backtester/backtest_results.csv`

### Jupyter Notebooks

Fire up Jupyter to see visualizations:

```bash
jupyter lab src/visualization/
```

You can play with:
- Residual plots
- Correlation heatmaps
- Trading signals

## Troubleshooting

### "python: command not found"

Use `python3` instead, or make an alias:
```bash
# Add to ~/.bashrc or ~/.zshrc
alias python=python3
```

### "g++: command not found"

You need a C++ compiler - check Prerequisites above.

### "ModuleNotFoundError: No module named 'pandas'"

Either you forgot to activate the venv or didn't install dependencies:
1. `source venv/bin/activate`
2. `pip install -r requirements.txt`

### "FileNotFoundError: ... sector_choice.txt"

Missing directories - run step 4 to create them.

### "Permission denied" on ./run_all.sh

Make it executable: `chmod +x run_all.sh`

### C++ compilation fails on macOS

Install Xcode tools:
```bash
xcode-select --install
```

### Windows: "correlation_tester.exe" not found

On Windows it's `.exe`, on Unix it's not. Just use the manual steps.

## Available Sectors

Pick one when prompted:

- **TECH**: Technology & semiconductors (45 stocks: NVDA, AMD, AAPL, etc.)
- **PHARMA**: Pharmaceuticals & biotech (45 stocks: PFE, LLY, MRNA, etc.)
- **NRG**: Energy - oil & gas (45 stocks: CVX, XOM, FANG, etc.)
- **INSUR**: Insurance & financial services (45 stocks: ALL, PGR, TRV, etc.)
- **FASTF**: Fast food chains (45 stocks: MCD, YUM, CMG, etc.)

## How Long This Takes

- Data download: 1-3 min (depends on your internet)
- Correlation: 10-30 sec
- Cointegration: 1-2 min
- Backtesting: 30-60 sec

About 5-10 minutes total per sector.

## Quick Check

Make sure everything's working:

```bash
# Check Python
python3 --version  # Should show 3.8+

# Check pip
pip3 --version

# Check C++ compiler
g++ --version

# Check virtual environment (if activated)
which python3  # Should point to venv/bin/python3

# Check installed packages
pip list | grep pandas
pip list | grep yfinance
```

## When You're Done

Exit the virtual environment:

```bash
deactivate
```

## Still Stuck?

If something's broken:
1. Double-check prerequisites
2. Make sure directories exist
3. Confirm venv is activated
4. Check file permissions (Unix)
5. Read the error message - usually tells you what's wrong

## What's Next

Once it's working:
1. Try different sectors
2. Tweak parameters in `src/backtester/backtester.py`
3. Check out the Jupyter notebooks
4. Read the paper: `informal_research_paper.pdf`
