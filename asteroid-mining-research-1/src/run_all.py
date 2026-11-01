from __future__ import annotations

from run_analysis import write_assumptions, write_baseline_results
from make_figures import main as make_figures


if __name__ == "__main__":
    write_assumptions()
    write_baseline_results()
    make_figures()
    print("Complete: assumptions, results, and figures generated.")
