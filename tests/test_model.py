from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from model import ModelInputs, run_model


def test_baseline_mass_balance():
    out = run_model(ModelInputs())
    assert abs(out["recovered_resource_t"] - 380.0) < 1e-9


def test_baseline_cost():
    out = run_model(ModelInputs())
    assert abs(out["total_cost_usd"] - 2_070_000_000.0) < 1e-6


def test_breakeven_price():
    out = run_model(ModelInputs())
    assert abs(out["break_even_price_usd_per_kg"] - 5447.368421052632) < 1e-6
