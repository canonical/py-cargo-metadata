# cargo-metadata

`cargo-metadata` provides Pydantic models for the JSON output of
`cargo metadata --format-version 1`, plus a small runner function that invokes
the command and returns validated data.

## Installation

```bash
pip install cargo-metadata
```

## What it includes

- `Metadata` and related model types (`Package`, `Dependency`, `Target`, `Resolve`, ...)
- `run(...)` helper to execute `cargo metadata` and parse the result

Unknown fields from Cargo are allowed and preserved on parsed model instances,
which helps with forward compatibility when Cargo adds fields. Refer to the
Pydantic documentation for how to interact with unknown fields.

## Quick start

Run `cargo metadata` and parse directly:

```python
from cargo_metadata import run

meta = run(no_deps=True)

print(meta.version)
print(meta.workspace_root)
print([pkg.name for pkg in meta.packages])
```

Parse existing JSON data:

```python
import json
from cargo_metadata import Metadata

data = json.loads(raw_json)
meta = Metadata.model_validate(data)

for pkg in meta.packages:
    print(pkg.name, pkg.version)
```

## Scope

This package focuses on typed parsing and a thin command wrapper.

It does not provide:

- project mutation APIs
- custom Cargo invocation strategies beyond the exposed flags
- higher-level dependency analysis helpers

## Snapshot tests

This repository includes a snapshot test for the Pydantic JSON schema of
`cargo_metadata.Metadata` at `tests/snapshots/metadata.schema.json`.

Run snapshot tests only:

```bash
uv run pytest tests/test_schema_snapshot.py
```

Accept and update snapshots when running tests:

```bash
uv run pytest --snapshot-update
```

When the schema changes, the snapshot diff appears in git, making the change
reviewable.

## Requirements

- Python 3.12+
- `cargo` available on `PATH` when using `run(...)`

All versions of Cargo should work. However, we do not regularly test compatibility
with old versions of Cargo.

## LLM disclosure

LLMs were used to generate code used in this package. All code has been fully
signed off, owned, and tested by the human(s) running the LLM tooling. 
