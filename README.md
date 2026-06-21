# GoTTY Docker

[![Docker image](https://img.shields.io/badge/docker-modenaf360%2Fgotty--docker-2496ED?logo=docker&logoColor=white)](https://hub.docker.com/r/modenaf360/gotty-docker)
[![Docker Pulls](https://img.shields.io/docker/pulls/modenaf360/gotty-docker?logo=docker&label=pulls)](https://hub.docker.com/r/modenaf360/gotty-docker)
[![GoTTY](https://img.shields.io/badge/GoTTY-v1.8.0-55cdfc)](https://github.com/sorenisanerd/gotty/releases/tag/v1.8.0)
[![Ubuntu](https://img.shields.io/badge/Ubuntu-26.04-E95420?logo=ubuntu&logoColor=white)](https://hub.docker.com/_/ubuntu)
[![License](https://img.shields.io/github/license/hyeonsangjeon/gotty-docker)](LICENSE)

![GoTTY Docker social preview](assets/social-preview.png)

Run a real Linux terminal in your browser with Docker. This repo revives the old GoTTY Docker image with a modern base image, a maintained GoTTY fork, Basic Auth helpers, Compose examples, and multi-architecture publishing.

![GoTTY Docker demo](assets/demo.gif)

## What's New

- Ubuntu base upgraded from `14.04` to `26.04`.
- GoTTY upgraded from the original `yudai/gotty v1.0.1` release to the maintained `sorenisanerd/gotty v1.8.0`.
- `linux/amd64` and `linux/arm64` image publishing support.
- Basic Auth can be configured with `GOTTY_USER` + `GOTTY_PASSWORD`, `GOTTY_CREDENTIAL`, or Docker secret files.
- Runnable examples for the common GoTTY patterns: authenticated shell, read-only monitor, shared `tmux`, random URL, and TLS.

## Quick Start

```console
export GOTTY_PASSWORD="$(openssl rand -base64 24)"
echo "GoTTY password: ${GOTTY_PASSWORD}"

docker run --rm -it \
  -p 8989:8080 \
  -e GOTTY_USER=gotty \
  -e GOTTY_PASSWORD="${GOTTY_PASSWORD}" \
  modenaf360/gotty-docker:latest
```

Open <http://localhost:8989> and sign in as `gotty`.

With Compose:

```console
cp .env.example .env
$EDITOR .env
docker compose up --build
```

## Common Samples

All samples live in [`examples/`](examples/README.md) and run from the repository root.

| Use case | Command | Port |
| --- | --- | --- |
| Authenticated writable shell | `GOTTY_PASSWORD=secret docker compose -f examples/basic-auth-shell.compose.yml up --build` | `8989` |
| Read-only `top` dashboard | `docker compose -f examples/read-only-monitor.compose.yml up --build` | `8990` |
| Shared `tmux` session | `GOTTY_PASSWORD=secret docker compose -f examples/tmux-shared-session.compose.yml up --build` | `8991` |
| Random URL | `GOTTY_PASSWORD=secret docker compose -f examples/random-url.compose.yml up --build` | `8992` |
| Self-signed TLS | `./examples/make-self-signed-cert.sh && GOTTY_PASSWORD=secret docker compose -f examples/tls-self-signed.compose.yml up --build` | `8993` |

## Configuration

| Variable | Default | Description |
| --- | --- | --- |
| `GOTTY_USER` | unset | Username used to build `user:password` Basic Auth credentials. |
| `GOTTY_PASSWORD` | unset | Password paired with `GOTTY_USER`. |
| `GOTTY_CREDENTIAL` | unset | Direct GoTTY credential string, for example `alice:correct-horse-battery-staple`. Takes precedence over `GOTTY_USER` and `GOTTY_PASSWORD`. |
| `GOTTY_CREDENTIAL_FILE` | unset | File containing a `user:password` credential, useful with Docker secrets. |
| `GOTTY_PASSWORD_FILE` | unset | File containing only the password for `GOTTY_USER`. |
| `GOTTY_COMMAND` | `/bin/bash -l` | Command GoTTY starts for each connection. |
| `GOTTY_PERMIT_WRITE` | `true` | Allows browser clients to type into the terminal. Set to `false` for dashboards. |
| `GOTTY_RECONNECT` | `true` | Enables browser reconnect behavior. |
| `GOTTY_RANDOM_URL` | unset | Set to `true` to generate a non-root URL path. |
| `GOTTY_TLS` | unset | Set to `true` to enable GoTTY TLS directly. |

GoTTY also reads its own `GOTTY_*` environment variables, including `GOTTY_MAX_CONNECTION`, `GOTTY_ONCE`, `GOTTY_TIMEOUT`, `GOTTY_TITLE_FORMAT`, `GOTTY_TLS_CRT`, and `GOTTY_TLS_KEY`.

## Security Notes

GoTTY exposes a terminal. Treat it like shell access.

- Never publish a writable shell without authentication.
- Basic Auth over plain HTTP is not encrypted. Use TLS or put GoTTY behind a reverse proxy when exposing it beyond localhost.
- Prefer `GOTTY_PERMIT_WRITE=false` for monitoring views.
- Use `tmux` for shared sessions so reconnects and multiple clients attach to the same process.
- Avoid mounting sensitive host paths or the Docker socket unless you explicitly want that level of control from the browser.

## Build

```console
make build
```

This tags:

- `modenaf360/gotty-docker:latest`
- `modenaf360/gotty-docker:v1.8.0-ubuntu26.04`
- `modenaf360/gotty:latest`
- `modenaf360/gotty:v1.8.0-ubuntu26.04`

## Publish

```console
docker login
make push
```

`make push` publishes multi-architecture images for `linux/amd64` and `linux/arm64`, including the legacy `modenaf360/gotty` alias used by the old README.

GitHub Actions can publish the same image on `master`, tags, or manual dispatch. Add these repository secrets first:

- `DOCKERHUB_USERNAME`
- `DOCKERHUB_TOKEN`

If those secrets are not configured, the workflow skips publishing instead of failing the build.

## Assets

The README GIF and social preview are generated, not hand-edited:

```console
python3 scripts/render_assets.py
```

Use [`assets/social-preview.png`](assets/social-preview.png) as the GitHub repository social preview image.

## References

- [sorenisanerd/gotty](https://github.com/sorenisanerd/gotty)
- [Original yudai/gotty](https://github.com/yudai/gotty)
- [Ubuntu official Docker image](https://hub.docker.com/_/ubuntu)
- [Docker Hub: modenaf360/gotty-docker](https://hub.docker.com/r/modenaf360/gotty-docker)
