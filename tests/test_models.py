from typing import Any

from cargo_metadata import Metadata

MINIMAL_METADATA: dict[str, Any] = {
    "version": 1,
    "workspace_root": "/tmp/myproject",
    "target_directory": "/tmp/myproject/target",
    "workspace_members": ["file:///tmp/myproject#0.1.0"],
    "workspace_default_members": ["file:///tmp/myproject#0.1.0"],
    "packages": [
        {
            "name": "myproject",
            "version": "0.1.0",
            "id": "file:///tmp/myproject#0.1.0",
            "manifest_path": "/tmp/myproject/Cargo.toml",
            "edition": "2021",
            "dependencies": [],
            "targets": [
                {
                    "name": "myproject",
                    "kind": ["lib"],
                    "crate_types": ["lib"],
                    "src_path": "/tmp/myproject/src/lib.rs",
                    "edition": "2021",
                    "doc": True,
                    "doctest": True,
                    "test": True,
                }
            ],
        }
    ],
    "resolve": None,
    "metadata": None,
}


FULL_METADATA: dict[str, Any] = {
    "version": 1,
    "workspace_root": "/workspace/demo",
    "target_directory": "/workspace/demo/target",
    "workspace_members": ["file:///workspace/demo#0.1.0"],
    "workspace_default_members": ["file:///workspace/demo#0.1.0"],
    "packages": [
        {
            "name": "demo",
            "version": "0.1.0",
            "id": "file:///workspace/demo#0.1.0",
            "source": None,
            "license": "MIT OR Apache-2.0",
            "license_file": "LICENSE",
            "description": "Demo package",
            "manifest_path": "/workspace/demo/Cargo.toml",
            "edition": "2021",
            "rust_version": "1.80",
            "authors": ["Jane Doe <jane@example.com>"],
            "categories": ["command-line-utilities"],
            "keywords": ["cargo", "metadata"],
            "readme": "README.md",
            "repository": "https://example.com/repo",
            "homepage": "https://example.com",
            "documentation": "https://docs.example.com",
            "default_run": "demo",
            "links": "demo-native",
            "publish": ["crates-io"],
            "features": {
                "default": ["serde"],
                "serde": [],
                "extras": ["serde"],
            },
            "metadata": {"tool": {"enabled": True}},
            "dependencies": [
                {
                    "name": "serde",
                    "source": "registry+https://github.com/rust-lang/crates.io-index",
                    "req": "^1.0",
                    "kind": None,
                    "rename": None,
                    "optional": False,
                    "uses_default_features": True,
                    "features": ["derive"],
                    "target": None,
                    "path": None,
                    "registry": None,
                },
                {
                    "name": "pytest-dev-dep",
                    "source": None,
                    "req": "*",
                    "kind": "dev",
                    "rename": "renamed-dev",
                    "optional": True,
                    "uses_default_features": False,
                    "features": ["feature-a"],
                    "target": "cfg(test)",
                    "path": "/workspace/dev-dep",
                    "registry": "https://example.com/index",
                },
                {
                    "name": "build-helper",
                    "source": None,
                    "req": "^0.2",
                    "kind": "build",
                    "rename": None,
                    "optional": False,
                    "uses_default_features": True,
                    "features": [],
                    "target": None,
                    "path": "/workspace/build-helper",
                    "registry": None,
                },
            ],
            "targets": [
                {
                    "name": "demo",
                    "kind": ["lib"],
                    "crate_types": ["lib"],
                    "src_path": "/workspace/demo/src/lib.rs",
                    "edition": "2021",
                    "required-features": ["serde"],
                    "doc": True,
                    "doctest": True,
                    "test": True,
                },
                {
                    "name": "demo-bin",
                    "kind": ["bin"],
                    "crate_types": ["bin"],
                    "src_path": "/workspace/demo/src/main.rs",
                    "edition": "2021",
                    "doc": False,
                    "doctest": False,
                    "test": True,
                },
            ],
        }
    ],
    "resolve": {
        "root": "file:///workspace/demo#0.1.0",
        "nodes": [
            {
                "id": "file:///workspace/demo#0.1.0",
                "features": ["default", "serde"],
                "dependencies": [
                    "https://github.com/rust-lang/crates.io-index#serde@1.0.0",
                ],
                "deps": [
                    {
                        "name": "serde",
                        "pkg": "https://github.com/rust-lang/crates.io-index#serde@1.0.0",
                        "dep_kinds": [
                            {"kind": None, "target": None},
                            {"kind": "dev", "target": "cfg(test)"},
                        ],
                    }
                ],
            }
        ],
    },
    "metadata": {"workspace": {"ci": "enabled"}},
}


