"""
pairs_backtest.py
Back-tests every <Y>_<X>.csv in data/processed/successes/

Each CSV must contain at least:
    <Y> Raw Price, <X> Raw Price, Residual, Beta
Residual must be  log(Y) − [Alpha + Beta · log(X)]

Strategy:
    • Rolling 21-day mean / std dev  →  z-score
    • Entry  when z crosses ±1.3
    • Exit   when z crosses back ±0.3
    • Size   so a further 1.2 σ adverse move ≈ $2 000 (2 % of 100 k)
    • HARD CAP: gross notional ≤ 150 % of equity
"""

import os
import numpy as np
import pandas as pd
from pathlib import Path


# ----------------------------- USER PARAMS -------------------------------- #
SUCCESS_DIR  = "data/processed/successes/"   # folder of pair CSVs
WINDOW       = 21          # rolling window for z-score
ENTRY_TH     = 1.5
EXIT_TH      = 0.5
INIT_CAP     = 100_000      # starting cash
MAX_RISK     = 0.01 * INIT_CAP   # $1,000, 1% of capital
MAX_LEV      = 0.5     # 50 % of equity
MAX_GROSS    = INIT_CAP * MAX_LEV # $50,000 max exposure
# -------------------------------------------------------------------------- #

def size_by_risk(beta, px_ind, px_dep, resid_std):

    #   Return (sharesY, sharesX) so that a 1.2 σ adverse move ≈ MAX_RISK.

    dollar_per_sigma = resid_std * px_dep
    shares_dep = MAX_RISK / (1.2 * dollar_per_sigma)
    shares_ind = shares_dep * beta * px_dep / px_ind
    return shares_ind, shares_dep


def backtest_pair(csv_path: str) -> dict:
    # Run the strategy on one CSV; return summary statistics.
    data = pd.read_csv(csv_path)

    # --- Detect tickers from filename and build column names -------------
    current_name = Path(csv_path).stem
    ind_tick, dep_tick = current_name.split("_")
    

    raw_ind = data[f"{ind_tick} Raw Price"]
    raw_dep = data[f"{dep_tick} Raw Price"]

    # --- Build z-score ----------------------------------------------------
    data["resid_mean"] = data["Residual"].rolling(WINDOW).mean()
    data["resid_std"]  = data["Residual"].rolling(WINDOW).std()
    data["z_score"]    = (data["Residual"] - data["resid_mean"]) / data["resid_std"]

    beta = data["Beta"].iloc[0]

    # --- State vars -------------------------------------------------------
    capital   = INIT_CAP
    position  = 0            # 0 flat | +1 long-spread | −1 short-spread
    shares    = {"Independent": 0.0, "Dependent": 0.0}
    entry_px  = {"Independent": np.nan, "Dependent": np.nan}
    trades    = []
    equity = []

    # --- Back-test loop ---------------------------------------------------
    for i in range(WINDOW, len(data)):
        z = data.at[i, "z_score"]
        prev_z = data.at[i - 1, "z_score"]
        px_ind, px_dep   = raw_ind.at[i]   , raw_dep.at[i]
        std_res       = data.at[i, "resid_std"]
        equity.append(capital)

        # -------------- ENTRY -----------------
        if position == 0:
            crossed_hi = prev_z <  ENTRY_TH and z >=  ENTRY_TH  # Y rich +z score
            crossed_lo = prev_z > -ENTRY_TH and z <= -ENTRY_TH  # Y cheap -z score

            if crossed_hi or crossed_lo:
                shares_ind, shares_dep = size_by_risk(beta, px_ind, px_dep, std_res)


                # ---- Leverage cap -----
                gross = abs(shares_ind * px_ind) + abs(shares_dep * px_dep)
                if gross > MAX_GROSS:
                    scale = MAX_GROSS / gross
                    shares_dep *= scale
                    shares_ind *= scale
                    gross = abs(shares_dep * px_dep) + abs(shares_ind * px_ind)

                # integer shares (round down) – ensure at least 1 share
                shares_dep = max(1, int(shares_dep))
                shares_ind = max(1, int(shares_ind))

                sign = -1 if crossed_hi else +1          # -1 short-spread
                position     = sign
                shares["Independent"]  = -sign * shares_ind              # opposite leg
                shares["Dependent"]  =  sign * shares_dep              # long or short Y
        
                entry_px["Independent"] = px_ind
                entry_px["Dependent"] = px_dep
                
                continue  # go to next day

        # -------------- EXIT ------------------
        exit_short = position == -1 and prev_z > EXIT_TH and z <=  EXIT_TH
        exit_long  = position == +1 and prev_z < -EXIT_TH and z >= -EXIT_TH
        if exit_short or exit_long:
            pnl = shares["Dependent"] * (px_dep - entry_px["Dependent"]) + shares["Independent"] * (px_ind - entry_px["Independent"])
            capital += pnl
            trades.append({"Side": "short-long" if position == -1 else "long-short",
                           "Profit & Loss": pnl})
            position  = 0
            shares    = {"Dependent":0.0, "Independent":0.0}



    # -------------- Summary stats ----------------
    total_pnl = round(capital - INIT_CAP, 2)
    days      = len(data)
    ann_ret   = round(((capital / INIT_CAP)**(252/days) - 1) * 100, 2) if days else 0

    trade_pct = [t["Profit & Loss"]/INIT_CAP for t in trades]
    sharpe    = 0
    equity = pd.Series(equity, index=data.index[WINDOW:])
    daily_ret = equity.pct_change().dropna()

    if len(daily_ret) > 1 and daily_ret.std():
        sharpe = round(daily_ret.mean() / daily_ret.std() * np.sqrt(252), 2)
    else:
        sharpe = 0

    return {
        "Pair": f"{dep_tick}_{ind_tick}",
        "Trades": len(trades),
        "TotalPnL": total_pnl,
        "AnnRet%": ann_ret,
        "Sharpe": sharpe
    }


def main():
    rows = []
    csv_files = [f for f in os.listdir(SUCCESS_DIR) if f.endswith(".csv")]
    
    if csv_files:
        for file in csv_files:
            rows.append(backtest_pair(os.path.join(SUCCESS_DIR, file)))
    else:
        print("Successes folder is empty.. No cointegrated pairs :(")
        exit()

    summary = pd.DataFrame(rows).sort_values("TotalPnL", ascending=False)
    print(summary.to_string(index=False))
    summary.to_csv("backtest_results.csv", index=False)
    print("\nSaved to backtest_results.csv")


if __name__ == "__main__":
    main()
