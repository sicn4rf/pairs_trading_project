#include <iostream>
#include <iomanip>          // std::setw
#include <string>

// ─── ANSI colours ──────────────────────────────────────────
const std::string RESET = "\033[0m";
const std::string BOLD  = "\033[1m";
const std::string CYAN  = "\033[96m";
const std::string GREEN = "\033[92m";
const std::string YEL   = "\033[93m";
const std::string GRAY  = "\033[90m";

// header() prints a dashed bar + title
inline void header(const std::string& title)
{
    std::string bar(title.length() + 6, '-');          // ASCII dash
    std::cout << GRAY << bar << RESET << '\n'
              << CYAN << BOLD << "  "
              << title << RESET << '\n'
              << GRAY << bar << RESET << '\n';
}

inline void keyval(const std::string& label,
                   const std::string& value,
                   const std::string& colour = CYAN)
{
    std::cout << "  " << BOLD << std::setw(22) << std::left << label << RESET
              << colour << value << RESET << '\n';
}