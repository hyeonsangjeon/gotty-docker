IMAGE ?= modenaf360/gotty-docker
LEGACY_IMAGE ?= modenaf360/gotty
GOTTY_VERSION ?= v1.8.0
UBUNTU_VERSION ?= ubuntu26.04
TAG ?= $(GOTTY_VERSION)-$(UBUNTU_VERSION)
PLATFORMS ?= linux/amd64,linux/arm64

.PHONY: build run push inspect

build:
	docker build \
		--build-arg GOTTY_VERSION=$(GOTTY_VERSION) \
		-t $(IMAGE):latest \
		-t $(IMAGE):$(TAG) \
		-t $(LEGACY_IMAGE):latest \
		-t $(LEGACY_IMAGE):$(TAG) \
		.

run:
	docker run --rm -it \
		-p $${GOTTY_HOST_PORT:-8989}:8080 \
		-e GOTTY_USER=$${GOTTY_USER:-gotty} \
		-e GOTTY_PASSWORD=$${GOTTY_PASSWORD:?Set GOTTY_PASSWORD before running make run} \
		-e GOTTY_COMMAND="$${GOTTY_COMMAND:-/bin/bash -l}" \
		$(IMAGE):latest

push:
	docker buildx build \
		--platform $(PLATFORMS) \
		--build-arg GOTTY_VERSION=$(GOTTY_VERSION) \
		-t $(IMAGE):latest \
		-t $(IMAGE):$(TAG) \
		-t $(LEGACY_IMAGE):latest \
		-t $(LEGACY_IMAGE):$(TAG) \
		--push \
		.

inspect:
	docker buildx imagetools inspect $(IMAGE):latest
