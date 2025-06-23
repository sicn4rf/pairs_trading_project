 -------------------------------------------------------------------
# 1. Imports
# -------------------------------------------------------------------
# TASK 1: import Python std‑lib & third‑party packages.
# Tip: keep standard library imports first, third‑party next, local last.
# Example:
# import os
# import pandas as pd
# import numpy as np
# -------------------------------------------------------------------

# -------------------------------------------------------------------
# 2. Constants / Strategy Parameters
# -------------------------------------------------------------------
# TASK 2: Declare configuration variables that control the strategy.
# Edit freely as you experiment.
SUCCESS_DIR   = "./data/processed/successes"  # where your residual CSVs live
CAPITAL       = 1_000_000          # dollars committed per pair
ROLL          = 60                 # rolling window length for z‑score
THRESHOLD_IN  = 1.8                # z threshold to *enter* trade
THRESHOLD_OUT = 0.5                # z threshold to *exit* trade
TRADING_DAYS  = 252                # used for annualisation
TC_PCT_SIDE   = 0.0005             # transaction cost per side (0.05 %)
MAX_HOLD      = 30                 # max holding period in days
# -------------------------------------------------------------------

# -------------------------------------------------------------------
# 3. backtest_pair
# -------------------------------------------------------------------

def backtest_pair(csv_path):
    """
    TASK 3 – Implement the core single‑pair back‑test.

    Parameters
    ----------
    csv_path : str
        Path to a CSV file produced by your cointegration routine.
        The file **must** contain a column called 'Residual' representing
        the spread (y - βx) between the two stocks.

    Returns
    -------
    dict
        Performance metrics for this pair (see TASK 3 instructions below).
    """

    # --- 3.a Load data -------------------------------------------------
    # Example:
    # import pandas as pd
    # df = pd.read_csv(csv_path)
    # residuals = df["Residual"]
    # ------------------------------------------------

    # TODO: Replace the lines below with your actual implementation.
    raise NotImplementedError("3.a – Read CSV and pull residual series")

    # --- 3.b Calculate rolling z‑score -------------------------------
    # μ_t = rolling_mean(residuals, window=ROLL)
    # σ_t = rolling_std(residuals, window=ROLL)
    # z_t = (residuals - μ_t) / σ_t
    # HINT: Series.rolling().mean()

    # TODO: compute mu, sig, z

    # --- 3.c Simulate trading loop ------------------------------------
    # Outline:
    #   position   = 0   # +1 long spread, -1 short spread
    #   entry_px   = np.nan
    #   entry_day  = None
    #   daily_pnl  = np.zeros(len(residuals))
    #
    #   for i in range(len(residuals)):
    #       if position == 0:
    #           # Look to *enter* trade
    #           if z[i] > THRESHOLD_IN:  -> open SHORT spread (position = -1)
    #           elif z[i] < -THRESHOLD_IN: -> open LONG spread (position = +1)
    #           # subtract transaction cost once at entry
    #
    #       else:
    #           # Already in trade – decide whether to exit
    #           exit_cond = (i - entry_day >= MAX_HOLD) or (abs(z[i]) < THRESHOLD_OUT)
    #           if exit_cond:
    #               # Realise PnL: position * (residuals[i] - entry_px) * CAPITAL
    #               # subtract exit transaction cost
    #               # reset position variables
    #
    #           else:
    #               # Mark‑to‑market: PnL change since yesterday
    #               # position * (residuals[i] - residuals[i-1]) * CAPITAL
    #
    #   Hint: Using `+=` into daily_pnl[i] captures cashflows each day.
    #
    # TODO: implement trading loop

    # --- 3.d Performance metrics --------------------------------------
    # Examples (replace vars when you have them):
    # total_pnl   = daily_pnl.sum()
    # total_ret   = total_pnl / CAPITAL
    # ann_return  = (1 + total_ret) ** (TRADING_DAYS / len(residuals)) - 1
    #
    # daily_ret   = daily_pnl / CAPITAL
    # sd = daily_ret.std(ddof=1)
    # sharpe = (np.sqrt(TRADING_DAYS) * daily_ret.mean() / sd) if sd > 0 else np.nan
    #
    # trades = (daily_pnl != 0).sum() // 2  # each trade = entry + exit
    #
    # return {
    #     "Pair": os.path.basename(csv_path).replace(".csv",""),
    #     "Trades": trades,
    #     "TotalPnL": round(total_pnl, 2),
    #     "Return_%": round(total_ret * 100, 2),
    #     "Annualised_%": round(ann_return * 100, 2),
    #     "Sharpe": round(sharpe, 2) if not np.isnan(sharpe) else "NA"
    # }
    # ------------------------------------------------------------------
    # TODO: compute stats & build results dict
# -------------------------------------------------------------------

# -------------------------------------------------------------------
# 4. main
# -------------------------------------------------------------------

def main():
    """
    TASK 4 – Portfolio orchestrator.
    Walk over every CSV in SUCCESS_DIR, call backtest_pair, aggregate results.
    Save output to 'backtest_results.csv' and pretty‑print to console.
    """
    # TODO: create results list, loop over files, build DataFrame, sort
    pass
# -------------------------------------------------------------------

# -------------------------------------------------------------------
# 5. Entrypoint
# -------------------------------------------------------------------
if __name__ == "__main__":
    # TASK 5 – Kick things off!
    main()
# -------------------------------------------------------------------
