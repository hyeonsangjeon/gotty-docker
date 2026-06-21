# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Community health files: `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, `SECURITY.md`,
  issue/PR templates, and Dependabot configuration.
- Continuous integration workflow that runs hadolint, shellcheck, Compose
  validation, an image build, and a runtime smoke test on every push and PR.
- `.editorconfig` and `.hadolint.yaml` for consistent contributions.
- Expanded README: badges, table of contents, features, reverse-proxy guidance,
  image tags, and a troubleshooting section.
- Makefile convenience targets (`make help`, `lint`, `validate`, `smoke`) that
  mirror the CI checks for a faster local workflow.

### Changed
- Documented the remaining `GOTTY_*` configuration variables in the README,
  including `GOTTY_RANDOM_URL_LENGTH`, `GOTTY_TITLE_FORMAT`, `GOTTY_ADDRESS`, and
  `GOTTY_PORT`.
- Replaced the leftover Java/Eclipse `.gitignore` with one scoped to this
  Docker/shell/Python project.

## [1.8.0] - 2026-06-21

The "revival" release. The project moved from an unmaintained 2016 image to a
modern, multi-architecture build.

### Changed
- Upgraded the base image from Ubuntu `14.04` to Ubuntu `26.04`.
- Replaced the original `yudai/gotty v1.0.1` binary with the maintained
  `sorenisanerd/gotty v1.8.0` fork.
- Reworked the entrypoint to support Basic Auth via `GOTTY_USER` +
  `GOTTY_PASSWORD`, `GOTTY_CREDENTIAL`, or Docker secret files.

### Added
- `linux/amd64` and `linux/arm64` image publishing.
- Checksum verification of the GoTTY release tarball against upstream
  `SHA256SUMS` during build.
- Container `HEALTHCHECK` that treats `200` and `401` as healthy.
- Runnable Compose examples: authenticated shell, read-only monitor, shared
  `tmux`, random URL, and self-signed TLS.
- `Makefile`, `docker-compose.yml`, `.env.example`, and generated README assets.
- GitHub Actions workflow for multi-architecture Docker Hub publishing.

## [1.0.1] - 2016

Original release built on Ubuntu 14.04 with `yudai/gotty`.

[Unreleased]: https://github.com/hyeonsangjeon/gotty-docker/compare/v1.8.0...HEAD
[1.8.0]: https://github.com/hyeonsangjeon/gotty-docker/releases/tag/v1.8.0
[1.0.1]: https://github.com/hyeonsangjeon/gotty-docker
