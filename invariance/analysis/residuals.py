from __future__ import annotations

import numpy as np
import pandas as pd


def sample_simulation_at_sensors(
    T: np.ndarray,
    sensors: pd.DataFrame,
    dt: float,
) -> pd.DataFrame:
    """
    Sample simulation temperature field at sensor locations and times.

    T: shape (n_steps+1, nx, ny)
    """
    step_indices = (sensors["t"] / dt).round().astype(int)
    step_indices = step_indices.clip(0, T.shape[0] - 1)

    predicted = T[
        step_indices,
        sensors["i"].to_numpy(),
        sensors["j"].to_numpy(),
    ]

    df = sensors.copy()
    df["predicted_temperature"] = predicted
    df["residual"] = predicted - df["temperature"]

    return df

def compute_error_metrics(df: pd.DataFrame) -> dict:
    r = df["residual"].to_numpy()

    return {
        "rmse": float(np.sqrt((r**2).mean())),
        "mae": float(np.abs(r).mean()),
        "max_error": float(np.abs(r).max()),
        "n_measurements": int(len(df)),
    }