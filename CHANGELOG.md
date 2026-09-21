# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

* Expand package metadata: add `keywords`, classifiers for the full supported
  Python version range and OS independence, and `Homepage`/`Changelog` URLs
* Internal development workflow improvements

## [1.1.0]

* Relax the `manifest_path` argument of `run()`'s typing to accept `PurePath`
* Add convenience accessor methods to `Metadata`
  * `root_package()`
  * `workspace_packages()`
  * `workspace_default_packages()`

## [1.0.0]

Initial release.

[Unreleased]: https://github.com/canonical/py-cargo-metadata/compare/1.1.0...HEAD
[1.1.0]: https://github.com/canonical/py-cargo-metadata/compare/1.0.0...1.1.0
[1.0.0]: https://github.com/canonical/py-cargo-metadata/releases/tag/1.0.0
