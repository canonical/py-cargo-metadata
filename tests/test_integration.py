import shutil
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
edition = "2021"
""".lstrip()
    )
    (tmp_path / "src").mkdir()
    (tmp_path / "src" / "lib.rs").write_text("")

    meta = cargo_metadata.run(manifest_path=tmp_path / "Cargo.toml", no_deps=True)

    assert meta.version == 1
    assert len(meta.packages) == 1
    pkg = meta.packages[0]
    assert pkg.name == "hello"
    assert pkg.version == "0.1.0"
    assert meta.resolve is None
