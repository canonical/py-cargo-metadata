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
which helps with forward compatibility when Cargo adds fields.

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

## Runner options

`run(...)` exposes common `cargo metadata` flags:

- `manifest_path`
- `no_deps`
- `filter_platform`
- `features`
- `all_features`
- `no_default_features`
- `locked`
- `frozen`
- `offline`

## Scope

This package focuses on typed parsing and a thin command wrapper.

It does not provide:

- project mutation APIs
- custom Cargo invocation strategies beyond the exposed flags
- higher-level dependency analysis helpers

## Requirements

- Python 3.12+
- `cargo` available on `PATH` when using `run(...)`
