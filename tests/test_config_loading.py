from pathlib import Path

from invariance.config.load import load_simulation_config


def test_load_example_config():
    cfg = load_simulation_config(Path("examples/sim.json"))
    assert cfg.grid.nx == 50
    assert cfg.material.alpha > 0