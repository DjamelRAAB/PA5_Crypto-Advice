CURRENT_PATH := $(shell pwd)
SHELL := /bin/bash
VENV := .venv
BIN=$(CURRENT_PATH)/$(VENV)/bin/
IMAGE := cryptoadvice-scraper-price
REL := 0.0.1
TAG := $(REL)
DOCKER_REGISTRY := localhost
PA5_REGISTRY := gcr.io/pa5-crypto-advice2
IMAGE_VERSION := latest
FROM_IMAGE := $(IMAGE):$(IMAGE_VERSION)
APPLICATION_NAME := cryptoadvice-scraper-price

build:
	docker build --rm=true -t $(DOCKER_REGISTRY)/$(IMAGE):$(TAG) .
	
run_container: build
	docker run -d --name $(APPLICATION_NAME) -v $(CURRENT_PATH)/conf/:/conf -ti  $(DOCKER_REGISTRY)/$(IMAGE):$(TAG)

tag: build
	docker tag $(DOCKER_REGISTRY)/$(IMAGE):$(TAG) $(PA5_REGISTRY)/$(IMAGE):$(IMAGE_VERSION)

push: tag
	gcloud docker -- push $(PA5_REGISTRY)/$(IMAGE):$(IMAGE_VERSION)

clean:
	docker rmi $(DOCKER_REGISTRY)/$(IMAGE):$(TAG)