from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path

from invariance import __version__
from invariance.config.sim import SimulationConfig


def create_run_directory(
    out_dir: Path,
    config: SimulationConfig,
) -> None:
    out_dir.mkdir(parents=True, exist_ok=False)

    # Write exact config used
    with (out_dir / "config.json").open("w") as f:
        json.dump(config.model_dump(), f, indent=2)

    # Metadata
    metadata = {
        "created_at": datetime.now(tz=UTC).isoformat(),
        "invariance_version": __version__,
    }

    with (out_dir / "metadata.json").open("w") as f:
        json.dump(metadata, f, indent=2)

    # Placeholder metrics
    with (out_dir / "metrics.json").open("w") as f:
        json.dump({}, f, indent=2)
        
def write_manifest(out_dir, command: str, args: dict):
    import json
    from datetime import datetime, timezone

    manifest = {
        "command": command,
        "args": args,
        "created_at": datetime.now(tz=timezone.utc).isoformat(),
    }

    with (out_dir / "manifest.json").open("w") as f:
        json.dump(manifest, f, indent=2)