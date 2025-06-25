import os, pandas as pd, numpy as np
# (your other imports)

# ── helper for coloured output ─────────────────────────────
C = {
    "HDR": "\033[96;1m",
    "GRN": "\033[92m",
    "RED": "\033[91m",
    "YLW": "\033[93m",
    "END": "\033[0m",
}

def colour(val, good=True):
    return f"{C['GRN' if good else 'RED']}{val}{C['END']}"

def print_plain(df: pd.DataFrame):
    hdr = f"{C['HDR']}{'Pair':<10}{'Trd':>5}{'PnL':>12}{'Ann%':>8}{'Shrp':>7}{C['END']}"
    print(hdr)
    for _, r in df.iterrows():
        sharpe_colour = (
            C["GRN"] if r.Sharpe >= 2.5 else
            C["YLW"] if r.Sharpe >= 1   else
            C["RED"]
        )
        pnl_txt = colour(f"{r.TotalPnL:>11,.0f}", r.TotalPnL >= 0)
        print(f"{r.Pair:<10}{r.Trades:>5}{pnl_txt} {r['AnnRet%']:>7.2f}"
              f"{sharpe_colour}{r.Sharpe:>7.2f}{C['END']}")