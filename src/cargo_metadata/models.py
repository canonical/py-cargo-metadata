from typing import Any, Literal, Optional

from pydantic import BaseModel, Field


class Dependency(BaseModel, extra="allow", use_attribute_docstrings=True):
    """A dependency entry from `package.dependencies` in cargo metadata output.

    Mirrors Cargo's `DependencyObject` for format version 1.
    """

    name: str
    """Dependency package name as declared in Cargo metadata."""
    source: Optional[str] = None
    """Source identifier, or null for path/workspace dependencies."""
    req: str
    """Version requirement string such as `^1.0` or `*`."""
    kind: Optional[str] = None
    """Dependency kind: null for normal, or `dev`/`build`."""
    rename: Optional[str] = None
    """Renamed crate name used in Cargo.toml, if present."""
    optional: bool
    """Whether this dependency is optional."""
    uses_default_features: bool
    """Whether default features of this dependency are enabled."""
    features: list[str] = Field(default_factory=list)
    """Explicitly enabled feature names for this dependency."""
    target: Optional[str] = None
    """Target cfg expression restricting this dependency, if present."""
    path: Optional[str] = None
    """Filesystem path for path dependencies, when present."""
    registry: Optional[str] = None
    """Registry URL for registry dependencies, if explicitly set."""


class Target(
    BaseModel,
    extra="allow",
    validate_by_alias=True,
    use_attribute_docstrings=True,
):
    """A target entry from `package.targets` in cargo metadata output.

    Mirrors Cargo's `TargetObject` for format version 1.
    """

    name: str
    """Target name as reported by Cargo."""
    kind: list[str]
    """Target kinds such as `lib`, `bin`, `example`, `test`, or `bench`."""
    crate_types: list[str] = Field(default_factory=list)
    """Rust crate types emitted for this target, such as `bin` or `rlib`."""
    src_path: str
    """Absolute source path to the target root file."""
    edition: str
    """Rust edition used by this target."""
    required_features: list[str] = Field(default_factory=list, alias="required-features")
    """Feature names required for this target to build."""
    doc: bool = True
    """Whether docs are built for this target."""
    doctest: bool = True
    """Whether doctests are enabled for this target."""
    test: bool = True
    """Whether this target participates in test builds."""


class Package(BaseModel, extra="allow", use_attribute_docstrings=True):
    """A package entry from the top-level `packages` array.

    Mirrors Cargo's `PackageObject` for format version 1.
    """

    name: str
    """Cargo package name."""
    version: str
    """Package semantic version string."""
    id: str
    """Opaque Cargo package ID specification string."""
    source: Optional[str] = None
    """Package source identifier, or null for path/workspace packages."""
    license: Optional[str] = None
    """License expression from Cargo.toml."""
    license_file: Optional[str] = None
    """License file path, if configured."""
    description: Optional[str] = None
    """Package description text."""
    manifest_path: str
    """Absolute path to the package Cargo.toml."""
    edition: str
    """Rust edition declared for the package."""
    rust_version: Optional[str] = None
    """Minimum supported Rust version, if set."""
    authors: list[str] = Field(default_factory=list)
    """Author strings from Cargo metadata."""
    categories: list[str] = Field(default_factory=list)
    """crates.io categories for the package."""
    keywords: list[str] = Field(default_factory=list)
    """crates.io keywords for the package."""
    readme: Optional[str] = None
    """Readme file path or identifier, if set."""
    repository: Optional[str] = None
    """Repository URL, if present."""
    homepage: Optional[str] = None
    """Homepage URL, if present."""
    documentation: Optional[str] = None
    """Documentation URL, if present."""
    default_run: Optional[str] = None
    """Default binary target name for `cargo run`, if set."""
    links: Optional[str] = None
    """Native library name linked by this package when using a `links` key."""
    publish: Optional[list[str]] = None
    """Allowed registries for publishing; empty list means publishing is forbidden."""
    features: dict[str, list[str]] = Field(default_factory=dict)
    """Feature map from feature name to enabled feature/dependency entries."""
    metadata: Optional[dict[str, Any]] = None
    """Raw `[package.metadata]` table contents, if present."""
    dependencies: list[Dependency] = Field(default_factory=list[Dependency])
    """Dependencies declared by this package."""
    targets: list[Target] = Field(default_factory=list[Target])
    """Build targets produced by this package."""


class DepKind(BaseModel, extra="allow", use_attribute_docstrings=True):
    """A dependency-kind selector from `resolve.nodes[].deps[].dep_kinds`.

    Captures the dependency kind and optional target filter used in graph resolution.
    """

    kind: Optional[str] = None
    """Dependency kind: null for normal, or `dev`/`build`."""
    target: Optional[str] = None
    """Optional target cfg expression for this dependency kind."""


class Dep(BaseModel, extra="allow", use_attribute_docstrings=True):
    """A resolved dependency edge entry from `resolve.nodes[].deps`.

    Represents one named edge and its package target in Cargo's resolved graph.
    """

    name: str
    """Dependency library name as used by the package."""
    pkg: str
    """Resolved package ID of the dependency target."""
    dep_kinds: list[DepKind] = Field(default_factory=list[DepKind])
    """Dependency-kind variants associated with this edge."""


class Node(BaseModel, extra="allow", use_attribute_docstrings=True):
    """A node entry from `resolve.nodes` in the resolved dependency graph."""

    id: str
    """Package ID for this resolved graph node."""
    features: list[str] = Field(default_factory=list)
    """Activated features for this package in the resolve graph."""
    dependencies: list[str] = Field(default_factory=list)
    """Resolved dependency package IDs in simple edge form."""
    deps: list[Dep] = Field(default_factory=list[Dep])
    """Resolved dependency edges with names and dependency kinds."""


class Resolve(BaseModel, extra="allow", use_attribute_docstrings=True):
    """The top-level resolve graph from cargo metadata output.

    This section may be null when `--no-deps` is used.
    """

    root: Optional[str] = None
    """Package ID of the workspace root package, or null for virtual workspaces."""
    nodes: list[Node] = Field(default_factory=list[Node])
    """Resolved dependency graph nodes."""


class Metadata(BaseModel, extra="allow", use_attribute_docstrings=True):
    """Top-level `cargo metadata --format-version 1` document.

    This model captures workspace-level package and resolve information emitted by Cargo.
    """

    version: Literal[1]
    """Cargo metadata format version (currently fixed to 1)."""
    workspace_root: str
    """Absolute path to the Cargo workspace root."""
    target_directory: str
    """Absolute path to Cargo's target directory."""
    workspace_members: list[str]
    """Package IDs for all workspace members."""
    workspace_default_members: list[str]
    """Package IDs selected as default workspace members."""
    packages: list[Package]
    """All packages included in metadata output."""
    resolve: Optional[Resolve] = None
    """Resolved dependency graph section; null when dependency resolution is omitted."""
    metadata: Optional[dict[str, Any]] = None
    """Workspace-level `[metadata]` table contents, if present."""

