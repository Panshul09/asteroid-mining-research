from __future__ import annotations

from pathlib import Path
import csv

import matplotlib.pyplot as plt
import numpy as np

from model import ModelInputs, run_model

ROOT = Path(__file__).resolve().parents[1]
FIG = ROOT / "figures"
FIG.mkdir(exist_ok=True)

BASE = ModelInputs()
RESULTS = ROOT / "results"
RESULTS.mkdir(exist_ok=True)


def write_csv(filename, header, rows):
    with (RESULTS / filename).open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(rows)


def save(fig, name: str) -> None:
    fig.tight_layout()
    fig.savefig(FIG / name, dpi=220, bbox_inches="tight")
    plt.close(fig)


def figure_1_throughput() -> None:
    throughputs = np.linspace(500, 15000, 100)
    concentrations = [0.05, 0.10, 0.15, 0.20]

    fig, ax = plt.subplots(figsize=(8.2, 5.1))
    csv_rows = []
    for c in concentrations:
        vals = []
        for t in throughputs:
            x = ModelInputs(feedstock_t=float(t), resource_fraction=c)
            price = run_model(x)["break_even_price_usd_per_kg"]
            vals.append(price)
            csv_rows.append([float(t), c, price])
        ax.plot(throughputs, vals, label=f"Resource fraction = {c:.0%}")
    write_csv("throughput_sensitivity.csv", ["feedstock_t", "resource_fraction", "breakeven_price_usd_per_kg"], csv_rows)
    ax.axhline(BASE.benchmark_cost_usd_per_kg, linestyle="--", label="Literature benchmark: $3,600/kg")
    ax.set_xlabel("Feedstock processed per mission (tonnes)")
    ax.set_ylabel("Break-even price (USD/kg)")
    ax.set_title("Break-even price falls as mission throughput increases")
    ax.grid(alpha=0.25)
    ax.legend()
    save(fig, "figure1_throughput_vs_breakeven.png")


def figure_2_heatmap() -> None:
    concentrations = np.linspace(0.02, 0.20, 19)
    recoveries = np.linspace(0.40, 0.95, 19)
    z = np.zeros((len(recoveries), len(concentrations)))

    for i, r in enumerate(recoveries):
        for j, c in enumerate(concentrations):
            x = ModelInputs(resource_fraction=float(c), extraction_efficiency=float(r))
            z[i, j] = run_model(x)["break_even_price_usd_per_kg"]

    grid_rows = []
    for i, r in enumerate(recoveries):
        for j, c in enumerate(concentrations):
            grid_rows.append([c, r, z[i, j]])
    write_csv("concentration_recovery_grid.csv", ["resource_fraction", "extraction_efficiency", "breakeven_price_usd_per_kg"], grid_rows)

    fig, ax = plt.subplots(figsize=(8.0, 5.5))
    im = ax.imshow(
        z,
        origin="lower",
        aspect="auto",
        extent=[concentrations.min() * 100, concentrations.max() * 100, recoveries.min() * 100, recoveries.max() * 100],
    )
    cbar = fig.colorbar(im, ax=ax)
    cbar.set_label("Break-even price (USD/kg)")
    ax.set_xlabel("Resource fraction in feedstock (%)")
    ax.set_ylabel("Extraction efficiency (%)")
    ax.set_title("Break-even price is highly sensitive to resource recovery")
    save(fig, "figure2_concentration_recovery_heatmap.png")


def figure_3_sensitivity() -> None:
    baseline_price = run_model(BASE)["break_even_price_usd_per_kg"]
    factors = {
        "Feedstock throughput": "feedstock_t",
        "Resource fraction": "resource_fraction",
        "Extraction efficiency": "extraction_efficiency",
        "Delivery efficiency": "delivery_efficiency",
        "Fixed cost": "fixed_cost_usd",
        "Variable cost/tonne": "variable_cost_usd_per_t",
        "Operating cost/month": "operations_cost_usd_per_month",
        "Mission duration": "mission_months",
    }

    rows = []
    for label, attr in factors.items():
        current = getattr(BASE, attr)
        low = current * 0.80
        high = current * 1.20
        if attr in {"resource_fraction", "extraction_efficiency", "delivery_efficiency"}:
            high = min(high, 0.99)
        low_inputs = BASE.__class__(**{**BASE.__dict__, attr: low})
        high_inputs = BASE.__class__(**{**BASE.__dict__, attr: high})
        low_price = run_model(low_inputs)["break_even_price_usd_per_kg"]
        high_price = run_model(high_inputs)["break_even_price_usd_per_kg"]
        rows.append((label, low_price - baseline_price, high_price - baseline_price))

    rows.sort(key=lambda x: abs(x[2] - x[1]), reverse=True)
    write_csv("local_sensitivity.csv", ["parameter", "minus_20pct_change_usd_per_kg", "plus_20pct_change_usd_per_kg"], rows)
    labels = [r[0] for r in rows]
    low_vals = [r[1] for r in rows]
    high_vals = [r[2] for r in rows]

    fig, ax = plt.subplots(figsize=(8.5, 5.7))
    y = np.arange(len(labels))
    h = 0.34
    ax.barh(y - h / 2, low_vals, height=h, label="-20% input")
    ax.barh(y + h / 2, high_vals, height=h, label="+20% input")
    ax.axvline(0, linewidth=1)
    ax.set_yticks(y)
    ax.set_yticklabels(labels)
    ax.invert_yaxis()
    ax.set_xlabel("Change in break-even price relative to baseline (USD/kg)")
    ax.set_title("Sensitivity of the model to a 20% change in each input")
    ax.grid(axis="x", alpha=0.25)
    ax.legend()
    save(fig, "figure3_sensitivity_tornado.png")


def figure_4_fixed_cost() -> None:
    fixed_costs = np.linspace(0.25e9, 2.5e9, 100)
    vals = []
    for cost in fixed_costs:
        x = ModelInputs(fixed_cost_usd=float(cost))
        vals.append(run_model(x)["break_even_price_usd_per_kg"])

    write_csv("fixed_cost_sensitivity.csv", ["fixed_cost_usd", "breakeven_price_usd_per_kg"], [[float(c), float(v)] for c, v in zip(fixed_costs, vals)])

    fig, ax = plt.subplots(figsize=(8.2, 5.1))
    ax.plot(fixed_costs / 1e9, vals)
    ax.axhline(BASE.benchmark_cost_usd_per_kg, linestyle="--", label="Literature benchmark: $3,600/kg")
    ax.set_xlabel("Fixed mission/development cost (USD billions)")
    ax.set_ylabel("Break-even price (USD/kg)")
    ax.set_title("Higher up-front cost raises the required resource price")
    ax.grid(alpha=0.25)
    ax.legend()
    save(fig, "figure4_fixed_cost_vs_breakeven.png")


def main() -> None:
    figure_1_throughput()
    figure_2_heatmap()
    figure_3_sensitivity()
    figure_4_fixed_cost()
    print("Generated four figures in figures/")


if __name__ == "__main__":
    main()
