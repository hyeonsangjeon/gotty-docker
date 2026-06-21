# GoTTY Docker Examples

Each sample can be run from the repository root with Docker Compose.

## 1. Authenticated Writable Shell

The default production shape: a writable Bash session protected by Basic Auth.

```console
export GOTTY_PASSWORD="$(openssl rand -base64 24)"
echo "GoTTY password: ${GOTTY_PASSWORD}"
docker compose -f examples/basic-auth-shell.compose.yml up --build
```

Open <http://localhost:8989> and sign in with `gotty` and the generated password.

## 2. Read-only System Monitor

Share live output without letting viewers type into the terminal.

```console
docker compose -f examples/read-only-monitor.compose.yml up --build
```

Open <http://localhost:8990>. This runs `top` with `GOTTY_PERMIT_WRITE=false`.

## 3. Shared tmux Session

Let multiple browser clients attach to the same terminal session instead of spawning one shell per connection.

```console
export GOTTY_PASSWORD="$(openssl rand -base64 24)"
echo "GoTTY password: ${GOTTY_PASSWORD}"
docker compose -f examples/tmux-shared-session.compose.yml up --build
```

Open <http://localhost:8991>. Reconnects attach to the same `tmux` session.

## 4. Random URL

Add a generated path segment so the terminal is not discoverable at `/`.

```console
export GOTTY_PASSWORD="$(openssl rand -base64 24)"
echo "GoTTY password: ${GOTTY_PASSWORD}"
docker compose -f examples/random-url.compose.yml up --build
```

Watch the container logs for the generated URL, then open the printed address on port `8992`.

## 5. TLS

Run GoTTY directly with HTTPS. For public deployments, a reverse proxy such as Caddy, Traefik, or Nginx is usually cleaner.

```console
./examples/make-self-signed-cert.sh
export GOTTY_PASSWORD="$(openssl rand -base64 24)"
echo "GoTTY password: ${GOTTY_PASSWORD}"
docker compose -f examples/tls-self-signed.compose.yml up --build
```

Open <https://localhost:8993> and accept the local self-signed certificate warning.