def test_parse_minimal_metadata() -> None:
    meta = Metadata.model_validate(MINIMAL_METADATA)

    assert meta.version == 1
    assert meta.resolve is None
    assert meta.metadata is None
    assert meta.packages[0].name == "myproject"
    assert meta.packages[0].targets[0].name == "myproject"


def test_parse_full_metadata() -> None:
    meta = Metadata.model_validate(FULL_METADATA)
    pkg = meta.packages[0]

    assert pkg.license == "MIT OR Apache-2.0"
    assert pkg.metadata == {"tool": {"enabled": True}}
    assert pkg.features["default"] == ["serde"]
    assert meta.metadata == {"workspace": {"ci": "enabled"}}


def test_package_with_multiple_targets() -> None:
    meta = Metadata.model_validate(FULL_METADATA)
    targets = meta.packages[0].targets

    assert len(targets) == 2
    assert targets[0].kind == ["lib"]
    assert targets[1].kind == ["bin"]


def test_package_with_dev_and_build_dependencies() -> None:
    meta = Metadata.model_validate(FULL_METADATA)
    deps = meta.packages[0].dependencies

    assert len(deps) == 3
    assert any(dep.kind == "dev" for dep in deps)
    assert any(dep.kind == "build" for dep in deps)


def test_target_required_features_alias_parsing() -> None:
    meta = Metadata.model_validate(FULL_METADATA)
    target = meta.packages[0].targets[0]

    assert target.required_features == ["serde"]


def test_resolve_with_deps_and_dep_kinds() -> None:
    meta = Metadata.model_validate(FULL_METADATA)
    assert meta.resolve is not None

    node = meta.resolve.nodes[0]
    dep = node.deps[0]

    assert node.features == ["default", "serde"]
    assert dep.name == "serde"
    assert dep.dep_kinds[1].kind == "dev"
    assert dep.dep_kinds[1].target == "cfg(test)"


def test_unknown_fields_are_allowed() -> None:
    data: dict[str, Any] = {
        **MINIMAL_METADATA,
        "future-field": {"foo": "bar"},
        "packages": [
            {
                **MINIMAL_METADATA["packages"][0],
                "unknown_package_field": 123,
                "targets": [
                    {
                        **MINIMAL_METADATA["packages"][0]["targets"][0],
                        "unknown_target_field": "ok",
                    }
                ],
            }
        ],
    }

    meta = Metadata.model_validate(data)

    assert getattr(meta, "future-field") == {"foo": "bar"}
    assert getattr(meta.packages[0], "unknown_package_field") == 123
    assert getattr(meta.packages[0].targets[0], "unknown_target_field") == "ok"


def test_metadata_with_resolve_null() -> None:
    meta = Metadata.model_validate(MINIMAL_METADATA)

    assert meta.resolve is None


def test_publish_null_and_empty_list() -> None:
    null_publish_data: dict[str, Any] = {
        **MINIMAL_METADATA,
        "packages": [{**MINIMAL_METADATA["packages"][0], "publish": None}],
    }
    empty_publish_data: dict[str, Any] = {
        **MINIMAL_METADATA,
        "packages": [{**MINIMAL_METADATA["packages"][0], "publish": []}],
    }

    null_publish_meta = Metadata.model_validate(null_publish_data)
    empty_publish_meta = Metadata.model_validate(empty_publish_data)

    assert null_publish_meta.packages[0].publish is None
    assert empty_publish_meta.packages[0].publish == []
