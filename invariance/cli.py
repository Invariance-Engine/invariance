from __future__ import annotations

from pathlib import Path
from typing import Annotated

import typer
from pydantic import ValidationError
from rich import print

from invariance import __version__
from invariance.config.load import load_simulation_config
from invariance.run.create import create_run_directory
from invariance.physics.heat2d import compute_stability_dt, simulate_heat_2d

import json
import numpy as np

app = typer.Typer(
    name="invariance",
    help="Invariance: auto-calibrated physics (starting with thermal diffusion).",
)


@app.callback(invoke_without_command=True)
def main_callback(ctx: typer.Context) -> None:
    """
    Invariance CLI entrypoint.
    """
    if ctx.invoked_subcommand is None:
        # If no subcommand is provided, show help.
        print(ctx.get_help())


@app.command()
def version() -> None:
    """
    Print the installed Invariance version.
    """
    print(f"[bold]invariance[/bold] v{__version__}")


# @app.command()
# def simulate(
#     config: Annotated[
#         Path,
#         typer.Option(
#             "--config",
#             "-c",
#             exists=True,
#             file_okay=True,
#             dir_okay=False,
#             readable=True,
#             help="Path to simulation config JSON file",
#         ),
#     ],
#     out: Annotated[
#         Path,
#         typer.Option(
#             "--out",
#             "-o",
#             help="Output directory for run artifacts",
#         ),
#     ],
# ) -> None:
#     """
#     Validate a simulation config and create a run directory.
#     (Physics comes in the next milestone.)
#     """
#     try:
#         sim_config = load_simulation_config(config)
#     except ValidationError as e:
#         typer.echo("Error: Validation failed for simulation config", err=True)
#         typer.echo(e, err=True)
#         raise typer.Exit(code=1) from e

#     try:
#         create_run_directory(out, sim_config)
#     except FileExistsError as e:
#         typer.echo(f"Error: Output directory already exists: {out}", err=True)
#         raise typer.Exit(code=1) from e


#     typer.echo(f"✔ Loaded simulation config from {config}")
#     typer.echo(f"✔ Created run directory: {out}")
@app.command()
def simulate(
    config: Annotated[
        Path,
        typer.Option(
            "--config",
            "-c",
            exists=True,
            file_okay=True,
            dir_okay=False,
            readable=True,
            help="Path to simulation config JSON file",
        ),
    ],
    out: Annotated[
        Path,
        typer.Option(
            "--out",
            "-o",
            help="Output directory for run artifacts",
        ),
    ],
) -> None:
    """
    Run a 2D heat diffusion simulation and write results to disk.
    """
    # 1. Load + validate config
    try:
        sim_config = load_simulation_config(config)
    except ValidationError as e:
        typer.echo("Error: Validation failed for simulation config", err=True)
        typer.echo(e, err=True)
        raise typer.Exit(code=1) from e

    # 2. Enforce stability (NEW — must be before writing anything)
    dt_max = compute_stability_dt(
        alpha=sim_config.material.alpha,
        dx=sim_config.grid.dx,
        dy=sim_config.grid.dy,
    )

    if sim_config.time.dt > dt_max:
        typer.echo(
            (
                "Error: Time step is unstable for explicit heat solver\n"
                f"  dt      = {sim_config.time.dt:.3e}\n"
                f"  dt_max  = {dt_max:.3e}"
            ),
            err=True,
        )
        raise typer.Exit(code=1)

    # 3. Create run directory
    try:
        create_run_directory(out, sim_config)
    except FileExistsError as e:
        typer.echo(f"Error: Output directory already exists: {out}", err=True)
        raise typer.Exit(code=1) from e

    typer.echo(f"✔ Loaded simulation config from {config}")
    typer.echo(f"✔ Created run directory: {out}")

    # 4. Run heat simulation
    T = simulate_heat_2d(
        nx=sim_config.grid.nx,
        ny=sim_config.grid.ny,
        dx=sim_config.grid.dx,
        dy=sim_config.grid.dy,
        dt=sim_config.time.dt,
        n_steps=sim_config.time.n_steps,
        alpha=sim_config.material.alpha,
        initial_temperature=sim_config.initial_temperature,
        boundary_value=sim_config.boundary.value,
    )

    # 5. Write outputs

    np.save(out / "field.npy", T[-1])
    np.save(out / "history.npy", T)

    metrics = {
        "t_final": sim_config.time.dt * sim_config.time.n_steps,
        "min_temperature": float(T[-1].min()),
        "max_temperature": float(T[-1].max()),
        "dt_max_stable": dt_max,
    }

    with (out / "metrics.json").open("w") as f:
        json.dump(metrics, f, indent=2)

    # 6. Done
    typer.echo("✔ Heat simulation completed")


def main() -> None:
    app()
