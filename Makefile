IMAGE ?= modenaf360/gotty-docker
LEGACY_IMAGE ?= modenaf360/gotty
GOTTY_VERSION ?= v1.8.0
UBUNTU_VERSION ?= ubuntu26.04
TAG ?= $(GOTTY_VERSION)-$(UBUNTU_VERSION)
PLATFORMS ?= linux/amd64,linux/arm64

.PHONY: build run push inspect help lint validate smoke

help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) \
		| sort \
		| awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-10s\033[0m %s\n", $$1, $$2}'

.DEFAULT_GOAL := help

build: ## Build the image with all local tags
	docker build \
		--build-arg GOTTY_VERSION=$(GOTTY_VERSION) \
		-t $(IMAGE):latest \
		-t $(IMAGE):$(TAG) \
		-t $(LEGACY_IMAGE):latest \
		-t $(LEGACY_IMAGE):$(TAG) \
		.

run: ## Run the image locally with Basic Auth (needs GOTTY_PASSWORD)
	docker run --rm -it \
		-p $${GOTTY_HOST_PORT:-8989}:8080 \
		-e GOTTY_USER=$${GOTTY_USER:-gotty} \
		-e GOTTY_PASSWORD=$${GOTTY_PASSWORD:?Set GOTTY_PASSWORD before running make run} \
		-e GOTTY_COMMAND="$${GOTTY_COMMAND:-/bin/bash -l}" \
		$(IMAGE):latest

push: ## Build and push multi-arch images to Docker Hub
	docker buildx build \
		--platform $(PLATFORMS) \
		--build-arg GOTTY_VERSION=$(GOTTY_VERSION) \
		-t $(IMAGE):latest \
		-t $(IMAGE):$(TAG) \
		-t $(LEGACY_IMAGE):latest \
		-t $(LEGACY_IMAGE):$(TAG) \
		--push \
		.

inspect: ## Inspect the multi-arch manifest of the latest image
	docker buildx imagetools inspect $(IMAGE):latest

lint: ## Lint the Dockerfile (hadolint) and shell scripts (shellcheck)
	docker run --rm -i hadolint/hadolint < Dockerfile
	docker run --rm -v "$(CURDIR):/mnt" -w /mnt koalaman/shellcheck:stable \
		run_gotty.sh examples/make-self-signed-cert.sh

validate: ## Validate every Compose file
	@status=0; \
	for f in docker-compose.yml examples/*.compose.yml; do \
		if GOTTY_PASSWORD=dummy docker compose -f "$$f" config -q; then \
			echo "OK: $$f"; \
		else \
			echo "FAIL: $$f"; status=1; \
		fi; \
	done; \
	exit "$$status"

smoke: build ## Build, then smoke test that auth is enforced
	docker run -d --name gotty-smoke -p 18989:8080 \
		-e GOTTY_USER=gotty -e GOTTY_PASSWORD=smoke-secret $(IMAGE):latest
	@sleep 4; \
	unauth="$$(curl -s -o /dev/null -w '%{http_code}' http://127.0.0.1:18989/ || true)"; \
	auth="$$(curl -s -o /dev/null -w '%{http_code}' -u gotty:smoke-secret http://127.0.0.1:18989/ || true)"; \
	docker rm -f gotty-smoke >/dev/null; \
	echo "Unauthenticated: $$unauth (expect 401), Authenticated: $$auth (expect 200)"; \
	[ "$$unauth" = "401" ] && [ "$$auth" = "200" ]
