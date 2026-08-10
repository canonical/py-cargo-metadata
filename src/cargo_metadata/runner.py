import json
import subprocess
from pathlib import Path
from typing import Literal, Optional

from .models import Metadata


def run(
    *,
    manifest_path: Optional[str | Path] = None,
    no_deps: bool = False,
    filter_platform: Optional[str] = None,
    features: Optional[list[str]] = None,
    all_features: bool = False,
    no_default_features: bool = False,
    locked: bool = False,
    frozen: bool = False,
    offline: bool = False,
    format_version: Literal[1] = 1,
) -> Metadata:
    """Invoke `cargo metadata` and return a parsed Metadata object."""
    cmd = ["cargo", "metadata", "--format-version", str(format_version)]
    if manifest_path is not None:
        cmd += ["--manifest-path", str(manifest_path)]
    if no_deps:
        cmd.append("--no-deps")
    if filter_platform is not None:
        cmd += ["--filter-platform", filter_platform]
    if features:
        cmd += ["--features", ",".join(features)]
    if all_features:
        cmd.append("--all-features")
    if no_default_features:
        cmd.append("--no-default-features")
    if locked:
        cmd.append("--locked")
    if frozen:
        cmd.append("--frozen")
    if offline:
        cmd.append("--offline")

    result = subprocess.run(cmd, capture_output=True, text=True, check=True)
    data = json.loads(result.stdout)
    return Metadata.model_validate(data)
