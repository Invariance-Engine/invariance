# Invariance

CLI-first tooling for physics calibration and fast simulation.  
V0 starts with thermal diffusion workflows.

## Development

Install dependencies:
```bash
uv venv
uv sync

## Run the CLI:
uv run invariance --help
uv run invariance version

## Run tests:
uv run pytest

## Lint:
uv run ruff check .
uv run ruff format .