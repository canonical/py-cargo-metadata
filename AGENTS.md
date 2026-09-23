# AGENTS.md

Guidance for AI coding agents working in this repository.

## Project

`cargo-metadata` (repo `py-cargo-metadata`): Pydantic models for the JSON
output of `cargo metadata --format-version 1`, plus a thin `run()` wrapper
that invokes the command. Python 3.10+, Pydantic is the only runtime
dependency. Managed with uv (`uv_build` backend, `uv.lock` committed).

## Commands

- Test: `uv run pytest`
- Lint (CI gate): `uv run ruff check .`
- Type check (CI gate): `uv run pyright`
- Update schema snapshot: `uv run pytest --snapshot-update`

## Layout

- `src/cargo_metadata/models.py` — all Pydantic models (`Metadata`,
  `Package`, `Dependency`, `Target`, `Resolve`, `Node`, `Dep`, `DepKind`)
- `src/cargo_metadata/runner.py` — `run(...)`, a keyword-only subprocess
  wrapper over `cargo metadata`
- `tests/snapshots/metadata.schema.json` — JSON schema snapshot of
  `Metadata`
- `tests/test_integration.py` — invokes real `cargo`; skips when `cargo`
  is not on PATH

## Modeling conventions

- Every model uses `extra="allow"`: unknown Cargo fields must parse and be
  preserved. Never change this.
- `use_attribute_docstrings=True`: field docs live in attribute
  docstrings, not `Field(description=...)`. Docstrings become field
  descriptions in the JSON schema, so docstring edits change the snapshot —
  run `--snapshot-update` and include the snapshot diff in the change.
- Non-identifier JSON keys use aliases: e.g. `Target.required_features`
  with `alias="required-features"` and `validate_by_alias=True`.
- Only fields guaranteed by format version 1 are required. Fields Cargo
  added later (or may add) default to `None`/empty collection.
- Package IDs, source IDs (`registry+...`, `git+...`, `sparse+...`), and
  dep-kind/target strings are opaque — type as `str`/`Optional[str]`,
  never parse internals, and expect new enum values within a format
  version.
- `Metadata.resolve` is `None` under `--no-deps`; `Resolve.root` is `None`
  for virtual workspaces.
- Keep `run()` a thin wrapper over exposed cargo flags. No project
  mutation or higher-level analysis APIs (see README scope).

## Cargo metadata reference

- Command docs: https://doc.rust-lang.org/cargo/commands/cargo-metadata.html
- Package ID spec: https://doc.rust-lang.org/cargo/reference/pkgid-spec.html
- Within a format version Cargo may add fields and enum values but will
  not change the meaning of existing fields.

## Changelog and releases

- `CHANGELOG.md` follows Keep a Changelog: record user-visible changes
  under `## [Unreleased]` in the same PR.
- Version lives in `pyproject.toml`; releases are tagged with the bare
  version (e.g. `1.1.0`).
- Publishing goes through `.github/workflows/publish.yml`: `uv build`,
  then trusted publishing to PyPI.

## Git

Do not commit, amend, or push. Stage changes so they can be reviewed; the
maintainer creates every commit.
