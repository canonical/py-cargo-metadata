import re
import shutil
import subprocess
from pathlib import Path

import pytest

import cargo_metadata

cargo = shutil.which("cargo")
pytestmark = pytest.mark.skipif(cargo is None, reason="cargo not available")


def test_run_basic(tmp_path: Path) -> None:
    (tmp_path / "Cargo.toml").write_text(
        """
[package]
name = "hello"
version = "0.1.0"
""".lstrip()
    )
    (tmp_path / "src").mkdir()
    (tmp_path / "src" / "lib.rs").write_text("")

    meta = cargo_metadata.run(manifest_path=tmp_path / "Cargo.toml")

    assert meta.version == 1
    assert len(meta.packages) == 1
    pkg = meta.packages[0]
    assert pkg.name == "hello"
    assert pkg.version == "0.1.0"

    cargo_version = subprocess.run(
        ["cargo", "--version"],
        capture_output=True,
        text=True,
        check=True,
    ).stdout.strip()
    version_match = re.match(r"cargo (\d)+\.(\d+)\.(\d+)", cargo_version)
    assert version_match is not None
    minor_version = int(version_match.group(2))

    if minor_version >= 71:
        assert meta.workspace_default_members is not None
