# utils/cli_ui.py  ──────────────────────────────────────────────
RESET = "\033[0m"
BOLD  = "\033[1m"
CYAN  = "\033[96m"
GREEN = "\033[92m"
RED   = "\033[91m"
YEL   = "\033[93m"
GRAY  = "\033[90m"

def header(title: str, color=CYAN):
    bar = GRAY + "─" * (len(title) + 6) + RESET
    print(f"{bar}\n{color}{BOLD}  {title}{RESET}\n{bar}")

def keyval(label: str, value, color=CYAN):
    print(f"  {BOLD}{label:<22}{RESET}{color}{value}{RESET}")

def cointegration_table(pairs):
    print(f"{BOLD}{' #':>3} {'Pair':<12} {'p-value':>8}{RESET}")
    for i, (pair, pval) in enumerate(pairs, 1):
        shade = GREEN if pval < 0.01 else (YEL if pval < 0.05 else "")
        print(f"{i:>3} {pair:<12} {shade}{pval:>8.4f}{RESET}")
