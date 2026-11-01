from __future__ import annotations

import csv
from pathlib import Path

from model import ModelInputs, run_model

ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results"
DATA = ROOT / "data"


def write_baseline_results() -> None:
    inputs = ModelInputs()
    outputs = run_model(inputs)
    RESULTS.mkdir(exist_ok=True)

    rows = [
        ("Feedstock processed", f"{outputs['feedstock_t']:.0f} t"),
        ("Recovered and delivered resource", f"{outputs['recovered_resource_t']:.1f} t"),
        ("Fixed mission cost", f"${outputs['fixed_cost_usd']/1e9:.2f}B"),
        ("Variable processing cost", f"${outputs['variable_cost_usd']/1e6:.1f}M"),
        ("Operations cost", f"${outputs['operations_cost_usd']/1e6:.1f}M"),
        ("Total modeled cost", f"${outputs['total_cost_usd']/1e9:.2f}B"),
        ("Break-even resource price", f"${outputs['break_even_price_usd_per_kg']:,.0f}/kg"),
        ("Reference benchmark", f"${outputs['benchmark_cost_usd_per_kg']:,.0f}/kg"),
        ("Break-even / benchmark", f"{outputs['break_even_to_benchmark_ratio']:.2f}x"),
    ]

    with (RESULTS / "baseline_results.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["metric", "value"])
        writer.writerows(rows)

    with (RESULTS / "baseline_results.txt").open("w", encoding="utf-8") as f:
        f.write("Asteroid mining scenario model - baseline\n")
        f.write("These results are scenario outputs, not a commercial forecast.\n\n")
        for metric, value in rows:
            f.write(f"{metric}: {value}\n")


def write_assumptions() -> None:
    DATA.mkdir(exist_ok=True)
    rows = [
        ["parameter", "value", "unit", "source_type", "notes"],
        ["feedstock_t", 5000, "tonnes", "modeling assumption", "Illustrative commercial-scale scenario."],
        ["resource_fraction", 0.10, "fraction", "modeling assumption", "10% resource fraction; not assigned to a specific asteroid."],
        ["extraction_efficiency", 0.80, "fraction", "modeling assumption", "Fraction of contained resource successfully recovered."],
        ["delivery_efficiency", 0.95, "fraction", "modeling assumption", "Fraction of recovered resource delivered to the customer."],
        ["fixed_cost_usd", 1200000000, "USD", "modeling assumption", "Up-front mission/development cost."],
        ["variable_cost_usd_per_t", 150000, "USD/tonne feedstock", "modeling assumption", "Mining and processing variable cost."],
        ["mission_months", 24, "months", "modeling assumption", "Illustrative operating period."],
        ["operations_cost_usd_per_month", 5000000, "USD/month", "modeling assumption", "Operations and support cost."],
        ["benchmark_cost_usd_per_kg", 3600, "USD/kg", "literature benchmark", "Approximate asteroid-derived propellant delivery cost reported for lunar orbit in Colvin, Crane & Lal (2020)."],
    ]
    with (DATA / "assumptions.csv").open("w", newline="", encoding="utf-8") as f:
        csv.writer(f).writerows(rows)


if __name__ == "__main__":
    write_assumptions()
    write_baseline_results()
    print("Wrote data/assumptions.csv and results/baseline_results.csv")
