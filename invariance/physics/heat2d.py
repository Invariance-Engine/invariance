from __future__ import annotations

import numpy as np


def compute_stability_dt(alpha: float, dx: float, dy: float) -> float:
    """
    Compute maximum stable dt for explicit 2D heat equation.
    """
    return 1.0 / (2.0 * alpha * (1.0 / dx**2 + 1.0 / dy**2))


def simulate_heat_2d(
    nx: int,
    ny: int,
    dx: float,
    dy: float,
    dt: float,
    n_steps: int,
    alpha: float,
    initial_temperature: float,
    boundary_value: float,
) -> np.ndarray:
    """
    Run an explicit finite-difference simulation of the 2D heat equation.

    Returns:
        T: array of shape (n_steps + 1, nx, ny)
    """
    # Initialize temperature field
    T = np.full((n_steps + 1, nx, ny), initial_temperature, dtype=np.float64)

    # Apply boundary conditions at t=0
    T[0, 0, :] = boundary_value
    T[0, -1, :] = boundary_value
    T[0, :, 0] = boundary_value
    T[0, :, -1] = boundary_value

    cx = alpha * dt / dx**2
    cy = alpha * dt / dy**2

    for n in range(n_steps):
        Tn = T[n]

        # Update interior points
        T[n + 1, 1:-1, 1:-1] = (
            Tn[1:-1, 1:-1]
            + cx * (Tn[2:, 1:-1] - 2.0 * Tn[1:-1, 1:-1] + Tn[:-2, 1:-1])
            + cy * (Tn[1:-1, 2:] - 2.0 * Tn[1:-1, 1:-1] + Tn[1:-1, :-2])
        )

        # Re-apply boundary conditions
        T[n + 1, 0, :] = boundary_value
        T[n + 1, -1, :] = boundary_value
        T[n + 1, :, 0] = boundary_value
        T[n + 1, :, -1] = boundary_value

    return T