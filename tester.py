# test.py  ──────────────────────────────────────────────────────────────
import os, pandas as pd, numpy as np

SUCCESS_DIR   = "./data/processed/successes"
CAPITAL       = 1_000_000          # notional stake per pair
ROLL          = 60                 # window for rolling z-score
THRESHOLD_IN  = 1.8                # tighter → fewer, stronger signals
THRESHOLD_OUT = 0.5
TRADING_DAYS  = 252
TC_PCT_SIDE   = 0.0005             # 0.05 % per side ≈ 1 bp each leg
MAX_HOLD      = 30                 # days; auto-close to stop “evergreen” trades

def backtest_pair(csv_path):
    df        = pd.read_csv(csv_path)
    residuals = df["Residual"]

    mu  = residuals.rolling(ROLL).mean()
    sig = residuals.rolling(ROLL).std()
    z   = (residuals - mu) / sig

    position, entry_px, entry_day = 0, np.nan, None
    daily_pnl  = np.zeros(len(residuals))

    for i in range(len(residuals)):

        # ── ENTRY ──────────────────────────────────────────────────────
        if position == 0:
            if   z[i] >  THRESHOLD_IN:
                position, entry_px, entry_day = -1, residuals[i], i
                daily_pnl[i] -= CAPITAL * TC_PCT_SIDE     # commission/slip
            elif z[i] < -THRESHOLD_IN:
                position, entry_px, entry_day =  1, residuals[i], i
                daily_pnl[i] -= CAPITAL * TC_PCT_SIDE

        # ── EXIT / MARK-TO-MARKET ─────────────────────────────────────
        elif position != 0:
            # Hard stop: max holding period
            if i - entry_day >= MAX_HOLD or abs(z[i]) < THRESHOLD_OUT:
                daily_pnl[i] += position * (residuals[i] - entry_px) * CAPITAL
                daily_pnl[i] -= CAPITAL * TC_PCT_SIDE      # exit cost
                position = 0

            else:
                # intra-trade mark to market
                daily_pnl[i] += position * (residuals[i] - residuals[i-1]) * CAPITAL

    # ── PERFORMANCE METRICS ───────────────────────────────────────────
    total_pnl   = daily_pnl.sum()
    total_ret   = total_pnl / CAPITAL

    # annualise over the *whole* data span, not just trading days
    ann_return  = (1 + total_ret) ** (TRADING_DAYS / len(residuals)) - 1

    daily_ret   = daily_pnl / CAPITAL
    sharpe      = np.nan
    sd = daily_ret.std(ddof=1)
    if sd > 0:
        sharpe = np.sqrt(TRADING_DAYS) * daily_ret.mean() / sd

    return {
        "Pair":   os.path.basename(csv_path).replace(".csv",""),
        "Trades": (daily_pnl != 0).sum() // 2,   # entry+exit = 1 trade
        "TotalPnL":   round(total_pnl, 2),
        "Return_%":   round(total_ret * 100, 2),
        "Annualised_%": round(ann_return * 100, 2),
        "Sharpe": round(sharpe, 2) if not np.isnan(sharpe) else "NA"
    }

def main():
    rows = []
    for f in os.listdir(SUCCESS_DIR):
        if f.endswith(".csv"):
            rows.append(backtest_pair(os.path.join(SUCCESS_DIR, f)))

    res = pd.DataFrame(rows).sort_values("TotalPnL", ascending=False)
    print(res.to_string(index=False))
    res.to_csv("backtest_results.csv", index=False)
    print("\nSaved to backtest_results.csv")

if __name__ == "__main__":
    main()