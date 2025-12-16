import numpy as np

from invariance.physics.heat2d import compute_stability_dt, simulate_heat_2d


def test_stability_dt_positive():
    dt = compute_stability_dt(alpha=1.0, dx=1.0, dy=1.0)
    assert dt > 0


def test_heat_diffusion_smooths_field():
    T = simulate_heat_2d(
        nx=10,
        ny=10,
        dx=1.0,
        dy=1.0,
        dt=0.01,
        n_steps=10,
        alpha=1.0,
        initial_temperature=100.0,
        boundary_value=0.0,
    )

    assert T[-1].max() < 100.0
    assert T[-1].min() >= 0.0