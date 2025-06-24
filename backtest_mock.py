"""
pairs_backtester.py
Back-tests every <Y>_<X>.csv in data/processed/successes/
Each CSV must contain:
    <Y> Raw Price, <X> Raw Price, Residual, Beta   (Alpha optional)
Residual must be   log(Y) - [Alpha + Beta * log(X)]
"""

import os, numpy as np, pandas as pd

SUCCESS_DIR = "data/processed/successes/"
WINDOW      = 21          # rolling window for z-score
ENTRY_TH    = 1.3
EXIT_TH     = 0.3
INIT_CAP    = 100_000
MAX_RISK    = 0.02 * INIT_CAP      # $2,000

# ------------------------------------------------------------
def size_by_risk(beta, px_y, px_x, resid_std):
    """
    How many Y-shares so that a 1.2σ adverse move ≈ MAX_RISK ?
    resid_std is σ of the *residual* (log-space)
    """
    # convert σ in residual-space to an approximate $ move of the spread
    #   Δspread_$  ≈  σ * px_y      (because residual ≈ log(Y) – β log(X))
    dollar_per_sigma = resid_std * px_y
    if dollar_per_sigma == 0:
        return 0, 0
    units = int(MAX_RISK / (1.2 * dollar_per_sigma))
    # hedge ratio in shares
    shares_y = max(units, 1)                    # at least 1 share
    shares_x = shares_y * (beta * px_y / px_x)  # dollar-neutral
    return shares_y, shares_x
# ------------------------------------------------------------
def backtest_pair(csv_path):
    df = pd.read_csv(csv_path)

    # detect tickers from file-name and matching columns
    y_tkr, x_tkr = os.path.basename(csv_path).replace(".csv", "").split("_")
    col_y = f"{y_tkr} Raw Price"
    col_x = f"{x_tkr} Raw Price"

    # sanity check
    if col_y not in df.columns or col_x not in df.columns:
        raise ValueError(f"Missing price columns in {csv_path}")

    # z-score of residual
    df["resid_mean"] = df["Residual"].rolling(WINDOW).mean()
    df["resid_std"]  = df["Residual"].rolling(WINDOW).std()
    df["z_score"]    = (df["Residual"] - df["resid_mean"]) / df["resid_std"]

    beta = df["Beta"].iloc[0]        # constant hedge ratio saved in CSV

    # state
    capital   = INIT_CAP
    position  = 0          # 0 flat | 1 long-spread | -1 short-spread
    entry_px  = {}         # remember entry prices
    shares    = {}         # {'Y': , 'X': }

    trade_log = []

    for i in range(WINDOW, len(df)):
        z, prev_z  = df.at[i, "z_score"], df.at[i-1, "z_score"]
        py, px     = df.at[i, col_y], df.at[i, col_x]
        sig        = df.at[i, "resid_std"]       # σ today (for sizing)

        # ---------- ENTRY ----------
        if position == 0:
            if prev_z <  ENTRY_TH and z >=  ENTRY_TH:      # +1.8 σ  → Y rich
                # short-spread: short Y, long β·X
                sh_y, sh_x = size_by_risk(beta, py, px, sig)
                if sh_y == 0:   # safety
                    continue
                position  = -1
                shares    = {'Y': -sh_y, 'X': +sh_x}
                entry_px  = {'Y': py,    'X': px}

            elif prev_z > -ENTRY_TH and z <= -ENTRY_TH:     # –1.8 σ → Y cheap
                # long-spread: long Y, short β·X
                sh_y, sh_x = size_by_risk(beta, py, px, sig)
                if sh_y == 0:
                    continue
                position  = 1
                shares    = {'Y': +sh_y, 'X': -sh_x}
                entry_px  = {'Y': py,    'X': px}

        # ---------- EXIT ----------
        elif position == -1 and prev_z > EXIT_TH and z <= EXIT_TH:
            pnl = shares['Y'] * (py - entry_px['Y']) \
                + shares['X'] * (px - entry_px['X'])
            capital += pnl
            trade_log.append({"side": "short-spread", "pnl": pnl})
            position = 0

        elif position ==  1 and prev_z < -EXIT_TH and z >= -EXIT_TH:
            pnl = shares['Y'] * (py - entry_px['Y']) \
                + shares['X'] * (px - entry_px['X'])
            capital += pnl
            trade_log.append({"side": "long-spread", "pnl": pnl})
            position = 0

    # -------- performance summary -------- #
    total_pnl = capital - INIT_CAP
    days      = len(df)
    ann_ret   = (capital / INIT_CAP)**(252/days) - 1 if days else 0

    trade_pcts = [p['pnl']/INIT_CAP for p in trade_log]
    sharpe = 0
    if len(trade_pcts) > 1 and np.std(trade_pcts):
        sharpe = np.mean(trade_pcts) / np.std(trade_pcts) * np.sqrt(len(trade_pcts))

    return {
        "Pair": f"{y_tkr}_{x_tkr}",
        "Trades": len(trade_log),
        "TotalPnL": round(total_pnl, 2),
        "AnnRet%": round(ann_ret*100, 2),
        "Sharpe": round(sharpe, 2)
    }
# ------------------------------------------------------------
def main():
    rows = []

    csv_files = [f for f in os.listdir(SUCCESS_DIR) if f.endswith(".csv")]

    if not csv_files:
        print('Successes folder is empty... No cointegrated pairs! :(')
        exit()
    else:
        for file in csv_files:
            if file.endswith(".csv"):
                rows.append(backtest_pair(os.path.join(SUCCESS_DIR, file)))

    summary = pd.DataFrame(rows).sort_values("TotalPnL", ascending=False)
    print(summary.to_string(index=False))
    summary.to_csv("backtest_results.csv", index=False)
    print("\nSaved to backtest_results.csv")

if __name__ == "__main__":
    main()
