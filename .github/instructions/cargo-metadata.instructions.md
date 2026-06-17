---
applyTo: "**"
---

# cargo metadata — Command Knowledge

## Overview
`cargo metadata` outputs JSON to stdout with machine-readable information about the workspace members and resolved dependencies of the current Rust package. It is commonly used by tools that need to introspect a Cargo project (editors, build systems, linters).

**Reference:** https://doc.rust-lang.org/cargo/commands/cargo-metadata.html

---

## Key Options

| Flag | Description |
|---|---|
| `--format-version 1` | Specify output format version. Always use this for stability; currently only `1` is valid. |
| `--no-deps` | Output only workspace members — skip fetching/resolving dependency info. Omits `resolve` section. |
| `--filter-platform <TRIPLE>` | Narrow the `resolve` output to deps for a specific target triple (e.g. `x86_64-unknown-linux-gnu`). Use `"host-tuple"` as a literal to substitute the current host. Does NOT filter the `packages` array. |
| `-F`/`--features <FEATURES>` | Comma/space-separated features to activate. |
| `--all-features` | Activate all available features. |
| `--no-default-features` | Do not activate the `default` feature. |
| `--manifest-path <PATH>` | Path to `Cargo.toml` (default: search upward from cwd). |
| `--locked` | Require `Cargo.lock` to be up-to-date (good for CI). |
| `--frozen` | Equivalent to `--locked --offline`. |
| `--offline` | Prevent network access; use only locally cached crates. |

---

## JSON Output Structure (format version 1)

```json
{
  "version": 1,
  "workspace_root": "/abs/path/to/workspace",
  "target_directory": "/abs/path/to/workspace/target",
  "workspace_members": ["<PackageID>", ...],
  "workspace_default_members": ["<PackageID>", ...],
  "packages": [ /* PackageObject, ... */ ],
  "resolve": { /* ResolveObject or null */ },
  "metadata": { /* workspace-level [metadata] table or null */ }
}
```

### PackageObject (element of `packages`)
```json
{
  "name": "my-package",
  "version": "0.1.0",
  "id": "file:///path/to/my-package#0.1.0",
  "source": null,                // null for workspace/path deps; "registry+URL", "git+URL", "sparse+URL" otherwise
  "license": "MIT/Apache-2.0",   // or null
  "license_file": "LICENSE",     // or null
  "description": "...",          // or null
  "manifest_path": "/abs/path/to/Cargo.toml",
  "edition": "2018",
  "rust_version": "1.56",        // MSRV, or null
  "authors": ["Jane Doe <user@example.com>"],
  "categories": ["command-line-utilities"],
  "keywords": ["cli"],
  "readme": "README.md",         // or null
  "repository": "https://...",   // or null
  "homepage": "https://...",     // or null
  "documentation": "https://...", // or null
  "default_run": null,
  "links": null,                 // native library name this package links, or null
  "publish": ["crates-io"],      // null = unrestricted; [] = forbidden
  "features": { "default": ["feat1"], "feat1": [], "feat2": [] },
  "metadata": { /* [package.metadata] table or null */ },
  "dependencies": [ /* DependencyObject, ... */ ],
  "targets": [ /* TargetObject, ... */ ]
}
```

### DependencyObject (element of `package.dependencies`)
```json
{
  "name": "bitflags",
  "source": "registry+https://github.com/rust-lang/crates.io-index",
  "req": "^1.0",                 // version requirement; "*" if none
  "kind": null,                  // null = normal; "dev"; "build"
  "rename": null,                // new name if renamed, else null
  "optional": false,
  "uses_default_features": true,
  "features": [],
  "target": "cfg(windows)",      // platform restriction, or null
  "path": "/path/to/dep",        // only present for path deps
  "registry": null               // registry URL or null (null = crates.io)
}
```

### TargetObject (element of `package.targets`)
```json
{
  "name": "my-package",
  "kind": ["bin"],       // "lib","rlib","dylib","proc-macro","bin","example","test","bench","custom-build"
  "crate_types": ["bin"],
  "src_path": "/abs/path/to/main.rs",
  "edition": "2018",
  "required-features": ["feat1"], // absent if none
  "doc": true,
  "doctest": false,
  "test": true
}
```

### ResolveObject
```json
{
  "root": "<PackageID or null>",  // null for virtual workspaces
  "nodes": [
    {
      "id": "<PackageID>",
      "features": ["default"],
      "dependencies": ["<PackageID>", ...],  // simple list
      "deps": [                              // richer list (added in Cargo 1.40)
        {
          "name": "bitflags",               // lib target name (renamed if applicable)
          "pkg": "<PackageID>",
          "dep_kinds": [
            { "kind": null, "target": "cfg(windows)" }
          ]
        }
      ]
    }
  ]
}
```

---

## Package ID Specification
- Path packages: `file:///abs/path/to/pkg#version`
- Registry packages: `https://github.com/rust-lang/crates.io-index#name@version`
- Full spec: https://doc.rust-lang.org/cargo/reference/pkgid-spec.html

## Source ID Formats
- `registry+URL` — standard registry
- `sparse+URL` — sparse registry (HTTP-based)
- `git+URL#<commit-sha>` — git dependency
- `null` — path dependency or workspace member

---

## Compatibility Notes
Within the same format version, Cargo may:
- **Add new fields** (consumers should handle unknown fields gracefully)
- **Add new enum values** for fields like `kind`, `source`
- **Change opaque fields** like source IDs (don't parse their internals)

Cargo will **not** silently change the meaning of existing fields within a version.

---

## Rust Crate
The [`cargo_metadata`](https://crates.io/crates/cargo_metadata) crate on crates.io provides a typed Rust API for consuming this output.
