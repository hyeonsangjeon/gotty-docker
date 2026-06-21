#!/usr/bin/env bash
set -euo pipefail

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cert_dir="${script_dir}/certs"

mkdir -p "$cert_dir"

openssl req \
  -x509 \
  -nodes \
  -newkey rsa:2048 \
  -days 30 \
  -keyout "${cert_dir}/gotty.key" \
  -out "${cert_dir}/gotty.crt" \
  -subj "/CN=localhost" \
  -addext "subjectAltName=DNS:localhost,IP:127.0.0.1"

chmod 0600 "${cert_dir}/gotty.key"
chmod 0644 "${cert_dir}/gotty.crt"

echo "Wrote ${cert_dir}/gotty.crt and ${cert_dir}/gotty.key"
