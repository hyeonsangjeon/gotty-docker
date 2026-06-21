#!/usr/bin/env bash
set -euo pipefail

: "${GOTTY_COMMAND:=/bin/bash -l}"

gotty_args=()

read_secret_file() {
  local file_path="$1"

  if [[ ! -r "$file_path" ]]; then
    echo "Cannot read secret file: $file_path" >&2
    exit 64
  fi

  IFS= read -r secret_value < "$file_path"
  printf '%s' "$secret_value"
}

if [[ -n "${GOTTY_CREDENTIAL_FILE:-}" ]]; then
  GOTTY_CREDENTIAL="$(read_secret_file "$GOTTY_CREDENTIAL_FILE")"
fi

if [[ -n "${GOTTY_PASSWORD_FILE:-}" ]]; then
  GOTTY_PASSWORD="$(read_secret_file "$GOTTY_PASSWORD_FILE")"
fi

if [[ -n "${GOTTY_CREDENTIAL:-}" ]]; then
  gotty_args+=(--credential "$GOTTY_CREDENTIAL")
elif [[ -n "${GOTTY_USER:-}" || -n "${GOTTY_PASSWORD:-}" ]]; then
  if [[ -z "${GOTTY_USER:-}" || -z "${GOTTY_PASSWORD:-}" ]]; then
    echo "Set both GOTTY_USER and GOTTY_PASSWORD, or use GOTTY_CREDENTIAL=user:password." >&2
    exit 64
  fi

  gotty_args+=(--credential "${GOTTY_USER}:${GOTTY_PASSWORD}")
else
  echo "Warning: GoTTY is starting without Basic Auth. Set GOTTY_USER and GOTTY_PASSWORD before exposing this container." >&2
fi

exec /usr/local/bin/gotty "${gotty_args[@]}" /bin/bash -lc "$GOTTY_COMMAND"
