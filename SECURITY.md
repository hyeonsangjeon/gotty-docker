# Security Policy

GoTTY serves an interactive terminal over HTTP/WebSocket. A misconfigured
deployment is equivalent to handing out a remote shell, so please treat this
image accordingly.

## Reporting a vulnerability

Please **do not** open a public issue for security problems.

- Use GitHub's [private vulnerability reporting](https://github.com/hyeonsangjeon/gotty-docker/security/advisories/new) for this repository, or
- email the maintainer at **wingnut0310@gmail.com** with the details and reproduction steps.

You can expect an acknowledgement within a few days. Once a fix is available we
will credit reporters who want to be named.

Note that this repository packages the upstream
[`sorenisanerd/gotty`](https://github.com/sorenisanerd/gotty) binary. Bugs in
GoTTY itself should also be reported upstream; we will pull in fixed releases.

## Supported versions

Only the latest published image (`modenaf360/gotty-docker:latest` and the
matching `vX.Y.Z-ubuntuNN.NN` tag) receives updates. Pin a digest if you need a
reproducible deployment.

## Hardening checklist

The defaults in this repo are aimed at being safe on `localhost`. Before you
expose the container anywhere else:

- **Always require authentication.** Set `GOTTY_USER` + `GOTTY_PASSWORD` (or
  `GOTTY_CREDENTIAL` / a Docker secret file). The entrypoint prints a warning and
  starts an open terminal only when nothing is configured.
- **Never run Basic Auth over plain HTTP across a network.** Credentials are
  base64, not encrypted. Use the TLS example or, preferably, a reverse proxy
  (Caddy, Traefik, Nginx) terminating HTTPS.
- **Use `GOTTY_PERMIT_WRITE=false`** for dashboards and monitors so viewers cannot
  type into the session.
- **Scope what the shell can reach.** Avoid mounting sensitive host paths or the
  Docker socket, drop capabilities, and consider `--read-only` plus a
  non-privileged `--user` for the container.
- **Limit exposure.** Bind to `127.0.0.1` on the host, put it behind a VPN or
  proxy, and set `GOTTY_MAX_CONNECTION` / `GOTTY_TIMEOUT` to cap abuse.
- **Rotate credentials** and prefer long, randomly generated passwords
  (`openssl rand -base64 24`).

## Image provenance

Images are built from this repository via GitHub Actions and published to Docker
Hub. The Dockerfile verifies the GoTTY release tarball against the upstream
`SHA256SUMS` before installing it.
