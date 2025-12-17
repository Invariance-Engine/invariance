from __future__ import annotations

import numpy as np

DEFAULT_SEED = 42


def set_deterministic(seed: int = DEFAULT_SEED) -> None:
    np.random.seed(seed)