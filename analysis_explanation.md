# What the analysis is doing

The model is intentionally simple and reproducible.

## Equations

Delivered resource mass:

`M_delivered = M_feedstock x resource_fraction x extraction_efficiency x delivery_efficiency`

Total modeled cost:

`C_total = fixed_cost + (feedstock x variable_cost_per_t) + (mission_months x operations_cost_per_month)`

Break-even resource price:

`P_break_even = C_total / M_delivered`

## Why this analysis is useful

The research literature identifies throughput, spacecraft/mission cost, resource price, and mission architecture as important drivers of asteroid-mining economics. The model tests related relationships in a simpler student-scale framework.

The output is a break-even requirement, not a forecast of a future commodity price. The model can be made more realistic later by replacing scenario assumptions with source-backed estimates and adding trajectory, propulsion, financing, and uncertainty models.
