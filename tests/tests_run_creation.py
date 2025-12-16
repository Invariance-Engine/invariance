from pathlib import Path

from invariance.config.sim import SimulationConfig
from invariance.run.create import create_run_directory


def test_create_run_directory(tmp_path: Path):
    config = SimulationConfig(
        grid={"nx": 10, "ny": 10, "dx": 1.0, "dy": 1.0},
        time={"dt": 0.1, "n_steps": 10},
        material={"alpha": 1.0},
        boundary={"type": "dirichlet", "value": 0.0},
        initial_temperature=0.0,
    )

    out = tmp_path / "run"
    create_run_directory(out, config)

    assert (out / "config.json").exists()
    assert (out / "metadata.json").exists()