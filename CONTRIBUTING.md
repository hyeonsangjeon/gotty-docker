# Contributing to GoTTY Docker

Thanks for taking the time to contribute! This project keeps a small surface area
on purpose, so most changes are quick to review.

## Ways to help

- Report a bug or rough edge by opening an [issue](https://github.com/hyeonsangjeon/gotty-docker/issues).
- Suggest a new Compose example for a real-world GoTTY pattern.
- Improve the docs, security notes, or hardening defaults.
- Bump GoTTY or the Ubuntu base when a new version lands.

## Development setup

You need Docker (with Buildx) and, optionally, Python 3 for regenerating assets.

```console
git clone https://github.com/hyeonsangjeon/gotty-docker.git
cd gotty-docker

# Build the image
make build

# Run it locally (Basic Auth)
GOTTY_PASSWORD="$(openssl rand -base64 24)" make run
```

Open <http://localhost:8989> and sign in as `gotty`.

## Before you open a pull request

Please run the same checks CI runs:

```console
# Lint the Dockerfile
docker run --rm -i hadolint/hadolint < Dockerfile

# Lint the shell scripts
docker run --rm -v "$PWD:/mnt" -w /mnt koalaman/shellcheck:stable \
  run_gotty.sh examples/make-self-signed-cert.sh

# Validate every Compose file
for f in docker-compose.yml examples/*.compose.yml; do
  GOTTY_PASSWORD=dummy docker compose -f "$f" config -q && echo "OK: $f"
done

# Smoke test the built image
docker run -d --name gotty-smoke -p 18989:8080 \
  -e GOTTY_USER=gotty -e GOTTY_PASSWORD=secret modenaf360/gotty-docker:latest
sleep 4
curl -s -o /dev/null -w '%{http_code}\n' -u gotty:secret http://127.0.0.1:18989/  # expect 200
docker rm -f gotty-smoke
```

If you change `assets/`, regenerate the images instead of hand-editing them:

```console
python3 -m pip install pillow
python3 scripts/render_assets.py
```

## Pull request checklist

- [ ] `hadolint` and `shellcheck` pass.
- [ ] Every Compose file still validates.
- [ ] The image builds and serves a terminal locally.
- [ ] Docs (README/examples) updated when behavior changes.
- [ ] Commits are focused and described in plain language.

## Commit and branch style

- Branch from `master` with a short, kebab-case name (`fix-tls-example`).
- Write imperative commit subjects (`Add reverse proxy example`).
- Keep unrelated changes in separate pull requests.

## Code of Conduct

By participating you agree to uphold our
[Code of Conduct](CODE_OF_CONDUCT.md).
