from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Dict


@dataclass(frozen=True)
class ModelInputs:
    """Baseline inputs for the scenario model.

    These are modeling assumptions, not measured properties of a real mission.
    """

    feedstock_t: float = 5000.0
    resource_fraction: float = 0.10
    extraction_efficiency: float = 0.80
    delivery_efficiency: float = 0.95
    fixed_cost_usd: float = 1_200_000_000.0
    variable_cost_usd_per_t: float = 150_000.0
    mission_months: float = 24.0
    operations_cost_usd_per_month: float = 5_000_000.0
    benchmark_cost_usd_per_kg: float = 3600.0


def validate_inputs(x: ModelInputs) -> None:
    if x.feedstock_t <= 0:
        raise ValueError("feedstock_t must be positive")
    for name in ("resource_fraction", "extraction_efficiency", "delivery_efficiency"):
        value = getattr(x, name)
        if not 0 < value <= 1:
            raise ValueError(f"{name} must be in (0, 1]")
    if x.fixed_cost_usd < 0 or x.variable_cost_usd_per_t < 0:
        raise ValueError("costs must be non-negative")
    if x.mission_months < 0 or x.operations_cost_usd_per_month < 0:
        raise ValueError("operations inputs must be non-negative")
    if x.benchmark_cost_usd_per_kg <= 0:
        raise ValueError("benchmark_cost_usd_per_kg must be positive")


def run_model(x: ModelInputs) -> Dict[str, float]:
    validate_inputs(x)

    recovered_t = (
        x.feedstock_t
        * x.resource_fraction
        * x.extraction_efficiency
        * x.delivery_efficiency
    )
    recovered_kg = recovered_t * 1000.0

    variable_cost = x.feedstock_t * x.variable_cost_usd_per_t
    operations_cost = x.mission_months * x.operations_cost_usd_per_month
    total_cost = x.fixed_cost_usd + variable_cost + operations_cost
    break_even_price = total_cost / recovered_kg

    benchmark_gap = break_even_price / x.benchmark_cost_usd_per_kg
    return {
        "feedstock_t": x.feedstock_t,
        "recovered_resource_t": recovered_t,
        "recovered_resource_kg": recovered_kg,
        "fixed_cost_usd": x.fixed_cost_usd,
        "variable_cost_usd": variable_cost,
        "operations_cost_usd": operations_cost,
        "total_cost_usd": total_cost,
        "break_even_price_usd_per_kg": break_even_price,
        "benchmark_cost_usd_per_kg": x.benchmark_cost_usd_per_kg,
        "break_even_to_benchmark_ratio": benchmark_gap,
    }


def as_dict(x: ModelInputs) -> Dict[str, float]:
    return asdict(x)
