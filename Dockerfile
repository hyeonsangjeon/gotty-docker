FROM ubuntu:26.04

ARG GOTTY_VERSION=v1.8.0
ARG TARGETARCH

LABEL maintainer="hyeonsangjeon" \
      org.opencontainers.image.title="gotty-docker" \
      org.opencontainers.image.description="A modern GoTTY web terminal container with optional Basic Auth." \
      org.opencontainers.image.source="https://github.com/hyeonsangjeon/gotty-docker" \
      org.opencontainers.image.licenses="MIT"

ENV LANG=C.UTF-8 \
    LC_ALL=C.UTF-8 \
    GOTTY_ADDRESS=0.0.0.0 \
    GOTTY_PORT=8080 \
    GOTTY_PERMIT_WRITE=true \
    GOTTY_RECONNECT=true \
    GOTTY_TITLE_FORMAT="GoTTY Docker" \
    GOTTY_COMMAND="/bin/bash -l" \
    SHELL=/bin/bash

RUN set -eux; \
    export DEBIAN_FRONTEND=noninteractive; \
    apt-get update; \
    apt-get install -y --no-install-recommends \
        bash \
        ca-certificates \
        curl \
        less \
        nano \
        procps \
        sudo \
        tmux; \
    rm -rf /var/lib/apt/lists/*

RUN set -eux; \
    case "${TARGETARCH:-amd64}" in \
        amd64) gotty_arch="amd64" ;; \
        arm64) gotty_arch="arm64" ;; \
        arm) gotty_arch="arm" ;; \
        *) echo "Unsupported TARGETARCH: ${TARGETARCH}" >&2; exit 1 ;; \
    esac; \
    asset="gotty_${GOTTY_VERSION}_linux_${gotty_arch}.tar.gz"; \
    base_url="https://github.com/sorenisanerd/gotty/releases/download/${GOTTY_VERSION}"; \
    curl -fsSLO "${base_url}/SHA256SUMS"; \
    curl -fsSLO "${base_url}/${asset}"; \
    grep "  ${asset}$" SHA256SUMS | sha256sum -c -; \
    tar -xzf "${asset}" -C /usr/local/bin ./gotty; \
    chmod 0755 /usr/local/bin/gotty; \
    rm -f "${asset}" SHA256SUMS

COPY run_gotty.sh /usr/local/bin/run_gotty.sh
RUN chmod 0755 /usr/local/bin/run_gotty.sh

EXPOSE 8080

HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
    CMD scheme="http"; curl_args="-sS"; [ "${GOTTY_TLS:-false}" = "true" ] && scheme="https" && curl_args="-k -sS"; status="$(curl $curl_args -o /dev/null -w '%{http_code}' "${scheme}://127.0.0.1:${GOTTY_PORT:-8080}/" || true)"; [ "$status" = "200" ] || [ "$status" = "401" ]

CMD ["/usr/local/bin/run_gotty.sh"]
